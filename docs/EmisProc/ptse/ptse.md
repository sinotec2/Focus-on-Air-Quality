---
layout: default
title: "Point Sources"
parent: "Emission Processing"
nav_order: 5
has_children: true
permalink: /docs/EmisProc/ptse/
last_modified_at:   2021-12-02 09:55:34
---

{: .fs-6 .fw-300 }

# 點源之處理
- 。
- 原則詳見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)。此處介紹完整的程序，分項另有詳述。

## 主要步驟程序
- 讀取TEDS之dbf檔案(環保署提供的`.dbf`檔案過於龐大，超過一般資料庫軟體可以處理，詳見[dbf2csv.py](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/))
- 計算直角座標值、儲存排放資料庫的**索引維度**、對應的排放量矩陣
- 劃分PM及VOCs物種、乘上日變化係數、網格整併、存入`nc`模版

## 後續處理
- CAMx面源檔案可以使用VERDI或MeteoInfo開啟、繪圖
- 經轉檔可以供CMAQ模式使用

## What's Learned
- 

## Reference
純淨天空, **python numpy tensordot用法及代碼示例- 純淨天空**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.tensordot.html), 27 May 2019