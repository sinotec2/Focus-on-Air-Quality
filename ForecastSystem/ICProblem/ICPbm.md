---
layout: default
title: IC related problems
parent: Forecast Systems
nav_order: 3
date: 2023-06-12
last_modified_date: 2023-06-12 14:28:24
has_children: true
permalink: /ForecastSystem/ICProblem
mermaid: true
tags: forecast CMAQ GFS CAMS ICON
---

# 預報系統初始條件相關問題
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

- 預報系統的初始條件與傳統模式模擬的差異如下

|項目|傳統模式模擬|預報系統模擬|說明
|:-:|:-:|:-:|-
|使用全球空品模擬結果|可|可但需要全球預報模式|後者如[歐洲中期天氣預報中心][ecmwf]或美國[WACCM][WACCM]之預報結果
|再分析結果|可|無(來不及進行再分析)|預報系統無法使用現行在分析數據庫
|前批次模擬之再啟動檔案|可|可|在較小尺度範圍受區域背景影響較低者、或受局部、鄰近排放影響較嚴重者

- 基本上初始條件即為邊界條件中的第0個時間的完整濃度場。因此處理過程併同邊界條件一起處理。詳見[CAMS預報數據寫成CMAQ初始檔](../../AQana/GAQuality/ECMWF_CAMS/4.CAMS_ic.md)或[WACCM](../../AQana/GAQuality/3WACCM.md)等之說明。

{: .no_toc .text-delta }

{:toc}

---
[ecmwf]: <https://zh.wikipedia.org/zh-tw/歐洲中期天氣預報中心> "歐洲中期天氣預報中心，創立於1975年，是一個國際組織，位於英格蘭雷丁。"
[WACCM]: ../../AQana/GAQuality/3WACCM.md "大氣社區氣候模型(Whole Atmosphere Community Climate Model, WACCM)"
