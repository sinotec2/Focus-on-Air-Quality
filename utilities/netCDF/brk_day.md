---
layout: default
title:  按日拆分m3.nc檔案
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2021-12-18 20:50:01
---
# 按日拆分m3.nc檔案(brk_day2.cs)
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
- 雖然CCTM的執行批次範圍是數日，但CCTM腳本常將所需的輸入檔切割成逐日檔，其考量可能是：
  * 方便進行批次範圍的組合，如果要拆散再另行組合成其他起訖日期的批次(如CCTM的邊界條件 之bld_19.cs)，有逐日檔案勢必方便許多
  * **MM5**/**WRF**以來的IO習慣，很多也是逐日儲存。
  * 檔案管理維護比單一大檔容易，壞了某一天檔案只須修復該日檔案即可
- 但是對於系統性修改，**逐月**檔案會比**逐日**檔案方便。這2個面向如果要同時滿足，勢必需要有轉換的程式。
  * 合併：可以將全月範圍的檔案放在同一目錄，有足夠的月前、月後日期，如此就可以應用[ncrcat]()一次整併。
  * 拆分：雖然可以用`ncks -d`來做，但其中還需少許的日期計算、確認等等。

## brk_day2.cs腳本程式

### 引數
- 需拆分的檔案名稱
- 檔案命名規則
  * 檔案必須以`dot`做為間隔
  * 年月必須在第2個`dot`間格位置，用以開啟目錄、判斷前後月份、
  * 「年月」將被「年月日」替換掉，檔名其餘部分不會更動
  * 範例：teds10.**1601**.timvar.nc、ind_EAsia_81K.**1601**.nc

### 數據所在路徑
- (無約定)
- 腳本會在數據所在位置下開設yymm的目錄。

### 日期的計算
* 按照**WRF**執行[批次的約定](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/#%E6%89%B9%E6%AC%A1%E7%9A%84%E5%AE%9A%E7%BE%A9)，前月15日為起始日，run5為當月CCTM執行開始日
* 將檔案內容所有時間都予以拆分，總小時數由`ncdump`得知
* 每一天筆數`HRPD` ：24小時與`TSTEP`的商數，`TSTEP`由`ncdump`得知
* 還要修正逐日檔的`SDATE`屬性(`yrj`)，CCTM會檢查
* 給定日期(`ymd`)做為新檔名```newfn=${fn/$yrmn/$ymd} ```
* yrj、ymd由`date`計算而得，才有一致性不會出錯。 

### brk_day2.cs腳本程式內容
```bash
if [ $HOSTNAME == '114-32-164-198.HINET-IP.hinet.net' ];then NCO='/opt/anaconda3/bin'
  elif [ $HOSTNAME == 'master' ];then NCO='/cluster/netcdf/bin'
  elif [ $HOSTNAME == 'centos8' ];then NCO='/opt/anaconda3/envs/py37/bin'
  elif [ $HOSTNAME == 'node03' ];then NCO='/opt/miniconda3/bin'
  else NCO='/usr/bin'
fi
NCKS=${NCO}/ncks
NCATTED=${NCO}/ncatted
fn=$1
yrmn=$(echo $fn|cut -d'.' -f2)
mkdir -p $yrmn
last=$(date -d "20${yrmn}01 -1days" +%Y%m%d)
y=$(date -d $last +%Y)
m=$(date -d $last +%m)
begd=$(date -d "${y}-${m}-15 +16days" +%Y%m%d)
begj=$(date -d "${begd}" +%Y%j)
SDATE=$(ncdump -h $fn|grep SDATE|awkk 3)
if [ $begj != $SDATE ]; then 
  echo $begj $SDATE 'not ok in SDATE'; 
  jj=$(( $SDATE - 2016001 ))
  begd=$(date -d "2016-01-01 +${jj}days" +%Y%m%d)
fi
nt=$(ncdump -h $fn|head -n3|tail -n1|cut -d'(' -f2|awkk 1)
nd=$(echo $nt/24|bc)
for ((d=1;d<=$nd;d+=1));do
  dd=$(( $d - 1 ))
  yrj=$(date -d "${begd} +${dd}days" +%Y%j)
  ymd=$(date -d "${begd} +${dd}days" +%Y%m%d)
  t1=$(( $dd * 24 )) 
  t2=$(( $d  * 24 )) 
  newfn=${fn/$yrmn/$ymd}
  $NCKS -O -d TSTEP,$t1,$t2 $fn $yrmn/$newfn
  $NCATTED -O  -a SDATE,global,o,i,$yrj $yrmn/$newfn
  echo $yrmn/$newfn 
done
```

### 平行運作
* ncks可以平行運做，但不見得有較高的效率，涉及檔案存取的速度瓶頸、以及工作站的記憶體。
* 此腳本一次處理一整個月，如果有跨月、大小月問題，應俟全年處理完後，執行[ln_run12.cs]()來連結修正