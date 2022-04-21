---
layout: default
title: CCTM之連續執行與監控
parent: Recommend System
grand_parent: CCTM Main Program
nav_order: 2
date: 2022-04-20 20:27:59
last_modified_date: 2022-04-20 20:45:42
---

# CCTM之連續執行與監控
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

## 前言/背景
## 執行方式
- 基本單元為一批次4天模擬，連續8批次或連續12月，則由上層do_job.csh控制
- 基本執行單元：`source run_cctmMM_RR_DM.csh 01 5 d04 `(執行1月run5第4層之cctm)
- 連續執行：`source do_job.csh cctm `(執行全年12月，每月5~12計8個批次，共96個批次之cctm)

```bash
#$ cat do_job.csh
set SCR=/home/cmaqruns/2016base
setenv CMAQ_HOME $PWD
set JOB = $argv[1]
foreach mm (`seq 1 12`)
  set mon=`printf '%02d' $mm`
  foreach DM ('d04')
    foreach RUN (`seq 5 12`)
      cd $SCR
      source $SCR/run_${JOB}MM_RR_DM.csh $mon $RUN $DM >& ${JOB}_$mon$RUN$DM
    end
  end
end
```
## 執行監視
- 由於程式使用大量電腦資源，「不建議」用top來監控其執行情形。
- 建議：

### 程序數
* 計數CCTM執行程序，如順利執行，此值=100

```bash
$ ps -ef|grep CCTM|wc -l
100
```

### 模式進度時間
 檢視CTM檔案或buff檔案之模式進度時間，如順利進行，時間將逐步增加

```bash
$ grep DDD CTM*|tail
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:165700
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:165830
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170000
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170130
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170300
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170430
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170600
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170730
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:170900
CTM_LOG_095.v53_gcc_1601_run8_20160113_TWN_3X3_10:     Processing Day/Time [YYYYDDD:HHMMSS]: 2016013:171030
```
- [https://sinotec2.github.io/cmaqprog/](https://sinotec2.github.io/cmaqprog/)
### 時間預計
- @supermicron
  - d04每批次約3小時，96批次約12天，基準及增(減)量案例各一，則需24天。
  - d02及前後處理時間另計。
