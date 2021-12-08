---
layout: default
title: "Elev. PTse for CAMx"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 3
date:               
last_modified_date:   2021-12-06 12:09:47
---

# CAMx高空點源排放檔案之產生
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
- 此處處理TEDS PM/VOCs年排放量之劃分、與時變係數相乘、整併到光化模式網格系統內。
- 高空點源的**時變係數**檔案需按CEMS數據先行[展開](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptseE_ONS/)。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/)中的副程式

## 副程式說明

### [ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/)

### 對煙道座標進行叢集整併
如題所示。整併的理由有幾：
- 鄰近煙流在近距離重疊後，會因整體煙流熱量的提升而提升其最終煙流高度，從而降低對地面的影響，此一現象並未在模式的煙流次網格模式中予以考量，須在模式外先行處理。
- 重複計算較小煙流對濃度沒有太大的影響，卻耗費大量儲存、處理的電腦資源，因此整併有其必須性。
  - 即使將較小的點源按高度切割併入面源，還是保留此一機制，以避免點源個數無限制擴張，有可能放大因品質不佳造成奇異性。

#### cluster_xy
- 調用`sklearn`之`KMeans`來做叢集分析

```python
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n cluster_xy.py
     1
     2
     3  def cluster_xy(df,C_NO):
     4    from sklearn.cluster import KMeans
     5    from pandas import DataFrame
     6    import numpy as np
     7    import sys
     8
```
- 由資料庫中選擇同一**管編**之煙道出來

```python
     9    b=df.loc[df.CP_NO.map(lambda x:x[:8]==C_NO)]
    10    n=len(b)
    11    if n==0:sys.exit('fail filtering of '+C_NO)
    12    colb=b.columns
```
- 此**管編**所有煙道的座標及高度，整併為一個大矩陣
  - 進行KMeans叢集分析

```python
    13    x=[b.XY[i][0] for i in b.index]
    14    y=[b.XY[i][1] for i in b.index]
    15    z=b.HEI
    16    M=np.array([x, y, z]).T
    17    clt = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300, \
    18         n_clusters=10, n_init=10, n_jobs=-1, precompute_distances='auto', \
    19         random_state=None, tol=0.0001, verbose=0)
    20    kmeans=clt.fit(M)
```
- 放棄原來的座標，改採叢集的平均位置

```python
    21  #  np.array(clt.cluster_centers_) for group
    22    b_lab=np.array(clt.labels_)
    23    df.loc[b.index,'UTM_E']=[np.array(clt.cluster_centers_)[i][0] for i in b_lab]
    24    df.loc[b.index,'UTM_N']=[np.array(clt.cluster_centers_)[i][1] for i in b_lab]
    25    return df
    26
```
#### XY_pivot
- 工廠點源個數太多者(如中鋼)，在座標叢集化之前，以pivot_tab取其管道(**管煙**編號=**管編**+**煙編**)排放量之加總值
  - 調用模組

```python   
    27  #XY clustering in CSC before pivotting
    28  #df=cluster_xy(df,'E5600841')
    29  #pivotting
    30  def XY_pivot(df,col_id,col_em,col_mn,col_mx):
    31    from pandas import pivot_table,merge
    32    import numpy as np
```
- 3類不同屬性欄位適用不同的`aggfunc`
  - 排放量(`col_em`)：加總
  - 煙道高度(`col_mx`)：最大值
  - 煙道其他參數(`col_mn`)：平均

```python   
    33    df_pv1=pivot_table(df,index=col_id,values=col_em,aggfunc=np.sum).reset_index()
    34    df_pv2=pivot_table(df,index=col_id,values=col_mn,aggfunc=np.mean).reset_index()
    35    df_pv3=pivot_table(df,index=col_id,values=col_mx,aggfunc=max).reset_index()
```
- 整併、求取等似直徑、以使流量能守恒

```python   
    36    df1=merge(df_pv1,df_pv2,on=col_id)
    37    df=merge(df1,df_pv3,on=col_id)
    38    df['DIA']=[np.sqrt(4/3.14159*q/60*(t+273)/273/v) for q,t,v in zip(df.ORI_QU1,df.TEMP,df.VEL)]
    39    return df
```

