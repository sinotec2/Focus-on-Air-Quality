---
layout: default
title: "WPS"
parent: "wind models"
has_children: true
nav_order: 4
date:               
last_modified_date:   2021-11-25 16:21:24
permalink: /docs/wind_models/WPS/
---
# WPS
WRF的前處理系統
[WPS](https://github.com/wrf-model/WPS)顧名思義就是WRF的前處理系統(WRF Pre-processing System)，包括準備地理地形檔案的`geogrid.exe`、初始邊界檔案要讀取的觀測值準備`ungrid.exe`及網格化`metgrid.exe`等3支程式，而這三支程式共用同一個**名單**([namelist.wps demo](http://homepages.see.leeds.ac.uk/~lecag/wiser/namelist.wps.pdf))。
- WPS要處理的數據包括
  - 地理地形等[靜態數據](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)、
  - 再分析數據(如FNL)、
  - [海溫數據](https://sinotec2.github.io/jtd/docs/wind_models/SST/)等等。
  - 其結果可以成為OBSGRID、及(或)real的輸入檔案，為每一WRF作業必須的步驟。
  - 詳細編譯、安裝、namelist.wps設定、VTable的設定等等，可由[官網](https://github.com/wrf-model/WPS)找到相關資源。此處著眼在批次操作、作業瓶頸、以及結果檢核等注意事項。

{: .fs-6 .fw-300 }
