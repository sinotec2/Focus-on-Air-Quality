---
layout: default
title: REAL & WRF
parent: WRF
nav_order: 3
has_children: true
permalink: /wind_models/REAL/
last_modified_date: 2022-11-28 11:57:12
tags: CWBWRF wrf real sed
---

{: .fs-6 .fw-300 }

---

# REAL & WRF

- 此處統合[OBSGRID](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/)或填入氣象局數值預報值([mk_metoa](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/5.mk_metoa/))之結果，準備WRF所需的初始、邊界、四階同化檔。
- [real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL//doreal_4Nests.sh)與[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)使用同一個名單([namelist.input](https://esrl.noaa.gov/gsd/wrfportal/namelist_input_options.html))，依序執行。
- 除了雙向巢狀網格的作業方式之外，由上到下依序執行單一網格的單向巢狀網格作法，也是替代[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/doreal_4Nests.sh/)的合理方式，特別在網格數較多、雙向巢狀作法太耗費記憶體時。此時會需要[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)
{: .no_toc }

## What's Learned 

- 設定與執行相關說明詳見[User Guide](https://pdfcoffee.com/version-4-modeling-system-users-guide-january-2019-pdf-free.html)，如需中文可見[谷哥首搜](https://report.nat.gov.tw/ReportFront/PageSystem/reportFileDownload/C09502689/001)。
- linux [sed](https://terryl.in/zh/linux-sed-command/)、[日期計算](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95)指令、背景執行[nohup](https://blog.gtwang.org/linux/linux-nohup-command-tutorial/)與[tmux](https://blog.gtwang.org/linux/linux-tmux-terminal-multiplexer-tutorial/)指令。
- [mpirun](https://www.itread01.com/content/1549571058.html)

## Reference

- Mesoscale and Microscale Meteorology Laboratory, NCAR, **Weather Research & Forecasting Model ARW Version 4 Modeling System User’s Guide**, [pdfcoffee](https://pdfcoffee.com/version-4-modeling-system-users-guide-january-2019-pdf-free.html), 2019,1.
- 黃光遠、劉聖宗, **赴美研習WRF數值天氣預報模式報告書**, [交通部民用航空局飛航服務總台](https://report.nat.gov.tw/ReportFront/PageSystem/reportFileDownload/C09502689/001), 2006,10,13
[ESRL](https://esrl.noaa.gov/), **WRF NAMELIST.INPUT FILE DESCRIPTION**, [namelist.input](https://esrl.noaa.gov/gsd/wrfportal/namelist_input_options.html), 
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
- G. T. Wang, **Linux tmux 終端機管理工具使用教學**, gtwang](https://blog.gtwang.org/linux/linux-tmux-terminal-multiplexer-tutorial/), 2019/12/04
- IT閱讀, **MPI常用命令**, [itread01](https://www.itread01.com/content/1549571058.html),2019-02-08