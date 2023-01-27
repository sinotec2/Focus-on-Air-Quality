---
layout: default
title:  Applications of Earth System
parent: earth
grand_parent: Graphics
last_modified_date: 2022-08-31 10:50:26
tags: earth GFS CAMS CWBWRF graphics
---

# earth套件之建置實例
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

## [earth][ens]的發展與應用

- [ESRI][esri] 2017年也將其繼續發展成類似[油畫質感](http://esri.github.io/wind-js/)的動畫版本。
- 持續的商業版本除了[windy][windy]之外，[ventusky](https://www.ventusky.com/)也有類似的應用。
- [WebGL][webgl]控制方案與3D繪圖效果([webgl-wind](https://mapbox.github.io/webgl-wind/demo/) by [XXHolic, 2022][XXHolic])。

## 本地[earth][ens]預報系統的建置實例

範圍|解析度|公司內|公司外@iMacKuang[^2]
:-:|:-:|:-:|:-:
全球|1度|[GFS/CAMS](http://200.200.31.47:8080)|[GFS/CAMS](http://125.229.149.182:8080)
東南中國|3Km|[CWBWRF/CAMS](http://200.200.31.47:8083)|[CWBWRF/CAMS](http://125.229.149.182:8083)
東亞|45Km|[WRF/CMAQ](http://200.200.31.47:8084)|[WRF/CMAQ](http://125.229.149.182:8084)
東南中國|9Km|[WRF/CMAQ](http://200.200.31.47:8085)|[WRF/CMAQ](http://125.229.149.182:8085)
臺灣|3Km|[WRF/CMAQ](http://200.200.31.47:8086)|[WRF/CMAQ](http://125.229.149.182:8086)

- GFS
  - 全球預報系統 (GFS) 是一個全球數值天氣預報系統，包含由美國國家氣象局 (NWS) 運行的全球尺度氣象數值預報模式和變分分析。
  - [current weather map over CONUS ](http://www.wpc.ncep.noaa.gov/noaa/noaa.gif)
- [CAMS][CAMS_desc]
  - 哥白尼大氣監測服務是由2014年11月11日啟動的歐洲中程天氣預報中心提供的一項服務，提供有關大氣成分的連續數據和信息。[CAMS][CAMS_desc]是哥白尼計劃的一部分， 它描述了當前情況，對未來幾天的情況進行了預測，並持續分析了近年來的回顧性數據記錄。 维基百科
  - [Ozone Forecasts Charts](https://atmosphere.copernicus.eu/charts/cams/ozone-forecasts?facets=undefined&time=2022083000,102,2022090306&projection=classical_south_east_asia_and_indonesia&layer_name=composition_o3_surface)
- CWBWRF：中央氣象局WRF數值預報產品
- WRF：逐日氣象重置結果  
- CMAQ：空氣品質預報結果

[ens]: <https://earth.nullschool.net/> "earth, a visualization of global weather conditions, forecast by supercomputers, updated every three hours"
[tkw]: <https://air.nullschool.net/> "東京都環境局環境改善部大気保全課, 東京都風速"
[陈晖2016]: <https://m.fx361.com/news/2016/1119/9135816.html> "陈晖, 范玉鑫, 陈杨,及 吴天亭(2016), 吉林省WRF模式数值预报可视化系统设计, 现代农业科技2016年4期."
[esri]: <https://zh.m.wikipedia.org/zh-tw/美國環境系統研究所公司> "美國環境系統研究所公司Environmental Systems Research Institute, Inc"
[webgl]: <https://zh.wikipedia.org/zh-tw/WebGL> "WebGL是一種JavaScript API，用於在不使用外掛程式的情況下在任何相容的網頁瀏覽器中呈現互動式2D和3D圖形。"
[XXHolic]: <https://developpaper.com/how-i-build-a-wind-map-with-webgl/> "How I build a wind map with webgl, 2022-2-12"
[windy]: <https://www.windy.com/> "Windy是一家提供天氣預報服務的捷克公司，由伊沃·盧卡喬維奇於2014年11月創立。 Windy提供的天氣預報基於美國國家海洋和大氣管理局全球預報系統、歐洲中期天氣預報中心及瑞士NEMS模型的數據。"
[CAMS_desc]: <https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview> "CAMS每天2次進行全球大氣成分的5天預報，包括50多種氣狀物和7種顆粒物(沙漠塵埃、海鹽、有機物、黑碳、硫酸鹽、硝酸鹽和銨氣溶膠)。初始條件為衛星及地面觀測數據同化分析結果，允許在地面觀測數據覆蓋率低、或無法直接觀測到的大氣污染物進行估計，除此之外，它還使用到基於調查清單或觀測反衍的排放估計，以作為表面的邊界條件。"

[^2]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。敬請逕洽作者：sinotec2@gmail.com.
