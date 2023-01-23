---
layout: default
title: "DEF's used"
parent: "Area Sources"
grand_parent: TEDS Python
nav_order: 3
date:               
last_modified_date:   2021-12-01 14:16:46
tags: TEDS
---

# 面源計算用到的副程式
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景
- 為消除資料庫在時間與空間的相依性，需要消除資料庫**類別-縣市**之維度，此處即針對面源的**時間變異係數與類別-縣市之對照表**(`nc_fac.json`)進行計算，以備未來套用。主要問題出現在環保署提供的**時變係數檔**，空間資料為**中文名稱**，與主資料庫是鄉鎮區代碼**2碼編號**不能對應，分3個程式說明：
  - 時間變異係數(`csv`)檔案前處理
  - `csv`檔案之產生
  - 將`csv`檔案應用到面源排放量資料庫，並展開至全年逐時之序列，存成`nc_fac.json`。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/#處理程序總綱)、針對[面源之處理](https://sinotec2.github.io/jFocus-on-Air-Quality/EmisProc/area/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)與[重新計算網格座標](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/prep_areagridLL/)，為此處之前處理。  

## 程式說明

### 引用模組及時間標籤轉換`dt2jul`, `jul2dt`
- `m3.nc`檔案的時間標籤`TFLAG`是個整數的序列`jul`，而為能計算，需轉成`datetime`。

```python
kuang@114-32-164-198 /Users/TEDS/teds10_camx/HourlyWeighted/area
$ cat -n include3.py 
     1	import numpy as np
     2	from pandas import *
     3	import sys, os, subprocess
     4	import netCDF4
     5	from datetime import datetime, timedelta
     6	import twd97
     7	from include2 import rd_ASnPRnCBM_A
     8	
     9	def dt2jul(dt):
    10	  yr=dt.year
    11	  deltaT=dt-datetime(yr,1,1)
    12	  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
    13	  return (yr*1000+deltaT.days+1,deltaH*10000)
    14	
    15	def jul2dt(jultm):
    16	  jul,tm=jultm[:]
    17	  yr=int(jul/1000)
    18	  ih=int(tm/10000.)
    19	  return datetime(yr,1,1)+timedelta(days=int(jul-yr*1000-1))+timedelta(hours=ih)
    20	
```

### 資料庫的網格化`disc`
- 座標軸中心點(`Xcent`,`Ycent`)、轉成`nc`檔案的`IX`、`IY`標籤
- 使用`pivot_table`加總，會自動啟動平行化作業。

```python
    21	def disc(dm,nc):
    22	#discretizations
    23	  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
    24	  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    25	  dm['IX']=np.array((dm.UTME-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
    26	  dm['IY']=np.array((dm.UTMN-Ycent-nc.YORIG)/nc.YCELL,dtype=int)
    27	  #time_const or time_variant df files
    28	  if 'JJJHH' not in dm.columns:
    29	    dmg=pivot_table(dm,index=['nsc2','IX','IY'],values=cole,aggfunc=sum).reset_index()
    30	  else:
    31	    dmg=pivot_table(dm,index=['IX','IY','JJJHH'],values=cole,aggfunc=sum).reset_index()
    32	  return dmg
    33	
```

