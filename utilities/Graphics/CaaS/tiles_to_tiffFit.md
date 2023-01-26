---
layout: default
title:  tiles_to_tiffFit
parent: CaaS to Graphs
grand_parent: Graphics
last_modified_date: 2023-01-24 09:15:39
tags: graphics CGI_Python plume_model OpenTopoMap gdal
---
# 集合OTM圖磚並修剪成tiff檔py程式說明

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

- OpenTopoMap (OTM[^1])是以圖磚形式，將各解析度圖磚放在遠端伺服器供下載顯示。
- 因此，本程式([tiles_to_tiffFit.py][1])的重點就在下載需要的圖磚、將其整併、裁切出指定範圍的地形圖，可以給SURFER或其他繪圖軟體使用，詳細參閱[merged_GeoTIFF][5]之說明。
- 本程式雖然沒有單獨的網路服務版本，卻也是個獨立的程式，而且[知乎網友][2]確實也將其發展成能夠單獨執行的GUI程式。
- 或參母程式NCLonOTM[^4]、[NCL繪製煙流模式等值圖](../NCL/PLT_cn.md) [^5]

## 程式說明

### 模組

- 除一般需求外，特別需要gdal
- 由於台灣地區一般煙流模式使用者都可接受twd97座標系統，需要將其轉成經緯度LL系統

```python
#!/opt/anaconda3/envs/env_name/bin/python
import math
import urllib.request
import os, sys, subprocess
import glob
import subprocess
import shutil
from osgeo import gdal
import twd97
from pyproj import Proj


Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
def TWD2LL(E,N):
  x,y=E-Xcent,N-Ycent
  lon,lat=pnyc(x, y, inverse=True)
  return lat,lon

Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
```

### 伺服器與外部程式

- 除了OTM之外，此處也保留了開放街道、mapbox衛星等伺服器位置備用。
- 外部程式：
  1. 蒙太奇合併腳本：mgt.cs
  2. 座標平移：[gdal_translate][gdal_translate]
  3. [ImageMagicK][IM] convert
  4. 圖檔資訊：[gdalinfo][gdalinfo]
  5. awk、wget等指令
  6. gdal_merge.py(詳下)

```python
#---------- CONFIGURATION -----------#
#tile_server = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + os.environ.get('MAPBOX_ACCESS_TOKEN')
#tile_server = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
tile_server = "https://tile.opentopomap.org/{z}/{x}/{y}.png"
store_dir = os.path.join(os.path.dirname(__file__), '../pngs')
temp_dir = 'temp'
if not os.path.exists(temp_dir):os.system('mkdir -p '+temp_dir)
output_dir = '.'
mtg=os.path.join(os.path.dirname(__file__), 'mtg.cs')
zoomi = 22 #initial zoomming level
lon_min = 21.49147
lon_max = 21.5
lat_min = 65.31016
lat_max = 65.31688
gd='/opt/anaconda3/envs/env_name/bin/gdal_translate'
env='GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
convert='/usr/local/bin/convert'
gdalinfo='/opt/anaconda3/envs/env_name/bin/gdalinfo'
awkk='/opt/local/bin/awkk'
wget='/opt/local/bin/wget -q -U zzzzzzzz '
```

### 讀入引數

