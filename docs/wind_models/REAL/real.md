---
layout: default
title: "REAL"
parent: "wind models"
nav_order: 6
has_children: true
permalink: /docs/wind_models/REAL/
last_modified_at: 2021-11-28 15:52:50
---

{: .fs-6 .fw-300 }

---

# REAL
此處統合[OBSGRID](https://sinotec2.github.io/jtd/docs/wind_models/OBSGRID/)結果，準備WRF所需的初始、邊界、四階同化檔。REAL與WRF使用同一個名單(namelist.input)。

## What's Learned 
- linux [sed](https://terryl.in/zh/linux-sed-command/)、[日期計算](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95)指令
{: .no_toc }

## Reference
- Brian Reen, **A Brief Guide to Observation Nudging in WRF**, [github](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/ObsNudgingGuide.pdf),February 2016.
- kkeene44, **WRF Objective Analysis Program**, [github](https://github.com/wrf-model/OBSGRID/blob/master/README),12 Oct 2018.
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
