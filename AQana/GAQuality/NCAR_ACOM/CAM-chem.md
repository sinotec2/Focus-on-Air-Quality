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
### 檔案管理
- 下載檔案名稱不含有時間資訊，需自nc檔內之歷史訊息(如下)中，將其讀出
- `"Thu Aug  6 20:02:09 2020: /usr/local/nco-4.7.9/bin/ncks -d lat,-2.0,47.0 -d lon,80.0,160.0 /data14a/CAM-Chem/2010/fmerra
.2.1003.FCSD.f09.qfedcmip.56L.001.cam.h1.2010-01-31-00000.nc /net/web3/webt/cam-chem/temp-test/20200806200209164866-20100131.nc" ;`

```bash
kuang@master /nas1/CAM-chem
$ cat mvv.cs
for nc in $(ls cam*nc);do i=$(ncdump -h $nc|grep ncks|cut -d/ -f10|cut -d . -f11|cut -c -10);mv $nc $i.nc;done
```

- 將下載檔案放在指定月份之目錄，方便後續逐月處理。

```bash
kuang@master /nas1/CAM-chem
$ cat ln_yy.cs

for y in 200{0..6};do for m in {01..12};do mkdir -p $y/$y$m;done;done
for y in 200{0..6};do for m in {01..12};do cd $y/$y$m;ln -s ../${y}-${m}-[12]1.nc .;cd ../..;done;done
for y in 200{0..6};do for m in {01..12};do cd $y/$y$m;yy=$(date -d "${y}-${m}-01 -1 days" +%Y);mm=$(date -d "${y}-${m}-01 -1 days" +%m);dd=$(date -d "${y}-${m}-01 -1 days" +%d);ln -sf ../../$yy/${yy}-${mm}-${dd}.nc .;cd ../..;done;done
```

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
- [mz2camxN3.job](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/mz2camxN3.job)之內容重點如下，注意
  - 化學物質的對照版本(CB6r4_CF__WACCM)
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

### 逐月檔案整併成全年
- 因每月檔案並不小，使用cbin_all策略雖然簡單卻不是很有效益，改採python進行。
- 執行批次檔腳本如下

```bash
kuang@master /nas1/CAM-chem
$ cat cb.cs
for y in {07..13};do cd 20$y;for m in {01..12};do cd *$m/output;python ../../../cbin.py $y${m};cd ../../;done;cd ..;done &
```
- cbin.py引用PseudoNetCDF的uamiv模組存取檔案

```python
#kuang@master /nas1/CAM-chem
#$ cat cbin.py
import sys,os,datetime
from PseudoNetCDF.camxfiles.Memmaps import uamiv

fname=sys.argv[1]+'IC.S.grd04L'
nc=uamiv(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
delH=6
nc.TSTEP=delH*10000
nn=24/delH
yr=2000+int(sys.argv[1][0:2])
mn=int(sys.argv[1][2:4])
date0=datetime.datetime(yr,1,1)
bdate=datetime.datetime(yr,mn,1)
nc.STIME=0
nc.SDATE=yr*1000+(bdate-date0).days+1
for v in ['PM10','PM25']:
  nc.variables[v].units='ug/m**3'
for t in range(nt):
  nc.variables['TFLAG'][t,:,1]=[ t%nn*nc.TSTEP for i in range(len(V[3]))] #utc
  tdate=bdate+datetime.timedelta(days=t*delH/24)
  if tdate.month != mn:continue
  fn_t=tdate.strftime("%Y%m%d%H")+'d4.ic.S.grd04'
  nc_t=uamiv(fn_t,'r')
  for v in V[3]:
    nc.variables[v][t,0,:,:]=nc_t.variables[v][0,0,:,:]
  nc_t.close
nc.close
```

## 模擬結果之鄉鎮區平均與校正
- Annual目錄下除彙整各年度年均值結果，其分析程式的用途與連結如下表。

|檔案時間|程式名稱與連結|用途|輸入檔|輸出檔|
|-|-|-|-|-|
|2020-08-14 15:53|[dfpm.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/dfpm.py)|將歷年PM2.5測值寫成[binary檔案][obs]備用，並對縣市範圍繪製逐年核鬚圖以供趨勢確認|環保署歷年PM2.5測值[逐時檔][mxhr]、[縣市][cnty]、[鄉鎮碼][town]對照表|[binary檔][obs]、./pngs/png圖檔|
|2020-08-18 17:03|[dfpm_yd.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/dfpm_yd.py)|逐2年北中南空品區環保署測站逐時觀測結果之盒鬚圖|(同上)|./pngs/box_AQD.png|
|2020-08-17 11:45|[grd04.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/grd04.py)|類似dfpm.py但對象是針對CAM逐6小時模擬結果|各月份目錄下逐6小時avrg檔、[TWN_CNTY_3X3.nc][mask](mask)、[縣市][cnty]、[鄉鎮碼][town]對照表|[binary檔][sim]、png圖檔|
|2020-08-17 13:25|[grd04_yd.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/grd04_yd.py)|逐2年北中南空品區CAM模擬結果之盒鬚圖|(同上)|box_AQD.png|
|2020-08-25 16:32|[join_yc.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/join_yc.py)|合併觀測及模擬(校正)，並繪製空品區之盒鬚圖|前述2個binary檔案、縣市鄉鎮碼對照表、mask檔|box_AQD.png|
|2020-09-07 13:08|[join_yd.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/join_yd.py)|同上，但逐年進行分析，將鄉鎮區平均值分析結果輸出成csv檔|(同上)|鄉鎮區平均值ymd_s_vYY.csv(如[範例](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/ymd_s_v08.csv))|
|2020-09-04 13:30|[ymd2nc.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/ymd2nc.py)|||

[mask]: <https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/TWN_CNTY_3X3.nc> "臺灣地區D4範圍解析度3公里縣市網格之遮蔽(mask)nc檔，縣市代碼2碼，檔案大小1.4M"
[cnty]: <https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/cnty2.csv> "縣市代碼(2碼)、名稱(漢語拼音)"
[town]: <https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/town_aqstEnew.csv> "code舊4瑪,code1縣市,code2鄉鎮區,Name漢音,aq_st測站代碼逗號分開,new_code新8碼,TOWNENG通用拼音"
[obs]: <> "檔名為PMf21_13_32_24_608.bin，各維度分別為21年、13月份、32日、24小時與608鄉鎮區"
[mxhr]: <> "路徑名稱/home/backup/data/epa/pys/PM2.5_mxhr.csv，為/home/backup/data/epa/pys/specMaxHr.py處理結果"
[sim]: <> "檔名為PMf13_12_124_137_83.bin，各維度分別為13年、12月份、124筆逐6小時與Y、X網格"
## Reference
- WEG Administrator, **Welcome to the CAM-chem Wiki**,[wiki.ucar](https://wiki.ucar.edu/display/camchem/Home),13 Jun 2021
- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.
