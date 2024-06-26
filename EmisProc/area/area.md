---
layout: default
title: "Area Sources"
parent: TEDS Python
nav_order: 2
has_children: true
permalink: /EmisProc/area/
last_modified_date:   2021-12-01 13:06:16
tags: CAMx emis TEDS uamiv
---

{: .fs-6 .fw-300 }

# 面源之處理

環保署[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)資料庫系統之面源處理，相對點源單純一些，與線源、點源處理都有些雷同，同樣是先對時間變化、及空間變化先行展開，之後再按光化模式的網格定義予以合併，詳見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/#處理程序總綱)及[面源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/)。此處介紹完整的程序，分項另有詳述。

## 主要步驟程序
- 讀取TEDS之dbf檔案(環保署提供的`.dbf`檔案過於龐大，超過一般資料庫軟體可以處理，詳見[dbf2csv.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/))
- 轉換到直角座標系統([prep_areagridLL.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/prep_areagridLL/))
- 進行**時變係數**的展開([prep_dfAdmw.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/prep_TimVar/))
- 併入NH3檔案、進行VOCs及PM的展開、整合成nc([uamiv][uamiv])檔案([area_YYMM.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/))

[uamiv]: <https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式> "CAMx所有二進制 I / O文件的格式，乃是遵循早期UAM(城市空氣流域模型EPA，1990年）建立的慣例。 該二進制文件包含4筆不隨時間改變的表頭記錄，其後則為時間序列的數據記錄。詳見CAMx(UAM)的檔案格式"

## 後續處理
- CAMx面源檔案可以使用VERDI或MeteoInfo開啟、繪圖，如[下圖](../../assets/images/teds10-11CCRS.PNG)所示。
![](../../assets/images/teds10-11CCRS.PNG)
- 經轉檔可以供CMAQ模式使用

## What's Learned
- 使用[np.tensordot](https://vimsky.com/zh-tw/examples/usage/python-numpy.tensordot.html)指令進行矩陣相乘，啟動程式的[平行化](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/#numpyscipy的平行運作)。

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1