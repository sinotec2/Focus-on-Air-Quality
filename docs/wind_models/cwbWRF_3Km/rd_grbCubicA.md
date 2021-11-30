---
layout: default
title: "grb2nc轉檔"
parent: "cwb WRF_3Km"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-30 10:43:16
---

# grb2nc轉檔

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
- 續[樓上](https://sinotec2.github.io/jtd/docs/wind_models/cwbWRF_3Km/)、以及[下載](https://sinotec2.github.io/jtd/docs/wind_models/cwbWRF_3Km/get_M-A0064/)程序之說明，此處詳述轉檔歷程。
- 雖然`grb2`格式也有其解讀、應用的軟體，然而在空氣污染領域還並不多。因此還是需要轉成`wrfout`的`nc`格式。
- 此處應用pygrib模組進行`grb2`檔案的解析

## rd_grbCubicA.py分段說明
- 引用模組
  - pygrib的建置比較特別，
```python
kuang@MiniWei /Users/Data/cwb/WRF_3Km
$ cat -n rd_grbCubicA.py
     1  #!/opt/anaconda3/envs/gribby/bin/python
     2  import pygrib
     3  import numpy as np
     4  import netCDF4
     5  from scipy.io import FortranFile
     6  from scipy.interpolate import CubicSpline
     7  from scipy.interpolate import interp1d
     8  import datetime
     9  import os
    10  import subprocess
    11
```
-
```python
    12  def buck(K):
    13      C=K-273.
    14      return 611.21*np.exp((18.678-C/234.5)*C/(257.14+C))
    15
    16
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


## 檢核
- 檔案個數大小：每層共**15個檔**(84/6+1)，3Km檔案共約**2.8G**，15Km檔案共約**0.8G**。
```bash
kuang@MiniWei /Users/Data/cwb/WRF_3Km/2021/20211129
$ ls M-A0064-0??.grb2|wc -l
      15
kuang@MiniWei /Users/Data/cwb/WRF_3Km/2021/20211129
$ du -ach M-A0064-0??.grb2|tail -n1
2.8G    total
kuang@MiniWei /Users/Data/cwb/WRF_3Km/2021/20211129
$ du -ach M-A0061-0??.grb2|tail -n1
878M    total
```

## Reference
