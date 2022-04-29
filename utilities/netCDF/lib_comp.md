---
layout: default
title:  程式庫之編譯
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-04-26 16:14:13
---
# NC相關程式庫之編譯
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
- WRF或者是CMAQ是非常高階的程式，以CMAQ而言，會呼叫[ioapi](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ioapi/#ioapi的編譯)的程式庫，ioapi又應用到netCDF的程式庫，而netCDF則會呼叫HDF的程式庫。
- 因此整體編譯必須由HDF開始，拾級而上，最後才能編譯到空氣品質應用模式。
- 這些程式又需要跨節點的[平行計算](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/ParallelComputation/)功能，因此需要MPICH、openMPI等先行編譯，再以編譯過的mpifort、mpicc進行上述程式庫的編譯。
- 除了平行計算之外，跨節點的平行IO(MPI-I/O)也會對執行速度造成顯著影響(CCTM至少可以減少20%時間)，因與PnetCDF編譯有關，就直接在此介紹。

## HDF5編譯
### 背景
- wiki([Hierarchical Data Format](https://zh.wikipedia.org/wiki/HDF))
  - HDF是设计用来存储和组织大量数据的一组文件格式。
  - 由美国国家超级计算应用中心開發，现在由非营利社团HDF Group支持。
  - HDF的设计组合了来自很多不同格式的想法，包括TIFF、CGM、FITS和Macintosh PICT格式。大约1990年代早期美国国家航空航天局（NASA）研究了用在地球观测系统（EOS）计划中的15种不同文件格式。在两年评述过程之后，HDF被选择为EOS数据和信息系统的标准格式。
  - 1996年美国能源部的劳伦斯利弗摩尔、洛斯阿拉莫斯和桑迪亚国家实验室与NCSA抽调人员成立了数据建模和格式（DMF）小组，研究满足高级模拟和计算规划（ASC）需要的并行I/O能力的文件格式。
  - 在HDF5文件中的资源可以使用类似POSIX语法的“/路径/至/资源”来访问，以及一般化的二元搜尋樹（binary search tree）技術。這使得HDF5的存取速度較SQL更加快速。
- 除了傳統的C、Fortran之外，HDF5也支援MATLAB、MATHMATICA、Python、R、等等語言及軟體系統。  
- 中文介紹可以參考[分層數據格式資料庫Hierarchical Data Format (HDF5)簡介](https://blog.xuite.net/cpy930814355/twblog/100497173-分層數據格式資料庫Hierarchical+Data+Format+(HDF5)簡介)
- HDF5可以使用MPI IO架構進行平行化之IO，如果程式中呼叫MPI_File指令
  - WRF程式有直接呼叫MPI_File指令、因此編譯不需要PnetCDF
  - CMAQ則沒有，CMAQ是在ioapi程式庫中呼叫PnetCDF進行MPI-I/O。

### 下載
- 至[官網](https://www.hdfgroup.org/downloads/hdf5)下載
  - 因每個編譯器版本略有差異，還是下載原始碼自行編譯較為穩定
### 編譯
- 因[netCDF]()會用到[HDF5]()的程式庫，因此要先編譯[HDF5]()
  - 同一版本可能會編譯好幾次，建議在目錄下另建`build_VER`目錄以資識別
  - 要記得開啟`--enable-fortran`、這樣netcdff才會連結得上
  - 開啟`--enable-parallel`才會開啟MPI-I/O([ucar](https://www.unidata.ucar.edu/software/netcdf/workshops/most-recent/pnetcdf/BuildingParallel.html))
- 編譯順序為傳統之configure->make->make install順序
#### intel version

```bash
$ cat ~/MyPrograms/hdf5-1.10.5/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
FC=ifort FCFLAG='-auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp' CC=icc ../configure --prefix=/opt/hdf/hdf5_intel --enable-parallel --enable-fortran 
```
#### gnu version

```bash
FC=mpifort CC=mpicc ../configure --prefix=/opt/hdf/hdf5_gccMPICH --enable-fortran --enable-parallel --with-zlib=/opt/Zlib
```

### 其他程式庫
- 編譯過程會連結到電腦裏既有的libz.a、libpng.a、libld.a、libm.a等
- 在$PREFIX/lib/libhdf5.settings中有詳細的說明
  - 如果在/lib64目錄下沒有這些程式庫，就必須建立LD_LIBRARY_PATH將其連結起來。

## netCDF
- [WRF]()、[CCTM]()等程式都會需要`libnetcdf.a`及`libnetcdff.a`2個檔案

### netCDF-c編譯

- [netcdf-c]()環境設定如下

```bash
export LD_LIBRARY_PATH=/opt/intel/oneapi/compiler/2022.0.2/linux/lib:/opt/intel/oneapi/compiler/2022.0.2/linux/lib/x64:/opt/intel/oneapi/compiler/2022.0.2/linux/lib/oclfpga/host/linux64/lib:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin:/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/lib
FC=mpifort CC=mpicc CPPFLAGS="-I/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/include" \
LDFLAGS="-L/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/lib" \
../configure --prefix=/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc --enable-parallel-tests
```

### netCDF-fortran編譯
- [netcdf-f]()環境設定如下

```bash
export LD_LIBRARY_PATH=/opt/intel/oneapi/compiler/2022.0.2/linux/lib:/opt/intel/oneapi/compiler/2022.0.2/linux/lib/x64:/opt/intel/oneapi/compiler/2022.0.2/linux/lib/oclfpga/host/linux64/lib:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin:/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/lib:/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc/lib
FC=mpifort CC=mpicc \
CPPFLAGS="-I/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/include -I/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc/include" \
LDFLAGS="-L/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/lib -L/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc/lib" \
../configure --prefix=/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc --enable-parallel-tests
```
- 遭遇錯誤
  1. `checking size of off_t... configure: error`
    - 可能原因：找不到程式庫
    - [ 求助：安装netcdf-fortran出错cannot compute sizeof (off_t)](http://bbs.06climate.com/forum.php?mod=viewthread&tid=91286)
    - [cannot compute sizeof (off_t)](https://www.unidata.ucar.edu/support/help/MailArchives/netcdf/msg13615.html)
  2. 要求較新版本的libnetcdf.a
    - 重新以新版netcdf-c編譯

## PnetCDF
- 因應UCAR提出平行HDF5的netCDF4技術，PnetCDF表示歡迎，因此除了原本的MPI-I/O方案，也可以接受與netCDF4結合([parallel-netcdf.github.io](https://parallel-netcdf.github.io/wiki/PnetcdfAndNetcdf4.html))。
- 此方案也是ioapi的路徑：利用開啟檔案(`nc_create_par`)時的NC_PNETCDF選項，就能連結到PnetCDF程式庫，而不必在程式內直接呼叫MPI_FILE指令。

### 編譯順序
- 流程與重要設定
  - HDF5：必須開啟--enable-parallel, 
  - netCDF-c
  - netCDF-fortran(會挑netCDF-c的版次)
  - PnetCDF編譯：必須開啟--enable-netcdf4選項，與前述所有程式庫連結
- 不必另建MPI-I/O系統
- 因為整個流程到PnetDF建置已屬於下游，強烈建議要進行完整測試，俟無誤後再安裝到定點。
  - make;make tests;make check;make ptest;make ptests;make install
- 可能錯誤
  - `undefined reference to `_intel_fast_memcpy'`
  - [解決方式](https://community.intel.com/t5/Intel-Fortran-Compiler/undefined-reference-to-intel-fast-memcpy/m-p/758815)：
    - 增加configure時c++的LDFLAGS環境變數內容
    - `LDFLAGS="-L/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin -lirc"`

### configure環境設定及選項
- with-mpi可以直接連到根目錄，不必再指定include及lib
- with-netcdf4亦然
- hdf並不需要特別指定，在netCDF程式庫中已經隱含，只要給定程式庫的路徑即可
- c++程式庫須特別指定，理由如上述。

```bash
source /opt/intel/oneapi/compiler/2022.0.2/env/vars.sh intel64
export PATH=/opt/mpich/mpich-3.4.2-icc/bin:$PATH
export LD_LIBRARY_PATH=/opt/intel/oneapi/compiler/2022.0.2/linux/lib:/opt/intel/oneapi/compiler/2022.0.2/linux/lib/x64:/opt/intel/oneapi/compiler/2022.0.2/linux/lib/oclfpga/host/linux64/lib:/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin:/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/lib:/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc/lib
FC=mpifort FCFLAG="-auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp" \
CC=mpicc \
LDFLAGS="-L/opt/intel/oneapi/compiler/2022.0.2/linux/compiler/lib/intel64_lin -lirc" \
../configure --prefix=/opt/pnetcdf/pnetcdf-1.12.3_intel_mpich-icc --with-mpi=/opt/mpich/mpich-3.4.2-icc --with-netcdf4=/opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc
```

-L/opt/bld/CMAQ-master/lib/x86_64/gcc/ioapi/lib -lpnetcdf -o cctm.exe
/usr/bin/ld: Warning: alignment 32 of symbol `bstate3_' in /opt/bld/CMAQ-master/lib/x86_64/gcc/ioapi/lib/libioapi.a(initblk3.o) is smaller than 64 in pshut3.o

## Reference
- 陳柏源, [分層數據格式資料庫Hierarchical Data Format (HDF5)簡介](https://blog.xuite.net/cpy930814355/twblog/100497173-分層數據格式資料庫Hierarchical+Data+Format+(HDF5)簡介), 2011-08-20
- 北京焱融科技有限公司, [关于MPI-IO，你该知道的](https://www.yanrongyun.com/zh-cn/blogs/all-you-should-know-about-MPI-IO), 2021-03-08 11:30
- William Gropp, [Lecture 32: Introduction to MPI I/O](https://wgropp.cs.illinois.edu/courses/cs598-s16/lectures/lecture32.pdf)
  - 啟用MPI IO需在程式內使用下列指令：`MPI_File_open`, `MPI_File_write`, `MPI_File_read`, `MPI_File_close`
- ucar,  2012 Unidata NetCDF Workshop, [Building NetCDF-4 with Parallel I/O](https://www.unidata.ucar.edu/software/netcdf/workshops/most-recent/pnetcdf/BuildingParallel.html), 2012.
- parallel-netcdf.github.io, [PnetCDF and NetCDF-4](https://parallel-netcdf.github.io/wiki/PnetcdfAndNetcdf4.html)
- TimP, community.intel.com, [undefined reference to `_intel_fast_memcpy'](https://community.intel.com/t5/Intel-Fortran-Compiler/undefined-reference-to-intel-fast-memcpy/m-p/758815), 09-05-2009.
