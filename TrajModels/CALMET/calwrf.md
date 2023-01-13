---
layout: default
title: calwrf
nav_order: 1
parent: CALMET
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
tags: cpuff cmet wrf
---

# calwrf
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
- *CALMET*系統可以接受多項氣流動力模式的結果，其中包括早期的*mm5*、以及目前美國大氣科學界主要發展的*wrf*模式，此外也包括澳洲發展的[TAPM](https://www.epa.sa.gov.au/files/477263_modelling.pdf)模式、以及NOAA [RUC](https://ruc.noaa.gov/ruc/RUC/)模式。
- 由於美國政府未支援*CALPUFF*模式系統的持續發展，因此*CALWRF*目前仍停留在*wrf*第2~3版，並不接受第4版的wrfout結果。
- 經查，版次間雖有實質的差異，但在wrfout只有一個global attribute(nc.TITLE=" OUTPUT FROM WRF V4.2 MODEL")在控制，只需加入第4版的版次標記即可。

## 原始碼下載與編譯
### 下載
- 下載點：[官網](http://www.src.com/calpuff/download/mod7_codes.htm)
- 使用*wget*即可下載

```bash
wget http://www.src.com/calpuff/download/Mod7_Files/CALWRF_v2.0.3_L190426.zip
```
- 下載解開後可以發現壓縮包裏提供了window版本的執行檔與dll檔，可以直接執行
- 在code目錄下除了原始碼，也提供了*pdf95*及*gfortran*的編譯方式
### 編譯方式

```bash
$ cat compile.*
REM Compiling and linking with gfortran

@REM prevent conflicts if G95 is installed
set LIBRARY_PATH=

c:\MinGW\bin\gfortran -o calwrf.exe calwrf.f -L. -llibnetcdf-0
#!/bin/sh
# Compile calwrf on Linux using pgf95

if [ -f calwrf.exe ]; then rm calwrf.exe; fi

pgf95 -Bstatic calwrf_v2.0.1.f -lnetcdf -lm -o calwrf.exe

```
- 基本上就只是連結netcdf程式庫，並沒有其他特殊選項。
- 就netcdf版本，雖然官網未特別說明，但可以由[網友](https://blog.csdn.net/weixin_39621794/article/details/116683516)的介紹大體瞭解，因屬較早期的程式，還是netcdf 3版的時代。
    - 不過經測試，netcdf 4版依然可以運作。

## 程式修改編譯
### 按照錯誤訊息搜尋原始碼
- 錯誤訊息，關鍵詞為**wrfout**

```bash
#$ /cluster/CALPUFF6/CALWRF/binary_linux/calwrf.exe_old ../calwrf/calwrf01.inp
  Control inp file:../calwrf/calwrf01.inp
  2D.DAT flag input not exist, set to one
  Set 2D.DAT flag to 1:            1
  Default 2D.DAT filename:1901d4.m2d
  Open WRF netcdf file             1 :
 /nas1/WRF4.0/WRFv4.2/201901/wrfout/wrfout_d04_2018-12-31_00:00:00
  N_TIMES:           24

 Processing GLOBAL ATTRIBUTES:

 This is not a wrfout file
 No 3D.DAT will be created
FORTRAN STOP
# find the location of error message
#$grep -n wrfout /cluster/CALPUFF6/CALWRF/code/calwrf.f
1894:            !! diagnostics only available for wrfout data
1895:            print*,"This is not a wrfout file "
```
### 修改原始碼
- calwrf.f新增一組判斷是否為**WRF V4**即可
```fortran

      if(INDEX(value_chr,'OUTPUT FROM WRF V2') == 0)then
         if(INDEX(value_chr,'OUTPUT FROM WRF V3') == 0)then
         if(INDEX(value_chr,'OUTPUT FROM WRF V4') == 0)then !add by kuang
            !! diagnostics only available for wrfout data
            print*,"This is not a wrfout file "
            print*,"No 3D.DAT will be created"
            stop
         endif !add by kuang
         endif
      endif
```

### *ifort* setting
- @master

```bash
ifort -O -I/cluster/netcdf/include -L/cluster/netcdf/lib -lnetcdf -lnetcdff  -o calwrf.exe calwrf.f
```
- @DEVP

```bash
ifort -O -I/opt/netcdf/netcdf4_intel/include -L/opt/netcdf/netcdf4_intel/lib -lnetcdf -lnetcdff  -o calwrf.exe calwrf.f
```

## calwrf之執行
### inp settings
- 分月進行轉檔
    - 由前月的最後1天，到下個月的第1天
- 各行意義
    1. TITLE
    1. log檔(除螢幕輸出外，另有品質確認項目)
    1. 結果檔案名稱。只需指定3d檔，2d會自行命名。
    1. 起迄網格，因wrfout的解析度與範圍與*calpuff*非常接近，此處設定全部轉換
    1. 起迄UTC時間。模式必須在8時之前開始，此處定為0時。
    1. wrfout檔案個數。因wrfout是每日1個檔案儲存，因此只需要改潤年2月即可。
    1. 檔案路徑與名稱：必須按照實際存放位置修改。(使用模板與*sed*指令一次性修改即可)

```bash
#$ head calwrf01.inp
Create 3D.DAT file for WRF output
calwrf.lst          ! Log file name
2001d4.m3d ! Output file name
-1,-1,-1,-1,-1,-1   ! Beg/End I/J/K ("-" for all)
2019123100          ! Start datetime (UTC yyyymmddhh, "-" for all)
2020020100          ! End   datetime (UTC yyyymmddhh, "-" for all)
33                  ! Number of WRF output files
/nas1/WRF4.0/WRFv4.2/202001/wrfout/wrfout_d04_2019-12-31_00:00:00
/nas1/WRF4.0/WRFv4.2/202001/wrfout/wrfout_d04_2020-01-01_00:00:00
/nas1/WRF4.0/WRFv4.2/202001/wrfout/wrfout_d04_2020-01-02_00:00:00
```

### 同步執行
- 由於*calwrf*並沒有設計程式內的同步或多工，因此可以由程式外的批次檔同時運作12個月的批次作業
    - 因輸入檔、輸出檔的檔名皆已妥善安排，即使在同一目錄下運作也不會發生覆蓋的情形
    - 同一目錄運作的好處是未來*calmet*執行時可以容易設定輸入檔位置

```bash
for i in {01..12};do sub calwrf.exe calwrf$i.inp >&calwrf$i.log;done
```
- *sub*(submit)指令的說明，可詳見[unix系統小工具](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/unix_tools/#sub)

