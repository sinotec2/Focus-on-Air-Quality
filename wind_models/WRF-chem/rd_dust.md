---
layout: default
title: WRF-chem的後處理
parent: WRF-chem
grand_parent: "WRF"
nav_order: 4
date: 2021-12-28 10:20:34
last_modified_date:   2021-12-28 10:20:38
tags: wrf-chem wrf
---

# WRF-chem的後處理
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
- **WRF-chem**的模擬結果基本上還是個`wrfout`，此次沙塵暴模擬結果與**WRF4.3**的`wrfout`檔案比較，只有下列29項變數的差異(如下表)。其中
  - PM10及PM2_5_DRY目前因沙塵個案沒有執行化學反應，此項為0，如有需要必須自行計算(加總即可)。
  - DUST_1~5為粒徑0.5~8 &mu;m之分量，此處以其[線性總合](https://ruc.noaa.gov/wrf/wrf-chem/wrf_tutorial_2017/WRF_CHEM_dust.pdf)做為PM<sub>10</sub>之比較
  ```python
  PM2.5=bin1+0.3125*bin2
  PM10=bin1+bin2+bin3+0.87*bin4
  ``` 
  - 單位&mu;g/Kg與&mu;g/M<sup>3</sup>之間差了空氣密度之倍數，此處參考[wiki](https://en.wikipedia.org/wiki/Density_of_air)取常壓室溫1.1839 Kg/M<sup>3</sup>


| Variable Name|Description|Units|
|----|----|----|
| CLDFRA2 | CLOUD FRACTION | - |
| CN2O5 | n2o5 velocity | m/s |
| DMS_0 | dms oceanic concentrations | nM/L |
| DRYDEPVEL | dust dry deposition velocity | m/s |
| DRY_DEP_LEN | dry deposition velocity | cm/s |
| DUST_1 | dust size bin 1: 0.5um effective radius | ug/kg-dryair |
| DUST_2 | dust size bin 2: 1.4um effective radius | ug/kg-dryair |
| DUST_3 | dust size bin 3: 2.4um effective radius | ug/kg-dryair |
| DUST_4 | dust size bin 4: 4.5um effective radius | ug/kg-dryair |
| DUST_5 | dust size bin 5: 8.0um effective radius | ug/kg-dryair |
| EBIO_API | Actual biog emiss | mol km^-2 hr^-1 |
| EBIO_ISO | Actual biog emiss | mol km^-2 hr^-1 |
| EVAPPROD | RAIN EVAPORATION RATE | s-1 |
| GAMN2O5 | n2o5 uptake by aerosol | numerical value |
| KN2O5 | n2o5 het reaction rate | s-1 |
| LAI_VEGMASK | MODIS LAI vegetation mask for this date; 0=no dust produced (vegetation) | none |
| MAX_MSTFX | Max map factor in domain |  |
| MAX_MSTFY | Max map factor in domain |  |
| PHOTR204 | CLNO2 Photolysis Rate | min{-1} |
| PM10 | pm10 dry mass | ug m^-3 |
| PM2_5_DRY | pm2.5 aerosol dry mass | ug m^-3 |
| PV | Potential Vorticity | pvu |
| RAINPROD | TOTAL RAIN PRODUCTION RATE | s-1 |
| ROUGH_COR | roughness elements correction |  |
| SAC | 2nd moment Aitken mode | m2 m-3 |
| SMOIS_COR | soil moisture correction |  |
| SNU | 2nd moment Aitken mode | m2 m-3 |
| UST_T | Threshold Friction Velocity | m s-1 |
| YCLNO2 | clno2 yield from n2o5 het | numerical value |


## 程式說明

### 程式I/O檔案
- dust*YYMM*.mc
  - 從逐日個別`wrfout`檔案中切出第1層、取出Times,DUST_1\~5等變數之結果檔。過程詳程式#說明，使用[ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)及[ncrcat]()。
  - 由於模擬結果檔案很大，無法直接進入[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)，必須加以裁切。
- dust.nc
  - 整個模擬期間所有日期的合併檔，為一模版，其值會被覆蓋。
  - `DUST_1`將為程式加總之結果。

### 程式說明
- 每個逐日檔案進行迴圈，將結果回存到整合所有日的模版`dust.nc`
  - 每個檔案的時間都是24小時，但最後檔只有1小時，因此還是以`nt`為長度，才不會出錯。
  - 加總後可以用[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)開啟、繪圖。
    - 使用imagineMagicks `convert`一次修剪所有的png檔案、再予以組合成gif
    - 或使用`-bordercolor white -trim` + `-bordercolor white -border 10%x10% `會比較整齊
    - 轉換成gif時，convert會自動回復成原來的背景，`-background none`可取消。

```bash
for i in {0..54};do convert WRF_chem-$i.png -crop 950x550 a.png;mv a.png WRF_chemC-$i.png;done
for i in {0..9};do mv WRF_chemC-$i.png WRF_chemC-0$i.png;done
convert -dispose 2 -coalesce +repage -background none  WRF_chem-*.png -size 895x565 WRF_chem.gif
```

- 北臺灣測點時間序列之讀取
  - `IX,IY`為[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)圖面上讀取結果，因此換到python上時須**減1**。
  - `wrfout`的時間標籤為`Times`，為12個`byte`的序列，因此須先轉成(`decode`)字元，串成(`join`)字串，再讀成`datetime`，轉成所要的格式。詳情見[WRF的時間標籤](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/DateTime/WRF_Times/)之說明
  - `csv`檔案可以用Excel等軟體繪製[時間序列圖](../../assets/images/WRFchemVSwanli.PNG)

```python
strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
tflag=[i.strftime('%Y%m%d%H') for i in Times]
```

### rd_dust.py code listing

```python
import netCDF4
import numpy as np
import datetime

#for i in 03-3{0..1} 04-0{1..9};do nc=wrfout_d01_2018-${i}_00:00:00;ncks -v Times,DUST_1,DUST_2,DUST_2,DUST_3,DUST_4,DUST_5 -d bottom_top,0 $nc dust$i.nc;done
#ncrcat -O dust0*.nc a
#ncks -O -v Times,DUST_1 a dust.nc

fnames=subprocess.check_output('ls dust??-??.nc',shell=True).decode('utf8').strip('\n').split('\n')
nc = netCDF4.Dataset('dust.nc', 'r+')
binf={i:1 for i in range(1,4)};binf.update({4:0.87,5:0})
it=0
for fname in fnames:
  nc_in = netCDF4.Dataset(fname, 'r')
  nt,nz,ny,nx=nc_in['DUST_1'].shape
  dust=np.zeros(shape=(nt,nz,ny,nx))
  for i in range(1,6):
    dust+=nc_in['DUST_'+str(i)][:]*binf[i]
  nc['DUST_1'][it:it+nt,:,:,:]=dust[:,:,:,:]
  it+=nt

IX,IY=335-1,212-1
nt,nz,ny,nx=nc['DUST_1'].shape
strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
tflag=[i.strftime('%Y%m%d%H') for i in Times]
zs=['WRFchem']
for z in zs:
  exec(z+'=nc["DUST_1"][:,0,IY,IX]*1.1839') #dens of air https://en.wikipedia.org/wiki/Density_of_air
DD={}
for z in zs+['tflag']:
  exec('DD.update({"'+z+'":'+z+'})')
df=DataFrame(DD)
df.set_index('tflag').to_csv('ntw.csv')

nc.close()
```

## 結果檢核
- 2018/4/5~4/7東亞沙塵暴傳播之模擬結果
  - [Youtube](https://youtu.be/kvF1gLMlE0Q)
  - [GIF](http://sinotec24.com/soong/20180405WRFchem.gif)
![](../../assets/images/2018040616.PNG)
- 比較EC再分析、WRF-chem模擬以及萬里實測PM<sub>10</sub>數據(時間軸為UTC)
![](../../assets/images/WRFchemVSwanli.PNG)
- 其他再分析與觀測
  - [nullschool](https://earth.nullschool.net/#2018/04/05/0000Z/particulates/surface/level/overlay=pm10/orthographic=-238.92,24.73,2072/loc=117.900,32.438)
  - 環保署官方[說明](https://drive.google.com/file/d/1cTQhDlfEl8w8ikw2SwdmPKJngayCZKy5/view)(https://airtw.epa.gov.tw/CHT/Forecast/Sand.aspx)

- 2019/10/24~11/3東亞沙塵暴傳播之模擬結果  
  - [GIF](http://sinotec24.com/soong/20191029D1PM10.gif)
  - 環保署官方[說明](https://drive.google.com/file/d/1Vy7Ca4Pz_P5zc3e6-206UDjvxYEneFBx/view)
  
## Reference
- Li Zhang, **Dust Options in WRF-Chem**, [WRF-Chem Tutorial](https://ruc.noaa.gov/wrf/wrf-chem/wrf_tutorial_2017/WRF_CHEM_dust.pdf), Feb. 6, 2017