---
layout: default
title: "EPs Emis for CAMx"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 3
date:               
last_modified_date:   2021-12-06 12:09:47
---

# CAMx高空點源排放檔案之產生
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
- 此處處理TEDS PM/VOCs年排放量之劃分、與時變係數相乘、整併到光化模式網格系統內。
- 高空點源的**時變係數**檔案需按CEMS數據先行[展開](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptseE_ONS/)。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式

## 副程式說明

### [ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)

### 對煙道座標進行叢集整併
如題所示。整併的理由有幾：
- 鄰近煙流在近距離重疊後，會因整體煙流熱量的提升而提升其最終煙流高度，從而降低對地面的影響，此一現象並未在模式的煙流次網格模式中予以考量，須在模式外先行處理。
- 重複計算較小煙流對濃度沒有太大的影響，卻耗費大量儲存、處理的電腦資源，因此整併有其必須性。
  - 即使將較小的點源按高度切割併入面源，還是保留此一機制，以避免點源個數無限制擴張，有可能放大因品質不佳造成奇異性。

#### cluster_xy
- 調用`sklearn`之`KMeans`來做叢集分析

```python
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n cluster_xy.py
     1
     2
     3  def cluster_xy(df,C_NO):
     4    from sklearn.cluster import KMeans
     5    from pandas import DataFrame
     6    import numpy as np
     7    import sys
     8
```
- 由資料庫中選擇同一**管編**之煙道出來

```python
     9    b=df.loc[df.CP_NO.map(lambda x:x[:8]==C_NO)]
    10    n=len(b)
    11    if n==0:sys.exit('fail filtering of '+C_NO)
    12    colb=b.columns
```
- 此**管編**所有煙道的座標及高度，整併為一個大矩陣
  - 進行KMeans叢集分析

```python
    13    x=[b.XY[i][0] for i in b.index]
    14    y=[b.XY[i][1] for i in b.index]
    15    z=b.HEI
    16    M=np.array([x, y, z]).T
    17    clt = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300, \
    18         n_clusters=10, n_init=10, n_jobs=-1, precompute_distances='auto', \
    19         random_state=None, tol=0.0001, verbose=0)
    20    kmeans=clt.fit(M)
```
- 放棄原來的座標，改採叢集的平均位置

```python
    21  #  np.array(clt.cluster_centers_) for group
    22    b_lab=np.array(clt.labels_)
    23    df.loc[b.index,'UTM_E']=[np.array(clt.cluster_centers_)[i][0] for i in b_lab]
    24    df.loc[b.index,'UTM_N']=[np.array(clt.cluster_centers_)[i][1] for i in b_lab]
    25    return df
    26
```
#### XY_pivot
- 工廠點源個數太多者(如中鋼)，在座標叢集化之前，以pivot_tab取其管道(**管煙**編號)排放量之加總值
  - 調用模組

```python   
    27  #XY clustering in CSC before pivotting
    28  #df=cluster_xy(df,'E5600841')
    29  #pivotting
    30  def XY_pivot(df,col_id,col_em,col_mn,col_mx):
    31    from pandas import pivot_table,merge
    32    import numpy as np
```
- 3類不同屬性欄位適用不同的`aggfunc`
  - 排放量(`col_em`)：加總
  - 煙道高度(`col_mx`)：最大值
  - 煙道其他參數(`col_mn`)：平均

```python   
    33    df_pv1=pivot_table(df,index=col_id,values=col_em,aggfunc=np.sum).reset_index()
    34    df_pv2=pivot_table(df,index=col_id,values=col_mn,aggfunc=np.mean).reset_index()
    35    df_pv3=pivot_table(df,index=col_id,values=col_mx,aggfunc=max).reset_index()
```
- 整併、求取等似直徑、以使流量能守恒
```python   
    36    df1=merge(df_pv1,df_pv2,on=col_id)
    37    df=merge(df1,df_pv3,on=col_id)
    38    df['DIA']=[np.sqrt(4/3.14159*q/60*(t+273)/273/v) for q,t,v in zip(df.ORI_QU1,df.TEMP,df.VEL)]
    39    return df
```

## 主程式說明

### 程式之執行
- 此處按月執行。由於nc檔案時間展開後，檔案延長非常緩慢，拆分成主程式（`ptseE.py`）與輸出程式（`wrtE.py`）二段進行。
```bash
for m in 0{1..9} 1{0..2};do python ptseE.py $m;done
for m in 0{1..9} 1{0..2};do python python wrtE.py $m;done
```

###
- 調用模組
  - 因無另存處理過後的資料庫，因此程式還是會用到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式`CORRECT`, `add_PMS`, `check_nan`, `check_landsea`, `FillNan`, `WGS_TWD`, `Elev_YPM`

```python   
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n ptseE.py
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
    12  from mostfreqword import mostfreqword
    13  from ptse_sub import CORRECT, add_PMS, check_nan, check_landsea, FillNan, WGS_TWD, Elev_YPM
    14  from ioapi_dates import jul2dt, dt2jul
    15  from cluster_xy import cluster_xy, XY_pivot
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

### 輸出結果 

-
```python   
```


## 檔案下載
- `python`程式：[ptseE_ONS.py](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/ptse/ptseE_ONS.py)。
- `jupyter-notebook`檔案[ptseE_ONS.ipynb](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/ptse/ptseE_ONS.ipynb)

## Reference
