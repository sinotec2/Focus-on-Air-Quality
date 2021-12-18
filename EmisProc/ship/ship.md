---
layout: default
title: "Marine Sources"
parent: TEDS Python
nav_order: 6
has_children: true
permalink: /EmisProc/ship/
last_modified_date:   2021-12-10 14:45:32
---

{: .fs-6 .fw-300 }

# 船舶排放之處理
- 在[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)資料庫的分類，船舶屬於面源的一個大類，其下還有各樣船隻種類的次類。
- 就港區停靠時較為集中的排放，過去分析經驗顯示，可能造成附近空氣品質的顯著影響，必須妥善處理其擴散特性，如視為網格平均(解析度為3Km)，顯然有所低估。
- 其他離岸之排放，資料庫的解析度為1Km，如果以點源處理，其個數也不少，因此還是另以面源處理為佳。

## 主要步驟程序
- 與面源一樣執行`area_YYMM`，但係針對特定NSC類別：`python area_YYMM_NSC.py YYMM 51A,51B,51C,51D`，以YYMM=1901為例，程式將產生`fortBE.413_teds11.51A_01.nc`。
- 執行`harb_ptse.py`，程式將取港區附近9格範圍之平均值，港區位置排放在該值以上者將集中為點源，當地之面源則修正為該值。
  - 點源檔名：`fortBE.413_teds11.HRBE01.nc_d04.nc`
  - 修正後面源：`fortBE.413_teds11.51Ab01.nc`

## 後續處理
- CAMx點源檔案無法使用什麼軟體開啟、繪圖，需使用[程式](https://github.com/sinotec2/TEDS_PTSE/blob/main/pt2em_d04.py)將其轉成面源形態(按網格加總)，使用[VERDI](https://github.com/CEMPD/VERDI/blob/master/doc/User_Manual/VERDI_ch01.md)來繪圖。如圖（2016 data）：
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/ships_NO.PNG)
- 經轉檔可以供CMAQ模式使用

## [github](https://github.com/sinotec2/TEDS_ship/)
## [船舶排放之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1