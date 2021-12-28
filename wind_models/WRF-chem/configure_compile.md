---
layout: default
title: 配置及編譯
parent: WRF-chem
grand_parent: "WRF"
nav_order: 1
date: 2021-12-27 16:53:48
last_modified_date: 2021-12-27 16:53:42
---

# WRF-chem 的配置及編譯 

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
- 基本上**WRF-chem**的配置與**WRF**沒有差異，需要netCDF、HD5、JASPER、Z等程式庫及包括檔。
- 唯一差異是必須開啟**chem**相關的環境變數

```bash
setenv EM_CORE 1
setenv WRF_CHEM 1
```

## WRF-chem程式碼之下載
- 雖然[WRF4.3](https://github.com/wrf-model/WRF)REPO目錄下也有`chem`，然其檔案並非最新、個數也不夠，還是由[官網](https://www2.mmm.ucar.edu/wrf/users/download/get_sources.html#WRF-Chem)下載重做為宜。
- 因[WRF]()進版時也搭配新版的[WPS](https://github.com/wrf-model/WPS)(由3版進到4版)，因此也要下載、裝置同一版本的[WPS]()。
- 注意
  - 編譯過程如有失敗，使用[clean](https://github.com/wrf-model/WRF/blob/master/clean)並不能完全清乾淨，還是需要重新解壓縮比較妥當，所以如未完成編譯，**不要**在目錄下存放任何重要檔案。
  - 雖然[WRF-chem]()包含有[WRF]()，但畢竟為不同領域的專家同時發展，因此有可能發生版本上先後的差異，建議**不要**在原來的[WRF]()目錄下發展，以避免混淆，即使很多工具是一樣、是可以互通的。

## centos上的裝置
- 目前centos上的gfortran雖然編譯成功，但wrf.exe無法執行，原因未明、還待偵錯。(版本為gcc (GCC) 4.8.5 20150623)
- ifort可以成功編譯、執行，路徑及環境變數設定如下(csh)
  - 多工使用mpich-3.4.2
  - netCDF使用netcdf-c-4.7.1  netcdf-fortran-4.5.2
  - HDF5使用hdf5-1.10.5

```bash
source /opt/intel/bin/compilervars.csh intel64
source /opt/intel_f/bin/compilervars.csh intel64
setenv PATH /opt/mpich/mpich-3.4.2-icc/bin:$PATH
setenv NETCDF /opt/netcdf/netcdf4_intel
setenv HDF5 /opt/hdf/hdf5_intel
JASPERLIB=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib
JASPERINC=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/include

setenv WRF_DIR /nas1/WRF4.0/WRF_chem
setenv EM_CORE 1
setenv WRF_CHEM 1

set LD_LIBRARY_PATH=/nas1/WRF4.0/WRF_chem/WPS/lib:/opt/intel/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin
```

### HDF5編譯
- 因netCDF會用到HDF5的程式庫，因此要先編譯HDF5
  - 要記得開啟`--enable-fortran`

```bash
cat ~/MyPrograms/hdf5-1.10.5/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
FC=ifort ./configure --enable-fortran --with-zlib=/usr/lib64 --prefix=/opt/hdf/hdf5_intel
```

### netCDF編譯
- netcdf-c環境設定如下

```bash
cat ~/MyPrograms/netCDF/netcdf-c-4.7.1/build_intel/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64

CC=icc CPPFLAGS=-I/opt/hdf/hdf5_intel/include LDFLAGS=-L/opt/hdf/hdf5_intel/lib ../configure --prefix=/opt/netcdf/netcdf4_intel  --disable-dap --with-zlib=/usr/lib64 --enable-netcdf4
```    
- netcdf-f環境設定如下

```bash
kuang@DEVP ~/MyPrograms/netCDF/netcdf-fortran-4.5.2/build_intel
$ cat ~/MyPrograms/netCDF/netcdf-fortran-4.5.2/build_intel/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
export NCDIR=/opt/netcdf/netcdf4_intel
export NFDIR=/opt/netcdf/netcdf4_intel
FC=ifort CC=icc CPPFLAGS=-I${NCDIR}/include LDFLAGS=-L${NCDIR}/lib FCFLAG=' -auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp' ../configure --prefix=${NFDIR} --enable-netcdf4
```


## macOS上的裝置
- 
## Reference
