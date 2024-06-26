---
layout: default
title: "程式修改及編譯"
parent: "OBSGRID"
grand_parent: "WRF"
nav_order: 1
date:               
last_modified_date:   2021-11-27 22:48:34
tags: wrf OBSGRID
---

# 程式修改及編譯

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
基本上`obsgrid`程式也是個內插程式，是需要給定搜索半徑等條件的。程式執行會因為解析度的變化而異，會需要修改編譯。

## 程式下載、率定、編譯
### 下載、設定
- `git clone https://github.com/wrf-model/OBSGRID.git`，會在工作目錄下產生`OBSGRID`的新目錄，並將`github`上的原始碼下載到本機。
- `csh`進入c shell 環境
- 設定環境變數
  - setenv NETCDF /usr/local/Cellar/netcdf/4.8.1
  - setenv HDF5 /usr/local/Cellar/hdf5/1.12.1
  - setenv JASPERLIB /usr/local/Cellar/jasper/2.0.33/lib
  - setenv JASPERINC /usr/local/Cellar/jasper/2.0.33/include
  - setenv WRF_DIR /Users/WRF4.3
- 執行`configure`選擇恰當的編譯方式
- 執行`compile`進行編譯
- 詳見[README](https://github.com/wrf-model/OBSGRID/blob/master/README)

### gfortran與ifort選項的差異
```bash
$ diff configure.oa_GNU configure.oa_ifort
26a27,28
> NETCDF          =       /opt/netcdf/netcdf4_intel
>
36c38
< # Settings for Darwin - with g95 compiler
---
> # Settings for PC Linux i486 i586 i686 x86_64, Intel compiler
38,48c40,48
< FC            =       gfortran
< FFLAGS                =       -O3 -ffree-form -fconvert=big-endian #-fallow-argument-mismatch
< F77FLAGS      =       -O3 -ffixed-form -fconvert=big-endian #-fallow-argument-mismatch
< FNGFLAGS      =       $(FFLAGS)
< LDFLAGS               =       -Wl,-stack_size,20000000,-stack_addr,0xc0000000
< CC            =       clang
< CFLAGS                =
< CPP           =       /usr/bin/cpp
< CPPFLAGS      =       -C -P -traditional
< RANLIB                =
< LOCAL_LIBS    =       -L/usr/X11R6/lib -lX11
---
> FC            =       ifort
> FFLAGS                =       -FR -convert big_endian
> F77FLAGS      =       -convert big_endian
> FNGFLAGS      =       $(FFLAGS)
> LDFLAGS               =
> CC            =       gcc
> CFLAGS                =       -w
> CPP           =       /opt/intel_f/compilers_and_libraries_2020.0.166/linux/bin/intel64/fpp #/lib/cpp
> CPPFLAGS      =       -I. -C -P -DDEC -traditional
```

## 修改`src/qc0_module.F90`

### 修改緣由
- 該程式會計算在測站附近的所有觀測點數，原程式是以**250**及網格距離的比例來計算box，
- 如果網格間距太小，box會很大，將會有太多的觀測點納入，
- 除了計算會非常沒有效率之外，還可能超過設定之最大觀測站點數而報錯。

```fortran
SUBROUTINE ob_density ( xob , yob , grid_dist , numobs , tobbox , iew , jns )

!  Compute a guess at the observation density for the surface FDDA.

   IMPLICIT NONE

   REAL    , DIMENSION ( : )      :: xob, yob 
   REAL                           :: grid_dist
   INTEGER                        :: numobs
   REAL    , DIMENSION ( : , : )  :: tobbox
   INTEGER                        :: iew, jns 

   INTEGER                        :: num, iob, job, i, j , & 
                                     iobs , iobe , jobs , jobe
   REAL                           :: dist
    

   !  Loop through each of the station locations (numobs).  

   DO num = 1, numobs

      iob       = xob (num) 
      job       = yob (num)
      jobs = MAX ( job - NINT( 250. / grid_dist ) - 1 ,   1   )   
      jobe = MIN ( job + NINT( 250. / grid_dist ) + 1 , jns-1 )
      iobs = MAX ( iob - NINT( 250. / grid_dist ) - 1 ,   1   )   
      iobe = MIN ( iob + NINT( 250. / grid_dist ) + 1 , iew-1 )
      DO j = jobs , jobe
         DO i = iobs , iobe
            dist = SQRT ( ( REAL(i) - xob(num) ) **2 + ( REAL(j) - yob(num) ) **2 ) 
            IF ( dist .LT. 250. / grid_dist ) THEN
               tobbox(j,i) = tobbox(j,i) + 1 
            END IF
         END DO
      END DO

   END DO

END SUBROUTINE ob_density
```

### 各層網格之修改值
此處進行修改：
- d1: 250.(不變)
- d2:  54.
- d3:  20.
- d4:   6.

### 編譯腳本
```bash
kuang@114-32-164-198 /Users/WRF4.1/OBSGRID
$ cat mk.cs
for d in {1..4};do
  rm src/*.o src/*.mod
  rm -f src/qc0_module.F90
  cp src/qc0_module.F90.d$d src/qc0_module.F90
  compile 
  cp src/obsgrid.exe src/obsgrid$d.exe
done
```

## Reference
- Brian Reen, **A Brief Guide to Observation Nudging in WRF**, [github](https://raw.githubusercontent.com/wrf-model/OBSGRID/master/ObsNudgingGuide.pdf),February 2016.
- kkeene44, **WRF Objective Analysis Program**, [github](https://github.com/wrf-model/OBSGRID/blob/master/README),12 Oct 2018.