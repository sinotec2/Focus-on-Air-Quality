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

- Delaunay Triangulation(DT)[^1]這個主題主要目的在建立各個測站(node)之間的關聯性(edge)。
  - 當然我們可以建立倆倆的關聯，但我們也知道那樣數量太過龐大，而且不具太大的物理意義，會花費太多力氣在無謂的計算上。
  - 我們也可以定義測站的「鄰近性」，但恐怕不是一個固定的數字可以清楚定義，或具有任何客觀性。
  - 篩選沒有必要計算的組合，在graph sample and aggregate([graphSAGE][^10])過程中也是非常必要、省時的關鍵點。
- 一般在輸入NN會使用[networkx(nx)](https://networkx.org/)輸出的json檔案，而nx官網介紹地理方面應用的[範例][dg]中，就是以DT來做為範例。
- 學術上有不少的討論，可以詳見Deligiorgi and Philippopoulos(2011)[^3]、王友群與陳冠瑋(2017)[^5]、Li and Shen(2023)[^6]、Bruce Denby et al.(2005)[^7]、Boso et al.(2022)[^8]、與Diego Mendez and Miguel A. Labrador(2013)[^9]，ChatGPT的說明也鼓舞了這方面的應用[^2]。

## 模組安裝

- 經測試，geopandas和networkx之間的相依性很高，如果太舊版本的geopandas會無法啟動networkx
  - 經試誤結果，至少需要python3.8以上版本。
- 這裡就不運用[前述](Voronoi.md)的[geovoronoi](https://github.com/WZBSocialScienceCenter/geovoronoi)[^4]模組，該模組綁定版本python 3.1 <= 3.6。版本太低很多模組都無法執行。
  - 幸好libpysal也提供了繪圖的模組，libpysal有持續更新。

```python
conda create -y -p ~/.conda/envs/py39 python=3.9
conda activate /home/kuang/.conda/envs/py39
pip install --user pandas pyproj fiona geopandas
pip install --user networkx libpysal contextily
```

## 程式說明

### 相依性

```python
from libpysal import weights
from libpysal.cg import voronoi_frames
from contextily import add_basemap
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import geopandas as gpd
```

```bash
kuang@DEVP ~/MyPrograms/GraphSAGE
$ pip list
Package            Version
------------------ ----------
contextily         1.3.0
Fiona              1.9.3
geopandas          0.13.0
libpysal           4.7.0
matplotlib         3.6.3
netCDF4            1.6.3
networkx           3.1
numpy              1.23.5
pandas             2.0.1
pip                23.1.2
proj               0.2.0
pyproj             3.4.1
rasterio           1.3.6
scipy              1.10.1
shapely            2.0.1
xarray             2023.4.2
xyzservices        2023.2.0
```

### IO's

- 因為取各縣市多邊形的聯集需時較久，此處就不再重複計算，直接以[前述](Voronoi.md)的unary_union結果為邊界作圖。
  - 第1個幾何圖形即為本島外圍框線的多邊形

```python
root='/nas2/cmaqruns/2022fcst/fusion/Voronoi/'
boundary=gpd.read_file(root+'boundary_shape.shp')
boundary_shape = boundary.geometry[0]
```

- 測站也是直接讀取shp檔案
  - 同樣判斷測站是否在島內

```python
df2 = gpd.read_file(root+'stn.shp')

df2=df2.reset_index(drop=True)
for i in range(len(df2)):
    p=df2.loc[i,'geometry']
    if not p.within(boundary_shape): # or boundary_shape.exterior.distance(p) < 0.01:
        df2=df2.drop(i)
df2=df2.reset_index(drop=True)
```

### Voronoi及Delaunay的計算

- libpysal.cg.voronoi_frames和舊版的geopandas不相容(可能libpysal沒有留下舊的版本)。
- libpysal的to_networkx與舊版的networkx也不相容

```python
coordinates = np.column_stack((df2.geometry.x, df2.geometry.y))
cells, generators = voronoi_frames(coordinates, clip="convex hull")
delaunay = weights.Rook.from_dataframe(cells)
delaunay_graph = delaunay.to_networkx()
positions = dict(zip(delaunay_graph.nodes, coordinates))
```

### 繪製最終結果

- 原[範例][dg]的範圍可能很大，因為台灣範圍的zoom值(z=26)，並不在add_basemap提供的選項範圍內(z=0-18)
- 原[範例][dg]的尺寸也太小，此處予以固定figsize=(12, 10)
- 因為沒了底圖，此處增加邊框與透明底層。
- 加上圖標題

```python
ax = cells.plot(facecolor="lightblue", alpha=0.50, edgecolor="cornsilk", linewidth=2,figsize=(12, 10))
add_basemap(ax)
ax.axis("off")
boundary.plot(ax=ax, color="gray", alpha=0.50)
nx.draw(
    delaunay_graph,
    positions,
    ax=ax,
    node_size=2,
    node_color="k",
    edge_color="k",
    alpha=0.8,
)
ax.set_title('Voronoi and Delaunay links of Taiwan Air Quality Station Networks')
plt.show()
```

|![](https://raw.githubusercontent.com/sinotec2/FAQ/main/attachments/2023-04-28-10-57-17.png)|![](https://raw.githubusercontent.com/sinotec2/FAQ/main/attachments/2023-05-11-16-13-05.png)|
|:-:|:-:|
|<b>環保署測站Voronoi</b>|<b>Voronoi+Delaunay</b>|

- 雖然使用不同的模組計算Voronoi，看不出有明顯的差異。

### 程式下載

{% include download.html content="從shp檔繪製空品測站的Voronoi分區及Delaunay圖：[delaunay.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/delaunay.py)" %}

[^1]: 在數學和計算幾何領域，平面上的點集P的德勞內三角剖分是一種是点P的一个三角剖分DT(Delaunay Triangulation)，使在P中沒有點嚴格處於 DT(P) 中任意一個三角形外接圓的內部。德勞內三角剖分最大化了此三角剖分中三角形的最小角，換句話，此算法儘量避免出現「極瘦」的三角形。此算法命名來源於前苏联数学家鮑里斯·德勞內(B. Delaunay)，以紀念他自1934年在此領域的工作。([wiki](https://zh.wikipedia.org/wiki/德勞內三角剖分))。
[^2]: Delaunay graphs（德劳内图）是一种基于一组点的连通图，其中相邻点之间的边没有其他点在它们的圆形范围内。具体来说，对于点集中的每个三角形，其外接圆上没有点。Delaunay graphs 在计算几何、计算机图形学、地理信息系统等领域中有广泛的应用，例如：点集的三角剖分、地图匹配、地形建模等。(chatGPT)
[^3]: Deligiorgi, D., Philippopoulos, K. (2011). Spatial Interpolation Methodologies in Urban Air Pollution Modeling: Application for the Greater Area of Metropolitan Athens, Greece, in: Advanced Air Pollution, Edited by Farhad Nejadkoorki. [doi](https://doi.org/10.5772/17734)
[^4]: Markus Konrad markus.konrad@wzb.eu / post@mkonrad.net, March 2022, geovoronoi – a package to create and plot Voronoi regions inside geographic areas.
[^5]: Wang, Y.-C., Chen, G.-W. (2017). Efficient Data Gathering and Estimation for Metropolitan Air Quality Monitoring by Using Vehicular Sensor Networks. IEEE Trans. Veh. Technol. 66, 7234–7248. [doi](https://doi.org/10.1109/TVT.2017.2655084)
[^6]: Li, R., Shen, Z. (2023). How does foreign direct investment improve urban air quality? Environ Sci Pollut Res Int 30, 43665–43676. [doi](https://doi.org/10.1007/s11356-023-25324-x)
[^7]: Bruce Denby, Jan Horálek, Sam Erik Walker, Jaroslav Fiala (2005). Interpolation and assimilation methodsfor European scale air qualityassessment and mappingPart I: Review and recommendations. The European Topic Centre on Air and Climate Change.[ETC/ACC Technical Paper 2005/7](https://www.eionet.europa.eu/etcs/etc-atni/products/etc-atni-reports/etcacc_technpaper_2005_7_spatial_aq_interpol_part_i/@@download/file/ETCACC_TechnPaper_2005_7_SpatAQ_Interpol_Part_I.pdf)
[^8]: Boso, À., Martínez, A., Somos, M., Álvarez, B., Avedaño, C., Hofflinger, Á. (2022). No Country for Old Men. Assessing Socio-Spatial Relationships Between Air Quality Perceptions and Exposures in Southern Chile. Appl. Spatial Analysis 15, 1219–1236. [doi](https://doi.org/10.1007/s12061-022-09446-2)
[^9]: Diego Mendez, Miguel A. Labrador (2013). On Sensor Data Verification for Participatory Sensing Systems - ProQuest. [JOURNAL OF NETWORKS 8, 576.](https://www.proquest.com/openview/afc2ebb0ff60953101af08e3e6f54e15/1?pq-origsite=gscholar&cbl=136095)
[^10]: GraphSAGE: Scaling up Graph Neural Networks, Introduction to GraphSAGE with PyTorch Geometric, by Maxime Labonne(2022), Towards Data Science, Published in Towards Data Science, Apr 21, [2022][sage]

[dg]: https://networkx.org/documentation/latest/auto_examples/geospatial/plot_delaunay.html#sphx-glr-auto-examples-geospatial-plot-delaunay-py "Delaunay graphs from geographic points"
[sage]: https://towardsdatascience.com/introduction-to-graphsage-in-python-a9e7f9ecf9d7 "GraphSAGE: Scaling up Graph Neural Networks"