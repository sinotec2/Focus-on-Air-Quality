---
layout: default
title: 農作物及土壤
parent: Geography and Land Data
grand_parent: CMAQ Models
nav_order: 2
date: 2022-01-17 09:02:06
last_modified_date: 2022-01-17 09:02:10
---

# 農作物及土嚷
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
- 農作物是CCTM雙向氨氣排放模式所需要的檔案，USEPA對美國大陸本土提供有資料庫及取用軟體，其他地區則須自行建置。
- [soilgrids](https://soilgrids.org/)是位於荷蘭世界土壤資訊機構[isric.org](https://isric.org/about/isric-org)轄下[SoilGrids]()及[WoSIS]()專案成果展示之互動地圖，該網站亦提供了[全球土壤GIS資料庫](https://isric.org/explore/soil-geographic-databases)，最高解析度達到250M，時間範圍自1997至2020。
  - 以方磚方式儲存，[如](https://files.isric.org/soilgrids/latest/data/ocd/ocd_0-5cm_mean/tileSG-017-045/tileSG-017-045_1-1.tif)
  - 項目有：bdod, cec, cfvo, clay, landmask, nitrogen, ocd, ocs, phh2o, sand, silt, soc, wrb
  - [30秒數據](https://data.isric.org/geonetwork/srv/eng/catalog.search#/metadata/dc7b283a-8f19-45e1-aaed-e9bd515119bc)

- [Our World in Data](https://ourworldindata.org/land-use)全球長期的土地使用、農業、肥料與作物土地面積等數據。解析度為國家。
- Ramankutty, N., Evan, A.T., Monfreda, C., and Foley, J.A. (2008). **Farming the planet: 1. Geographic distribution of global agricultural lands in the year 2000**. [Global Biogeochemical Cycles](https://onlinelibrary.wiley.com/doi/abs/10.1029/2007GB002952) 22 (1). doi:10.1029/2007GB002952.
  - Data distributed by the Socioeconomic Data and Applications Center, NASA ([SEDAC](https://sedac.ciesin.columbia.edu/data/set/aglands-croplands-2000/data-download))
  - 數據為2000年基準，單位為農地面積比例，解析度為5分~10Km。資料格式為geoTiff、ESRI gridfile。
  - Data presented as five-arc-minute, 4320 x 2160 cell grid, Spatial Reference: GCS_WGS_1984, Datum: D_WGS_1984, Cell size: 0.083333 degrees, Layer extent: Top : 90, Left: -180, Right: 180, Bottom: -90 [earthstat.org](http://www.earthstat.org/cropland-pasture-area-2000/)
  - Harvested Area and Yield for 175 Crops, [earthstat.org](http://www.earthstat.org/harvested-area-yield-175-crops/)

- Smith, W.K., Zhao, M., and Running, S.W. (2012). **Global Bioenergy Capacity as Constrained by Observed Biospheric Productivity Rates**. [BioScience](https://academic.oup.com/bioscience/article/62/10/911/238201) 62 (10):911–922. doi:10.1525/bio.2012.62.10.11.

## CCTM 所需土壤數據
### 控制選項
- E2C_SOIL – EPIC soil **properties**
  - Used by: CCTM – bidirectional NH3 flux version only
- E2C_CHEM – **DAILY** EPIC crop types and fertilizer application
  - Used by: CCTM – bidirectional NH3 flux version only  

### 變數名稱及內容
- 層數：L1(0 to 1 cm depth) and L2 (1 cm to 100 cm depth)
- 'SoilNum'：放在L1之下：'L1_SoilNum'
- 各層變數共6個：

|var. name|desc|unit|range|link|
|-|-|-|-|-|
|SoilNum|Soil Number|-|1\~8005||
|Bulk_D|Bulk Density|t/m**3|0.85\~1.67|[bdod](https://files.isric.org/soilgrids/latest/data/bdod/)|
|Cation|Cation Ex|cmol/kg|1.03\~48.82|[cec](https://files.isric.org/soilgrids/latest/data/cec/)|
|Field_C|Field Capacity|m/m|0.07~0.48||
|PH|potential of H ions|-|5.36\~ 7.47|[phh2o]()|
|Porosity|Porosity|%|0.2~0.55|[](https://files.isric.org/public/wise/wise_30min_v3.zip)|
|Wilt_P|Wilting Point|m/m|0.03~0.32||
