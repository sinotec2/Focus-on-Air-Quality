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


## `namelist.input`模版說明
### 起迄時間之設定
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

### wrfout輸出變數項目之增減
- wrfout輸出哪些變數，是在Regisry/Registry.EM檔案中指定的(IO設定值含有h)，如要修改，可以修改該登記檔，clean -a、configure、compile重新編譯，如範例
```python
state    real    CLDFRA2      ikj    misc     1         -      h        "CLDFRA2"             "CLOUD FRACTION"
state    real    RAINPROD     ikj    misc     1         -      h        "RAINPROD"            "TOTAL RAIN PRODUCTION RATE"       "s-1"
state    real    EVAPPROD     ikj    misc     1         -      h        "EVAPPROD"            "RAIN EVAPORATION RATE"            "s-1"
```
- 如不重新編譯亦可在nmelist.input檔案中[設定](http://www2.mmm.ucar.edu/wrf/users/docs ... #runtimeio)
  - my_file_d01\~2.txt為文字檔，每個domain必須要有一個檔案。內容如後。
```python
&time_control
iofields_filename = “my_file_d01.txt”, “my_file_d02.txt”
ignore_iofields_warning = .true.,
/
```
- my_file_d01.txt的內容
  - `+`、`-`增加或減少之標籤
  - `i` for input/`h` for history(output)
  - 0 for default, number for stream number
  ` variable names
```python
-:h:0:RAINC,RAINNC
+:h:0:EDUST1,EDUST2,EDUST3,EDUST4,EDUST5
```


## 下載`namelist.input.loop`
點選[github](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/wind_models/REAL/namelist.input.loop)

## Reference
- Brian Reen, **A Brief Guide to Observation Nudging in WRF**, [github](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/ObsNudgingGuide.pdf),February 2016.

