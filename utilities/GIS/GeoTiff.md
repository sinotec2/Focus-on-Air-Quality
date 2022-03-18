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

### [tif2nc](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Crops/#tif2nc)
- 應用在全球250M解析度之土壤參數tiff檔[解讀](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2nc)，採**平均**方式合併，然因記憶體需求較大，須先進行範圍切割。
- 高解析度作物檔案轉到解析度較低(1~10Km)之[應用](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Crops/#tif2nc)，採**加總**方式進行合併。
- 高解析度(500m)船隻密度tiff檔案為基底，作為[重新分配排放量](https://github.com/sinotec2/Focus-on-Air-Quality/Global_Regional_Emission/EDGARv5/ShipDensity/)的依據。

### [tif2kml.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/tif2kml.py)
- 顧名思義，此程式將tiff檔轉成kml檔案，便於檢視等值圖。
- 呼叫[cntr_kml.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/cntr_kml.py)，詳見[等值線之KML檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)
- 引數：tiff檔的名稱(TIF)
- 結果：TIF.kml
- 如果邊界的平均值正好是中心點的經緯度，判定座標系統是經緯度系統，否則設定是twd系統

```python
img = rasterio.open(fname)
l,b,r,t=img.bounds[:]
LL=False
if (l+r)/2==img.lnglat()[0]:LL=True
...
if LL:
  lon, lat = np.meshgrid(x, y)
else:
  x_g, y_g = np.meshgrid(x, y)
  Xcent=(x[0]+x[-1])/2
  Ycent=(y[0]+y[-1])/2
  Latitude_Pole, Longitude_Pole=twd97.towgs84(Xcent, Ycent)
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
  xgl,ygl=x_g-Xcent,  y_g-Ycent
  lon,lat=pnyc(xgl, ygl, inverse=True)
result=cntr_kml(data, lon, lat, fname)
```

## Reference
- Mohit Kaushik, **Reading and Visualizing GeoTiff \| Satellite Images with Python**, [towardsdatascience](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510),Aug 2, 2020
- Mapbox Revision, **Rasterio: access to geospatial raster data**, [readthedocs](https://rasterio.readthedocs.io/en/latest/), 2018
- Chimin, **Day26 網格資料的處理-Rasterio初探**, [ithome](https://ithelp.ithome.com.tw/articles/10209222)2018-11-10 21:56:37