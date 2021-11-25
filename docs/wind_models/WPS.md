---
layout: post
title: "WPS"
parent: "氣象模式"
nav_order: 1
date:               
last_modified_date:   2021-11-25 09:41:21
---

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

### 背景
- [WPS](https://github.com/wrf-model/WPS)顧名思義就是WRF的前處理系統(WRF Pre-processing System)，包括準備地理地形檔案的geogrid.exe、初始邊界檔案要讀取的觀測值準備ungrid.exe及網格化metgrid.exe等3支程式。
- WPS要處理的數據包括
    -地理地形等[靜態數據](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)、
    - 再分析數據(如FNL)、
    - [海溫數據](https://sinotec2.github.io/jtd/docs/wind_models/SST/)等等。
- 其結果可以成為OBSGRID、及(或)real的輸入檔案，為每一WRF作業必須的步驟。
- 詳細編譯、安裝、namelist.wps設定、VTable的設定等等，可由[官網](https://github.com/wrf-model/WPS)找到相關資源。此處著眼在批次操作、作業瓶頸、以及結果檢核等注意事項。


### Reference
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)
---
