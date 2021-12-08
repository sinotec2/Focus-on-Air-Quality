---
layout: default
title: "Point Sources"
parent: "Emission Processing"
nav_order: 5
has_children: true
permalink: /EmisProc/ptse/
last_modified_at:   2021-12-02 09:55:34
---

{: .fs-6 .fw-300 }

# 點源之處理
- 點源的**時變係數**有2處來源，一者設有自動連續監設施(CEMS)者，再者環保署資料庫中亦有每筆數據的工作時間(weeks of year, days of week, hours of day)。
- 此外，光化模式因設有垂直網格，對於較小的點源、工廠的逸散性排放，煙流無法超越第1層範圍者，不必以點源處理，可以納入地面排放。
- 其他原則詳見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)。此處介紹完整的程序，分項另有詳述。

## 主要步驟程序
- 讀取TEDS之dbf檔案(環保署提供的`.dbf`檔案過於龐大，超過一般資料庫軟體可以處理，詳見[dbf2csv.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/))
- 按污染項目、排放高度特性計算污染源的**時變係數**
- 地面污染量乘上**時變係數**、進行PM及VOCs物種、網格整併、存入`nc`模版
- 高空污染源進行同樣之程序，但需記載排放口之物理條件

## 後續處理
- CAMx點源檔案無法使用什麼軟體開啟、繪圖，需使用[程式](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/pt2em_d04.py)將其轉成面源形態(按網格加總)
- 經轉檔可以供CMAQ模式使用

## What's Learned
- 

## Reference
純淨天空, **python numpy tensordot用法及代碼示例- 純淨天空**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.tensordot.html), 27 May 2019