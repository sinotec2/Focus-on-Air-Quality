---
layout: default
title: "Prepare for MobileS"
parent: "Mobile Sources"
grand_parent: "Emission Processing"
nav_order: 1
date:               
last_modified_date:   2021-12-02 11:08:53
---

# 移動源排放檔案之準備
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
- 由環保署移動源檔案讀取資料庫**索引維度**，排放量則改寫成矩陣形式。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[交通源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/line/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，為此處之前處理。  

## 程式分段說明

- 引用模組

```python
kuang@node03 /nas1/TEDS/teds11/line
$ cat -n prep_linegridLL.py
     1  import numpy as np
     2  from pandas import *
     3  import twd97
     4  from pyproj import Proj
     5  from scipy.io import FortranFile
     6
```
- 直角座標之中心點

```python
     7  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
     8  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
     9  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
    10          lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
    11
```
- 直角座標之中心點

```python
    12  df=read_csv('TEDS11_LINE_WGS84.csv')
    13  APOL=[i for i in df.columns if 'EM_' in i]
    14  APOL.sort()
    15  NPOL=len(APOL)
    16  LTYP=len(set(df.NSC_SUB))
    17  VTYPE=list(set(df.NSC))
    18  VTYPE.sort()
    19  NVTYP=len(VTYPE)
    20  iVTYP=np.array([VTYPE.index(i) for i in df.NSC],dtype=int)
    21
    22
```
- 計算每筆數據的直角座標值

```python
    23  lon,lat=np.array(df.WGS84_E),np.array(df.WGS84_N)
    24  x,y=pnyc(lon,lat, inverse=False)
    25  df['UTME']=x+Xcent
    26  df['UTMN']=y+Ycent
```
- 紀錄資料庫的**索引維度**

```python
    27  X=np.array([int(i/1000) for i in df.UTME],dtype=int)
    28  Y=np.array([int(i/1000) for i in df.UTMN],dtype=int)
    29  R=np.array(df.NSC_SUB,dtype=int)
    30  C=np.array([i//100 for i in df.DICT],dtype=int)
    31  XYRC=X*10000*10*100+Y*10*100+R*100+C
    32  df['XYRC']=XYRC
    33  DD={}
    34  for s in 'XYRC':
    35    exec('DD.update({"'+s+'":'+s+'})')
    36  kin=DataFrame(DD)
    37  kin.drop_duplicates(inplace=True)
    38  kin=kin.reset_index(drop=True)
    39  XYRCk=list(kin.X*10000*10*100+kin.Y*10*100+kin.R*100+kin.C)
    40  kin.set_index('X').to_csv('df_kin.csv')
```
- 針對相同座標、道路種類、鄉鎮區別，給定**筆數編號**(REC)值，再按REC與車種的組合進行加總，消除畸零座標之紀錄。

```python
    41  NREC=len(kin)
    42  df['REC']=-1
    43  for i in range(NREC):
    44    boo=df.XYRC==XYRCk[i]
    45    idx=df.loc[boo].index
    46    df.loc[idx,'REC']=i
    47  if len(df.loc[df.REC==-1]) !=0:sys.exit('wrong REC!')
    48  df['RECV']=np.array(df.REC,dtype=int)*100+iVTYP
    49  pv=pivot_table(df,index='RECV',values=APOL,aggfunc=sum).reset_index()
    50  pv.set_index('RECV').to_csv('TEDS11_LINE_WGS84_1Km.csv')
```
- 將橫式的資料庫型態，轉置成矩陣型態

```python
    51  pv['REC']=np.array(pv.RECV//100,dtype=int)
    52  pv['iVT']=np.array(pv.RECV%100,dtype=int)
    53  EM=np.zeros(shape=(NREC,NPOL,NVTYP))
    54  for i in range(NREC):
    55    boo=(pv.REC==i)
    56    EM[i,:,:]=np.array(pv.loc[boo,APOL]).T
```
- 儲存排放量矩陣備用

```python
    57  fname = 'cl08_'+'{:d}_{:d}_{:d}'.format(NREC,NPOL,NVTYP)+'.bin'
    58  with FortranFile(fname, 'w') as f:
    59    f.write_record(EM)
    60
```

## 檔案下載
- `python`程式：[prep_linegridLL.py](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/line/prep_linegridLL.py)。

## Reference
