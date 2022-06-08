---
layout: default
title: CALINE4 I/O
parent: CALINE
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2022-04-08 15:30:32
---
# *CALINE4*的標準輸入及3/4版轉換
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
- *CALINE4*並未列在USEPA的網站中，CALtran似乎也已經下架，但[EAST Lab -  University of Michigan](http://www-personal.umich.edu/~weberg/caline4.htm)還有一份可以下載(32bit執行檔)，[此處](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/caline4.zip)為壓縮檔。
  - 圖形界面尚可運用(64位元PC)，可用於輸入、檢視、及儲存（.dat自由格式詳下），主程式無法作動，需將.dat轉至CALINE3執行。

## *CALINE4* 輸入檔範例
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
## 轉換程式
- 界面程式CL4結果.dat檔案，原本是為輸入*CALINE4*，但因該程式無法在64位元電腦執行，只能使用*CALINE3*來執行，過程需轉換格式。
- python程式可由github.io下載（[rd_dat.py](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/rd_dat.py)）
  - 依照前述段落順序、依序讀取模式各項變數
  - NR、NL、NM必須轉成整數
  - 需注意*CALINE3*/4版間的定義差異（詳下述）

### 執行方式

```bash
#.dat轉成.INP
python rd_dat.py central_campus.dat

#執行CALINE3
../CALINE3/caline3 <central_campus3.INP >central_campus3.OUT 
```

### 3、4版CALINE輸入的差異

||CALINE3|CALINE4|
|-|-|-|
|ATIM|min|hour|
|TYP|AG,DP,FL,BR|1~4|
|CLAS|1~6|1~7|

### code listing

```python
import numpy as np
import fortranformat as ff
import sys

fnameI=sys.argv[1]
fnameO=fnameI.replace('.dat','3.INP')
with open(fnameI,'r') as f:
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
dtyp={1:'AG',2:'DP',3:'FL',4:'BR'}
TYP=[dtyp[int(i)] for i in TYP] #change int to A2
ATIM*=60. #change hour to min
run=lines[iend]
VPH=[float(i) for i in lines[iend+1].split()]
EMF=[float(i) for i in lines[iend+2].split()]
for var in 'U,BRG,CLAS,MIXH,SIGM,AMB,T'.split(','):
  exec(var+'=np.zeros(shape=NM)')
istr=iend+3
iend=istr+NM
for i in range(NM):
  BRG[i],U[i],CLAS[i],MIXH[i],SIGM[i],AMB[i],T[i]=[float(j) for j in lines[istr+i].split()]
CLAS=[min([6,i]) for i in CLAS]

#1:SITE VARIABLES, 2:RECEPTOR LOCATIONS, 3:RUN CASE, 4:LINK VARIABLES, 5:MET CONDITIONS
fmt=['A40,2F4.0,2F5.0,I2,F10.0','A12,8X,3F10.0',  'A40,2I3',  'A8,12X,A2,4F7.0,F8.0,3F4.0',      'F3.0,F4.0,I1,F6.0,F4.0']
var=[(job,ATIM,z0,vs,vd,NR,SCAL),(recp,xr,yr,zr),(run,NL,NM),(lnks,TYP,X1,Y1,X2,Y2,VPH,EMF,H,W),(U,BRG,CLAS,MIXH,AMB)]
nln=[1,NR,1,NL,NM]
lns=[]
for ig in range(5):
  w_line = ff.FortranRecordWriter(fmt[ig])
  if ig in [0,2]:
    lns.append(w_line.write([v for v in var[ig]])+'\n')
  else:
    for l in range(nln[ig]):
      lns.append(w_line.write([v[l] for v in var[ig]])+'\n')
with open(fnameO,'w') as f:
  for l in lns:
    f.write(l)
```

## *CALINE3* 執行CL4 .dat之結果範例
```
$ cat central_campus3.OUT
1                     CALINE3              (DATED 12317)
0                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  1


      JOB:                           Central Campus             RUN:                        31101Hour 1      



        I.  SITE VARIABLES


       U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
     BRG =   0. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  3.0 PPM



       II.  LINK VARIABLES


        LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                             *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
    -------------------------*--------------------------------*-------------------------------------------------------
    A. Fuller                *    347.   1896.    860.   1662.*      564.      115.      AG   2995.  10.0   0.0  16.0
    B. State                 *    464.   1820.    439.    396.*     1424.      181.      AG    481.  10.0   0.0  16.0
    C. Catherin              *    461.   1460.    977.   1460.*      516.       90.      AG    776.  10.0   0.0  16.0
    D. Ann                   *    458.   1370.   1151.   1375.*      693.       90.      AG    330.  10.0   0.0  16.0
    E. Huron                 *    456.   1272.    977.   1288.*      521.       88.      AG   1025.  10.0   0.0  16.0
    F. Washingt              *    456.   1192.    712.   1192.*      256.       90.      AG    515.  10.0   0.0  16.0
    G. N. Unive              *    456.   1031.    794.   1031.*      338.       90.      AG    523.  10.0   0.0  16.0
    H. Washtena              *    794.   1031.   1509.    254.*     1056.      137.      AG   1835.  10.0   0.0  16.0
    I. S. Unive              *    450.    690.   1479.    682.*     1029.       90.      AG    436.  10.0   0.0  16.0
    J. Hill                  *    439.    396.   1345.    428.*      907.       88.      AG    963.  10.0   0.0  16.0
    K. Fletcher              *    709.   1277.    709.   1031.*      246.      180.      AG    801.  10.0   0.0  16.0
    L. E. Unive              *    794.    685.    794.    232.*      453.      180.      AG    653.   0.0   0.0  16.0
    M. Church                *    890.    928.    884.    232.*      696.      180.      AG    700.   0.0   0.0  16.0
    N. S. Fores              *    971.    235.    977.   1460.*     1225.        0.      AG    647.   0.0   0.0  16.0
    O. Observat              *   1151.   1375.   1149.    898.*      477.      180.      AG   1059.   0.0   0.0  16.0
    P. Geddes                *   1149.    898.   1487.    767.*      362.      111.      AG    823.   0.0   0.0  16.0
    Q. E. Med.               *   1149.   1285.   1460.   1288.*      311.       89.      AG   1080.   0.0   0.0  16.0
    R. Glen-Sec              *    832.   1460.    860.   1662.*      204.        8.      AG   1325.   0.0   0.0  16.0
    S. Glen-Sec              *    860.   1662.   1051.   1765.*      217.       62.      AG   1325.   0.0   0.0  16.0
    T. Oxford                *   1487.    761.   1449.    317.*      446.      185.      AG    413.   0.0   0.0  16.0
```
```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  2


      JOB:                           Central Campus             RUN:                        31101Hour 1      



        I.  SITE VARIABLES


       U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
     BRG =   0. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  3.0 PPM





      III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                             *                               *  TOTAL
                             *        COORDINATES (M)        *  + AMB
        RECEPTOR             *      X        Y        Z      *  (PPM)
    -------------------------*-------------------------------*--------
     1.     Universi         *     1296.    1555.      2.0   *   3.0
     2.     Kresge           *     1045.    1394.      2.0   *   3.0
     3.     Frieze           *      508.    1206.      2.0   *   3.3
     4.     Rackham          *      639.    1209.      2.0   *   3.3
     5.     Power Pl         *      911.    1192.      2.0   *   3.1
     6.     Mary Mar         *     1302.    1201.      2.0   *   3.0
     7.     Hill Aud         *      578.    1045.      2.0   *   3.2
     8.     Dental S         *      786.    1067.      2.0   *   3.2
     9.     Mosher J         *     1130.    1100.      2.0   *   3.0
    10.     Angell H         *      513.     827.      2.0   *   3.2
    11.     CC Littl         *      827.     876.      2.0   *   3.4
    12.     West Hal         *      778.     715.      2.0   *   3.1
    13.     East Hal         *      843.     720.      2.0   *   3.3
    14.     Michigan         *      387.     674.      2.0   *   3.1
    15.     Social W         *      761.     608.      2.0   *   3.2
    16.     Law Quad         *      548.     630.      2.0   *   3.2
    17.     Buisines         *      668.     461.      2.0   *   3.1
    18.     East Qua         *      851.     472.      2.0   *   3.2
    19.     Trotter          *     1228.     614.      2.0   *   3.1
    20.     Wallace          *     1473.     619.      2.0   *   3.0
```
```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  3


      JOB:                           Central Campus             RUN:                        31101Hour 1      



        I.  SITE VARIABLES


       U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
     BRG =   0. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  3.0 PPM





       IV.  MODEL RESULTS (RECEPTOR-LINK MATRIX)


                             *
+                                                                           CO/LINK
                             *                                               (PPM)
        RECEPTOR             *   A    B    C    D    E    F    G    H    I    J    K    L    M    N    O    P    Q    R    S    T
    -------------------------*
+                             ------------------------------------------------------------------------------------------------------
     1.     Universi         *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     2.     Kresge           *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     3.     Frieze           *  0.1  0.0  0.1  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     4.     Rackham          *  0.1  0.0  0.1  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     5.     Power Pl         *  0.0  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     6.     Mary Mar         *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     7.     Hill Aud         *  0.1  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     8.     Dental S         *  0.1  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
     9.     Mosher J         *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    10.     Angell H         *  0.1  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    11.     CC Littl         *  0.1  0.0  0.0  0.0  0.1  0.0  0.0  0.2  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    12.     West Hal         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    13.     East Hal         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.2  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    14.     Michigan         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    15.     Social W         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    16.     Law Quad         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    17.     Buisines         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    18.     East Qua         *  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    19.     Trotter          *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
    20.     Wallace          *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0
(base) 
```