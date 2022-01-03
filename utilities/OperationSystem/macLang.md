---
layout: default
title: Mac Fortran/C compiler
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## ifort
- intel® Fortran Compiler 19.0 for macOS* Release Notes for Intel® Parallel Studio XE 2019[intel®](https://software.intel.com/en-us/articles/intel-fortran-compiler-190-for-macos-release-notes-for-intel-parallel-studio-xe-2019)

## 在MacOS下搭建Fortran开发环境by 李宇琨

- https://lyk6756.github.io/fortran/2017/08/04/Fortran_for_MacOS.html

## gcc(gfortran included):

```bash
brew install gcc
gfortran 10 argument mismatch of type
https://github.com/Unidata/netcdf-fortran/issues/212
export FCFLAGS="-w -fallow-argument-mismatch -O2"
export FFLAGS="-w -fallow-argument-mismatch -O2"
```
## Downgrade of gcc

```bash
brew install gcc@9
(brew switch is deprecated, link the file directly or accept the suggestion of brew doctor)
(base) 10:45:59:kuang@MiniWei:/usr/local/opt $ ls -lh
total 0
...
lrwxr-xr-x  1 kuang  admin    21B Dec 16 06:18 gcc -> ../Cellar/gcc@9/9.3.0
lrwxr-xr-x  1 kuang  admin    21B Dec 16 06:18 gcc@9 -> ../Cellar/gcc@9/9.3.0
```


