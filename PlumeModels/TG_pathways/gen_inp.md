---
layout: default
title: Prepare and Exec. of AERMAP
parent: TG Pathways
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
- [AERMAP](https://www.epa.gov/scram/air-quality-dispersion-modeling-related-model-support-programs#aermap)是[AERMOD](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#aermod)地形檔案的前處理程式，執行複雜地形中的煙流模擬必經的程序。最大的障礙在於必須要以美國地理調查局的[DEM格式](https://gdal.org/drivers/raster/usgsdem.html?highlight=dem)讀取數值地形資料，過去的作法包括：
  - 直接按照[AERMAP]()結果格式將地形高程與山丘高度(特徵高)，寫出檔案，完全取代[AERMAP]()。
  - 事先處理台灣地區20M的數值地形成為DEM格式，為[鳥哥](https://linux.vbird.org/enve/aermap-op.php)的作法，好處是一般使用者不需自行轉檔，較為單純。且為內政部最新調查成果較符合實況。壞處是DEM檔會非常大，且增加[AERMAP]()篩選的時間。
  - 事先將台灣地區數值地形切割並處理成較小範圍的DEM檔案，因為[AERMAP]()可以同時讀取數個DEM檔案。從其中整併出所需要的範圍進行內插。(not tried)
  - 使用者自行轉檔方案(this note)：將[gdal_translate](https://gdal.org/programs/gdal_translate.html)指令包裹在python程式中，只需轉換所需的範圍，較為經濟有效。缺點是使用者還是必須下載[正確版本](https://www.gisinternals.com/release.php)的[gdal_translate](https://gdal.org/programs/gdal_translate.html)程式，並且將其執行路徑貼在程式內。
- 執行步驟
  1. 由GeoTiff檔案中切割指定範圍之地形數據，內插、再以GeoTiff格式寫出數據。
  1. 呼叫[gdal_translate](https://gdal.org/programs/gdal_translate.html)程式進行轉檔
  1. 準備其他[aermap.inp](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/aermap.inp)所需參數
  1. 呼叫[AERMAP]()程式完成作業
  1. 將數據寫成isc格式之地形檔案備用
  1. 將數據寫成kml格式以備檢查
- 有關GeoTiff格式的讀取、寫出等等，可以參考[筆記](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)及[df範例](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2df)、[nc範例](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/Soils/#tiff2nc)

## 下載數值地形資料
### 內政部
- 內政部地政司定期公開其調查結果在**政府資料開放平台**，如"[2020年版全臺灣及部分離島20公尺網格數值地形模型DTM資料](https://data.gov.tw/dataset/138563)"。
  - 下載、解壓縮後可以得到一GeoTiff檔案，將其更名為taiwan2020.tiff備用。
  - 不分幅檔案可能較大，但處理還算順暢。
- 內政部亦有5M解析度地形數據，需另行向主管單位申請，並未在**政府資料開放平台**提供。
- 目前尚未有金門縣與連江縣數據，需另由其他來源取得。

### EIO
- [EIO(elevation)](https://pypi.org/project/elevation/)為pypi上的公開程式，會連結到NASA及NGA所維護的地形數據庫(SRTM 30m Global 1 arc second V003 )以及CGIAR-CSI所維護的 SRTM 90m Digital Elevation Database v4.1。
- 由於為全球性質，因此包括所有離島與境外其他國家範圍。
  - 索取範圍(`--bounds`)，為西南到東北角之經緯度，範例如下(向外擴張20倍間距)

```python
llmin=pnyc(xmin-2000.*dx/100-Xcent, ymin-2000*dx/100.-Ycent, inverse=True) #long/lati
llmax=pnyc(xmax+2000.*dx/100-Xcent, ymax+2000*dx/100.-Ycent, inverse=True)
smax=str(llmax[0])+' '+str(llmax[1])                #long/lati
smin=str(llmin[0])+' '+str(llmin[1])+' '+smax
```
- 雖然是動態連結下載，程式可以將原始數據(cache檔)儲存至指定目錄，如下次有下載需求時，就不會重複下載檔案。
  - 如下例將cache儲存在(`--cache_dir`)/tmp/gdal目錄
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

## [gen_inp.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/gen_inp.py)
### 引數
- GDNAME  Xinit Xnum Xdelta Yinit Ynum Ydelta
  - GDNAME:網格系統名稱(自行命名，將用做產生檔案之filename ROOT)
  - Xinit及Yinit為西南角落之TWD97座標(m)
  - Xnum及Ynum為x/y方向的點數(整數)，全部共Xnum*Ynum點
  - Xdelta及Ydelta為x/y方向的間距(m)，以正值為宜，但不限定。
  - 自由格式，不須逗號，不接受全形或中文碼
  - 範例 gd3 277500. 50 100. 2776500. 50 100.

### 輸入檔案
- taiwan2020.tiff([2020全臺20M_DTM](https://data.gov.tw/dataset/138563))
- 模版
  - [aermap.inp](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/aermap.inp)
  - template.tiff
### 輸出檔案
- 輸入[aermap.inp](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/aermap.inp)
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
  - gd3.REC：此檔將輸入[AERMOD]()模式中，設定地形及特徵山高

### gen_inp.py程式下載
- [FAQ](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/gen_inp.py)  

### 修改呼叫程式之路徑
- [gdal_translate](https://gdal.org/programs/gdal_translate.html)
  - 內設為/opt/anaconda3/envs/ncl_stable/bin/
- 環境變數GDAL_DATA
  - 內設為GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal
- [AERMAP]()執行檔  
  - 內設為./

## gen_inp.py程式分段說明  
### 調用模組
- 因計算等濃度線，調用了`cntr`模組。
  - 在python2為matplotlib的內容
  - 在python3為第3方提供的軟體，並不屬`matplotlib`內容，需另行自[githup](https://github.com/matplotlib/legacycontour.git)安裝，詳附註。
  - 此模組主要用在副程式[cntr_kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/cntr_kml.py)，見[wr_kml筆記](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)。

- [AERMAP]()使用的是UTM系統，因此需用到[utm](https://pypi.org/project/utm/)模組，在台灣地區不適用，需另安裝。台灣地區使用[twd97](https://pypi.org/project/twd97/)。絕對座標轉換使用utm及twd97，相對座標批次轉換，還是使用pyproj的Proj比較方便快速。
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
from cntr_kml import cntr_kml
```

### 內政部dtm檔案之讀取、切割、內插與轉存
- 讀取：
  - 使用[rasterio](https://rasterio.readthedocs.io/en/latest/intro.html)，因南北向y軸是由北向南、`(x0,y0)`為左上方座標，需進行轉置
  - 矩陣用`np.flip`、序列用`.sort()`

```python
#read the 20M DTM data TIFF from https://dtm.moi.gov.tw/2020dtm20m/台灣本島及4離島\(龜山島_綠島_蘭嶼_小琉球\).7z
fname='taiwan2020.tif'
img = rasterio.open(fname)
data=np.flip(img.read()[0,:,:],[0])
x0,y0=img.xy(0,0)
mn=img.shape
dxm,dym=(img.bounds.right-img.bounds.left)/img.width,-(img.bounds.top-img.bounds.bottom)/img.height
x1d = np.array([x0+dxm*i for i in range(mn[1])])
y1d = np.array([y0+dym*i for i in range(mn[0])])
y1d.sort()
```
- 切割
  - 用[bisect](https://docs.python.org/zh-tw/3/library/bisect.html)定位所需座標範圍
  - 向外再擴張2格40M
  - 將高程矩陣、座標值x及y線性化，準備進行內插

```python
I1=bisect.bisect_left(x1d,x_mesh[0])-2;I2=bisect.bisect_left(x1d,x_mesh[-1])+2
J1=bisect.bisect_left(y1d,y_mesh[0])-2;J2=bisect.bisect_left(y1d,y_mesh[-1])+2
c=data[J1:J2,I1:I2].flatten()
c=np.where(c<0,0,c)
x=np.array([x1d[I1:I2] for j in range(J2-J1)]).flatten()
y=np.array([[j for i in range(I2-I1)] for j in y1d[J1:J2]]).flatten()
```
- 內插
  - [AERMAP]()應有內插功能，此處內插是為ISC模式與結果展示所需。DEM與接受點的網格系統都一樣，在[AERMAP]()內也可提高計算速度。
  - 因一般20M的解析度較需求為高，採用線性內插即可

```python
#interpolation from points to the receptor grid (x_g, y_g)
points=[(i,j) for i,j in zip(x,y)]
grid_z2 = griddata(points, c, (x_g, y_g), method='linear')
```

- 轉寫
  - for [gdal_translate](https://gdal.org/programs/gdal_translate.html)
  - 需以經緯度座標輸出
  - 南北向轉置

```python
#save tiff file
TIF,DEM,NUL=fname+'.tiff',last+'.dem',' >>'+dir+'geninp.out'
os.system('cp template.tiff '+TIF)
resx,resy=(np.max(lon)-np.min(lon))/(nx+2*M-1),(np.max(lat)-np.min(lat))/(ny+2*M-1),
transform = Affine.translation(np.min(lon), np.max(lat)) * Affine.scale(resx, -resy)
new_dataset = rasterio.open(TIF,'w',driver='GTiff',height=grid_z2.shape[0],width=grid_z2.shape[1],count=1,
  dtype=grid_z2.dtype,crs='+proj=latlong',transform=transform,)
data=np.flip(grid_z2,[0])
new_dataset.write(data, 1)
new_dataset.close()
```

### 呼叫[gdal_translate](https://gdal.org/programs/gdal_translate.html)程式進行轉檔
- 因目前還沒有發展讀寫DEM格式的獨立模組。因此還是以[gdal_translate](https://gdal.org/programs/gdal_translate.html)的使用為主。
- [gdal_translate](https://gdal.org/programs/gdal_translate.html)對範圍(`-projwin`)的界定方式是西北角與東南角經緯度。呼叫方式如下：
  - 此處讀取前述GeoTiff範圍將內縮一格，為避免邊界上剪裁太過密合。
  - 順序為先經度、再緯度
- [gdal_translate](https://gdal.org/programs/gdal_translate.html)程式與數據的路徑
  - 內設為`/opt/anaconda3/envs/ncl_stable/bin/`及`/opt/anaconda3/envs/py37/share/gdal`
  - 如有不同應予修改

```python
TIF,DEM,NUL=fname+'.tiff',last+'.dem',' >>'+dir+'geninp.out'
# convert the tiff to dem
llSE=str(lon[1,-2])+' '+str(lat[1,-2])
llNW=str(lon[-2,1])+' '+str(lat[-2,1])+' '+llSE
pth1='/opt/anaconda3/bin/'
pth2='/opt/anaconda3/envs/ncl_stable/bin/'
gd_data=';export PATH='+pth1+':'+pth2+':$PATH;GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal'
os.system('echo "before gdal"'+NUL)
gd='gdal_translate'
cmd='cd '+dir+gd_data+gd+' -of USGSDEM -ot Float32 -projwin '+llNW+' '+TIF+' '+DEM+NUL
os.system('echo "'+cmd+'"'+NUL)
os.system(cmd)
```    

### [aermap.inp](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/aermap.inp)之改寫與執行
- [aermap.inp](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/aermap.inp)為aermap控制檔案之模版，此檔案會加入指定範圍之參數與接受點座標
  - DATAFILE：aermap的結果檔，輸出給aermod使用(.REC)
  - DOMAINXY：接受點的UTM範圍，確認邊界角落都在DEM檔案範圍內
  - ANCHORXY：接受點自訂座標值(台灣地區建議直接使用twd97座標系統)與UTM間錨定點的對照關係。
- xy：UTM之`(x,y)`值，2維矩陣。因旋轉後可能有些歪斜，因此需取最大範圍
- uxanc,uyanc：錨定點(此處取模擬範圍的中心點，以避免誤差累計)的UTM值

```python
#generate aermap.inp,
xy=utm.from_latlon(lat,lon)
uxmn,uxmx=int(np.min(xy[0][M:-M,M])),int(np.max(xy[0][M:-M,-M]))
uymn,uymx=int(np.min(xy[1][M,M:-M])),int(np.max(xy[1][-M,M:-M]))
co,an,z='   DOMAINXY  ','   ANCHORXY  ',' 51 '
UTMrange=co+str(uxmn)+' '+str(uymn)+z+str(uxmx)+' '+str(uymx)+z
xmid,ymid=(xmin+xmax)/2., (ymin+ymax)/2.
llanc=pnyc(xmid-Xcent, ymid-Ycent, inverse=True)
uxanc,uyanc=utm.from_latlon(llanc[1],llanc[0])[0:2]
UTMancha=an+str(int(xmid))+' '+str(int(ymid))+' '+str(int(uxanc))+' '+str(int(uyanc))+z+'0'

#change the contain of aermap
text_file = open("aermap.inp", "r+")
d=[line for line in text_file]
keywd=[i[3:11] for i in d]
ifile=keywd.index('DATAFILE')
idmxy=keywd.index('DOMAINXY')
ianxy=keywd.index('ANCHORXY')
ihead=keywd.index('ELEVUNIT')
iend=d.index('RE FINISHED\n')

text_file = open("aermap.inp", "w")

x0,y0=xmin,ymin
sta='RE GRIDCART '+last+' STA\n'
args[0]=last
STR='RE GRIDCART {:s} XYINC {:s} {:s} {:s} {:s} {:s} {:s}\n'.format(*args)
s=[sta,STR,sta.replace('STA','END')]
for l in range(ihead+1):
#  if l == ifile:
#    text_file.write( "%s" % '   DATAFILE  '+DEM+'\n')
  if l == idmxy:
    text_file.write( "%s" % UTMrange+'\n')
  elif l == ianxy:
    text_file.write( "%s" % UTMancha+'\n')
  else:
    text_file.write( "%s" % d[l])
for l in range(len(s)):
    text_file.write( "%s" % s[l])
for l in range(iend,len(d)):
    text_file.write( "%s" % d[l])
text_file.close()
```
- [AERMAP]()之執行

```python
# execute the aermap
aermap_path='./'
os.system(aermap_path+'aermap >& isc.out')
```

## 其他處理
### KML檔案之輸出
- 呼叫[cntr_kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/cntr_kml.py)
- 參考[等值線之KML檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)之說明

```python
result=cntr_kml(grid_z2, lon, lat, fname)
```

### 複雜地形ISC模式所需輸入檔
- 因GeoTiff檔案提供了較大的範圍，實際輸出時回歸正確範圍`[M:-M,M:-M]`
- 使用簡單的with open及write指令，將高程寫進檔案中
  - re.dat：接受點位置及高程
  - TG.txt：高程網格數據檔

```python
# generate the ISC files
if M>0:
  grid_z2=grid_z2[M:-M,M:-M]
  x_g, y_g = x_g[M:-M,M:-M], y_g[M:-M,M:-M] 

xy = np.array([[(i, j) for i, j in zip(x_g[k], y_g[k])] for k in range(ny)])
with open(fname + '_re.dat','w') as f:
  f.write('RE ELEVUNIT METERS\n')
  for j in range(ny):
    for i in range(nx):
      f.write('RE DISCCART '+str(xy[j,i,0])+' '+str(xy[j,i,1])+' '+str(grid_z2[j,i])+'\n')

#terrain grid file
with open(fname + '_TG.txt','w') as f:
  f.write(str(nx)+' '+str(ny)+' '+str(xmin)+' '+str(xmax)+' '+str(ymin)+' '+str(ymax)+' '+str(dx)+' '+str(dy)+'\n')
  for j in range(ny):
    ele=[str(int(grid_z2[j,i])) for i in range(nx)]
    st=ele[0]
    for i in range(1,nx):
      st+=' '+ele[i]
    f.write(st+'\n')
```
    
## 結果比較
### 林口電廠範例貼圖結果

| ![kml_demo.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/kml_demo.png) |
|:--:|
| <b>圖 林口電廠周邊地形KML檔案輸出結果範例</b>|  

### 檢查項目
- [範圍]()：是否以污染源排放為中心、是否符合設定範圍(海面範圍可視情況減少)
- [高值]()部分：是否符合地圖（鄉鎮區界線、稜線道路、山峰位置等）
  - 煙流大致會在2倍煙囪高度之等高線，產生高值。
  - 有群峰之地形範圍，煙流會在第一個碰觸點產生高值。
- [解析度]()：太低→地形特徵會消失。煙流本身會模糊化，解析度太高會增加執行時間，沒有必要。
- 等高線：一般公路設計會平行於等高線，可藉地圖中公路的走向，檢視地形數據結果的正確性
- 低值位置：一般地圖上是河流、住家村落、陂塘、農地等。
- 海岸線：等高線是否與地圖之海岸線平行

### 林口電廠周邊地形檔輸入aermod模擬結果範例
- mmif氣象1/21\~31
- 有建築物

| ![noterr.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/noterr.png) |![withterr.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/withterr.png)|
|:--:|:--:|
| <b>無地形，煙流偏西南方，為東北季風影響</b>|有地形，煙流方向偏南，擴散範圍受到限制，集中在河谷低地。受限於80\~100M等高線範圍。最大值較高51\~754&mu;/M<sup>3</sup>|

## Reference