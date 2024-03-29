---
layout: default
title: choose10.py程式說明
nav_order: 3
parent: WRF三維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-16 10:30:54
tags: trajectory
---

# choose10.py程式說明

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

- 這支程式讀取[bt2.py](#bt2_DVP_py)所計算而得之軌跡點L.csv檔案，從中選取10個點，整理成合計(x,y)共20個維度之矩陣，以便進行後續的k_means分析。
- 因為座標值的有效位數太多，不適合用做叢集分析的對象，此處以D1_3Km網格系統作為離散化的架構，以提高計算的效率。
- 個別軌跡線進行處理(而不是併入叢集分析)的理由
  1. 搭配軌跡線平行計算
  2. 提供低解析度繪圖  
  3. 留存原高解析度之結果以供繪圖或機率分析

## 程式說明

### IO

- 輸入檔案：
  - tmplateD1_3km.nc：讀取網格設定，以簡化軌跡點
  - fnames.txt(檔案路徑名稱之listing)
- 輸出檔案：
  - *10.csv

### D1_3Km網格系統說明

- 此一網格系統是為繪製軌跡通過機率而設計的，範圍涵蓋原來d01範圍，但是解析度為3km。

```bash
#ncdump -h $nc|H
netcdf tmplateD1_3km {
dimensions:
        TSTEP = UNLIMITED ; // (1 currently)
        LAY = 1 ;
        ROW = 1539 ;
        COL = 1539 ;
        VAR = 223 ;
        DATE-TIME = 2 ;
#ncdump -h $nc|grep -e ORIG -e CELL
                :XORIG = -2389500 ;
                :YORIG = -2389500 ;
                :XCELL = 3000 ;
                :YCELL = 3000 ;
```

### 網格標籤之合併

- 因網格標籤(I,J)值很大，此處以公式計算其冪值，以便合併成一個整數。

```python
ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
tex=10**ex
...
df['JI']=[j*tex+i for i,j in zip(ix,iy)]
```

### 軌跡點的網格化

- 基本上叢集分析的對象是類別性質的物件，座標值的有效數字太多，幾乎沒有重疊的可能，因此要定義類別並不容易，計算上也會需要整併。
- 此處以3公里作為網格化的解析度，不但可以簡化計算，也可以拉近軌跡線之間的距離。

```python
x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
...
  x=np.array(df.TWD97_x)-Xcent
  y=np.array(df.TWD97_y)-Ycent
  ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
  iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
  df['JI']=[j*tex+i for i,j in zip(ix,iy)]  
```

- 整併

```python
...
  reduced_ji=[]
  for i in range(1,len(df)):
    if df.JI[i-1]!=df.JI[i]:
      reduced_ji.append(df.JI[i-1])
  df=DataFrame({'JI3':reduced_ji})
...
```

### 每10取1

```python
  if len(df)<10:continue
  ji10=[df.JI3[i] for i in range(0,len(df),int(len(df)/10))]
  df=DataFrame({'JI3':ji10[:10]})
  df.set_index('JI3').to_csv(fname+'10.csv')
```

## 程式下載

{% include download.html content="[軌跡叢集分析前處理程式choose10.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/choose10.py)" %}