---
layout: default
title: CALINE4 I/O
parent: CALINE
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2022-04-08 15:30:32
---
# CALINE3的標準輸入輸出
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
- CALINE4並未列在USEPA的網站中，CALtran似乎也已經下架，但[EAST Lab -  University of Michigan](http://www-personal.umich.edu/~weberg/caline4.htm)還有一份可以下載(32bit執行檔)，[此處](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/caline4.zip)為壓縮檔。
  - 圖形界面尚可運用，可用於輸入、檢視、及儲存（.dat自由格式詳下），主程式無法作動，需將.dat轉至CALINE3執行。

## CALINE4 輸入檔範例
- 專案名稱
- 污染物
- z0(cm)、分子量、Vs、Vd、NR、NL、平均時間(小時)、座標轉換係數、氣象個案數、ASL(m)

```bash
Central Campus
1Carbon Monoxide
100.0 28.0 0.0 0.0 20 20 1.0 1 1 0.0
```
- 20個接受點的名稱

```bash
Universi
Kresge
Frieze
Rackham
Power Pl
Mary Mar
Hill Aud
Dental S
Mosher J
Angell H
CC Littl
West Hal
East Hal
Michigan
Social W
Law Quad
Buisines
East Qua
Trotter
Wallace
```
- 20個接受點的座標(X、Y、Z)

```bash
1296.0 1555.0 1.8
1045.0 1394.0 1.8
508.0 1206.0 1.8
639.0 1209.0 1.8
911.0 1192.0 1.8
1302.0 1201.0 1.8
578.0 1045.0 1.8
786.0 1067.0 1.8
1130.0 1100.0 1.8
513.0 827.0 1.8
827.0 876.0 1.8
778.0 715.0 1.8
843.0 720.0 1.8
387.0 674.0 1.8
761.0 608.0 1.8
548.0 630.0 1.8
668.0 461.0 1.8
851.0 472.0 1.8
1228.0 614.0 1.8
1473.0 619.0 1.8
```
- 20個路段的名稱

```bash
Fuller
State
Catherine
Ann
Huron
Washington
N. Universit
Washtenaw
S. Universit
Hill
Fletcher
E. Universit
Church
S. Forest
Observatory
Geddes
E. Med. Cent
Glen-Sec. 1
Glen-Sec. 2
Oxford
```
- 20個路段的路形(1\~4)、端點X、Y、link Hgt高度、混合區寬度、Canyon/Bluff Mixing left、right（峽谷、斷崖）

```bash
1 347.0 1896.0 860.0 1662.0 0.0 16.0 0.0 0.0 0
1 464.0 1820.0 439.0 396.0 0.0 16.0 0.0 0.0 0
1 461.0 1460.0 977.0 1460.0 0.0 16.0 0.0 0.0 0
1 458.0 1370.0 1151.0 1375.0 0.0 16.0 0.0 0.0 0
1 456.0 1272.0 977.0 1288.0 0.0 16.0 0.0 0.0 0
1 456.0 1192.0 712.0 1192.0 0.0 16.0 0.0 0.0 0
1 456.0 1031.0 794.0 1031.0 0.0 16.0 0.0 0.0 0
1 794.0 1031.0 1509.0 254.0 0.0 16.0 0.0 0.0 0
1 450.0 690.0 1479.0 682.0 0.0 16.0 0.0 0.0 0
1 439.0 396.0 1345.0 428.0 0.0 16.0 0.0 0.0 0
1 709.0 1277.0 709.0 1031.0 0.0 16.0 0.0 0.0 0
1 794.0 685.0 794.0 232.0 0.0 16.0 0.0 0.0 0
1 890.0 928.0 884.0 232.0 0.0 16.0 0.0 0.0 0
1 971.0 235.0 977.0 1460.0 0.0 16.0 0.0 0.0 0
1 1151.0 1375.0 1149.0 898.0 0.0 16.0 0.0 0.0 0
1 1149.0 898.0 1487.0 767.0 0.0 16.0 0.0 0.0 0
1 1149.0 1285.0 1460.0 1288.0 0.0 16.0 0.0 0.0 0
1 832.0 1460.0 860.0 1662.0 0.0 16.0 0.0 0.0 0
1 860.0 1662.0 1051.0 1765.0 0.0 16.0 0.0 0.0 0
1 1487.0 761.0 1449.0 317.0 0.0 16.0 0.0 0.0 0
```
- 批次名稱
- 20個VPH、20個EMF(g/mile)
- 氣象訊息：風向(度)、風速(m/s)、穩定度(1\~7)、混合層(m)、風向標準偏差(度)、背景濃度(ppm)、氣溫(度C)

```bash
31101Hour 1
2995.0 481.0 776.0 330.0 1025.0 515.0 523.0 1835.0 436.0 963.0 801.0 653.0 700.0 647.0 1059.0 823.0 1080.0 1325.0 1325.0 413.0
10.0 10.0 10.0 10.0 10.0 10.0 10.0 10.0 10.0 10.0 10.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
0.0 1.0 7 1000.0 15.0 3.0 0.0
```
## 讀取程式
- 讀取界面結果.dat檔案的python程式[rd_dat.py](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/rd_dat.py)
  - 依照前述段落順序、依序讀取模式各項變數
  - NR、NL、NM必須轉成整數

```python
import numpy as np
with open('central_campus.dat','r') as f:
    lines=[i.strip('\n') for i in f]
job=lines[0].strip(' ')
z0,mw,vs,vd,NR,NL,ATIM,SCAL,NM,ASL=[float(i) for i in lines[2].split()]
NR,NL,NM=[int(i) for i in [NR,NL,NM]]
recp=[lines[i] for i in range(3,NR+3)]
xr,yr,zr=np.zeros(shape=NR),np.zeros(shape=NR),np.zeros(shape=NR)
for i in range(NR):
    xr[i],yr[i],zr[i]=[float(j) for j in lines[3+NR+i].split()]
lnks=[lines[i] for i in range(NR*2+3,NR*2+3+NL)]
for var in 'X1,Y1,X2,Y2,H,W,CBMl,CBMr,D'.split(','):
    exec(var+'=np.zeros(shape=NL)')
istr=NR*2+3+NL
iend=istr+NL
for var in 'TYP,X1,Y1,X2,Y2,H,W,CBMl,CBMr,D'.split(','):
    exec(var+'=np.zeros(shape=NL)')
for i in range(NL):
    TYP[i],X1[i],Y1[i],X2[i],Y2[i],H[i],W[i],CBMl[i],CBMr[i],D[i]=[float(j) for j in lines[istr+i].split()]
run=lines[iend]
VPH=[float(i) for i in lines[iend+1].split()]
EMF=[float(i) for i in lines[iend+2].split()]
for var in 'U,BRG,CLAS,MIXH,SIGM,AMB,T'.split(','):
    exec(var+'=np.zeros(shape=NM)')
istr=iend+3
iend=istr+NM
for i in range(NM):
    U[i],BRG[i],CLAS[i],MIXH[i],SIGM[i],AMB[i],T[i]=[float(j) for j in lines[istr+i].split()]
```