---
layout: default
title: 配置及編譯
parent: WRF-chem
grand_parent: "WRF"
nav_order: 1
date: 2021-12-27 16:53:48
last_modified_date: 2021-12-27 16:53:42
tags: wrf wrf-chem
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
- 基本上**WRF-chem**的配置與**WRF**沒有差異，需要netCDF、HD5、JASPER、Z等程式庫及內含文件。
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
- 目前centos上的[gfortran]()雖然編譯成功，但wrf.exe無法執行，原因未明、還待偵錯。(版本為gcc (GCC) 4.8.5 20150623)
- [ifort]()可以成功編譯、執行，路徑及環境變數設定如下(csh)

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

set LD_LIBRARY_PATH=/opt/netcdf/netcdf4_intel/lib:/opt/hdf/hdf5_intel/lib:/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin
```
- 支援軟體的版本
  - 多工使用mpich-3.4.2
  - netCDF使用netcdf-c-4.7.1  netcdf-fortran-4.5.2
  - HDF5使用hdf5-1.10.5
  - 執行時必須設定**LD_LIBRARY_PATH**
  ```bash
  LD_LIBRARY_PATH=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin /opt/mpich/mpich-3.4.2-icc/bin/mpirun -np 90 wrf.exe
  ```

### HDF5編譯
- 有關HDF5的編譯與應用，詳見[NC相關程式庫之編譯](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/lib_comp/)
- 因[netCDF]()會用到[HDF5]()的程式庫，因此要先編譯[HDF5]()
  - 要記得開啟`--enable-fortran`

```bash
cat ~/MyPrograms/hdf5-1.10.5/cfg.kng
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
FC=ifort ./configure --enable-fortran --with-zlib=/usr/lib64 --prefix=/opt/hdf/hdf5_intel
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

## macOS上的裝置
- 因為**macOS**上可以接受[brew]()建置的[netcdf4]()及[hdf5]()程式庫，不必重新編譯，相對單純些。
- 但因**macOS**上的[gcc]()版本更新很快，須留意版本的一致性。

### 支援軟體版本管理
- 因為[brew]()建置的軟體都會放在`/usr/local/Cellar/`下按照名稱及版本存放，因此引用較為方便
- 路徑是呼叫到編譯程式的關鍵，要控制編譯程式的版本就要先行設定好程式路徑。

```bash
setenv NETCDF /usr/local/Cellar/netcdf/4.8.1
setenv HDF5 /usr/local/Cellar/hdf5/1.12.1
setenv JASPERLIB /usr/local/Cellar/jasper/2.0.33/lib
setenv JASPERINC /usr/local/Cellar/jasper/2.0.33/include
setenv WRF_DIR /Users/WRF4.3/WRF-CHEM

setenv PATH /usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/X11/bin:/usr/local/opt/coreutils/libexec/gnubin:.:/Users/kuang/bin:/opt/local/bin:/opt/local/sbin:/opt/grads-2.2.1/bin
setenv EM_CORE 1
setenv WRF_CHEM 1
```
- 編譯與執行軟體版本

```bash
/usr/local/bin/mpirun --version
mpirun (Open MPI) 4.1.2

$ /usr/local/bin/gcc --version
gcc (Homebrew GCC 11.2.0_3) 11.2.0

$ /usr/local/bin/gfortran --version
GNU Fortran (Homebrew GCC 11.2.0_3) 11.2.0
```
### 編譯軟體的版本管理
- 因為macOS上的[gcc]()升級很快，要特別注意[gcc]()、[gfortran]()與[mpicc]()、[mpif90]()等程式其間版本的一致性。
  - 如不一致將出現錯誤：`implicit declaration of function 'sym_forget' [-werror,-wimplicit-function-declaration] sym_forget()`
  - 即使增加**CCFLAG**如`-std=c89`、`-std=gnu99`等，皆無法過關。
