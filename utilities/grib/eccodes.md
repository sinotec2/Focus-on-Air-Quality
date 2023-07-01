---
layout: default
title: eccodes程式編譯與應用
parent: grib Relatives
grand_parent: Utilities
nav_order: 3
date: 2023-06-30 11:26:00
last_modified_date: 2023-06-30 11:26:11
tags: grib ecmwf eccodes
---

# eccodes程式編譯與應用
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

- eccodes顧名思義是ecmwf釋出的程式碼，其中有不少好用的小工具，此處應用來做grib的解讀與轉檔，有關eccodes的說明，可以參考[官網][eccodes_desc]。
- `grib_dump`指令在NRT數據從高斯網格[內插到直角座標系統](../../AQana/GAQuality/ECMWF_NRT/2.CAMS_NRT.md#內插到直角座標系統)時曾經有應用案例。

## 下載及編譯

- eccodes不時更新，所以編譯時所用的cmake也必須是最新版。
- cmake的執行檔可以直接從[官網](https://cmake.org/files/v3.14/)下載使用。

### 下載原始碼

- eccodes官網之[download](https://confluence.ecmwf.int/display/ECC/Releases)有程式碼的tar包，命名方式為`eccodes-x.y.z-Source`，`x.y.z`為版次數字，大約每季會更新一個版次。
- 解壓縮後，進入目錄，從README.md可以找到編譯的方式。

### 編譯

- 建立一個新的編譯目錄，以避免干擾到原始碼

```bash
mkdir build
cd build
```

- 確認cmake的版次，必須是3.11以上
- 執行cmake，目標(`PREFIX`)需要自行設定(放在既有的gribby環境下，這樣就不會找不到了)。

```bash
cmake  ../../eccodes-2.30.2-Source -DCMAKE_INSTALL_PREFIX=/opt/anaconda3/envs/gribby
```

- 執行make及install。

```bash
make
ctest
make install
```

- 與python3結合在一起
  - 不知道是dev2工作站本地的pip(22.3.1)比較新還是甚麼原因，官網建議的選項無法運作(`--install-option="--prefix==..." `)，
  - 必須如下設定

```bash
 pip3 install --prefix=/opt/anaconda3/envs/gribby eccodes
```

## eccodes的應用

### grib_dump

- 這支程式有點類似ncdump的功能。但畢竟grib檔案是個循序讀取的檔案，還是以record(grib檔的專有名詞是MESSAGE)的概念在設計檔案架構。
- grib檔案沒有檔頭，但是每個MESSAGE會有說明(SECTION、`grib_dump -O FILENAME`可以顯示SECTION內容)
- `grib_dump -D FILENAME` (偵錯模式)，會顯示維度的設定內容
  
### grib_to_netcdf

- 這支程式是專為ecmwf grib檔案寫的，可以接受等間距經緯度、以及高斯網格系統。比起`ncl_convert2nc`更能適應ecmwf grib檔案的特性。
- 指令`grib_to_netcdf  -u time -o TargetNCFileName SourceGribFileName`
  - grib檔案沒有unlimiting dimension的概念，所以如果轉成nc檔案，一定要在某個階段予以設定，否則不能修改(延長)檔案。
  - 此處指定`time`維度為unlimiting。
- affected scripts:[下載分析之腳本get_all.cs](../../ForecastSystem/5daysVersion/1.CMAQ_fcst.md#執行下載分析之腳本)

[eccodes_desc]: https://confluence.ecmwf.int/display/ECC/What+is+ecCodes?src=contextnavpagetreemode "ecCodes is a package developed by ECMWF which provides an application programming interface and a set of tools for decoding and encoding messages in the grib, bufr and gts formats"
