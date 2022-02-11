---
layout: default
title: Prepare and Exec. of AERMAP
parent: Terrain Processing
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-02-11 10:57:05
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
  - 事先將台灣地區數值地形切割並處理成較小範圍的DEM檔案，因為AERMAP可以同時讀取數個DEM檔案。從其中整併出所需要的範圍進行內插。(not tried)
  - 使用者自行轉檔方案(this note)：將`gdal_translate`指令包裹在python程式中，只需轉換所需的範圍，較為經濟有效。缺點是使用者還是必須下載[正確版本](https://www.gisinternals.com/release.php)的`gdal_translate`程式，並且將其執行路徑貼在程式內。
- 執行步驟
  1. 由GeoTiff檔案中切割指定範圍之地形數據，內插、再以GeoTiff格式寫出數據。
  1. 呼叫`gdal_translate`程式進行轉檔
  1. 準備其他aermap.inp所需參數
  1. 呼叫AERMAP程式完成作業
  1. 將數據寫成isc格式之地形檔案備用
  1. 將數據寫成kml格式以備檢查
- 有關GeoTiff格式的讀取、寫出等等，可以參考[筆記](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)及[df範例](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2df)、[nc範例](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2nc)

## 下載數值地形資料
### 內政部
- 內政部地政司定期公開其調查結果在**政府資料開放平台**，如"[2020年版全臺灣及部分離島20公尺網格數值地形模型DTM資料](https://data.gov.tw/dataset/138563)"。
  - 下載、解壓縮後可以得到一GeoTiff檔案，將其更名為taiwan.tiff備用。
  - 不分幅檔案可能較大，但處理還算順暢。
- 內政部亦有5M解析度地形數據，需另行向主管單位申請，並未在**政府資料開放平台**提供。
- 目前尚未有金門縣與連江縣數據，需另由其他來源取得。

### EIO
- [EIO(elevation)](https://pypi.org/project/elevation/)為pypi上的公開程式，會連結到NASA及NGA所維護的地形數據庫(SRTM 30m Global 1 arc second V003 )以及CGIAR-CSI所維護的 SRTM 90m Digital Elevation Database v4.1。
- 由於為全球性質，因此包括所有離島與境外其他國家範圍。
  - 索取範圍(--bounds)，為西南到東北角之經緯度，範例如下(向外擴張20倍間距)

```python
llmin=pnyc(xmin-2000.*dx/100-Xcent, ymin-2000*dx/100.-Ycent, inverse=True) #long/lati
llmax=pnyc(xmax+2000.*dx/100-Xcent, ymax+2000*dx/100.-Ycent, inverse=True)
smax=str(llmax[0])+' '+str(llmax[1])                #long/lati
smin=str(llmin[0])+' '+str(llmin[1])+' '+smax
```
- 雖然是動態連結下載，程式可以將原始數據(cache檔)儲存至指定目錄，如下次有下載需求時，就不會重複下載檔案。
  - 如下例將cache儲存在(--cache_dir)/tmp/gdal目錄
  - 須指定環境變數GDAL_DATA之位置
  - 下載結果檔案為一GeoTiff檔案。由於已經指定範圍，下載後就不必另行切割

```python
ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
tmp='/tmp/gdal'#_'+ran
pth1='/opt/anaconda3/bin/'
pth2='/opt/anaconda3/envs/ncl_stable/bin/'
eio='/opt/anaconda3/bin/eio'
gd_data=';export PATH='+pth1+':'+pth2+':$PATH;GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
TIF,DEM,NUL=fname+'.tiff',last+'.dem',' >>'+dir+'geninp.out'
cmd='cd '+dir+gd_data+eio+' --cache_dir '+tmp+' clip -o '+TIF+' --bounds '+smin+NUL
os.system('echo "'+cmd+'"'+NUL)
os.system(cmd)
```

## [gen_inp.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/Terrain/gen_inp.py)
### 引數
- GDNAME  Xinit Xnum Xdelta Yinit Ynum Ydelta
  - GDNAME:網格系統名稱(自行命名，將用做產生檔案之filename ROOT)
  - Xinit及Yinit為西南角落之TWD97座標(m)
  - Xnum及Ynum為x/y方向的點數(整數)，全部共Xnum*Ynum點
  - Xdelta及Ydelta為x/y方向的間距(m)，以正值為宜，但不限定。
  - 自由格式，不須逗號，不接受全形或中文碼
  - 範例 gd3 277500. 50 100. 2776500. 50 100.

### 輸入檔案
- taiwan.tiff([2020全臺20M_DTM](https://data.gov.tw/dataset/138563))
- 模版
  - aermap.inp
  - template.tiff
### 輸出檔案
- 輸入aermap.inp
- 檔名為gd3(範例)為首之6個檔案
	- gd3.kml→模擬範圍的等高線，彙入google map-my map作圖
	- gd3_re.dat→文字檔。以DISCCART方式標示每一格點的地形高程，併入iscst3的控制檔(.INP)內，取代原有XYINC設定
	- gd3_TG.txt→文字檔。iscst3所需要的地形網格外部檔案，須在控制檔(.INP)內設定TG INPUTFIL gd3_TG.txt，以進行連結。
		- 第1行：Xnum Ynum Xinit Yinit Xend Yend Xdelta Ydelta (Xend/Yend為東北角座標)
		- 第2行→第1個Y值，自西到東X方向所有點之高程，
		- 第3行→第2個Y值，自西到東X方向所有點之高程，
		- ...
	- gd3.tiff→作DEM檔案時使用。
		- 可以用QGIS檔GIS程式檢視。
		- 或以tif2kml.py檢視
		  - tif2kml.py -f  gd3.tiff
			- 結果檔為gd3.tiff.kml
	- gd3.dem→文字檔。aermap所需數值地形之外部檔案。aermap輸入檔案格式中較容易處理者(格式詳[DEM](https://gdal.org/drivers/raster/usgsdem.html?highlight=dem))。
- aermap執行結果
  - aermap.out：回饋輸入數據及錯誤訊息
  - MAPDETAIL.OUT：地圖的細節
  - MAPPARAMS.OUT：確認DEM的正確性
  - DOMDETAIL.OUT：如四角未落在DEM檔內，檢查範圍的設定  
  - gd3.REC：此檔將輸入AERMOD模式中，設定地形及特徵山高

### gen_inp.py程式下載
- [FAQ](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/Terrain/gen_inp.py)  

### 修改呼叫程式之路徑
- gdal_translate
  - 內設為/opt/anaconda3/envs/ncl_stable/bin/
- 環境變數GDAL_DATA
  - 內設為GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal
- AERMAP執行檔  
  - 內設為./

## gen_inp.py程式分段說明  
### 調用模組
- 因計算等濃度線，調用了`cntr`模組。在python3為第3方提供的軟體，並不屬`matplotlib`內容，需另行自[githup](https://github.com/matplotlib/legacycontour.git)安裝，詳附註。
- AERMAP使用的是UTM系統，因此需用到[utm](https://pypi.org/project/utm/)模組，在台灣地區不適用，需另安裝。台灣地區使用[twd97](https://pypi.org/project/twd97/)。絕對座標轉換使用utm及twd97，相對座標批次轉換，還是使用pyproj的Proj比較方便快速。
- tiff的讀寫，使用[rasterio](https://rasterio.readthedocs.io/en/latest/)，基本指令及應用詳見[筆記](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)說明。

```python
import numpy as np
from pandas import *
import twd97, utm
from scipy.interpolate import griddata
#python3 -m pip install --index-url https://github.com/matplotlib/legacycontour.git legacycontour
import legacycontour._cntr as cntr
import bisect
import sys,os
import tempfile as tf
from pyproj import Proj
import rasterio
from rasterio.transform import Affine
```

## Reference