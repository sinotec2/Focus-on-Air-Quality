---
layout: default
title: "area_YYMM"
parent: "Area Sources"
grand_parent: TEDS Python
nav_order: 4
date:               
last_modified_date:   2021-12-01 14:16:46
---

# 面源資料庫轉CAMx排放`nc`檔
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
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)、針對[面源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)與[重新計算網格座標](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/prep_areagridLL/)，為此處之前處理。  

## 程式說明

### 引用模組
- `include2`, `include2`, `mostfreqword`詳見[面源計算用到的副程式](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/include3/)

```python
kuang@114-32-164-198 /Users/TEDS/teds10_camx/HourlyWeighted/area
$ cat -n area_YYMMinc.py 
     1	"""usage:
     2	python YYMM(year and month both in 2 digits)
     3	1.Domain is determined by the template chosen.
     4	2.One file(month) at a time. The resultant file will not be overwritten.
     5	3.nc files may be corrupted if not properly written. must be remove before redoing.
     6	4.nc_fac.json file is needed, df_Admw.py must be excuted earlier.
     7	"""
     8	import numpy as np
     9	from pandas import *
    10	from calendar import monthrange
    11	import sys, os, subprocess
    12	import netCDF4
    13	from datetime import datetime, timedelta
    14	from include2 import rd_ASnPRnCBM_A, WGS_TWD, tune_UTM
    15	from include3 import dt2jul, jul2dt, disc, add_PMS, add_VOC
    16	from mostfreqword import mostfreqword
    17	import json
    18	import warnings
    19	
    20	if not sys.warnoptions:
    21	    import warnings
    22	    warnings.simplefilter("ignore")
    23	
```
### 讀入引數、計算起訖日期
```python
    24	#Main
    25	ym=sys.argv[1]
    26	mm=sys.argv[1][2:4]
    27	mo=int(mm)
    28	yr=2000+int(sys.argv[1][:2])
    29	if (yr-2016)%3 !=0 or 0==mo or mo>12:sys.exit('wrong ym='+ym)
    30	teds=str((yr-2016)//3+10) #TEDS version increase every 3 years
    31	P='./'
    32	
    33	#time and space initiates
    34	ntm=(monthrange(yr,mo)[1]+2)*24+1
    35	bdate=datetime(yr,mo,1)+timedelta(days=-1+8./24)
    36	edate=bdate+timedelta(days=monthrange(yr,mo)[1]+3)
```

### `nc`模版之準備
- `nc`模版如何形成？
  - 修改CAMx提供的範例檔案
  - 使用`pncgen`轉換一個既有的[uamiv][uamiv]檔案
  - 從CMAQ排放量檔案轉換而來

[uamiv]: <https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式> "CAMx所有二進制 I / O文件的格式，乃是遵循早期UAM(城市空氣流域模型EPA，1990年）建立的慣例。 該二進制文件包含4筆不隨時間改變的表頭記錄，其後則為時間序列的數據記錄。詳見CAMx(UAM)的檔案格式"

```python
    37	#prepare the template
    38	fname='fortBE.413_teds'+teds+'.area'+mm+'.nc'
    39	try:
    40	  nc = netCDF4.Dataset(fname, 'r+')
    41	except:
    42	  os.system('cp '+P+'template_d4.nc '+fname)
    43	  nc = netCDF4.Dataset(fname, 'r+')
    44	V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    45	nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
    46	nv=len(V[3])
    47	nc.SDATE,nc.STIME=dt2jul(bdate)
    48	nc.EDATE,nc.ETIME=dt2jul(edate)
    49	nc.NOTE='grid Emission'
    50	nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
    51	#Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
    52	#nc.NAME='EMISSIONS '
    53	if 'ETFLAG' not in V[2]:
    54	  zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
```
- 延長模版時間維度的長度

