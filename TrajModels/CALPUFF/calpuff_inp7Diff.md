---
layout: default
title: calpuff.inp from V7.0 eg
nav_order: 4
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-04-05 14:28:18
---

# 由7.0版範例編輯calpuff.inp
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
- 由[官方網站](http://www.src.com/calpuff/download/download.htm)提供的控制檔範例開始編輯，是一個穩妥的方案。畢竟大多數設定已經通過測試。
   - 目前官網提供的是7.3.1版，以下範例是7.1.0版
- 主要編輯的內容是臺灣地區的座標系統是TWD系統，有別於一般常用的UTM系統，如果有外島、或範圍超過2度範圍(如執行WRF)，也無法適用TWD，必須改用LCC系統。
- 離散接受點的設定，也必須視使用者的需要而更改。

## 時間與空間架構

### [起訖時間](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-group-1--general-run-control-parameters)
- [METRUN](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#run-all-periods)

```bash
root@114-32-164-198 /Library/WebServer/Documents/cpuff_results/cpuf_6nbnk12i
# !diff
diff calpuff_7.0.inp calpuff.inp 
265c265
<     in the met. file     (METRUN)   Default: 0       ! METRUN =   0  !
---
>     in the met. file     (METRUN)   Default: 0       ! METRUN =   1  !
```
- 時區

```bash
286c286
<      Base time zone:          (ABTZ)  --    No default   ! ABTZ= UTC-0500 !
---
>      Base time zone:          (ABTZ)  --    No default   ! ABTZ= UTC-0000 !
```
### [座標系統](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#projection-for-all-xy)
- UTM：適用在6度範圍內小範圍、高解析度的直角座標系統（TWD系統係2度範圍）
- LCC：超過2～6度、大範圍、直角座標系統

```bash
766c766
<      (PMAP)                     Default: UTM    ! PMAP = UTM  !
---
>      (PMAP)                     Default: UTM    ! PMAP = LCC  !
782c782
<      (IUTMZN)                   No Default      ! IUTMZN =  19   !
---
>      (IUTMZN)                   No Default      ! IUTMZN =  51   !
792,793c792,793
<      (RLAT0)                    No Default      ! RLAT0 = 0N  !
<      (RLON0)                    No Default      ! RLON0 = 0E  !
---
>      (RLAT0)                    No Default      ! RLAT0 = 23.61N  !
>      (RLON0)                    No Default      ! RLON0 =120.99E  !
808,809c808,809
<      (XLAT1)                    No Default      ! XLAT1 = 0N  !
<      (XLAT2)                    No Default      ! XLAT2 = 0N  !
---
>      (XLAT1)                    No Default      ! XLAT1 = 10N  !
>      (XLAT2)                    No Default      ! XLAT2 = 40N  !
843c843
<      (DATUM)                    Default: WGS-84    ! DATUM = NAS-C  !
---
>      (DATUM)                    Default: WGS-84    ! DATUM = WGS-G  !
```
- 網格數及網格間距

```bash
851,853c851,853
<             No. X grid cells (NX)      No default     ! NX =  99   !
<             No. Y grid cells (NY)      No default     ! NY =  99   !
<          No. vertical layers (NZ)      No default     ! NZ =  10   !
---
>             No. X grid cells (NX)      No default     ! NX =  83   !
>             No. Y grid cells (NY)      No default     ! NY = 137   !
>          No. vertical layers (NZ)      No default     ! NZ =  15   !
855c855
<            Grid spacing (DGRIDKM)      No default     ! DGRIDKM = 1.0 !
---
>            Grid spacing (DGRIDKM)      No default     ! DGRIDKM = 3.0 !
```
- 垂直層高度、座標原點、計算範圍起訖網格

```bash
861c861
<    ! ZFACE = .0, 20.0, 40.0, 80.0, 160.0, 300.0, 600.0, 1000.0, 1500.0, 2200.0, 3000.0 !
---
>    !ZFACE=0.0,20.0,47.0,75.0,106.5,141.5,181.0,226.0,277.0,334.5,399.5,555.5,757.0,1177.0,1566.5,2403.5!
867,868c867,868
<             X coordinate (XORIGKM)     No default     ! XORIGKM = 310.0 !
<             Y coordinate (YORIGKM)     No default     ! YORIGKM = 4820.0 !
---
>             X coordinate (XORIGKM)     No default     ! XORIGKM = -124.5!
>             Y coordinate (YORIGKM)     No default     ! YORIGKM = -205.5!
887c887
<         X index of UR corner (IECOMP)      No default     ! IECOMP =  99   !
---
>         X index of UR corner (IECOMP)      No default     ! IECOMP =  83   !
890c890
<         Y index of UR corner (JECOMP)      No default     ! JECOMP =  99   !
---
>         Y index of UR corner (JECOMP)      No default     ! JECOMP = 137   !
```
## 化學設定
- 臭氧值設定方式([MOZ](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-group-11--chemistry-parameters))
```bash
1279c1279
<      Ozone data input option (MOZ)     Default: 1            ! MOZ =  1   !
---
>      Ozone data input option (MOZ)     Default: 1            ! MOZ =  0   !
```
## 排放設定
- [點源位置及其條件](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#subgroup-13b-constant-emissions)

```bash
1797c1797
<    1 ! X =    340.5,   4870.5,   40.0,   157.0,      3.0,   5.0,  355.0,   .0, 
---
>    1 ! X =    -49.873, 63.288,  150,      4.7,    11.00,  19.8, 363.0,    .0, 
1803,1804c1803,1804
<    2 ! X =    323.6,   4833.1,    33.0,  241.0,      3.5,  10.0,  330.0,   .0, 
<                            1.5E01,  0.0E00,  6.0E00,  1.5E00,  0.0E00,  0.0E00,  1.5E01 ! 
---
>    2 ! X =    -49.873, 63.288,  150,      4.7,    11.00,  19.8, 363.0,    .0, 
>                            1.0E01,  0.0E00,  4.0E00,  1.0E00,  0.0E00,  0.0E00,  1.0E01 ! 
1809,1810c1809,1810
<    3 ! X =    367.2,   4871.8,    43.0,  121.5,      3.1,   7.6,  340.0,   .0,
<                            1.1E01,  0.0E00,  5.0E00,  1.1E00,  0.0E00,  0.0E00,  1.1E01 ! 
---
>    3 ! X =    -49.873, 63.288,  150,      4.7,    11.00,  19.8, 363.0,    .0, 
>                            1.0E01,  0.0E00,  4.0E00,  1.0E00,  0.0E00,  0.0E00,  1.0E01 ! 
```
## 接受點
- 離散接受點([NREC](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#subgroup-17a-number-of-receptors))

```bash
2569c2569
<      Number of non-gridded receptors (NREC)  No default  !  NREC =  10   !
---
>      Number of non-gridded receptors (NREC)  No default  !  NREC =   0   !
```

## 編輯後檔案下載點
- [githup.io](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/calpuff.inp)