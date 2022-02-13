---
layout: default
title: PLOTFILE to KML
parent: OU Pathways
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-02-12 19:52:38
---
# PLOTFILE to KML
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
- PLOTFILE指令將會產生所有接受點(網格及離散點)的濃度結果、以及接受點的高程等訊息。
- 除了可以使用SURFER等軟體進行等值圖的繪製之外，此處將PLOTFILE轉成KML檔案，以運用快速便捷的網路地圖貼圖功能。
  - 使用[legacycontour._cntr](https://github.com/matplotlib/legacycontour)模組
  - 安裝：可動態連結github，或下載完整原始碼再`python setup.py install`
  - KML檔案之寫出，可以參考[等值圖KML檔之撰寫](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)

## 讀取PLOTFILE
### [PLT2kml.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/OU_pathways/PLT2kml.py)之執行
- 引數：PLOTFILE輸入檔名稱
- 結果：
  - .kml:等濃度圖檔,以google map或OSM等界面貼圖
  - .grd:以SURFER繪圖
  
### PLOTFILE範例
-  ISC和AERMOD的PLOTFILE非常類似，如下所示：

```bash
* AERMOD ( 19191):  A Simple Example Problem for the AERMOD Model with PRIME                03/28/21
* AERMET ( 15181):                                                                          17:48:56
* MODELING OPTIONS USED:   RegDFAULT  CONC  ELEV  RURAL  MMIF_Data
*         PLOT FILE OF PERIOD VALUES AVERAGED ACROSS   0 YEARS FOR SOURCE GROUP: ALL     
*         FOR A TOTAL OF  1600 RECEPTORS.
*         FORMAT: (3(1X,F13.5),3(1X,F8.2),2X,A6,2X,A8,2X,I8.8,2X,A8)                                                                                                                                                      
*        X             Y      AVERAGE CONC    ZELEV    ZHILL    ZFLAG    AVE     GRP      NUM HRS   NET ID
* ____________  ____________  ____________   ______   ______   ______  ______  ________  ________  ________
  271200.00000 2765700.00000       0.01421    39.00    39.00     0.00  PERIOD  ALL       00008761  LINKO   
  271520.00000 2765700.00000       0.01309    41.30    41.30     0.00  PERIOD  ALL       00008761  LINKO   
  271840.00000 2765700.00000       0.01203    41.70    41.70     0.00  PERIOD  ALL       00008761  LINKO   
  272160.00000 2765700.00000       0.01106    47.00    47.00     0.00  PERIOD  ALL       00008761  LINKO   
  272480.00000 2765700.00000       0.01028    50.40    52.00     0.00  PERIOD  ALL       00008761  LINKO   
  272800.00000 2765700.00000       0.00975    47.00    48.00     0.00  PERIOD  ALL       00008761  LINKO   
...
  283680.00000 2778180.00000       0.02015   -15.50   -15.50     0.00  PERIOD  ALL       00008761  LINKO   
```
- 讀取時先將所有內容按行讀入，再一一分解。

### 程式說明
- desc:有關模擬個案的敘述（TITLEONE）
- x,y,c：東西向、南北向座標值，濃度序列

```python
# read the iscst result plot file, must be in TWD97-m system, with 8 lines as header
with open(fname, 'r') as f:
  g = [line for line in f]
#description txt is read from the third line
desc = ' '
if g[0][0:3] in ['* A','* I']:
  desc = g[:3]
  g = g[8:]
lg = len(g)
x, y, c = (np.array([float(i.split()[j]) for i in g]) for j in range(3))
```

## REGRID
### REGRID的理由
- PLOTFILE會將離散點結果寫在網格接受點之後，不見得都是網格結果，因此建議還是重寫進行網格化、重新內插會比較單純。

### REGRID系統參數
  - 重新估計東西與南北網格數nx,ny
  - 以最小及最大座標值範圍除以網格數，成為間距dx,dy
  - 重新給定x_mesh,y_mesh, 產生2維座標值
  - 以twd97進行中心點經緯度之求取、平移座標系統到中心點。
  - 以Porj進行經緯度計算
  - 以scipy.interpolate.griddata進行內插。

```python
# 1-d X/Y coordinates
fac=1.
nx, ny = int(max(int(np.sqrt(lg)), len(set(x)))*fac),int(max(int(np.sqrt(lg)), len(set(y)))*fac)

#the domain of meshes must smaller than data domain to avoid extra_polation
dx, dy=(np.max(x)-np.min(x))/nx,(np.max(y)-np.min(y))/ny
x_mesh = np.linspace(np.min(x)+dx, np.max(x)-dx, nx)
y_mesh = np.linspace(np.min(y)+dy, np.max(y)-dy, ny)
Xcent, Ycent = (x[0]+x[-1])/2.,(y[0]+y[-1])/2.
Lat, Lon=twd97.towgs84(Xcent, Ycent)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=Lat, lon_0=Lon, x_0=0, y_0=0.0)
# 2-d mesh coordinates, both in TWD97 and WGS84
x_g, y_g = np.meshgrid(x_mesh, y_mesh)

#lat,lon pairs are used in KML locations
xgl,ygl=x_g-Xcent,y_g-Ycent
lon,lat=pnyc(xgl, ygl, inverse=True)
points=[(i,j) for i,j in zip(x,y)]
grid_z2 = griddata(points, c, (x_g, y_g), method='linear')
```

### 等值線圖繪製
- 呼叫[cntr_kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/cntr_kml.py)
- 參考[等值線之KML檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)之說明

## [PLT2kml.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/OU_pathways/PLT2kml.py)下載
- [FAQ](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/OU_pathways/PLT2kml.py)  