---
layout: default
title: HUADON_3k 
parent: Abundant NoG Runs
grand_parent: CMAQ Model System
nav_order: 2
last_modified_date:   2022-03-18 16:39:52
---

# 華東地區解析度3Km之CMAQ模擬分析
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
-

## WRF之模擬
- WRF_chem的[ndown](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)尚未成功，且由於CMAQ亦有揚塵機制，此處並不使用WRF_chem，使用WRFv4.3進行模擬。

### 水平網格系統設計
- 採15Km、3Km等2層網格
- CWBWRF_15k維持不變。
- HUADON_3k網格範圍以涵括大陸地區主要污染源為主，臺灣仍維持在東西向之中央，位置略偏南，主要考量過去臺灣地區反軌跡來源，主要以偏北方向居多。

- namelist.wps設定如下

```bash
 parent_id         =   1,    1,
 parent_grid_ratio =   1,    5,
 i_parent_start    =   1,  252,
 j_parent_start    =   1,  144,
 e_we              =  671, 751,
 e_sn              =  395, 951,
 geog_data_res = 'default','default','default','default'
 dx = 15000,
 dy = 15000,
 map_proj = 'lambert',
 ref_lat   =23.08689
 ref_lon   =121.7359
 truelat1  =  10.0,
 truelat2  =  40.0,
 stand_lon = 121.7359,
 geog_data_path = '/nas1/WRF4.0/WPS_GEOG/WPS_GEOG',
```

### 垂直網格設計
-

### [ndown](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)及整體程序
- 執行2層的WPS、OBSGRID及REAL
- 執行CWBWRF_15k(單層)之WRF結束後，隨即進行[ndown](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)程序，以產生HUADON_3k逐時邊界場。
- 最後再執行HUADON_3k(單層)之WRF，將結果連結到mcip作業指定位置。

