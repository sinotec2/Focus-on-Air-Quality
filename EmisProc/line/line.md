---
layout: default
title: "Mobile Sources"
parent: TEDS Python
nav_order: 4
has_children: true
permalink: /EmisProc/line/
last_modified_date:   2021-12-02 09:55:34
---

{: .fs-6 .fw-300 }

# 交通源之處理
- 環保署[TEDS]((https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx))資料庫系統中交通源排放量視道路種類、車種及排放型態、鄉鎮區編號、座標等條件(**索引維度**)而異，其時變係數車種又與主資料庫不同，也只有主要道路才有時變係數，因此在展開時需要對照表的情形，較其他類型污染源更複雜。
- 原則詳見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)。此處介紹完整的程序，分項另有詳述。

## 主要步驟程序
- 讀取TEDS之dbf檔案(環保署提供的`.dbf`檔案過於龐大，超過一般資料庫軟體可以處理，詳見[dbf2csv.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/))
- 計算直角座標值、儲存排放資料庫的**索引維度**、對應的排放量矩陣
- 劃分PM及VOCs物種、乘上日變化係數、網格整併、存入`nc`模版

## 後續處理
- CAMx面源檔案可以使用VERDI或MeteoInfo開啟、繪圖
- 經轉檔可以供CMAQ模式使用

## What's Learned
- 

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1
