---
layout: default
title: "obsYYMM_run.sh"
parent: "OBSGRID"
grand_parent: "wind models"
nav_order: 3
date:               
last_modified_date:   2021-11-28 20:33:12
---

# obsYYMM_run.sh

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
- 除了wrf本身之外，系統各個階段的執行所需時間，以`obsgrid`最多，因此其執行平行化也最有必要。
- `obsgrid`程式本身並沒有平行化的設計，因此在OS層次就必須多考量。
- 此處所面對的作業挑戰是要做**全年**的`obsgrid`，所以分月執行，是基本的分工方式。
- 由於wrf的執行期間不能太長，以避免數值發散。此處規劃每批次間隔**4天**，批次時間為**5天**，其中重疊**1天**。

## OBSGRID 之全月執行方案

### `final`之預備
- `obsgrid`彙整所有[little_R](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式的觀測數據。由於`little_r`是個[ASCII](https://zh.wikipedia.org/wiki/ASCII)檔案，可以用[cat](https://weikaiwei.com/linux/cat-command/)指令將其整併
- 如果不存在檔案，`cat`指令仍然繼續執行。

```bash
y=2019
f1=/Users/WRF4.1/NCEP/SRF_ds461.0/$y/SURFACE_OBS:${y}
f2=/Users/WRF4.1/NCEP/SUPA_ds351.0/$y/OBS:${y}
f3=/Users/WRF4.1/NCEP/cwb_data/$y/cwbsrf/cwbsrf:${y}
f4=/Users/WRF4.1/NCEP/cwb_data/$y/cwbupa/cwbupa:${y}
f5=/Users/WRF4.1/NCEP/epa_data/$y/epasrf:${y}
f6=/Users/WRF4.1/NCEP/SOBSGRID_DATA/final:${y}
for m in 0{1..9} {10..12};do
  for d in 0{1..9} {10..31};do
    for h in 0{0..9} {10..23};do
      cat ${f1}${m}${d}${h} ${f2}${m}${d}${h} ${f3}-${m}-${d}_${h} ${f4}-${m}-${d}_${h} ${f5}-${m}-${d}_${h} > ${f6}-${m}-${d}_${h}
    done
  done
done
```

### `namelist.oa`模版
- 因為每批次、每層網格的`namelist.oa`都有所不同，必須按照規則進行修改，此處以複製模版、局部置換的方式辦理。
- 置換的方式採用linux [sed](https://terryl.in/zh/linux-sed-command/)指令
- 模版詳見[namelist.oa](https://sinotec2.github.io/jtd/docs/wind_models/OBSGRID/namelist.oa/)說明

### `obsYYMM_run.sh`的執行
- 開啟12個月份的專屬目錄（OBS01~OBS12），其下再開啟12個批次run1~run12,共144個批次同時進行。
- 每批次工作目錄執行：`obsYYMM_run.sh` YYMM RR，YYMM為年月(4碼)、RR批次編號(1~12)

```bash
y=19
for m in 0{1..9} {10..12};do
  for r in {1..12};do
    dir=OBS$m/run$r
    mkdir -p $dir
    cd $dir
    sub obsYYMM_run.sh $y$m $r
    cd ../..
  done
done
```

## `obsYYMM_run.sh`分段說明
- 讀進引數與連結`met_em`檔案
  - 第一引數：年月(4碼)
  - 第二引數：批次編號(1~12)

```bash
     1	#usage: obsYYMM_run.sh 1304 5
     2	path=/Users/WRF4.3/OBSGRID
     3	ym=$1
     4	j=$2
     5	ln -sf $path/../WPS/20$ym/met/met_em* .
```

- 起訖年月日之[計算](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95)
  - 每批次起始日差**4天**，使用[bc](https://blog.gtwang.org/linux/linux-bc-command-tutorial-examples/)進行計算`"4*($j-1)"|bc -l`。
  - 每批次執行**5天**(1天重疊)

```bash
     6	begd=$(date -v-1m -j -f "%Y%m%d" "20${ym}15" +%Y%m%d)
     7	dd=`echo "4*($j-1)"|bc -l`
     8	ymd1=$(date -v+${dd}d -j -f "%Y%m%d" "${begd}" +%Y%m%d)
     9	ymd2=$(date -v+5d     -j -f "%Y%m%d" "${ymd1}" +%Y%m%d)
    10	yea1=`echo $ymd1|cut -c1-2`;mon1=`echo $ymd1|cut -c3-4`;day1=`echo $ymd1|cut -c5-6`
    11	yea2=`echo $ymd2|cut -c1-2`;mon2=`echo $ymd2|cut -c3-4`;day2=`echo $ymd2|cut -c5-6`
    12	
```

- 每層網格**依序**執行
  - `namelist.oa.loop`模版的複製
  - 替換其中起訖年月日、網格編號。使用[sed](https://terryl.in/zh/linux-sed-command/)指令

```bash
    13	for d in {1..4};do #domain
    14	#copy the template and change the beg/end dates by sed
    15	  cp -f $path/namelist.oa.loop namelist.oa
    16	  for cmd in   "s/SYEA/20$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" \
    17	    "s/GID/$d/g" "s/EYEA/20$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g";do
    18	    sed -ie $cmd namelist.oa
    19	  done
    20	
```

- 依序執行`obsgrid`, [run_cat_obs_files.csh](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/run_cat_obs_files.csh), `filter_p`
  - 按照grid_size編譯`obsgrid`，參考[程式修改及編譯](https://sinotec2.github.io/jtd/docs/wind_models/OBSGRID/程式修改及編譯/)
  - [run_cat_obs_files.csh](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/run_cat_obs_files.csh)為WRF系統提供的批次腳本，旨在將OBS_DOMAIN檔案合併，以備obs納進使用。
  - [filter_p]((http://200.200.31.47/nas1/WRF4.0/WRFv3.9/OBSGRID/filter_p.f))濾掉OBS_DOMAIN檔案中測站數據完全無效者。

```bash
    21	#execution the programs
    22	  $path/src/obsgrid$d.exe
    23	  $path/run_cat_obs_files.csh $d
    24	  $path/../FILTER/filter_p $d
    25	done
    26	
```

- 儲存（整併）結果

```bash
    27	#store the results
    28	mkdir -p $path/20$ym/run$j
    29	mv -f metoa_em* OBS_DOMAIN* wrfsfdda* $path/20$ym/run$j
    30	
```

## 下載`obsYYMM_run.sh`
點選[github](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/wind_models/OBSGRID/obsYYMM_run.sh)

## Reference
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- G. T. Wang, **Linux 計算機bc 指令用法教學與範例**, [gtwang](https://blog.gtwang.org/linux/linux-bc-command-tutorial-examples/), 2018/08/23
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
- weikaiwei, **Linux教學：cat指令**, [weikaiwei.com](https://weikaiwei.com/linux/cat-command/), 2021