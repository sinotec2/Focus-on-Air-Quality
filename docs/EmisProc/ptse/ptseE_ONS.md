---
layout: default
title: "TimVar for Elevated PTS"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 2
date:               
last_modified_date:   2021-12-03 09:54:07
---

# 高空點源之時變係數
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
- 高空點源的**時變係數**骨幹是CEMS數據，然而同一工廠無數據、鄰近工業區其他廠無數據者，亦會參考CEMS設定其**時變係數**。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式

## 程式說明

- 引用模組
  - 程式用到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式`CORRECT`, `add_PMS`, `check_nan`, `check_landsea`, `FillNan`, `WGS_TWD`, `Elev_YPM`

```python
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n ptseE_ONS.py
     1
     2  #! crding = utf8
     3  from pandas import *
     4  import numpy as np
     5  import os, sys, subprocess
     6  import netCDF4
     7  import twd97
     8  import datetime
     9  from calendar import monthrange
    10  from scipy.io import FortranFile
    11
    12  from ptse_sub import CORRECT, add_PMS, check_nan, check_landsea, FillNan, WGS_TWD, Elev_YPM
    13
```
- 檔案讀取與品質確認
  - 此個案將所有點源資料庫的數據都以「高空」方式處理(cutting height of stacks`Hs=0`)

```python
    14  #Main
    15  hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
    16  P='./'
    17  Hs=0 #cutting height of stacks
    18  #Input the TEDS csv file
    19  try:
    20    df = read_csv('point.csv', encoding='utf8')
    21  except:
    22    df = read_csv('point.csv')
    23  # check_NOPandSCC(0)
    24  df = check_nan(df)
    25  # check and correct the X coordinates for isolated islands
    26  df = check_landsea(df)
    27  df = Elev_YPM(df)
```
- 使用`Hs`進行篩選「高空」點源
```python
    28  df=df.loc[(df.HEI>=Hs) & (df.NO_S.map(lambda x:x[0]=='P'))].reset_index(drop=True)
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python
```
- 
```python

## 檔案下載
- `python`程式：[prep_linegridLL.py](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/line/prep_linegridLL.py)。

## Reference
