---
layout: default
title: Redistribution of Ship Emissions
parent: EDGAR Emission Processing
grand_parent: Global/Regional Emission
nav_order: 2
date: 2022-03-17 18:42:30
last_modified_date: 2022-03-17 18:42:34
---

# EDGARv5船隻排放空間分布之重分配
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
- 雖然EDGAR解析度0.1度與HUADON_3k的解析度已經相差無幾，然而模擬結果仍然顯示出濃度分布的奇異點，當風向與船隻路線有顯著交角是，突高的面源產生類似點源的效應，圖面上呈現出平行的煙流，而不是均勻的片狀線源貢獻之濃度分布。
- 造成此一結果的主要原因是EDGAR在同一路線上的排放量本身就具有很大的差異性，當程式進行內插時就很難避免加深此一差異而造成路線上的不連續結果。
- 解決方式
  - 以照片處理技巧拉大路線及非路線排放量的差距([Noise Removal of a Raster Data](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/noise_removal/))。可以消除公海部分的零星排放量，但不能增加路線上的排放量。
  - [Extracting Road Vector Data from Raster Maps](https://www.researchgate.net/publication/227067853_Extracting_Road_Vector_Data_from_Raster_Maps)。全球港埠設施逾萬處，燈塔更不計其數、還有內陸河流湖泊之水路，此舉無法達成。
  - 重新以高解析度數據進行排放量的空間分配，例如歐洲水路的[交通密度圖](https://emodnet.ec.europa.eu/en/traffic-density-maps-better-understanding-maritime-traffic-0)。
    - 以一定範圍內的排放總量除以該範圍交通量總數得到比例，將排放量正比分配到高解析度網格、再合併到3公里網格。
    - 經嘗試錯誤，範圍太小(如EDGAR之0.1度網格)，還是無法解決不連續的情況，EDGAR排放量差異比交通密度差異更大。必須以整個HUADON_3k範圍總量方具有最佳效果。
    - 以歐洲範圍數據為1公里解析度、時間範圍則為逐月，似乎可行。

## 全球水路交通密度數據
- 經查世界銀行在其網站公開IMF分析歷年0.005度解析度（赤道處約為500m）之[船隻總密度數據](https://datacatalog.worldbank.org/search/dataset/0037580)，具有足夠的範圍與解析度
  - 船隻種類：共有商業、油氣、娛樂、漁船、客輪、以及總和等6個檔案。其中以商業佔絕大多數。
  - 數據時間自2015/1\～2021/2。時間變化上較為不足。
  - 單位為AIS顯示在網格內出現的總次數，包括移動中與固定。
- 下載方式：該網站以java程式提供使用者點選，透過瀏覽器自動將zip檔案複製到使用者的Downloads目錄。再行解壓縮。
- 檔案格式：[GeoTiff](/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)

### 程式下載
- [EDGAR2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR2cmaqD2.py)

## Results

| ![NOx_EastAsia.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NOx_EastAsia.PNG) |![NO2_D6.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NO2_D6.PNG) |
|:--:|:--:|
| <b></b>|  

## Reference
- Diego A. Cerdeiro, Andras Komaromi, Yang Liu, and Mamoon Saeed, **World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based Nowcasts from Scratch**, [IMF paper](https://www.imf.org/en/Publications/WP/Issues/2020/05/14/World-Seaborne-Trade-in-Real-Time-A-Proof-of-Concept-for-Building-AIS-based-Nowcasts-from-49393), May 14, 2020 

