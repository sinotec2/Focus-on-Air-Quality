---
layout: default
title: BC related problems
parent: Forecast Systems
nav_order: 4
date: 2023-03-27
last_modified_date: 2023-03-27 11:58:47
has_children: true
permalink: /ForecastSystem/BCProblem
mermaid: true
tags: forecast CMAQ GFS CAMS BCON
---

# 預報系統邊界條件相關問題
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

- 使用全球預報數據做為地區空品模式的邊界檔案，可以詳見全球空品數據應用項下-[CAMS預報數據寫成CMAQ邊界檔](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF_CAMS/3.CAMS_bc/)，[歐洲中期天氣預報中心][ecmwf]每天2次的[CAMS](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview)預報產品也是最後的選項。
- 建置過程中也嘗試使用[GFS](../../utilities/Graphics/earth/wind_ozone.md#cams與gfs數據之間需合併的項目)、[WACCM][WACCM]的預報產品，則列在此目錄下做為參考。同時也因為是過程中的努力，就沒有繼續維護下去了。
- 這裡不論5天或者10天作業化並持續維護的版本還是以[CAMS](../../AQana/GAQuality/ECMWF_CAMS/3.CAMS_bc.md#grb2bconpy)的5天預報結果為主。

{: .no_toc .text-delta }

{:toc}

---
[ecmwf]: <https://zh.wikipedia.org/zh-tw/歐洲中期天氣預報中心> "歐洲中期天氣預報中心，創立於1975年，是一個國際組織，位於英格蘭雷丁。"
[WACCM]: ../../AQana/GAQuality/3WACCM.md "大氣社區氣候模型(Whole Atmosphere Community Climate Model, WACCM)"