```python
    55	if nt!=ntm or (nc.variables['TFLAG'][0,0,0]!=nc.SDATE and nc.variables['TFLAG'][0,0,1]!=nc.STIME):
    56	  for t in range(ntm):
    57	    sdate,stime=dt2jul(bdate+timedelta(days=t/24.))
    58	    nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    59	    nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    60	    ndate,ntime=dt2jul(bdate+timedelta(days=(t+1)/24.))
    61	    nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    62	    nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
```
- 所有項目歸零。否則會出現`mask`導致錯誤。
```python
    63	for v in V[3]:
    64	  nc.variables[v][:]=0.
    65	sdatetime=[jul2dt(nc.variables['TFLAG'][t,0,:]) for t in range(ntm)]
```

### 污染物名稱、對照表
```python
    66	col=['PM','PM25', 'CO', 'NOX', 'NMHC', 'SOX','NH3'] #1NO   2NO2   3SO2   4NH3   5CCRS   6FCRS   7PAR
    67	cole=['EM_'+i for i in col] #1NO   2NO2   3SO2   4NH3   5CCRS   6FCRS   7PAR
    68	#define the crustals/primary sources
    69	colc=['CCRS','FCRS','CPRM','FPRM']
    70	c2v={i:i for i in colc}
    71	c2m={i:1 for i in colc}
    72	colv='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
    73	NC=len(colv)
    74	c2v.update({i:i for i in colv if i not in ['NR','ETHY']})
    75	c2m.update({i:1 for i in colv if i not in ['NR','ETHY']})
    76	c2v.update({'EM_SOX':'SO2','EM_NOX':'NO','EM_CO':'CO','EM_NH3':'NH3'})
    77	c2m.update({'EM_SOX':64,'EM_NOX':46,'EM_CO':28,'EM_NH3':17})
    78	
    79	
```

### 開啟面源及氨氣排放量資料庫
```python
    80	#import the gridded area sources
    81	fname=P+'areagrid'+teds+'LL.csv'
    82	df = read_csv(fname)
    83	minx,miny=min(df.UTME),min(df.UTMN)
    84	df.UTME=round(df.UTME-minx,-3)
    85	df.UTMN=round(df.UTMN-miny,-3)
    86	df['YX']=np.array(df.UTMN+df.UTME/1000,dtype=int)
    87	
    88	#add nh3 separately
    89	YX_DICT=pivot_table(df,index=['YX'],values='DICT',aggfunc=mostfreqword).reset_index()
    90	YX_DICT={i:j for i,j in zip(YX_DICT.YX,YX_DICT.DICT)}
```
- 氨氣排放量讀取

```python
    91	df['EM_NH3']=0.
    92	fname=P+'nh3.csv'
    93	nh3=read_csv(fname)
    94	nh3 = tune_UTM(nh3)
    95	nh3['NSC']='nh3'
    96	nh3['NSC_SUB']='b'
    97	if 'nsc2' in df.columns: nh3['nsc2']='nh3b'
    98	nh3.UTME=round(nh3.UTME-minx,-3)
    99	nh3.UTMN=round(nh3.UTMN-miny,-3)
   100	nh3['YX']=np.array(nh3.UTMN+nh3.UTME/1000,dtype=int)
   101	nh3=nh3.loc[nh3.YX.map(lambda x:x in YX_DICT)].reset_index(drop=True)
   102	nh3['DICT']=[YX_DICT[i] for i in nh3.YX]
   103	for c in df.columns:
   104	  if c not in nh3.columns:
   105	    nh3[c]=0
   106	df=df.append(nh3,ignore_index=True)
   107	nh3=0#clean_up of mem
   108	
   109	#The two levels of the NCS are grouped as one.
   110	if 'nsc2' not in df.columns:
   111	  df.loc[df['NSC_SUB'].map(lambda x: (type(x)==float and np.isnan(x)==True) or ( x==' ')),'NSC_SUB']='b'
   112	  df['nsc2']=[str(x)+str(y) for x,y in zip(df['NSC'],df['NSC_SUB'])]
   113	df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
   114	if 'CNTY' not in df.columns:
   115	  df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
```
- 加總縣市邊界上的重複資料

```python
   116	coli=['CNTY', 'nsc2','YX']
   117	df=pivot_table(df,index=coli,values=cole,aggfunc=np.sum).reset_index()
   118	
```

