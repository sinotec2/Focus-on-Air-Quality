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

# executable file
- 國網臺灣杉3號上的執行檔、搭配高速平行運算的程式庫

```bash
#sinotec2@lgn301 ~/cmaq_recommend/CCTM/scripts/BLD_CCTM_v532_intel
-rwxr-xr-x 1 sinotec2 TRI1111114  24M Nov 16 09:05 CCTM_v532.exe*
-rwxr-xr-x 1 sinotec2 TRI1111114 18M Feb 15 15:18 cmaq_recommend/POST/combine/scripts/BLD_combine_v532_intel/combine_v532.exe
```
# lib links
## cmaq_recommand/lib下的連結
### intel目錄

```bash
#sinotec2@clogin2 ~/cmaq_recommend/lib/x86_64/intel
# ls -lh ~/cmaq_recommend/lib/x86_64/intel
drwxr-xr-x 2 sinotec2 TRI1111114 4.0K Aug 31  2021 ioapi
lrwxrwxrwx 1 sinotec2 TRI1111114  173 Sep 23  2021 mpi -> /opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib:/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/lib/release:/opt/ohpc/Taiwania3/pkg/intel/2021/mpi/2021.1.1/libfabric/lib
drwxr-xr-x 2 sinotec2 TRI1111114 4.0K May 19  2021 netcdf
drwxr-xr-x 2 sinotec2 TRI1111114 4.0K May 19  2021 netcdff
```

### netcd lib
```bash
#sinotec2@lgn301 ~/cmaq_recommend/lib/x86_64/intel/netcdf
lrwxrwxrwx 1 sinotec2 TRI1111114 56 May 19  2021 include -> /opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/include
lrwxrwxrwx 1 sinotec2 TRI1111114 52 May 19  2021 lib -> /opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib
#$ ls -lrth /opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib
-rw-r--r-- 1 root root 2.9M Mar 16  2021 libnetcdf.a
-rw-r--r-- 1 root root 975K Mar 16  2021 libnetcdff.a
```
### ioapi lib
```bash
lrwxrwxrwx 1 sinotec2 TRI1111114 33 Aug 31  2021 include_files -> /home/joy01162002/ioapi-3.2/ioapi
lrwxrwxrwx 1 sinotec2 TRI1111114 49 Aug 31  2021 lib -> /home/joy01162002/ioapi-3.2/Linux2_x86_64ifortmpi
```
### mpi lib
```bash
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

## COMBINE 腳本

### bash版本的run_combine
- 公版的combine相對較單純，只有執行濃度部分，沉降就沒有進一步分析
- 因為所有檔案都在同一個目錄，沒有run的區別，此處以ymd來成為疊代的變數，逐一處理每天的結果
- 此處的程式庫為devp/dev2的gcc與intel版本

```bash
#!/bin/bash
cpl=intel #gcc
if [ $cpl == "gcc" ];then
  LD_LIBRARY_PATH=/home/cmaqruns/2016base/lib/x86_64/gcc/netcdf/lib:/opt/netcdf/netcdf4_gcc/lib:/opt/openmpi/openmpi4_gcc/lib
  PATH=/opt/openmpi/openmpi4_gcc/bin:/usr/bin:$PATH
  export BASE=/nas2/cmaq2019/download/model/cmaq_recommend_Gfortran/POST/combine/scripts
elseif [ $cpl == "intel" ];then
  LD_LIBRARY_PATH=/opt/netcdf/netcdf4_intel/lib:/opt/mpich/mpich-3.4.2-icc/lib:/opt/hdf/hdf5_intel/lib
  PATH=/opt/mpich/mpich-3.4.2-icc/bin:/usr/bin:$PATH
  export BASE=/nas2/cmaq2019/download/model/cmaq_recommend_ifort/POST/combine/scripts
fi

export m3input=/nas2/cmaq2019/download/input/201901/grid03
# user define
#> File [1]: CMAQ conc/aconc file
#> File [2]: MCIP METCRO3D file
#> File [3]: CMAQ APMDIAG file
#> File [4]: MCIP METCRO2D file
export INFILE2="${m3input}/mcip/METCRO3D_Taiwan.nc"
export INFILE4="${m3input}/mcip/METCRO2D_Taiwan.nc"

# programs
export LC_ALL=C
export LANG=C
export EXEC=${BASE}/BLD_combine_v532_${cpl}/combine_v532.exe
export GENSPEC=N
export SPECIES_DEF=${BASE}/spec_def_files/SpecDef_cb6r3_ae7_aq.txt

