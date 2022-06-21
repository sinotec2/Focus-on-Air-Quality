---
layout: default
title: 增量濃度之分析
parent: Post Processing
grand_parent: CMAQ Model System
nav_order: 5
last_modified_date: 2022-06-21 15:16:03
---

# 增量濃度之分析
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

## 前言/背景
- 計算不同排放情境模擬結果的濃度差異，是執行空品模式常見的作業。如CMAQ這樣有nc檔案輸出的模式，以[dNC][dNC]就可以簡單解決。但因為CMAQ的粒狀物定義同時有i,j,k濃度與其重量比例等2個場同時介入，因此造成非常高度之非線性結果。
  1. 在看似非關連之區域出現微幅的濃度擾動(如圖1在某一時間山區、西南海域出現增量、而在海面則出現負值之增量)。
  2. PM2.5增量高於PM10的增量(圖2)
  3. 營運前後粗細粒比例(CCTM_APMDIAG檔)具有差異性，如圖3a以營運前為1.0，營運後PM25AC月均值的增加幅度，圖3b則為PM10AC的增加幅度。

[dNC]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/dNC/> "2個nc檔案間的差值"


| ![圖1a-N3G_NO3.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_NO3.png) |![圖1b-N3G_NO3.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_NO3T.png)
|:--:|:--:|
| <b>圖1a 2019/01/01/00Z 興達新3氣機組PM<sub>2.5</sub>中NO3濃度值之增量。空白處為無法取log值之負值增量區域</b>|<b>圖1b 同左但為月平均值</b>|
| ![圖2a-N3GPMdiff.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3GPMdiff.png) |![圖2b-N3GPMdiffT.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3GPMdiffT.png) |
| <b>圖2a 同上時間PM<sub>2.5</sub>與PM<sub>10</sub>增量之差值</b>|<b>圖2b 同左但為月平均值</b>|
| ![圖3a-PM25ACdiffT.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM25ACdiffT.png) |![圖3b-PM10ACdiffT.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM10ACdiffT.png) |
| <b>圖3a 計畫營運前後Aitken mode濃度在PM<sub>2.5</sub>部分之比例(PM25AC)之月均值增加率</b>|<b>圖2b 同左但為PM<sub>10</sub>部分比例(PM10AC)</b>|
