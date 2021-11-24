---
layout: default
title: 海溫的讀取
nav_order: 9
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
海面溫度雖然變化緩慢，但牽動全球的大氣環流，因此在氣象模擬過程中是一項非常重要的地面強制邊界。
---
### 資料來源與下載
- nc檔案：NOAA再分析0.25度日均值，檔案有2個出處：
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
    使用wget或curl都可以直接下載。下載後可以fortran或python程式解讀、切割、轉檔。

- grib檔案：[ECMWF再分析數據(ERA5)](https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation)，有提供31公里逐時之高解析度檔(HRES)、以及10個叢集低解析度檔案(EDA)。最早回溯到1950年1月。每月更新到前3個月的數據。下載方式為[網頁](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=form)選取及(或)CDS API python模組，如以下範例

```python
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-land',
    {
        'format': 'grib',
        'variable': 'skin_temperature',
        'year': '2008',
        'month': '01',
        'day': '21',
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
    },
    'download.grib')
```

### nc檔案轉WPS/ungrib.exe暫存檔格式(intermediate format)
<p>WPS歷來解讀grib檔之後，在進入metgrid.exe之前有個暫存檔案，其格式為Fortran binary檔案，稱之為**WPS暫存檔格式**([intermediate format](https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.3/users_guide_chap3.html#_Writing_Meteorological_Data))，FNL檔案經ungrib.exe轉檔成為FILE:YYYY-MM-DD-HH_00, 之暫存檔，海溫則轉成SST:YYYY-MM-DD-HH_00。因此如果另有海溫數據來源，在WPS過程中即可跳過SST之ungrib.exe，直接將數據寫成暫存檔格式，以進行下一步驟metgrid.exe的整併與轉檔。</p>
<p>轉換方式有fortran及python兩種：</p>
- fortran：
- python：使用netCDF4與[pywinter](https://pywinter.readthedocs.io/en/latest)之模組進行讀寫，

 


### Reference
- [NCO](https://github.com/nco/nco)
- [ncks](https://linux.die.net/man/1/ncks)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)
---
