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

## NCL程式

### IO

- GRIDCRO2D.nc：讀取網格點之經緯度
- COMBINE_ACONC.nc：讀取CMAQ模擬結果
- EPA_ALL2016102013.csv：該小時測站測值，由[rd_O3.py]()前處理而得。
- COUNTY_MOI_1090820.shp：內政部官網縣市界線圖檔
- rcm.000001.png, rcm.000002.png：結果圖檔

### 重要設定

- levels:0~最大值間線性區分16層
- 色階span_color_rgba：gui_default
- 圓點大小gsMarkerSizeF：0.008
- 圓點邊線gsMarkerThicknessF：0.7

### 程式下載

{% include download.html content="等值圖加上色點之NCL腳本[o3.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/o3.ncl)" %}

## 結果

![rcm.000002.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/rcm.000002.png)