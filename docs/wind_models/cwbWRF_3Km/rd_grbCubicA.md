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
  - pygrib的建置比較特別，可以參考[pygrib的安裝、重要語法](http://www.evernote.com/l/AH12nyLrGkBL2qg3WTonSwDC-0Rtq_S9npA/)
  - 其餘時間內插使用到CubicSpline，空間內差使用到interp1d
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
- 溫濕度轉換
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
- 可以使用MeteoInfo(*)或[CWB網站](https://npd.cwb.gov.tw/NPD/products_display/product?menu_index=1)

## Reference
- sinotec2, **pygrib的安裝、重要語法**, [evernote](http://www.evernote.com/l/AH12nyLrGkBL2qg3WTonSwDC-0Rtq_S9npA/), 2021年4月1日