---
layout: default
title: mcip結果初始小時值的延伸
parent: Met. Chem. Interface Proc.
grand_parent: CMAQ Model System
nav_order: 3
date: 2021-12-19 21:21:37
last_modified_date:  2023-03-21 19:49:43
tags: mcip CMAQ
---

# mcip結果初始小時值的延伸
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

- `mcip`與`wrfout`時間的解讀有所不同，會差1個小時。指定CMAQ模式自0時開始模擬，而同樣批次範圍內這個時間並沒有`wrfout`的模擬結果。
- 此處並沒有自前批次結果的最後小時讀取，乃以本批次頭一小時替代，以降低模式初始化的衝擊。
- 影響到的檔案：
  - 沒有時間序列的檔案：`GRIDBDY2D`、`GRIDCRO2D`、`GRIDDOT2D`、`LUFRAC_CRO`
  - 具有時間維度的檔案：`METBDY3D`、`METCRO2D`、`METCRO3D`、`METDOT3D`、`SOI_CRO`。

## 腳本與程式

### 執行腳本

- 對那些沒有時間序列的檔案
  - 直接將起算時間更改為0時(00Z),執行`add_firstHr.py`
- 具有時間維度的檔案
  - 先用[ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)切割出第一小時(01Z)的片段檔案
  - 將片段時間更改為0時(00Z)
  - 用`ncrcat`將檔案按照時間連起來，覆蓋原來檔案

```bash
#!/bin/bash
for i in $(ls [GL]*.nc);do python ~/bin/add_firstHr.py ${i};done
for i in $(ls [MS]*.nc);do ncks -O -d TSTEP,0,0 $i ${i}_1; python ~/bin/add_firstHr.py ${i}_1;ncrcat -O ${i}_1 ${i} a;mv a ${i};rm ${i}_1;done
```

### add_firstHr.py

```python
import netCDF4
import sys
fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r+')
nc.variables['TFLAG'][0,:,1]=[0 for i in range(nc.NVARS)]
nc.STIME=0
nc.close()
```

### all_in_one version

- 在csh腳本中使用bash腳本是一件很尷尬的事情，比較好的方式是包裝在python程式內。
- 以下版本是在國網上運作的方案

```python
#!/opt/ohpc/pkg/rcec/pkg/python/wrfpost/bin/python
import netCDF4
import sys,os
fname=sys.argv[1]
fnameO=fname+'_1'
nc = netCDF4.Dataset(fname,'r')
if nc.variables['TFLAG'][0,0,1]==0:sys.exit()
nc.close()
os.system('/work/sinotec2/opt/cmaq_recommend/bin/ncks -O -d TSTEP,0,0 '+fname+' '+fnameO)
nc = netCDF4.Dataset(fnameO,'r+')
nc.variables['TFLAG'][0,:,1]=[0 for i in range(nc.NVARS)]
nc.STIME=0
nc.close()
os.system('/work/sinotec2/opt/cmaq_recommend/bin/ncrcat -O '+fnameO+' '+fname+' a;rm -f '+fnameO+';mv a '+fname)
```