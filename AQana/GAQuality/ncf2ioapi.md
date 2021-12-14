---
layout: default
title: "NCF to IOAPI Converter"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 3
date: 2021-12-12 16:29:18              
last_modified_date:   2021-12-12 16:29:14
---

# 全球模式結果檔案的轉換
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
- 雖然都是`netCDF`格式的檔案，但是全球社群模式（如[MOZART](https://en.wikipedia.org/wiki/MOZART_(model))、[CAM-chem](https://wiki.ucar.edu/display/camchem/Home),、[WACCM](https://www2.acom.ucar.edu/gcm/waccm)等）檔案系統的設定、與區域模式系統（如[CMAQ](https://www.epa.gov/cmaq)、[CAMx](https://www.camx.com/about/)等），有很大的出入，最主要的差異：
  - 經緯度座標系統vs直角座標系統
  - 垂直軸的範圍、分隔方式
  - 時間標籤
  - 空氣品質濃度的名稱、意義、及單位
- 前者的檔案格式詳見[Using MOZART-4 output](https://wiki.ucar.edu/display/mozart4/Using+MOZART-4+output)
- 後者格式稱之為[IOAPI](https://www.cmascenter.org/ioapi/)格式
- 此處應用**Ramboll**公司多年來提供的[NCF2IOAPI](https://camx-wp.azurewebsites.net/getmedia/mozart2camx.26feb19_1.tgz)進行轉檔

## 下載、準備、編譯

### 下載
- NCF2IOAPI為`mozart2camx`壓縮包裡的一支程式，目前最新版本是`v3.2.1`。

### netCDF及IOAPI的編譯
- netCDF需要有libnetcdf.a（`C`） 及libnetcdff.a（`fortran`、似乎只能自行編譯）、以及相應包括檔
- IOAPI
  - 需連結前述netCDF程式庫、以及相應電腦系統硬體的程式庫`libioapi.a`、以及相應包括檔。
  - 目前IOAPI的程式庫只能自行編譯。
  - CMAQ**5.3**版之後可接受IOAPI**3.1**版本程式庫

### NCF2IOAPI的編譯
- IOAPI 3.1版本(ifort example)
```bash
kuang@master /cluster/src/CAMx/mozart2camx_v3.0/ncf2ioapi_mozart
$ cat Makefile.NCF2IOAPI.kng
FC = ifort
OMPFLAGS  = -openmp -parallel
FOPTFLAGS = -O3 -unroll -stack_temps -safe_cray_ptr \
  -convert big_endian -assume byterecl  ${MFLAGS} ${OMPFLAGS}
MFLAGS    = -traceback -xHost                                   # this-machine
ARCHLIB   = -Bstatic
OMPLIBS   = -openmp
FFLAGS = -O3 -convert big_endian
PROGRAM = NCF2IOAPI
LIBS =    -L/cluster/bld/ioapi3.1/Linux2_x86_64ifort -lioapi \
          -L/cluster/netcdf/lib -lnetcdf -lnetcdff \
         $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS)
INCLUDE = -I/cluster/bld/ioapi3.1/ioapi \
          -I/cluster/netcdf/include
RAW = get_envlist.o \
      NCF2IOAPI.opoutfile.o  NCF2IOAPI.o
.f.o:
        $(FC) $(FFLAGS) $(INCLUDE) -c -o $@ $<
.F.o:
        $(FC) $(FFLAGS) $(INCLUDE) -c -o $@ $<
$(PROGRAM):     $(RAW)
        $(FC) $(FFLAGS) $(INCLUDE) -o $(@) $(RAW) $(LIBS)
clean:
        rm -f $(PROGRAM)
```
- IOAPI 3.2版本

```bash
LIBS =    -L/opt/ioapi/Linux2_x86_64gfort -lioapi -L/opt/netcdf/lib -lnetcdf -lnetcdff
INCLUDE = -I/opt/ioapi/fixed_src \
          -I/opt/netcdf/include
```

## CAM-chem的成分
CAM模式與CMAQ模式成分對照如下表：
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CAM-chemSpec.png)

## Reference
- WEG Administrator, **Welcome to the CAM-chem Wiki**,[wiki.ucar](https://wiki.ucar.edu/display/camchem/Home),13 Jun 2021
- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.