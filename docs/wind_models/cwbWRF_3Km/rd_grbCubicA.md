---
layout: default
title: "grb2nc轉檔"
parent: "cwb WRF_3Km"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-30 10:43:16
---

# grb2nc轉檔

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
- 續[樓上](https://sinotec2.github.io/jtd/docs/wind_models/cwbWRF_3Km/)、以及[下載](https://sinotec2.github.io/jtd/docs/wind_models/cwbWRF_3Km/get_M-A0064/)程序之說明，此處詳述轉檔歷程。
- 雖然`grb2`格式也有其解讀、應用的軟體，然而在空氣污染領域還並不多。因此還是需要轉成`wrfout`的`nc`格式。
- 此處應用pygrib模組進行`grb2`檔案的解析

## rd_grbCubicA.py分段說明
- 引用模組
  - pygrib的建置比較特別，可以參考[pygrib的安裝、重要語法](http://www.evernote.com/l/AH12nyLrGkBL2qg3WTonSwDC-0Rtq_S9npA/)
  - 其餘時間內插使用到CubicSpline，空間內差使用到interp1d
```python
kuang@MiniWei /Users/Data/cwb/WRF_3Km
$ cat -n rd_grbCubicA.py
     1  #!/opt/anaconda3/envs/gribby/bin/python
     2  import pygrib
     3  import numpy as np
     4  import netCDF4
     5  from scipy.io import FortranFile
     6  from scipy.interpolate import CubicSpline
     7  from scipy.interpolate import interp1d
     8  import datetime
     9  import os
    10  import subprocess
    11
```
- 溫度轉飽和蒸汽壓[Arden Buck equation](https://www.omnicalculator.com/chemistry/vapour-pressure-of-water)
```python
    12  def buck(K):
    13      C=K-273.
    14      return 611.21*np.exp((18.678-C/234.5)*C/(257.14+C))
    15
    16
```
- 開啟模版、讀取d04的網格數
  - 由於wrfout的變數較`grb2`檔案還多，需事先處理好(`ncks -O -x -v VAR1,VAR2... $oldNC $newNC`)。
  - 
```python
    17  fname='wrfout_d04'
    18  tmax=36+1
    19  nc = netCDF4.Dataset(fname,'r+')
    20  Vs=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    21  nt1,nrow1,ncol1=(nc.variables['U10'].shape[i] for i in range(3))
    22
```
- 讀取空間內插之**標籤**檔案`idxD4.bin`、**權重矩陣**檔案`wtsD4.bin`
  - 因2個網格系統的位置不會隨時間改變，可以事先處理好備用。
```python
    23  #path='/Users/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/raw/'
    24  #path='/home/cpuff/UNRESPForecastingSystem/CWB_data/raw/'
    25  #path='/nas1/backup/data/CWB_data/raw/'
    26  path='/Users/Data/cwb/WRF_3Km/'
    27  f=FortranFile(path+'idxD4.bin', 'r')
    28  idx=f.read_record(dtype=np.int64)
    29  idx=idx.reshape(nrow1,ncol1,2)
    30
    31  f=FortranFile(path+'wtsD4.bin', 'r')
    32  wts=f.read_record(dtype=np.float64)
    33  wts=wts.reshape(nrow1,ncol1,4)
    34
```
- 時間迴圈前之準備
  - `atbs`:變數名稱對照表，**短**名稱為`wrfout`內的名稱，**長**名稱為`grb2`內的變數屬性
```python
    35  one=np.ones(shape=(nrow1,ncol1),dtype=np.int64)
    36  atbs={'U10': '10 metre U wind component',
    37   'V10': '10 metre V wind component',
    38   'T': 'Temperature',
    39   'V': 'V component of wind',
    40   'U': 'U component of wind',
    41   'W': 'Geometric vertical velocity',
    42   'QVAPOR': 'Relative humidity',
    43   'T2': '2 metre temperature',
    44   'SST': 'Temperature',
    45   'TSK': 'Skin temperature',
    46   'SWNORM': 'Net short-wave radiation flux (surface)',
    47   'SWDOWN': 'Net short-wave radiation flux (surface)',
    48   'PHB': 'Geopotential Height',
    49   'PSFC': 'Surface pressure',
    50   'RAINC':'Total precipitation'}
```
  - `atbs2`:3維變數
```python
    51  atbs2=[]
    52  for v in atbs:
    53    if v in Vs[2]:atbs2.append(v)
    54  #'U10','V10','T2','SWNORM','SWDOWN','PSFC','SST','TSK']
    55  #atbs2.append('TSLB') #3d in grb but 4d in wrfout
```
- 開啟變數陣列
  - `b`為時間標籤
  - 每個atbs項目都有自己的陣列(`s`開頭的全時間變數)
  - `grb2`的高度順序是相反的，`lv`為其標籤。
```python
    56  b=[t for t in range(0,tmax)]
    57  for a in atbs:
    58    if a in atbs2:
    59      exec('s'+a+'=np.zeros(shape=(tmax,nrow1,ncol1),dtype=np.float64)')
    60    else:
    61      exec('s'+a+'=np.zeros(shape=(tmax,11,nrow1,ncol1),dtype=np.float64)')
    62   #'GPH': 'Geopotential Height',
    63
    64  lv=[i for i in range(10,-1,-1)]
    65  PB,level=[],[]
    66
```
- 開始時間迴圈、開啟`grb2`檔案  
```python
    67  for t in range(0,tmax,6):
    68    fname='M-A0064-0'+'{:02d}'.format(t)+'.grb2'
    69    grbs = pygrib.open(fname)
    70
```
- 除累積雨量外、讀取每一`grb2`變數
  - `len(grb)==1`：只有一層數據
  - 有11層數據者：要記得高度須**反向**儲存
  - 海溫`SST`設定為**地面**溫度
```python
    71    for a in set(atbs)-set(['RAINC']):
    72      grb = grbs.select(name=atbs[a])
    73      if len(grb)==1:
    74        cmd=a+'=grb[0].values'
    75        exec(cmd)
    76      else:
    77        arr=[]
    78        for k in range(11):
    79          arr.append(grb[lv[k]].values)
    80        arr=np.array(arr)
    81        exec(a+'=arr')
    82      if len(grb)==11 and len(level)==0:
    83        level=[grb[lv[i]].level for i in range(11)]
    84      if len(grb)==12 and a=='SST':SST=grb[11].values
```
- 由`gr2`的相對濕度計算`wrfout`中的水汽量
```python
    85    nlay,nrow,ncol=QVAPOR.shape
    86    if len(PB)==0:
    87      PB=np.ones(shape=(nlay,nrow,ncol),dtype=np.int64)
    88      for k in range(nlay):
    89        PB[k,:,:]=level[k]*100
    90    ps=buck(T)
    91    QVAPOR=QVAPOR/100.*(ps*18.)/(PB*28.)
    92
```
- 
```python
```


## 檢核
- 可以使用[MeteoInfo](http://meteothink.org/)或[CWB網站](https://npd.cwb.gov.tw/NPD/products_display/product?menu_index=1)

## Reference
- sinotec2, **pygrib的安裝、重要語法**, [evernote](http://www.evernote.com/l/AH12nyLrGkBL2qg3WTonSwDC-0Rtq_S9npA/), 2021年4月1日
- Yaqiang Wang, **MeteoInfo Introduction**, [meteothink](http://meteothink.org/), 2021,10,16