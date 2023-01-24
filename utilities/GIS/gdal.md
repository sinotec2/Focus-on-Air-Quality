---
layout: default
title: GDAL
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-01-27 11:57:06
tags: GIS gdal
---

# GDAL程式集

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

- GDAL全名為*地理空間數據* **萃取** *程式庫*[^1]。中文官網：[地理空间数据抽象库][1]、wikipedia：[用於地理空間資料格式的C++轉換器庫][wiki]。為地理資訊處理常用（最重要）的程式集。
- 作業環境：Linux, window, macOS等。包裝在GIS程式如 ArcGIS, QGIS, and GRASS等系統與 Google Earth 等公開平台。
- 常見功能：檔案格式轉換、參考點或座標系統轉換、平移、切割、合併等等。

## gdal_translate

- 官網使用說明：[gdal_translate](https://gdal.org/programs/gdal_translate.html)

### 應用範例

- [AERMAP之準備與執行](../../PlumeModels/TG_pathways/gen_inp.md)

```python
gd_data=';export PATH='+pth1+':'+pth2+':$PATH;GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
gd='gdal_translate' 
cmd='cd '+dir+gd_data+gd+' -of USGSDEM -ot Float32 -projwin '+llNE+' '+TIF+' '+DEM+NUL 
os.system('echo "'+cmd+'"'+NUL) 
os.system(cmd)
```
- [集合OTM圖磚並修剪成tiff檔py程式](../Graphics/CaaS/tiles_to_tiffFit.md)

```python
gd='/opt/anaconda3/envs/env_name/bin/gdal_translate'
env='GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
llSE=' {:f} {:f} '.format(lon_max,lat_min)
llNW=' {:f} {:f} '.format(lon_min,lat_max)+llSE
ULLR=' {:f} {:f} {:f} {:f} '.format(ullon, ullat, lrlon, lrlat)
os.system(env+gd+' -of GTiff -a_ullr'+ULLR+'-a_srs EPSG:4269 merged_montage.tif merged_montageC.tif')
os.system(env+gd+' -projwin '+llNW+' -of GTiff merged_montageC.tif fitted.tif')
```


[1]: https://www.osgeo.cn/gdal/index.html "GDAL-地理空间数据抽象库"
[wiki]: https://zh.wikipedia.org/zh-tw/GDAL "GDAL是一個開源的用於柵格和向量地理空間資料格式的C++轉換器庫。"

[^1]:  GDAL: Geospatial Data Abstraction Library, Mark Altaweel, June 16, 2021, GIS Software [gislounge.com][2]，Abstraction譯為*萃取*可參考[^2]
[^2]:  由「為什麼 “abstraction”不應該譯為“抽象化”」談正名, Luis Wu(2017), [medium.com](https://medium.com/@wdyluis/由-為什麼-abstraction-不應該譯為-抽象化-談正名-a2dfb7159c47)

[2]: https://www.gislounge.com/gdal-geospatial-data-abstraction-library/ "The Geospatial Data Abstraction Library (GDAL) is a set of software tools used by GIS platforms such as ArcGIS, QGIS, and GRASS GIS."