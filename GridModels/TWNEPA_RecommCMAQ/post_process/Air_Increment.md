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
- 按照月份、污染物、平均時間、逐時/逐日檔案
- PM及SO2沒有逐時濃度分布。應為依照法規項目的作法。

```bash
kuang@centos8 /data/cmaqruns/cmaq_recommend/post_process/Performance/Perf_Tools/Air_Increment_tool/Data/Evaluate
$ tree
.
├── 2022-05-30-08-58-43 (2019-01)
│   └── plot2D
├── 2022-05-30-08-59-45 (2019-01)
│   ├── 2019-01_(各縣市最大值)PM10年平均值增量.csv
│   ├── 2019-01_(各縣市最大值)PM10日平均值增量.csv
│   ├── 2019-01_(各縣市最大值)PM25年平均值增量.csv
│   ├── 2019-01_(各縣市最大值)PM25日平均值增量.csv
│   ├── 2019-01_(所有網格點)PM10年平均值增量.csv
│   ├── 2019-01_(所有網格點)PM10日平均值增量.csv
│   ├── 2019-01_(所有網格點)PM25年平均值增量.csv
│   ├── 2019-01_(所有網格點)PM25日平均值增量.csv
│   └── plot2D
│       ├── 2019-01_PM10年平均值增量.png
│       ├── 2019-01_PM10日平均值增量.png
│       ├── 2019-01_PM25年平均值增量.png
│       └── 2019-01_PM25日平均值增量.png
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
- 2019/1月底事件的NO2及O3小時濃度變化，如[GIF](https://sinotec2.github.io/RecModResults/)所示


| ![air_plot_result.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/air_plot_result.png) |
|:--:|
| <b>環保署建議公版模式2D模擬結果([GIF](https://sinotec2.github.io/RecModResults/))</b>|

- 該個案雖為典型的東方渦旋，然而背景也有很高濃度的臭氧，約67ppb,與內陸高值 ～ 70ppb，所差無幾。
- SO2只有出日均值濃度分布，無法討論大型污染源的行為。

## [Air_plotSimObs.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/post_process/Air_plotSimObs.py)

### 結果檔案系統
- 按照月份、空品區、每個測站所有污染物
- PM及SO2沒有逐時濃度時間序列。也是依照法規項目的作法。

```bash
kuang@centos8 /data/cmaqruns/cmaq_recommend/post_process/Performance/Perf_Tools/Air_plot_tool/Output
$ tree
.
── output_scatter
│   └── 2019-01
│       └── 北部
│           ├── 001基隆201901.png
│           ├── 002汐止201901.png
│           ├── 003萬里201901.png
│           ├── 004新店201901.png
│           ├── 005土城201901.png
│           ├── 006板橋201901.png
│           ├── 007新莊201901.png
│           ├── 008菜寮201901.png
│           ├── 009林口201901.png
│           ├── 010淡水201901.png
│           ├── 011士林201901.png
│           ├── 012中山201901.png
│           ├── 013萬華201901.png
│           ├── 014古亭201901.png
│           ├── 015松山201901.png
│           └── 017桃園201901.png
└── output_timeseries
    └── 2019-01
        └── 北部
            ├── 001基隆201901.png
            ├── 002汐止201901.png
            ├── 003萬里201901.png
            ├── 004新店201901.png
            ├── 005土城201901.png
            ├── 006板橋201901.png
            ├── 007新莊201901.png
            ├── 008菜寮201901.png
            ├── 009林口201901.png
            ├── 010淡水201901.png
            ├── 011士林201901.png
            ├── 012中山201901.png
            ├── 013萬華201901.png
            ├── 014古亭201901.png
            ├── 015松山201901.png
            └── 017桃園201901.png
```



### 結果圖面
- 2019/1月北部空品區基隆站的濃度時間變化，如圖所示

| ![001基隆201901.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/001基隆201901.png) |
|:--:|
| <b>環保署建議公版模式基隆站模擬結果之時間序列</b>|

| ![001基隆201901.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/001基隆201901S.png) |
|:--:|
| <b>環保署建議公版模式基隆站模擬結果與觀測值配對散布圖</b>|