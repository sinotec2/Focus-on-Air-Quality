---
layout: default
title: "Monthly Breakdown"
parent: "Biogenic Sources"
grand_parent: TEDS Python
nav_order: 1
date:               
last_modified_date:   2021-12-02 11:08:53
---

# 植物排放量之逐月變化
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
- 環保署全年排放量乘上月變化係數
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/#處理程序總綱)、針對[植物源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/biog/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，為此處之前處理。  

## 程式分段說明
- 說明與宣告

```fortran
kuang@node03 /nas1/TEDS/teds11/merg/bioemis.space
$ cat -n bio2month-teds11.f
     1        program bio2month
     2
     3  C     read teds bio data and transfer to 1~12 month
     4  C     檔名areabio01~areabio12 為1～12月
     5  C     欄位1-3   UTME座標(km),I3
     6  C     欄位4     空白
     7  C     欄位5-8   UTMN座標(km),I4
     8  C     欄位9     空白
     9  C     欄位10-19 isoprene當月份該網格排放總量(kg/month),F10.3
    10  C     欄位20    空白
    11  C     欄位21-30 monoterpene當月份該網格排放總量(kg/month),F10.3
    12  C     欄位31    空白
    13  C     欄位32-41 otherVOCs當月份該網格排放總量(kg/month),F10.3
    14  C     欄位42    空白
    15  C     欄位43-52 MBO當月份該網格排放總量(kg/month),F10.3
    16
    17        integer m,utme,utmn
    18        real iso,mono,onmhc,mbo
    19        real miso(12),mmono(12),monmhc(12),mmbo(12),mtnmhc(12) !各月數值
    20        real piso(13),pmono(13),ponmhc(13),pmbo(13) !比例(12個月及全年)
    21        character mm*2
```
- 各月份時變化係數
```fortran
    22  C     各月份比例可參考生物源技術手冊
    23
    24        data piso /0.42,0.66,0.95,1.02,1.69,2.24,
    25       +           2.39,2.18,1.79,1.21,0.68,0.35,15.58/
    26        data pmono /0.64,0.79,1.01,1.12,1.56,1.84,
    27       +            1.89,1.94,1.65,1.26,0.95,0.62,15.27/
    28        data ponmhc /0.66,0.78,0.97,1.08,1.47,1.68,
    29       +             1.71,1.79,1.54,1.22,0.96,0.65,14.51/
    30        data pmbo /0.01,0.02,0.03,0.03,0.05,0.07,
    31       +           0.08,0.07,0.06,0.04,0.02,0.01,0.49/
    32
```
- 開啟新、舊檔案

```fortran
    33        do m=1,12
    34          write(mm,'(I2.2)')m
    35          open(20+m,file='bioemis.space.'//mm,status='unknown')
    36        enddo
    37        open(13,file='teds11_bio_twd97.csv',status='old')
    38        read(13,*)
    39
```
- 逐月進行相乘、輸出結果

```fortran
    40        do while(.true.)
    41           read(13,*,end=100) utme,utmn,tnmhc,iso,mono,onmhc,mbo
    42           do m=1,12
    43             miso(m)=iso*piso(m)/piso(13)*1000. !乘上該月份比例,單位換算kg
    44             mmono(m)=mono*pmono(m)/pmono(13)*1000.
    45             monmhc(m)=onmhc*ponmhc(m)/ponmhc(13)*1000.
    46             mmbo(m)=mbo*pmbo(m)/pmbo(13)*1000.
    47             mtnmhc(m)=miso(m)+mmono(m)+monmhc(m)
    48             write(m+20,60) utme,utmn,mtnmhc(m),miso(m),mmono(m),monmhc(m),mmbo(m)
    49  60         format(T2,I6,T9,I7,T17,5F10.3)
    50           enddo
    51        enddo
    52  100   continue
    53
    54        do m=1,12
    55          close(20+m)
    56        enddo
    57        stop
    58        end
```

## DataFrame整合
- 將逐月檔整合成一個大的DataFrame(`biogrid2019.csv`)、另存備用。

```python
kuang@node03 /nas1/TEDS/teds11/biog
$ cat wrt_csv.py
from pandas import *

P='/nas1/TEDS/teds11/merg/bioemis.space/'
col=['UTME','UTMN','tnmhc','iso','mono','onmhc','mbo']
df=DataFrame({})
for m in range(1,13):
  mo='{:02d}'.format(m)
  dfT=read_csv(P+'bioemis.space.'+mo,header=None,delim_whitespace = True)
  dfT.columns=col
  dfT['mon']=[m for i in dfT.index]
  df=df.append(dfT,ignore_index=True)
df.set_index('UTME').to_csv('biogrid2019.csv')
```

## 檔案下載

{% include download.html content="fortran程式：[bio2month-teds11.f](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/biog/bio2month-teds11.f)" %}

## Reference
