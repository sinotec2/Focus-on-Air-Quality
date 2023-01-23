---
layout: default
title: "Construct the MobileS"
parent: "Mobile Sources"
grand_parent: TEDS Python
nav_order: 2
date:               
last_modified_date:   2021-12-02 11:08:53
tags: TEDS
---

# 移動源排放檔案之轉檔
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
- 由環保署移動源檔案讀取資料庫維度，改寫成矩陣形式。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/#處理程序總綱)、針對[植物源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/biog/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，為此處之前處理。  

## 程式分段說明

### 引用與檔案輸入
- 引用模組。
  - 此處用到[include2.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/include2.py)的`rd_hwcsv`,`rd_ASnPRnCBM`
  - 還包括[include3.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/include3.py)的[dt2jul, jul2dt](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/include3/#引用模組及時間標籤轉換dt2jul-jul2dt)

```python
kuang@node03 /nas1/TEDS/teds11/line
$ cat -n lineinc.py
     1  #!/cluster/miniconda/envs/py37/bin/python
     2  import numpy as np
     3  import netCDF4
     4  import os,sys
     5  from pathlib import Path
     6  from include2 import rd_hwcsv,rd_ASnPRnCBM
     7  from include3 import jul2dt, dt2jul
     8  from scipy.io import FortranFile
     9  from pandas import *
    10  from calendar import monthrange
    11  import datetime
    12  import twd97
    13  import subprocess
    14
    15
```

- 由工作目錄讀取teds及年代、輸入資料庫維度、
```python
    16  #Input the record csv and EM matrix, then reshaping them.
    17  P=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n')+'/'
    18  teds=int(P.split('/')[3][-2:])
    19  yr=2016+(teds-10)*3
    20
    21  #read the index
    22  df=read_csv(P+'df_kin.csv')
    23  NREC,X,Y,R,C=len(df),list(df.X),list(df.Y),list(df.R),list(df.C)
    24  APOL=['CO', 'EHC', 'EXHC', 'NH3', 'NMHC', 'NOX', 'PB', 'PM', 'PM25', 'PM6', 'RHC', 'RST', 'SOX', 'THC', 'TSP']
    25  VT_TM=['bhddt', 'bhdgv', 'blddt', 'blddv', 'bldgt', 'bldgv', 'bldhev', 'bldlpg', 'bus', 'hdsv', 'ldsv', 'mc2', 'mc4', 'phddt', 'phdgv', 'plddt', 'plddv', 'pldgt', 'pldgv', 'pldhev', 'pldlpg']
    26  NPOLn=len(APOL);LTYP=4;NVTYP=len(VT_TM)
    27
```

- 讀取排放量矩陣(詳[移動源排放檔案之準備]())，並去除非必要污染項目
```python
    28  #read the emission matrix
    29  fname = 'cl08_'+'{:d}_{:d}_{:d}'.format(NREC,NPOLn,NVTYP)+'.bin'
    30  with FortranFile(P+fname, 'r') as f:
    31    TM3=f.read_record(dtype=np.float64)
    32  #The line type are dependent to NREC series also redundent, degrading it.
    33  #convert the unit from T/Y to g/hr
    34  ndays=365
    35  if yr%4==0:ndays=366
    36  UNIT=1000.*1000./(24.*ndays)
    37  TM3=np.reshape(TM3,[NREC,NPOLn,NVTYP])*UNIT
    38  #from TSP and PM2.5 calculate CPRM and store replacing original TSP
    39  Aold='TSP PM25 SOX NOX CO EXHC EHC RHC NMHC PB'.split()
    40  NPOL=len(Aold)
    41  EM3=np.zeros(shape=(NREC,NPOL,NVTYP))
    42  d_ON={i:APOL.index(Aold[i]) for i in range(NPOL)}
    43  for i in range(NPOL):
    44    EM3[:,i,:]=TM3[:,d_ON[i],:]
    45  TM3=0
    46  TSP,FPRM=EM3[:,0,:],EM3[:,1,:]
    47  CPRM=TSP-FPRM
    48  EM3[:,0,:]=CPRM
    49  APOL='CPRM FPRM SO2 NO CO EXHC EHC RHC NMHC PB'.split()
    50
```

-  時變係數以及VOCs成份劃分所需資料庫

```python
    51  #Time varied factors
    52  (df_t,sdf2csv)=rd_hwcsv()
    53
    54  #SPECIATE, PROFILE database for vehicles
    55  (df_asgn,df_prof,df_cbm)= rd_ASnPRnCBM()
    56  MW={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['MW']))}
    57  colc=['CCRS','FCRS','CPRM','FPRM']
    58  c2v={i:i for i in colc}
    59  c2m={i:1 for i in colc}
    60  colv='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
    61  c2v.update({i:i for i in colv if i not in ['NR','ETHY']})
    62  c2m.update({i:1 for i in colv if i not in ['NR','ETHY']})
    63  c2v.update({'EM_SOX':'SO2','EM_NOX':'NO','EM_CO':'CO'})
    64  c2m.update({'SO2':64,'NO':46,'CO':28})
    65
    66  BASE={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['BASE']))}
    67  NC=[5,20] #number pf compounds for non-VOCs and VOCs
    68  SPNAM='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
    69  if len(SPNAM) != NC[1]: sys.exit('wrong NC_vocs or SPNAM')
    70  colv=SPNAM
    71  cole=APOL[:NC[0]]
    72  #define the crustals/primary sources
    73  try:
    74    prof_cbm=read_csv(P+'prof_cbm.csv')
    75    prof_cbm.PRO_NO=['{:04d}'.format(m) for m in prof_cbm.PRO_NO]
    76  except:
    77    HC=1
    78    prof_cbm=DataFrame({})
    79    prof_cbm['PRO_NO']=list(set(df_asgn.PRO_NO))
    80    for c in colv:
    81      prof_cbm[c]=0.
    82    for i in range(len(prof_cbm)):
    83      prof=prof_cbm.PRO_NO[i]
    84      spec=df_prof.loc[df_prof.PRO_NO==prof].reset_index(drop=True)
    85      for K in range(len(spec)):
    86        W_K_II,IS=spec.WT[K],spec.SPE_NO[K]
    87        if W_K_II==0.0 or sum(BASE[IS])==0.0:continue
    88        VOCwt=HC*W_K_II/100.
    89        VOCmole=VOCwt/MW[IS]
    90        for LS in range(NC[1]): #CBM molar ratio
    91          if BASE[IS][LS]==0.:continue
    92          prof_cbm.loc[i,colv[LS]]+=VOCmole*BASE[IS][LS]
    93    prof_cbm.set_index('PRO_NO').to_csv('prof_cbm.csv')
```
- 車輛形態(排放量資料庫)、車輛大小(時變係數)、與排放種類等對照表

```python
    95  cart=['CAR_LT','CAR_LV','CAR_HT','CAR_HV']
    96  ncar=len(cart)
    97  VT21_13={ 'bhddt': 'hddt', 'bhdgv': 'hdgv', 'blddt': 'lddt', 'blddv': 'pldd',
    98   'bldgt': 'ldgt', 'bldgv': 'bldg', 'bldhev':'pldg', 'bldlpg':'bldl', 'bus':   'bus',
    99   'hdsv':'hdsv', 'ldsv':'ldsv', 'mc2': 'mc2', 'mc4': 'mc4', 'phddt': 'hddt', 'phdgv': 'hdgv',
   100   'plddt': 'lddt', 'plddv': 'pldd', 'pldgt': 'ldgt', 'pldgv': 'pldg', 'pldhev':'pldg',
   101   'pldlpg':'bldl'}
   102  for i in VT21_13:
   103    VT21_13.update({i:VT21_13[i].upper()+' '*(4-len(VT21_13[i]))})
   104  lVT=list(set(VT21_13))
   105  lVT.sort()
   106  VT21_CAR={ 'bhddt':3, 'bhdgv':4, 'blddt':1, 'blddv':2,
   107   'bldgt':1, 'bldgv':2, 'bldhev':2, 'bldlpg':2, 'bus':3,
   108   'hdsv':4, 'ldsv':2, 'mc2':0, 'mc4':0, 'phddt':3, 'phdgv': 3,
   109   'plddt': 1, 'plddv': 2, 'pldgt': 1, 'pldgv': 2, 'pldhev':2,
   110   'pldlpg':2}
   111  #old Viehle type
   112  VTYP=['PLDG','BLDG', 'LDGT','LDDT','HDGV','HDDT', \
   113       'BUS ','MC2 ','MC4 ','PLDD','BLDL', 'LDSV','HDSV']
   114  ETYP=['EX ','E  ','R  ']
   115
```
- 排放形態、車種之碳鍵乘數
```python
   116  #Applied the PROFILE to the vehicles and emis. sources
   117  NETYP=3
   118  prod=np.zeros(shape=(NETYP,NVTYP,NC[1]))
   119  for I in range(NETYP):
   120    for J in range(NVTYP):
   121      boo1=(df_asgn['ET']==ETYP[I]) & (df_asgn['VT']==VT21_13[lVT[J]])
   122      prof=list(df_asgn.loc[boo1,'PRO_NO'])[0]
   123      cbms=prof_cbm.loc[prof_cbm.PRO_NO==prof].iloc[0,1:]
   124      prod[I,J,:]=cbms
   125
```

### 時空基準與模版之應用
- 時間與空間之基準
```python
   126  #Temporal and Spatial bases
   127  mm=sys.argv[1]
   128  mo=int(mm)
   129  ntm=(monthrange(yr,mo)[1]+2)*24+1
   130  bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
   131  edate=bdate+datetime.timedelta(days=monthrange(yr,mo)[1]+3)
   132  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
   133  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
   134
   135
```
- `nc`模版之開啟、時間維度之延長

```python
   136  #prepare the uamiv template
   137  fname='fortBE.413_teds10.line'+mm+'.nc'
   138  try:
   139    nc = netCDF4.Dataset(fname, 'r+')
   140  except:
   141    os.system('cp '+P+'template_d4.nc '+fname)
   142    nc = netCDF4.Dataset(fname, 'r+')
   143  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
   144  nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
   145  nv=len(V[3])
   146  nc.SDATE,nc.STIME=dt2jul(bdate)
   147  nc.EDATE,nc.ETIME=dt2jul(edate)
   148  nc.NOTE='grid Emission'
   149  nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
   150  #Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
   151  #nc.NAME='EMISSIONS '
   152  #Time stamps
   153  if 'ETFLAG' not in V[2]:
   154    zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
   155  if 'nt' not in locals() or nt!=ntm:
   156    for t in range(ntm):
   157      sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
   158      nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
   159      nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
   160      ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
   161      nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
   162      nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
   163  sdatetime=[jul2dt(nc.variables['TFLAG'][t,0,:]) for t in range(ntm)]
   164  for c in V[3]:
   165    nc.variables[c][:]=0.
   166
```
- 資料庫增加`IX`,`IY`以備(最終)整併使用

```python
   167  #Horizontal Grid system, which is dependent to template
   168  df['UTME']=df.X*1000.
   169  df['UTMN']=df.Y*1000.
   170  df['IX']=np.array((df.UTME-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
   171  df['IY']=np.array((df.UTMN-Ycent-nc.YORIG)/nc.YCELL,dtype=int)
   172
   173
```

### 時變係數之整理與相乘
- 形成時變係數矩陣

```python
   174  #Expand and store the hourly factors into facs and fact matrix
   175  DICT=list(set(df_t.DICT))
   176  NCNT=len(DICT)+1
   177  idict={i:len(DICT) for i in set(df.C)-set(df_t.DICT)} #df.CNTY not in df_t.DICT, mappint to 17(last one)
   178  idict.update({i:DICT.index(i) for i in DICT})
   179  NSLT=ncar+1 #0 for motorcycles, 1/2/3/4 are small, light and heavy T and V
   180  facs=np.ones(shape=(ntm,NCNT,NSLT))
```
   - 依次進行逐時、逐行政區迴圈
   - `facs`:大、中、小車的時變係數，`fact`:按照資料庫之21種車型
```python
   181  #loop for time
   182  for it in range(ntm):
   183    year,mo,da,hr=sdatetime[it].year,sdatetime[it].month,sdatetime[it].day,sdatetime[it].hour
   184    boo=(df_t['MONTH']==mo)&(df_t['DATE']==da)&(df_t['HOUR']==hr*100)
   185    df1=df_t.loc[boo]
   186    if len(df1)==0:
   187      sys.exit('DateHr not found:'+str(mo)+str(da)+str(hr))
   188    for cnt in DICT:
   189      idc=idict[cnt]
   190      df2=df1.loc[df1['DICT']==cnt]
   191      if len(df2)==0:continue
   192      facs[it,idc,:]=[0]+[list(df2[cart[icar]])[0]*ndays*24. for icar in range(ncar)]
   193  facs[:,:,0]=np.mean(facs[:,:,1:2],axis=2) #motocycle is same as light
   194  facs[:,len(DICT),:]=np.mean(facs[:,:len(DICT)+1,:],axis=1) #last one store the mean values
   195
   196  df['idc']=[idict[i] for i in df.C]
   197  fact=np.zeros(shape=(ntm,NREC,NVTYP))
   198  for J in range(NVTYP):
   199    fact[:,:,J]=facs[:,df.idc[:],VT21_CAR[lVT[J]]]
   200
   201  facs=0
```
- 排放量(時間、空間)矩陣=全年排放量*時變係數矩陣
  - 一般污染物
  - 無法使用np.tensordot的理由：因為不是每個矩陣都有一樣、明確的長度。必須依序執行相乘與加總

```python
   202  #expand the POLs matrixs
   203  EM4=np.zeros(shape=(ntm,NREC,NC[0],NVTYP))
   204  c2mv=np.array([c2m[cole[I]] for I in range(NC[0])])
   205  EM4[:,:,:,:]=EM3[None,:,:NC[0],:]*fact[:,:,None,:]/c2mv[None,None,:,None]
   206
   207  #sum-up the vehicle dimension
   208  POL=np.sum(EM4[:,:,:,:],axis=3)
```

- VOCs成分項目矩陣之相乘
```python
   209  #expand the VOCs matrixs
   210  EM4=np.zeros(shape=(ntm,NREC,NETYP,NVTYP))
   211  EM4[:,:,:,:]=EM3[None,:,NC[0]:NC[0]+NETYP,:]*fact[:,:,None,:]
   212  VOC=np.dot(EM4.reshape(ntm, NREC, NETYP*NVTYP), prod.reshape(NETYP*NVTYP,NC[1]))
```

### 整併與輸出
- 矩陣轉DataFrame，以便進行網格排放量之整併

```python
   213  sdt,ix,iy=(np.zeros(shape=(ntm*NREC),dtype=int) for i in range(3))
   214  idatetime=np.array([i for i in range(ntm)],dtype=int)
   215  for t in range(ntm):
   216      t1,t2=t*NREC,(t+1)*NREC
   217      ix[t1:t2]=list(df.IX)
   218      iy[t1:t2]=list(df.IY)
   219  for t in range(ntm):
   220      t1,t2=t*NREC,(t+1)*NREC
   221      sdt[t1:t2]=idatetime[t]
   222  dfT=DataFrame({'YJH':sdt,'IX':ix,'IY':iy})
   223  for ic in range(NC[0]):
   224      dfT[cole[ic]]=POL[:,:,ic].flatten()
   225  for ic in range(NC[1]):
   226      dfT[colv[ic]]=VOC[:,:,ic].flatten()
   227  pv=pivot_table(dfT,index=['YJH','IX','IY'],values=colv+cole,aggfunc=sum).reset_index()
```
- 準備矩陣各維度之標籤序列

```python
   228  pv.IX=[int(i) for i in pv.IX]
   229  pv.IY=[int(i) for i in pv.IY]
   230  pv.YJH=[int(i) for i in pv.YJH]
   231  imn,jmn=min(pv.IX),min(pv.IY)
   232  imx,jmx=max(max(pv.IX)+abs(imn)*2+1,ncol), max(max(pv.IY)+abs(jmn)*2+1,nrow)
   233  if imn<0 and imx+imn<ncol:sys.exit('negative indexing error in i')
   234  if jmn<0 and jmx+jmn<nrow:sys.exit('negative indexing error in j')
   235  idx=pv.index
   236  idt=np.array(pv.loc[idx,'YJH'])
   237  iy=np.array(pv.loc[idx,'IY'])
   238  ix=np.array(pv.loc[idx,'IX'])
   239
```
- 對每一污染項目逐一輸出到`nc`檔案

```python
   240  for c in colv+cole:
   241    if c not in V[3]:continue
   242    z=np.zeros(shape=(ntm,jmx,imx))
   243    ss=np.array(pv.loc[idx,c])
   244    #Note that negative indices are not bothersome and are only at the end of the axis.
   245    z[idt,iy,ix]=ss
   246  #also mapping whole matrix, NOT by parts
   247    nc.variables[c][:,0,:,:]=z[:,:nrow,:ncol]
   248  nox=nc.variables['NO'][:]+nc.variables['NO2'][:]
   249  nc.variables['NO'][:,0,:,:]=nox*0.9
   250  nc.variables['NO2'][:,0,:,:]=nox-nc.variables['NO'][:]
   251
   252  nc.close()
   253  #pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
   254  #result=os.system(pncg+' -O --out-format=uamiv '+fname+' '+fname.replace('.nc',''))
```

## 檔案下載

{% include download.html content="python程式：[lineinc.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/line/lineinc.py)" %}

## Reference
