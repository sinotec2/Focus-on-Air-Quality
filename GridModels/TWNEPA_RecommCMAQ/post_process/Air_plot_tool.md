---
layout: default
title: Air_plot_tool
parent: 後製工具
grand_parent: Recommend System
nav_order: 2
date: 2022-04-22 10:28:51
last_modified_date: 2022-04-22 10:28:56
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
### Results
- matplotlib等值圖檔的容量並不小，一個檔案約140KB
- 2019/1月底事件的NO2及O3小時濃度變化，如[GIF]()所示

## [Air_plotSimObs.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/post_process/Air_plotSimObs.py)


