---
layout: default
title: CALPUFF結果轉nc檔
nav_order: 3
parent: CALPOST
grand_parent: Trajectory Models
last_modified_date: 2022-06-07 11:56:20
tags: cpuff cpost
---

# CALPUFF模擬結果轉nc檔案
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
- 基本上，本程式是在[con2avrg](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2avrg/)之後，再進一步呼叫[pncgen](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pncgen/#pncgen)將[uamiv][uamiv]檔案轉成nc檔案。


[uamiv]: <https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式> "CAMx所有二進制 I / O文件的格式，乃是遵循早期UAM(城市空氣流域模型EPA，1990年）建立的慣例。 該二進制文件包含4筆不隨時間改變的表頭記錄，其後則為時間序列的數據記錄。詳見CAMx(UAM)的檔案格式"

## 呼叫pncgen
- 使用`system`內函數

```fortran
 2503       call system('/usr/kbin/pnc_congrd02')
```
### pnc_congrd02
- 詳見[utilities](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pncgen/#examples)的說明
- pncdump用法可以參考[utility->ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump/)

```bash
$ cat /usr/kbin/pnc_congrd02
PTH=/cluster/miniconda/envs/unresp/bin
PNCD=$PTH/pncdump
NSTEP=`$PNCD --head -f uamiv calpuff.con.S.grd02 |grep NSTEPS|grep \=|awkk 3|tail -n1`
$PTH/pncgen.py -f uamiv -a TSTEP,global,o,i,$NSTEP --from-conv=ioapi --to-conv=cf -O calpuff.con.S.grd02 calpuff.con.S.grd02.nc
$PTH/pncgen --out-format=uamiv -O calpuff.con.S.grd02.nc  calpuff.con.S.grd02
#rm calpuff.con.S.grd02.nc
$PTH/pncgen -f uamiv -O calpuff.con.S.grd02 calpuff.con.S.grd02.nc
```


