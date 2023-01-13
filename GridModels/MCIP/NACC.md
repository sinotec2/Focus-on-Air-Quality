---
layout: default
title: 解讀GFS之MCIP版本
parent: Met. Chem. Interface Proc.
grand_parent: CMAQ Model System
nav_order: 5
date: 2022-11-24 14:11:20
last_modified_date:   2022-11-25 10:15:02
tags: mcip CMAQ GFS
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
- 每6小時預報、最多保存1天
- atm檔案名稱規則
  - https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/v16.V/gfs.YYYYMMDD/HH/atmos/gfs.tHHz.atmfFFF.nc
    - V：2/3版本
    - YYYY、MM、DD、HH：4碼年，2碼月、日、時(預報起始時刻HH=00/06/12/18)
    - FFF：預報時間。目前網站只提供0~12時。
- sfc檔案(同一目錄)
  - gfs.tHHz.sfcfFFF.nc
    - HH、FFF意義同上
- 下載指令
  
```bash
for i in {01..12};do 
for S in atm sfc;do 
  wget -q --no-check-certificate https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/v16.3/gfs.20221124/00/atmos/gfs.t00z.${S}f0$i.nc
done
done
```

## 執行

### 說明

- 原始檔案是ksh腳本，如果系統沒有安裝ksh，其與bash有很高的相似性，直接使用bash並無大礙。
- 輸入檔案的檔名規則
  - 路徑
    - required：InMetDir
    - optional：InGeoDir、InVIIRSDir_GVF、InVIIRSDir_LAI
  - NTIMES：gfs檔案的時間長度。
    - MCIP採用一一載明的策略，以適應wrfout檔名中的時間標籤。
    - NACC則採用程式自行產生，這是因為gfs系列檔名都是以整數序列來對照time frames
  - file_mm：為高空數據檔名的根、及附加檔名，中間的3碼整數略去(程式自行產生、自000開始)
  - file_sfc：同上，但為地面數據
- &USERDEFS段落
  - 為gfs檔案的網格設定
    - 可以ncdump了解檔案的設定
    - 不知何以要再次給定輸入檔案的網格系統資訊，可能gfs(FV3)檔名中並沒有相關訊息，不似wrfout。
  - mcip_start/end、intvl：從gfs檔案中擷取的時間範圍(wrfout格式、UTC)與間隔(分鐘)
- &WINDOWDEFS段落
  - 類似MCIP的X0、Y0、NCOLS、NROWS
- 輸出檔案
  - 與MCIP相同
  - 多了MOSAIC_CRO

### 腳本

```bash
#kuang@DEVP /nas2/cmaqruns/2022fcst/grid45/NACC
#$ cat run-nacc-fv3.ksh
#!/bin/bash -l

#Set number of nacc times  = processors, and # of nodes
NTIMES=12

InMetDir=/nas2/cmaqruns/2022fcst/grid45/NACC
InGeoDir=/nas2/cmaqruns/2022fcst/grid45/NACC
#InVIIRSDir_GVF=/gpfs/hps3/emc/naqfc/noscrub/Patrick.C.Campbell/viirs_gvf_test/grib2
#InVIIRSDir_LAI=/gpfs/hps3/emc/naqfc/noscrub/Patrick.C.Campbell/viirs_lai_test/
OutDir=/nas2/cmaqruns/2022fcst/grid45/NACC
ProgDir=~/MyPrograms/NACC/parallel/src
PROG=mcip.exe

if [ ! -s $InMetDir ]; then
  echo "No such input directory $InMetDir"
  exit 1
fi

if [ ! -s $InGeoDir ]; then
  echo "No such input directory $InGeoDir"
  exit 1
fi

if [ ! -d $OutDir ]; then
  echo "No such output directory...will try to create one"
  mkdir -p $OutDir
  if [ $? != 0 ]; then
    echo "Failed to make output directory, $OutDir"
    exit 1
  fi
fi

if [ ! -d $ProgDir ]; then
  echo "No such program directory $ProgDir"
  exit 1
fi

#  file_geo   =
#  file_viirs_gvf =
#  file_viirs_lai =
cd $OutDir
cat>namelist.mcip<<!
&FILENAMES
  file_gd    = 'GRIDDESC'
  file_mm    = '$InMetDir/gfs.t00z.atmf','.nc',
  file_sfc   = '$InMetDir/gfs.t00z.sfcf','.nc',
  ioform     =  1
 &END

 &USERDEFS
  inmetmodel =  3
  dx_in      =  12000
  dy_in      =  12000
  met_cen_lat_in =  0.0
  met_cen_lon_in =  0.0
  lpv        =  0
  lwout      =  1
  luvbout    =  1
  ifdiag_pbl = .FALSE.
  ifviirs_gvf = .FALSE.
  ifviirs_lai = .FALSE.
  iffengsha_dust = .FALSE.
  ifbioseason = .FALSE.
  ifcanopy    = .FALSE.
  mcip_start = "2022-11-23-01:00:00.0000"
  mcip_end   = "2022-11-23-02:00:00.0000"
  intvl      =  60
  coordnam   = "FV3_RPO"
  grdnam     = "FV3_CONUS"
  ctmlays    =  1.000000, 0.995253, 0.990479, 0.985679, 0.980781,
              0.975782, 0.970684, 0.960187, 0.954689, 0.936895,
              0.930397, 0.908404, 0.888811, 0.862914, 0.829314,
              0.786714, 0.735314, 0.645814, 0.614214, 0.582114,
              0.549714, 0.511711, 0.484394, 0.451894, 0.419694,
              0.388094, 0.356994, 0.326694, 0.297694, 0.270694,
              0.245894, 0.223694, 0.203594, 0.154394, 0.127094, 0.000000
  cutlay_collapx = 22
  btrim      =  -1
  lprt_col   =  0
  lprt_row   =  0
  ntimes     = $NTIMES
  projparm = 2., 33.,45., -97., -97., 40.
  domains = -2508000., -1716000., 12000., 12000., 442, 265
 &END

 &WINDOWDEFS
  x0         =  1
  y0         =  1
  ncolsin    =  442
  nrowsin    =  265
 &END
!

export IOAPI_CHECK_HEADERS=T
export EXECUTION_ID=$PROG

export GRID_BDY_2D=GRID_BDY_2D.nc
export GRID_CRO_2D=GRID_CRO_2D.nc
export GRID_DOT_2D=GRID_DOT_2D.nc
export MET_BDY_3D=MET_BDY_3D.nc
export MET_CRO_2D=MET_CRO_2D.nc
export MET_CRO_3D=MET_CRO_3D.nc
export MET_DOT_3D=MET_DOT_3D.nc
export LUFRAC_CRO=LUFRAC_CRO.nc
export SOI_CRO=SOI_CRO.nc
export MOSAIC_CRO=MOSAIC_CRO.nc

rm -f *.nc

# Parallel
mpirun -n 10 $ProgDir/mcip.exe
```

[NACC]: <https://github.com/noaa-oar-arl/NACC> "The NOAA-EPA Atmosphere-Chemistry Coupler (NACC) is adapted from the Meteorology-Chemistry Interface Processor (MCIP), and can ingest output from the Finite Volume Cubed Sphere (FV3) version of the Global Forecast System (GFS), Regional (i.e., Limited Area Model; LAM) FV3-based Short Range Weather (SRW)-Application, and the Weather Research and Forecasting WRF) Model to prepare the meteorology files that are used within the CMAQ Modeling System."
[FV3]: <https://www.gfdl.noaa.gov/fv3/> "Finite Volume Cubed Sphere，自2019年以後GFS已經使用此等網格形式"
