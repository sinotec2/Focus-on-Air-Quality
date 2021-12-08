---
layout: default
title: "namelist.input"
parent: "REAL & WRF"
grand_parent: "WRF"
nav_order: 1
date:               
last_modified_date:   2021-11-28 20:31:23
---

# namelist.input

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
- `namelist.input`同時是控制`real`和`wrf`的名單，其中起訖時間、網格編號，會隨著執行批次而異，此處以**變數**填入，以備各個批次執行時可以隨時替換。


## `namelist.input`模版分段說明
- 批次執行的起訖時間，日期保持變數狀態，以便自動執行時能隨時替換。
  - `SYEA`, `SMON`, `SDAY`:起始年、月、日
  - `EYEA`, `EMON`, `EDAY`:結束年、月、日
  - 起訖小時：為方便後續光化學模式的執行，一律設為**00UTC**

```bash
&time_control
 run_days                            = 5,
 run_hours                           = 0,
 run_minutes                         = 0,
 run_seconds                         = 0,
 start_year                          = SYEA, SYEA, SYEA, SYEA,
 start_month                         = SMON, SMON, SMON, SMON,
 start_day                           = SDAY, SDAY, SDAY, SDAY,
 start_hour                          = 00,   00,   00,  00,
 start_minute                        = 00,   00,   00,  00,
 start_second                        = 00,   00,   00,  00,
 end_year                            = EYEA, EYEA, EYEA, EYEA,
 end_month                           = EMON, EMON, EMON, EMON,
 end_day                             = EDAY, EDAY, EDAY, EDAY,
 end_hour                            = 00,   00,   00,  00,
 end_minute                          = 00,   00,   00,  00,
 end_second                          = 00,   00,   00,  00,
```

## 下載`namelist.input.loop`
點選[github](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/real/namelist.input.loop)

## Reference
- Brian Reen, **A Brief Guide to Observation Nudging in WRF**, [github](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/ObsNudgingGuide.pdf),February 2016.

