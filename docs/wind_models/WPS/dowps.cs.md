---
layout: default
title: "dowps.cs"
parent: "WPS"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-25 16:21:24
---

# dowps.cs 
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
- [WPS](https://github.com/wrf-model/WPS)顧名思義就是WRF的前處理系統(WRF Pre-processing System)，包括準備地理地形檔案的`geogrid.exe`、初始邊界檔案要讀取的觀測值準備`ungrid.exe`及網格化`metgrid.exe`等3支程式，而這三支程式共用同一個**名單**([namelist.wps demo](http://homepages.see.leeds.ac.uk/~lecag/wiser/namelist.wps.pdf))。
- WPS要處理的數據包括
  - 地理地形等[靜態數據](https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html)、
  - 再分析數據(如FNL)、
  - [海溫數據](https://sinotec2.github.io/jtd/docs/wind_models/SST/)等等。
  - 其結果可以成為OBSGRID、及(或)real的輸入檔案，為每一WRF作業必須的步驟。
  - 詳細編譯、安裝、namelist.wps設定、VTable的設定等等，可由[官網](https://github.com/wrf-model/WPS)找到相關資源。此處著眼在批次操作、作業瓶頸、以及結果檢核等注意事項。

## WPS之全月執行方案

### `dowps.cs`的執行
此處以批次檔[dowps.cs](https://github.com/sinotec2/jtd/blob/main/docs/wind_models/dowps.cs)做為處理全月之工具，則執行全年的迴圈為:
```bash
ROOT=/data/WRF4.1
for i in {0..11};do 
    ii=$(printf "%02d" $(( $i + 1 )) )
    mkdir -p $ROOT/WPS/$y$ii
    mkdir -p WPS$ii
    cd WPS$ii
    ln -s $ROOT/WPS/* .
    rm namelist.wps Vtable FILE* met_em* SST* PFILE* GRIBFILE*  
  sub dowps.cs $i
done
```
- 其中`sub`為將程序放在背景執行之小工具`bash=$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} &`
- `dowps.cs`的引數`m`為0~11的月份數。
- 原本在WPS目錄中的檔案(`namelist.wps`, `Vtable`, `FILE*`, `met_em*`, `SST*`, `PFILE*`, `GRIBFILE*`等)會造成衝突，必須刪除工作目錄中的連結。

### `dowps.cs`分段說明
- 路徑定義
  - PATH1：WPS路徑，結果將會在此目錄下產生，每月一個目錄，名稱為YYYYMM
  - PATH2：FNL及SST共同路徑
```bash
     1  3#usage: dowps.cs m (m=0~11)
     2  PATH1=$PWD
     3  PATH2=/airappz/WRF4.1.3/NCEP
```
- 模擬範圍、解析度等如有異動，要在`ungrib`前執行`geogrid`
```bash
     5  #cp -f $PATH1/namelist.wps.loop namelist.wps
     6  #./geogrid.exe
```
- 時間管理
  - 定義起訖時間（前月YP/MP/15日到下月初YN/MN/05），
    - 這些變數將代入名單模版中，成為本次執行的名單。
    - 使用`date`指令進行日期的計算，可以有效避免潤年、大小月等問題。(詳[Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+指令+用法))
  - 此範例運作年份為2019年
```bash
     8  yyyy=2019
     9  i=$1
    10    ym=$(date -ud "${yyyy}-01-01 + ${i} month" +%Y%m)
    11    YY=$(date -ud "${yyyy}-01-01 " +%y)
    12    MM=$(date -ud "${yyyy}-01-01 + ${i} month" +%m)
    13    YP=$(date -ud "${yyyy}-${MM}-01 - 1 month" +%y)
    14    YN=$(date -ud "${yyyy}-${MM}-01 + 1 month" +%y)
    15    MP=$(date -ud "${yyyy}-${MM}-01 - 1 month" +%m)
    16    MN=$(date -ud "${yyyy}-${MM}-01 + 1 month" +%m)
```
- 因全月作業會涉及到前一個月及後一個月的部分檔案，須先將FNL彙集到NCEP下各個月份(覆蓋)，以便整批一起使用`./link_grib.csh`連結到工作目錄，並完成更名備月。
```bash
    18    for pth in FNL SST;do
    19      cd ${PATH2}/$pth/
    20      mkdir -p $ym
    21      cd $ym
    22      ln -sf ../20$YP/*$YP${MP}1[5-9]* .
    23      ln -sf ../20$YP/*$YP$MP[23]* .
    24      ln -sf ../20$YY/*$YY$MM* .
    25      ln -sf ../20$YN/*$YN${MN}0[123456]* .
    26    done
```
- 因同步運作，必須避免不同月份間檔案發生衝突。
- 創建`WPS??(??=01~12)`目錄並移動到該目錄，以避免平行計算時覆蓋到其他作業的控制檔([Vtable](https://sinotec2.github.io/jtd/docs/wind_models/WPS/#檔案解讀的工作核心：建立對照關係)及namelist.wps)。
```bash
    27    ii=$(printf "%02d" $(( $i + 1 )) )
    28    echo "ii:"$ii
    29    mkdir -p $PATH1/WPS$ii
    30    cd $PATH1/WPS$ii
```
- 名單[模版](https://github.com/sinotec2/jtd/blob/main/docs/wind_models/namelist.wps.loop)的應用
  - 從主目錄複製一份名單的模版`namelist.wps.loop`到工作目錄
    - namelist.wps.loop的起迄時間為此處要置換的變數
    ```bash
      start_date = '20YP-MP-15_00:00:00','20YP-MP-15_00:00:00','20YP-MP-15_00:00:00','20YP-MP-15_00:00:00'
      end_date   = '20YN-MN-05_00:00:00','20YN-MN-05_00:00:00','20YN-MN-05_00:00:00','20YN-MN-05_00:00:00'
    ```
    - 起迄小時都設為0點的必要性
      - WRF模式會另要求計算模擬日數、小時數，起迄小時皆0則不必須計算小時數。
      - CMAQ模式的起迄小時都必須為0時UTC
  - 用`sed`指令置換其中的起訖時間、檔案型態
    - 在腳本中執行一變數的置換必須注意雙引號的使用：**不能**將變數放在雙引號之內。
    - `sed`指令的使用可以參考[說明](https://shengyu7697.github.io/linux-sed/)
    - 此階段執行FNL檔案解讀，其結果檔之前綴為`FILE`
```bash
    31    cp -f $PATH1/namelist.wps.loop namelist.wps
    32    for cmd in "s/YN/"$YN/g  "s/YP/"$YP/g  "s/MN/"$MN/g  "s/MP/"$MP/g  ;do sed -i $cmd namelist.wps;done
    33    sed -i "s/PREWD/FILE/g" namelist.wps
```
- 執行FNL檔案之解讀
  - 使用[link_grib.csh](https://github.com/wrf-model/WPS/blob/master/link_grib.csh)腳本將FNL檔案連結到工作目錄
  - 執行`ungrib.exe`讀取FNL檔案
```bash
    34    ./link_grib.csh $PATH2/FNL/$ym/fnl* .
    35    ln -sf ./ungrib/Variable_Tables/Vtable.GFS Vtable
    36    ./ungrib.exe
    37
```
- 同樣方式讀取SST檔案。
  - 如SST檔案非`grib`格式，則不需要執行此段，
  - 而需另行準備SST:YYYY-MM-DD-HH_00(WPS暫存檔)。參[海溫的讀取](https://sinotec2.github.io/jtd/docs/wind_models/SST/#nc檔案轉WPS暫存檔格式(intermediate format))。
```bash
    38    cp -f $PATH1/namelist.wps.loop namelist.wps
    39    for cmd in "s/YN/"$YN/g  "s/YP/"$YP/g  "s/MN/"$MN/g  "s/MP/"$MP/g  ;do sed -i $cmd namelist.wps;done
    40    sed -i "s/PREWD/SST/g" namelist.wps
    41    ./link_grib.csh  $PATH2/SST/$ym/rtg_sst* .
    42    ln -sf $PATH1/ungrib/Variable_Tables/Vtable.SST Vtable
    43    ./ungrib.exe
```
- 執行`metgrid`
```bash
    44
    45    ./metgrid.exe
    46
```
- 將`WPS??(??=01~12)`下的成果彙整到$PATH1/年月目錄下，以備`REAL`或`OBSGRID`使用。
```bash
    47    mkdir -p $PATH1/$ym/met
    48    mkdir -p $PATH1/$ym/SST_FILE
    49
    50    cp met_em*nc $PATH1/$ym/met
    51    cp  FILE:20* $PATH1/$ym/SST_FILE
    52    cp  SST:20* $PATH1/$ym/SST_FILE
```

## Reference
- University of Waterloo, [WRF Tutorial](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial),  27 June 2019, at 14:53.
- Andre R. Erler, WRF-Tools/Python/wrfrun/[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py), Commits on Nov 23, 2021.
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)

