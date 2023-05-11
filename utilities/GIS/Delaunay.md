---
layout: default
title:  空品測站之Delaunay圖
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2023-05-11 16:01:26
tags: GIS Voronoi Delaunay
---

# 空品測站之Delaunay圖
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

- Delaunay Graph[^1]這個主題主要目的在建立各個測站(node)之間的關聯性(edge)，當然我們可以建立倆倆的關聯，但我們也知道那樣數量太過龐大，而且不切實際。
- 一般在輸入CNN會使用[networkx(nx)](https://networkx.org/)輸出的json檔案，而nx官網介紹地理方面應用的範例中，就是以

## 程式說明

- 程式運用到第3方模組[geovoronoi](https://github.com/WZBSocialScienceCenter/geovoronoi)[^4]，綁定版本python 3.1 <= 3.6。過高版本將無法執行。

### 相依性

```python
import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.ops import cascaded_union, unary_union
from shapely.geometry import Point
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords
```

- 安裝過程有些順序需要遵守

```python
 1382  pip install --user pyproj
 1383  pip install --user fiona
 1384  pip install --user geovoronoi
 1390  pip install --user descartes
```

- python3.6早期的netCDF安裝過程需指定HDF5及netCDF4的包括檔頭(header of include files)環境變數，否則裝不起來

```bash
export NETCDF4_DIR=/opt/netcdf/netcdf4_gcc
export HDF5_DIR=/opt/hdf/hdf5_gcc
pip install netCDF4
```

### IO's

- 讀取內政部之縣市界shp檔。從中讀取本島海岸線範圍(島內縣市範圍之聯集)。
  - 採排他法：去除金門澎湖與連江範圍之物件
  - 本島縣市也可能有離島(綠島、蘭嶼、龜山、小琉球等)，因此以最大面積之多邊形為代表。這個邏輯需要每個縣市一一檢討。

```python
shp_fname="/home/kuang/bin/TWN_COUNTY.shp"
gdf = gpd.read_file(shp_fname)

CNTYNAM=set(gdf.COUNTYNAME)-{'金門縣','澎湖縣','連江縣'}
ifirst=1
for c in list(CNTYNAM)[:]:
    a=gdf.loc[gdf.COUNTYNAME==c].reset_index(drop=True)
    area=[i.area for i in a.geometry]
    imax=area.index(max(area))
    if len(a)==1:
        b=a.to_crs(epsg=4326)
    else:
        b=a.loc[a.index==imax].reset_index(drop=True).to_crs(epsg=4326)
    if ifirst==1:
        df0=b.to_crs(epsg=4326)
        ifirst=0
    else:
        df0=gpd.GeoDataFrame(pd.concat([df0,b],ignore_index=True))
```

- 讀取[測站經緯度csv檔案](../../GridModels/POST/6.wsite.md#測站模擬值之讀取)
  - 並將資料表寫成GeoDataFrame方便後續繪圖

```python
stn=pd.read_csv('/nas1/cmaqruns/2016base/data/sites/sta_ll.csv')
stnpnt=[Point(i,j) for i,j in zip(stn.lon,stn.lat)]

for i in range(len(stn)):
    b=gpd.GeoDataFrame({'COUNTYSN':stn.loc[i,'ID'] ,'COUNTYNAME':stn.loc[i,'New'],'geometry':[stnpnt[i]]})
    df0=gpd.GeoDataFrame(pd.concat([df0,b],ignore_index=True))

df1=df0.loc[:21]
df1.to_file('mainisland.shp',mode='w')
df2=df0.loc[22:]
df1.to_file('stn.shp',mode='w')
```

### 取本島海岸線範圍內的測點

- 理論上`plot_voronoi_polys_with_points_in_area`似乎會直接繪製範圍界線內的點，但似乎程式不允許界線外存在有點。
- 使用`within`函數來判斷。(與邊界的距離長短似乎沒有作用)

```python
boundary = gpd.read_file("mainisland.shp")
boundary = boundary.to_crs(epsg=4326)
boundary_shape = unary_union(boundary.geometry)

df2=df2.reset_index(drop=True)
for i in range(len(df2)):
    p=df2.loc[i,'geometry']
    if not p.within(boundary_shape): # or boundary_shape.exterior.distance(p) < 0.01:
        df2=df2.drop(i)
df2=df2.reset_index(drop=True)
```

### 執行第3方模組

- `points_to_coords`這個函數是否有必要值得挑戰，檢討原始碼發現也沒有太大的作用，就是將geometry形式的物件改成array而已。
- 此處主要呼叫`voronoi_regions_from_coords`，會輸出2個字典(dict)，編號為其內定順序，並無意義，只是用來串聯點及多邊形。 
  - 如果需要測點原來的ID，還是需要從[測站經緯度csv檔案](../../GridModels/POST/6.wsite.md#測站模擬值之讀取)來連結。

```python
gdf_proj = df2.to_crs(boundary.crs)
coords = points_to_coords(gdf_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, boundary_shape)
```

### 繪製本島之邊框範圍

- 做為測試邊框及內部測點

```python
boundary = gpd.read_file("mainisland.shp")
fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color="gray")
df1.plot(ax=ax, markersize=3.5)#, color="brown")
df2.plot(ax=ax, markersize=3.5, color="brown")
ax.axis("off")
plt.axis("equal")
plt.show()
```

### 繪製最終結果

```python
fig, ax = subplot_for_map(figsize=(12, 10))
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, region_polys, coords, region_pts)
ax.set_title('Voronoi regions of Air Quality Station Networks')
plt.tight_layout()
plt.show()
```

![](https://raw.githubusercontent.com/sinotec2/FAQ/main/attachments/2023-04-28-10-57-17.png)|![](https://raw.githubusercontent.com/sinotec2/FAQ/main/attachments/2023-05-11-16-13-05.png)
|:-:|:-:|
|<b>環保署測站</b>|<b>環保署+微型感測</b>|

- 大致還能保持方、圓形為主的分布，表示測站在範圍內還算均勻分配。
- 細長條情況仍然存在(如屏東站)，然較[Sinica][sinica]少很多。

### 程式下載

{% include download.html content="從shp檔繪製空品測站的Voronoi分區圖：[Voronoi.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/Voronoi.py)" %}


[^1]: 在數學和計算幾何領域，平面上的點集P的德勞內三角剖分是一種是点P的一个三角剖分DT，使在P中沒有點嚴格處於 DT(P) 中任意一個三角形外接圓的內部。德勞內三角剖分最大化了此三角剖分中三角形的最小角，換句話，此算法儘量避免出現「極瘦」的三角形。此算法命名來源於鮑里斯·德勞內(B. Delaunay)，以紀念他自1934年在此領域的工作。([wiki](https://zh.wikipedia.org/wiki/德勞內三角剖分))。

[sinica]: https://pm25.lass-net.org/GIS/voronoi/ "PM2.5 開放資料入口網站"