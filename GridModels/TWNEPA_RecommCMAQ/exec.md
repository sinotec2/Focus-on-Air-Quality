---
layout: default
title: 執行檔與程式庫
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 3
date: 2022-04-18 12:31:17
last_modified_date: 2022-04-18 12:31:20
---

# EXEC and Libs
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

## executable file
```bash
#sinotec2@lgn301 ~/cmaq_recommend/CCTM/scripts/BLD_CCTM_v532_intel
-rwxr-xr-x 1 sinotec2 TRI1111114  24M Nov 16 09:05 CCTM_v532.exe*
-rwxr-xr-x 1 sinotec2 TRI1111114 18M Feb 15 15:18 cmaq_recommend/POST/combine/scripts/BLD_combine_v532_intel/combine_v532.exe
```
## lib links
```bash
#sinotec2@clogin2 ~/cmaq_recommend/lib/x86_64/intel
# ls -lh ~/cmaq_recommend/lib/x86_64/intel
drwxr-xr-x 2 sinotec2 TRI1111114 4.0K Aug 31  2021 ioapi
lrwxrwxrwx 1 sinotec2 TRI1111114  173 Sep 23  2021 mpi -> /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib:/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release:/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/libfabric/lib
drwxr-xr-x 2 sinotec2 TRI1111114 4.0K May 19  2021 netcdf
drwxr-xr-x 2 sinotec2 TRI1111114 4.0K May 19  2021 netcdff


#netcd lib
#sinotec2@lgn301 ~/cmaq_recommend/lib/x86_64/intel/netcdf
lrwxrwxrwx 1 sinotec2 TRI1111114 56 May 19  2021 include -> /opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/include
lrwxrwxrwx 1 sinotec2 TRI1111114 52 May 19  2021 lib -> /opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib
#$ ls -lrth /opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib
-rw-r--r-- 1 root root 2.9M Mar 16  2021 libnetcdf.a
-rw-r--r-- 1 root root 975K Mar 16  2021 libnetcdff.a
#ioapi lib
lrwxrwxrwx 1 sinotec2 TRI1111114 33 Aug 31  2021 include_files -> /home/joy01162002/ioapi-3.2/ioapi
lrwxrwxrwx 1 sinotec2 TRI1111114 49 Aug 31  2021 lib -> /home/joy01162002/ioapi-3.2/Linux2_x86_64ifortmpi
#mpi lib
mpi -> /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib:/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release:/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/libfabric/lib
#$ ls -lrth /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/*.a|T
-rw-r--r-- 1 root root 9.7M Nov 12  2020 /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/libmpifort.a
-rw-r--r-- 1 root root 241K Nov 12  2020 /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/libmpicxx.a
#$ ls -lrth /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release/*.a|T
-rw-r--r-- 1 root root 145M Nov 12  2020 /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release/libmpi.a
-rw-r--r-- 1 root root 363K Nov 12  2020 /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release/libmpi_ilp64.a
#$ ls -lrth /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/libfabric/lib
-rwxr-xr-x 1 root root 348K Nov 12  2020 libfabric.so.1
lrwxrwxrwx 1 root root   14 Nov 16  2020 libfabric.so -> libfabric.so.1
```
## Effective Libs
```bash
#$ cat ~/cmaq_recommend/exec.sh
#!/bin/bash
P0=/opt/ohpc/Taiwania3/libs/Iimpi-2021/hdf5-1.12/lib:/opt/ohpc/Taiwania3/libs/Iimpi-2021/szip-2.1.1/lib
P1=/opt/ohpc/Taiwania3/libs/Iimpi-2020/pnetcdf-1.12.2/lib
P2=/opt/ohpc/Taiwania3/pkg/cmp/compilers/intel/compilers_and_libraries_2017.7.259/linux/compiler/lib/intel64_lin
P3=/opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib
P4=/opt/ohpc/Taiwania3/libs/libfabric/1.11.2/lib
LD_LIBRARY_PATH=${P0}:${P1}:${P2}:${P3}:${P4}:$LD_LIBRARY_PATH 
```

# scripts

