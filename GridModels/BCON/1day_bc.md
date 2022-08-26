---
layout: default
title: 逐日循序執行bcon.exe
parent: Boundary Condition
grand_parent: CMAQ Model System
nav_order: 6
date: 2022-08-25 12:11:42
last_modified_date: 2022-08-25 12:11:46
---

# 逐日循序執行bcon.exe
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
- 大型、多層網格、連日的CMAQ執行結果，要接續執行bcon.exe會遭遇到龐大濃度檔(ACONC)的問題。雖然如[大型網格系統切割邊界濃度](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/hd_bc)文中所述，可以python程式來執行內插與切割，但仍然不夠快速、簡潔。
- 由於CMAQ結果是逐日輸出，因此發展逐日執行bcon.exe還是比較合理的作法，唯一的困難，是bcon程式內設會從METBDY3D讀取相對應的起始時間，會需要：
  1. 將執行批次的METBDY3D檔案切割成逐日
  2. 逐日METBDY3D檔案的SDATE需配合ACONC濃度檔案的內容。
- 前述2項作業在[brk_day2.cs](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/brk_day)中已經妥善處理好了，只需執行即可(還好METBDY3D檔案並不太大，即使重複儲存也還能容忍)。

## 腳本內容
### 引數
- 1個引數：上層CCTM執行成果(CCTM_ACONC檔案)
  - 檔案需含網格系統名稱的目錄，對照關係如下
  - 如`/nas2/cmaqruns/2022fcst/grid45/cctm.fcst/daily/CCTM_ACONC_v532_intel_Taiwan_20220828.nc`，
  - 腳本會自檔案目錄的第5欄找到網格名稱，以對應到mcip檔案、開啟下一層的輸出檔。

序號|公版模式習慣|網格系統名稱|說明
:-:|:-:|:-:|:-:
1|grid45|CWBWRF_45k|
2|grid09|SECN_9k|
3|grid03|TWEAP_3k|

- 說明：公版模式的GDNAM全部設成'Taiwan'，因此無從辨識其網格系統內容。

### 輸出檔名的設定
- 雖然ACONC檔名中即有日期資訊，此處還是從nc.SDATE內容來讀取，比較穩妥。
  - y, j分別為年代及julian day
  - 使用date指令計算日期

```bash
set DATE  = `ncdump -h $nc|grep SDATE|awk '{print $3}'`
set y = `echo $DATE|cut -c1-4`
set j = `echo $DATE|cut -c5-`
set NDAYS = 1

    set YYYYJJJ  = ${DATE}   #> Convert YYYY-MM-DD to YYYYJJJ
    set YYYYMMDD = `date -d "${y}-01-01 +${j}days -1days" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
```      

### 執行批次
- 雖然bcon.exe也可以同步執行，但因速度還可以接受，此處就循序進行，
- 最後用ncrcat將其連成一個大檔，還要加上最後一個小時值的bc就完成了。

```bash
dates=()
for id in {0..4};do
  dates=( ${dates[@]} $(date -d "$BEGD +${id}days" +%Y%m%d) )
done
for i in 0 1 2;do
  ii=$(echo ${GRD[$i]}|cut -c5-)
  cd $fcst/grid$ii/smoke
  ../../mk_emis.py $BEGD
  cd $fcst
  csh ./run.cctm.${ii}.csh >&/dev/null

  # nest down BCON and ICON
  test $i -eq 2 && continue
  for id in {0..4};do
    nc=$fcst/grid$ii/cctm.fcst/daily/CCTM_ACONC_v532_intel_${DOM[$i]}_${dates[$id]}.nc
    csh ./run_bcon_NC.csh $nc >&/dev/null
  done
  cd $fcst/grid$ii/bcon #(same bcon pool)
  j=$(( $i + 1))
  f=()
  for id in {0..4};do
    f=( ${f[@]} BCON_${dates[id]}_${DOM[$j]} )
  done
  ncrcat -O  ${f[@]} BCON_today_${DOM[$j]}
  cd $fcst
  csh ./run_icon_NC.csh $fcst/grid$ii/icon/ICON_yesterday_${DOM[$i]} >&/dev/null
done
```

### 腳本內容

```bash
#kuang@DEVP /nas2/cmaqruns/2022fcst
#$ cat run_bcon_NC.csh
#!/bin/csh -f

