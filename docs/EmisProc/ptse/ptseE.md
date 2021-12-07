---
layout: default
title: "EPs Emis for CAMx"
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
- 高空點源的**時變係數**檔案需按CEMS數據先行[展開](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptseE_ONS/)。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式

## 副程式說明

### [ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)

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
for m in 0{1..9} 1{0..2};do python python wrtE.py 19$m;done
```

###
- 調用模組
  - 因無另存處理過後的資料庫，因此程式還是會用到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式`CORRECT`, `add_PMS`, `check_nan`, `check_landsea`, `FillNan`, `WGS_TWD`, `Elev_YPM`

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
    26  mm=sys.argv[1][2:4]
    27  mo=int(mm)
    28  yr=2000+int(sys.argv[1][:2])
```
- 使用`Hs`進行篩選「高空」點源

```python   
    29  Hs=0 #cutting height of stacks
```
- 起迄日期、模擬範圍中心點位置
```python   
    30  ntm=(monthrange(yr,mo)[1]+2)*24+1
    31  bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
    32  edate=bdate+datetime.timedelta(days=ntm/24)#monthrange(yr,mo)[1]+3)
    33  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
    34  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
```
- nc模版的應用與延長

```python   
    35  #prepare the uamiv template
    36  print('template applied')
    37  NCfname='fortBE.413_teds10.ptsE'+mm+'.nc'
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
    52  nc.name='PTSOURCE  '
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
- 讀取點源資料庫並進行品質管控

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
- 對

```python   
   101  #pivot table along the dimension of NO_S (P???)
   102  df_cp=pivot_table(df,index='CP_NO',values=cole+['ORI_QU1'],aggfunc=sum).reset_index()
   103  df_xy=pivot_table(df,index='CP_NO',values=XYHDTV+colT,aggfunc=np.mean).reset_index()
   104  df_sc=pivot_table(df,index='CP_NO',values='SCC', aggfunc=mostfreqword).reset_index()
   105  df1=merge(df_cp,df_xy,on='CP_NO')
   106  df=merge(df1,df_sc,on='CP_NO')
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```
-
```python   
```

### 輸出結果 

-
```python   
```


## 檔案下載
- `python`程式：[ptseE_ONS.py](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/ptse/ptseE_ONS.py)。
- `jupyter-notebook`檔案[ptseE_ONS.ipynb](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/ptse/ptseE_ONS.ipynb)

## Reference