```bash
#sinotec2@clogin2 ~/cmaq_recommend/work/0000.model.source:
-rwxr-xr-x 1 sinotec2 TRI1111114 33537 Mar  4 12:38 cctm.source.v5.3.1.ae7
#sinotec2@clogin2 ~/cmaq_recommend/work/2019-01:
-rwxr-xr-x 1 sinotec2 TRI1111114  512 Mar  1 15:57 project.config
#sinotec2@clogin2 ~/cmaq_recommend/work/2019-01/grid03/cctm.raw/
-rwxr-xr-x 1 sinotec2 TRI1111114  783 Feb 25 14:39 intel.sh
-rwxr-xr-x 1 sinotec2 TRI1111114   12 Mar  1 15:57 machines8
-rwxr-xr-x 1 sinotec2 TRI1111114 1361 Mar  1 14:46 run.cctm.03.csh
```

## intel.sh and running scripts

###  intel.sh
```bash
#sinotec2@clogin2 ~/cmaq_recommend
#$ ls -lh ~/cmaq_recommend/work/2019-01/grid03/cctm.raw/intel.sh
-rwxr-xr-x 1 sinotec2 TRI1111114 783 Feb 25 14:39 /home/sinotec2/cmaq_recommend/work/2019-01/grid03/cctm.raw/intel.sh
#$ cat ~/cmaq_recommend/work/2019-01/grid03/cctm.raw/intel.sh
#!/bin/bash
#SBATCH -A GOV110197                 # Account name/project number
#SBATCH -J CMAQ532                   # Job name
#SBATCH -p ct224                     # Partiotion name
#SBATCH --ntasks=200                 # Number of MPI tasks (i.e. processes)
#SBATCH --cpus-per-task=1            # Number of cores per MPI task
#SBATCH --nodes=5                    # Maximum number of nodes to be allocated
#SBATCH --ntasks-per-node=40         # Maximum number of tasks on each node
#SBATCH -o %j.out                    # Path to the standard output file
#SBATCH -e %j.err                    # Path to the standard error ouput file


module load compiler/intel/2021
module load IntelMPI/2021
module load hdf5/1.12
module load netcdf/4.7.4
module load pnetcdf/1.12.2

./run.cctm.03.csh
```
### Effects of module load compiler

```bash
#sinotec2@lgn301 ~/cmaq_recommend/lib/x86_64/intel
#$ module load compiler/intel/2021
echo $LD_LIBRARY_PATH
## group 1 ucx
/opt/ohpc/Taiwania3/libs/ucx/1.11.2/lib/ucx:
/opt/ohpc/Taiwania3/libs/ucx/1.11.2/lib:
## group 2 mpi
/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/libfabric/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release:
/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib:
## group 3 compiler 
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/lib/x64:
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/lib/emu:
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/compiler/lib/intel64_lin:
## group 3 debugger 
/opt/ohpc/Taiwania3/pkg/intel/2021/debugger/10.0.0/dep/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/debugger/10.0.0/libipt/intel64/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/debugger/10.0.0/gdb/intel64/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/mkl/2021.1.1/lib/intel64:
/opt/ohpc/Taiwania3/pkg/intel/2021/tbb/2021.1.1/lib/intel64/gcc4.8
```
### Effects of module load hdf5
```bash
#echo $LD_LIBRARY_PATH|grep -i hdf
/opt/ohpc/Taiwania3/libs/Iimpi-2021/hdf5-1.12/lib:/opt/ohpc/Taiwania3/libs/Iimpi-2021/szip-2.1.1/lib
```

