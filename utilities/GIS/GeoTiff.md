---
layout: default
title:  GeoTiff檔之讀取
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-01-27 11:57:06
---

# python解析KML檔
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
- python 2.7 時代有libtiff可用，可參考[githup](https://github.com/pearu/pylibtiff)
- [introduction to python libraries for working with GeoTiff or satellite images](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510)


## [rasterio]()

### 檔案開啟、參數及數據之讀取

```python
import rasterio
from rasterio.plot import show
fp = r'GeoTiff_Image.tif'
img = rasterio.open(fp)
show(img)
```

```python
import rasterio
fname='giam_28_classes_global.tif'
img = rasterio.open(fname)
nx,ny,nz=img.width,img.height,img.count
data=img.read()
print(len(set(data.flatten()))) #29
```

### [tif2df](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2df)
- 此一應用的情況是因為檔案切割成約10.5公里見方的250m高解析度tiff檔，須同步進行轉換方符合效益。
- 轉成(無檔頭)csv檔之後，以cat合併成完整檔案進行解讀與轉換。

### [tif2nc]()
- 應用在全球250M解析度之tiff檔[解讀](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2nc)，採**平均**方式合併，然因記憶體需求較大，須先進行範圍切割。
- 解析度較低(1~10Km)之[應用](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Crops/#tif2nc)，採**加總**方式進行合併。

## Reference
- Mohit Kaushik, **Reading and Visualizing GeoTiff | Satellite Images with Python**, [towardsdatascience](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510),Aug 2, 2020
- Mapbox Revision, **Rasterio: access to geospatial raster data**, [readthedocs](https://rasterio.readthedocs.io/en/latest/), 2018
- Chimin, **Day26 網格資料的處理-Rasterio初探**, [ithome](https://ithelp.ithome.com.tw/articles/10209222)2018-11-10 21:56:37