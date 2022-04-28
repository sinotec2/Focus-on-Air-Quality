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
## EXT檔案的原始碼格式
- 涉及檔案：ioapi目錄下的STATE3.EXT、IODECL3.EXT及FDESC3.EXT等個包括檔
- 由於Fortran原始碼長度的定義，編譯時可能啟動了自由格式，因此原本72格的F77格式失效了，須在行尾加上&符號將下一行連起來。
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
- 包括netcdf、hdf、或其中所需要的程式庫，因為所有編譯動作都在$BIN目錄下進行，因此直接連結是最方便。
- 注意：編譯完成、存到最終位置時，要記得去除這些連結，否則在應用時會重複連結。

## 應用程式是否開啟openmp
- 一般程式有2個多工的選項
  - 使用編譯器的openmp(SMP)，或者是
  - mpi方案(DMP)，包括openmpi或者是mpich
  - 二者無法同時開啟
- 如果是後者，ioapi編譯時不能出現openmp選項(如ifort的-qopenmp)，否則後面的編譯會出錯。

## Reference
