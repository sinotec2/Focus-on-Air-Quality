---
layout: default
title: "CAM-chem"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 2
date: 2021-12-12 16:29:18              
last_modified_date: 2022-06-13 10:40:45
---

# CAM-chem模式結果之讀取及應用
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

## 前言
- 社群大氣化學模式 (Community Atmosphere Model with Chemistry， [CAM-chem][CAM-chem]) 是 NCAR 社群地球系統模型 (CESM) 的一部分，用於模擬全球對流層和平流層大氣成分。 
- CAM-chem 使用 MOZART 化學機制，對流層和平流層化學具有多種複雜性選擇。 為美國大氣研究學界(UCAR)建議的全球模式結果，解析度1.25度X0.94度。 
  - CAM-chem 的初始版本可參考Lamarque 等人(2012)。 
  - 用於 CCMI 和 HTAP 的 CAM-chem版本可參考Tilmes 等人(2016)。
  - Tilmes 等人描述了 CESM1.2 中的 CAM-chem。 (2015)。

[CAM-chem]: <https://wiki.ucar.edu/display/camchem/Home> "The Community Atmosphere Model with Chemistry (CAM-chem) is a component of the NCAR Community Earth System Model (CESM) and is used for simulations of global tropospheric and stratospheric atmospheric composition."

## 下載
### 逐日、全球模擬結果檔案之下載
- CAM-chem有段時間提供全年、全球範圍的模擬結果檔案下載。
  - 網址為：`https://www.acom.ucar.edu/cam-chem/DATA/${Y}/fmerra.2.1003.FCSD.f09.qfedcmip.56L.001.cam.h1.${YMD}-${tail}.nc` 
  - (當時)可使用批次檔下載全球數據，再以[ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)進行切割。

```bash
kuang@master /nas1/CAM-chem
$ cat ./2010/gg2010.cs
BEG=2009-12-31
ENDD=2011-01-01
tot_days=367
for ((j=0;j<=$tot_days;j+=1));do
  if [ $HOSTNAME == 'node03' ] ||  [ $HOSTNAME == 'master' ];then
    YMD=$(date -ud "${BEG}+${j}days" +%Y-%m-%d)
    Y=$(date -ud "${BEG}+${j}days" +%Y)
  elif [ $HOSTNAME == 'Mac-mini.local' ] ||  [ $HOSTNAME == '114-32-164-198.HINET-IP.hinet.net' ];then
    YMD=$(date -v+${j}d -j -f "%Y-%m-%d" "${BEG}" +%Y-%m-%d)
    Y=$(date -v+${j}d -j -f "%Y%j"  "${BEG}" +%Y)
  fi
  echo 'YMD= '$YMD
  path=https://www.acom.ucar.edu/cam-chem/DATA/${Y}/
  tail='00000'
  test $Y -eq '2017' && tail='21600'
  file=fmerra.2.1003.FCSD.f09.qfedcmip.56L.001.cam.h1.${YMD}-${tail}.nc
  wget -q ${path}${file}
  if [ -e $file ];then
    ncks -O -d lon,64,128 -d lat,94,145 ${file} tmp
    mv tmp ${file}
  fi
  if [ $YMD == $ENDD ];then break;fi
done
```
### 下載政策的改變
- 2021年後因管理政策改變(可能受限於頻寬負荷)，鼓勵使用者直接上機檢視模擬結果，甚至鼓勵在本地工作站自行模擬。
  - 因此再沒有提供全年、全球檔案的直接下載。
  - 切割與部分日期的[下載界面](https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)，則仍舊繼續服務。  

- 界面與前述[MOZART](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/MOZART/)一樣，[下載網址](https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)略有不同，提供2001/1 ~ 半年前的模擬（再分析）結果。

![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cam-chem_download.png)

