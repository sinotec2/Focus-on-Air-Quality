---
layout: default
title: CALPUFF結果轉nc檔
nav_order: 3
parent: CALPOST
grand_parent: Trajectory Models
last_modified_date: 2022-06-07 11:56:20
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
- 基本上，本程式是在[con2avrg]()之後，再進一步呼叫[pncgen]()將[uamiv]()檔案轉成nc檔案。

## 呼叫pncgen
- 使用`system`內函數

```fortran
 2503       call system('/usr/kbin/pnc_congrd02')
```
### pnc_congrd02
- 詳見
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