## 主程式說明

### 程式之執行
- 此處按月執行。由於nc檔案時間展開後，檔案延長非常緩慢，拆分成主程式（`ptseE.py`）與輸出程式（`wrtE.py`）二段進行。

```bash
for m in 0{1..9} 1{0..2};do python ptseE.py 19$m;done
for m in 0{1..9} 1{0..2};do python wrtE.py 19$m;done
```

### 程式基本定義、資料庫檔案QC、nc檔案之延展
- 調用模組
  - 因無另存處理過後的資料庫，因此程式還是會用到[ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/)中的副程式`CORRECT`, `add_PMS`, `check_nan`, `check_landsea`, `FillNan`, `WGS_TWD`, `Elev_YPM`

```python   
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n ptseE.py
     1
     2  #! crding = utf8
     3  from pandas import *
     4  import numpy as np
     5  import os, sys, subprocess
     6  import netCDF4
     7  import twd97
     8  import datetime
     9  from calendar import monthrange
    10  from scipy.io import FortranFile
    11
    12  from mostfreqword import mostfreqword
    13  from ptse_sub import CORRECT, add_PMS, check_nan, check_landsea, FillNan, WGS_TWD, Elev_YPM
    14  from ioapi_dates import jul2dt, dt2jul
    15  from cluster_xy import cluster_xy, XY_pivot
    16
```
- 程式相依性及年月定義(由引數)
  - `pncgen`、`ncks`是在`wrtE.py`階段使用

```python   
    17  #Main
    18  #locate the programs and root directory
    19  pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
    20  ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
    21  hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
    22  P='./'
    23
    24  #time and space initiates
    25  ym=sys.argv[1]
    26  mm=ym[2:4]
    27  mo=int(mm)
    28  yr=2000+int(ym[:2]);TEDS='teds'+str((yr-2016)/3+10)
```
- 使用`Hs`進行篩選「高空」點源

```python   
    29  Hs=10 #cutting height of stacks
```
- 起迄日期、模擬範圍中心點位置
 
```python   
    30  ntm=(monthrange(yr,mo)[1]+2)*24+1
    31  bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
    32  edate=bdate+datetime.timedelta(days=ntm/24)#monthrange(yr,mo)[1]+3)
    33  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
    34  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
```
- nc模版的應用與延展。注意`name`在新版`NCF`可能會被保留不能更改。(另在`CAMx`程式碼中處理)

```python   
    35  #prepare the uamiv template
    36  print('template applied')
    37  NCfname='fortBE.413_'+TEDS+'.ptsE'+mm+'.nc'
    38  try:
    39    nc = netCDF4.Dataset(NCfname, 'r+')
    40  except:
    41    os.system('cp '+P+'template_v7.nc '+NCfname)
    42    nc = netCDF4.Dataset(NCfname, 'r+')
    43  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    44  nt,nv,dt=nc.variables[V[2][0]].shape
    45  nv=len([i for i in V[1] if i !='CP_NO'])
    46  nc.SDATE,nc.STIME=dt2jul(bdate)
    47  nc.EDATE,nc.ETIME=dt2jul(edate)
    48  nc.NOTE='Point Emission'
    49  nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
    50  nc.NVARS=nv
    51  #Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
    52  #nc.name='PTSOURCE  '
    53  nc.NSTEPS=ntm
    54  if 'ETFLAG' not in V[2]:
    55    zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
    56  if nt!=ntm or (nc.variables['TFLAG'][0,0,0]!=nc.SDATE and nc.variables['TFLAG'][0,0,1]!=nc.STIME):
    57    for t in range(ntm):
    58      sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
    59      nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    60      nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    61      ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
    62      nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    63      nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
    64  nc.close()
    65  #template OK
    66
```
- 污染物名稱對照、變數群組定義

