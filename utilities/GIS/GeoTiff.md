---
layout: default
title:  GeoTiff檔之讀取
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-01-27 11:57:06
---

# python解析GeoTiff檔
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
- 這篇對GeoTiff解析及應用有完整的比較說明：[introduction to python libraries for working with GeoTiff or satellite images](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510)

## [rasterio](https://rasterio.readthedocs.io/en/latest/)
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
nx,ny,nz=img.width,img.height,img.count #格數
dxm,dym=(img.bounds.right-img.bounds.left)/img.width,-(img.bounds.top-img.bounds.bottom)/img.height #間距
x0,y0=img.xy(0,0) #左上方中心點
l,b,r,t=img.bounds[:] #左、下、右、上邊界線座標
lonCent,latCent=img.lnglat() #中心點經緯度
data=img.read() #shape=(1,ny,nx)，南北方向為北向南
data=np.flip(data[0,:,:],[0]) #轉向
```

### 寫出檔案
- 寫出GeoTiff的情況不多，如提供gdal_translate進行轉檔、或在(Q)GIS內進一步檢視處理。
  - `resx,resy`：gdal_translate讀取的tiff檔是以經緯度為系統的，因此需先計算經緯度的格距。
  - `translate`：指定座標轉換的函數，因南北向是由北向南，間距為負值
  - `open`：開啟輸出檔，給定格數、層數、數據型態、座標系統及轉換函數

```python
import rasterio
from rasterio.transform import Affine

resx,resy=(np.max(lon)-np.min(lon))/(nx+2*M-1),(np.max(lat)-np.min(lat))/(ny+2*M-1)
transform = Affine.translation(np.min(lon), np.max(lat)) * Affine.scale(resx, -resy)
new_dataset = rasterio.open(TIF,'w',driver='GTiff',height=grid_z2.shape[0],width=grid_z2.shape[1],count=1,
  dtype=grid_z2.dtype,crs='+proj=latlong',transform=transform,)  
data=np.flip(grid_z2,[0]) #翻轉南北向
new_dataset.write(data, 1) #寫出數據
new_dataset.close() #關閉檔案
```

### [tif2df](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2df)
- 此一應用的情況是因為檔案切割成約10.5公里見方的250m高解析度tiff檔，須同步進行轉換方符合效益。
- 轉成(無檔頭)csv檔之後，以cat合併成完整檔案進行解讀與轉換。

### [tif2nc]()
- 應用在全球250M解析度之tiff檔[解讀](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2nc)，採**平均**方式合併，然因記憶體需求較大，須先進行範圍切割。
- 解析度較低(1~10Km)之[應用](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Crops/#tif2nc)，採**加總**方式進行合併。

## Reference
- Mohit Kaushik, **Reading and Visualizing GeoTiff \| Satellite Images with Python**, [towardsdatascience](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510),Aug 2, 2020
- Mapbox Revision, **Rasterio: access to geospatial raster data**, [readthedocs](https://rasterio.readthedocs.io/en/latest/), 2018
- Chimin, **Day26 網格資料的處理-Rasterio初探**, [ithome](https://ithelp.ithome.com.tw/articles/10209222)2018-11-10 21:56:37