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
- 中央氣象局(CWB)每天對外提供其WRF預報之數值產品，公開在opendata網站，項目包括垂直層定壓層的風速、溫度、geopotentail height、相對濕度，以及2維的地面風、氣溫、地表溫度、短波淨通量等共24項變數，其3公里解析度及範圍(如[下圖](https://github.com/sinotec2/jtd/raw/main/assets/images/geo_emWRF_3Km.PNG))完全涵蓋空氣污染模式模擬之D4層範圍，具有高度的參考及應用價值。
- 唯該檔案格式為WMO約定的GRIB2格式(下略grb2)，並非wrfout.nc格式(下略wrfout)，因此在應用上須另外建置應用軟體。
- 目前已經發展完成該產品應用在`CALPUFF`模式之逐日預報、地面風之軌跡線([臺灣地區高解析度軌跡產生/自動分析系統](http://114.32.164.198/traj2.html)、以及即期`AERMOD`之模式模擬作業之中。前者應用`python gribapi`直接讀取，後2者則應用`pygrib`，程式設計較為單純。
- 中央氣象局WRF預報3公里解析度之模式模擬範圍
![https://github.com/sinotec2/jtd/raw/main/assets/images/geo_emWRF_3Km.PNG]
{: .no_toc }

## What's Learned 
- 

## Reference
- [evernote](https://www.evernote.com/shard/s125/sh/b3f7003a-fd1d-4918-b617-1acb90b45219/25b5cbe6b72feca8dc5f0cec636eee78)