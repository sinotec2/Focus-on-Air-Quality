---
layout: default
title: "NCEP"
parent: "wind models"
nav_order: 2
has_children: true
permalink: /docs/wind_models/NCEP/
last_modified_at: 2021-11-27 08:45:19
---

# NCEP

{: .fs-6 .fw-300 }

## What's Learned 
- 自動批次[執行排程](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/)及報錯方式的設定、監控。
- 修改一個其他作者寫的`python2`的程式
  - 讓`python`程式從檔案系統中讀取檔名、解析日期
  - 日期的計算
  - 字串的連接、管理

## 背景
- [NCEP](https://www.weather.gov/ncep/) (National Centers for Environmental Prediction)是美國海洋大氣總署NOAA轄下有關環境議題的預測研究及作業中心。所提供全球觀測數據是大氣動力模式必須之初始及邊界條件。
  - 此處介紹自動下載作業的細節，包括再分析數據([ds.083.2](https://rda.ucar.edu/datasets/ds083.2/index.html#!description))、地面觀測([ds461.0](https://rda.ucar.edu/datasets/ds461.0/#!description))、以及探空觀測([ds351.0](https://rda.ucar.edu/datasets/ds351.0/#!description))等3項。
- NCEP提供下載的`python`腳本，早期是`python2`,現已更新至`python3`。此處依據的是舊版腳本。

## 批次執行
- 3項下載**依序**執行。
- **不建議**同時多次登入NCEP網站，會引發網站保護機制，列入黑名單。
- 腳本說明
  - 每天登入網站，因此需刪除舊的登入許可檔`auth.rda.ucar.edu`
  - 依序執行再分析數據([ds.083.2](https://rda.ucar.edu/datasets/ds083.2/index.html#!description))、地面觀測([ds461.0](https://rda.ucar.edu/datasets/ds461.0/#!description))、以及探空觀測([ds351.0](https://rda.ucar.edu/datasets/ds351.0/#!description))等3項下載。
  - 如果下載成功、每天將會增加12個檔案。
  - 檢查結果，如果`log`檔內不是12個，則呼叫`macOS`的`osascript`程式，印出錯誤訊息。
  - 因隔天程式還是會補上遺失的檔案，檔案個數仍然不是12個3，所以還是會再報錯。但第三天報錯就一定要人工檢查、修正錯誤。

```bash
$ cat /Users/WRF4.1/NCEP/fus.cs
cd /Users/WRF4.1/NCEP
if [ -e auth.rda.ucar.edu ];then rm -f auth.rda.ucar.edu;fi
./ff.py
./uu.py
./ss.py
n=$(grep done crontab_log.txt|wc -l)
if ! [ $n == 12 ];then 
  d=$(date "+%Y/%m/%d")
  /usr/bin/osascript -e 'tell app "System Events" to display dialog "Something wrong in fus.cs @'$d' !"' &
fi
```

## 自動執行
- 設計夜間21:00進行下載，`crontab`如下：
```bash
crontab -l|grep fus
0 21  *  *  * /Users/WRF4.1/NCEP/fus.cs &> /Users/WRF4.1/NCEP/crontab_log.txt 2>&1
```

## Reference
- G. T. Wang, **Linux 設定 crontab 例行性工作排程教學與範例**,[G. T. Wang](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/), 2019/06/28
- PengboGai, **Mac OS X 执行osascript命令**, [jianshu](https://www.jianshu.com/p/d42dff738d70), 2018.07.18
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- [Here](https://sinotec2.github.io/jdt/doc/wind_models/NCEP/)
- 
