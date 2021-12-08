---
layout: default
title: "WRF_3Km空間內插"
parent: "cwb WRF_3Km"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-30 10:43:16
---

# WRF_3Km空間內插

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
- 續[樓上](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/)、以及[下載](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/get_M-A0064/)程序之說明，此處詳述水平內插之細節。
- 由於`grb2`檔案與`wrfout_d04`的解析度相同、又是等間距直角座標系統，似乎網格系統的互換沒有問題，實則2個系統的原點不一樣，投影也略有差異，因此還是必須建立內插模式。

## [gen_D4bin.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/cwbWRF_3Km/gen_D4bin.py_txt)分段說明
- 引用模組
```python
     1  import netCDF4
     2  import numpy as np
     3  import os
     4  import twd97
     5  from scipy.io import FortranFile
     6  from bisect import bisect
     7
```
- 分別開啟`grb2`及`wrfout_d04`檔案。前者先經`ncl_convert2nc`轉成`nc`檔案，以方便讀取。
```python
     8  fname='M-A0064-084.nc'
     9  nc = netCDF4.Dataset(fname,'r')
    10  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    11  nlay,nrow,ncol=nc.variables[V[2][0]].shape
    12
    13  nc1= netCDF4.Dataset('wrfout_d04_2020-06-14_06:00:00','r+')
    14  V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
    15  nt1,nlay1,nrow1,ncol1=nc1.variables[V1[3][3]].shape
    16
```
- 建立2個檔案的座標系統
  - `wrfout_d04`的變數為`XLONG`、`XLAT`，`grb2`則為`gridlon_0`、`gridlat_0`。
  - 此處以`twd97`模組進行轉換
```python
    17  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
    18  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    19
    20  xlon,xlat=nc1.variables['XLONG'][0,:,:].flatten(),nc1.variables['XLAT'][0,:,:].flatten()
    21  xy1=np.array([twd97.fromwgs84(i, j) for i, j in zip(xlat, xlon)])
    22  x1,y1=(xy1[:,i].reshape(nrow1,ncol1) for i in range(2))
    23
    24  xlon,xlat=nc.variables['gridlon_0'][:,:].flatten(),nc.variables['gridlat_0'][:,:].flatten()
    25  xy=np.array([twd97.fromwgs84(i, j) for i, j in zip(xlat, xlon)])
    26  x,y=(xy[:,i].reshape(nrow,ncol) for i in range(2))
    27
```
- 找到每個`wrfout_d04`座標點在`grb2`系統的位置標籤`idx`
  - 1格對應到至少1格者
```python
    28  idx=np.zeros(shape=(nrow1,ncol1,2),dtype=np.int)
    29  for j in range(nrow1):
    30    min_j=min([bisect(list(y[:,ii]),y1[j,0]) for ii in range(ncol)])-1
    31    min_i=min([bisect(list(x[jj,:]),x1[j,0]) for jj in range(nrow)])-1
    32    max_j=max([bisect(list(y[:,ii]),y1[j,-1]) for ii in range(ncol)])+1
    33    max_i=max([bisect(list(x[jj,:]),x1[j,-1]) for jj in range(nrow)])+1
    34    for i in range(ncol1):
    35      for jj in range(min_j,max_j):
    36        for ii in range(min_i,max_i):
    37          if x[jj,ii]<=x1[j,i]<=x[jj+1,ii+1] and y[jj,ii]<=y1[j,i]<=y[jj+1,ii+1]:(idx[j,i,0],idx[j,i,1])=(jj,ii)
    38
```
  - 對應不到的狀況，將以距離最近的4個網格來進行內插
```python
    39  idx0=np.where(idx==0)
    40  for j,i in zip(idx0[0],idx0[1]):
    41    min_j=min([bisect(list(y[:,ii]),y1[j,i]) for ii in range(ncol)])-1
    42    min_i=min([bisect(list(x[jj,:]),x1[j,i]) for jj in range(nrow)])-1
    43    max_j=max([bisect(list(y[:,ii]),y1[j,i]) for ii in range(ncol)])+1
    44    max_i=max([bisect(list(x[jj,:]),x1[j,i]) for jj in range(nrow)])+1
    45    xr=x[min_j:max_j,min_i:max_i]
    46    yr=y[min_j:max_j,min_i:max_i]
    47    di=np.sqrt((xr-x1[j,i])**2+(yr-y1[j,i])**2)
    48    dis=di.flatten()
    49    dis.sort()
    50    ii,jj=[],[]
    51    for k in range(4):
    52      min_k=np.where(di==dis[k])
    53      jj.append(min_j+min_k[0])
    54      ii.append(min_i+min_k[1])
    55    idx[j,i,0],idx[j,i,1]=(min(jj),min(ii))
    56
```
- 計算4個網格點的加權值(距離反比)
```python
    57  wts=np.zeros(shape=(nrow1,ncol1,4),dtype=np.float64)
    58  one=np.ones(shape=(nrow1,ncol1),dtype=np.int64)
    59  kk=0
    60  for jj in [0,1]:
    61    for ii in [0,1]:
    62      xr,yr=x[idx[:,:,0]+one*jj,idx[:,:,1]+one*ii],y[idx[:,:,0]+one*jj,idx[:,:,1]+one*ii]
    63      wts[:,:,kk]=one/((xr-x1)**2+(yr-y1)**2)
    64      kk+=1
    65  sum_wts=np.sum(wts,axis=2)
    66  for kk in range(4):
    67     wts[:,:,kk]=wts[:,:,kk]/sum_wts[:,:]
```
- 寫出檔案備用
```python
    68  fname = 'idxD4.bin'
    69  with FortranFile(fname, 'w') as f:
    70    f.write_record(idx)
    71  fname = 'wtsD4.bin'
    72  with FortranFile(fname, 'w') as f:
    73    f.write_record(wts)
```

## 下載程式碼
- 可以由[github](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/cwbWRF_3Km/gen_D4bin.py_txt)找到原始碼。

## 檢核

## Reference
