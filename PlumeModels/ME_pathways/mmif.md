---
layout: default
title: MMIF
parent: ME Pathways
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-03-28 11:02:41
tags: plume_model mmif
---

# MMIF

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

### 緣起與目標

由於aermet需要綜合彙整大量觀測數據、地區土地利用、蒸散、粗糙度等參數，而這些數據在中尺度大氣動力模式、如WRF或不再更新的MM5中，已經詳細考慮納入了，其空間解析度為1\~9公里、時間解析度為1\~6小時。因此以其模擬結果取代aermet來產生氣象數據檔案，將會有最高的地區代表性與資料的完整性。

[USEPA](https://www.epa.gov/scram/air-quality-dispersion-modeling-related-model-support-programs#mmif)多年來持續發展並維護mmif程式（Mesoscale Model Interface Program），其目的就是從大氣模式結果中，讀取並轉換AERMOD所需的氣象檔案。最新版本為06-30-2021，使用該轉接程式有官方提供持續性的技術支援。

詳細使用方式可以參考[MMIF使用手冊](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/related/mmif/MMIFv3.4.2_Users_Manual.pdf)。

mmif將會生成aermod執行所需要的氣象檔案，包括地面氣象要素與參數.sfc檔，以及垂直探空數據檔.pfl檔案。

### 遠端執行系統

- 這個遠端執行系統有3個版本，目前營運的是第2與第3版本(詳[MMIF_CaaS](mmif_caas.md))。
- 2016～2020 3Km網格點預處理結果檔案[連結](https://umap.openstreetmap.fr/zh-tw/map/mmif-resultstwn_3x3_grids_588696)。

## 版本差異

- MMIF目前最新版本為2021年版。
- 2019年至2021年間新增之改變

|date|change|
|-|:-|
|2019-09-05|  Added "UAWINDOW -6 6 " keyword for AERMOD mode. At high latitudes, the morning sounding falls outside the default "UAWINDOW -1 1" so no convective mixing heights were being calculated by AERMET. Only affects "aer_mixht AERMET" modes.|
|2019-11-08|  Added reading CLDFRA, if it exists in MM5 files.|
|2019-11-08|  Bug fix: some older versions of WRF don't have CLDFRA, so test and skip if it's not found. Error if CLOUDCOVER WRF has been chosen.|
|2020-03-02|  Bug fix: lat's for points in KML output formatted incorrectly.|
|2020-04-17|  Change Bowen ratio calculation to use day-time hours only. It was using all hours, which conflicts with the AERMET User Guide.|
|2020-07-09|  Use lowest layer instead of U10, V10 if Z(1) < 13, to match the methodology when running in AERMET mode.|
|2020-10-17|  Add ALPHA options to use TSKY in AERMET mode, and BULKRN option.|
|2020-11-30|  Changed format statement for ASCII MEDOC files to avoid rounding roughness length values to 0.0000 (impossible value).|
|2020-12-15|  When using MMIF’s re-diagnosis of the mixing height, use temporal smoothing – the same as AERMET does.|
|2021-06-24|  Add ability to use WRF's hybrid vertical coordinate.|

## 準備及編譯

雖然USEAP SCRAM網頁提供有PC上可執行的程式，但隨著電腦世界的發展，可能無法在每一個使用者平台上可以運作，因此有必要下載其程式原始碼，在本地平台上進行編譯。

- Source Code ：[ZIP](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/related/mmif/MMIFv3.4.2_2021-06-30.zip)

- 以下為centOS及macOS作業系統所面對到的問題與解決方案(2019及2021年版)。

|作業系統|Compilations|問題|
|-|-|-|
|centOS|ifort|(取消-static設定)|
|macOS|gfortran(9~11)|crt0.o、-fbounds-check、 mismatch between  arguments|

- 問題1：missing of crt0.o, macOS沒有這個C的obj。
  - 解決：參考ifort的問題與解法，不要static link即可
  - 參考
    - [developer.apple](https://developer.apple.com/library/archive/qa/qa1118/_index.html)
    - [software.intel](https://software.intel.com/en-us/articles/library-not-found-crt0)
    - [Crt0 wiki](https://en.wikipedia.org/wiki/Crt0 )
- 問題2：新版gfortran對-fbounds-check 較舊版嚴格，程式對iPt、OutTyp等變數並不是從0開始，會嚴格檢查，因此拒絕執行。
  - 解決1.：修改程式碼(parse_control.f90)
  - 解決2.：取消-fbounds-check選項
- 問題3：呼叫副程式的引數型態不一致(2021版本僅有此項問題)
  - 解決：增加-fallow-argument-mismatch選項
  - 參考[gentoo -fallow-argument-mismatch for gfortran v10](https://github.com/gentoo/gentoo/pull/16093)

## mmif.inp之設定

mmif程式的輸入檔，除了WRF或MM5檔案本身之外，其餘設定總集在[mmif.inp](./mmif.inp)文字檔之內，使用者需要確認及修正的項目說明如下。

### 時間及空間範圍

- start/stop 起迄時間、當地時間
- TimeZone 時區，台灣為+8
- grid模式網格範圍，-5表示內設值(去掉邊界5格)

|變數名稱|設定值|說明|
|-|:-:|-|
|start|      2020 06 18 08 | start time in LST, hour-ending format|
|stop|       2020 07 20 08 | end   time in LST, hour-ending format|
|grid |      IJ -5,-5 -5,-5   | default|

### 高度、穩定度、及風速等設定

- 各層高度：按照EPA建議
- 穩定度等級分類方式：GOLDER（內設）
- PBL重算：否（內設）
- 最小風速、混合層高度、莫寧尺度：0.5m/s、1m、1m

|變數名稱|設定值|說明|
|-|:-:|-|
|layers |top 20 40 80 160 320 640 1200 2000 3000 4000   | default|
|stability | GOLDER   | default|
|PBL_recalc| FALSE  | default|
|aer_min_speed| 0.5  | default|
aer_min_mixht| 1.0  | default|
aer_min_obuk|  1.0  | default|

### 最低4層結果之輸出

- 4類輸出檔案(shell script、onsite、upair、aersfc)

|變數名稱|設定值|說明|
|-|:-:|-|
|POINT  LL |25.1208  121.2983|代表位置點的經緯度座標：緯度、經度|
|AER_layers|        1        4  | write 2m, 10m, and the 4 lowest WRF layers。|
|Output aermet    useful|  run_aermet_linko.csh | use .csh on Linux|
|Output aermet    onsite|  link.dat||
|Output aermet    upperair| link.fsl||
|Output aermet    aersfc|  link.aersfc.dat||

### 逐6小時高空氣象數據檔

|變數名稱|設定值|說明|
|-|:-:|-|
|FSL_INTERVAL|      6        | output every 6 hours, not 12 (the default)高空檔時間間隔：6小時|
|POINT  latlon|    25.1208  121.2983      8|高空氣象代表位置點座標：緯度、經度、時差|
|Output aermet   | FSL 'Upper air at link.FSL'|高空氣象檔名、內容標記|

### aermod直接可讀檔案

- 3類輸出檔案(shell script、sfc、upair)

|變數名稱|設定值|說明|
|-|:-:|-|
|POINT  latlon|     25.156327 121.740297     8 ||
|AER_layers|        0        0            | write only 2m and 10m data|
|Output aermod     useful|   xiehe.info.txt||
|Output aermod    sfc|      xiehe.sfc||
|Output aermod     PFL|      xiehe.pfl||

### wrf或mm5檔案及目錄

- 檔案必須包括所有起迄時間

|變數名稱|設定值|說明|
|-|:-:|-|
|INPUT| /Users/Data/cwb/WRF_3Km/2020/20200101/wrfout_d04||

- WRF檔名之準備

```bash
for i in $(ls /Users/WRF4.1/WRFv3/201909/run1[01]/wrfout_d04*);do
  echo INPUT $i
done >fnames.wrf
cat fnames.wrf >> mmif.inp
```

## Reference

- [MMIF使用手冊](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/related/mmif/MMIFv3.4.2_Users_Manual.pdf)，2021-06-30