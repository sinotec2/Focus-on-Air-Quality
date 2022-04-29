---
layout: default
title:  compilation of IOAPI
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date:   2022-04-14 16:21:45
---
# IOAPI的編譯
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
- I/O API(Input/Output Applications Programming Interface)是美國環保署發展Models-3/EDSS時順帶產生的程式庫([cmascenter, I/O API concept](https://www.cmascenter.org/ioapi/))，用來快速存取NetCDF格式檔案，尤其對Fortran等高階語言而言，是非常必須之簡化程序。
- 因此相關後續所發展的程式包括CMAQ系統、SMOKE系統、以及周圍軟體如VERDI，都會連結到其程式庫。迄今發展至3.2版，並沒有取而代之的界面程式庫或計畫。
- WRF、CAMx雖然也能存取nc檔案，並沒有使用ioapi，而是自行撰寫存取副程式。
- 其說明詳見[官網](https://www.cmascenter.org/ioapi/documentation/all_versions/html/index.html)、原始碼見於[github.com](https://github.com/cjcoats/ioapi-3.2)
- 何時會需要重新編譯
  - ioapi更新版本
  - 使用新的fortran compiler、mpi system、HDF或netCDF版本、任何一項更新都須重新編譯

## EXT檔案的原始碼格式
- 涉及檔案：ioapi目錄下的STATE3.EXT、IODECL3.EXT及FDESC3.EXT等個包括檔
- 由於Fortran原始碼長度的定義，編譯時可能啟動了自由格式，因此原本72格的F77格式失效了，須在行尾加上&符號將下一行連起來(gfortran)。
```
<         COMMON  / BSTATE3 /
<      &          P_ALP3, P_BET3, P_GAM3,
---
>         COMMON  / BSTATE3 /                                             &
>      &          P_ALP3, P_BET3, P_GAM3,                                 &
```

## CPP編譯前定義的失誤
- 原本根目錄說明了IOAPI_NCF4的開啟方式`IOAPIDEFS = "-DIOAPI_NCF4"`
- 但實際make程式進行時並沒有確實替換模版裏的變數。
```
...
IOAPIDEFS = "-DIOAPI_NCF4"

SEDCMD = \
...
-e 's|IOAPI_DEFS|$(IOAPIDEFS)|' \
...

configure: ${IODIR}/Makefile ${TOOLDIR}/Makefile
        (cd $(IODIR)   ;  sed $(SEDCMD) < Makefile.$(CPLMODE).sed > Makefile )
        (cd $(TOOLDIR) ;  sed $(SEDCMD) < Makefile.$(CPLMODE).sed > Makefile )
```
- 解決方式：直接編輯Makefile.$(CPLMODE).sed檔，開啟-DIOAPI_NCF4=1

## 連結程式庫到目標目錄($BIN)
- 包括netcdf、hdf、pnetcdf或其中所需要的程式庫，因為所有編譯動作都在$BIN目錄下進行，因此直接連結是最方便。
- 注意：編譯完成、存到最終位置時，要記得去除這些連結，否則在應用時會重複連結。

## 應用程式是否開啟openmp
- 一般程式有2類型多工的選項
  - 使用編譯器的openmp([SMP](https://zh.wikipedia.org/wiki/对称多处理))在單機多核平行運算，或者是
  - 跨節點多工mpi方案([DMP](https://en.wikipedia.org/wiki/Distributed_memory))，包括openmpi或者是mpich
  - 二者無法同時開啟
- 如果是後者(eg. CCTM)，編譯ioapi時不能出現openmp選項(如ifort的-qopenmp、gfortran的-fopenmp)，否則後面mpifort的編譯會出錯。

## Reference
- cmascenter.org, [The EDSS/Models-3 I/O API](https://www.cmascenter.org/ioapi/documentation/all_versions/html/index.html), 2020-03-25
