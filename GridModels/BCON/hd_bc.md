---
layout: default
title: 大型網格系統切割邊界濃度
parent: Boundary Condition
grand_parent: CMAQ Model System
nav_order: 5
date: 2022-03-03 15:50:20
last_modified_date: 2022-03-03 15:50:24
---

# 大型網格系統切割邊界濃度
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
- [run_bconMM_RR_DM.csh](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/run_bconMM_RR_DM.csh)腳本應用在數十萬格以上的大型網格系統時，在[ncrcat]()連結母網格CCTM_ACONC檔案時，不但耗時、耗費磁碟機空間，非常不經濟，必須另行處理，無法使用腳本或bcon.exe程式。
- 類似情形在讀取全球模擬結果時，也曾發生過。然此處CCTM_ACONC在污染項目上與BCON檔案完全一致，座標均為直角系統，時間標籤也完全一致，因此在程式設計上較為單純。
- 當然也可以調整[run_bconMM_RR_DM.csh]()中的起迄時間，逐日進行解析，再將逐日之BCON以ncrcat連結，以避免處理連日之ACONC檔案。然因BCON檔案自0時開始，結束於0時，連結時要先去除最後1小時，程序也不容易。

## [hd_bc.py](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/hd_bc.py)程式說明
### 程式名稱
- 此程式讀取CWBWRF_15k模擬結果(格數671X395)，切割出HUADON_3k網格系統的邊界濃度(格數751X951)。

### 調用模組
- 由於母網格與子網格的格距比例較大(15k/3k=5)，因此使用`scipy.interpolate.CubicSpline`進行內插，以使結果較為均勻。

```python
import netCDF4
import numpy as np
import datetime
from bisect import bisect
from pyproj import Proj
import sys,os,subprocess
from dtconvertor import dt2jul, jul2dt
from scipy.interpolate import CubicSpline
```

### 子網格邊界檔基本環境與時間之設定
- 事先將空白邊界檔的模版準備好。調整好格數、原點、中心點等空間設定，以及模擬期程內的所有時間標籤。
- 使用pyproj的Proj進行座標轉換，將母網格位置轉成子網格系統
- 為確保填寫到正確的時間，先將逐時datetime的順利予以標籤化(idate)

```python
#open the template BC file
fname='BCON_v53_1804_run5_regrid_20180331_HUADON_3k'
nc1= netCDF4.Dataset(fname,'r+')
V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nt1,nlay1,nbnd1=nc1.variables[V1[2][1]].shape
DATES=[jul2dt([i,j]) for i,j in zip(nc1['TFLAG'][:,0,0],nc1['TFLAG'][:,0,1])]
idate={DATES[i]:i for i in range(nt1)}
SDATE=[jul2dt([i,0]) for i in set(nc1['TFLAG'][:,0,0])]
SDATE.sort()
ymds=[i.strftime("%Y%m%d") for i in SDATE]
pnyc1 = Proj(proj='lcc', datum='NAD83', lat_1=nc1.P_ALP, lat_2=nc1.P_BET,lat_0=nc1.YCENT, lon_0=nc1.XCENT, x_0=0, y_0=0.0)
x1d1=[nc1.XORIG+i*nc1.XCELL for i in range(-1,nc1.NCOLS+1)]
y1d1=[nc1.YORIG+j*nc1.YCELL for j in range(-1,nc1.NROWS+1)]
```

### 依序讀取母網格之模擬結果
- 由於網格甚多，CCTM_ACONC檔案甚大(210G per file)，採一一讀取方式，而不使用[ncrcat]()連結成單一大檔。
- 因CWBWRF_15k為40層之模擬，地面至24層之內不變，26~40採跳號執行，轉成32層之子系統
- 準備邊界軌跡中的轉角指標N0~N4。

```python    
#read the d1 CCTM_ACONC files (K40)
lay32_40={i:i for i in range(25)}
lay32_40.update({25+(i-26)//2:i for i in range(26,40,2)})
root='/u01/cmaqruns/2018base/data/output_CCTM_v53_gcc_1804_run5/CCTM_ACONC_v53_gcc_1804_run5_'
tail='_CWBWRF_15k_11.nc'
fnames=[root+ymd+tail for ymd in ymds]
# turning points among nbnd1 sequence
N0=0
N1=N0+nc1.NCOLS+1
N2=N1+nc1.NROWS+1
N3=N2+nc1.NCOLS+1
N4=N3+nc1.NROWS+1
for fname in fnames[:1]:
  nc = netCDF4.Dataset(fname,'r')
```
### 在母網格中定位子網格的4個角落
- 定位只需執行一次
- 由於子、母網格的中心點不同，有位移(dx,dy)，需先將其計算出來。
- 母網格座標系統平移到子網格上
- 以bisect在母網格x1d,y1d序列中，找到子網格4個角落的位置

```python
# interpolation indexing
  if fname==fnames[0]:
    V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
# traslation of map centers
    dx,dy=pnyc1(nc.XCENT,nc.YCENT, inverse=False)
# parent grid coordinates in new system
    x1d=[nc.XORIG+i*nc.XCELL+dx for i in range(ncol)]
    y1d=[nc.YORIG+j*nc.YCELL+dy for j in range(nrow)]
# locate the corner grids
    i0,i1=bisect(x1d,x1d1[0])-1, bisect(x1d,x1d1[-1])
    j0,j1=bisect(y1d,y1d1[0])-1, bisect(y1d,y1d1[-1])
```
### CubicSpline進行內插
- 子網格的邊界軌跡始於其西南角落，向東、向北、向西、再向南逆時針方向行進，讀取母網格數據。
- 向西、向南的順序與x1d1、y1d1相反，此處使用np.flip翻轉內插結果，填入子網格檔案。

```python
  for tt in range(nt):
    t=idate(jul2dt(nc['TFLAG'][tt,0,:]))
    for k in range(nlay1):
      kk=lay32_40[k]
# set(V[3])==set(V1[2]) ,checked before running
      for v in V[3]:
# boundary tract begin with South-West corner(j0,i0), and go around the domain in counter-clock wise direction
        nc1[v][t,k,N0:N1] =         CubicSpline(x1d[i0:i1+1], nc[v][tt,kk,j0,i0:i1+1]) (x1d1[:-1])
        nc1[v][t,k,N1:N2] =         CubicSpline(y1d[j0:j1+1], nc[v][tt,kk,j0:j1+1,i1]) (y1d1[:-1])
        nc1[v][t,k,N2:N3] = np.flip(CubicSpline(x1d[i0:i1+1], nc[v][tt,kk,j1,i0:i1+1]) (x1d1[:-1]),axis=0)
        nc1[v][t,k,N3:N4] = np.flip(CubicSpline(y1d[j0:j1+1], nc[v][tt,kk,j0:j1+1,i0]) (y1d1[:-1]),axis=0)
    print(t)
  nc.close()
nc1.close()
```


## hd_bc.py程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/hd_bc.py)

## 參考
