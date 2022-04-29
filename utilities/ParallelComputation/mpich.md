---
layout: default
title:  mpich編譯及應用 
parent:   Parallel Computation
grand_parent: Utilities
last_modified_date: 2022-04-25 12:20:36
---
# mpich編譯及應用
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
- [MPICH](https://baike.baidu.hk/item/MPICH/7488372) (MPI  derived from Chameleon)、原名MPICH2、是免費提供的、便攜式的[MPI方案](https://zh.wikipedia.org/wiki/訊息傳遞介面)，用於傳遞消息並行計算中使用分佈式內存應用的標準的程式及程式庫。
- MPICH是由美國政府組織開發的具有某些公共領域組件的免費開源軟件，可用於大多數類Unix操作系統
- 何時會需要重新編譯mpich
  - 更新編譯器：種類或版本
  - 更新mpich版本
  - 啟用更多nodes、欲啟用溝通設備或方式時
- [openmpi](https://www.open-mpi.org/)為另一常用的MPI種類，主要為大學間開放平台所發展，經常應用於全球最快的超級電腦，二者在局部比較似乎以[MPICH較快些](https://users.open-mpi.narkive.com/ZE5vyikd/ompi-performance-mpich2-vs-openmpi)

## 安裝與編譯
- 由於MPICH的核心程式及程式庫都與編譯器緊迫連結，必須按照編譯器版本進行安裝。
  - 因此如果是[直接安裝]，要注意其內設的fortran/c 編譯器種類及版本
  - 一般是GNU，可以執行mpifort --version檢視
- 由於空品模式應用大量浮點運算，一般會以ifort/pgi等商業編譯器執行fortran的編譯，必須下載原始碼重新編譯。

### 下載MPICH原始碼
- 自[官網](https://www.mpich.org/downloads/)下載合適版本

### 安裝
- 為傳統的configure->make->make install程序
- 執行前注意準備好編譯器執行檔及程式庫所需的路徑
- 目標路徑(--prefix)：如果是**跨機器**的架構，可以考慮放在網路磁碟機。如果沒有，**跨機器**執行時也必須在每一台工作站上相同位置複製一份。
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

## mpirun的**跨機器**執行
- 使用者必須在各機器間能夠[免密登入](https://dywang.csie.cyut.edu.tw/dywang/security/node84.html)。
  - 免密登入「**必須**」包括本機，否則mpirun還是會問本機的登入密碼
- 裝置[ssh-askpass](https://ishm.idv.tw/?p=53)
  - 為了讓使用者有安全的通訊協定之外，ssh-askpass還提供了遠端登入、遠端傳遞檔案、遠端執行命令、以及為 rsync 和 rdist 提供安全通道等功能。
  - [How To Install openssh-askpass on CentOS 7](https://installati.one/centos/7/openssh-askpass/)，雖然工作站間已經設定好免密登入，但執行mpirun時仍會需要執行ssh-askpass。正常的centos是不會自帶的，需要安裝。
- 關閉機器間所有[防火牆設定](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/ParallelComputation/firewall/)
- 編輯machinefile

```bash
#kuang@dev2 /nas2/cmaqruns/2019force/output/2019-01
#$ cat machinefile
DEVP:96
dev2:96
```
- 所有的機器都需要相同版本的mpirun程式與程式庫、以及相同的路徑
- 將所需的程式庫(compiler、netcdf、hd5、mpi、等)，存放在共用的網路磁碟機
- 設定環境變數`LD_LIBRARY_PATH`
  - 注意：csh必須`setenv`，只`set`不能作用
- 執行指令：`time $MPIRUN -f machinefile -np 192  $EXEC`

## Reference
- dywang.csie.cyut.edu.tw, [SSH 免密碼登入](https://dywang.csie.cyut.edu.tw/dywang/security/node84.html), 2020-05-19
- chenhh, [MPICH安裝與設定](https://chenhh.gitbooks.io/parallel_processing/content/mpi/mpich_setting.html)，此說明為Ubuntu直接安裝執行檔與程式庫。