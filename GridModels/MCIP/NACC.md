---
layout: default
title: 解讀GFS之MCIP版本
parent: Met. Chem. Interface Proc.
grand_parent: CMAQ Model System
nav_order: 5
date: 2022-11-24 14:11:20
last_modified_date:   2022-11-24 14:11:23
---

# 解讀GFS之MCIP版本(NACC)
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

- 除了wrfout之外，是否可以有直接讀取GFS檔案、準備成CCTM所需氣象資料。答案是肯定的，就是此處要介紹的NACC(The NOAA-EPA Atmosphere-Chemistry Coupler)
- [NACC][NACC]是NOAA大氣科學家 Patrick Campbell等人所發展的轉接程式，除了GFS([FV3][FV3]版本)之外，也可讀取LAM及WRF模式結果。
- 程式下載點：https://github.com/noaa-oar-arl/NACC.git

## 編譯

- 使用netcdf4.7、ioapi3.2、mpich3.4.2
- 作者同時也提供了序列版，似乎也類似CMAQ提供的MCIP程式，雖有平行版本，但執行時卻常常出錯，還不如直接編譯成序列版本即可。

```bash
kuang@DEVP ~/MyPrograms/NACC/parallel/src
$ diff Makefile_intel_DEVP Makefile_intel_hopper
51c51
< NETCDF =   /opt/netcdf/netcdf4_hdf5P_mpich3.4.2-icc
---
> NETCDF =  /opt/sw/spack/apps/linux-centos8-cascadelake/intel-20.0.2-intel-mpi-2019.8.254/netcdf-c-4.7.4-wr/
54c54
< IOAPI_ROOT =   /opt/ioapi-3.2/Linux2_x86_64ifort
---
> IOAPI_ROOT =   /opt/sw/other/apps/linux-centos8-cascadelake/intel-19.1.2.254-impi-19.8.254/ioapi/3.2-spack
58c58
< MPI_ROOT =  /opt/mpich/mpich-3.4.2-icc_DEVP
---
> MPI_ROOT =   /opt/intel/2020.2/compilers_and_libraries_2020.2.254/linux/mpi/intel64
60,61c60
< FFLAGS  = -FR -O3 -traceback -I$(NETCDF)/include -I$(IOAPI_ROOT) -I$(MPI_ROOT)/include \
<       -I/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/include
---
> FFLAGS  = -FR -O3 -traceback -I$(NETCDF)/include -I$(IOAPI_ROOT) -I$(MPI_ROOT)/include
66,68c65
<          -L$(MPI_ROOT)/lib -lmpifort \
<       -L/opt/hdf/hdf5-1.12.1_mpich3.4.2-icc/lib \
<       -lhdf5_hl -lhdf5 -lm -lz -lcurl
---
>          -L$(MPI_ROOT)/lib -lmpifort
```

## 檔案IO

### 官網說明

**Table 1. NACC input files**

|**File Name**|**Format**|**Description**|**Required**|
|------------|------------------------------|-----------------------------------------------------|---------------------|
|InMetFiles|netCDF (WRF, FV3-GFS, or FV3-SRW App (LAM))|List of WRF, FV3-GFS, or FV3-SRW App (LAM) output files for input to NACC|required|
|InSfcFiles|netCDF (FV3-GFS or FV3-SRW App (LAM))|List of FV3-GFS or FV3-SRW App (LAM) output files for input to NACC|required (only FV3-GFS or FV3-SRW App (LAM))|
|InGeoFile|netCDF (WRF, FV3-GFS, or FV3-SRW App (LAM))|Output from WRF Geogrid processor | optional; only required if fractional land use, LAI, etc are not part of the WRF, FV3-GFS, or FV3-SRW App (LAM) output.  Offline Pre-processed NOAA-ARL "geofiles" with LAI (VIIRS 2018-2020 climatology) and LANDUSEF (based on 12-month climatological IGBP-MODIS) for the global GFSv16 Gaussian NetCDF Grid are available via FTP by request (Contact:  Patrick C. Campbell; Patrick.C.Campbell@noaa.gov)|
|InVIIRSFile|netCDF (FV3-GFS or FV3-SRW App (LAM))|Input from VIIRS data |optional; only if global NetCDF VIIRS Input COARDS file is provided. Global ~ 4km VIIRS NetCDF Grid are available via FTP by request. (Contact:  Patrick C. Campbell; Patrick.C.Campbell@noaa.gov)|

**Table 2. NACC output files**

|**File Name**|**Format**|**Description**|**Required**|
|--------------------|-----------------|------------------------------------------------------------------|---------------------------|
|GRIDDESC|ASCII|Grid description file with coordinate and grid definition information|required|
|GRID_BDY_2D|I/O API|Time-independent 2-D boundary meteorology file|required|
|GRID_CRO_2D|I/O API|Time-independent 2-D cross-point meteorology file|required|
|GRID_CRO_3D|I/O API|Time-independent 3-D cross-point meteorology file|required|
|GRID_DOT_2D|I/O API|Time-independent 2-D dot-point meteorology file|required|
|LUFRAC_CRO|I/O API|Time-independent fractional land use by category|created if fractional land use was provided in WRF's, FV3-GFS's, or FV3-SRW App's (LAM) output or in Geogrid output|
|MET_BDY_3D|I/O API|Time-varying 3-D boundary meteorology file|required|
|MET_CRO_2D|I/O API|Time-varying 2-D cross-point meteorology file|required|
|MET_CRO_3D|I/O API|Time-varying 3-D cross-point meteorology file|required|
|MET_DOT_3D|I/O API|Time-varying 3-D dot-point meteorology file|required|
|MOSAIC_CRO|I/O API|Time-varying 3-D output from mosaic land use|created if the Noah Mosaic land-surface model was run in WRF|
|SOI_CRO|I/O API|Time-varying soil properties in each soil layer|created if a land-surface model was run in WRF, FV3-GFS, or FV3-SRW App (LAM)|

### NOAA提供之預報檔案

- 目前有2個版本：16.2及16.3
- 網址 https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/
- atm檔案名稱規則
  - https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/v16.V/gfs.YYYYMMDD/HH/atmos/gfs.tHHz.atmfFFF.nc
    - V：2/3版本
    - YYYY、MM、DD、HH：4碼年，2碼月、日、時(預報起始時刻HH=00/06/12/18)
    - FFF：預報時間。目前網站只提供0~12時。
- sfc檔案(同一目錄)
  - gfs.tHHz.sfcfFFF.nc
    - HH、FFF意義同上

### 執行腳本

```bash
```

[NACC]: <https://github.com/noaa-oar-arl/NACC> "The NOAA-EPA Atmosphere-Chemistry Coupler (NACC) is adapted from the Meteorology-Chemistry Interface Processor (MCIP), and can ingest output from the Finite Volume Cubed Sphere (FV3) version of the Global Forecast System (GFS), Regional (i.e., Limited Area Model; LAM) FV3-based Short Range Weather (SRW)-Application, and the Weather Research and Forecasting WRF) Model to prepare the meteorology files that are used within the CMAQ Modeling System."
[FV3]: <https://www.gfdl.noaa.gov/fv3/> "Finite Volume Cubed Sphere，自2019年以後GFS已經使用此等網格形式"
