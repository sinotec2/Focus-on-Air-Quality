---
layout: default
title: REAS文字檔轉CMAQ高空排放
parent: REAS Python
grand_parent: CMAQ Models
nav_order: 2
date: 2022-01-10 09:04:56
last_modified_date: 2022-01-10 09:05:00
---

# REAS文字檔轉CMAQ高空排放
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
- REAS (Regional Emission inventory in ASia)資料庫中以點源形態的檔案名稱為包括**POWER_PLANTS_POINT**的電廠排放量檔案，格式與面源檔案一樣，只有在行末多了國家與省份名稱之縮寫。
  - 除XY經緯度外，並沒有煙囪其他條件。
  - 也沒有詳細逐日、逐時之排放形態之數據可供參考。


## 
## 程式下載
- [reas2cmaqD1.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD1.py)
- [reas2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD2.py)

## 結果檢視
- m3.nc檔案可以用[VERDI]()檢視，如以下：

| ![REAS_pointXY.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/REAS_pointXY.PNG) |
|:--:|
| <b>圖 REAS 2015年電廠排放點位置之分布</b>|

## Reference
