---
layout: default
title: "OBSGRID"
parent: "WRF"
nav_order: 2
has_children: true
permalink: /docs/wind_models/OBSGRID/
last_modified_at: 2021-11-27 17:15:30
---

{: .fs-6 .fw-300 }

---

# OBSGRID
此處準備WRF四階同化所需要的檔案，整合包括自[NCEP](https://sinotec2.github.io/jtd/docs/wind_models/NCEP/)下載之全球地面及高空觀測、台灣地區[CODiS](https://sinotec2.github.io/jtd/docs/wind_models/CODiS/add_srfFF/)及環保署觀測值，以及[metgrid.exe](https://sinotec2.github.io/jtd/docs/wind_models/WPS/namelist.wps/#metgridexe%E5%86%8D%E5%88%86%E6%9E%90%E6%95%B8%E6%93%9A%E4%B9%8B%E7%B6%B2%E6%A0%BC%E5%8C%96)所產生的`met_em`檔。
{: .no_toc }

## What's Learned 
- Fortran程式修改、[編譯](https://github.com/wrf-model/OBSGRID/blob/master/README)、
- linux [sed](https://terryl.in/zh/linux-sed-command/)、[date](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95)、[cat](https://weikaiwei.com/linux/cat-command/)指令
- 使用[METINFO](http://meteothink.org/)繪製向量與流線圖

## Reference
- Brian Reen, **A Brief Guide to Observation Nudging in WRF**, [github](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/ObsNudgingGuide.pdf),February 2016.
- kkeene44, **WRF Objective Analysis Program**, [github](https://github.com/wrf-model/OBSGRID/blob/master/README),12 Oct 2018.
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
- weikaiwei, **Linux教學：cat指令**, [weikaiwei.com](https://weikaiwei.com/linux/cat-command/), 2021
- Yaqiang Wang, **MeteoInfo Introduction**, [meteothink](http://meteothink.org/), 2021,10,16