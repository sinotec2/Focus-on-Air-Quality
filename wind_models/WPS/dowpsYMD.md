---
layout: default
title: "dowpsYMD.sh"
parent: "WPS"
grand_parent: "WRF"
nav_order: 99
date:               
last_modified_date: 2021-12-21 22:23:21
tags: wrf WPS sed
---

# dowpsYMD.sh 

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

- 這個版本一次只執行(`ungrib.exe`+`metgrid.exe`)一天，以因應短期模擬的需求。
- `date`指令修改成`macOS`版本
- 讀取海溫的[python](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/SST/#python)也改成一次讀取一天

## WPS之單日執行方案

### `dowpsYMD.sh`的執行

- `dowpsYMD.sh`的引數有3:
  1. `YYYY`為4碼年代
  1. `MM`為01~12的月份
  1. `DD`為01~31的日期

### `dowpsYMD.sh`分段說明

- 路徑及引數

```bash
kuang@MiniWei /Users/WRF4.3/WPS
$ cat dowpsYMD.cs
#usage: dowps.cs y m d
PATH1=$PWD 
PATH2=/Users/WRF4.1/NCEP

YYYY=$1
MM=$2
DD=$3
```

- 本日及次日之計算(*Mac*版本)

```bash
ym=$(date       -j -f "%Y-%m-%d" "${YYYY}-${MM}-${DD}" +%Y%m)
YY=$(date       -j -f "%Y-%m-%d" "${YYYY}-${MM}-${DD}" +%y)
YN=$(date -v+1d -j -f "%Y-%m-%d" "${YYYY}-${MM}-${DD}" +%y)
MN=$(date -v+1d -j -f "%Y-%m-%d" "${YYYY}-${MM}-${DD}" +%m)
DN=$(date -v+1d -j -f "%Y-%m-%d" "${YYYY}-${MM}-${DD}" +%d)
```

- 用[sed](../../utilities/OperationSystem/sed.md)指令修改模版中的起訖日期
  - 輸出檔的preface一併修改

```bash
cp -f $PATH1/namelist.wps.loopYMD namelist.wps
for cmd in "s/YN/"$YN/g  "s/YP/"$YY/g  "s/MN/"$MN/g  "s/MP/"$MM/g "s/DN/"$DN/g  "s/DP/"$DD/g ;do 
  sed -ie $cmd namelist.wps
done
sed -ie "s/PREWD/FILE/g" namelist.wps
```

- 連結FNL檔案到工作目錄來、執行`ungrib.exe`

```bash
$PATH1/link_grib.csh $PATH2/FNL/$YYYY/fnl_$YYYY$MM${DD}* $PATH2/FNL/$YYYY/fnl_20$YN$MN${DN}* 
ln -sf $PATH1/ungrib/Variable_Tables/Vtable.GFS Vtable

$PATH1/ungrib.exe
```

- 讀取起訖日的[海溫](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/SST/#python)
  - 執行`metgrid.exe`

```bash  
$PATH2/SST/transNC2inter.py $YYYY $MM $DD
$PATH2/SST/transNC2inter.py 20$YN $MN $DN

./metgrid.exe
```

- 儲存結果檔案備用([OBSGRID](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/))

```bash
mkdir -p $PATH1/$ym/met $PATH1/$ym/SST_FILE

mv met_em*nc $PATH1/$ym/met
mv FILE:20* SST:20* $PATH1/$ym/SST_FILE
```

## 腳本出處

- dowpsYMD.sh：[github](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/wind_models/WPS/dowpsYMD.sh_txt)
- 模版：[github](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/wind_models/WPS/namelist.wps.loopYMD)

## Reference
