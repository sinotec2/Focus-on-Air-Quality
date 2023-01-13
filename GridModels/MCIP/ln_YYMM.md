---
layout: default
title: wrfout檔案之連結
parent: Met. Chem. Interface Proc.
grand_parent: CMAQ Model System
nav_order: 1
date: 2021-12-19 21:21:37
last_modified_date:   2021-12-19 21:21:33
tags: mcip CMAQ
---

# wrfout檔案之連結
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
- 如果`mcip`的批次定義與**WRF**相同，直接在`run_mcip.csh`腳本之設定`wrfout`路徑檔名即可。如果不是，就需要另外的目錄空間，進行前處理（[調整批次定義](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/add_xtime/)），以另外的名稱輸入`mcip`程式。
- 為保持彈性，此處採取後者策略，在`$CMAQ_HOME/data/wrfout`下另外建立目錄，儲存檔案的連結，以備`mcip`來讀取。

## ln_YYMM.cs腳本

### 引數
- 1個引數：年月(4碼)，如範例：

```bash
for mm in 0{1..9} {10..12};do ln_YYMM.cs 19$mm;done
```

### ln_YYMM.cs腳本內容

```bash
YY=`echo $1|cut -c1-2`
MM=`echo $1|cut -c3-4`
begd=$(date -d "20${YY}-${MM}-15 -1 month" +%Y-%m-%d)
prem=$YY$(date -d "20${YY}-${MM}-15 -1 month" +%m)
nexm=$YY$(date -d "20${YY}-${MM}-15 +1 month" +%m)
mkdir -p $1
ROOT=$(echo $PWD|cut -d'/' -f 2)
cd $1
for r in {5..12};do 
  mkdir -p run$r
  cd run$r
  for d in {0..6};do 
    ds=$(( ( $r - 1 ) * 4 + $d -1 ))
    dd=$(date -d "$begd +${ds} day" +%Y-%m-%d )
    ft=20$1
#    if [ $r -eq 5 ] && [ $d -eq 1 ];then ft=20$prem;fi
#    if [ $r -eq 12 ] && [ $d -ge 5 ];then ft=20$nexm;fi
    for DM in 1 2 4;do 
      f=/$ROOT/WRF4.1/WRFv4.1.3/$ft/wrfout/wrfout_d0${DM}_${dd}_00\:00\:00
      ln -sf $f wrfout_d0${DM}_$d
      ln -sf $f ..
    done
  done
  cd ..
done
cd ..
```

## 執行結果
- 以2016/01為例

```bash
kuang@114-32-164-198 /Users/cmaqruns/2016base/data/wrfout
$ tree
.
├── 1601
│   ├── run10
│   │   ├── wrfout_d01_0 -> /Users/WRF4.1/WRFv4.1.3/201601/wrfout/wrfout_d01_2016-01-19_00:00:00
│   │   ├── wrfout_d01_1 -> /Users/WRF4.1/WRFv4.1.3/201601/wrfout/wrfout_d01_2016-01-20_00:00:00
│   │   ├── ...
│   │   └── wrfout_d04_6 -> /Users/WRF4.1/WRFv4.1.3/201601/wrfout/wrfout_d04_2016-01-25_00:00:00
│   ├── run11
│   │   ├── wrfout_d01_0 -> /Users/WRF4.1/WRFv4.1.3/201601/wrfout/wrfout_d01_2016-01-23_00:00:00
│   │   ├── wrfout_d01_1 -> /Users/WRF4.1/WRFv4.1.3/201601/wrfout/wrfout_d01_2016-01-24_00:00:00
```