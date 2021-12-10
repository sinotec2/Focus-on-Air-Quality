---
layout: default
title: "Marine Sources"
parent: "Emission Processing"
nav_order: 6
has_children: true
permalink: /EmisProc/ship/
last_modified_date:   2021-12-10 14:45:32
---

{: .fs-6 .fw-300 }

# 船舶排放之處理
- 在[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)資料庫的分類，船舶屬於面源的一個大類，其下還有各樣船隻種類的次類。
- 就港區停靠時較為集中的排放，過去分析經驗顯示，可能造成附近空氣品質的顯著影響，必須妥善處理其擴散特性，如視為網格平均(解析度為3Km)，顯然有所低估。

## 主要步驟程序
- 

## 後續處理
- CAMx點源檔案無法使用什麼軟體開啟、繪圖，需使用[程式](https://github.com/sinotec2/TEDS_PTSE/blob/main/pt2em_d04.py)將其轉成面源形態(按網格加總)，使用[VERDI](https://github.com/CEMPD/VERDI/blob/master/doc/User_Manual/VERDI_ch01.md)來繪圖。
- 經轉檔可以供CMAQ模式使用

## [github](https://github.com/sinotec2/TEDS_PtSe/)

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1