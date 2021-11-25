---
layout: default
title: "WPS:WRF的前處理系統"
parent: "氣象模式"
nav_order: 1
date:               
last_modified_date:   2021-11-25 09:41:21
---

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

# WPS:WRF的前處理系統 

## 背景
- [WPS](https://github.com/wrf-model/WPS)顧名思義就是WRF的前處理系統(WRF Pre-processing System)，包括準備地理地形檔案的geogrid.exe、初始邊界檔案要讀取的觀測值準備ungrid.exe及網格化metgrid.exe等3支程式，而這三支程式共用同一個**名單**([namelist.wps demo](http://homepages.see.leeds.ac.uk/~lecag/wiser/namelist.wps.pdf))。
- WPS要處理的數據包括
  - 地理地形等[靜態數據](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)、
  - 再分析數據(如FNL)、
  - [海溫數據](https://sinotec2.github.io/jtd/docs/wind_models/SST/)等等。
  - 其結果可以成為OBSGRID、及(或)real的輸入檔案，為每一WRF作業必須的步驟。
  - 詳細編譯、安裝、namelist.wps設定、VTable的設定等等，可由[官網](https://github.com/wrf-model/WPS)找到相關資源。此處著眼在批次操作、作業瓶頸、以及結果檢核等注意事項。

## 地形網格設定
地形網格的namelist需要設定項目範例及說明如下。
- 東西與南北向的網格數(e_we、e_sn)：會影響執行需要的時間、檔案的大小、平行運作可以使用的資源(網格數是否能被核心數整除)、以及後續空氣品質模擬的範圍。
- 網格解析度(parent_grid_ratio, dx, dy)：親子網格系統網格間距的比例必須大於2。最小的網格間距與模式控制方程式的基本假設有關，在時間間距之內大氣能夠在網格內完成均勻混合。
- 投影設定：與模擬範圍大小有關。在後續空品模擬過程，直角座標系統與排放的網格系統整合較為容易。將模式中心點設定在臺灣島的中心，對來自四面八方的天氣系統，都會有較好的模擬。
- 地理數據的路徑(geog_data_path)：將[靜態數據](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)下載、解壓縮後，將其路徑填在此處。<注意：WPS_GEOG會佔用29G之磁碟機空間>
```bash
&geogrid
parent_id = 1, 1, 2, 3,
parent_grid_ratio = 1, 3, 3, 3,
i_parent_start = 1, 19, 25, 16,
j_parent_start = 1, 19, 22, 16,
e_we = 60, 70, 58, 94,
e_sn = 60, 70, 76,148,
geog_data_res = 'default','default','default','default'
dx = 81000,
dy = 81000,
map_proj = 'lambert',
ref_lat =23.61,
ref_lon =120.99 ,
truelat1 = 10.0,
truelat2 = 40.0,
stand_lon =120.99 ,
geog_data_path = '/Users/WRF4.1/WPS/WPS_GEOG',
/
```
- 因後續空氣品質模擬也會使用到[土地使用分類方式]()，還會再讀取geo_em.d??.nc的內容，以保持一致。
- 雖然WPS_GEOG已經儘可能將數據更新到最新，但與現況(模擬個案)還可能有些差異，如需修改，可以使用python程式，或者直接用NCO工具進行局限修改，可以參考[滑鐵盧大學](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial)的建議。如以下範例：
  - Change LANDUSEF from 1 to 0 at soil category 20: `ncap2 -O -s 'LANDUSEF(:,20,y1:y2,x1:x2)=0;' geo_em.d01.nc geo_em.d01.nc`
  - change the land type to grassland in a rectangular region x1 to x2 and y1 to y2, type: `ncap2 -O -s 'LU_INDEX(:,y1:y2,x1:x2)=7;' geo_em.d01.nc geo_em.d01.nc`

## 再分析數據之轉檔(ungrib.exe)

### 何為「再分析」? 何為grib? 又為何要ungrib?
- 為整合全球地面、高空、衛星等觀測成為系統性、網格化的數據，各大氣象中心作業單位持續投入所謂「再分析」工作，將觀測與模式整合成具系統性檔案。
- 充分性：
  - 再分析數據的時、空解析度不會太高、但作為真實個案模式模擬的初始與邊界條件，已經非常足夠。
  - 加上各單位再分析工作已經作業化、常態化，因此對ungrib.exe的支援非常充分、穩定。
- 必要性：
  - 因大多數再分析數據是以`grib`格式存檔，所以下載後要進行轉檔，以準備下一階段的切割與網格化([metgrid.exe]())。
  - 是否一定需要進行`ungrib.exe`？答案是否定也是肯定。
    - 使用python當然也能進行grib檔案的讀取及metgrid的準備，程式也更為靈活、因應日新月異的再分析數據也有更短的更新週期(如[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py))，如有特殊需求可以參考應用。
    - 因近年來很多單位也提供`nc`檔案，那就不需要`ungrib.exe`，反而是要進行`unNC`的工作，因為在所提供的`nc`檔案中，其變數名稱、單位、網格定義等等，也各不相同，要將其轉寫成WPS格式進入WRF系統，也會是一番工程(如[nc檔案轉WPS暫存檔格式](https://sinotec2.github.io/jtd/docs/wind_models/SST/#nc%E6%AA%94%E6%A1%88%E8%BD%89wpsungribexe%E6%9A%AB%E5%AD%98%E6%AA%94%E6%A0%BC%E5%BC%8Fintermediate-format))。

### 檔案解讀的工作核心：建立對照關係
- 由於各作業單位再分析檔案內的變數名稱、單位等等都不相同，解讀時就需要逐一進行對照、單位與名稱轉換、這需要一個完整的對照表，稱之為**Vtable**(**V**ariable dictionary **table**)。
- WPS累積至今已經建有40種檔案、變數對照關係表，可以按照再分析數據的來源選用。包括：
```bash
for i in $(ls ./ungrib/Variable_Tables/Vtable.*|cut -d '.' -f3);do echo ${i},;done
AFWAICE, AGRMETSNOW, AGRMETSOIL, AGRMETSOIL2, AGRWRF, ARW, ARWp, AVN0P5WRF, AWIP, CFSR, CFSR_mean, ECMWF, ECMWF_sigma, ERA-interim, ERA-interim, GFDL, GFS, GFSENS, GODAS, GSM, JMAGSM, NAM, NARR, NCEP2, NNRP, NOGAPS, NOGAPS_needs_GFS_soil, NavySST, RAP.hybrid.ncep, RAP.pressure.ncep, RAP.sigma.gsd, RUCb, RUCp, SREF, SST, TCRP, UKMO_ENDGame, UKMO_LANDSEA, UKMO_no_heights, raphrrr
```
- 使用時，只須將``./ungrib/Variable_Tables/`目錄下該特定之Vtable.???連結到工作目錄，覆蓋既有的`Vtable`即可。
- Vtable的選用範例
  - FNL之分析：`ln -sf ./ungrib/Variable_Tables/Vtable.GFS Vtable`
  - SST grib檔之解析：`ln -sf ./ungrib/Variable_Tables/Vtable.SST Vtable`
- Vtable的內容範例
```bash
cat ./ungrib/Variable_Tables/Vtable.SST
GRIB1| Level| From |  To  | metgrid  | metgrid | metgrid                                 |GRIB2|GRIB2|GRIB2|GRIB2|
Param| Type |Level1|Level2| Name     | Units   | Description                             |Discp|Catgy|Param|Level|
-----+------+------+------+----------+---------+-----------------------------------------+-----------------------+
  11 |   1  |   0  |      | SST      | K       | Sea Surface Temperature                 |  0 |  0 |  0  |   1 |
-----+------+------+------+----------+---------+-----------------------------------------+-----------------------+
```

### ungrib.exe名單的設定
namelist.wps中有關ungrib.exe的設定不多，主要定義都在Vtable的對照關係中詳列，
```bash
&ungrib
 out_format = 'WPS',
 prefix = 'SST',
/
```
- out_format：'WPS'格式即為**暫存檔格式**([intermediate format](https://www2.mmm.ucar.edu/wrf/users/docs/user_guide_v4/v4.3/users_guide_chap3.html#_Writing_Meteorological_Data))，因ungrib.exe輸出結果只給metgrid.exe使用，不必另行偵錯，如欲檢查整體內容，可以直接察看metgrid.exe的結果，該結果是`nc`檔案，有許多顯示軟體可以分析。
- prefix：產出檔案的檔頭，選項包括`FILE`、`SST`、`PRES`等等，視要ungrib的數據內容而定，此協定也是為下一階段metgrid.exe讀取。

## metgrid.exe再分析數據之網格化
這個階段的目標是形成`met_em.dNN.YYYY-MM-DD_HH:00:00.nc`(NN=01~巢狀網格層數)，其空間定義乃按照之前產生geo_em.d??.nc的內容，氣象數據則整併ungrib.exe的WPS暫存結果。`met_em`檔案為下一階段包括real(或obsgrid)的輸入檔案。

### metgrid.exe名單的設定
namelist.wps中有關metgrid.exe的設定包括2項：
```bash
&metgrid
 fg_name = 'FILE','SST'
 io_form_metgrid = 2,
/
```
- fg_name：ungrib.exe結果檔名的前綴。如果找不到檔案，metgrid.exe會提出警告，不會停止。
- io_form_metgrid：2為內設值，表示將產生`NETCDF`檔。其他選項還包括(僅限):`1:BINARY`、`3:GRIB1`。

### met_em檔案範例與GFS版本問題
檔頭如範例所示。
```bash
kuang@114-32-164-198 /Users/WRF4.3/WPS
$ ncdump -h $nc|M
netcdf met_em.d01.2018-04-05_00\:00\:00 {
dimensions:
        Time = UNLIMITED ; // (1 currently)
        DateStrLen = 19 ;
        west_east = 59 ;
        south_north = 59 ;
        num_metgrid_levels = 32 ;
        num_st_layers = 4 ;
        num_sm_layers = 4 ;
        south_north_stag = 60 ;
        west_east_stag = 60 ;
        z-dimension0012 = 12 ;
        z-dimension0016 = 16 ;
        z-dimension0021 = 21 ;
```
- `num_metgrid_levels`：這個數字是GFS再分析檔的層數，會在後續`real`的名單中用到。
  - GFS曾經在2019年6月12日12時(UTC)有進行改版([NCEP/GFS Version Update 12 June, 2019 at 1200 UTC](https://forum.mmm.ucar.edu/phpBB3/viewtopic.php?f=94&t=5451))，層數由32增加到34，因此不同時間案例取用不同時間的GFS再分析數據，將會有不一樣的層數。(see [metgrid.exe error GFS FV3 transition](https://forum.wrfforum.com/viewtopic.php?f=6&t=11314))。
  - 如果正好做到2019年6月12日的個案，解決方式：
    - 將個案分成舊版與新版2個小個案執行wrf(不建議、涉個案初始化問題)
    - 使用ncks工具減少(或)增加新、舊版本期間`met_em`檔案的層數，以符合整體個案層數的一致性。(建議方式)

### met_em檔案的檢視
因為`met_em`是nc檔案，可以用VERDI或其他軟體開啟、檢視，如[下圖](https://github.com/sinotec2/jtd/blob/main/assets/images/a.png)2020年6月太平洋高壓範例。

![image](/assets/images/a.png)

## Reference
- University of Waterloo, [WRF Tutorial](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial),  27 June 2019, at 14:53.
- Andre R. Erler, WRF-Tools/Python/wrfrun/[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py), Commits on Nov 23, 2021.
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)

