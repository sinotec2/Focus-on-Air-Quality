---
layout: default
title: CALPOST
nav_order: 3
has_children: true
parent: Trajectory Models
permalink: /TrajModels/CALPOST
---

# CALPOST
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

這裡介紹CALPUFF的後處理。

## 概要
- CAPUFF的模擬結果包括濃度(.con)、乾濕沉降(.dry、.wet)檔案，為fortran的二進位檔案，必須由CALPOST.EXE來讀取，無法由其他程式直接處理。
- 因CALPOST.EXE有許多繁雜的設定、很多是沿襲CALPUFF的設定，會影響到讀取的方式，因此如果要重新撰寫fortran程式，還不如直接承襲CALPOST.FOR+CALPUFF.INP加以修改即可。

## CALPOST.EXE安裝
- CALPOST.FOR可以自[官網](http://www.src.com/calpuff/download/download.htm)下載。需注意與CALPUFF版本之搭配。

### gfortran
- 注意加入legacy設定

```bash
kuang@master /home/cpuff/src/CALPOST/CALPOST_v7.1.0_L141010
$ cat cpl_gfortran
gfortran -O2 -fno-align-commons -fconvert=big-endian -frecord-marker=4 -ffixed-line-length-72 -std=legacy -o cpost710g calpost.for
```
### pgi fortran
- 官方提供的編譯方式。pgi需要自己的lib檔。

```bash
kuang@master /home/cpuff/src/CALPOST/CALPOST_v7.1.0_L141010
$ cat cpl_unix.bat
# Example settings for compiling on Linux with Portland Group 64-bit Compiler (make 32-bit executable!)

pgf90 -O0 -Kieee -Ktrap=fp -Msave -tp k8-32 -L/opt/pgi/linux86/11.5/liblf calpost.for -o calpost.x


# Switch settings ------------------------------
# pgf90           Portland Group Fortran 90 compiler (64-bit library here)
# -O0             Set the optimization level at Level 0
# ▒Kieee          Request  special  compilation semantics from the compiler.  Perform float and double  divides  in
                    conformance with the IEEE 754 standard
# ▒Ktrap=fp       Trap NDP errors (halt program)
# ▒Msave          All  local  variables  are  subject to the SAVE statement
# -tp k8-32       Create 32-bit executable
# -L              Library path that is installation-specific
# ▒o file         Use file as the name of the executable program, rather than the default a.out
```

### window版本的fortran
- 需視記憶體大小調整params檔案

```bash
kuang@master /home/cpuff/src/CALPOST/CALPOST_v7.1.0_L141010
$ cat cpl.bat
REM Compiling and linking with CALPOST using Lahey LF95 for Windows

lf95 calpost.for -o0 -co -sav -trap doi -out calpost.exe >cpl.txt

del *.obj
del *.map

rem Switch settings ------------------------------
rem -o0             No optimization
rem -co             Display the compiler options that are used
rem -sav            Save local variables
rem -trap doi       Trap NDP divide-by-zero (d), overflow (o), and invalid operation (i)
rem -out            Name the compiled executable to "calpost.exe"
rem >               Send compiler screen output to file "cpl.txt"
```

### ifort版本

```bash
kuang@master /home/cpuff/src/CALPOST/CALPOST_v7.1.0_L141010
$ cat ifort_cpost
ifort -convert big_endian -Bstatic calpost.for -o cpost710
```

{: .fs-6 .fw-300 }

## Table of CALPOST contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---


