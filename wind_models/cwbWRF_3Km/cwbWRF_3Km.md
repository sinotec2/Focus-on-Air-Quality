---
layout: default
title: "cwb WRF_3Km"
parent: "wind models"
nav_order: 2
has_children: true
permalink: /wind_models/cwbWRF_3Km/
last_modified_date: 2021-11-28 15:52:50
---

{: .fs-6 .fw-300 }

---

# cwb WRF_3Km
- 中央氣象局(CWB)每天對外提供其WRF預報之數值產品，公開在opendata網站，項目包括垂直層定壓層的風速、溫度、geopotentail height、相對濕度，以及2維的地面風、氣溫、地表溫度、短波淨通量等共24項變數。
  - 其3公里解析度及範圍(如[下圖](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_3Km.PNG))完全涵蓋空氣污染模式模擬之D4層範圍，具有高度的參考及應用價值。
  - 除3公里解析度外，該局亦公開其15公里解析度成果。
  - `nlay,nrow,ncol= (11, 673, 1158)|3km;  (11, 385, 661)|15Km`，皆為東西長、南北短(landscape)之地區範圍。
- CWB WRF預報的作業方式、演進與評估，可以參考其[發表](https://conf.cwb.gov.tw/media/cwb_past_conferences/106/2017_ppt/A2/A2-26-中央氣象局區域模式2017年更新_陳依涵.pdf)內容。
- 唯該檔案格式為WMO約定的`GRIB2`[格式](https://perillaroc.github.io/eccodes-tutorial-cn/01-introduction/)(下略`grb2`)，並非`wrfout.nc`格式(下略`wrfout`)，因此在應用上須另外建置應用軟體。
- 目前已經發展完成該產品應用在`CALPUFF`模式之逐日預報、地面風之軌跡線([臺灣地區高解析度軌跡產生/自動分析系統](http://125.229.149.182/traj2.html)、以及即期`AERMOD`之模式模擬作業之中。前者應用`python gribapi`直接讀取，後2者則應用[pygrib](https://medium.com/%E6%9F%BF%E7%94%9C%E8%8C%B6%E9%A6%99/pygrib-%E7%AC%AC%E4%B8%80%E7%AB%A0-6b47e54f9085)，程式設計較為單純。
- 中央氣象局WRF預報3公里解析度之模式模擬範圍
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_3Km.PNG)
{: .no_toc }

## What's Learned 
- 

## Reference
- [evernote](https://www.evernote.com/shard/s125/sh/b3f7003a-fd1d-4918-b617-1acb90b45219/25b5cbe6b72feca8dc5f0cec636eee78)
- 劉正欽, **[Pygrib]第一章**, [medium.com](https://medium.com/%E6%9F%BF%E7%94%9C%E8%8C%B6%E9%A6%99/pygrib-%E7%AC%AC%E4%B8%80%E7%AB%A0-6b47e54f9085), Sep 10, 2020
- 陳依涵、戴俐卉、賴曉薇、陳怡儒、林伯勳、黃小玲、江琇瑛、江晉孝、陳白榆、洪景山、馮欽賜（2017）[中央氣象局區域模式2017 年更新 (OP41)](https://conf.cwb.gov.tw/media/cwb_past_conferences/106/2017_ppt/A2/A2-26-中央氣象局區域模式2017年更新_陳依涵.pdf)，中央氣象局氣象資訊中心
- CWB, [CWB WRF模式](https://opendata.cwb.gov.tw/opendatadoc/MIC/A0061.pdf) @opendata.cwb.gov.tw