# ======================= BCONv5.3 Run Script ========================
# Usage: run.bcon.csh >&! bcon_v53.log &
#
# To report problems or request help with this script/program:
#             http://www.cmascenter.org
# ====================================================================

# ==================================================================
#> Runtime Environment Options
# ==================================================================

#> Choose compiler and set up CMAQ environment with correct
#> libraries using config.cmaq. Options: intel | gcc | pgi
 setenv compiler gcc

#> Source the config_cmaq file to set the run environment
 setenv CMAQ_HOME /nas2/cmaqruns/2022fcst
 source /opt/CMAQ_Project/config_cmaq.csh $compiler

# popd

#> Set General Parameters for Configuring the Simulation
set nc         = $argv[1]
set DM         = `echo $nc|cut -d'/' -f5`

set VRSN      = v53                     #> Code Version
#> Horizontal grid definition
set BCTYPE   = regrid             #> Initial conditions type [profile|regrid]
if ( $DM == 'grid45' ) then
  setenv GRID_NAMEC CWBWRF_45k    # 16-character maximum
  setenv GRID_NAME  SECN_9k       # 16-character maximum
  set DMF = grid09
else if ( $DM == 'grid09' ) then
  setenv GRID_NAMEC  SECN_9k       # 16-character maximum
  setenv GRID_NAME  TWEPA_3k      # 16-character maximum
  set DMF = grid03
else
  echo "Error input nc, must with grid??"
  exit 1
endif
set CMAQ_DATA = ${CMAQ_HOME}/${DMF}


#> Set the build directory:
 set BLD      = /opt/CMAQ_Project/PREP/bcon/scripts/BLD_BCON_${VRSN}_${compilerString}
 set EXEC     = BCON_${VRSN}.exe
 set EXEC_ID  = bcon
 cat $BLD/BCON_${VRSN}.cfg; echo " "; set echo

#> Horizontal grid definition
 setenv GRIDDESC $CMAQ_DATA/mcip/GRIDDESC #> grid description file
 setenv IOAPI_ISPH 20                     #> GCTP spheroid, use 20 for WRF-based modeling

#> I/O Controls
 setenv IOAPI_LOG_WRITE F     #> turn on excess WRITE3 logging [ options: T | F ]
 setenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]
 setenv EXECUTION_ID $EXEC    #> define the model execution id

# =====================================================================
#> BCON Configuration Options
#
# BCON can be run in one of two modes:
#     1) regrids CMAQ CTM concentration files (BC type = regrid)
#     2) use default profile inputs (BC type = profile)
# =====================================================================

 setenv BCON_TYPE ` echo $BCTYPE | tr "[A-Z]" "[a-z]" `

# =====================================================================
#> Input/Output Directories
# =====================================================================

 setenv OUTDIR  $CMAQ_HOME/$DMF/bcon       #> output file directory

set DATE  = `/usr/bin/ncdump -h $nc|grep SDATE|awk '{print $3}'`
set y = `echo $DATE|cut -c1-4`
set j = `echo $DATE|cut -c5-`
set NDAYS = 1

    set YYYYJJJ  = ${DATE}   #> Convert YYYY-MM-DD to YYYYJJJ
    set YYYYMMDD = `date -d "${y}-01-01 +${j}days -1days" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
    set YYMMDD   = `echo $YYYYMMDD|cut -c3-` #> Convert YYYY-MM-DD to YYMMDD

 setenv CTM_CONC_1 $nc
 setenv MET_CRO_3D_CRS $CMAQ_HOME/$DM/mcip/METCRO3D.nc
 setenv MET_BDY_3D_FIN $CMAQ_DATA/mcip/nc/METBDY3D.${YYYYMMDD}
 setenv BNDY_CONC_1    "$OUTDIR/BCON_${YYYYMMDD}_${GRID_NAME} -v"

# =====================================================================
#> Output File
# =====================================================================

#>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR
 if ( -e "$BNDY_CONC_1" ) rm $BNDY_CONC_1

 ls -l $BLD/$EXEC; size $BLD/$EXEC
 #unlimit
 #limit

#> Executable call:
 time $BLD/$EXEC

 exit()
(pyn_env)

```