### 粒狀物與VOCs之劃分
```python
   119	#note the df is discarded
   120	df=add_PMS(df)
   121	#add the VOC columns and reset to zero
   122	if 'EM_NMHC' in df.columns:
   123	  nmhc=df.loc[df.EM_NMHC>0]
   124	  if len(nmhc)>0:
   125	    for c in colv:
   126	      df[c]=np.zeros(len(df))
   127	    nsc2=set(nmhc.nsc2)
   128	    for n in nsc2:
   129	      df=add_VOC(df,n)
   130	#Summed up for all the categories. The results are filled into the nc template
   131	if set(c2v).issubset(set(df.columns)):
   132	  df=pivot_table(df,index=['CNTY', 'YX', 'nsc2'],values=list(c2v),aggfunc=sum).reset_index()
   133	else:
   134	  sys.exit('not pivot')
   135	
```

### 儲存排放量矩陣`TPY`
```python
   136	#df store to matrix 
   137	for c in ['CNTY','nsc2','YX']:
   138	  exec(c+'=list(set(df.'+c+'))')
   139	  exec(c+'.sort()')
   140	  exec('n'+c+'=len('+c+')')
   141	  exec('d'+c+'={'+c+'[i]:i for i in range(n'+c+')}')
   142	  exec('df["i'+c+'"]=[d'+c+'[i] for i in df.'+c+']')
   143	list_c2v=list(c2v)
   144	list_c2v.sort()
   145	NLC=len(c2v)
   146	TPY=np.zeros(shape=(NLC,nCNTY,nnsc2,nYX))
   147	for i in range(NLC):
   148	  c=list_c2v[i]
   149	  TPY[i,df.iCNTY[:],df.insc2[:],df.iYX[:]]=df[c][:]
   150	
```

### 時間變化係數矩陣`fac`
- 讀取對照表`json`檔，將展開成為完整的`DataFrame`，最後形成**矩陣**`fac`以利相乘

```python
   151	#processing all the time-variation and constant categories
   152	with open('nc_fac.json', 'r', newline='') as jsonfile:
   153	  nc_fac=json.load(jsonfile)
   154	
```
- 全年的時間標籤(`dts`)，用在序列數據的拮取

```python
   155	yr=2016+(int(teds)-10)*3
   156	bdate0=datetime(yr,1,1)-timedelta(days=1)
   157	nd365=365
   158	if yr%4==0:nd365=366
   159	nty=(nd365+2)*24
   160	dts=[bdate0+timedelta(days=i/24.) for i in range(nty)]
   161	
```
- 具有時間變化的排放類別

```python
   162	#time-variant part of nsc2
   163	ll=list(nc_fac)
   164	df=DataFrame({'nsc2':[i.split('_')[0] for i in ll],\
   165	'CNTY':[i.split('_')[1] for i in ll],\
   166	'fac':[nc_fac[i] for i in ll]})
   167	nc_fac=0#clean_up of mem
   168	#time variation files use ??b to represent all kind of NSC_SUB
   169	for n2 in set(df.nsc2)-set(nsc2):
   170	  a=df.loc[df.nsc2==n2].reset_index(drop=True)
   171	  nns=[i for i in nsc2 if i[:-1]==n2[:-1]]
   172	  for n in nns:
   173	    a.nsc2=n
   174	    df=df.append(a,ignore_index=True)
   175	df=df.loc[df.nsc2.map(lambda x:x in nsc2)].reset_index(drop=True) #drop these surrogate nsc2
   176	df=df.loc[df.CNTY.map(lambda x:x in CNTY)].reset_index(drop=True) #drop 53
   177	nfac=len(df)
   178	var2=np.zeros(shape=(nfac,nty),dtype=int)
   179	fac =np.zeros(shape=(nCNTY,nnsc2,nty))
   180	for c in ['CNTY','nsc2']:
   181	  exec('var2[:,:]=np.array([d'+c+'[i] for i in df.'+c+'])[:,None]')
   182	  exec('i'+c+'=var2[:,:].flatten()')
   183	var2[:,:]=np.arange(nty)[None,:];    it=var2.flatten()
   184	fac1=np.array([np.array(i) for i in df.fac]).flatten()
   185	fac[iCNTY[:],insc2[:],it[:]]=fac1[:]
   186	fac1=0#clean_up of mem
   187	
```
- 常數類別，其**時變係數**為一定值