- 10版以上的[gfortran](https://matsci.org/t/macos-install-gfortran-issues/4990)對副程式呼叫的引數個數、形態等檢查較為嚴格，因此編譯時要增加[選項](https://gcc.gnu.org/onlinedocs/gfortran/Fortran-Dialect-Options.html)：

```bash
kuang@MiniWei /Users/WRF4.3/WRF-chem
$ grep allow configure.wrf
FCBASEOPTS      =       $(FCBASEOPTS_NO_G) $(FCDEBUG)  -fallow-argument-mismatch -fallow-invalid-boz
```
- 注意：
  - 錯誤訊息為`Error: Rank mismatch between actual argument at (1) and ...`
  - 要注意加在`configure.wrf`檔案內適當位置，並確認會對FC產生作用。
  - `configure.wrf`檔案會在`./configure`動作後被覆蓋。

## 輸出變數項目之管理
### Modification of Registry/registry.chem file
- 除了輸出濃度之外，WRF-chem亦能輸出逐時之揚沙量。修改設定如下：
  1. clean -a、configure
  1. 在Registry/registry.chem檔案內，將EDUST1~5的IO形式增加`h` (means: history file output)、存檔
  1. 其單位WRFV4.0為&mu;gm<sup>-2</sup>s<sup>-1</sup>(`./chem/module_uoc_dust.F:243: emis_dust(i,1,j,p_edust5)=bems(5)*converi      ![kg/m2/s] -> [ug/m2/s]`)、WRFV4.3.2為kg/m2。
  1. compile >& compile.log
  1. 結果wrfout檔案中就會增加EDUST1~5之排放量

### Reusults
```python
$ ncdump -h $nc|grep float|grep DUST
        float EDUST1(Time, klevs_for_dust, south_north, west_east) ;
        float EDUST2(Time, klevs_for_dust, south_north, west_east) ;
        float EDUST3(Time, klevs_for_dust, south_north, west_east) ;
        float EDUST4(Time, klevs_for_dust, south_north, west_east) ;
        float EDUST5(Time, klevs_for_dust, south_north, west_east) ;
        float DUST_FLUX(Time, south_north, west_east) ;
        float DUST_1(Time, bottom_top, south_north, west_east) ;
        float DUST_2(Time, bottom_top, south_north, west_east) ;
        float DUST_3(Time, bottom_top, south_north, west_east) ;
        float DUST_4(Time, bottom_top, south_north, west_east) ;
        float DUST_5(Time, bottom_top, south_north, west_east) ;
```
- 注意
  - DUST_FLUX無數值、全為0
  - 第1軸`klevs_for_dust`不為[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)所解析，需使用[ncrename](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#維度更名ncrename)將其更名為`bottom_top`

## 程式編譯
- 目前沒有centos平台上[WRF]()或[WRF-chem]()的執行檔可供下載。
- macOS上雖然有較早先的[WRF4.1](https://github.com/WRF-CMake/wrf)版執行檔，但因為搭配的[gcc]()較舊，新的OS上已經無法順利進行[brew]()，必須自行編譯。
- 編譯步驟
  1. 解壓縮、進入全新的程式碼目錄
  1. 進入`csh`環境
  1. 設定路徑及環境變數(見前)
  1. 執行`./configure`，選定編譯方式。(選擇[dmp](https://www.researchgate.net/figure/Comparison-of-SMP-and-DMP-Architecture_fig1_265002373)方式以便後續執行時能指定恰當的核心數量、單機或跨機)
  1. 確認`configure`的結果，如發現任何支援軟體不能使用，系統會報錯，需確實準備好再開始編譯。
  1. 如有需要修改`configure.wrf`內容，可以在此階段進行(macOS)
  1. 如無錯誤，繼續執行`compile em_real >& em_real.log &`、確認`./main`目錄下會產生`real.exe`等執行檔
  1. 如無錯誤，繼續執行`compile wrf >& wrf.log &`、確認`./main`目錄下會產生`wrf.exe`執行檔

## WRF-chem的測試
- 在沒有啟動化學(`&chem`) 設定情況下，WRF-chem的表現理論上是與傳統編譯的WRF完全一樣，因此可以使用一既有個案，以WRF-chem程式來執行，看結果是否相同。
- 以最簡單的揚塵個案進行模擬
 
## Reference
- GCC team, **Options controlling Fortran dialect**, [gnu.org](https://gcc.gnu.org/onlinedocs/gfortran/Fortran-Dialect-Options.html)