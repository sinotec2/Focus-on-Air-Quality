---
layout: default
title: WACCM
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 3
date: 2022-11-21 10:04:08              
last_modified_date:  2022-11-22 22:37:55
---

# WACCM模式結果之下載、讀取及應用

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

- [官網][WACCM]敘述
  - 大氣社區氣候模型(Whole Atmosphere Community Climate Model, WACCM) 是一個NCAR社群綜合數值模型，涵蓋從地球表面到熱氣層的高度範圍。
  - WACCM 的開發是一項部門間合作，包括
    - HAO 高層大氣建模、
    - ACOM 中層大氣建模和 
    - CGD 對流層建模之某些部分，
    - 使用 NCAR 社區地球系統模型 (NCAR Community Earth System Model CESM) 作為通用數值模型框架。
  - [Marsh等人(2013)][Marsh(2013)]文中有對最新版本WACCM完整的描述。
  - WACCM-X 將 WACCM 擴展到上層熱層，並包括對電離層重要程序之模擬。
- 目前以[NASA/GMAO][GMAO] GEOS-5氣象預報進行實時全球空氣品質預報。
  - 空氣品質項目詳見[Species_CESM2-WACCM.pdf](https://www2.acom.ucar.edu/sites/default/files/documents/Species_CESM2-WACCM.pdf)，
  - 再分析結果包括
    - 再分析濃度圖([word view](https://worldview.acom.ucar.edu))，項目包括O3, PM2.5, CO(fires), NOx等。
    - [等濃度圖(chemical map)](https://www.acom.ucar.edu/waccm/map.shtml)，項目包括O3, PM2.5, Dust, CH2O, CO(fires), NOx, SO2等。
    - [WACCM PLOTTING](https://www.acom.ucar.edu/waccm/plot.shtml)，包括
      - 等值圖
      - 特定經度或緯度的垂直濃度分布
      - 特定地點的時序濃度變化
      - 包括所有模擬項目
  - 預報結果包括
    - [WACCM CHEMISTRY AND AEROSOL FORECASTS](https://www.acom.ucar.edu/waccm/forecast/)濃度圖播放器
      - 未來逐3小時數據檔案
      - 項目：地面10項、中層大氣11項、垂直13項、範圍4項
      - CO排放情境：QFED、FFIN(Fire INventory of NCAR, based on MODIS Rapid Response fire counts FIRMS)
  - 所有NCAR近實時預報產品整理在[Forecasts and Near Real Time (NRT) Products](https://www2.acom.ucar.edu/acresp/forecasts-and-near-real-time-nrt-products)
- NCAR [ACOM][ACOM]其他產品
  - 美國本土森林火災WRF-chem空品10天逐3小時預報[WRF-CHEM FORECAST MAPS](https://www.acom.ucar.edu/firex-aq/forecast.shtml)，運作中。
  - 2019/7~9美國本土森林火災[FLEXPART模式分析](https://www.acom.ucar.edu/firex-aq/flexpart/forecast.shtml)，[FLEXPART](https://www.flexpart.eu/)是個拉氏模式。運作2個月後後續似乎取消了作業化系統。
  - CAM-chem只有[資料同化結果](https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)，沒有預報。

## [WACCM][WACCM]預報數據之下載

### 策略

- 與載分析數據一樣，預報數據也是全球數據都在同一個檔案內，可以：
  1. 使用[ACOM][ACOM]提供的切割介面，指定所要的範圍、日期、以及接收的電郵，按照系統給定的網址下載檔案。然此法不能應用在自動化作業系統。
  2. 下載全球檔案，再行切割。此法會浪費頻寬及下載時間。一天的檔案(~8G)需要約20~30min，10天需4個小時(node03負責下載)。
  3. 倘若一天執行一次，尚能以不同機器同步運作第2方案。

### 切割範圍之決定

- WACCM或是MOZART模式輸出檔案都是經緯度系統，要裁切出足夠的範圍、同時又能有效降低檔案大小，會需要反覆試誤來達到最佳條件。
- 可以先在ipython內以bisect模組挑出足以涵蓋CCTM模式之水平範圍
- 執行[mozart2camx][mz2]
  - 如果範圍不足，程式會跳停。
  - 有超過換日線的部分，雖然[mozart2camx][mz2]會顯示出-179等類的低值，但基本上程式還是會解析其為東邊界線，直接調整lon指標的上限值即可。
- 結果：`$ncks -O -d lon,44,146 -d lat,87,150 $nc $YMD`

### 批次檔腳本

```bash
#kuang@master /nas1/WACCM
#$ cat dl_tdy.cs
wget=/usr/bin/wget
ncks=/usr/bin/ncks
root=https://www.acom.ucar.edu/waccm/DATA/
fnroot=f.e22.beta02.FWSD.f09_f09_mg17.cesm2_2_beta02.forecast.002.cam.h3.
fntail='-00000.nc'

cd /nas1/WACCM
for i in {-1..9};do
  YMD=$(date -d "today +${i}days" +%Y-%m-%d)
  nc=${fnroot}${YMD}${fntail}
  $wget -q ${root}$nc
  test ! -e $nc && continue
  $ncks -O -d lon,44,146 -d lat,87,150 $nc $YMD
  test -e $YMD && rm -f $nc
done
```

### 自動執行排程

```bash
#kuang@node03 ~
#$ crontab -l|grep dl
10 20 * * * /nas1/WACCM/dl_tdy.cs
```

## [WACCM][WACCM]預報數據之處理

### nc檔案格式之轉換

- 執行[NCF2IOAPI](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ncf2ioapi/)，即為nc2m3.cs片段(如下)
  - 因執行檔為Fortran，因此如在不同工作站執行，需重新編譯，以下為master、node01~03版本。

```bash
export EXECUTION_ID=CAM-chem2m3.job
export PROMPTFLAG=N
export IOAPI_ISPH=20
export EXE=/cluster/src/CAMx/mozart2camx_v3.2.1/ncf2ioapi_waccm/NCF2IOAPI
for i in {-3..7};do
  YMD=$(date -d "today +${i}days" +%Y-%m-%d)
  export INFILE=$YMD
  export OUTFILE3D=${YMD}.m3.nc
  $EXE
  test -e ${YMD}.m3.nc && rm -f $YMD
done
```

### 網格、污染物系統轉換的策略考量

- 包括垂直及經緯度系統的轉換
- 策略有三
  1. 以Ramboll公司持續更新發展的[MOZART2CAMx][mz2]程式轉接成CAMx模式初始檔(如[CAM-chem模式結果之應用](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM))，再以[camx2ioapi][camx2ioapi]轉成CMAQ初始檔。好處是同時產生CAMx以及CCTM的IC/BC檔案。
  2. 類似前述，新版官網[MOZART2CAMx][mz2]程式轉接不單可以指定轉成CAMx5/6格式、也提供直接轉成cmaq BC/IC檔案的選項。此選項不必再執行[camx2ioapi][camx2ioapi]程式。
  3. 執行[MOZARD/WACCM模式輸出轉成CMAQ初始條件_垂直對照](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/moz2cmaqH/)、及[水平內插與污染項目對照](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/moz2cmaqV/)。好處是可以平行作業、壞處是程式碼需要更新。
  - 似以官網提供程式為宜。速度較慢問題則以下載時間平行處理，避免延時太久。

### 氣象檔案(模版)之準備

#### CAMx 方案

- 此處仍以wrfcamx4.6版執行轉換
- 因僅為模版(只執行一次)，隨機選取任意日期進行轉換。
- 座標參數取自d01 mcip之GRIDDESC結果。

```bash
kuang@master /nas1/WACCM/d01_met
$ cat wrfcamx.job
#!/bin/csh

set PATH = "."
set OUT  = "."

if (! -d $OUT) mkdir $OUT

#yymmddhh(UTC+8)
set START = "22112408"
set FIN   = "22112507"

foreach DOM ( 1 )
if ( $DOM == 1 ) then
   set GridS = "218,126,24"
   set DxDy  = "45.,45."
   set OrigP = "-4905.0, -2835.0, 120.00, 25.00, 10., 40."
endif
set OUTNM = $OUT"/2211d"$DOM
set DOMYR = $DOM"_2022"

/nas1/WRF3.7/wrfcamx_v4.6/src/wrfcamx << ieof
Diagnostic Fields  |T
KV Method          |OB70
Minimum Kv         |0.1
Project            |LAMBERT
Subgrid convecton  |DIAG
Subgrid stratiform |T
Start/end date     |$START $FIN
WRF output freq    |60
Grid time zone     |-8
CAMx grid size     |$GridS
CAMx Grid spacing  |$DxDy
CAMx orig & params |$OrigP
Layer mapping      |1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
CAMx LU file       |$OUTNM.lu
CAMx 3D file       |$OUTNM.3d
CAMx 2D file       |$OUTNM.2d
CAMx Kv file       |$OUTNM.kv
CAMx Cld/rain file |$OUTNM.cr
Make pre-6.3 snow? |T
v6.3+ In snow age  |
v6.3+ Init snow age|
v6.3+ Out snow age |
WRF filename       |$PATH/wrfout_d0$DOMYR-11-24_00:00:00
ieof

end
```

#### mcip 方案

- [MOZART2CAMx][mz2]的cmaq選項需要將mcip結果檔案設定成環境變數，而不是std input
- 需要2格檔案，分別是METCRO3D與METCRO2D
- 同樣地，程式並不是真的讀取變數，而是讀取與網格系統有關的氣象項目。

### CAMx方案之執行腳本

#### mz2camx.job

- 注意事項
  - 執行檔有2個工作站版本，要注意選取。
  - cshell的變數置換方式與bash略有不同(bash：`YMD=${YMD1//-}`、csh：`YMD = $YMD1:as/-//`)
  - 全球檔案如未經切割，會發生問題
    - mz2camx不允許含有南北極，需先去除
    - 處理速度會很慢(全球1個小時的數據約需2個小時處理、經ncks裁減後可降為20分鐘)

```bash
kuang@master /nas1/WACCM
$ cat mz2camx.job
#!/bin/csh -f
setenv PROMPTFLAG N
setenv IOAPI_ISPH 20
setenv LD_LIBRARY_PATH /opt/netcdf4/lib:/opt/hdf5/lib:/cluster/intel/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin
#set EXE = /nas1/camxruns/src/mozart2camx_v3.2.1/src/mozart2camx_CB6r4_CF__WACCM #devp version
set EXE = /cluster/src/CAMx/mozart2camx_v3.2.1/src/mozart2camx_CB6r4_CF__WACCM

set YMD1 = `echo $1|cut -c1-10`
set t    = `echo $1|cut -c11-12`
set YMD = $YMD1:as/-//
set MET = /nas1/WACCM/d01_met/2211d1

# DEFINE OUTPUT FILE NAMES
setenv EXECUTION_ID mz2camx.job
echo $1
set NINFILE = 1
setenv OUTFILEIC ${YMD}${t}".ic"
setenv OUTFILEBC ${YMD}${t}".bc"
setenv INFILE ../../$YMD1
setenv INFILE1 ../../$YMD1
echo $OUTFILEIC

$EXE << IEOF
CAMx5,CAMx6,CMAQ   |CAMx 6
ProcessDateYYYYMMDD|$YMD
Output BC file?    |.true.
Output IC file?    |.true.
If IC, starting hr |$t
Output TC file?    |.false.
Max num MZRT files |$NINFILE
CAMx 3D met file   |$MET.3d
CAMx 2D met file   |$MET.2d
IEOF
```

#### cmaq.job

```bash
kuang@master /nas1/WACCM
$ cat cmaq.job
#!/bin/csh -f
setenv PROMPTFLAG N
setenv IOAPI_ISPH 20
setenv LD_LIBRARY_PATH /opt/netcdf4/lib:/opt/hdf5/lib:/cluster/intel/compilers_and_libraries_2016.1.150/linux/compiler/lib/intel64_lin
set EXE = /nas1/camxruns/src/mozart2camx_v3.2.1/src/mozart2camx_CB6r4_CF__WACCM #devp version
set EXE = /cluster/src/CAMx/mozart2camx_v3.2.1/src/mozart2camx_CB6r4_CF__WACCM

set YMD1 = `echo $1|cut -c1-10`
set t    = `echo $1|cut -c11-12`
set YMD = $YMD1:as/-//
set MET = /nas2/cmaqruns/2022fcst/grid45/mcip/METCRO
setenv INFILEMET3D ${MET}3D.nc
setenv INFILEMET2D ${MET}2D.nc
# DEFINE OUTPUT FILE NAMES
setenv EXECUTION_ID mz2camx.job
setenv OUTFILEBC ${YMD}${t}".bc"
set NINFILE = 1

setenv OUTFILEIC ${YMD}${t}".ic"
setenv INFILE today_mz.m3.nc
setenv INFILE1 today_mz.m3.nc
echo $OUTFILEIC $t $YMD
set BCFLAG = .false.
if ( $t == "00" ) then
  set BCFLAG = .true.
endif

$EXE << IEOF
CAMx5,CAMx6,CMAQ   |CMAQ
ProcessDateYYYYMMDD|$YMD
Output BC file?    |$BCFLAG
Output IC file?    |.true.
If IC, starting hr |$t
Output TC file?    |.false.
Max num MZRT files |$NINFILE
IEOF
```

#### camx2ioapi

- 這支程式較為舊版，2016迄今尚未更新。然經過測試，轉檔結果進入CCTM執行並無問題。
- job檔較單純，併入前述mz2camx.job之後執行
- 注意事項
  1. Sigma Levels可以由WRF之namelist.input檔案(NLAYS+1)、抑或由一個標準ICON檔案的全域屬性(NLAYS)中讀取。
  2. 不同工作站執行檔與程式庫路徑各有不同，要注意設定。
  3. 產生之ICON結果需真正進行CCTM以測試其內容與格式完全正確。

```bash
setenv IOAPI_OUT ICON
rm -f $IOAPI_OUT

$EXE << EOF
Input CAMx filename|OUTFILEIC
Data Type          |AVRG
Sigma Levels       |0.995,0.990,0.980,0.960,0.930,0.910,0.890,0.850,0.816,0.783,0.751,0.693,0.637,0.537,0.449,0.372,0.304,0.245,0.194,0.131,0.082,0.046,0.019,0.000,
EOF
```

#### BCON之產生

- 策略上
- 此處無法使用run_bcon.csh(bcon.exe)將ICON之外圍切割出邊界濃度，因為BCON的實質位置還較ICON大一圈。
- [fil_rean.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/BCON/fil_rean.py)有類似的功能，可以從此點開始（待發展）。

#### CAMx方案之自動執行腳本(dl_tdy.cs)


```bash
...
  for it in {0..3};do
    t=${ts[$it]}
    s=${st[$it]}
    mkdir -p ${YMD0}/$t
    cd ${YMD0}/$t
    if [ $it -eq 00 ];then
      ln -sf ../../$YMD today_mz.m3.nc
    else
      $ncks -O -d TSTEP,$it ../../$YMD today_mz.m3.nc
      $ncatted -a STIME,global,o,i,$s today_mz.m3.nc
    fi
    ~/bin/sub csh ../../mz2camx.job $YMD$t >& out
    cd ../../
  done
...
```

### 直接轉成cmaq方案之執行腳本

#### mz2cmaq.job

- 此處同樣顧及Fortran的執行效率，需要按照bc/ic，區分成各日期、各個小時分別進行轉檔。
- 策略上
  - BCON：每日產生一個BCON（4個timeframe）即可，不需要拆成4筆BCON檔案->工作目錄設定在日期/00。每批次最後一小時需要延長，可以待所有檔案都轉檔完成、經ncrcat連成11天的大檔案後再延長。
  - ICON：
    - 每批次產生一個ICON已經足夠執行CCTM。
    - 逐6小時轉成ICON檔案，可以用本地的earth套件將WACCM數據予以展現。工作目錄設定在日期/06、12、18等3個目錄。這項工作應該與$fcst/grid45/cctm.ic相同。（待發展）
- 注意事項
  1. BCON一定是從0時開始，不會隨著初始時間而變動。（因此在00目錄下執行）
  2. ICON可以接受非0的STIME，因此可以將逐日檔案按小時予以切割（修改STIME值）、平行計算，以爭取時效。

```bash
cat mz2cmaq.job
```

#### cmaq方案之dl_tdy.cs

- 與前述CAMx方案差異
  - 4個timeframe差異處理
    - 00：執行全日之轉檔（BCON and ICON）
    - 06～18：只執行該小時內容之轉檔(ICON only)

```bash
...
  for it in {0..3};do
    t=${ts[$it]}
    s=${st[$it]}
    mkdir -p ${YMD0}/$t
    cd ${YMD0}/$t
    if [ $it -eq 00 ];then
      ln -sf ../../$YMD today_mz.m3.nc
    else
      $ncks -O -d TSTEP,$it ../../$YMD today_mz.m3.nc
      $ncatted -a STIME,global,o,i,$s today_mz.m3.nc
    fi
    ~/bin/sub csh ../../mz2cmaq.job $YMD$t >& out
    cd ../../
  done
...
```

[WACCM]: <https://www2.acom.ucar.edu/gcm/waccm> "The Whole Atmosphere Community Climate Model (WACCM) is a comprehensive numerical model, spanning the range of altitude from the Earth's surface to the thermosphere"
[Marsh(2013)]: <https://opensky.ucar.edu/islandora/object/articles%3A12836> "Marsh, D., Mills, M., Kinnison, D. E., & Lamarque, J. -F. (2013). Climate change from 1850 to 2005 simulated in CESM1(WACCM). Journal Of Climate, 26, 7372-7391. doi:10.1175/JCLI-D-12-00558.1"
[GMAO]: <https://gmao.gsfc.nasa.gov/> "National Aeronautics and Space Administration GMAO - Global Modeling and Assimilation Office"
[ACOM]: <https://www2.acom.ucar.edu/> "ATMOSPHERIC CHEMISTRY OBSERVATIONS & MODELING"
[mz2]: <ttps://camx-wp.azurewebsites.net/getmedia/mozart2camx.6apr22.tgz> "mozart2camx"
[camx2ioapi]: <https://camx-wp.azurewebsites.net/getmedia/camx2ioapi.8apr16_1.tgz> "camx2ioapi"