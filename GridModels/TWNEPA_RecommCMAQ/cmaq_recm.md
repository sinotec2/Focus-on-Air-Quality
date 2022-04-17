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

### Usage of module commands
    +-----------------------------------------------------------------------------+
    |                        Module Command Usage Information                     |
    +-----------------------------------------------------------------------------+
    |         Command          |           Module Comamnd Description             |
    +-----------------------------------------------------------------------------+
    |   $ module load [...]    |   load module(s)                                 |
    |   $ module unload [...]  |   Remove module(s)                               |
    |   $ module purge         |   unload all modules                             |
    |   $ module list          |   List loaded modules                            |
    |   $ module avail         |   List available modules                         |
    |   $ module whatis module |   Print whatis information about module          |
    |   $ module keyword string|   Search all name and whatis that contain string |
    +-----------------------------------------------------------------------------+

###    
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

## run scripts

```bash
#inotec2@lgn301 ~/cmaq_recommend/work/0000.model.source
#$ ls -lrth
total 65K
-rwxr-xr-x 1 sinotec2 TRI1111114  11K Sep 14  2021 mcip.source.csh
-rwxr-xr-x 1 sinotec2 TRI1111114 3.2K Oct  1  2021 bcon.source.csh
-rwxr-xr-x 1 sinotec2 TRI1111114 3.4K Feb 24 18:20 icon_source.csh
-rwxr-xr-x 1 sinotec2 TRI1111114  33K Mar  4 12:38 cctm.source.v5.3.1.ae7
```

## slurm commands
    +-----------------------------------------------------------------------------+
    |                   Resource Manager Command Usage Information                |
    +-----------------------------------------------------------------------------+
    |         Command          |                SLURM                             |
    +-----------------------------------------------------------------------------+
    | Submit batch jobl        | sbatch [job script]                              |
    | Request interactive shell| srun –pty /bin/bash                              |
    | Delete job               | scancel [job id]                                 |
    | Queue status             | sinfo                                            |
    | Job status               | scontrol show job [job id]                       |
    | Node status              | scontrol show node [NodeID]                      |
    +-----------------------------------------------------------------------------+

### SBATCH
```bash
#sinotec2@lgn301 ~/cmaq_recommend/1901
#$ cat ~/bin/gorun.sh 

pro="ENT111046"
queue="ct224"

module load compiler/intel/2021
module load IntelMPI/2021
module load hdf5/1.12
module load netcdf/4.7.4
module load pnetcdf/1.12.2

sbatch --get-user-env --account=$pro --job-name=cmaqruns --partition=${queue} --ntasks=${1} --cpus-per-task=1 --nodes=5 --ntasks-per-node=40  ${2}
```
### SCONTROL
```bash
#scontrol show job $j

```
### SREPORT
  Workload Characterization Key (WCKey)

```bash
#$ sreport cluster AccountUtilizationByUser All_Clusters accounts=ent111046 start=4/15/22 end=4/17/22 format=Accounts,Cluster,TresCount,Login,Proper,Used
```
--------------------------------------------------------------------------------
    Cluster/Account/User Utilization 2022-04-15T00:00:00 - 2022-04-16T23:59:59 (172800 secs)
    Usage reported in CPU Minutes
--------------------------------------------------------------------------------
        Account   Cluster TRES Count     Login     Proper Name     Used 
--------------- --------- ---------- --------- --------------- -------- 
      ent111046 taiwania3          0                               5218 
      ent111046 taiwania3          0  sinotec2        sinotec2     5218 


```bash
#sreport job sizesbyaccount accounts=ent111046 start=4/15/22 end=4/17/22
```
--------------------------------------------------------------------------------
    Job Sizes 2022-04-15T00:00:00 - 2022-04-16T23:59:59 (172800 secs)
    Time reported in Minutes
--------------------------------------------------------------------------------
      Cluster   Account     0-49 CPUs   50-249 CPUs  250-499 CPUs  500-999 CPUs  >= 1000 CPUs % of cluster 
--------- --------- ------------- ------------- ------------- ------------- ------------- ------------ 
    taiwania3 ent111046             0          5176            42             0             0      100.00% 
### Billing
- [會員中心->計畫管理->我的計畫->計畫資訊->用量統計->區間類型-日區間](https://iservice.nchc.org.tw/module_page.php?module=nchc_service#nchc_service/nchc_service.php?action=nchc_service_usage_statistic&uuid=33b3eda2-480b-40aa-97cc-5dddec5540c5&searchs_type=member&searchs_date=day&searchs_str=111/04/15&searchs_end=111/04/17&service_type=&detail_search=)

|姓名| 	狀態|	111/04/15| 	111/04/16| 	111/04/17| 	小計|
|-|-|-|-|-|-|
|曠永銓|計畫建立者|	8.5714| 	5.3424| 	0| 	13.9138|
|小計| 	  	|8.5714| 	5.3424| 	0| 	13.9138| 

#### 單價
- 13.9/(5218/200)=0.53元/min@200CPU
- [表列單價](https://iservice.nchc.org.tw/module_page.php?module=nchc_service#nchc_service/nchc_service.php?action=su_apply_step_1&prj_uuid=33b3eda2-480b-40aa-97cc-5dddec5540c5&prj_mode=personal) 0.16元/核心小時 *200/60
  - = 0.53 元/min
#### file-time estimates
- (datetime(2022,2,24,16,1)-datetime(2022,2,16,21,34)).days/11 * 12 * 24 * 60 * 0.53 元/min
  - = **7.63** days * 24 * 60 * 0.53 元/min
  - = **5828.07**元
- （12個月似乎不是連續操作）

#### job-time estimates
- 4/15~16 共run了（5+3=8）次，每次約26min/8~3min,全年應約～1200min
- 全年job billing=1200*0.53～600元