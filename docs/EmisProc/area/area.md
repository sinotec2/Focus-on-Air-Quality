---
layout: default
title: "area"
parent: "Emission Processing"
nav_order: 2
has_children: true
permalink: /docs/EmisProc/area/
last_modified_at:   2021-12-01 13:06:16
---

{: .fs-6 .fw-300 }

# 面源之處理

面源處理相對其他點源單純一些，與線源、點源處理都有些雷同，同樣是先對時間變化、及空間變化先行展開，之後再按光化模式的網格定義予以合併，詳見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)及[面源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/area/)。此處介紹完整的程序，分項另有詳述。

## 主要步驟程序
- 讀取TEDS之dbf檔案(環保署提供的`.dbf`檔案過於龐大，超過一般資料庫軟體可以處理，詳見[dbf2csv.py](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/))
- 轉換到直角座標系統([prep_areagridLL.py](https://sinotec2.github.io/jtd/docs/EmisProc/area/prep_areagridLL/))
- 進行**時變係數**的展開([prep_dfAdmw.py](https://sinotec2.github.io/jtd/docs/EmisProc/area/prep_TimVar/))
- 併入NH3檔案、進行VOCs及PM的展開、整合成nc(uamiv)檔案([area_YYMM.py](https://sinotec2.github.io/jtd/docs/EmisProc/area/area_YYMMinc/))

## 後續處理
- CAMx面源檔案可以使用VERDI或MeteoInfo開啟、繪圖，如[下圖](https://github.com/sinotec2/jtd/raw/main/assets/images/teds10-11CCRS.PNG)所示。
![](https://github.com/sinotec2/jtd/raw/main/assets/images/teds10-11CCRS.PNG)
- 經轉檔可以供CMAQ模式使用

## What's Learned
- 使用[np.tensordot](https://vimsky.com/zh-tw/examples/usage/python-numpy.tensordot.html)指令進行矩陣相乘，啟動程式的[平行化](https://sinotec2.github.io/jtd/docs/EmsProc/#numpyscipy的平行運作)。

## Reference
純淨天空, **python numpy tensordot用法及代碼示例- 純淨天空**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.tensordot.html), 27 May 2019