## MCIP之執行
### 網格系統
- 將d06設定如下(相較其他巢狀網格設定詳見[網格系統詳細定義](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/run_mcipMM_RR_DM/#網格系統詳細定義))：
  - 網格名稱GridName   = HUADON_3k
  - 內縮X0    =   1
  - 內縮Y0    =   1
  - 東西網格數NCOLS = 744
  - 南北網格數NROWS = 948
- 格數考量因素除在WRF格數範圍內，也考量其因數分解後，可以達成工作佔核心數之均勻分配、以及同時使用到最多核心數，詳下說明。

### 執行時間
- wrfout之時間
  - 一般為5天，WRF執行了8天
  - 腳本設定

```bash
set InMetFiles = ( \
                   $InMetDir/wrfout_${argv[3]}_0 \
                   $InMetDir/wrfout_${argv[3]}_1 \
                   $InMetDir/wrfout_${argv[3]}_2 \
...
                   $InMetDir/wrfout_${argv[3]}_7 )
```

### 檔案連結
- MCIP會抓d06檔名

```bash
wrfout_dHUADON_3k_0 -> /nas1/WRF4.0/WRF_chem/201804_run56N12/HUADON_3k/wrfout_d01_2018-03-30_00:00:00
wrfout_dHUADON_3k_1 -> /nas1/WRF4.0/WRF_chem/201804_run56N12/HUADON_3k/wrfout_d01_2018-03-31_00:00:00
...
wrfout_dHUADON_3k_7 -> /nas1/WRF4.0/WRF_chem/201804_run56N12/HUADON_3k/wrfout_d01_2018-04-06_00:00:00
wrfout_d06_0 -> wrfout_dHUADON_3k_0
wrfout_d06_1 -> wrfout_dHUADON_3k_1
...
wrfout_d06_7 -> wrfout_dHUADON_3k_7
```

## BCON之準備
- 因為模擬範圍大、解析度高，如果準備區內所有時間、3維的空品數據，檔案會非常大(>1T)，難以操作，且run_bcon.csh只運用到空品檔案周圍一圈的數據，非常沒有效率。
- 改以讀取EAC4數據、內插後直接寫進BCON檔案方式處理，[grb2bc](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2bc.py)與詳細處理過程詳見[EAC4檔案轉成4階邊界檔案](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF_rean/grb2bc/)。
  - CCTM可以接受邊界條件僅指定部分空氣品質項目，因此檔案容量可以減至最小。
  - 配合MCIP的起迄時間，共10天數據。
  - 檔名約定(`BCON_v53_1804_run5_regrid_20180331_CWBWRF_15k`)除了批次序之外，還需要有模擬起始日。因此如果進行restart模擬，需給予正確的日期

## ICON之準備
- CCTM會需要226項每一空氣品質之起始值。除了部分(NVARS=50)可以由EAC4數據給定，其餘則須**暫時**由隨機取得之數據填入。
- 模式先以此開始模擬，會經過一段發散期，逐漸穩定。經過1天的模擬之後，再將當天23時的空品細項做為啟始濃度。(更改CCTM_CGRID檔案的SDATE及TFLAG)，以避免發散(cold start-up方式)。

## 土地使用
- 由於REAS已經有估算農作畜牧的氨氣排放，因此關閉在線雙向氨氣排放(`CTM_ABFLUX`)機制。因此模擬不需要農作及土壤、土地使用等條件。直接由mcip結果提供相關數據。
- 由於mcip使用與WRF-chem所讀取的[geo_em](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WPS/geogrid/#wrfchem之geogridexe設定)檔案，因此會有相同的揚砂條件。

```bash
geo_em.d00.nc -> /nas1/WRF4.0/WRF_chem/WPS/geo_em.d01.nc_121.7359
```    

## 地面排放檔案
- 使用REAS3.2數據庫，轉換程式[reas2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD2.py)之說明，詳見[地面排放檔之轉換(CMAQ)](https://sinotec2.github.io/Focus-on-Air-Quality/REASnFMI/REAS/reas2cmaq/)。
- 雖然為逐日檔案、逐時數據，但此處沒有設定任何的時間變化，只有REAS資料庫本身逐月的差異。

## 高空排放檔案
- 即為REAS之POWER_PLANTS_POINT排放量，分布詳見[高空排放檔之轉換(CMAQ)](https://sinotec2.github.io/Focus-on-Air-Quality/REASnFMI/REAS/rd_REASptsrce/)。
- CCTM所讀取const.nc檔案內需設定正確的點源位置網格點，因此需改成CWBWRF_15k網格系統。

## CCTM之執行
### 腳本修改項目
- 開啟`CTM_WB_DUST`
- 關閉`CTM_ABFLUX`
- 模擬期間為啟始後9天結束

```bash
...
setenv CTM_WB_DUST Y
...
setenv CTM_ABFLUX N
...
  @ A = $RUN - 1; @ DD = $A * 4  ; @ ED = $A * 4 + 9    
```
### 計算核心之安排
- 因模擬範圍東西較寬，南北較窄，比例約為1.7:1，為使計算負荷及記憶體分配較為平均，此處設定接近2:1。

```bash
@ NPCOL  = 14 ; @ NPROW = 7
```

- 共使用14*7=98個核心。

## 後處理
### COMBINE
- 修改`GRID_NAME`
- 無需修改腳本日期，只需將原本屬於run6的日期予以更名即可直接使用[原腳本](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)。

```bash
...
if ( $DM == 'd01' ) then
#  setenv GRID_NAME  EAsia_81K
  setenv GRID_NAME  CWBWRF_15k
...
```  

### [pm10.ncl](https://github.com/sinotec2/cmaq_relatives/blob/master/post/pm10.ncl)
- [ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)將COMBINE中的TFLAG及PM10取出另存，再以`ncrcat`照日期連接成pm10.nc
- 進行[NCL等值圖繪製](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL/)
