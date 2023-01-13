---
layout: default
title: 逐日循序執行bcon.exe
parent: Boundary Condition
grand_parent: CMAQ Model System
nav_order: 7
date: 2022-08-25 12:11:42
last_modified_date: 2022-10-13 22:52:07
tags: CMAQ BCON forecast
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
### 策略面之考量
- 大型、多層網格、連日的CMAQ執行結果，要接續執行bcon.exe會遭遇到龐大濃度檔(ACONC)的問題。雖然如[大型網格系統切割邊界濃度](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/hd_bc)文中所述，可以python程式來執行內插與切割，但仍然不夠快速、簡潔。
- 由於CMAQ結果是逐日輸出，因此發展逐日執行bcon.exe還是比較合理的作法，唯一的困難，是bcon程式內設會從METBDY3D讀取相對應的起始時間，會需要：
  1. 將執行批次的METBDY3D檔案切割成逐日
  2. 逐日METBDY3D檔案的SDATE需配合ACONC濃度檔案的內容。
- 前述2項作業在[brk_day2.cs](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/brk_day)中已經妥善處理好了，只需執行即可(還好METBDY3D檔案並不太大，即使重複儲存也還能容忍)。
- 此一策略對[逐日CMAQ預報系統](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ForecastSystem/)中減省檔案容量有非常重要的關鍵性角色。

### 腳本之執行批次（[fcst.cs][fcst.cs]）
- 雖然bcon.exe也可以同步執行，但因速度還可以接受，此處就循序進行，
- 最後用ncrcat將其連成一個大檔，還要加上最後一個小時值的bc就完成了。

```bash
...
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
...
```

- {% include download.html content="逐日WRF及CMAQ預報之執行腳本[fcst.cs][fcst.cs]" %}

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
### 日期的辨識與應用
- 由輸入之CCTM_ACONC檔案中以ncdump讀取，不需要從別處取得資訊。
- Julian day轉成日曆天：使用`date`指令計算。
- y, j分別為年代及julian day

```bash
set nc         = $argv[1]
...
set DATE  = `/usr/bin/ncdump -h $nc|grep SDATE|awk '{print $3}'`
set y = `echo $DATE|cut -c1-4`
set j = `echo $DATE|cut -c5-`
set NDAYS = 1

    set YYYYJJJ  = ${DATE}   #> Convert YYYY-MM-DD to YYYYJJJ
    set YYYYMMDD = `date -d "${y}-01-01 +${j}days -1days" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
    set YYMMDD   = `echo $YYYYMMDD|cut -c3-` #> Convert YYYY-MM-DD to YYMMDD
```

### 檔名的設定
- 應用前述計算出來的日期，找到對應的MET_BDY_3D_FIN檔案
- 設定輸出檔名，以便後續處理(ncrcat連結)

```bash
 setenv CTM_CONC_1 $nc
 setenv MET_CRO_3D_CRS $CMAQ_HOME/$DM/mcip/METCRO3D.nc
 setenv MET_BDY_3D_FIN $CMAQ_DATA/mcip/nc/METBDY3D.${YYYYMMDD}
 setenv BNDY_CONC_1    "$OUTDIR/BCON_${YYYYMMDD}_${GRID_NAME} -v"
```

## 腳本下載點

- {% include download.html content="逐日循序執行bcon.exe腳本[run_bcon_NC.csh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/ForecastSystem/run_bcon_NC.csh)" %}


[fcst.cs]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/ForecastSystem/fcstcs.txt> "逐日WRF及CMAQ預報之執行腳本"