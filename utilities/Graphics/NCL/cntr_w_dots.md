---
layout: default
title: 等值圖加上色點
parent: NCL Programs
grand_parent: Graphics
has_children: true
date: 2023-02-01
last_modified_date: 2023-02-01 11:09:54
tags: NCL graphics 
---

# 等值圖加上色點
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

- ncl參考：[NCL Graphics: Regional Climate Model](https://www.ncl.ucar.edu/Applications/rcm.shtml)

## NCL程式

### IO

- GRIDCRO2D.nc：讀取網格點之經緯度
- COMBINE_ACONC.nc：讀取CMAQ模擬結果
- EPA_ALL2016102013.csv：該小時測站測值，由[rd_O3.py][1]前處理而得。
- COUNTY_MOI_1090820.shp：內政部官網縣市界線圖檔
- rcm.000001.png, rcm.000002.png：結果圖檔

### 重要設定

- levels:0~最大值間線性區分16層
- 色階span_color_rgba：gui_default
- 圓點大小gsMarkerSizeF：0.008
- 圓點邊線gsMarkerThicknessF：0.7

### 程式下載

{% include download.html content="等值圖加上色點之NCL腳本[o3.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/o3.ncl)" %}

## 前處理程式

- 因NCL需要測站的經緯度座標，[rd_O3.py][1]除了讀取該小時測值外，另行加上測站位置座標。

### IO

- 引數：*YYYYMMDDHH*
- 外部程式：[specHrSliderRect.py](../../../AQana/TWNAQ/specHrSlider.md)
- 測站經緯度：`/nas1/cmaqruns/2019base/data/wsites/sta_ll.csv`
- 無表頭、無行號之csv檔(lat,lon,O3)：EPA_ALL*YYYYMMDDHH*.csv

### 程式下載

{% include download.html content="全台測站濃度前處理程式[rd_O3.py][1]" %}

## 結果

|![rcm.000002.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/rcm.000002.png)|![PM25.000002.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM25.000002.png)|
|:-:|:-:|
|<p><br>2016年10月20日海馬颱風外圍環流</p>造成竹苗地區臭氧高值之CMAQ模擬結果</br>|<br>2019全年PM2.5模擬與測站平均結果<br>|

[1]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/rd_O3.py "全台測站濃度前處理程式[rd_O3.py]"
