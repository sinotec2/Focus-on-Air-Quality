---
layout: default
title: 空品增量模擬工具
parent: 後製工具
grand_parent: Recommend System
nav_order: 3
date: 2022-04-22 10:28:51
last_modified_date: 2022-05-29 22:30:50
---

# 空品增量模擬工具(Air_Increment_tool)
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

## 背景

| ![air_Inc.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/inc_plot.png) |
|:--:|
| <b>圖1公版模式增量分析模擬工具程式庫、數據檔案目錄架構</b>|

- 執行：
  - 這2支程式的引數都是年-月，必須以標準輸入的方式鍵入
  - 必須在特定目錄提供檔案(或連結)，如上圖所示。
  - cctm檔名必須是**v1.** *YYYY* **-** *MM* **.conc.nc**
  - 檔案必須含有wspd10項目
  - 第一次執行會連結到NatureEarth網站，因此必須保持網路對外暢通。

## [Air_plot2D.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/post_process/Air_plot2D.py)
### 結果檔案系統
- 按照執行批次存放
  - 各縣市最大值分析結果
  - 所有網格點之最大時間結果
  - plot2D目錄下有各增量濃度分布圖

```bash
kuang@centos8 /data/cmaqruns/cmaq_recommend/post_process/Performance/Perf_Tools/Air_Increment_tool/Data/Evaluate
$ tree
.
└── 2022-05-30-09-11-14 (2019-01)
    ├── 2019-01_(各縣市最大值)NO2年平均值增量.csv
    ├── 2019-01_(各縣市最大值)NO2最大小時平均值增量.csv
    ├── 2019-01_(各縣市最大值)O3八小時平均值增量.csv
    ├── 2019-01_(各縣市最大值)O3最大小時平均值增量.csv
    ├── 2019-01_(各縣市最大值)PM10年平均值增量.csv
    ├── 2019-01_(各縣市最大值)PM10日平均值增量.csv
    ├── 2019-01_(各縣市最大值)PM25年平均值增量.csv
    ├── 2019-01_(各縣市最大值)PM25日平均值增量.csv
    ├── 2019-01_(各縣市最大值)SO2年平均值增量.csv
    ├── 2019-01_(各縣市最大值)SO2最大小時平均值增量.csv
    ├── 2019-01_(所有網格點)NO2年平均值增量.csv
    ├── 2019-01_(所有網格點)NO2最大小時平均值增量.csv
    ├── 2019-01_(所有網格點)O3八小時平均值增量.csv
    ├── 2019-01_(所有網格點)O3最大小時平均值增量.csv
    ├── 2019-01_(所有網格點)PM10年平均值增量.csv
    ├── 2019-01_(所有網格點)PM10日平均值增量.csv
    ├── 2019-01_(所有網格點)PM25年平均值增量.csv
    ├── 2019-01_(所有網格點)PM25日平均值增量.csv
    ├── 2019-01_(所有網格點)SO2年平均值增量.csv
    ├── 2019-01_(所有網格點)SO2最大小時平均值增量.csv
    └── plot2D
        ├── 2019-01_NO2年平均值增量.png
        ├── 2019-01_NO2最大小時平均值增量.png
        ├── 2019-01_O3八小時平均值增量.png
        ├── 2019-01_O3最大小時平均值增量.png
        ├── 2019-01_PM10年平均值增量.png
        ├── 2019-01_PM10日平均值增量.png
        ├── 2019-01_PM25年平均值增量.png
        ├── 2019-01_PM25日平均值增量.png
        ├── 2019-01_SO2年平均值增量.png
        └── 2019-01_SO2最大小時平均值增量.png
```

### 結果圖面
- matplotlib等值圖檔的容量並不小，一個檔案約140KB
- 2019/1月船舶排放之增量如圖所示

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/2019-01_NO2最大小時平均值增量.png) |![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/2019-01_SO2最大小時平均值增量.png) |
|:--:|:--:|
|<b>NO<sub>2</sub>月最大小時值增量濃度分布</b>|<b>SO<sub>2</sub>月最大小時值增量濃度分布</b>|

- 比較VERDI繪製2019年1月份月均值模擬結果如圖所示。

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SO2SHIP_JanT.PNG)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SO2_JanT.PNG)|
|:-:|:--:|
| <b>船舶排放所造成的濃度差異(增量)</b>| <b>一月份SO2月平均濃度</b>|

- 繪圖程式的上下界是固定的，無法畫出負值。圖中系將Base與Case濃度檔互換的結果
- 因最大值超過色標，雖在Footer位置標示有最大濃度的數值，但位置卻無法確認。