```python   
    67  #item sets definitions
    68  c2s={'NMHC':'NMHC','SOX':'SO2','NOX':'NO2','CO':'CO','PM':'PM'}
    69  c2m={'SOX':64,'NOX':46,'CO':28,'PM':1}
    70  cole=[i+'_EMI' for i in c2s]+['PM25_EMI']
    71  XYHDTV=['UTM_E','UTM_N','HEI','DIA','TEMP','VEL']
    72  colT=['HD1','DY1','HY1']
    73  colc=['CCRS','FCRS','CPRM','FPRM']
    74
```
- 讀取點源資料庫並進行品質管控。新版`coding`只接受`big5`

```python   
    75  #Input the TEDS csv file
    76  try:
    77    df = read_csv('point.csv', encoding='utf8')
    78  except:
    79    df = read_csv('point.csv')
    80  df = check_nan(df)
    81  df = check_landsea(df)
    82  df = WGS_TWD(df)
    83  df = Elev_YPM(df)
    84  #only P??? an re tak einto account
    85  boo=(df.HEI>=Hs) & (df.NO_S.map(lambda x:x[0]=='P'))
    86  df=df.loc[boo].reset_index(drop=True)
    87  #delete the zero emission sources
    88  df['SUM']=[i+j+k+l+m for i,j,k,l,m in zip(df.SOX_EMI,df.NOX_EMI,df.CO_EMI,df.PM_EMI,df.NMHC_EMI)]
    89  df=df.loc[df.SUM>0].reset_index(drop=True)
    90  df['DY1']=[i*j for i,j in zip(df.DW1,df.WY1)]
    91  df['HY1']=[i*j for i,j in zip(df.HD1,df.DY1)]
    92  df=CORRECT(df)
    93  df['CP_NO'] = [i + j for i, j in zip(list(df['C_NO']), list(df['NO_S']))]
    94
    95  #
```
- 座標轉換

```python   
    96  #Coordinate translation
    97  df.UTM_E=df.UTM_E-Xcent
    98  df.UTM_N=df.UTM_N-Ycent
    99  df.SCC=[str(int(i)) for i in df.SCC]
   100  df.loc[df.SCC=='0','SCC']='0'*10
```
- 對**管煙**編號進行資料庫重整
  - 3類不同屬性欄位適用不同的`aggfunc`
    - 排放量(`col_em`)：加總
    - 煙道高度(`col_mx`)：最大值
    - 煙道其他參數(`col_mn`)：平均

```python   
   101  #pivot table along the dimension of NO_S (P???)
   102  df_cp=pivot_table(df,index='CP_NO',values=cole+['ORI_QU1'],aggfunc=sum).reset_index()
   103  df_xy=pivot_table(df,index='CP_NO',values=XYHDTV+colT,aggfunc=np.mean).reset_index()
   104  df_sc=pivot_table(df,index='CP_NO',values='SCC', aggfunc=mostfreqword).reset_index()
   105  df1=merge(df_cp,df_xy,on='CP_NO')
   106  df=merge(df1,df_sc,on='CP_NO')
```
- 排放量單位轉換
  - 因小時數在`ons`中已經應用了(個別煙道加總為1.)，因此只需考量重量之轉換即可。
  - 留下之前計算版本，以供對照

