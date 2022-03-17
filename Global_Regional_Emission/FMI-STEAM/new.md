---
layout: default
title: 船隻排放之處理_CMAQ
parent: STEAM Emission Processing
grand_parent: Global/Regional Emission
nav_order: 2
date: 2022-02-05 16:09:08
last_modified_date: 2022-02-05 16:09:11
---

# 全球船隻排放量之處理_CMAQ
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
- 主要依據[CAMx] (/Focus-on-Air-Quality/REASnFMI/FMI-STEAM/old/)的處理與griddata的[內插](/Focus-on-Air-Quality/GridModels/LAND/Soils/#nasa-gldas)經驗。
  - 由於FMI-STEAM全球船隻排放的解析度較低，因此採用griddata內插方式轉換座標系統。
  - 污染項目直接使用REAS2CMAQ.csv。
  - 不再轉成Mozart模式檔案格式或CAMx排放檔案，直接產生CMAQ地面排放檔案


## 程式說明
- 網格面積的計算方式：採取array批次計算，較迴圈計算更快，且因只有緯度方向有變異，採用arry[None,:,None]方式即可搭配應用在3維變數中。
- 直接轉換到CMAQ模式，參考[reas2cmaq](/Focus-on-Air-Quality/REASnFMI/REAS/reas2cmaq/)的對照方式
- 因FMI-STEAM檔案為全年逐日，此處縮減為選取當月，以減省記憶體容量。空間上則無篩選，直接使用griddata內插

### 單位轉換
- FMI-STEAM 排放量的單位為kg/day/grid_cell。其grid_cell是非等間距之經緯度網格，因此需先計算原系統之網格面積，轉換為單位面積排放量，才能進行內插。
- area為南北1維之面積，約為5x5~27x5 平方公里
- lat並非由-90~+90，因此要特別處理之。
- 東西方向的寬度並非等間具，以梯形方式計算。
- NOx(3階矩陣)與面積(1階矩陣)之相除，在沒有維度的方向補上[空值None](https://www.796t.com/post/ZWNndnc=.html)
  - 有關矩陣形狀不同情況下進行逐項計算，請參考[筆記:矩陣階層numpy.newaxis(None)的用法](/Focus-on-Air-Quality/utilities/netCDF/MatrixRankNone/)。

```python
pi=3.14159265359
peri_x=40075.02
peri_y=40008
r_x=peri_x/2./pi
r_y=peri_y/2./pi
dlon=(max(lst['lon'])-min(lst['lon']))/(ncol-1)
dlat=(max(lst['lat'])-min(lst['lat']))/(nrow-1)
lat,lon=np.array(lst['lat']),np.array(lst['lon'])
rad=abs(lat/90.)*pi/2.
r=(r_x*np.cos(rad)+r_y*np.sin(pi/2.-rad))/2.
dx=2.*pi*r * dlon/360.
dx=list(dx)+[dx[-1]]
dx=np.array([(dx[i]+dx[i+1])/2. for i in range(nrow)])  
dy=dlat/180.*(peri_x*np.cos(rad)**2+peri_y*np.sin(rad)**2)/2.
area=dx*dy
NOx=NOx/area[None,:,None] #kg/day/KM^2
...
NOx=NOx[min(js):max(js)+1,:,:]*nc.XCELL/1000*nc.YCELL/1000 #kg/day/GRID-CELL
```
- kg/day轉成gmole/s

```python
facG=1E3/24/3600. # 10^3 for kg/day to gmole/s
unit_SHIP={i:facG/mw for i,mw in zip(spec,mw)}
```
- 乘上物種間的排放比例
```python
    rat=list(dfm.loc[dfm.spec==s,'sum_file'])[0]/vNOx
    if s=='NOx': rat=1.
    arr=np.zeros(shape=(len(idt),nrow,ncol))
    arr[:,:,:]=var[None,:,:]*rat*unit_SHIP[s]
```    

### griddata 內插
- 此處因原網格較粗，因此採用內插方式，以轉換至CWBWRF_15k座標系統

```python
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
lonm, latm = np.meshgrid(lst['lon'],lst['lat'])
x,y=pnyc(lonm,latm, inverse=False)
boo=(abs(x) <= (maxx - minx) /2+nc.XCELL*10) & (abs(y) <= (maxy - miny) /2+nc.YCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]
...
  NOx2d=NOx[js[idt[0]],:,:]
  var=np.zeros(shape=(nrow,ncol))
  c = NOx2d[idx[0][:],idx[1][:]]
  var[:,:] = griddata(xyc, c[:], (x1, y1), method='linear')
```

### 程式碼
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/ship2cmaq.py)

### 後處理
- [按日拆分m3.nc檔案](/Focus-on-Air-Quality/utilities/netCDF/brk_day/#brk_day2cs腳本程式)

## Results

| ![ship_co.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/ship_co.PNG) |
|:--:|
| <b>圖 d01範圍船舶CO排放之分布(log gmole/s)</b>|  



