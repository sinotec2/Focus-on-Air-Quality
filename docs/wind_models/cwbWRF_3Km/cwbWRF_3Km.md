---
layout: default
title: "cwb WRF_3Km"
parent: "wind models"
nav_order: 7
has_children: true
permalink: /docs/wind_models/cwbWRF_3Km/
last_modified_at: 2021-11-28 15:52:50
---

{: .fs-6 .fw-300 }

---

# cwb WRF_3Km
- 中央氣象局(CWB)每天對外提供其WRF預報之數值產品，公開在opendata網站，項目包括垂直層定壓層的風速、溫度、geopotentail height、相對濕度，以及2維的地面風、氣溫、地表溫度、短波淨通量等共24項變數。
  - 其3公里解析度及範圍(如[下圖](https://github.com/sinotec2/jtd/raw/main/assets/images/geo_emWRF_3Km.PNG))完全涵蓋空氣污染模式模擬之D4層範圍，具有高度的參考及應用價值。
  - 除3公里解析度外，該局亦公開其15公里解析度成果。
  - `nlay,nrow,ncol= (11, 673, 1158)|3km;  (11, 385, 661)|15Km`，皆為東西長、南北短(landscape)之地區範圍。
- CWB WRF預報的作業方式、演進與評估，可以參考其[發表](http://photino.cwb.gov.tw/conf/history/106/2017_ppt/A2/A2-26-%E4%B8%AD%E5%A4%AE%E6%B0%A3%E8%B1%A1%E5%B1%80%E5%8D%80%E5%9F%9F%E6%A8%A1%E5%BC%8F2017%E5%B9%B4%E6%9B%B4%E6%96%B0_%E9%99%B3%E4%BE%9D%E6%B6%B5.pdf)內容。
- 唯該檔案格式為WMO約定的`GRIB2`[格式](https://perillaroc.github.io/eccodes-tutorial-cn/01-introduction/)(下略`grb2`)，並非`wrfout.nc`格式(下略`wrfout`)，因此在應用上須另外建置應用軟體。
- 目前已經發展完成該產品應用在`CALPUFF`模式之逐日預報、地面風之軌跡線([臺灣地區高解析度軌跡產生/自動分析系統](http://114.32.164.198/traj2.html)、以及即期`AERMOD`之模式模擬作業之中。前者應用`python gribapi`直接讀取，後2者則應用[pygrib](https://medium.com/%E6%9F%BF%E7%94%9C%E8%8C%B6%E9%A6%99/pygrib-%E7%AC%AC%E4%B8%80%E7%AB%A0-6b47e54f9085)，程式設計較為單純。
- 中央氣象局WRF預報3公里解析度之模式模擬範圍
![](https://github.com/sinotec2/jtd/raw/main/assets/images/geo_emWRF_3Km.PNG)
{: .no_toc }

## What's Learned 
- 

## Reference
- [evernote](https://www.evernote.com/shard/s125/sh/b3f7003a-fd1d-4918-b617-1acb90b45219/25b5cbe6b72feca8dc5f0cec636eee78)
- 劉正欽, **[Pygrib]第一章**, [medium.com](https://medium.com/%E6%9F%BF%E7%94%9C%E8%8C%B6%E9%A6%99/pygrib-%E7%AC%AC%E4%B8%80%E7%AB%A0-6b47e54f9085), Sep 10, 2020