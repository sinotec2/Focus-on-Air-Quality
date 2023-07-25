---
layout: default
title: Forecast Systems
nav_order: 11
has_children: true
permalink: /ForecastSystem/
last_modified_date:  2023-03-24 08:55:48
tags: forecast
---

# 逐日WRF與CMAQ預報系統之建置
{: .no_toc }

- 全球空品預報
  - [CAMS網站][1]有每12小時進行未來5天全項目、逐3小時之空氣品質預報，數值產品包括全球與個別分區時序圖檔、以及數據檔案。
  - NCAR [CAM-chem][CAM-chem]及[WACCM ][WACCM]模式
  - 空品預報的準確度除了排放量之外，最主要的影響因素來自氣象的預報，而其不準度會隨著時間增加，WMO現正積極努力投入在天氣預報這一領域，以支援空品預報品質的提升。[^1]。
- 區域性
  - 美國領土：NASA [GMO][2]
  - [日本大氣污染情報網站](https://pm25.jp/)
- 本地預報系統的建置實例
  - 環保署空氣品質監測網[全國各空品區空氣品質指標(AQI)預報][3]
  - 行政法人國家災害防救科技中心天氣與監測氣候網災害模式 ► [懸浮微粒模式][4]
  - 中研院環境變遷研究中心[高解析度空氣品質診斷與預報模式發展計畫模擬預報資料][5]
  - 東亞~台灣未來10天逐時預報[(time-bar版本)][6]

範圍|動畫|解析度|公司內|公司外
:-:|:-:|:-:|:-:|:-:
全球|earth|1度|[GFS/CAMS](http://200.200.31.47:8080)|[GFS/CAMS](http://125.229.149.182:8080)
東南中國|earth|3Km|[CWBWRF/CAMS](http://200.200.31.47:8083)|[CWBWRF/CAMS](http://125.229.149.182:8083)
東亞|earth|45Km|[WRF/CMAQ](http://200.200.31.47:8084)|[WRF/CMAQ](http://125.229.149.182:8084)
東南中國|earth|9Km|[WRF/CMAQ](http://200.200.31.47:8085)|[WRF/CMAQ](http://125.229.149.182:8085)
臺灣|earth|3Km|[WRF/CMAQ](http://200.200.31.47:8086)|[WRF/CMAQ](http://125.229.149.182:8086)
東亞～臺灣|GIF|3~45Km|-|[GithubPageSite](https://sinotec2.github.io/cmaq_forecast/)

{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


[^1]: Nicolas Huneeus, Johannes Flemming, Jessica Seddon (2022). Global Air Quality Forecasting and Information System (GAFIS) Implementation Plan: 2022–2026. World Meteorological Organization (WMO), Geneva, Switzerland.[(pdf)](https://library.wmo.int/doc_num.php?explnum_id=11358)


[1]: https://atmosphere.copernicus.eu/charts/packages/cams/?facets=%7B%22Family%22%3A%5B%22Reactive%20gases%22%5D%7D "Global forecast plots"
[2]: https://gmao.gsfc.nasa.gov/ "The Global Modeling and Assimilation Office, Goddard Space Flight Center, NASA"
[3]: https://airtw.epa.gov.tw/CHT/Forecast/Forecast_3days.aspx "全國各空品區空氣品質指標(AQI)預報"
[4]: https://watch.ncdr.nat.gov.tw/watch_cmaq "「CMAQ空污模式」及「排放源」是與 國立中央大學 大氣科學系 多維空氣品質模擬實驗室鄭芳怡教授合作落實"
[5]: https://ci.taiwan.gov.tw/dsp/Views/dataset/forecast_air.aspx "中研院環境變遷研究中心高解析度空氣品質診斷與預報模式發展計畫模擬預報資料"
[6]: http://125.229.149.182/time-bar "中國東南沿海地區未來10天CMAQ空品預報"
[CAM-chem]: <https://wiki.ucar.edu/display/camchem/Home> "The Community Atmosphere Model with Chemistry (CAM-chem) is a component of the NCAR Community Earth System Model (CESM) and is used for simulations of global tropospheric and stratospheric atmospheric composition."
[WACCM]: <https://www2.acom.ucar.edu/gcm/waccm> "The Whole Atmosphere Community Climate Model (WACCM) is a comprehensive numerical model, spanning the range of altitude from the Earth's surface to the thermosphere"
