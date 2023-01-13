---
layout: default
title: "doreal_4Nests.sh"
parent: "REAL & WRF"
grand_parent: "WRF"
nav_order: 2
date:               
last_modified_date:   2021-11-28 20:30:22
tags: wrf real
---

# doreal_4Nests.sh

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
- 執行REAL所需要的時間雖然不是很多，但是對12個月、共144個執行批次置換名單（[namelist.input]()）的起訖日期，還真是一個繁瑣、容易出錯的工程。
- 雖然可以先行產生，只修改年度。然而不同年度因著閏年、3月之後每個批次將不會一樣，因此還是需要就年度逐一產生，比較不易出錯。
- 對於任意起訖時間的執行批次，也可經由邏輯性的置換作業，得到需要的名單。

## REAL 之全月執行方案

### 各月份12個批次`met_em`之預備
- 詳見[WPS](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WPS/)之運作。

### 各月份12個批次`wrfsfdda`, `OBS_DOMAIN`, `wrfsfdda`之預備
- 詳見[OBSGRID](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/)之運作。

### `namelist.input`模版
- 因為每批次、每層網格的`namelist.oa`都有所不同，必須按照規則進行修改，此處以複製模版、局部置換的方式辦理。
- 置換的方式採用linux [sed](https://terryl.in/zh/linux-sed-command/)指令
- 模版詳見[namelist.input](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/namelist.input/)說明

### `doreal_4Nests.sh`的執行
- 開啟12個月份的專屬目錄（YYYY01~YYYY12），其下再開啟12個批次run1~run12,共144個批次同時進行。
- 每批次工作目錄執行：`doreal_4Nests.sh` 

```bash
y=2019
for m in 0{1..9} {10..12};do
  dir=/Users/WRF4.3/${y}$m
  mkdir -p $dir
  cd $dir
  sub doreal_4Nests.sh
done
```

## `doreal_4Nests.sh`分段說明
- 定義工作及輸入檔路徑
```bash
     1	#!/usr/local/bin/bash
     2	PATH1=/Users/WRF4.3
     3	PATH2=/Users/WRF4.3/OBSGRID
```
- 由所在目錄中讀取年月資訊、設定`run1`的起始日期（前月的15日）
```bash
     4	# working directory path name contains YYYYMM in the fourth section
     5	ym=`echo $PWD|cut -d'/' -f4|cut -c3-6`
     6	begd=$(date -v-1m -j -f "%Y%m%d" "20${ym}15" +%Y%m%d)
```
- 每一批次逐一進行
  - [計算](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95)批次的起訖日期
    - 每批次起始日差**4天**，使用[bc](https://blog.gtwang.org/linux/linux-bc-command-tutorial-examples/)進行計算`"4*($j-1)"|bc -l`。
    - 每批次執行**5天**(1天重疊)
  - 創建批次工作目錄
  - 連結執行`real.exe`, `wrf.exe`等所需的執行檔、參數條件檔案（`$PATH1/run/*`）
  - 下到批次目錄、連結[OBSGRID](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/)對應結果
```bash
     7	for j in {1..12};do
     8	  dd=`echo "4*($j-1)"|bc -l`
     9	  ymd1=$(date -v+${dd}d -j -f "%Y%m%d" "${begd}" +%Y%m%d)
    10	  ymd2=$(date -v+5d     -j -f "%Y%m%d" "${ymd1}" +%Y%m%d)
    11	  yea1=`echo $ymd1|cut -c1-2`;mon1=`echo $ymd1|cut -c3-4`;day1=`echo $ymd1|cut -c5-6`
    12	  yea2=`echo $ymd2|cut -c1-2`;mon2=`echo $ymd2|cut -c3-4`;day2=`echo $ymd2|cut -c5-6`
    13	  mkdir -p $PATH1/20$ym/run$j
    14	  ln $PATH1/run/* $PATH1/20$ym/run$j
    15	  cd $PATH1/20$ym/run$j
    16	  ln -sf $PATH2/20$ym/run$j/metoa_em* .
    17	  ln -sf $PATH2/20$ym/run$j/wrfsfdda* .
    18	  for d in {1..4};do #domain
    19	    ln -sf $PATH2/20$ym/run$j/OBS_DOMAIN$d"01p" OBS_DOMAIN$d"01"
    20	  done
```
- 複製[namelist.input.loop模版](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/wind_models/REAL/namelist.input.loop)、使用[sed](https://terryl.in/zh/linux-sed-command/)指令置換起訖日期
  - 一般`sed`指令使用`-i`(Edit files in-place)選項即可，`macOS`需要用`-ie`(editing commands)
```bash
    21	  cp -f $PATH1/20$ym/namelist.input.loop namelist.input
    22	  for cmd in "s/SYEA/20$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" "s/SHOU/00/g"\
    23	    "s/EYEA/20$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g" "s/EHOU/00/g";do
    24	    sed -ie $cmd namelist.input
    25	  done
```
- 使用[nohup](https://blog.gtwang.org/linux/linux-nohup-command-tutorial/)將`real.exe`放在背景執行。
  
```bash
    26	  nohup ./real.exe&
    27	done
```

### 用`tmux` 取代`nohup`
- 由於`nohup`的年代有點久遠，現在大多的OS提供了[tmux](https://stackoverflow.com/questions/31902929/how-to-write-a-shell-script-that-starts-tmux-session-and-then-runs-a-ruby-scrip)來取代`nohup`，zsh甚至不主動提供nohup.
- 此處的`nohup`將會變成...
```bash
#!/bin/bash
tmux new-session -d -s run${j}${d} './real.exe'
```

- 使用`tmux ls`指令，可以看到[tmux](https://blog.gtwang.org/linux/linux-tmux-terminal-multiplexer-tutorial/)正在運作(假設`j=6;d=1`)
```bash
kuang@114-32-164-198 /Users/WRF4.3/201804/run6
$ tmux ls
run6d1: 1 windows (created Mon Nov 29 21:15:09 2021)
$ ps
  PID TTY           TIME CMD
74431 ttys000    0:00.29 -bash
98383 ttys001    0:00.05 -bash
 2488 ttys002    0:00.17 ./real.exe
```
- 簡單的`tmux`6個基本指令亦可參考[tumx@FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/tmux/#%E5%9F%BA%E6%9C%AC%E6%8C%87%E4%BB%A4)

## 下載`doreal_4Nests.sh`
點選[github](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/REAL/doreal_4Nests.sh_txt)

## Reference
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
- weikaiwei, **Linux教學：cat指令**, [weikaiwei.com](https://weikaiwei.com/linux/cat-command/), 2021
- G. T. Wang, **Linux 計算機bc 指令用法教學與範例**, [gtwang](https://blog.gtwang.org/linux/linux-bc-command-tutorial-examples/), 2018/08/23
- G. T. Wang, **Linux 的nohup 指令使用教學與範例，登出不中斷程式執行**, [gtwang](https://blog.gtwang.org/linux/linux-nohup-command-tutorial/), 2017/09/12
- Nick, **How to write a shell script that starts tmux session, and then runs a ruby script**, [stackoverflow](https://stackoverflow.com/questions/31902929/how-to-write-a-shell-script-that-starts-tmux-session-and-then-runs-a-ruby-scrip), 2016,Sep 14.
- G. T. Wang, **Linux tmux 終端機管理工具使用教學**, [gtwang](https://blog.gtwang.org/linux/linux-tmux-terminal-multiplexer-tutorial/), 2019/12/04