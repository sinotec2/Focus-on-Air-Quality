---
layout: default
title: CALINE3 I/O
parent: CALINE
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-04-08 15:30:32
---
# *CALINE3*的標準輸入輸出
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
- 執行*CALINE3*模式不必設定檔案，全部的數據都以標準輸入(standard input)方式，以 < 符號飼入程式。輸出數據也是以standard out形式，需以 > 指引到指定的檔名。
- *CALINE3*模式沒有複雜的氣象檔案，但是對於線源的設定有別於其他煙流模式，需要進一步說明。
- *CALINE3*有圖形界面版本([CALINE4](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/CALINE4IO/))。
- 使用手冊可自[官網](https://gaftp.epa.gov/Air/aqmg/SCRAM/models/other/caline3/caline3-unabridged.pdf)下載。

## 輸入檔範例
- *CALINE3*為舊式[fortran固定格式](http://homepage.ntu.edu.tw/~weitingc/fortran_lecture/Lecture_F_File_IO_Format.pdf)的輸入方式
- 一般設定：JOB(title)、ATIM(平均時間、分鐘)、z0(粗糙度cm)、Vs(沉降速cm/s)、Vd(沉積速度cm/s)、NR(接受點個數)、SCAL(座標、高、寬度等轉換系數m)
  - '(A40,2F4.0,2F5.0,I2,F10.0)'
- 各接受點位置：名稱、X、Y、Z
  - '(A20,3F10.0)'
- 批次訊息：RUN(title)、NL(路段數)、NM(氣象條件筆數)
  - '(A40,2I3)'
- 路段訊息：道路類型(路堤AG、填平FL、路塹DP、橋樑BR)、(XL1,YL1)、(XL2,YL2)路段端點座標、VPHL(流量veh/hr)、EFL([排放係數](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/EMISFACT/)g/mile)、HL(排放源高度)、WL(混合區寬度)
  - '(A20,A2,4F7.0,F8.0,3F4.0)'
  - 路段座標只有7格無法容納TWD座標值（南北向7碼加小數點至少8格，需修改原始碼、或輸入7碼整數值）
- 氣象個案：U(風速m/s)、BRG(正Y方向之夾角0\~360度)、CLAS(穩定度1~6)、混合層(m)、背景濃度(PPM)
  - '(F3.0,F4.0,I1,F6.0,F4.0)'

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

## 輸出檔範例
### 範例1
- 共執行了4個批次、測試路型的敏感性

|CASE|Road Type|CO ppm|
|-|-|-|
|1|AG路堤|7.6|
|2|BR橋樑|6.2|
|3|DP路塹|5.8|
|4|FL平坦|7.6|

```bash
kuang@114-32-164-198 /Users/1.PlumeModels/CALINE3
$ cat CALINE3.LST 
                     CALINE3              (DATED 89219)

                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  1


     JOB: EXAMPLE ONE                                          RUN: CASE ONE                                



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG = 270. DEGREES          Z0 =  10. CM         VD =   0.0 CM/S        AMB =  3.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *     0.  -5000.      0.   5000. *    10000.      360.      AG   7500.  30.0   0.0  30.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *        COORDINATES (M)        *  CO
       RECEPTOR             *      X        Y        Z      * (PPM)
   -------------------------*-------------------------------*-------
    1. RECP. 1              *       30.       0.      1.8   *  7.6
```
```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  2


     JOB: EXAMPLE ONE                                          RUN: CASE TWO                                



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG = 270. DEGREES          Z0 =  10. CM         VD =   0.0 CM/S        AMB =  3.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *     0.  -5000.      0.   5000. *    10000.      360.      BR   7500.  30.0   5.0  30.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *        COORDINATES (M)        *  CO
       RECEPTOR             *      X        Y        Z      * (PPM)
   -------------------------*-------------------------------*-------
    1. RECP. 1              *       30.       0.      1.8   *  6.2
```
```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  3


     JOB: EXAMPLE ONE                                          RUN: CASE THREE                              



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG = 270. DEGREES          Z0 =  10. CM         VD =   0.0 CM/S        AMB =  3.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *     0.  -5000.      0.   5000. *    10000.      360.      DP   7500.  30.0  -5.0  30.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *        COORDINATES (M)        *  CO
       RECEPTOR             *      X        Y        Z      * (PPM)
   -------------------------*-------------------------------*-------
    1. RECP. 1              *       30.       0.      1.8   *  5.8
```
```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  4


     JOB: EXAMPLE ONE                                          RUN: CASE FOUR                               



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG = 270. DEGREES          Z0 =  10. CM         VD =   0.0 CM/S        AMB =  3.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *     0.  -5000.      0.   5000. *    10000.      360.      FL   7500.  30.0   5.0  30.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *        COORDINATES (M)        *  CO
       RECEPTOR             *      X        Y        Z      * (PPM)
   -------------------------*-------------------------------*-------
    1. RECP. 1              *       30.       0.      1.8   *  7.6
```
### 範例2
- S-CURVE

```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  5


     JOB: EXAMPLE TWO                                          RUN: RURAL LOCATION: S-CURVE                 



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG =  45. DEGREES          Z0 =  50. CM         VD =   0.0 CM/S        AMB =  3.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *  -707.   -707.      0.      0. *     1000.       45.      AG   8500.  30.0   0.0  28.0
   B. LINK B                *     0.      0.    120.    175. *      212.       34.      AG   8500.  30.0   0.0  28.0
   C. LINK C                *   120.    175.    150.    350. *      178.       10.      AG   8500.  30.0   0.0  28.0
   D. LINK D                *   150.    350.    150.   1350. *     1000.      360.      AG   8500.  30.0   0.0  28.0
   E. LINK E                *   150.   1350.    175.   1510. *      162.        9.      AG   8500.  30.0   0.0  28.0
   F. LINK F                *   175.   1510.    265.   1640. *      158.       35.      AG   8500.  30.0   0.0  28.0
   G. LINK G                *   265.   1640.    350.   1760. *      147.       35.      AG   8500.  30.0   0.0  28.0
   H. LINK H                *   350.   1760.    475.   1830. *      143.       61.      AG   8500.  30.0   0.0  28.0
   I. LINK I                *   475.   1830.    650.   1850. *      176.       83.      AG   8500.  30.0   0.0  28.0
   J. LINK J                *   650.   1850.   1650.   1850. *     1000.       90.      AG   8500.  30.0   0.0  28.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *                               * TOTAL *
                                                                                            CO/LINK
                            *        COORDINATES (M)        * + AMB *                        (PPM)
       RECEPTOR             *      X        Y        Z      * (PPM) *   A    B    C    D    E    F    G    H    I    J
   -------------------------*-------------------------------*-------*
                                                                     ----------------------------------------------------
    1. RECP. 1              *      400.    1700.      1.8   *  6.1  *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  3.1  0.0
    2. RECP. 2              *      100.    1500.      1.8   * 10.7  *  0.0  0.0  0.0  0.0  0.0  1.5  3.7  2.1  0.4  0.0
    3. RECP. 3              *      200.    1300.      1.8   *  4.4  *  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.1  1.3
    4. RECP. 4              *      100.     350.      1.8   *  8.3  *  0.0  0.0  0.0  4.8  0.0  0.0  0.0  0.0  0.0  0.5
```
### 範例3
- INTERSECTION

```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  6


     JOB: EXAMPLE THREE                                        RUN: URBAN LOCATION: INTERSECTION            



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =   100. M
    BRG =  90. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  5.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *     0.    500.      0.     50. *      450.      180.      AG   1000.  50.0   0.0  14.0
   B. LINK B                *   100.      0.    500.      0. *      400.       90.      AG   5000.  60.0   0.0  26.0
   C. LINK C                *     0.    -50.      0.   -500. *      450.      180.      AG   1000.  50.0   0.0  14.0
   D. LINK D                *  -500.      0.   -100.      0. *      400.       90.      AG   5000.  60.0   0.0  26.0
   E. LINK E                *  -100.      0.    100.      0. *      200.       90.      AG   5000. 100.0   0.0  28.0
   F. LINK F                *     0.     50.      0.    -50. *      100.      180.      AG   1000. 100.0   0.0  14.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *                               * TOTAL *
                                                                                  CO/LINK
                            *        COORDINATES (M)        * + AMB *              (PPM)
       RECEPTOR             *      X        Y        Z      * (PPM) *   A    B    C    D    E    F
   -------------------------*-------------------------------*-------*
                                                                     --------------------------------
    1. RECP. 1              *      -30.      30.      1.8   * 13.1  *  0.0  5.4  0.0  0.0  0.8  1.9
    2. RECP. 2              *      -30.     -30.      1.8   * 13.1  *  0.0  5.4  0.0  0.0  0.8  1.9
    3. RECP. 3              *     -100.      30.      1.8   * 13.6  *  0.0  5.1  0.0  0.0  2.5  1.0
```
### 範例4
- BRG=0度北風

```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  7


     JOB: EXAMPLE FOUR                                         RUN: URBAN LOCATION: MULTIPLE LINKS, ETC.    



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG =   0. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB = 12.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *   500.      0.   3000.      0. *     2500.       90.      AG   9700.  30.0   0.0  23.0
   B. LINK B                *   500.      0.   1000.    100. *      510.       79.      DP   1200. 150.0  -2.0  13.0
   C. LINK C                * -3000.      0.    500.      0. *     3500.       90.      AG  10900.  30.0   0.0  23.0
   D. LINK D                * -3000.    -75.   3000.    -75. *     6000.       90.      AG   9300.  30.0   0.0  23.0
   E. LINK E                *  -500.    200.   -500.   -300. *      500.      180.      BR   4000.  50.0   6.1  27.0
   F. LINK F                *  -100.    200.   -100.   -200. *      400.      180.      BR   5000.  50.0   6.1  27.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *                               * TOTAL *
                                                                                  CO/LINK
                            *        COORDINATES (M)        * + AMB *              (PPM)
       RECEPTOR             *      X        Y        Z      * (PPM) *   A    B    C    D    E    F
   -------------------------*-------------------------------*-------*
                                                                     --------------------------------
    1. RECP. 1              *     -350.      30.      1.8   * 12.0  *  0.0  0.0  0.0  0.0  0.0  0.0
    2. RECP. 2              *        0.      30.      1.8   * 12.0  *  0.0  0.0  0.0  0.0  0.0  0.0
    3. RECP. 3              *      750.     100.      1.8   * 12.0  *  0.0  0.0  0.0  0.0  0.0  0.0
    4. RECP. 4              *      850.      30.      1.8   * 14.8  *  0.0  2.8  0.0  0.0  0.0  0.0
    5. RECP. 5              *     -850.    -100.      1.8   * 21.6  *  0.0  0.0  3.6  6.0  0.0  0.0
    6. RECP. 6              *     -550.    -100.      1.8   * 21.9  *  0.0  0.0  3.6  6.0  0.3  0.0
    7. RECP. 7              *     -350.    -100.      1.8   * 21.6  *  0.0  0.0  3.6  6.0  0.0  0.0
    8. RECP. 8              *       50.    -100.      1.8   * 21.6  *  0.0  0.0  3.6  6.0  0.0  0.0
    9. RECP. 9              *      450.    -100.      1.8   * 21.6  *  0.0  0.0  3.6  6.0  0.0  0.0
   10. RECP. 10             *      800.    -100.      1.8   * 22.6  *  3.2  1.4  0.0  6.0  0.0  0.0
   11. RECP. 11             *     -550.      25.      1.8   * 12.0  *  0.0  0.0  0.0  0.0  0.0  0.0
   12. RECP. 12             *     -550.      25.      6.1   * 12.0  *  0.0  0.0  0.0  0.0  0.0  0.0
```
- BRG=90度

```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  8


     JOB: EXAMPLE FOUR                                         RUN: URBAN LOCATION: MULTIPLE LINKS, ETC.    



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG =  90. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  7.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *   500.      0.   3000.      0. *     2500.       90.      AG   9700.  30.0   0.0  23.0
   B. LINK B                *   500.      0.   1000.    100. *      510.       79.      DP   1200. 150.0  -2.0  13.0
   C. LINK C                * -3000.      0.    500.      0. *     3500.       90.      AG  10900.  30.0   0.0  23.0
   D. LINK D                * -3000.    -75.   3000.    -75. *     6000.       90.      AG   9300.  30.0   0.0  23.0
   E. LINK E                *  -500.    200.   -500.   -300. *      500.      180.      BR   4000.  50.0   6.1  27.0
   F. LINK F                *  -100.    200.   -100.   -200. *      400.      180.      BR   5000.  50.0   6.1  27.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *                               * TOTAL *
                                                                                  CO/LINK
                            *        COORDINATES (M)        * + AMB *              (PPM)
       RECEPTOR             *      X        Y        Z      * (PPM) *   A    B    C    D    E    F
   -------------------------*-------------------------------*-------*
                                                                     --------------------------------
    1. RECP. 1              *     -350.      30.      1.8   * 28.4  *  5.7  1.3  8.9  3.9  0.0  1.6
    2. RECP. 2              *        0.      30.      1.8   * 26.6  *  8.0  2.1  5.9  3.6  0.0  0.0
    3. RECP. 3              *      750.     100.      1.8   * 13.7  *  3.2  2.6  0.0  0.9  0.0  0.0
    4. RECP. 4              *      850.      30.      1.8   * 21.7  * 12.0  0.0  0.0  2.7  0.0  0.0
    5. RECP. 5              *     -850.    -100.      1.8   * 29.6  *  3.1  0.4  1.8 15.3  1.1  0.9
    6. RECP. 6              *     -550.    -100.      1.8   * 30.5  *  3.5  0.3  1.1 15.1  2.3  1.2
    7. RECP. 7              *     -350.    -100.      1.8   * 28.2  *  3.7  0.3  0.7 14.9  0.0  1.6
    8. RECP. 8              *       50.    -100.      1.8   * 25.5  *  3.9  0.1  0.0 14.5  0.0  0.0
    9. RECP. 9              *      450.    -100.      1.8   * 24.5  *  3.5  0.0  0.0 14.0  0.0  0.0
   10. RECP. 10             *      800.    -100.      1.8   * 23.6  *  3.1  0.0  0.0 13.5  0.0  0.0
   11. RECP. 11             *     -550.      25.      1.8   * 33.0  *  4.9  1.0 12.3  4.3  2.3  1.2
   12. RECP. 12             *     -550.      25.      6.1   * 32.0  *  4.8  1.0 11.7  4.3  2.0  1.2
```
- BRG=180度

```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE  9


     JOB: EXAMPLE FOUR                                         RUN: URBAN LOCATION: MULTIPLE LINKS, ETC.    



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG = 180. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  5.0 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *   500.      0.   3000.      0. *     2500.       90.      AG   9700.  30.0   0.0  23.0
   B. LINK B                *   500.      0.   1000.    100. *      510.       79.      DP   1200. 150.0  -2.0  13.0
   C. LINK C                * -3000.      0.    500.      0. *     3500.       90.      AG  10900.  30.0   0.0  23.0
   D. LINK D                * -3000.    -75.   3000.    -75. *     6000.       90.      AG   9300.  30.0   0.0  23.0
   E. LINK E                *  -500.    200.   -500.   -300. *      500.      180.      BR   4000.  50.0   6.1  27.0
   F. LINK F                *  -100.    200.   -100.   -200. *      400.      180.      BR   5000.  50.0   6.1  27.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *                               * TOTAL *
                                                                                  CO/LINK
                            *        COORDINATES (M)        * + AMB *              (PPM)
       RECEPTOR             *      X        Y        Z      * (PPM) *   A    B    C    D    E    F
   -------------------------*-------------------------------*-------*
                                                                     --------------------------------
    1. RECP. 1              *     -350.      30.      1.8   * 14.5  *  0.0  0.0  6.5  3.0  0.0  0.0
    2. RECP. 2              *        0.      30.      1.8   * 14.5  *  0.0  0.0  6.5  3.0  0.0  0.0
    3. RECP. 3              *      750.     100.      1.8   * 13.0  *  3.2  2.5  0.0  2.3  0.0  0.0
    4. RECP. 4              *      850.      30.      1.8   * 13.8  *  5.8  0.0  0.0  3.0  0.0  0.0
    5. RECP. 5              *     -850.    -100.      1.8   *  5.0  *  0.0  0.0  0.0  0.0  0.0  0.0
    6. RECP. 6              *     -550.    -100.      1.8   *  5.1  *  0.0  0.0  0.0  0.0  0.1  0.0
    7. RECP. 7              *     -350.    -100.      1.8   *  5.0  *  0.0  0.0  0.0  0.0  0.0  0.0
    8. RECP. 8              *       50.    -100.      1.8   *  5.0  *  0.0  0.0  0.0  0.0  0.0  0.0
    9. RECP. 9              *      450.    -100.      1.8   *  5.0  *  0.0  0.0  0.0  0.0  0.0  0.0
   10. RECP. 10             *      800.    -100.      1.8   *  5.0  *  0.0  0.0  0.0  0.0  0.0  0.0
   11. RECP. 11             *     -550.      25.      1.8   * 15.5  *  0.0  0.0  7.0  3.1  0.4  0.0
   12. RECP. 12             *     -550.      25.      6.1   * 11.8  *  0.0  0.0  3.8  2.6  0.4  0.0
```
- BRG=270度

```
                            CALINE3: CALIFORNIA LINE SOURCE DISPERSION MODEL - SEPTEMBER, 1979 VERSION                     PAGE 10


     JOB: EXAMPLE FOUR                                         RUN: URBAN LOCATION: MULTIPLE LINKS, ETC.    



       I.  SITE VARIABLES


      U =  1.0 M/S            CLAS =   6  (F)        VS =   0.0 CM/S       ATIM =  60. MINUTES                   MIXH =  1000. M
    BRG = 270. DEGREES          Z0 = 100. CM         VD =   0.0 CM/S        AMB =  6.7 PPM



      II.  LINK VARIABLES


       LINK DESCRIPTION     *      LINK COORDINATES (M)      * LINK LENGTH  LINK BRG   TYPE  VPH     EF     H    W
                            *   X1      Y1      X2      Y2   *     (M)       (DEG)                 (G/MI)  (M)  (M)
   -------------------------*--------------------------------*-------------------------------------------------------
   A. LINK A                *   500.      0.   3000.      0. *     2500.       90.      AG   9700.  30.0   0.0  23.0
   B. LINK B                *   500.      0.   1000.    100. *      510.       79.      DP   1200. 150.0  -2.0  13.0
   C. LINK C                * -3000.      0.    500.      0. *     3500.       90.      AG  10900.  30.0   0.0  23.0
   D. LINK D                * -3000.    -75.   3000.    -75. *     6000.       90.      AG   9300.  30.0   0.0  23.0
   E. LINK E                *  -500.    200.   -500.   -300. *      500.      180.      BR   4000.  50.0   6.1  27.0
   F. LINK F                *  -100.    200.   -100.   -200. *      400.      180.      BR   5000.  50.0   6.1  27.0


     III.  RECEPTOR LOCATIONS AND MODEL RESULTS


                            *                               * TOTAL *
                                                                                  CO/LINK
                            *        COORDINATES (M)        * + AMB *              (PPM)
       RECEPTOR             *      X        Y        Z      * (PPM) *   A    B    C    D    E    F
   -------------------------*-------------------------------*-------*
                                                                     --------------------------------
    1. RECP. 1              *     -350.      30.      1.8   * 25.8  *  0.0  0.0 14.3  3.2  1.6  0.0
    2. RECP. 2              *        0.      30.      1.8   * 28.4  *  0.0  0.0 14.8  3.6  0.9  2.4
    3. RECP. 3              *      750.     100.      1.8   * 15.2  *  0.0  0.0  5.2  2.0  0.5  0.8
    4. RECP. 4              *      850.      30.      1.8   * 32.8  *  3.4  5.2 11.9  4.3  0.5  0.8
    5. RECP. 5              *     -850.    -100.      1.8   * 23.5  *  0.0  0.0  3.4 13.4  0.0  0.0
    6. RECP. 6              *     -550.    -100.      1.8   * 24.4  *  0.0  0.0  3.8 13.9  0.0  0.0
    7. RECP. 7              *     -350.    -100.      1.8   * 26.6  *  0.0  0.0  4.1 14.2  1.6  0.0
    8. RECP. 8              *       50.    -100.      1.8   * 28.9  *  0.0  0.0  4.6 14.7  0.9  2.0
    9. RECP. 9              *      450.    -100.      1.8   * 28.6  *  0.0  0.0  5.0 15.1  0.7  1.1
   10. RECP. 10             *      800.    -100.      1.8   * 28.7  *  0.0  0.0  5.3 15.3  0.6  0.8
   11. RECP. 11             *     -550.      25.      1.8   * 26.3  *  0.0  0.0 16.3  3.3  0.0  0.0
   12. RECP. 12             *     -550.      25.      6.1   * 25.6  *  0.0  0.0 15.7  3.2  0.0  0.0
```

## caline3遠端計算服務
- 網址[http://114.32.164.198/CALINE3.html](http://114.32.164.198/CALINE3.html)
- 選取輸入檔案、按下Run鍵即可。