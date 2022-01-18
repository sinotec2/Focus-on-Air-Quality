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
  - 項目有：bdod, cec, cfvo, clay, landmask, nitrogen, ocd, ocs, phh2o, sand, silt, soc(Soil Organic Carbon), wrb
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

### 檔案結構
- layer有42個，為各作[物種類數](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/CWBWRF_15k/#背景)(e2c_cats)。
  - 因網格內同時有多種作物，因此土壤有種植該作物時對應之性質。
  - 會對應到土地使用檔中的穀物面積分率

```bash
$ nc=/home/cmaqruns/2018base/data/land/1804/2018_EAsia_81K_soil_bench1804.nc
$ ncdump -h $nc|H
netcdf 2018_EAsia_81K_soil_bench1804 {
dimensions:
        COL = 53 ;
        TSTEP = 1 ;
        LAY = 42 ;
        ROW = 53 ;
        VAR = 13 ;
        DATE-TIME = 2 ;
```

### 變數名稱及內容
- 層數：L1(0 to 1 cm depth) and L2 (1 cm to 100 cm depth)
- 'SoilNum'：放在L1之下：'L1_SoilNum'
- 各層變數含SoilNum共7類：

|var. name|desc|unit|range|usage|link|
|-|-|-|-|-|-|
|SoilNum|Soil Number|-|1\~8005|(not found)||
|Bulk_D|Bulk Density|t/m**3|0.85\~1.67||[bdod](https://files.isric.org/soilgrids/latest/data/bdod/)|
|Cation|Cation Ex|cmol/kg|1.03\~48.82|cec1\~2(ncols, nrows, e2c_cats) in depv_data_module|[cec](https://files.isric.org/soilgrids/latest/data/cec/)|
|Field_C|Field Capacity, [Water holding capacity](https://gmd.copernicus.org/preprints/gmd-2016-165/gmd-2016-165.pdf), water retention capacity|m/m|0.07~0.48|(not found)|LSM_MOD.F:!-- WFC is soil field capacity (Rawls et al 1982)[available water capacity (-33 to -1500 kPa)](https://data.isric.org/geonetwork/srv/eng/catalog.search#/metadata/dc7b283a-8f19-45e1-aaed-e9bd515119bc)|
|PH|potential of H ions|-|5.36\~ 7.47|pHs1\~2|[phh2o]()|
|Porosity|Porosity|%|0.2~0.55|por1,por2 in module depv_data_module|[total porosity](https://files.isric.org/public/wise/wise_30min_v3.zip)|
|Wilt_P|Wilting Point|m/m|0.03~0.32|wp1\~2|[soil water capacity (volumetric fraction) until wilting point](https://data.isric.org/geonetwork/srv/eng/catalog.search#/metadata/e33e75c0-d9ab-46b5-a915-cb344345099c)|


### number of soil type in LSM_MOD.F
```fortran
      INTEGER, PARAMETER :: N_SOIL_TYPE_WRFV4P = 16
      INTEGER, PARAMETER :: N_SOIL_TYPE_WRFV3  = 11
```
- METCRO2D_1804_run5.nc SLTYP:var_desc = "soil texture type by USDA category "

### e2c categories number in depv_data_module.F
```fortran
! depv_data_module.F:32:
            integer, parameter :: e2c_cats = 42   ! number of crop catigories
```

### lookup tab of LSM_MOD.F 
```python
C-------------------------------------------------------------------------------
C Soil Characteristics by Type for WRF4+
C
C   #  SOIL TYPE  WSAT  WFC  WWLT  BSLP  CGSAT   JP   AS   C2R  C1SAT  WRES
C   _  _________  ____  ___  ____  ____  _____   ___  ___  ___  _____  ____
C   1  SAND       .395 .135  .068  4.05  3.222    4  .387  3.9  .082   .020
C   2  LOAMY SAND .410 .150  .075  4.38  3.057    4  .404  3.7  .098   .035
C   3  SANDY LOAM .435 .195  .114  4.90  3.560    4  .219  1.8  .132   .041
C   4  SILT LOAM  .485 .255  .179  5.30  4.418    6  .105  0.8  .153   .015
C   5  SILT       .480 .260  .150  5.30  4.418    6  .105  0.8  .153   .020
C   6  LOAM       .451 .240  .155  5.39  4.111    6  .148  0.8  .191   .027
C   7  SND CLY LM .420 .255  .175  7.12  3.670    6  .135  0.8  .213   .068
C   8  SLT CLY LM .477 .322  .218  7.75  3.593    8  .127  0.4  .385   .040
C   9  CLAY LOAM  .476 .325  .250  8.52  3.995   10  .084  0.6  .227   .075
C  10  SANDY CLAY .426 .310  .219 10.40  3.058    8  .139  0.3  .421   .109
C  11  SILTY CLAY .482 .370  .283 10.40  3.729   10  .075  0.3  .375   .056
C  12  CLAY       .482 .367  .286 11.40  3.600   12  .083  0.3  .342   .090
C  13  ORGANICMAT .451 .240  .155  5.39  4.111    6  .148  0.8  .191   .027
C  14  WATER      .482 .367  .286 11.40  3.600   12  .083  0.3  .342   .090
C  15  BEDROCK    .482 .367  .286 11.40  3.600   12  .083  0.3  .342   .090
C  16  OTHER      .420 .255  .175  7.12  3.670    6  .135  0.8  .213   .068
C-------------------------------------------------------------------------------
```

## Crop names Dict
- CCTM系統中的種穀物詳[亞洲土地使用檔案>背景](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/CWBWRF_15k/#背景)
- 175種穀物為解開[earthstat>壓縮檔](http://www.earthstat.org/harvested-area-yield-175-crops/)之結果
- 可食豆：包括175種穀物中所有含有bean之種類
- earthstat沒有乾草(straw)或其他畜牧用草等名稱，只有mixedgrass比較接近。
- grain/silage之分，前者為穀粒、人類食物或種子，後者為畜用。
- other_crop，經查wiki，21種穀物中漏了雜穀，將其列為other_crop
- 春麥/冬麥在earthstat無法區分，只能依照長城所在緯度(略以40度)為界區別之。

|spec in CCTM sys 21 kinds|spec in earthstat database|中文名稱|
|-|-|-|
|beans|bean|豆|
|beansedible|broadbean,greenbean,greenbroadbean,stringbean]|可食豆|
|canola|rapeseed|油菜|
|corngrain|popcorn|玉米粒|
|cornsilage|greencorn|玉米青貯飼料|
|hay|mixedgrass|乾草|
|other_crop|millet|[雜穀](https://zh.wikipedia.org/wiki/谷物)|
|other_grass|grassnes|未標示草|
|peanuts|groundnut|落花生|
|potatoes|potato|馬鈴薯|
|sorghumgrain|sorghum|高粱粒|
|sorghumsilage|sorghumfor|高粱粒粉貯飼料|
|soybeans|soybean|大豆|
|wheat_spring|wheat(lat>40)|春麥|
|wheat_winter|wheat(lat<=40)|冬麥|




## Reference
- W. J. Rawls, D. L. Brakensiek, K. E. Saxtonn (1982). **Estimation of Soil Water Properties**. Transactions of the ASAE. 25, 1316–1320. https://doi.org/10.13031/2013.33720
  - [lookup table](https://www.researchgate.net/figure/The-RA-soil-hydraulic-property-look-up-table-Rawls-et-al-1982_tbl3_254240905)
- Aliku, O., Oshunsanya, S.O. (2016). **Establishing relationship between measured and predicted soil water characteristics using SOILWAT model in three agro-ecological zones of Nigeria**. Geosci. Model Dev. Discuss. https://doi.org/10.5194/gmd-2016-165
  - Field Capacity moisture (33 kPa), %v

