---
layout: default
title:  軌跡線貼在Marble底圖上
parent: NCL
grand_parent: Graphics
last_modified_date: 2023-07-21 11:31:15
tags: NCL graphics traj_model Marble
---

# 軌跡線貼在Marble底圖上

{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## 背景

- 除了研究與報告試誤過程中的貼版之外，對於印刷品質要求較高的完稿，會需要使用更高解析度的地形圖做為背景底圖，這是NCL
的強項之一。
- 這個系列延續自[反軌跡線通過網格機率分布圖](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL/prob2png/)之底圖，以WPS 333公尺解析度地形高程為基底，貼上縣市界、並視軌跡線的範圍需要，減小圖面尺促以加大局部內容細節。
- 下載ncl[程式碼](./taiMarbleScale.ncl)

## 程式說明

- 程式可以獨立執行，也可搭配cgi-python呼叫`os.system`

### 輸入檔案

- WPS 333公尺解析度地形高程：`/nas1/WRF4.0/WPS/geo_em/geo_em.d04_333m.nc`
- 縣市界shp檔：`/var/www/html/taiwan/TWN_COUNTY.shp`(dbf, prj, shx also needed)
- 存著csv檔名之容器：`./filename.txt`
- 軌跡線csv檔(處理過程詳[daily_traj.cs](../../../TrajModels/ftuv10/daily_traj_cs.md))
  - (如)`./btrj23.74_120.4_2023032912.csv`，檔頭為`xp,yp,Hour,ymdh`、單位為公尺，TWD97系統座標值
  - 線段端點座標，前述主檔名+`_line.csv`，無檔頭，單位為度，經度及緯度。
  - 標記點座標，前述主檔名+`_mark.csv`，無檔頭，單位為度，經度及緯度。

### 結果

![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-07-21-09-25-35.png)

