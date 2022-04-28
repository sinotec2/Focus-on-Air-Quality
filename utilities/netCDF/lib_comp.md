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

## HDF5編譯
### 背景
- HDF([Hierarchical Data Format](https://zh.wikipedia.org/wiki/HDF))是设计用来存储和组织大量数据的一组文件格式。
  - 由美国国家超级计算应用中心開發，现在由非营利社团HDF Group支持。
  - HDF的设计组合了来自很多不同格式的想法，包括TIFF、CGM、FITS和Macintosh PICT格式。大约1990年代早期美国国家航空航天局（NASA）研究了用在地球观测系统（EOS）计划中的15种不同文件格式。在两年评述过程之后，HDF被选择为EOS数据和信息系统的标准格式。
  - 1996年美国能源部的劳伦斯利弗摩尔、洛斯阿拉莫斯和桑迪亚国家实验室与NCSA抽调人员成立了数据建模和格式（DMF）小组，研究满足高级模拟和计算规划（ASC）需要的并行I/O能力的文件格式。
  - 在HDF5文件中的资源可以使用类似POSIX语法的“/路径/至/资源”来访问，以及一般化的二元搜尋樹（binary search tree）技術。這使得HDF5的存取速度較SQL更加快速。
- 除了傳統的C、Fortran之外，HDF5也支援MATLAB、MATHMATICA、Python、R、等等語言及軟體系統。  
- 中文介紹可以參考[分層數據格式資料庫Hierarchical Data Format (HDF5)簡介](https://blog.xuite.net/cpy930814355/twblog/100497173-分層數據格式資料庫Hierarchical+Data+Format+(HDF5)簡介)
- HDF5可以使用MPI IO架構進行平行化之IO，如果程式中呼叫MPI_File指令
  - WRF程式有
  - CMAQ無，CMAQ是在ioapi程式庫中呼叫PnetCDF進行MPI-I/O。

### 下載
- 至[官網](https://www.hdfgroup.org/downloads/hdf5)下載
  - 因每個編譯器版本略有差異，還是下載原始碼自行編譯較為穩定
### 編譯
- 因[netCDF]()會用到[HDF5]()的程式庫，因此要先編譯[HDF5]()
  - 同一版本可能會編譯好幾次，建議在目錄下另建`build_VER`目錄以資識別
  - 要記得開啟`--enable-fortran`、這樣netcdff才會連結得上
  - 開啟`--enable-parallel`才會開啟MPI-I/O
- 編譯順利為傳統之configure->make->make install順序
- intel version

```bash
$ cat ~/MyPrograms/hdf5-1.10.5/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
FC=ifort FCFLAG='-auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp' CC=icc ../configure --prefix=/opt/hdf/hdf5_intel --enable-parallel --enable-fortran 
```
- gnu version

```bash
FC=gfortran ./configure --enable-fortran --with-zlib=/usr/lib64 --prefix=/opt/hdf/hdf5_gcc
```
### 其他程式庫
- 編譯過程會連結到電腦裏既有的libz.a、libpng.a、libld.a、libm.a等
- 在$PREFIX/lib/libhdf5.settings中有詳細的說明
  - 如果在/lib64目錄下沒有這些程式庫，就必須建立LD_LIBRARY_PATH將其連結起來。


## netCDF

### netCDF編譯
- [WRF]()程式會需要`libnetcdf.a`及`libnetcdff.a`2個檔案
- [netcdf-c]()環境設定如下

```bash
cat ~/MyPrograms/netCDF/netcdf-c-4.7.1/build_intel/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64

CC=icc CPPFLAGS=-I/opt/hdf/hdf5_intel/include LDFLAGS=-L/opt/hdf/hdf5_intel/lib ../configure --prefix=/opt/netcdf/netcdf4_intel  --disable-dap --with-zlib=/usr/lib64 --enable-netcdf4
```    
- [netcdf-f]()環境設定如下

```bash
kuang@DEVP ~/MyPrograms/netCDF/netcdf-fortran-4.5.2/build_intel
$ cat ~/MyPrograms/netCDF/netcdf-fortran-4.5.2/build_intel/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
export NCDIR=/opt/netcdf/netcdf4_intel
export NFDIR=/opt/netcdf/netcdf4_intel
FC=ifort CC=icc CPPFLAGS=-I${NCDIR}/include LDFLAGS=-L${NCDIR}/lib FCFLAG=' -auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp' ../configure --prefix=${NFDIR} --enable-netcdf4
```
## Reference
- 陳柏源, [分層數據格式資料庫Hierarchical Data Format (HDF5)簡介](https://blog.xuite.net/cpy930814355/twblog/100497173-分層數據格式資料庫Hierarchical+Data+Format+(HDF5)簡介), 2011-08-20
- 北京焱融科技有限公司, [关于MPI-IO，你该知道的](https://www.yanrongyun.com/zh-cn/blogs/all-you-should-know-about-MPI-IO), 2021-03-08 11:30
- William Gropp, [Lecture 32: Introduction to MPI I/O](https://wgropp.cs.illinois.edu/courses/cs598-s16/lectures/lecture32.pdf)
  - 啟用MPI IO需在程式內使用下列指令：`MPI_File_open`, `MPI_File_write`, `MPI_File_read`, `MPI_File_close`