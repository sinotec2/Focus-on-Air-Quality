---
layout: default
title: 海溫的讀取
parent: wind models
nav_order: 1
---
# 海溫的讀取
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

### 背景
海面溫度雖然變化緩慢，但牽動全球的大氣環流，因此在氣象模擬過程中是一項非常重要的地面強制邊界。

### 再分析資料來源與下載
- [NASS多尺度超高解析度海溫數據MUR](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)的解析度為0.01度網格，時間解析度為小時，年代自2002年5月底開始迄今。下載需要登入，只提供https點選方式下載。檔案以年代為目錄，每天一個檔案。檔名協定方式：
```bash
yyyy=4碼年代2002~迄今
mm=2碼月份01~12
dd=2碼日期01~31
nc=https://cmr.earthdata.nasa.gov/virtual-directory/collections/C1996881146-POCLOUD/temporal/$yyyy/$mm/$dd/$yyyy$mm${dd}090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1
```

- NASA再分析0.25度日均值(`nc`檔案)，檔案有3個出處：
    - [海洋物理分散式數據庫活化中心(PODAAC)](https://podaac.jpl.nasa.gov/datasetlist?search=AVHRR_OI-NCEI-L4-GLOB-v2.1)，逐日存檔，數據項目包括海溫、誤差、海冰部分等，海溫單位為K。檔案名稱協定：
    ```bash
    yyyy=4碼年代2016~迄今
    jul=3碼julian日期001~366
    ymd=8碼年月日
    nc=https://podaac-opendap.jpl.nasa.gov/opendap/allData/ghrsst/data/GDS2/L4/GLOB/NCEI/AVHRR_OI/v2.1/$yyyy/$jul/${ymd}120000-NCEI-L4_GHRSST-SSTblend-AVHRR_OI-GLOB-v02.0-fv02.1.nc
    ```
    - [國家環境資訊中心(NCEI)](https://www.ncei.noaa.gov/products/optimum-interpolation-sst)，也是逐日存檔，方法版本似乎與前述一樣，數據項目包括海溫、偏差、誤差、海冰百分比等，海溫單位為C。檔案名稱協定：
    ```bash
    yyyy=4碼年代1981(0901)~迄今
    mm=2碼月份01~12
    dd=2碼日期01~31
    nc=https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/$yyyy$mm/oisst-avhrr-v02r01.$yyyy$mm$dd.nc
    ```
    - [海洋物理實驗室(PSL.NOAA)](https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/)有全球重要的海洋物理數據，集合成全年一個檔案，一個檔案一個變數，sst單位為C。
    ```bash
    yyyy=4碼年代1981~迄今
    nc=https://downloads.psl.noaa.gov/Datasets/noaa.oisst.v2.highres/sst.day.mean.$yyyy.nc
    ```
    - NASA或NOAA的再分析數據都是`nc`檔案，使用wget或curl都可以直接下載。下載後`nc`檔案可以用fortran或python程式解讀、切割、轉檔。

- [ECMWF再分析數據(ERA5)](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation)
    - 提供有31公里逐時之高解析度檔(HRES)、以及10個叢集低解析度檔案(EDA)。最早回溯到1950年1月。每月更新到前3個月的數據。檔案格式為`grib2`檔案(也有試驗性質的`nc`檔)。
    - 下載點為`ERA5 hourly data on single levels from 1979 to present`，方式為[網頁](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=form)選取登入下載，及(或)[CDS API](https://cds.climate.copernicus.eu/api-how-to)(也需要登入取得API鑰匙) python模組，如以下範例

```python
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': 'sea_surface_temperature',
        'year': '2018',
        'month': '04',
        'day': ['{:02d}'.format(i) for i in range(1,31)],                
        'time': ['{:02d}:00'.format(i) for i in range(24)],
    },
    'download.grib')
```
    - ERA5檔案格式是`grib2`，下載後可以用`ungrib.exe`來解讀。
    - ecmwf也綜合了NOAA、MetOP等眾多衛星所拍到的海溫數據，下載點：[Sea surface temperature daily data from 1981 to present derived from satellite observations](https://cds.climate.copernicus.eu/cdsapp#!/dataset/satellite-sea-surface-temperature?tab=form)

### NOAA GFS模式輸出
模式輸出的好處是有較高的系統性，也有逐時、高解析度的架構，雖然沒有歷史數據，但還是可以藉由每一天自動化下載排程，逐漸累積。
```bash
kuang@114-32-164-198 /Users/WRF4.1/NCEP/SST
$ cat get_noaa.cs
wget=/opt/local/bin/wget
ftp=ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/sst.
today=$(date +"%Y%m%d")
yesd=$(date -v-1d -j -f "%Y%m%d" "${today}" +%Y%m%d)
yr=$(date -v-1d -j -f "%Y%m%d" "${today}" +%Y)
pth=/Users/WRF4.1/NCEP/SST/$yr
mkdir -p $pth
cd  $pth
$wget -q $ftp${yesd}/rtgssthr_grb_0.083.grib2 -O rtg_sst_grb_hr_0.083.$yesd
```
GFS檔案格式是`grib2`，下載後可以用`ungrib.exe`來解讀。


### nc檔案轉WPS/ungrib.exe暫存檔格式(intermediate format)
WPS歷來解讀grib檔之後，在進入metgrid.exe之前有個暫存檔案，其格式為Fortran binary檔案，稱之為**WPS暫存檔格式**([intermediate format](https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.3/users_guide_chap3.html#_Writing_Meteorological_Data))，FNL檔案經ungrib.exe轉檔成為FILE:YYYY-MM-DD-HH_00, 之暫存檔，海溫則轉成SST:YYYY-MM-DD-HH_00。因此如果另有海溫數據來源，在WPS過程中即可跳過SST之ungrib.exe，直接將數據寫成暫存檔格式，以進行下一步驟metgrid.exe的整併與轉檔。
轉換方式有fortran及python兩種：
#### fortran
網友[WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)提供[MUR](https://podaac.jpl.nasa.gov/dataset/MUR-JPL-L4-GLOB-v4.1)的轉檔fortran檔案。執行時會讀取工作目錄中的namelist.wps與geo_em.d01.nc來切割時間與空間範圍。

#### python
使用netCDF4與[pywinter](https://pywinter.readthedocs.io/en/latest)之模組進行讀寫，以下範例為2018年全年日均海溫檔案中提取4/5~4/8日數據：

```python   
$ cat /Users/WRF4.1/NCEP/SST/2018/transNC2inter.py
import netCDF4
import numpy as np
import pywinter.winter as pyw
from datetime import datetime

fname='sst.day.mean.2018.nc'
data = netCDF4.Dataset(fname, 'r')
lat = data.variables['lat'][:]
lon = data.variables['lon'][:]
dlat = np.abs(lat[1] - lat[0])
dlon = np.abs(lon[1] - lon[0])

#Geo0是inter0指定投影方式
winter_geo = pyw.Geo0(lat[0],lon[0],dlat,dlon)

#度C要加273成為度K
sst=data.variables['sst'][:]+273
# 年度開始日，也是時間維度0的基準
bdate=datetime(2018, 1, 1)

# 提取時間範圍的起始日Start Date
sdate=datetime(2018, 4, 5)

# 日數差值即為時間維度的標籤
isdate=(sdate-bdate).days
total_fields = [winter_sst]
path_out='/Users/WRF4.3/WPS/'
for d in range(5,9):
    sdate=datetime(2018,4,d)
    i=(d-5)+isdate
    winter_sst = pyw.V2d('SST', sst[i,:,:])

#   metgrid.exe要求每6小時1個檔案，海溫變化不大，此處並沒有另外再進行時間的內插
    for t in range(0, 23, 6):
        tt='{:02d}'.format(t)
        pyw.cinter('SST', sdate.strftime("%Y-%m-%d")+'_'+tt, winter_geo, total_fields, path_out)

```


### Reference
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)
---
