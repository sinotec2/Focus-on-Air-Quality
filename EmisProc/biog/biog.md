---
layout: default
title: "Biogenic Sources"
parent: "Emission Processing"
nav_order: 3
has_children: true
permalink: /EmisProc/biog/
last_modified_date:   2021-12-02 09:55:34
---

{: .fs-6 .fw-300 }

# 植物源之處理

由於環保署提供的生物源(植物)排放檔案是已經處理過的全年排放量網格分布，而沒有**時變係數**，僅有手冊中的月變化係數，以及文獻中找到的日變化係數，沒有類別與空間的相依性，較為單純。處理程式部分仍為舊版`fortran`並未更新。

## 主要步驟程序
- 讀取TEDS之dbf檔案(環保署提供的`.dbf`檔案過於龐大，超過一般資料庫軟體可以處理，詳見[dbf2csv.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/))
- 乘上月變化係數成為逐月排放量([fortran]())，整合成一個大的`DataFrame`
- 網格化、劃分VOCs物種、乘上日變化係數、存入`nc`模版

## 後續處理
- CAMx面源檔案可以使用VERDI或MeteoInfo開啟、繪圖
- 經轉檔可以供CMAQ模式使用

## What's Learned
- 線性序列填入矩陣的[作法](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/biog/bioginc/#線性之DataFrame填入3維矩陣)

## Reference
純淨天空, **python numpy tensordot用法及代碼示例- 純淨天空**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.tensordot.html), 27 May 2019