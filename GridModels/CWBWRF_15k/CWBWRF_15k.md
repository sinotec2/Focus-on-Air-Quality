---
layout: default
title: CWBWRF_15k System
parent: CMAQ Model System
nav_order: 9
permalink: /GridModels/CWBWRF_15k
last_modified_date:   2022-02-09 09:03:45
---

# 東亞地區解析度15Km之CMAQ模擬分析
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
- 東亞地區高解析度模擬的挑戰非但是資料面，也是電腦硬體的困難，包括計算核心與記憶體的分配、硬碟的容量等等。
- 雖然模擬各個階段的細節都已經在FAQ中各單元交代，此處還是綜整因應東亞地區之考慮、以及特殊修改之要點。
- 有關網格系統的考量
  - 範圍類似[大氣污染情報網站](https://pm25.jp/)或[REAS](/Focus-on-Air-Quality/REASnFMI/REAS/rd_REASptsrce/#結果檢視)，具有可比較性。
  - 解析度(15km)較其他地區模擬為高。  
  - 因以台灣地區為服務標的，位於模擬範圍的正中心，可以接受各方向天氣系統的作用效果，沒有方向上的偏頗。  
  - 囊括中國及中亞砂塵暴排放源位置，有效提高模擬的正確性。
  - 網格系統定義詳見中央氣象局opendata數值預報模式-區域預報模式(WRF-15公里)之[說明](https://opendata.cwb.gov.tw/opendatadoc/MIC/A0061.pdf)。

## WRF之模擬
- 詳細說明如[WRF-chem](/Focus-on-Air-Quality/wind_models/WRF-chem/)
- 為提高模擬的正確性，揚砂排放與4階同化都有開啟。
- 並未使用WRF-chem輸出的揚砂排放量，而是啟動CMAQ本身的線上揚砂機制(`CTM_WB_DUST`)。

## MCIP之執行
### 網格系統
- 將d00設定如下(相較其他巢狀網格設定詳見[網格系統詳細定義](/Focus-on-Air-Quality/GridModels/MCIP/run_mcipMM_RR_DM/#網格系統詳細定義))：
  - 網格名稱GridName   = CWBWRF_15k
  - 內縮X0    =   3
  - 內縮Y0    =   3
  - 東西網格數NCOLS = 665
  - 南北網格數NROWS = 389

### 執行時間
- wrfout之時間
  - 一般為5天，WRF-chem執行了10天
  - 腳本設定

```bash
set InMetFiles = ( \
                   $InMetDir/wrfout_${argv[3]}_1 \
                   $InMetDir/wrfout_${argv[3]}_2 \
...
                   $InMetDir/wrfout_${argv[3]}_10 )
```

### 檔案連結
- MCIP會抓d00檔名

```bash
 wrfout_dCWBWRF_15k_1 -> /nas1/WRF4.0/WRF_chem/201804_run56/wrfout_d01_2018-03-31_00:00:00
 wrfout_dCWBWRF_15k_2 -> /nas1/WRF4.0/WRF_chem/201804_run56/wrfout_d01_2018-04-01_00:00:00
...
 wrfout_dCWBWRF_15k_10 -> /nas1/WRF4.0/WRF_chem/201804_run56/wrfout_d01_2018-04-09_00:00:00
 wrfout_d00_1 -> wrfout_dCWBWRF_15k_1
 wrfout_d00_2 -> wrfout_dCWBWRF_15k_2
...
 wrfout_d00_10 -> wrfout_dCWBWRF_15k_10
```

## BCON之準備
- 因為模擬範圍大、解析度高，如果準備區內所有時間、3維的空品數據，檔案會非常大(>1T)，難以操作，且run_bcon.csh只運用到空品檔案周圍一圈的數據，非常沒有效率。
- 改以讀取EAC4數據、內插後直接寫進BCON檔案方式處理，[grb2bc](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2bc.py)與詳細處理過程詳見[EAC4檔案轉成4階邊界檔案](/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2bc/)。
  - CCTM可以接受邊界條件僅指定部分空氣品質項目，因此檔案容量可以減至最小。
  - 配合MCIP的起迄時間，共10天數據。
  - 檔名約定(`BCON_v53_1804_run5_regrid_20180331_CWBWRF_15k`)除了批次序之外，還需要有模擬起始日。因此如果進行restart模擬，需給予正確的日期

## ICON之準備
- CCTM會需要226項每一空氣品質之起始值。除了部分(NVARS=50)可以由EAC4數據給定，其餘則須**暫時**由隨機取得之數據填入。
- 模式先以此開始模擬，會經過一段發散期，逐漸穩定。經過1天的模擬之後，再將當天23時的空品細項做為啟始濃度。(更改CCTM_CGRID檔案的SDATE及TFLAG)，以避免發散(cold start-up方式)。

## 土地使用
- 由於REAS已經有估算農作畜牧的氨氣排放，因此關閉在線雙向氨氣排放(`CTM_ABFLUX`)機制。因此模擬不需要農作及土壤、土地使用等條件。直接由mcip結果提供相關數據。
- 由於mcip使用與WRF-chem所讀取的[geo_em](/Focus-on-Air-Quality/wind_models/WPS/geogrid/#wrfchem之geogridexe設定)檔案，因此會有相同的揚砂條件。

```bash
geo_em.d00.nc -> /nas1/WRF4.0/WRF_chem/WPS/geo_em.d01.nc_121.7359
```    

## 地面排放檔案
- 使用REAS3.2數據庫，轉換程式[reas2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD2.py)之說明，詳見[地面排放檔之轉換(CMAQ)](/Focus-on-Air-Quality/REASnFMI/REAS/reas2cmaq/)。
- 雖然為逐日檔案、逐時數據，但此處沒有設定任何的時間變化，只有REAS資料庫本身逐月的差異。

## 高空排放檔案
- 即為REAS之POWER_PLANTS_POINT排放量，分布詳見[高空排放檔之轉換(CMAQ)](/Focus-on-Air-Quality/REASnFMI/REAS/rd_REASptsrce/)。
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
- 無需修改腳本日期，只需將原本屬於run6的日期予以更名即可直接使用[原腳本](/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)。

```bash
...
if ( $DM == 'd01' ) then
#  setenv GRID_NAME  EAsia_81K
  setenv GRID_NAME  CWBWRF_15k
...
```  

### [pm10.ncl](https://github.com/sinotec2/cmaq_relatives/blob/master/post/pm10.ncl)
- [ncks](/Focus-on-Air-Quality/utilities/netCDF/ncks/)將COMBINE中的TFLAG及PM10取出另存，再以`ncrcat`照日期連接成pm10.nc
- 進行[NCL等值圖繪製](/Focus-on-Air-Quality/utilities/Graphics/NCL/)