### PM成份劃分
- 理論上PM的劃分也應從[SPECIATE](https://www.epa.gov/air-emissions-modeling/speciate-4)資料庫來，但目前本程式尚未引用，只有CCRS、FCRS、CPRM、FPRM 4項。只用簡單邏輯的劃分：
  - 如果是燃燒源(C+N+S) > 0：所有細顆粒都是FPRM、PM-PM25則為CPRM
  - 如果非燃燒源(C+N+S) == 0 且 V==0： 所有細顆粒都是FCRS、PM-PM25則為CCRS
  - 如果非燃燒源且為VOC逸散源(事實上無PM排放，但還是留下邏輯)：一半為CRS、一半為PRM， 粗細皆同

```python
    34	#A simple scheme is in place for PM splitting, and the SPECCIATE is not adopted.
    35	def add_PMS(dm):
    36	  #add the PM columns and reset to zero
    37	  colc=['CCRS','FCRS','CPRM','FPRM']
    38	  for c in colc:
    39	    dm[c]=np.zeros(len(dm))
    40	  #in case of non_PM sources, skip the routines
    41	  if 'EM_PM' not in dm.columns or sum(dm.EM_PM)==0:return dm
    42	  # fugitive sources
    43	  not_burn=dm.loc[dm.EM_NOX+dm.EM_CO+dm.EM_SOX==0]
    44	  crst=not_burn.loc[not_burn.EM_PM>0]
    45	  idx=crst.index
    46	  dm.loc[idx,'FCRS']=np.array(crst.EM_PM25)
    47	  dm.loc[idx,'CCRS']=np.array(crst.EM_PM)-np.array(crst.EM_PM25)
    48	  # combustion sources allocated into ?PRM, not PEC or POA
    49	  burn=dm.loc[(dm.EM_NOX+dm.EM_CO+dm.EM_SOX)>0]
    50	  prim=burn.loc[burn.EM_PM>0]
    51	  idx=prim.index
    52	  dm.loc[idx,'FPRM']=np.array(prim.EM_PM25)
    53	  dm.loc[idx,'CPRM']=np.array(prim.EM_PM)-np.array(prim.EM_PM25)
    54	  # check for left_over sources(NMHC fugitives), in fact no PM emits at all
    55	  boo=(dm.EM_PM!=0) & ((dm.CCRS+dm.FCRS+dm.CPRM+dm.FPRM)==0)
    56	  idx=dm.loc[boo].index
    57	  if len(idx)!=0:
    58	    res=dm.loc[idx]
    59	    dm.loc[idx,'FPRM']=np.array(res.EM_PM25)/2
    60	    dm.loc[idx,'FCRS']=np.array(res.EM_PM25)/2
    61	    dm.loc[idx,'CPRM']=(np.array(res.EM_PM)-np.array(res.EM_PM25))/2.
    62	    dm.loc[idx,'CCRS']=(np.array(res.EM_PM)-np.array(res.EM_PM25))/2.
    63	  return dm
    64	
```

### VOCs成分劃分
- VOC成份劃分的方式
    - 為污染源類別的特性，這個特性的對照關係在ASSIGN-A.TXT(df_asgn)中設定，
    - 如果要修改、進版，只需要依據最新的SPECIATE資料庫內容，修正這個對照關係即可。
- VOC成份與模式模擬成份的對照關係
    - 與所選取的光化機制有關，這個對照關係需要2個對照表，
        - 一者是V_PROFIL.TXT(df_prof)，這個檔案也是SPECIATE資料庫的內容，
        - 另一個是CBM.DAT(BASE)這是碳鍵機制的制式表格，與碳鍵機制版本有關。
- profile number
    - 由於PRO_NO的個數有限，沒有必要臨時再計算累加各物質碳鍵，
    - 可以事先準備好，做好對照關係(prof_cbm)，
    - 計算時只要叫出PRO_NO對照到的(每單位重量)碳鍵莫耳數(prod)，直接與排放量相乘即可。

```python
    65	def add_VOC(dm,n):
    66	  df_asgn,df_prof,df_cbm=rd_ASnPRnCBM_A()
    67	  df_asgn.NSC=[i.strip() for i in df_asgn.NSC]
    68	  MW={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['MW']))}
    69	  BASE={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['BASE']))}
    70	  colv='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
    71	  NC=len(colv)
    72	  try:
    73	    prof_cbm=read_csv('prof_cbm.csv')
    74	    prof_cbm.PRO_NO=['{:04d}'.format(m) for m in prof_cbm.PRO_NO]
    75	  except:
    76	    HC=1
    77	    prof_cbm=DataFrame({})
    78	    prof_cbm['PRO_NO']=list(set(df_prof.PRO_NO))
    79	    for c in colv:
    80	      prof_cbm[c]=0.
    81	    for i in range(len(prof_cbm)):
    82	      prof=prof_cbm.PRO_NO[i]
    83	      spec=df_prof.loc[df_prof.PRO_NO==prof].reset_index(drop=True)
    84	      for K in range(len(spec)):
    85	        W_K_II,IS=spec.WT[K],spec.SPE_NO[K]
    86	        if W_K_II==0.0 or sum(BASE[IS])==0.0:continue
    87	        VOCwt=HC*W_K_II/100. #in T/Y
    88	        VOCmole=VOCwt/MW[IS] #in Tmole/Y
    89	        for LS in range(NC): #CBM molar ratio
    90	          if BASE[IS][LS]==0.:continue
    91	          prof_cbm.loc[i,colv[LS]]+=VOCmole*BASE[IS][LS]
    92	    prof_cbm.set_index('PRO_NO').to_csv('prof_cbm.csv')
    93	
    94	  #matching the category profile number
    95	  if n not in set(df_asgn.NSC):sys.exit('nsc not assigned: '+n)
    96	  prof=df_asgn.loc[df_asgn.NSC==n,'PRO_NO'].values[0]
    97	  if prof not in set(prof_cbm.PRO_NO):sys.exit('prof not found: '+prof)
    98	  prod=prof_cbm.loc[prof_cbm.PRO_NO==prof].iloc[0,1:]
    99	  HC=dm.loc[dm.nsc2==n,'EM_NMHC']
   100	  idx=HC.index
   101	  for LS in range(NC): #CBM molar ratio
   102	    dm.loc[idx,colv[LS]]=HC*prod[LS]
   103	  return dm
   104	
```

### VOCs資料庫之讀取`rd_ASnPRnCBM_A`
- 來自[include2.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/include2.py)

```python
   102	def rd_ASnPRnCBM_A():
   103	    from pandas import DataFrame, read_csv
   104	    import subprocess
   105	    ROOT='/'+subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
   106	    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/area/ASSIGN-A.TXT'
   107	    df_asgn=read_csv(fname,header=None,delim_whitespace = True)
   108	    df_asgn.columns=['NSC','PRO_NO']+[str(i) for i in range(len(df_asgn.columns)-2)]
   109	    df_asgn.fillna(0,inplace=True)
   110	    df_asgn.PRO_NO=['{:04d}'.format(int(m)) for m in df_asgn.PRO_NO]
   111	    for i in range(len(df_asgn)):
   112	        nsc=df_asgn.NSC[i]
   113	        if not nsc[-1].isalpha():
   114	            df_asgn.loc[i,'NSC']=nsc.strip()+'b'                
   115	    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/area/V_PROFIL.TXT'
   116	    with open(fname) as text_file:
   117	        d=[line[:41] for line in text_file]
   118	    PRO_NO,SPE_NO,WT=[i[:4] for i in d],[int(i[11:14]) for i in d],[float(i[24:30]) for i in d]
   119	    df_prof=DataFrame({'PRO_NO':PRO_NO,'SPE_NO':SPE_NO,'WT':WT})
   120	    NC=20
   121	    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/line/CBM.DAT'
   122	    with open(fname) as text_file:
   123	        d=[line.strip('\n') for line in text_file]
   124	    d=d[1:]
   125	    SPE_NO,MW=[int(i[41:44]) for i in d],[float(i[57:63]) for i in d]
   126	    BASE=[[i[63+j*6:63+(j+1)*6] for j in range(NC)] for i in d]
   127	    d=BASE
   128	    for i in range(len(d)):
   129	        ii=d[i]
   130	        for j in range(NC):
   131	            s=ii[j].strip(' ')
   132	            if len(s)==0:
   133	                BASE[i][j]=0.
   134	            else:
   135	                BASE[i][j]=float(s)
   136	    df_cbm=DataFrame({'SPE_NO':SPE_NO,'MW':MW,'BASE':BASE})
   137	    return (df_asgn,df_prof,df_cbm)
   138	
```

### mostfreqword
- 序列中最常使用到的字串，作為`pivot_table`的`aggfunc`

```python
def compareItems(wc1,wc2):
    (w1,c1), (w2,c2)=wc1,wc2
    if c1 > c2:
        return - 1
    elif c1 == c2:
        return cmp(w1, w2)
    else:
        return 1
def mostfreqword(list_of_w):
    counts = {}
    for w in list_of_w:
        counts[w] = counts.get(w,0) + 1
    it=sorted(counts.items(),reverse=False)
    return it[0][0]
def mostfreq10word(list_of_w):
    if len(list_of_w)<10: 
        return []
    counts = {}
    for w in list_of_w:
        counts[w] = counts.get(w,0) + 1
    it=sorted(counts.items(),reverse=True)
#p2    it=compareItems(it)
#p2    it=counts.items()
#p2    it.sort(compareItems)
    return [(it[x][0],it[x][1]) for x in xrange(10)]
```

## 檔案下載

{% include download.html content="python程式：[include2.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/include2.py)" %}

## Reference
