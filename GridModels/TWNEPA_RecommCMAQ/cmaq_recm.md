---
layout: default
title: Elev. Point Sources
parent: CMAQ Model System
nav_order: 6
has_children: true
permalink: /GridModels/PTSE/
date:               
last_modified_date:   2021-12-02 11:08:53
---

# 環保署建議公版模式
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
```bash
#results

sinotec2@clogin2 /work1/simenvipub01/download/model/output_cctm_combine
-rwxrwxr-x 1 simenvipub01 TRI111490 4.8G Feb 16 21:34 v4.2019-05.conc.nc
-rwxrwxr-x 1 simenvipub01 TRI111490 4.7G Feb 24 15:48 v4.2019-01.conc.nc
-rwxrwxr-x 1 simenvipub01 TRI111490 4.7G Feb 24 16:02 v4.2019-12.conc.nc
-rw------- 1 simenvipub01 TRI111490   19 Apr  6 14:57 nohup.out
#executable file
sinotec2@lgn301 ~/cmaq_recommend/CCTM/scripts/BLD_CCTM_v532_intel
-rwxr-xr-x 1 sinotec2 TRI1111114  24M Nov 16 09:05 CCTM_v532.exe*
-rwxr-xr-x 1 sinotec2 TRI1111114 18M Feb 15 15:18 cmaq_recommend/POST/combine/scripts/BLD_combine_v532_intel/combine_v532.exe
#lib links
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
## intel.sh
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

/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/lib/x64:
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/lib/emu:
/opt/ohpc/Taiwania3/pkg/intel/2021/compiler/2021.1.1/linux/compiler/lib/intel64_lin:
/opt/ohpc/Taiwania3/pkg/intel/2021/debugger/10.0.0/dep/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/debugger/10.0.0/libipt/intel64/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/debugger/10.0.0/gdb/intel64/lib:
/opt/ohpc/Taiwania3/pkg/intel/2021/mkl/2021.1.1/lib/intel64:
/opt/ohpc/Taiwania3/pkg/intel/2021/tbb/2021.1.1/lib/intel64/gcc4.8
```