for i in in $(ls daily/CCTM_ACONC_v532_${cpl}_Taiwan_*);do ymd=$(echo $i|cut -d'_' -f6|cut -c1-8);echo $ymd
export INFILE1="daily/CCTM_ACONC_v532_${cpl}_Taiwan_${ymd}.nc"
export INFILE3="daily/CCTM_APMDIAG_v532_${cpl}_Taiwan_${ymd}.nc"
export OUTFILE="out.${ymd}.conc.nc"
if [ -e ${OUTFILE} ]; then
        echo "${OUTFILE} exist..."
        exit 1
fi

time ${EXEC}
done
```

### SpecDef_cb6r3_ae7_aq.txt
- 公版模式並未提供其定義檔
- 相較USEPA之[原始設定檔](https://raw.githubusercontent.com/USEPA/CMAQ/main/CCTM/src/MECHS/cb6r3_ae7_aq/SpecDef_cb6r3_ae7_aq.txt)，公版模式多輸出6項氣象數據
  - 雲量、雲底、雲頂高、2m及地表溫度、以及平均雲中水含量
- 打開VOC(此處以USEPA的設定方式計算)
- 另創8種PM顆粒之組合
  - 顆粒水含量、金屬物質(無汞等重金屬)、OC之原生與二次分量濃度、海鹽之總量、SOC之人為與生物分量濃度、以及OTHER
- 輸出3種PM粒徑比例

```bash
#sinotec2@lgn303 ~/cmaq_recommend/1901
#$ diff ../POST/combine/scripts/spec_def_files/SpecDef_cb6r3_ae7_aq.txt /tmp/sinotec2/cmaq_recommend/1901/SpecDef_cb6r3_ae7_aq.txt
#49,55c49
< !! from v4.2019-01.conc.nc
< CFRAC           ,1         ,CFRAC[4]
< CLDT            ,m         ,CLDT[4]
< CLDB            ,m         ,CLDB[4]
< TEMP2           ,k         ,TEMP2[4]
< TEMPG           ,k         ,TEMPG[4]
< WBAR            ,g m-3     ,WBAR[4]
---
>
#114,119c108,113
< VOC             ,ppbC       ,1000.0* (PAR[1] +2.0*ETHA[1] +3.0*PRPA[1] +MEOH[1]\
<                             +2.0*ETH[1] +2.0*ETOH[1] +2.0*OLE[1] +3.0*ACET[1] \
<                             +7.0*TOL[1] +8.0*XYLMN[1] +6.0*BENZENE[1] \
<                             +FORM[1] +3.0*GLY[1] +4.0*KET[1] +2.0*ETHY[1] \
<                             +2.0*ALD2[1] + 2.0*ETHA[1] + 4.0*IOLE[1] + 2.0*ALDX[1]  \
<                             +5.0*ISOP[1] + 10.0*TERP[1]+ 10.0*NAPH[1] +10.*APIN[1])
#277,290c271
< !! from v4.2019-01.conc.nc
< PM25_H2O        ,ug m-3     ,AH2OI[1]*PM25AT[3]+AH2OJ[1]*PM25AC[3]+AH2OK[1]*PM25CO[3]
< PM25_METAL      ,ug m-3     ,PM25_MG[0]+PM25_K[0]+PM25_CA[0]
< PM25_OC_PRI     ,ugC m-3    ,APOCI[0]*PM25AT[3]+APOCJ[0]*PM25AC[3]
< PM25_OC_SEC     ,ugC m-3    ,ASOCI[0]*PM25AT[3]+ASOCJ[0]*PM25AC[3]
< PM25_OTHER      ,ug m-3     ,PM25_TOT[0]-(PM25_SO4[0]+PM25_NO3[0]+PM25_NH4[0] \
<                             +PM25_OC_PRI[0]+PM25_OC_SEC[0]+PM25_METAL[0])
< PM25_SEA        ,ug m-3     ,PM25_CL[0]+PM25_NA[0]
< PM25_SOC_BIO    ,ug m-3     ,AORGBJ[0]*PM25AC[3]
< PM25_SOC_MAN    ,ug m-3     ,AORGAJ[0]*PM25AC[3]
< RAC             ,%          ,PM25AC[3]
< RAT             ,%          ,PM25AT[3]
< RCO             ,%          ,PM25CO[3]
---
```