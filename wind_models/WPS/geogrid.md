---
layout: default
title: 地形、土地使用之定義與處理
parent: "WPS"
grand_parent: "WRF"
nav_order: 2
date:               
last_modified_date: 2022-01-03 09:13:39
tags: CWBWRF
---

# geogrid

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
- 地形、土地使用之定義與處理(`geogrid.exe`)是WPS的第一步，是整個WRF系統在空間上的基礎，也是後續空間品質模擬的空間架構。因是空間設定，不必每次事件個案都重新處理。
- WRF範圍的考量視最終目的為空氣品質或氣象預報分析，略有不同，比較詳下表，後續將詳細討論。
- [WPS](https://github.com/wrf-model/WPS)顧名思義就是WRF的前處理系統(WRF Pre-processing System)，包括準備地理地形檔案的`geogrid.exe`、初始邊界檔案要讀取的觀測值準備`ungrid.exe`及網格化`metgrid.exe`等3支程式。
  - 這三支程式共用同一個**名單**([namelist.wps demo](http://homepages.see.leeds.ac.uk/~lecag/wiser/namelist.wps.pdf))。
  - 詳細編譯、安裝、namelist.wps設定、VTable的設定等等，可由[官網](https://github.com/wrf-model/WPS)找到相關資源。

|設定項目|氣象預報分析為目標|空氣品質分析為目標|此處設定|
|----|----|----|----|
|範圍|視天氣系統移動速度及預報天數而定。陸上及海上天氣現象同樣重要|會以同時納入排放源與受體、同時納入其間所有的大氣擴散傳輸現象為考量|以3天軌跡範圍、中國東半部排放量較大範圍為主|
|解析度|視地面強迫機制複雜度而異|視污染排放空間解析度而異|採81/27/9/3巢狀網格解析度|
|格點數|因無化學反應之計算，計算資源需求較低，可以允許較多的網格點|視反應機制的複雜度(計算資源需求較高)、子網格所需邊界條件解析度等而定|58~148|
|中心點|以關注標的為中心，東、西向對稱，以囊括到最多的天氣系統活動|不見得以關注標的之地理中心為中心，而是以污染傳播軌跡為中心|以台灣為中心|
|套疊關係|雙向與否視解析度而異|雙向與否與主要污染源有關|WRF採雙向、CMAQ採單向|


## 模擬範圍
- 整體而言氣象及空品模式模擬的範圍，都以天氣系統的移動速度及關切現象的天數而定，亦即污染軌跡在一定時間內所能延伸至之範圍。
- 以同樣是東亞範圍(d01)，圖1為中央氣象局WRF15公里解析度模擬範圍，其東西向範圍9,000公里、南北向6,000公里，約可掌握3~6天之天氣現象。
  - 模擬範圍可以完整包括[青康藏高原](https://zh.wikipedia.org/wiki/青康藏高原)、[蒙古高原](https://zh.wikipedia.org/wiki/蒙古高原)的主要部分，對地形效應有較完整的掌握。
  - 東側海面則以換日線為界，在資料整合上也能保持便利性。

| ![geo_emWRF_15Km.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_15Km.PNG) |
|:--:|
| <b>圖1 中央氣象局WRF15公里解析度模擬範圍之地形高程。東西向範圍9,000公里、南北向6,000公里</b>|
  
- 圖2為CMAQ 東亞模擬範圍，自台灣起算亦有至少3天反軌跡範圍，東西南北皆為4,860公里。
  - 包括了中國大陸東半壁，韓、日、中南半島與東南亞等主要境外污染來源。
  - 因大陸西部及海上無顯著污染源，縮減範圍也可減省計算資源。

| ![geo_emWRF_81Km.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_81Km.PNG) |
|:--:|
| <b>圖2 CMAQ 東亞範圍之地形高程，東西南北皆為4,860公里</b>|

### 各層網格詳細設定
- 中央氣象局WRF15及3公里解析度模擬範圍之namelist.wps內容設定如下

```bash
&geogrid
 parent_id         =   1,    1,
 parent_grid_ratio =   1,    5,
 i_parent_start    =   1,  213,
 j_parent_start    =   1,  133,
 e_we              = 671, 1166,
 e_sn              = 395,  681,
 geog_data_res = 'default','default','default','default'
 dx = 15000,
 dy = 15000,
 map_proj = 'lambert',
 ref_lat   =23.08689
 ref_lon   =121.7359
 truelat1  =  10.0,
 truelat2  =  40.0,
 stand_lon = 121.7359
 geog_data_path = '/nas1/WRF4.0/WPS_GEOG/WPS_GEOG',
/
```

## 子網格系統套疊關係
### 格數與母網格起點
- 格數
  - 新版[geogrid.exe]()對次網格的格數要求較嚴格，減1後必須是`parent_grid_ratio`的倍數。
  - 母網格起點(`i_parent_start`, `j_parent_start`)的決定與網格的格數間距有關
- 母網格起點
  1. 母網格及子網格總長差異/母網格之格距/2
  1. 需將臺灣本島置於中央

### 中央氣象局WRF3公里解析度模擬範圍
- 圖3為中央氣象局WRF3公里解析度模擬範圍，東西向範圍3,500公里、南北向2,050公里。
  - 其解析度足供鄉鎮區之天氣預報及分析
  - 由於沒有化學反應之計算，其網格數多達1166 X 681
  - 因d01的解析度也很高，足以反映局部重要特性，因此並不需要雙向套疊關係，d01即能呈現足夠的預報度。

| ![geo_emWRF_3Km.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_3Km.PNG) |
|:--:|
| <b>圖3 中央氣象局WRF3公里解析度模擬範圍之地形高程。東西向範圍3,500公里、南北向2,050公里</b>|
  
### WRF/CMAQ 各層子網格之模擬範圍
- 圖4~6為CMAQ 東南沿海(d02)、臺澎金馬(d03)與臺灣本島(d04)等各層子網格之模擬範圍。
  - 每個網格系統皆以臺灣為中心點，讓網格範圍有最大程度之重疊。
  - 因主要模擬標的為d04臺灣本島範圍，其餘範圍則保持雙向套疊關係
  
| ![geo_emWRF_27Km.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_27Km.PNG) |
|:--:|
| <b>圖4 CMAQ 東南沿海範圍之地形高程，東西南北皆為1,890公里</b>|
| ![geo_emWRF_9Km.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emWRF_9Km.PNG) |
|:--:|
| <b>圖5 CMAQ 臺澎金馬範圍之地形高程，東西向範圍552公里、南北向684公里</b>|
| ![geo_emCMAQ_3Km.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/geo_emCMAQ_3Km.PNG) |
|:--:|
| <b>圖6 CMAQ 臺灣本島範圍之地形高程，東西向範圍282公里、南北向444公里</b>|

### 各層網格詳細設定
- namelist.wps內容詳[地形網格設定](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WPS/namelist.wps/#地形網格設定) 

## WRF/chem之geogrid.exe設定
### 整體流程
- 作業流程詳WRF-chem/[geo_em檔案之準備](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WRF-chem/WPS-OBSGRID/#geo_em檔案之準備)

### 揚沙所需特定檔案
- 下載風蝕、沙及泥的比例參數計算所需[Thompson全球數據](https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_thompson28_chem.tar.gz)
- 到geog_data_path所指定的目錄(`/nas1/WRF4.0/WPS_GEOG/WPS_GEOG`)下進行解壓縮動作，得到下列3個目錄及以下檔案

```bash
uang@DEVP /nas1/WRF4.0/WPS_GEOG/WPS_GEOG
$ ls -lrth |grep "^d"
drwxr-xr-x.  2 kuang SESAir 4.0K Jan  5  2013 clayfrac_5m
drwxr-xr-x.  2 kuang SESAir 4.0K Jan  5  2013 sandfrac_5m
drwxr-xr-x.  2 kuang SESAir 4.0K May  8  2018 erod

$ ls -lrth clayfrac_5m sandfrac_5m erod
clayfrac_5m:
total 20M
-rwxr-xr-x. 1 kuang SESAir 288 Oct 16  2010 index
-rw-r--r--. 1 kuang SESAir 20M Oct 16  2010 00001-04500.00001-02250

sandfrac_5m:
total 20M
-rwxr-xr-x. 1 kuang SESAir 288 Oct 16  2010 index
-rw-r--r--. 1 kuang SESAir 20M Oct 16  2010 00001-04500.00001-02250

erod:
total 6.1M
-rwxr-xr-x. 1 kuang SESAir  282 May  8  2018 index
-rw-r--r--. 1 kuang SESAir 6.0M May  8  2018 00001-01440.00001-00720
```

### 揚沙參數之執行結果
- EROD風蝕係數之維度須先以[ncwa](https://linux.die.net/man/1/ncwa)予以[去除](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#維度刪除ncwa)方能以[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)檢視。
  - EROD的維度名稱為：` EROD(Time, dust_erosion_dimension, south_north, west_east) `，其中`dust_erosion_dimension`VERDI無法辨識

| ![erod.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/erod.PNG) |
|:--:|
| <b>圖7 d01範圍的風蝕係數(EROD)</b>|
| ![crayfrac.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/crayfrac.PNG) |
|:--:|
| <b>圖8 d01範圍的黏土比例係數(CRAYFRAC)</b>|
| ![SANDFRAC.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SANDFRAC.PNG) |
|:--:|
| <b>圖9 d01範圍的沙土比例係數(SANDFRAC)</b>|

## Reference

