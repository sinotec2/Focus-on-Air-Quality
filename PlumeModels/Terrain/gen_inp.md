---
layout: default
title: Generation AERMAP.inp
parent: Terrain Processing
nav_order: 1
last_modified_date: 2022-02-10 10:18:31
---
# AERMAP之準備與執行
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
- AERMAP是AERMOD地形檔案的前處理程式，執行複雜地形中的煙流模擬必經的程序。最大的障礙在於必須要以美國地理調查局的[DEM格式](https://gdal.org/drivers/raster/usgsdem.html?highlight=dem)讀取數值地形資料，過去的作法包括：
  - 直接按照AERMAP結果格式將地形高程與山丘高度(特徵高)，寫出檔案，完全取代AERMAP。
  - 事先處理台灣地區20M的數值地形成為DEM格式，為[鳥哥](https://linux.vbird.org/enve/aermap-op.php)的作法，好處是一般使用者不需自行轉檔，較為單純。且為內政部最新調查成果較符合實況。壞處是DEM檔會非常大，且增加AERMAP篩選的時間。
  - 使用者自行轉檔方案(此筆記)：將`gdal_translate`指令包裹在python程式中，只需轉換所需的範圍，較為經濟有效。缺點是使用者還是必須下載[正確版本](https://www.gisinternals.com/release.php)的`gdal_translate`程式，並且更改其執行路徑。
- 執行步驟
  1. 由GeoTiff檔案中切割指定範圍之地形數據，再以GeoTiff格式寫出數據。
  1. 呼叫`gdal_translate`程式進行轉檔
  1. 準備其他aermap.inp所需參數
  1. 呼叫AERMAP程式完成作業
  1. 將數據寫成isc格式之地形檔案備用
  1. 將數據寫成kml格式以備檢查
- 有關GeoTiff格式的讀取、寫出等等，可以參考[筆記](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)及[df範例](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2df)、[nc範例](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2nc)

## 數值地形資料下載
### 內政部
- 
### EIO
- 
```python

```