### 下載檔案管理
- 時間
  - 與Mozart一樣，CAM模式模擬結果為每6小時一筆，一日的起始時間為06Z，最後一筆為00Z。
  - 下載時以10天為原則，每檔案約在3.1~3.4G範圍，尚能在傳輸的負荷之內。
  - 使用[mozart模擬結果之下載](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/MOZART/#mozart模擬結果之下載)方案中之**5個檔案**方案，讓檔案的起迄完全不重疊，以利ncrcat銜接。
- 空間
  - `lev = 56 ; lat = 52 ; lon = 65 ;`
  - `ncks -d lat,-2.0,47.0 -d lon,80.0,160.0`(按經緯度值)
  - `ncks -O -d lon,64,128 -d lat,94,145 ${file} tmp`(按經緯度index、頭尾都算)
- 其餘等候ucar網站寄來email與信件內網址之處理、更名等過程，詳見[mozart模擬結果之下載](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/MOZART/#mozart模擬結果之下載)。

## 檔案處理
### 下載檔案轉成ioapi之nc檔(nc2m3)
- 使用Ramboll公司提供的[ncf2ioapi](https://camx-wp.azurewebsites.net/getmedia/mozart2camx.6apr22.tgz)，詳[全球模式結果檔案的轉換(nc2m3)](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/ncf2ioapi/)，轉換結果為ioapi之nc檔(`$jj.m3.nc`、不必保留)。 
- 主要進行nc檔案的格式轉換，座標、網格、化學物質種類等內容並無差異。

```bash
#kuang@master /nas1/CAM-chem
#$ cat nc2m3.cs
export EXECUTION_ID=CAM-chem2m3.job
export PROMPTFLAG=N
export IOAPI_ISPH=20
EXE=/cluster/src/CAMx/mozart2camx_v3.2.1/ncf2ioapi_waccm/NCF2IOAPI
for i in $(ls $1/*/????.nc) ;do
  jj=${i/.nc/}
  export INFILE=$i
  export OUTFILE3D=$jj.m3.nc
  echo $i
  $EXE|tail -n5
done
```
### ioapi檔案之轉檔(mz2camx)
- 主要轉換項目
  1. 座標與網格系統成為直角座標系統
  2. 化學物質之對照
  3. 單位轉換
- 逐月執行之批次檔如下。處理結果為[uamiv格式](https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式)檔案

```bash
#kuang@master /nas1/CAM-chem
#$ cat do_job.csh
set YR = $argv[1]
foreach mm (`seq 1 12`)
    set mon=`printf '%02d' $mm`
    cd /nas1/CAM-chem/20$YR/20$YR$mon
    source ../../mz2camxN3.job $YR$mon >& $YR$mon.txt &
end
cd /nas1/CAM-chem
```
- mz2camxN3.job內容，注意化學物質的對照版本(CB6r4_CF__WACCM)
- 座標及網格系統參照檔：`1709d4`([uamiv格式](https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式))
- 檔案管理
  - 輸入檔即為前述m3.nc檔
  - 因逐6小時處理，結果檔案會很多，放在output目錄下

```bash
#kuang@master /nas1/CAM-chem
#$ cat  mz2camxN3.job
...
set EXE = /nas1/camxruns/src/mozart2camx_v3.2.1/src/mozart2camx_CB6r4_CF__WACCM
...
set MET = /nas1/camxruns/2017/met/mm09/1709d4
...
setenv OUTFILEIC ./output/$DATE$t"d4.ic"
foreach INFILE ($YYMM.m3.nc)
...
```

### CAM-chem的成分
CAM模式與CMAQ模式成分對照如下表：

![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CAM-chemSpec.png)

### 整併與轉換結果
- 利用[shrink](https://sinotec2.github.io/Focus-on-Air-Quality/CAMx/PostProcess/shrink)進行[uamiv格式](https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式)檔案的污染物質壓縮，以產生PM2.5、PM10及VOC項目。
- 逐日結果[合併][cbin]成為逐月檔
- 進行月均值之計算([tmavrg](https://github.com/sinotec2/CAMx_utility/wiki/tmavrg))

```bash
$ cat ic2grd04.cs
for m in {01..12};do 
  cd *$m/output
  for i in $(ls *ic);do 
    ln -s $i $i.avrg.grd04
    shk $i.avrg.grd04
  done
  cbin_all "*.S.grd04" $y${m}IC.S.grd04 >&/dev/null
  tmavrg  $y${m}IC.S.grd04 >&/dev/null
  cd ../../
done
```
[cbin]: <https://github.com/sinotec2/CAMx_utility/wiki/cbin_avrg(cn)> "cbin_all 為傳統uamiv檔案的連接程式，功能與ncrcat之基本功能相同，詳見 https://github.com/sinotec2/CAMx_utility/blob/master/cbin_avrg.par.f"

## Reference
- WEG Administrator, **Welcome to the CAM-chem Wiki**,[wiki.ucar](https://wiki.ucar.edu/display/camchem/Home),13 Jun 2021
- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.
