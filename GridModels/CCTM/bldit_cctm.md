---
layout: default
title: CCTM之編譯
parent: CCTM Main Program
grand_parent: CMAQ Model System
nav_order: 1
date: 2022-04-20 20:27:59
last_modified_date: 2022-04-20 20:45:42
---

# CCTM之編譯
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
- 什麼時間會需要重新編譯CCTM程式
  - CMAQ進版
  - 軟硬體、OS更新
  - 測試不同編譯器、MPI方式之穩定性與速度(tuning)
  - 程式偵錯、修改  
- 大致流程
  1. HDF5 (nc檔案壓縮使用)
  1. netCDF4 (c and fortran)
  1. [mpi](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/ParallelComputation/mpich/)(CCTM不適用openMP，只有mpi方式)
  1. (pnetcdf，如果有大型nc檔案，pnetcdf會有幫助)
  1. ioapi：視編譯器、mpi版本而異
  1. bldmake：啟動make的程式。不同編譯器、mpi有自己的bldmake
  1. CCTM程式的編譯
- HDF5、netCDF、及ioapi除了應用在CCTM之外，也是常用的程式庫，另行說明。此處介紹bldmake及CCTM編譯

