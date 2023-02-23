---
layout: default
title: m3nc檔轉成GeoTiff檔
parent: GIS Relatives
grand_parent: Utilities
date: 2023-02-20
last_modified_date: 2023-02-21 03:16:28
tags: GeoTiff netCDF GIS
---

# m3nc檔轉成GeoTiff檔
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

- GIS中要能夠充分使用其自動切割圖磚、啟用WMS服務，與格柵檔案的網格座標系統有關，空氣品質模式常用的等距離直角座標系統，必須改成等經緯度系統。
- 意即經由regrid、resampling作業，將m3nc檔轉成GeoTiff檔案格式。
- 此處選擇scipy 的griddata模組進行內插，以xarrayio來進行轉檔。
- 解讀GeoTiff之程式另見[GeoTiff.md](GeoTiff.md)內之討論
- 其他nc2geotiff的討論，詳[geoserver](https://sinotec2.github.io/FAQ/2023/02/22/GeoServer.html#nc2tiff)

## 程式說明

### IO

- 引數：m3nc檔案名稱，
- 結果檔：字尾更換或新增延伸檔名`.tiff`
- `GRIDCRO2D`:mcip處理結果檔案，從中讀取網格點的經緯度座標。
- 偵錯輸出
  - 等經緯度內插結果、另存成m3nc格式
  - 等經緯度網格之數值(1d array)

### 程式設計重要細節

- 目標網格數：與輸入之m3nc檔案一致，以保持模式範圍中央部分，會有相同的解析度。
- 外插部分將會出現nan，此處將其設定為0
- 運用xarrayio進行轉檔

```python
da=xr.Dataset(data_vars=dict(pm=(["lat","lon"],var1)),coords=dict(lon=(["lon"],x1_1d),lat=(["lat"],y1_1d)))
pr=da.rio.set_spatial_dims("lon", "lat")
pr.rio.set_crs("epsg:4326")
...
pr.rio.to_raster(fname,driver="COG")
```

## 程式下載

{% include download.html content="[grb2D1m3.py](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2D1m3.py)" %}