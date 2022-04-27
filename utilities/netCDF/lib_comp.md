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

### 下載
- 至[官網](https://www.hdfgroup.org/downloads/hdf5)下載
  - 因每個編譯器版本略有差異，還是下載原始碼自行編譯較為穩定
### 編譯
- 因[netCDF]()會用到[HDF5]()的程式庫，因此要先編譯[HDF5]()
  - 同一版本可能會編譯好幾次，建議在目錄下另建`build_VER`目錄以資識別
  - 要記得開啟`--enable-fortran`、這樣netcdff才會連結得上
- 編譯順利為傳統之configure->make->make install順序
- intel version

```bash
$ cat ~/MyPrograms/hdf5-1.10.5/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
FC=ifort FCFLAG='-auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp' CC=icc ../configure --prefix=/opt/hdf/hdf5_intel
```
- gnu version

```bash
FC=gfortran ./configure --enable-fortran --with-zlib=/usr/lib64 --prefix=/opt/hdf/hdf5_gcc
```

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