## CCTM run scripts
- 公版模式將原來USEPA提供的[run_cctm.csh](https://github.com/USEPA/CMAQ/tree/main/CCTM/scripts)腳本拆分成主程式、案例時間設定以及科學設定等3個部分。

### 主程式([run.cctm.03.csh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/run.cctm.03.csh.TXT))
- 稱之為主程式，是因為此程式會包括到其他2個設定檔，為gorun.sh的執行標的。
- 本身也有NPROC(mpirun核心數)之設定、排放量檔案的設定等等

```bash
#kuang@DEVP /nas2/cmaq2019/download
#$ diff ./model/cmaq_recommend/work/2019-01/grid03/cctm.raw/run.cctm.03.csh /nas2/cmaqruns/2019force/run.cctm.03.csh
#3,6c3,8
< set mydomain    = "grid03"
< set mympi       = "yes"
< set sfile       = "../../project.config"
< set sourcefile  = ../../../0000.model.source/cctm.source.v5.3.1.ae7
---
> set compilerString = intel
> set mydomain    = grid03
> set mympi       = yes
> set sfile       = ./project.config
> set sourcefile  = ./cctm.source.v5.3.1.ae7
> set CMAQ_HOME   = /nas2/cmaq2019/download/model/cmaq_recommend_ifort
#27c29,30
<  setenv NPCOL_NPROW "10 20"; set NPROCS   = 200
---
>  setenv NPCOL_NPROW "8 12"; set NPROCS   =  96
35c38
<  setenv N_EMIS_GR 2
---
>  setenv N_EMIS_GR 3
37,39c40,41
<  setenv GR_EMIS_002    ${cmaqproject}/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.ContEms.ncf
<
<  setenv GR_EMIS_LAB_001  biotaiwan
---
>  setenv GR_EMIS_LAB_001  bio3taiwan
>  setenv GR_EMIS_002    ${cmaqproject}/smoke/egts_l.20181225.38.d4.ea2019_d4.ncf
40a43,44
>  setenv GR_EMIS_003    ${cmaqproject}/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf
>  setenv GR_EMIS_LAB_003  basetaiwan
```

### 模擬案例與時間(project.config)
- cmaqproject：為CCTM工作目錄
- startdate/START_DATE：為icon檔案的時間，必須在mcip、smoke等檔案時間範圍之內
- runlen/END_DATE：執行時間，與END_DATE二者取最先到達者。
- MCIP_START/MCIP_END：與mcip檔案一致即可

```bash
kuang@DEVP /nas2/cmaqruns/2019force
$ cat project.config
#!/bin/csh -f

#for total settings:
 set cmaqproject = /nas2/cmaqruns/2019force/output/2019-01
 set startdate = 2018359        # YYYYDDD
 set runlen    = 8400000        # HHH0000

#for MCIP start and end time
 set MCIP_START = 2018-12-25-00:00:00.0000  # [UTC]
 set MCIP_END   = 2019-01-31-23:00:00.0000  # [UTC]

#for BC startdate
 set cmaqbcdate = ${startdate}

#for IC startdate
 set cmaqicdate = ${startdate}

#for CCTM 請配合 MCIP 的時間即可！
 set START_DATE   = "2018-12-25"
 set END_DATE     = "2019-01-31"
```

### 科學設定檔[cctm.source.v5.3.1.ae7](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/cctm.source.v5.3.1.ae7)
- CCTM主要的設定、科學設定全都在此，公版模式不允許更動內容。

```bash
#inotec2@lgn301 ~/cmaq_recommend/work/0000.model.source
#$ ls -lrth
total 65K
-rwxr-xr-x 1 sinotec2 TRI1111114  11K Sep 14  2021 mcip.source.csh
-rwxr-xr-x 1 sinotec2 TRI1111114 3.2K Oct  1  2021 bcon.source.csh
-rwxr-xr-x 1 sinotec2 TRI1111114 3.4K Feb 24 18:20 icon_source.csh
-rwxr-xr-x 1 sinotec2 TRI1111114  33K Mar  4 12:38 cctm.source.v5.3.1.ae7
```

- 本地執行須修改項目
  1. mpirun的位置
  1. mpirun的執行方式
  1. NPROCS另外在[run.cctm.03.csh]()中給定

```bash
#kuang@DEVP /nas2/cmaqruns/2019force
#$ diff cctm.source.v5.3.1.ae7 /nas2/cmaq2019/download/model/cmaq_recommend/work/0000.model.source/cctm.source.v5.3.1.ae7
#579,581c579
<   set MPI = /opt/mpich/mpich-3.4.2-icc/bin
---
>   set MPI = /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/bin
#583c581,586
<   ( /usr/bin/time -p $MPIRUN -np $NPROCS $BLD/$EXEC ) |& tee buff_${EXECUTION_ID}.txt
---
>    ${MPIRUN} -bootstrap slurm -n $SLURM_NTASKS  $BLD/$EXEC  |& tee buff_${EXECUTION_ID}.txt
```  