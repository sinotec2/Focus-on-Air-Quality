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
|Porosity|Porosity|%|0.2~0.55|por1,por2 in module depv_data_module||[total porosity](https://files.isric.org/public/wise/wise_30min_v3.zip)|
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

## Reading the isric tiff's
### 解題策略
- 由於isric採用多階層GIS形式對外提供數據，並非全球一個大檔案，而是約12.5公里見方一個tif檔案，因此需要解決檔案管理的問題、拼接的問題與效率的問題。
- 最高解析度為250M，因此用單一矩陣來承接每個檔案為不可行，必須將其線性化，並去掉無效值(水域)，以減少體積。
- 即使單一tif檔存成一個df，此df總集後將會有上億行，也不合理。須先將其整併(平均)成公里網格。
- 處理完tif成為df後，以cat指令一次拼接，成為範圍內公里解析度之大檔，再轉成CWBWRF_15Km網格系統

### file name rules
- filename sample:https://files.isric.org/soilgrids/latest/data/cec/cec_0-5cm_mean/tileSG-028-080/tileSG-028-080_1-1.tif
  - url=https://files.isric.org/soilgrids/latest/data/cec/cec_0-5cm_mean
  - rot=tileSG-${iy}-${ix}
  - tif=${rot}_${j}-${i}.tif
- second num:
  - seq. of latitude, from 90 to -90, every ~4 degree
  - 000~032 total 33 items
  - first try 010 to 025, from lat_deg 50~-10
- third num:
  - seq. of longitude, from -180 to 180, every ~4 degree
  - 000~088 total 88 items (without '037')
  - first try 060 to 088, from lon_deg 60 to 180
- total 1131 tiles
  - 每個tile目錄下最多4X4=16個檔案
  - 每個tif最多為450X450個網格，解析度250M，可能會有重疊，需個別校準。
- wget scripts
  - 如沒有該tile，程式會跳開不去搜尋
  - 如果已經有了tiff檔案，程式也會跳開不重複下載

### Downloading Scripts

```bash
url=https://files.isric.org/soilgrids/latest/data/cec/cec_0-5cm_mean
for iy in 0{10..25};do
for ix in 0{60..80};do
  rot=tileSG-${iy}-${ix}
  n=$(grep $rot fnames.txt |wc|awkk 1)
  if [ $n == 0 ];then continue;fi
  dir=${url}/${rot}
  for j in {1..4};do
  for i in {1..4};do
    tif=${rot}_${j}-${i}.tif
    if [ -e $tif ];then continue;fi
    fil=${dir}/$tif
    wget -q $fil
  done
  done
done
done
```  
- 經試誤發現在北方與東方尚有不足之坵塊，應是直角座標系統與地球系統造成之問題。再多向外補充。
- 最後有用到的tif檔僅有2736個。檔名存成tiffs.txt。
- 使用2迴圈同時下載其他深度之tif檔

```bash
for d in '5-15' '15-30' '30-60' '60-100';do sub gg2.cs $d;done
```
- gg2.cs

```bash
#for d in '0-5' '5-15' '15-30' '30-60' '60-100';do
d=$1
cec=cec_${d}cm_mean
mkdir -p $cec
cd $cec

url=https://files.isric.org/soilgrids/latest/data/cec/$cec

for tif in $(cat  ../tiffs.txt);do
rot=$(echo $tif|cut -d'_' -f1) #tileSG-${iy}-${ix}
dir=${url}/${rot}
if [ -e $tif ];then continue;fi
fil=${dir}/$tif
wget -q $fil
done
cd ..
#done
```

### rasterio functions
- img.width,img.height,img.count：東西、南北、高度之網格數
- img.read()將數據讀成矩陣
- img.lnglat()
  - 為tif[中心點](https://rasterio.readthedocs.io/en/latest/api/rasterio.rio.options.html)之經緯度
- img.bounds每圖四圍邊界座標
  - BoundingBox(left=7975000.0, bottom=3088250.0, right=8087500.0, top=3200750.0)
  - 以函數方式呼叫：minx=img.bounds.left
- img.xy(0,0)每格中心點座標
  - Out[1302]: (7975125.0, 3200625.0)    

### tiff2df
- 使用[rasterio]()讀取tif內容

```python
def tif2df(tif_name,nc_name):
  import numpy as np
  import netCDF4
  from pyproj import Proj
  import rasterio
  import numpy as np

  img = rasterio.open(tif_name)
  nx,ny,nz=img.width,img.height,img.count
  data=img.read()
  dx,dy=(img.bounds.right-img.bounds.left)/img.width,(img.bounds.top-img.bounds.bottom)/img.height
  
  nc = netCDF4.Dataset(nc_name, 'r')
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
  x0,y0=pnyc(img.lnglat()[0],img.lnglat()[1], inverse=False)
  x0,y0=x0-dx*(nx/2.),y0-dy*(ny/2.)
  x_1d=[x0+dx*i for i in range(nx)]
  y_1d=[y0+dy*i for i in range(ny)] 
  xm, ym = np.meshgrid(x_1d, y_1d)
  x,y=xm.flatten(),ym.flatten()
  lon, lat = pnyc(x, y, inverse=True)
  DD={'lon':lon,'lat':lat,'X':x,'Y':y,'val':data[0,:,:].flatten()}
  df=DataFrame(DD)
  boo=(df.lon>=60)&(df.lon<=180)&(df.lat>=-10)&(df.lat<=50)&(df.val!=-32768)
  df=df.loc[boo].reset_index(drop=True)
  if len(df)==0:
    df.to_csv(tif_name.replace('.tif','.csv'),header=None)
    return 1
  df['ix'],df['iy']=df.X//1000,df.X//1000
  df['ixy']=[str(i)+'_'+str(j) for i,j in zip(df.ix,df.iy)]
  df['ixy2']=df.ixy
  pv1=pivot_table(df,index='ixy',values='val',aggfunc=np.mean).reset_index()
  pv2=pivot_table(df,index='ixy',values='ixy2',aggfunc='count').reset_index()
  pv1['N']=pv2.ixy2
  pv1['X']=[float(i.split('_')[0])*1000 for i in pv1.ixy]
  pv1['Y']=[float(i.split('_')[1])*1000 for i in pv1.ixy]
  col=['X','Y','N','val']
  pv1[col].set_index('X').to_csv(tif_name.replace('.tif','.csv'),header=None)
  return 0
```
### 主程式
- 由於tif檔案甚多，必須採多工同步處理，所以此段必須獨立進行。
- 多工進行時會同時佔領同一檔，須以touch指令先行產生空白檔，讓其他程序跳開。
- 執行結果再以cat指令將其接續成一個大檔，另行讀取。

```python
import os
from pandas import *
with open('fnames.txt','r') as f:
  fnames=[i.strip('\n') for i in f]
nc_name='a0.nc'  
for tif_name in fnames:
  csv=tif_name.replace('.tif','.csv')
  if os.path.exists(csv):continue
  os.system('touch '+csv)
  print(tif_name,tif2df(tif_name,nc_name))
```
- 多工指令
  - 因pandas的pivot_table會自動啟動多核心運作，因此不必太多工，工作站會超頻運作。
  - 為避免touch時間太近，造成誤判，需減少多工線程數量，再行檢查。

```bash
for i in {1..20};do sub python ../tif2df.py ;done
```

### 後處理
- 將所有df檔案予以整併、轉成CWBWRF_15Km系統，輸出成nc檔案繪圖
  - `cat ../header.txt *.csv > all.txt`

```python
fname='a1.nc'
nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v=V[3][0]
nc[v][:]=0

df=read_csv('all.txt')
x,y=df.X,df.Y
df['ix']=np.array((x-nc.XORIG)/nc.XCELL,dtype=int)
df['iy']=np.array((y-nc.YORIG)/nc.YCELL,dtype=int)
df=df.loc[(df.ix>=0)&(df.ix<ncol)&(df.iy>=0)&(df.iy<nrow)].reset_index(drop=True)
df['ixy']=[str(i)+'_'+str(j) for i,j in zip(df.ix,df.iy)]
df['vn']=df.val*df.N
pv=pivot_table(df,index='ixy',values=['N','vn'],aggfunc=np.sum).reset_index()
pv['ix']=[int(i.split('_')[0]) for i in pv.ixy]
pv['iy']=[int(i.split('_')[1]) for i in pv.ixy]
pv['cec']=pv.vn/pv.N
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
var=np.zeros(shape=(nrow,ncol))
var[pv.iy,pv.ix]=pv.cec
nc[v][0,0,:,:]=var[:,:]
nc.close()
```

### Results

| ![CEC.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CEC.PNG) |
|:--:|
| <b>圖 d01範圍表土CEC(cmolc/Kg)</b>|  

## Reading the earthstat tiff's
### Crop names Dict
- CCTM系統中的種穀物詳[亞洲土地使用檔案>背景](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/LAND/CWBWRF_15k/#背景)
- 175種穀物為解開[earthstat>壓縮檔](http://www.earthstat.org/harvested-area-yield-175-crops/)之結果
- 可食豆：包括175種穀物中所有含有bean之種類
- earthstat沒有乾草(straw)或其他畜牧用草等名稱，只有mixedgrass比較接近。
- grain/silage之分，前者為穀粒、人類食物或種子，後者為畜用。
- other_crop，經查[wiki](https://zh.wikipedia.org/wiki/谷物)，21種穀物中漏了**雜穀**，將其列為other_crop
- [春麥/冬麥](https://read01.com/zh-tw/mmPJxE.html#.YeiuDdXP2po)在earthstat無法區分，只能依照**長城**所在緯度(略以40度)為界區別之，再按區分結果群聚之現象詳細界定(IY=320)。

|spec in CCTM sys 21 kinds|175 spec in earthstat database|中文名稱|
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
|wheat_spring|wheat(lat>40)|春麥、長城以北|
|wheat_winter|wheat(lat<=40)|冬麥|


### tif2nc
- 這支副程式需要3個引數：tiff檔名、nc檔名、以及lev層數
  - tiff檔：全球為範圍，解析度1~10Km，高於nc檔案，採取aggregation整併到nc網格系統
  - nc檔：東亞範圍(CWBWRF_15Km網格系統)
- lev層數：0~20共21層
  - lev=3時，nc檔將會累加tiff檔的內容，因此要記得先在主程式將nc檔清空。(lev其他值會在副程式內清空)
  - lev=19或20時(c='wheat')，只會將tiff檔內容的一部分轉移到nc檔內，以iy=320為界

```python
def tif2nc(tif_name,nc_name,lev):
  import numpy as np
  import netCDF4
  from pyproj import Proj
  import rasterio
  import numpy as np

  img = rasterio.open(tif_name)
  nx,ny,nz=img.width,img.height,img.count
  if nz!=1:return -1
  dx,dy=360./(nx-1),180./(ny-1)
  lon_1d=[-180+dx*i for i in range(nx)]
  lat_1d=[90-dy*i for i in range(ny)]
  data=img.read()
  lonm, latm = np.meshgrid(lon_1d, lat_1d)
  DD={'lon':lonm.flatten(),'lat':latm.flatten(),'val':data.flatten()}
  df=DataFrame(DD)
  boo=(df.lon>=60)&(df.lon<=180)&(df.lat>=-10)&(df.lat<=50)
  df=df.loc[boo].reset_index(drop=True)
  
  nc = netCDF4.Dataset(nc_name, 'r+')
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))

  #d00範圍：北緯-10~50、東經60~180。'area': [50, 60, -10, 180,],
  x,y=pnyc(list(df.lon),list(df.lat), inverse=False)
  x,y=np.array(x),np.array(y)
  df['ix']=np.array((x-nc.XORIG)/nc.XCELL,dtype=int)
  df['iy']=np.array((y-nc.YORIG)/nc.YCELL,dtype=int)
  df=df.loc[(df.ix>=0)&(df.ix<ncol)&(df.iy>=0)&(df.iy<nrow)].reset_index(drop=True)
  df['ixy']=[str(i)+'_'+str(j) for i,j in zip(df.ix,df.iy)]
  pv=pivot_table(df,index='ixy',values='val',aggfunc=np.sum).reset_index()
  pv['ix']=[int(i.split('_')[0]) for i in pv.ixy]
  pv['iy']=[int(i.split('_')[1]) for i in pv.ixy]
  var=np.zeros(shape=(nrow,ncol))
  var[pv.iy,pv.ix]=pv.val
  if lev==3: #beansedible
    nc[V[3][0]][0,lev,:,:]+=var[:,:]
  else:
    nc[V[3][0]][0,lev,:,:]=0.
    if lev==19: #wheat_spring
      nc[V[3][0]][0,lev,320:,:]=var[320:,:]
    elif lev==20: #wheat_winter
      nc[V[3][0]][0,lev,:320,:]=var[:320,:]
    else:
      nc[V[3][0]][0,lev,:,:]+=var[:,:]
  nc.close()
  return 0
```
### 主程式
- 轉錄各種穀物在網格範圍內的總種植面積(hectare)，存到0~20層

```python
nc_name='temp.nc'
fnameO='d21_175.json'
with open(fnameO,'r') as jsonfile:
  d21_175=json.load(jsonfile)
crop21=list(d21_175)
crop21.sort()
#18項1對1
s=set([d21_175[i] for i in crop21 if i not in ['wheat_spring','wheat_winter','beansedible']]) 
d175_21={d21_175[i]:crop21.index(i) for i in s}
fn1,fn2,fn3='HarvestedAreaYield175Crops_Geotiff/','_HarvAreaYield_Geotiff/','_HarvestedAreaHectares.tif'
for c in s:
  tif_name=fn1+c+fn2+c+fn3
  i=tif2nc(tif_name,nc_name,d175_21[c])
#crop21.index('beansedible')=3，多對1
for c in ['broadbean', 'greenbean', 'greenbroadbean', 'stringbean']:
  tif_name=fn1+c+fn2+c+fn3
  i=tif2nc(tif_name,nc_name,3)
#1對多
c='wheat' 
tif_name=fn1+c+fn2+c+fn3
for lev in [19,20]:
  i=tif2nc(tif_name,nc_name,lev)
```
- 區分灌溉與旱作(rainfed)

```python
fname='irr28.nc'
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
irr=nc[V[3][0]][0,0,:,:] #28種灌溉形式之總合(area fraction)

fname='temp.nc'
nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v=V[3][0]
nt,nlay,nrow,ncol=(nc.variables[v].shape[i] for i in range(4))
km2=nc[v][0,:21,:,:]*0.01
for lev in range(21,42):
  nc[v][0,lev,:,:]=irr[:,:]*km2[lev-21,:,:]
for lev in range(21):
  nc[v][0,lev,:,:]=(1-irr[:,:])*km2[lev,:,:]
svar=np.sum(nc[v][0,:,:,:],axis=0)
a=np.where(svar<255,255,svar)
nc[v][0,:,:,:]=nc[v][0,:,:,:]/a[None,:,:]
nc.close()
```
### Results

| ![Rice.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/Rice.PNG) |
|:--:|
| <b>圖 d01範圍大米種植面積的網格佔比(%)</b>|  
| ![Rice_irr.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/Rice_irr.PNG) |
|:--:|
| <b>圖 d01範圍大米(灌溉)種植面積的網格佔比(%)</b>|  

## Reference
- W. J. Rawls, D. L. Brakensiek, K. E. Saxtonn (1982). **Estimation of Soil Water Properties**. Transactions of the ASAE. 25, 1316–1320. https://doi.org/10.13031/2013.33720
  - [lookup table](https://www.researchgate.net/figure/The-RA-soil-hydraulic-property-look-up-table-Rawls-et-al-1982_tbl3_254240905)
- Aliku, O., Oshunsanya, S.O. (2016). **Establishing relationship between measured and predicted soil water characteristics using SOILWAT model in three agro-ecological zones of Nigeria**. Geosci. Model Dev. Discuss. https://doi.org/10.5194/gmd-2016-165
  - Field Capacity moisture (33 kPa), %v

