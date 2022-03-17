---
layout: default
title: Initial Condition
parent: CMAQ Model System
nav_order: 3
has_children: true
permalink: /GridModels/ICON/
---

# 初始條件之準備
{: .no_toc }

**CMAQ**模式的初始條件有3種給定方式：
1. 由[全球模式模擬結果](/Focus-on-Air-Quality/GridModels/BCON/moz2cmaqH/)檔案解讀(`REGRID`)
1. 由前一批次**CMAQ**執行成果解讀(`REGRID`)
1. 以一組觀測值或符合化學平衡的模擬結果設定(`PROFILE`)
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## 初始檔案的連結
- 前一批次模擬的最後一小時CCTM程式會將瞬間濃度值寫入檔案
  - 檔案名稱的根部為**CCTM_CGRID**
  - 含有226項污染物，包括氣狀物及各mode的氣膠濃度

### 全新的開始(NEW_START)
- 約定$ICFILE檔名=`ICON_${VRSN}_${APPL}_${GRID_NAME}_${ICTYPE}_${YYYYMMDD}`
  - 第一個月的run5要以手動方式連結
  - 其他月份，則由前一批次(`PRUNID`)的最後一天CCTM_CGRID檔案連結過來到$ICpath

```python
kuang@MiniWei /Users/cmaqruns/2018base
$ cat mac_cctmMM_RR_DM.csh 
298 # =====================================================================
299 #> Input Files (Some are Day-Dependent)
300 # =====================================================================
301 
302   #> Initial conditions
303   if ($NEW_START == true || $NEW_START == TRUE ) then
304      setenv ICFILE ICON_${VRSN}_${APPL}_${GRID_NAME}_${ICTYPE}_${YYYYMMDD}
305      if ( $MO != '01' ) then
306        set PYM = `date -v-1m -j -f "%Y%m%d" "20${APYM}01" +%y%m`
307        set PRUNID = ${VRSN}_${compilerString}_${PYM}_run12
308        set POUTDIR = ${OUTDIR}/../output_CCTM_${PRUNID}
309        ln -sf ${POUTDIR}/CCTM_CGRID_${PRUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc \
310                 $ICpath/$ICFILE
311      endif
312      setenv INIT_MEDC_1 notused
313      setenv INITIAL_RUN Y #related to restart soil information file
```

### 再開始(RESTART)情況
- 設定成同一批次前一天最後一小時的CCTM_CGRID檔案
- 如果為批次的第一天則將前一批次(`PRUNID`)的最後一天CCTM_CGRID/CCTM_MEDIA_CONC檔案連結過來到$ICpath

```python
314   else
315      set ICpath = $OUTDIR
316      setenv ICFILE CCTM_CGRID_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
317      setenv INIT_MEDC_1 $ICpath/CCTM_MEDIA_CONC_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
318      setenv INITIAL_RUN N
319      if ( $TODAYJ == $START_DAY ) then
320        @ PRUN = $RUN - 1
321        set PRUNID = ${VRSN}_${compilerString}_${APYM}_run${PRUN}
322        set POUTDIR = ${OUTDIR}/../output_CCTM_${PRUNID}
323        ln -sf ${POUTDIR}/CCTM_CGRID_${PRUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc \
324                 $OUTDIR/CCTM_CGRID_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
325        ln -sf ${POUTDIR}/CCTM_MEDIA_CONC_${PRUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc \
326                 $OUTDIR/CCTM_MEDIA_CONC_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
327      endif
328   endif
```