- 使用者至少需輸入[GRIDCART](../NCL/PLT_cn.md#re-gridcart)指令後6個數字
- 將煙流模式模擬範圍轉成LL座標系統

```python
larg=len(sys.argv)
if larg<6:
    fname=sys.argv[1]
    with open(fname,'r') as f:
        ll=[l for l in f]
    if ll[0][0]=='*':
      ll=ll[8:]
    X,Y=([float(l.split()[i]) for l in ll] for i in [0,1])
    mnX,mnY,mxX,mxY=(min(X),min(Y),max(X),max(Y))
else:
    mnX,nx,dx,mnY,ny,dy=(float(sys.argv[i]) for i in range(larg-6,larg))
    mxX,mxY=mnX+nx*dx,mnY+ny*dy
lat_min,lon_min=TWD2LL(mnX,mnY)
lat_max,lon_max=TWD2LL(mxX,mxY)
#-----------------------------------#
```

### 處理圖磚相關副程式

- 使用網友提供之程式碼（如programtalk網友[^3]、中文可參考知乎網友[^2]）
- 搜尋關鍵字：*tiles_to_tiff*

```python
from math import log, tan, radians, cos, pi, floor, degrees, atan, sinh
def sec(x):
    return(1/cos(x))


def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(tile_count*x, tile_count*y)

def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max), floor(y_min), floor(y_max))

def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return(lon1, lon2)

def mercatorToLat(mercatorY):
    return(degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = y * unit
    relative_y2 = relative_y1 + unit
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return(lat1, lat2)

def tile_edges(x, y, z):
    lat1, lat2 = y_to_lat_edges(y, z)
    lon1, lon2 = x_to_lon_edges(x, z)
    return[lon1, lat1, lon2, lat2]


def download_tile(x, y, z, tile_server):
    url = tile_server.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    store = f'{store_dir}/{x}_{y}_{z}.png'
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    if os.path.exists(store):
        os.system('ln -sf '+store+' '+path)	
        return(path)
    if "street" in tile_server:
        os.system(wget+url+' -O '+path)
    else:
        urllib.request.urlretrieve(url, path)
    os.system('cp '+path+' '+store)
    return(path)


def merge_tiles(input_pattern, output_path):

    merge_command = ['/opt/anaconda3/envs/env_name/bin/gdal_merge.py','-o', output_path]

    for name in glob.glob(input_pattern):
        merge_command.append(name)
    if os.path.exists(output_path):os.system('rm -f '+output_path)
    subprocess.call(merge_command)


def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)
```

### 圖檔的管理

- png
  - 雖然OSM/OTM的更新速度很快，沒有必要儲存在工作站，但如果在嘗試錯誤期間，同一地區地圖不斷重複下載，似乎也沒有必要。
  - 此處修改原程式的設計，先測試是否已經有過去下載過的檔案，如果沒有，才真的進行下載。依然暫時儲存在temp目錄下。
  - 執行裁切後，原程式內設是刪除temp目錄下所有檔案，在此修改成備份到工作站某處儲存備用。
- tif
  - 原程式是將結果檔案另存在output目錄之下，如此就檔案性質分類自然是為了方便檔案管理。
  - cgi_python每次呼叫會開一個暫存目錄(cntr_????)，output似乎沒有必要存在，為減少目錄的複雜性，在此取消output，將裁切結果直接存在cntr_????下即可。

### 求解最適解析度與下載

- 為避免解析度太高、下載檔案太多，以及解析度太低精度不足等等情況，以致[等值圖](../NCL/PLT_cn.md#結果圖檔)與[地圖](#fittedpng)的像素數差異太大。
- 經嘗試錯誤，下載檔案個數以20～150之間為合宜，需一一測試以得到最佳解析度（`zoom`）
- 以此解析度與範圍進行檔案下載。

```python
for zoom in range(zoomi,5,-1):
  x_min, x_max, y_min, y_max = bbox_to_xyz(
    lon_min, lon_max, lat_min, lat_max, zoom)
  ntiles=(x_max - x_min + 1) * (y_max - y_min + 1)
  if 150 > ntiles > 20:break
print(f"Downloading {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")
for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        print(f"{x},{y}")
        png_path = download_tile(x, y, zoom, tile_server)
        georeference_raster_tile(x, y, zoom, png_path)

print("Download complete")
```

### 拼接所有下載檔案

- 拼接腳本：詳述如下[mtg.cs](#mtgcs)
- 需要5個引數，分別為xy起訖序號與解析度

```python
print("Merging tiles")
merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
if 'satellite' not in tile_server:
  cmd ='cd '+temp_dir+';'
  cmd+= mtg+' {:d} {:d} {:d} {:d} {:d}'.format(x_min,x_max,y_min,y_max,zoom)
  os.system(cmd)
print("Merge complete")
```

### 精確裁切範圍邊界

- 使用gdalinfo得到檔案的左上、右下角座標
- 再使用gdal_translate切割出模式模擬範圍
- 最後使用ImageMagicK的convert程式轉成png檔案、輸出。

```python
llSE=' {:f} {:f} '.format(lon_max,lat_min)
llNW=' {:f} {:f} '.format(lon_min,lat_max)+llSE
UL={'ul':'\"Upper Left\"','lr':'\"Lower Right\"'}
aa={'lon':',','lat':')'}
cc={'lon':4,'lat':5}
for l in aa:
     for p in ['ul','lr']:
         exec("{:s}{:s}=subprocess.check_output(gdalinfo+' merged.tif |grep {:s}|'+awkk+' {:d}',shell=True).decode('utf8').split('{:s}\\n')".format(p,l,UL[p],cc[l],aa[l]))
         exec(p+l+'=[float(i) for i in '+p+l+' if len(i)>0][0]')

ULLR=' {:f} {:f} {:f} {:f} '.format(ullon, ullat, lrlon, lrlat)
os.system(env+gd+' -of GTiff -a_ullr'+ULLR+'-a_srs EPSG:4269 merged_montage.tif merged_montageC.tif')
os.system(env+gd+' -projwin '+llNW+' -of GTiff merged_montageC.tif fitted.tif')
os.system(convert+' fitted.tif fitted.png >&/dev/null')

#os.system('rm -f '+temp_dir+'/*.[t]*')
#shutil.rmtree(temp_dir)
#os.makedirs(temp_dir)
```

### 輸出圖檔格式的選擇

- [原程式][5]是設計讓圖檔自帶座標資料，因此使用GeoTiff格式
  - 如果NCL的等值線是按照座標繪製、地圖也是按照座標裁切，
  - 二者疊圖是再沒有需要知道座標值或任何座標系統相關資訊，tiff似無必要
- 經比較tiff的RGB色譜與png格格不入，縮放、疊圖時，都會發生變色的情形，
- 結論就是不必再維護tiff檔、利用Imagmagic的convert指令，將裁切結果都轉成png檔

### 程式下載

{% include download.html content="[tiles_to_tiffFit.py][1]" %}

## mtg.cs

### 合併(merge)或拼接(montage)

- [原程式][5]是使用gdal_merge.py這支程式進行下載圖檔的合併。但遭遇困難：

1. 整合時衛星圖像不會改變顏色，造成突兀。
2. OSM/OTM每個圖檔的顏色種類個數不同，合併是會按照第一個圖片的色譜來解讀後續圖檔，因此合併後全變成黑白版，因為如此才能達成最大公約數。
- 解決方案
  - 使用OSMosis(未執行)
  - 改採[ImageMagicK montage][mtg]拼接：
    - 唯一要修改檔案命名方式，原本x-y-z的檔名，轉變成z-y-x，以利程式按照各圖所在位置直接拼接
    - 需使用批次檔mtg.cs

### 腳本內容

- 使用[ImageMagicK的蒙太奇][mtg]程式
- 拼接之後檔案的地理訊息會消失，需執行[gdalwarp][gdalwarp]再予以定義。

```bash
$ cat /Users/Data/GIS/OSM_20210318/merged_GeoTIFF/mtg.cs

#$1=X1,$2=X2,$3=Y1,$4=Y2
X1=$1
X2=$2
Y1=$3
Y2=$4
Z=$5
for x in `seq $X1 $X2`; do for y in `seq $Y1 $Y2`; do ln -sf ${x}_${y}_${Z}.tif ${Z}_${y}_${x}.tif;done;done
/usr/local/bin/montage -mode concatenate -tile "$((X2-X1+1))x" "${Z}_*.tif" ../merged_montage.tif >&/dev/null
cd ..
/opt/anaconda3/envs/env_name/bin/gdalwarp -t_srs "+proj=longlat +ellps=WGS84" -to DST_METHOD=NO_GEOTRANSFORM merged.tif merged_montage.tif
```

## 基隆某電廠附近地形範例

### 控制條件

    STR:    290700 40 1250 2746400 40 1250
    檔案大小：3.7MB
    像素矩陣： (1464, 1457)

### fitted.png

![fitted.png](https://drive.google.com/uc?id=1QjRN3gTShz3jDu8hGgRhAlhAtqAOIpYF)

[^1]: OpenTopoMap：開放地形圖[官網](https://opentopomap.org)、[wiki](https://wiki.openstreetmap.org/wiki/OpenTopoMap)
[^2]: Python+gdal制作一个简单的地图下载器（支持高德、arcgis、google）、tom的gis笔记 (编辑于 2022-04-29 21:51)，[知乎專欄][2]。
[^3]: tiles-to-tiff, Jimmy Utterström(2019), [programtalk][3] or [bolg][5]
[^4]: 獨立程式說明[NCL貼在OTM底圖上](../NCL/NCLonOTM.md)或NCLonOTM遠端服務,[NCLonOTM-cgi.py](../CaaS/NCLonOTM-cgi.md)
[^5]: 煙流模式結果繪製等值線圖之NCL程式，詳見[程式說明](../NCL/PLT_cn.md)，或下載[PLT_cn.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/PLT_cn.ncl)

[1]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/tiles_to_tiffFit.py "tiles_to_tiffFit.py"
[2]: https://zhuanlan.zhihu.com/p/505288791 "tom的gis笔记（編按：含PysimpleGUI封包"
[3]: https://programtalk.com/vs4/python/jimutt/tiles-to-tiff/ "python/jimutt/tiles-to-tiff"
[5]: https://jimmyutterstrom.com/blog/2019/06/05/map-tiles-to-geotiff/ "Generate merged GeoTIFF imagery from web maps (xyz tile servers) with Python, Jimmy Utterström(2019)"
[IM]: https://imagemagick.org/index.php "mageMagick® is a free and open-source software suite for displaying, converting, and editing raster image and vector image files. It can read and write over 200 image file formats, and can support a wide range of image manipulation operations, such as resizing, cropping, and color correction."
[gdalinfo]: https://www.osgeo.cn/gdal/programs/gdalinfo.html "gdalinfo 程序列出了有关GDAL支持的栅格数据集的各种信息。"
[gdal_translate]: https://www.osgeo.cn/gdal/programs/gdal_translate.html "gdal_translate 程序可用于在不同格式之间转换栅格数据，可能在处理过程中执行一些操作，如子设置、重采样和重缩放像素。"
[mtg]: https://legacy.imagemagick.org/Usage/montage/#montage "The 'montage' command is designed to produce an array of thumbnail images. Sort of like a proof sheet of a large collection of images. "
[gdalwarp]: https://www.osgeo.cn/gdal/programs/gdalwarp.html "gdalwarp 程序是一种图像拼接、重投影和扭曲实用程序。该程序可以重新投影到任何支持的投影，也可以应用与图像一起存储的gcp，如果图像是带有控制信息的“原始”图像。"