```python   
   107  #T/year to g/hour
   108  for c in cole:
   109    df[c]=[i*1E6 for i in df[c]]
   110  #  df[c]=[i*1E6/j/k for i,j,k in zip(df[c],df.DY1,df.HD1)]
```
- CAMx版本差異在此選擇
  - 6~7版的差異可以參考[CMAQ/CAMx排放量檔案之轉換](http://www.evernote.com/l/AH1z_n2U--lM-poNlQnghsjFBfDEY6FalgM/)，
  - 如要做不同版本，應重新準備模版階段

```python   
   111  #determination of camx version
   112  ver=7
   113  if 'XSTK' in V[0]:ver=6
   114  print('NMHC/PM splitting and expanding')
```

### VOCs與PM的劃分
- 讀取profile number、preference table

```python   
   114  print('NMHC/PM splitting and expanding')
   115  #prepare the profile and CBMs
   116  fname='/'+hmp+'/SMOKE4.5/data/ge_dat/gsref.cmaq_cb05_soa.txt'
   117  gsref=read_csv(fname,delimiter=';',header=None)
   118  col='SCC Speciation_profile_number Pollutant_ID'.split()+['C'+str(i) for i in range(3,10)]
   119  gsref.columns=col
   120  for c in col[3:]:
   121    del gsref[c]
   122  fname='/'+hmp+'/SMOKE4.5/data/ge_dat/gspro.cmaq_cb05_soa.txt'
   123  gspro=read_csv(fname,delimiter=';',header=None)
   124  col=['Speciation_profile_number','Pollutant_ID','Species_ID','Split_factor','Divisor','Mass_Fraction']
   125  gspro.columns=col
```
- 自從TEDS9之後，國內新增(或修正)很多資料庫中沒有的SCC。此處以對照既有SCC碼簡單處理。
  - 對照方式：網站上找到最新的SCC資料庫，找到新SCC的製程類別特性
  - 找到既有SCC profile number資料表中，前幾碼(4~6)相同的SCC，如果類似就指定取代
  - 如果真的找不到，也只能找數字最接近的取代

```python   
   126  #new SCC since TEDS9,erase and substude
   127  sccMap={
   128  '30111103':'30111199', #not in df_scc2
   129  '30112401':'30112403', #Industrial Processes  Chemical Manufacturing  Chloroprene Chlorination Reactor
   130  '30115606':'30115607',#Industrial Processes  Chemical Manufacturing  Cumene  Aluminum Chloride Catalyst Process: DIPB Strip
   131  '30118110':'30118109',#Industrial Processes  Chemical Manufacturing  Toluene Diisocyanate  Residue Vacuum Distillation
   132  '30120554':'30120553', #not known, 548~  Propylene Oxide Mixed Hydrocarbon Wash-Decant System Vent
   133  '30117410':'30117421',
   134  '30117411':'30117421',
   135  '30117614':'30117612',
   136  '30121125':'30121104',
   137  '30201111':'30201121',
   138  '30300508':'30300615',
   139  '30301024':'30301014',
   140  '30400213':'30400237',
   141  '30120543':'30120502',
   142  '40300215':'40300212'} #not known
   143  for s in sccMap:
   144    df.loc[df.SCC==s,'SCC']=sccMap[s]   
```
- 只篩選有關的SCC以縮減資料庫長度、提升對照速度
  - 因有些profile number含有英文字，在此先做整理，以使格式一致

```python   
   145  #reduce gsref and gspro
   146  dfV=df.loc[df.NMHC_EMI>0].reset_index(drop=True)
   147  gsrefV=gsref.loc[gsref.SCC.map(lambda x:x in set(dfV.SCC))].reset_index(drop=True)
   148  prof_alph=set([i for i in set(gsrefV.Speciation_profile_number) if i.isalpha()])
   149  gsrefV=gsrefV.loc[gsrefV.Speciation_profile_number.map(lambda x:x not in prof_alph)].reset_index(drop=True)
   150  gsproV=gspro.loc[gspro.Speciation_profile_number.map(lambda x:x in set(gsrefV.Speciation_profile_number))].reset_index(drop=True)
```
- 只篩選有關的profile number且污染物含有`TOG`者

```python   
   151  pp=[]
   152  for p in set(gspro.Speciation_profile_number):
   153    a=gsproV.loc[gsproV.Speciation_profile_number==p]
   154    if 'TOG' not in set(a.Pollutant_ID):pp.append(p)
   155  boo=(gspro.Speciation_profile_number.map(lambda x:x not in pp)) & (gspro.Pollutant_ID=='TOG')
   156  gsproV=gspro.loc[boo].reset_index(drop=True)
   157
```
- 準備乘數矩陣，其大小為`(SCC總數,CBM物質項目總數)`

```python   
   158  cbm=list(set([i for i in set(gsproV.Species_ID) if i in V[1]]))
   159  idx=gsproV.loc[gsproV.Species_ID.map(lambda x:x in cbm)].index
   160  sccV=list(set(dfV.SCC))
   161  sccV.sort()
   162  nscc=len(sccV)
   163  prod=np.zeros(shape=(nscc,len(cbm)))
```
- 對得到SCC，但是資料庫中卻沒有`TOG`也沒有`VOC`。記下、執行下個SCC

```python   
   164  #dfV but with PM scc(no TOG/VOC in gspro), modify those SCC to '0'*10 in dfV, drop the pro_no in gsproV
   165  noTOG_scc=[]
   166  for i in range(nscc):
   167    s=sccV[i]
   168    p=list(gsrefV.loc[gsrefV.SCC==s,'Speciation_profile_number'])[0]
   169    a=gsproV.loc[gsproV.Speciation_profile_number==p]
   170    if 'TOG' not in set(a.Pollutant_ID) and 'VOC' not in set(a.Pollutant_ID):
   171      noTOG_scc.append(s)
   172      continue
```
- 找到對應的profile number，將分率存入乘數矩陣`prod`

```python   
   173    boo=(gsproV.Speciation_profile_number==p) & (gsproV.Pollutant_ID=='TOG')
   174    a=gsproV.loc[boo]
   175    for c in a.Species_ID:
   176      if c not in cbm:continue
   177      j=cbm.index(c)
   178      f=a.loc[a.Species_ID==c,'Mass_Fraction']
   179      d=a.loc[a.Species_ID==c,'Divisor']
   180      prod[i,j]+=f/d
```
- `NMHC_EMI`排放量乘上乘數矩陣，形成`CBM`排放量

```python   
   181  df.loc[df.SCC.map(lambda x:x in noTOG_scc),'SCC']='0'*10
   182  for c in cbm:
   183    df[c]=0.
   184  for s in set(dfV.SCC):
   185    i=sccV.index(s)
   186    idx=df.loc[df.SCC==s].index
   187    for c in cbm:
   188      j=cbm.index(c)
   189      df.loc[idx,c]=[prod[i,j]*k for k in df.loc[idx,'NMHC_EMI']]
```
- PM的劃分，詳見[ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/#%E7%B0%A1%E5%96%AE%E7%9A%84pm%E5%8A%83%E5%88%86%E5%89%AF%E7%A8%8B%E5%BC%8F)

```python   
   190  #PM splitting
   191  df=add_PMS(df)
   192
```

### 年均排放量乘上時變係數
- **時變係數**檔案，因筆數與不同的定義高度有關，須先執行後，將檔名寫在程式內。
  - 此處的`fns0`~`fns30`分別是高度0~30所對應的**時變係數**檔案
  - 好處是：如此可以將對照關係記錄下來
  - 壞處是：必須手動修改程式碼、每版teds的檔案名稱會不一樣

```python   
   193  #pivot along the axis of XY coordinates
   194  #def. of columns and dicts
   195  fns0={
   196  'CO'  :'CO_ECP7496_MDH8760_ONS.bin',
   197  'NMHC':'NMHC_ECP2697_MDH8760_ONS.bin',
   198  'NOX' :'NOX_ECP13706_MDH8760_ONS.bin',
   199  'PM'  :'PM_ECP17835_MDH8760_ONS.bin',
   200  'SOX' :'SOX_ECP8501_MDH8760_ONS.bin'}
   201
   202  fns10={
   203  'CO'  :'CO_ECP4919_MDH8784_ONS.bin',
   204  'NMHC':'NMHC_ECP3549_MDH8784_ONS.bin',
   205  'NOX' :'NOX_ECP9598_MDH8784_ONS.bin',
   206  'PM'  :'PM_ECP11052_MDH8784_ONS.bin',
   207  'SOX' :'SOX_ECP7044_MDH8784_ONS.bin'}
   208  fns30={
   209  'CO'  :'CO_ECP1077_MDH8784_ONS.bin',
   210  'NMHC':'NMHC_ECP1034_MDH8784_ONS.bin',
   211  'NOX' :'NOX_ECP1905_MDH8784_ONS.bin',
   212  'PM'  :'PM_ECP2155_MDH8784_ONS.bin',
   213  'SOX' :'SOX_ECP1468_MDH8784_ONS.bin'}
   214  F={0:fns0,10:fns10,30:fns30}
   215  fns=F[Hs]
```
- 排放名稱與空品名稱對照表、排放名稱與分子量對照表

```python   
   216  cols={i:[c2s[i]] for i in c2s}
   217  cols.update({'NMHC':cbm,'PM':colc})
   218  colp={c2s[i]:i+'_EMI' for i in fns}
   219  colp.update({i:i for i in cbm+colc})
   220  lspec=[i for i in list(colp) if i not in ['NMHC','PM']]
   221  c2m={i:1 for i in colp}
   222  c2m.update({'SO2':64,'NO2':46,'CO':28})
   223  col_id=["C_NO","XY"]
   224  col_em=list(colp.values())
   225  col_mn=['TEMP','VEL','UTM_E', 'UTM_N','HY1','HD1','DY1']
   226  col_mx=['HEI']
   227  df['XY']=[(x,y) for x,y in zip(df.UTM_E,df.UTM_N)]
   228  df["C_NO"]=[x[:8] for x in df.CP_NO]
   229
   230
```
- 讀取**時變係數**並將其常態化(時間軸加總為1.0)
  - SPECa為每煙道逐時排放量
  
```python   
   231  print('Time fraction multiplying and expanding')
   232  #matching of the bin filenames
   233  nopts=len(df)
   234  SPECa=np.zeros(shape=(ntm,nopts,len(lspec)))
   235  id365=365
   236  if yr%4==0:id365=366
```
  - 依序開啟各污染物之**時變係數**檔案

```python   
   237  for spe in fns:
   238    fnameO=fns[spe]
   239    with FortranFile(fnameO, 'r') as f:
   240      cp = f.read_record(dtype=np.dtype('U12'))
   241      mdh = f.read_record(dtype=np.int)
   242      ons = f.read_record(dtype=float)
```
  - `FortranFile`的特色是只有總長度，沒有形狀，需要`reshape`
  - 對時間軸加總

```python   
   243    ons=ons.reshape(len(cp),len(mdh))
   244    s_ons=np.sum(ons,axis=1)
```
  - 重新整理順序，只處理有排放的煙道(加總>0者)、且**管煙**編號存在於資料庫(確認用)

```python   
   245    #only those CP with emission accounts
   246    idx=np.where(s_ons>0)
   247    cp1 = [i for i in cp[idx[0]] if i in list(df.CP_NO)]
```
  - 因為序列的`index`指令會很耗時，先將做成`array`。

```python   
   248    idx= np.array([list(cp).index(i) for i in cp1])
   249    cp, ons, s_ons =cp1,ons[idx,:],s_ons[idx]
   250    #normalize to be the fractions in a year
```
  - 常態化

```python   
   251    ons=ons/s_ons[:,None]
```
- 製作煙道、當月啟始及終結時間的標籤
  - 從全年的**時變**係數矩陣中提取當月部分，存成`ons2`矩陣

```python   
   252    idx_cp=[list(df.CP_NO).index(i) for i in cp]
   253    ibdate=list(mdh).index(int(bdate.strftime('%m%d%H')))
   254    iedate=list(mdh).index(int(edate.strftime('%m%d%H')))
   255    ons2=np.zeros(shape=(nopts,ntm)) #time fractions for this month
   256    if ibdate>iedate:
   257      endp=id365*24-ibdate
   258      ons2[idx_cp,:endp]=ons[:,ibdate:]
   259      ons2[idx_cp,endp:ntm]=ons[:,:iedate]
   260    else:
   261      ons2[idx_cp,:]=ons[:,ibdate:iedate]
```
- `SPEC`為全年排放總量(時間軸為定值)，單位轉成gmole，或g。

```python   
   262    NREC,NC=nopts,len(cols[spe])
   263    ons =np.zeros(shape=(ntm,NREC,NC))
   264    SPEC=np.zeros(shape=(ntm,NREC,NC))
   265    for c in cols[spe]:
   266      ic=cols[spe].index(c)
   267      for t in range(ntm):
   268        SPEC[t,:,ic]=df[colp[c]]/c2m[c]
```
- 借用之前用過的`ons`矩陣來儲存ons2的轉置結果。並進行排放總量與**時變**係數相乘

```python   
   269    OT=ons2.T[:,:]
   270    for ic in range(NC):
   271      ons[:,:,ic]=OT
   272    #whole matrix production is faster than idx_cp selectively manupilated
   273    for c in cols[spe]:
   274      if c not in V[1]:continue
   275      ic=cols[spe].index(c)
   276      icp=lspec.index(c)
   277      SPECa[:,:,icp]=SPEC[:,:,ic]*ons[:,:,ic]
```

### 將逐時排放量存成fth檔案並清空記憶體
- 形成新的逐時資料表(`dfT`)
  - **管煙**編號序列重新整理，取得順位標籤`CP_NOi`
  - 時間標籤`idatetime`

```python   
   278  print('pivoting along the C_NO axis')
   279  #forming the DataFrame
   280  CPlist=list(set(df.CP_NO))
   281  CPlist.sort()
   282  pwrt=int(np.log10(len(CPlist))+1)
   283  CPdict={i:CPlist.index(i) for i in CPlist}
   284  df['CP_NOi']=[CPdict[i] for i in df.CP_NO]
   285  idatetime=np.array([i for i in range(ntm) for j in range(nopts)],dtype=int)
   286  dfT=DataFrame({'idatetime':idatetime})
```
- 將原來的排放資料表`df`展開成`dft`

```python   
   287  ctmp=np.zeros(shape=(ntm*nopts))
   288  for c in col_mn+col_mx+['CP_NOi']+['ORI_QU1']:
   289    clst=np.array(list(df[c]))
   290    for t in range(ntm):
   291      t1,t2=t*nopts,(t+1)*nopts
   292      a=clst
   293      if c=='CP_NOi':a=t*10**(pwrt)+clst
   294      ctmp[t1:t2]=a
   295    dfT[c]=ctmp
```
- 將排放量矩陣壓平後，覆蓋原本的資料庫`df`內容。
```python   
   296  #dfT.C_NOi=np.array(dfT.C_NOi,dtype=int)
   297  for c in lspec:
   298    icp=lspec.index(c)
   299    dfT[c]=SPECa[:,:,icp].flatten()
   300  #usage: orig df, index, sum_cols, mean_cols, max_cols
   301  df=XY_pivot(dfT,['CP_NOi'],lspec,col_mn+['ORI_QU1'],col_mx).reset_index()
   302  df['CP_NO']=[int(j)%10**pwrt for j in df.CP_NOi]
   303
```
- 進行pivot_table整併

```python   
   304  pv=XY_pivot(df,['CP_NO'],lspec,col_mn+['ORI_QU1'],col_mx).reset_index()
   305  Bdict={CPdict[j]:[bytes(i,encoding='utf-8') for i in j] for j in CPlist}
   306  pv['CP_NOb'] =[Bdict[i] for i in pv.CP_NO]
   307  nopts=len(set(pv))
   308
```
- 控制料堆排放量
  - 將`df`另存成`fth`檔案，釋放記憶體，以接續nc檔案之儲存。

```python   
   309  #blanck the PY sources
   310  PY=pv.loc[pv.CP_NOb.map(lambda x:x[8:10]==[b'P', b'Y'])]
   311  nPY=len(PY)
   312  a=np.zeros(ntm*nPY)
   313  for t in range(ntm):
   314    t1,t2=t*nPY,(t+1)*nPY
   315    a[t1:t2]=t*nopts+np.array(PY.index,dtype=int)
   316  for c in colc:
   317    ca=df.loc[a,c]/5.
   318    df.loc[a,c]=ca
   319  df.to_feather('df'+mm+'.fth')
   320  pv.set_index('CP_NO').to_csv('pv'+mm+'.csv')
   321
   322  sys.exit()
```

## 檔案下載
- `python`程式：[ptseE_ONS.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptseE.py)。
- `jupyter-notebook`檔案
  - [ptseE_ONS.ipynb](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/ptse/ptseE.ipynb)
  - [nbviewer](https://nbviewer.org/github/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/ptse/ptseE.ipynb)


## Reference
