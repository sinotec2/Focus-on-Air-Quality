---
layout: default
title: "GFS"
parent: "wind models"
nav_order: 99
has_children: true
permalink: /wind_models/GFS/
last_modified_date: 2022-08-05 13:37:05
---

{: .fs-6 .fw-300 }

---

# GFS (Global Forecast System)
- 全球預報系統 ([GFS](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast)) 是一個全球數值天氣預報系統，包含由美國國家氣象局 (National Weather Service, [NWS](https://www.weather.gov/)) 運行的全球尺度氣象數值預報模式和變分分析([wiki](https://en.wikipedia.org/wiki/Global_Forecast_System))。
- 模式輸出之變數名稱、意義及單位詳見官網之[GFS PARAMETERS & UNITS](https://www.nco.ncep.noaa.gov/pmb/docs/on388/table2.html)。
- 下載點、層數、變數與範圍等perl程式控制方式及範例，可以詳見[GRIB Filters and View the URL](https://nomads.ncep.noaa.gov/txt_descriptions/grib_filter_doc.shtml)#Scripting file retrievals 。

## What's Learned 
- wget與cgi-bin(perl)的交互作用
- GFS grib2 -> [json](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/earth/wind_ozone/) -> [earth展示系統][earth]
- GFS grib2 -> ungrib([WPS](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WPS/)) -> [WRF](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/GFS/2.GFS2WRF/) -> [CMAQ](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ForecastSystem/1.CMAQ_fcst/) -> [earth展示系統][earth]

## Reference

[earth]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/earth> "earth套件之應用"
