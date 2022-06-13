---
layout: default
title: 空品繪圖工具
parent: 後製工具
grand_parent: Recommend System
nav_order: 2
date: 2022-04-22 10:28:51
last_modified_date: 2022-05-29 22:30:57
---

# 空品繪圖工具(Air_plot_tool)
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
- 此部分繪製
  1. 各平均時間空氣品質地面2維濃度分布，範圍為所有grid03模擬範圍。([Air_plot2D.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/post_process/Air_plot2D.py))
  2. 各測站模擬與實測值的時間序列圖([Air_plotSimObs.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/post_process/Air_plotSimObs.py))
- 由於地面濃度分布圖是掌握模擬事件時間空間變化最重要的系列圖，對事件的說明最為重要。
- 測站時間序列可以看出模擬是否有整體高、低估的傾向，是否正確抓住事件的高值。

| ![air_plot.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/air_plot.png) |
|:--:|
| <b>圖1公版模式後製工具程式庫、數據檔案目錄架構</b>|

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
kuang@centos8 /data/cmaqruns/cmaq_recommend/post_process/Performance/Perf_Tools/Air_plot_tool/Output
$ tree
.
├── output_2D
│   └── 2019-01
│       ├── NMHC
│       │   └── hour
│       │       ├── 2019010100_NMHC.png
│       │       ├── 2019010101_NMHC.png
│       │       ├── 2019010102_NMHC.png
...
│       │       └── 2019013123_NMHC.png
│       ├── NO2
│       │   ├── day
│       │   │   ├── 20190101_NO2.png
│       │   │   ├── 20190102_NO2.png
...
│       │   │   └── 20190131_NO2.png
│       │   └── hour
│       │       ├── 2019010100_NO2.png
│       │       ├── 2019010101_NO2.png
│       │       ├── 2019010102_NO2.png
...
│       │       └── 2019013123_NO2.png
│       ├── O3
│       │   └── hour
│       │       ├── 2019010100_O3.png
│       │       ├── 2019010101_O3.png
...
│       │       └── 22019013123_O3.png
│       ├── PM10
│       │   └── day
│       │       ├── 20190101_PM10.png
│       │       ├── 20190102_PM10.png
...
│       │       └── 20190131_PM10.png
│       ├── PM25
│       │   └── day
│       │       ├── 20190101_PM25.png
│       │       ├── 20190102_PM25.png
...
│       │       └── 20190131_PM25.png
│       └── SO2
│           └── day
│               ├── 20190101_SO2.png
│               ├── 20190102_SO2.png
...
│               └── 20190131_SO2.png
├── output_scatter
└── output_timeseries
```

### 結果圖面
- matplotlib等值圖檔的容量並不小，一個檔案約140KB
- 2019/1月底事件的NO2及O<sub>3</sub>小時濃度變化，如[GIF](https://sinotec2.github.io/RecModResults/)所示


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