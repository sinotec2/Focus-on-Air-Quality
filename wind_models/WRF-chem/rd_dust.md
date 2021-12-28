---
layout: default
title: WRF-chem的後處理
parent: WRF-chem
grand_parent: "WRF"
nav_order: 3
date: 2021-12-28 10:20:34
last_modified_date:   2021-12-28 10:20:38
---

# WRF-chem的後處理

## 背景
- 沙塵暴(Wind-Blown Dust))**WRF-chem(WBD)**的模擬結果基本上還是個`wrfout`，與**WRF4.3**的`wrfout`檔案比較，只有下列29項變數的差異。其中
  - PM10及PM2_5_DRY目前因沒有執行化學反應，此項為0
  - DUST_1~5為粒徑0.5~8 &mu;m之分量，此處以其總合做為PM<sub>10</sub>之比較 
  - 單位&mu;g/Kg與&mu;g/M<sup>3</sup>之間差了空氣密度之倍數，此處取常壓室溫1.1839 Kg/M<sup>3</sup>


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
- `dust*YYMM*.mc`：
  - 為個別`wrfout`取出第1層、Times,DUST_1\~5變數之結果。詳程式#說明，使用[ncks]()及[ncrcat]()。
  - 由於模擬結果檔案很大，無法直接進入[VERDI]，必須加以裁切。
- `dust.nc`：整個模擬期間之合併檔模版。令`DUST_1`為加總之結果。

### 程式說明
- 每個逐日檔案進行迴圈，將結果回存到整合所有日的模版`dust.nc`
  - 每個檔案的時間都是24小時，但最後檔只有1小時，因此還是以`nt`為長度，才不會出錯。
  - 加總後可以用[VERDI]()開啟、繪圖。
- 北臺灣測點時間序列之讀取
  - `IX,IY`為[VERDI]()圖面上讀取結果，因此換到python上時須減1。
  - `wrfout`的時間標籤為`Times`，為12個`byte`的序列，因此須先轉成字元(`decode`)，串成字串(`join`)，再讀成`datetime`，轉成所要的格式。
```python
strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
tflag=[i.strftime('%Y%m%d%H') for i in Times]
```

### rd_dust.py listing
```python
import netCDF4
import numpy as np
import datetime

#for i in 03-3{0..1} 04-0{1..9};do nc=wrfout_d01_2018-${i}_00:00:00;ncks -v Times,DUST_1,DUST_2,DUST_2,DUST_3,DUST_4,DUST_5 -d bottom_top,0 $nc dust$i.nc;done
#ncrcat -O dust0*.nc a
#ncks -O -v Times,DUST_1 a dust.nc

fnames='dust03-30.nc dust03-31.nc dust04-01.nc dust04-02.nc dust04-03.nc dust04-04.nc dust04-05.nc dust04-06.nc dust04-07.nc dust04-08.nc dust04-09.nc'.split()
nc = netCDF4.Dataset('dust.nc', 'r+')
it=0
for fname in fnames:
  nc_in = netCDF4.Dataset(fname, 'r')
  nt,nz,ny,nx=nc_in['DUST_1'].shape
  dust=np.zeros(shape=(nt,nz,ny,nx))
  for i in range(1,6):
    dust+=nc_in['DUST_'+str(i)][:]
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
- 比較EC再分析、這次WRF-chem模擬以及萬里實測PM10數據
![]()

## Reference
