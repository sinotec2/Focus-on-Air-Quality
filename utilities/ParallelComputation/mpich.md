---
layout: default
title:  mpich installation
parent:   ParallelComputation
grand_parent: Utilities
last_modified_date: 2022-04-25 12:20:36
---
# mpich
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
- MPICH(High-Performance Portable MPI)、原名MPICH2，是免費提供的，便攜式的實施MPI，用於消息傳遞用於並行計算中使用分佈式內存應用的標準的程式庫。
- MPICH是由美國政府組織開發的具有某些公共領域組件的免費開源軟件，可用於大多數類Unix操作系統

## 安裝
- 由於MPICH的核心程式及程式庫都與編譯器緊迫連結，必須按照編譯器版本進行安裝。
  - 因此如果是[直接安裝]，要注意其內設的fortran/c 編譯器種類及版本
  - 一般是GNU，可以執行mpifort --version檢視
- 由於空品模式應用大量浮點運算，一般會以ifort/pgi等商業編譯器執行fortran的編譯，必須下載原始碼重新編譯。

### 下載MPICH原始碼
- 自[官網](https://www.mpich.org/downloads/)下載合適版本

### 安裝
- 為傳統的configure->make->make install程序
- 執行前注意準備好編譯器執行檔及程式庫所需的路徑
- 此處以ifort為例
  - 指定環境變數FC及CC為機器上的ifort及icc


```bash
source /opt/intel/oneapi/compiler/2022.0.2/env/vars.sh intel64 
unset F90
unset F90FLAGS
FC=/opt/intel/oneapi/compiler/2022.0.2/linux/bin/intel64/ifort CC=/opt/intel/oneapi/compiler/2022.0.2/linux/bin/intel64/icc ./configure --prefix=/opt/mpich/mpich-3.4.2-icc --with-device=ch4:ofi 2>&1 | tee c.txt
make 2>&1 | tee m.txt
make install 2>&1 | tee mi.txt
```
### MPI communication devices
- OpenFabrics Interfaces([OFI](https://ofiwg.github.io/libfabric/))
  - OFI is a framework focused on exporting fabric communication services to applications. 
  - OFI is best described as a collection of libraries and applications used to export fabric services. 
  - The key components of OFI are: application interfaces, provider libraries, kernel services, daemons, and test applications.
- [libfabric](https://www.openfabrics.org/libfabrics-a-user-perspective/)
  - Libfabric is designed to minimize the impedance mismatch between applications, middleware and fabric communication hardware. 
  - Its interfaces target high- bandwidth, low-latency NICs([network interface controller](https://zh.wikipedia.org/wiki/%E7%BD%91%E5%8D%A1)), with a goal to scale to **tens of thousands of nodes**. 
  - Libfabric is supported by a variety of open source HPC middleware applications, including **MPICH**, **Open MPI**, Sandia SHMEM, Open SHMEM, Charm++, GasNET, Clang, UPC, and others. 

- https://installati.one/centos/7/openssh-askpass/
## Reference
- chenhh, [MPICH安裝與設定](https://chenhh.gitbooks.io/parallel_processing/content/mpi/mpich_setting.html)，此說明為Ubuntu直接安裝執行檔與程式庫。