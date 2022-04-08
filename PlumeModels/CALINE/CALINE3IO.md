---
layout: default
title: CALINE3 I/O
parent: CALINE
grand_parent: Plume Models
nav_order: 1
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
- 執行CALINE3模式不必設定檔案，全部的數據都以標準輸入(standard input)方式，以**<**符號飼入程式。輸出數據也是以standard out形式，需以**>**指引到指定的檔名。
- CALINE3模式沒有複雜的氣象檔案，但是對於線源的設定有別於其他煙流模式，需要進一步說明。
- CALINE3有圖形界面版本([CALINE4]())。使用手冊可自[官網](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/other/caline3/caline3-unabridged.pdf)下載。

## 輸入檔範例
1. 一般設定：JOB(title)、ATIM(平均時間、分鐘)、z0(粗糙度cm)、Vs(沉降速cm/s)、Vd(沉積速度cm/s)、NR(接受點個數)、SCAL(座標、高、寬度等轉換系數1/m)
1. 各接受點位置：名稱、X、Y、Z
1. 批次訊息：RUN(title)、NL(路段數)、NM(氣象條件筆數)
1. 路段訊息：道路類型(路堤AG、填平FL、路塹DP、橋樑BR)、(XL1,YL1)、(XL2,YL2)路段端點座標、VPHL(流量veh/hr)、EFL(排放係數g/mile)、HL(排放源高度)、WL(混合區寬度)
1. 氣象個案：U(風速m/s)、BRG(正Y方向之夾角0\~360度)、CLAS(穩定度1\~6)

### 範例1
- 同一路段、同一接受點、
- 共執行了4個批次、測試路型的敏感性

```bash
$ cat CALINE3.EXP
EXAMPLE ONE                              60. 10.   0.   0. 1        1.
RECP. 1                    30.        0.       1.8
CASE ONE                                  1  1
LINK A              AG     0. -5000.     0.  5000.   7500. 30.  0. 30.
 1.270.6 1000. 3.0
EXAMPLE ONE                              60. 10.   0.   0. 1        1.
RECP. 1                    30.        0.       1.8
CASE TWO                                  1  1
LINK A              BR     0. -5000.     0.  5000.   7500. 30.  5. 30.
 1.270.6 1000. 3.0
EXAMPLE ONE                              60. 10.   0.   0. 1        1.
RECP. 1                    30.        0.       1.8
CASE THREE                                1  1
LINK A              DP     0. -5000.     0.  5000.   7500. 30. -5. 30.
 1.270.6 1000. 3.0
EXAMPLE ONE                              60. 10.   0.   0. 1        1.
RECP. 1                    30.        0.       1.8
CASE FOUR                                 1  1
LINK A              FL     0. -5000.     0.  5000.   7500. 30.  5. 30.
 1.270.6 1000. 3.0
```
### 範例2
- 4個接受點、10個路段(S形)、

```bash
EXAMPLE TWO                              60. 50.   0.   0. 4        1.
RECP. 1                   400.     1700.       1.8
RECP. 2                   100.     1500.       1.8
RECP. 3                   200.     1300.       1.8
RECP. 4                   100.      350.       1.8
RURAL LOCATION: S-CURVE                  10  1
LINK A              AG  -707.  -707.     0.     0.   8500. 30.  0. 28.
LINK B              AG     0.     0.   120.   175.   8500. 30.  0. 28.
LINK C              AG   120.   175.   150.   350.   8500. 30.  0. 28.
LINK D              AG   150.   350.   150.  1350.   8500. 30.  0. 28.
LINK E              AG   150.  1350.   175.  1510.   8500. 30.  0. 28.
LINK F              AG   175.  1510.   265.  1640.   8500. 30.  0. 28.
LINK G              AG   265.  1640.   350.  1760.   8500. 30.  0. 28.
LINK H              AG   350.  1760.   475.  1830.   8500. 30.  0. 28.
LINK I              AG   475.  1830.   650.  1850.   8500. 30.  0. 28.
LINK J              AG   650.  1850.  1650.  1850.   8500. 30.  0. 28.
 1. 45.6 1000. 3.0
```
### 範例3
- 3個接受點、6個路段(交錯)

```bash
EXAMPLE THREE                            60.100.   0.   0. 3        1.
RECP. 1                   -30.       30.       1.8
RECP. 2                   -30.      -30.       1.8
RECP. 3                  -100.       30.       1.8
URBAN LOCATION: INTERSECTION              6  1
LINK A              AG     0.   500.     0.    50.   1000. 50.  0. 14.
LINK B              AG   100.     0.   500.     0.   5000. 60.  0. 26.
LINK C              AG     0.   -50.     0.  -500.   1000. 50.  0. 14.
LINK D              AG  -500.     0.  -100.     0.   5000. 60.  0. 26.
LINK E              AG  -100.     0.   100.     0.   5000.100.  0. 28.
LINK F              AG     0.    50.     0.   -50.   1000.100.  0. 14.
 1. 90.6  100. 5.0
```
### 範例4
- 12個接受點、6路段、4個風向

```bash
EXAMPLE FOUR                             60.100.   0.   0.12        1.
RECP. 1                  -350.       30.       1.8
RECP. 2                     0.       30.       1.8
RECP. 3                   750.      100.       1.8
RECP. 4                   850.       30.       1.8
RECP. 5                  -850.     -100.       1.8
RECP. 6                  -550.     -100.       1.8
RECP. 7                  -350.     -100.       1.8
RECP. 8                    50.     -100.       1.8
RECP. 9                   450.     -100.       1.8
RECP. 10                  800.     -100.       1.8
RECP. 11                 -550.       25.       1.8
RECP. 12                 -550.       25.       6.1
```
- 路段資訊
  - 6段落、4個方向
  - 路段名稱、型態(路堤AG、路塹DP、橋樑BR)

```bash
URBAN LOCATION: MULTIPLE LINKS, ETC.      6  4
LINK A              AG   500.     0.  3000.     0.   9700. 30.  0. 23.
LINK B              DP   500.     0.  1000.   100.   1200.150. -2. 13.
LINK C              AG -3000.     0.   500.     0.  10900. 30.  0. 23.
LINK D              AG -3000.   -75.  3000.   -75.   9300. 30.  0. 23.
LINK E              BR  -500.   200.  -500.  -300.   4000. 50. 6.1 27.
LINK F              BR  -100.   200.  -100.  -200.   5000. 50. 6.1 27.
 1.  0.6 1000.12.0
 1. 90.6 1000. 7.0
 1.180.6 1000. 5.0
 1.270.6 1000. 6.7
```


