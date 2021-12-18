---
layout: default
title: Writing Elev PTse
parent: Point Sources
grand_parent: TEDS Processing
nav_order: 4
date: 2021-12-07 17:06:30 
last_modified_date:   2021-12-07 17:06:30
---

# CAMx高空點源排放檔案之轉寫
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
- 因程式記憶體耗用太大(多達150G、DEVP之50%)，nc檔案在輸出時遭到困難。最終決定先寫成`.fth`檔案，同時也有提供中間檢查、確認的方便性。
- `feather`檔案可以說是目前壓縮比例最高、存取速度最快的資料庫檔案形式，詳情可以參考[知乎](https://zhuanlan.zhihu.com/p/247025752)。

## 程式說明

### 程式分段說明
- 調用`pandas`的版本必須含有`pyarrow`，會連動到`numpy`、`xarray`的版本
- `str2lst`：`netCDF`檔案內的字串內容必須是`bytes`格式，一般的字串要經過轉換。

```python
$ cat -n wrtE.py
     1  '''
     2  Purpose: Generate CAMx Elev. PtSe. NC file from dfMM.fth (MM=01~12)
     3  Usage: python wrtE.py YYMM
     4  see descriptions at https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/wrtE/
     5  '''
     6  #! crding = utf8
     7  from pandas import *
     8  import numpy as np
     9  import os, sys, subprocess
    10  import netCDF4
    11  import datetime
    12  from calendar import monthrange
    13
    14  from ioapi_dates import dt2jul
    15  if not sys.warnoptions:
    16      import warnings
    17      warnings.simplefilter("ignore")
    18
    19
    20  def str2lst(A):
    21      return [bytes(i,encoding='utf-8') for i in A[1:-1].replace("b'","").replace("'","").replace(" ","").split(',')][:8]
    22
    23
```
- 外部程式之相依性

```python
    24  #Main
    25  #locate the programs and root directory
    26  ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
    27  P='./'
    28
```
- 讀取引數(4碼年月)、定義起迄時間
  - CAMx的時間是LST，因此自上月最末日的早上8時開始。以同時符合CMAQ的要求(自00UTC開始)。

```python
    29  #time and space initiates
    30  ym=sys.argv[1]
    31  mm=ym[2:4]
    32  mo=int(mm)
    33  yr=2000+int(ym[:2])
    34  ntm=(monthrange(yr,mo)[1]+2)*24+1
    35  bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
    36  edate=bdate+datetime.timedelta(days=ntm/24)#monthrange(yr,mo)[1]+3)
```
- 讀取模版並進行時間軸的延長
  - 一般nc檔案的矩陣會自動以`masked array`[numpy.ma.array](https://numpy.org/doc/stable/reference/generated/numpy.ma.array.html)型式儲存，模版內容如果被遮罩遮蔽了，延長放大之後會是個災難。有關模版的mask array的檢查與修正見[另文](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/masked/)

```python
    37  #prepare the uamiv template
    38  print('template applied')
    39  NCfname='fortBE.413_teds10.ptsE'+mm+'.nc'
    40  try:
    41    nc = netCDF4.Dataset(NCfname, 'r+')
    42  except:
    43    os.system('cp '+P+'template_v7.nc '+NCfname)
    44    nc = netCDF4.Dataset(NCfname, 'r+')
    45  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    46  nt,nv,dt=nc.variables[V[2][0]].shape
    47  nv=len([i for i in V[1] if i !='CP_NO'])
    48  nc.SDATE,nc.STIME=dt2jul(bdate)
    49  nc.EDATE,nc.ETIME=dt2jul(edate)
    50  nc.NOTE='Point Emission'
    51  nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
    52  nc.NVARS=nv
```
  - 注意`name` 屬性之調用，可能會遭遇問題。

```python
    53  #Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
    54  nc.name='PTSOURCE  '
    55  nc.NSTEPS=ntm
    56  if 'ETFLAG' not in V[2]:
    57    zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
    58  if nt!=ntm or (nc.variables['TFLAG'][0,0,0]!=nc.SDATE and nc.variables['TFLAG'][0,0,1]!=nc.STIME):
    59    for t in range(ntm):
    60      sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
    61      nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    62      nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    63      ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
    64      nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    65      nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
    66  for c in V[1]:
    67    nc.variables[c].set_auto_mask(False)
    68    if c=='CP_NO': continue
    69    nc.variables[c][:]=0.
    70  nc.close()
    71  #template OK
    72
```
- 讀取逐時、逐煙道之排放量`.fth`檔案
- 讀取煙囪條件

```python
    73  df=read_feather('df'+mm+'.fth')
    74  pv=read_csv('pv'+mm+'.csv')
    75  pv.CP_NOb=[str2lst(i) for i in pv.CP_NOb]
    76  nopts=len(pv)
    77  #item sets definitions
    78  XYHDTV=['UTM_E','UTM_N','HEI','DIA','TEMP','VEL','ORI_QU1']
    79
```
- CAMx版本在此設定

```python
    80  #determination of camx version
    81  ver=7
    82  if 'XSTK' in V[0]:ver=6
    83  col_mn=['ORI_QU1','TEMP','VEL','UTM_E', 'UTM_N','HY1','HD1','DY1']
    84  lspec=[i for i in df.columns if i not in col_mn+['index','C_NO']]
    85
    86  dimn={6:'NSTK',7:'COL'}
```
- 為延長煙道數(`COL`軸)，須先將模版的`COL`軸設為可增加之[記錄軸](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#%E7%B6%AD%E5%BA%A6)(`--mk_rec_dmn`)

```python
    87  print(dimn[ver]+' expanding and reopening')
    88  res=os.system(ncks+' -O --mk_rec_dmn '+dimn[ver]+' '+NCfname+' tmp'+mm)
    89  if res!=0: sys.exit(ncks+' fail')
    90  res=os.system('mv tmp'+mm+' '+NCfname)
    91  if res!=0: sys.exit('mv fail')
```
- 準備煙囪參數的對照表
  - CAMx 6與CAMx 7的煙囪參數變數名稱有很大的改變
  - CAMx設有開啟`pig`的機制。對CMAQ沒有效果。

```python
    92  #CP_NO in S1(byte) format
    93  print('ncfile Enlargement')
    94  #prepare the parameter dicts
    95  PRM='XYHDTV'
    96  v2n={PRM[i]:XYHDTV[i] for i in range(6)}
    97  names={7:['xcoord','ycoord','stkheight','stkdiam','stktemp','stkspeed'],
    98         6:[v+'STK' for v in PRM]}
    99  v2c={PRM[i]:names[ver][i] for i in range(6)}
   100  a=DataFrame({'SN':df.SO2+df.NO2})
   101  a=a.sort_values('SN',ascending=False)
   102  pig=[]#a.index[:100]
   103  #filling the stack parameters for camx700nc
   104
```
- 再次開啟模版。關閉再開的理由是節省不必要的暫存記憶體。
  - `set_auto_mask(False)`或`set_always_mask(False)`的原因，是因為模版中有被遮蔽的矩陣內容。須先在模版階段[解決](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/masked/)。

```python
   105  nc = netCDF4.Dataset(NCfname, 'r+')
   106  #enlarge the record dimension (COL)
   107  z=np.zeros(shape=ntm)
   108  for c in V[1]:
   109    nc.variables[c].set_auto_mask(False)
   110    if c in ['CP_NO']:continue
   111    for i in range(nopts):
   112      nc.variables[c][:ntm,i]=z
   113  if ver==7:nc.variables['pigflag'][:nopts]=0
   114  nc.close()
```
- 如不再增加時間的長度，不必再將**記錄軸**設回來。

```python
   115  #res=os.system(ncks+' -O --mk_rec_dmn TSTEP '+NCfname+' tmp'+mm)
   116  #if res!=0: sys.exit(ncks+' fail')
   117  #res=os.system('mv tmp'+mm+' '+NCfname)
   118  #if res!=0: sys.exit('mv fail')
   119
```
- 寫入煙囪參數，CAMx的單位是每小時

```python   
   120  nc = netCDF4.Dataset(NCfname, 'r+')
   121  for v in PRM:
   122    var=v2c[v]
   123    nc.variables[var].set_auto_mask(False)
   124    nc.variables[var][:nopts]=np.array(pv[v2n[v]])
   125  nc.variables[v2c['V']][:nopts]=nc.variables[v2c['V']][:]*3600.
   126  nc.variables[v2c['T']][:nopts]=nc.variables[v2c['T']][:]+273.
```
- 開啟`pig`設定

```python
   127  #first 100 for PiG
   128  if len(pig)>0:
   129    if ver==7:
   130      nc.variables['pigflag'][pig]=1
   131    else:
   132      nc.variables[v2c['D']][pig]=nc.variables[v2c['D']][pig]*-1.
```
- 寫入每污染物之排放量

```python
   133  for c in V[1]:
   134    if c not in lspec:continue
   135    if c not in df.columns:continue
   136    if c in ['CP_NO']: continue
   137    ic=lspec.index(c)
   138    nc.variables[c][:,:nopts]=np.array(df[c]).reshape(ntm,nopts)
   139    print(c)
```
- 將**管煙編號**(=管編+煙道編號)寫進檔案中以備後續增、減排放源使用。
  - CMAQ雖然有`FIP`編號可供追蹤，但因`FIP`編號是整數，與國內的編碼系統不符合，且為管編，不能指定到個別煙道，因此建立自己的編號系統是必須的。
  - 且因非CAMx或CMAQ控制之變數名稱，程式會跳開不讀，並不會報錯。

```python
   140  nc.variables['CP_NO'][:nopts,:8]=np.array(list(pv.CP_NOb)).flatten().reshape(nopts,8)
   141  nox=nc.variables['NO2'][:,:nopts]
   142  nc.variables['NO'][:,:nopts]=nox[:,:nopts]*0.9
   143  nc.variables['NO2'][:,:nopts]=nox-nc.variables['NO'][:,:nopts]
   144  nc.NOPTS=nopts
   145  nc.close()
   146
```

## 檔案下載
- `python`程式：[wrtE.py](https://github.com/sinotec2/TEDS_PTSE/blob/main/wrtE.py)。


## Reference
- The NumPy community, [numpy.ma.array](https://numpy.org/doc/stable/reference/generated/numpy.ma.array.html), Jun 22, 2021
- 数据如琥珀, **轻如“鸿毛（Feather）”的文件格式却重于泰山**, [知乎](https://zhuanlan.zhihu.com/p/247025752), 2020-09-16 