```python
   188	#constant part of nsc2
   189	insc2=np.array([dnsc2[n] for n in set(nsc2)-set(df.nsc2)])
   190	nnsc2=len(insc2)
   191	var3=np.zeros(shape=(nCNTY,nnsc2,nty),dtype=int)
   192	var3[:,:,:]=np.arange(nCNTY)[:,None,None];iCNTY=var3.flatten()
   193	var3[:,:,:]=           insc2[None,:,None];insc2=var3.flatten()
   194	var3[:,:,:]=  np.arange(nty)[None,None,:];it   =var3.flatten()
   195	fac[iCNTY[:],insc2[:],it[:]]=1./nty
   196	
```
- 由全年序列中，按照`dts`拮取本月之**時變係數**備用

```python
   197	#cutting for desired month from whole year time-factors
   198	ib=dts.index(bdate)
   199	dts=dts[ib:ib+ntm]
   200	fac=fac[:,:,ib:ib+ntm] #clean_up of mem
   201	
```
- 採用[np.tensordot](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/#whats-learned)矩陣內積，消除中間的2個維度(`nsc2`, `cnty`)，成為單純的(物種、空間、時間)3維度矩陣

```python
   202	#eliminate the nsc2 and CNTY dimensions (multiply-and-sum by tensordot)
   203	df,var2,var3,iCNTY,insc2,it=0,0,0,0,0,0 			#clean_up of mem
   204	aTPY = np.tensordot(TPY,fac, axes=([1,2],[0,1])) 	#in shape of (isp, nYX, ntm)
   205	TPY,fac=0,0											#clean_up of mem
   206	
```

### 網格化與存檔
- 注意nc檔案並不適用np.array的fancy indexing(line 230~231)
   - 詳[NC檔案多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)

```python
   207	idx=np.where(np.sum(aTPY[:,:,:],axis=0)>0)
   208	dd,ic={},0
   209	for c in list_c2v:
   210	  dd[c]=aTPY[ic,idx[0][:],idx[1][:]]
   211	  ic+=1
   212	dd['YX']=[YX[i] for i in idx[0]]
   213	dd['idt']=idx[1]
   214	df=DataFrame(dd)
   215	df['UTME']=(df.YX%1000)*1000+minx
   216	df['UTMN']=(df.YX//1000)*1000+miny
   217	df=disc(df,nc)											#disc after tensordot
   218	
   219	fac=1000.*1000./nd365/24 #ton/yr to g/hr
   220	  
   221	#Filling to the template
   222	var3=np.zeros(shape=(ntm,nrow,ncol))
   223	for c in c2v:
   224	  if c not in df.columns:continue
   225	  if sum(df[c])==0.:continue
   226	  if c2v[c] not in V[3]:continue
   227	  #T/Y to gram/hour (gmole for SNC and VOCs)
   228	  dfc=df.loc[df[c]>0].reset_index(drop=True)
   229	  var3[:]=0.
   230	  var3[dfc.idt,dfc.IY,dfc.IX]=dfc[c]*fac/c2m[c]
   231	  nc.variables[c2v[c]][:,0,:,:]=var3[:,:,:]
   232	
```

## 程式之執行
- 依月份呼叫即可
- machine-dependancy
  - 如要改寫成[uamiv][uamiv]檔案，系統必須要有`pncgen`程式
  - 因pandas及no.tensordot會自己啟動多工運作，同時執行3個月份node01~03尚能消化(CPU~4500%)，如太多月份同時運作，系統資源將會耗盡。不但拖慢速度，結果也不正確

```bash
for m in {01..04};do sub python area_YYMM.py 19$m >&/dev/null;done
for m in {05..08};do sub python area_YYMM.py 19$m >&/dev/null;done
for m in {09..12};do sub python area_YYMM.py 19$m >&/dev/null;done
```
  
## 檔案下載
- `python`程式：[area_YYMMinc.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/area_YYMMinc.py)。

## Reference
