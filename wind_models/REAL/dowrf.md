---
layout: default
title: "dowrf"
parent: "REAL & WRF"
grand_parent: "WRF"
nav_order: 4
date:               
last_modified_date:   2021-11-29 16:48:48
---

# dowrf

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
- WRF主程式(`wrf.exe`)的執行和REAL是在同一個工作目錄下進行(run)，因所有的初始化(`wrfinput_d01`~`wrfinput_d04`)、邊界條件(`wrfbdy_d01`)、底層條件(`wrflow_d01`~`wrflow_d04`)、FDDA相關檔案都已經產生或連結好，因此可以直接在run目錄執行`wrf.exe`。
- `wrf.exe`是整個過程最耗時的程序，因此其平行化需仔細安排。

## dowrf

### 基本`mpirun`指令
- dowrf的基本指令就是運用`mpirun`啟動`wrf.exe`，如在macOS的環境：
```bash
wrf=/Users/WRF4.3/main/wrf.exe
/usr/local/Cellar/open-mpi/4.1.1_2/bin/mpirun --use-hwthread-cpus $wrf
```

### 全年執行
- 因為run1~4的日子大多落在前一個月，除了1月以外，應沒有必要重新執行，實際執行run5~12即可，如centos的環境：
  - 即使各批次起迄有異，各批次結果皆按日分檔儲存，易於管理。
- 因`wrf.exe`編譯採`dmp`(Distributed Memory Parallelism)設定，會均勻使用工作站核心。過多核心反而會超過範圍內的水平網格數(至少1核負責2個網格點)，由於d01設定是60X60，因此核心數無法超過30。

```bash
kuang@centos8 /data/WRF2019
$ cat dowrf.cs
yyyy=2019
y=$(date -ud "${yyyy}-01-01" +%Y)
exe=/opt/bld/WRF4.3/main/wrf.exe
p=$PWD
for mt in {01..12};do
  ym=${y}${mt}
  if [ $ym == '201901' ];then
    for r in {1..4};do
      cd $p/$ym/run$r
      /opt/mpich/bin/mpirun -np 30 $exe
    done
  fi
  for r in {5..12};do
      cd $p/$ym/run$r
      /opt/mpich/bin/mpirun -np 30 $exe
  done
done
```

## Reference
- Mesoscale and Microscale Meteorology Laboratory, NCAR, **Weather Research & Forecasting Model ARW Version 4 Modeling System User’s Guide**, [pdfcoffee](https://pdfcoffee.com/version-4-modeling-system-users-guide-january-2019-pdf-free.html), 2019,1.
- 黃光遠、劉聖宗, **赴美研習WRF數值天氣預報模式報告書**, [交通部民用航空局飛航服務總台](https://report.nat.gov.tw/ReportFront/PageSystem/reportFileDownload/C09502689/001), 2006,10,13
[ESRL](https://esrl.noaa.gov/), **WRF NAMELIST.INPUT FILE DESCRIPTION**, [namelist.input](https://esrl.noaa.gov/gsd/wrfportal/namelist_input_options.html), 
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
- weikaiwei, **Linux教學：cat指令**, [weikaiwei.com](https://weikaiwei.com/linux/cat-command/), 2021
- G. T. Wang, **Linux 計算機bc 指令用法教學與範例**, [gtwang](https://blog.gtwang.org/linux/linux-bc-command-tutorial-examples/), 2018/08/23
- G. T. Wang, **Linux 的nohup 指令使用教學與範例，登出不中斷程式執行**, [gtwang](https://blog.gtwang.org/linux/linux-nohup-command-tutorial/), 2017/09/12
