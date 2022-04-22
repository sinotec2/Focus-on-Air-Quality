---
layout: default
title: 國網環境與Slurm
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 5
date: 2022-04-18 13:17:33
last_modified_date: 2022-04-18 13:17:43
---

# OTP, Module and Slurm
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

## 快速取得OTP的作法
- OTP的輸入需要在30秒內執行點選(double click)、Ctrl-C複製、切回ssh登入界面、Ctrl-V貼上，過程還蠻緊張的，貼慢一點就得重來。
- [教材](https://drive.google.com/drive/mobile/folders/1_GdUsRXQU1p8QhwwDbhz-nVhgUQBbftX?usp=sharing)中提到國網OTP的相機掃描功能(設定如下圖1)，是利用瀏覽器自動填入密碼提供的方便門
  - 有Microsoft會員帳號的用戶，使用[Edge]()及Authenticator for Microsoft Edge
  - 使用google帳戶及Chrome者，下載[authenticator擴充套件](https://chrome.google.com/webstore/detail/authenticator/bhghoamapcdpbohphigoooaddinpkbai)  
- 下載Authenticator後、在瀏覽器設定處(右上方選單)啟用該延伸功能
  - 點選圖2的icon後會告知還沒有設定使用者帳號，點選[-]方塊將國網右上方二維條碼納入(內容為登入使用者名稱、只需執行一次)
  - 點選右上方二維條碼icon(圖2)便可隨時顯示6位數OTP(圖3)，點一次即複製。
    - 藍色數字表示正常
    - 如果出現紅字表示時限快到、可以等等再點一次
  - 再到ssh登入對話框貼上即可
  
| ![OTP_iphone.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/OTP_iphone.PNG) |
|:--:|
| <b>圖1以手機相機取得國網OTP並由Edge自動填入</b>|

| ![chrome_extend.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/chrome_extend.PNG) |
|:--:|
| <b>圖2啟動Chrome Authenticator擴充套件後右上方出現icon </b>|

| ![6digit.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/6digit.PNG) |
|:--:|
| <b>圖3Chrome顯示6位數OTP，只需在數字上點1次即複製到剪貼簿</b>|

## Usage of module commands
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

### modules in intel.sh
- 須按照順序載入環境
- 主要影響PATH及LD_LIBRARY_PATH等2個環境變數

```bash
module load compiler/intel/2021
module load IntelMPI/2021
module load hdf5/1.12
module load netcdf/4.7.4
module load pnetcdf/1.12.2
```
- 因遇記憶體不足問題(如下)，module load還不如直接設定LD_LIBRARY_PATH，啟用下列5個目錄的程式庫即可。

```bash
#sinotec2@lgn303 ~/cmaq_recommend/1901
#$ head buff_CMAQ_CCTMv532_sinotec2_20220416_150403_523992255.txt
[1650121445.321789] [cpn3286:242769:0]          select.c:514  UCX  ERROR   no active messages transport to <no debug data>: posix/memory - Destination is unreachable, sysv/memory - Destination is unreachable, self/memory0 - Destination is unreachable, cma/memory - no am bcopy, knem/memory - no am bcopy
```

```bash
#$ source ~/cmaq_recommend/exec.sh
#$ cat ~/cmaq_recommend/exec.sh
#!/bin/bash
P0=/opt/ohpc/Taiwania3/libs/Iimpi-2021/hdf5-1.12/lib:/opt/ohpc/Taiwania3/libs/Iimpi-2021/szip-2.1.1/lib
P1=/opt/ohpc/Taiwania3/libs/Iimpi-2020/pnetcdf-1.12.2/lib
P2=/opt/ohpc/Taiwania3/pkg/cmp/compilers/intel/compilers_and_libraries_2017.7.259/linux/compiler/lib/intel64_lin
P3=/opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib
P4=/opt/ohpc/Taiwania3/libs/libfabric/1.11.2/lib
LD_LIBRARY_PATH=${P0}:${P1}:${P2}:${P3}:${P4}
```

### python
- @clogin2
  - module load biology/Python3/default
  - 為py37
- @lgn303
  - module purge
  - module load pkg/Anaconda3
  - module load pkg/Python/3.9.7
  - 另有py37
- 執行時必須加註版本(python3)，否則會啟動python2 (/usr/bin/python)

### 其它可用模組
- $ module avail


      -------------------------------------------------------- /opt/ohpc/Taiwania3/modulefiles --------------------------------------------------------
      abaqus/2018                           biology/SRAToolkit/2.10.2                libs/ucx/1.11.2                       (D)
      abaqus/2021                    (D)    biology/SRAToolkit/2.11.1         (D)    libs/ucx/1.12.1
      adf/2021.102-intelmpi                 biology/Samtools/1.13                    lsdyna/R10.1.0
      ansoft/v20.1                          biology/SolexaQA/3.1.7.1                 lsdyna/R11.2.2
      ansys/CFX/v162                        biology/Trimmomatic/0.39                 lsdyna/R12.0.0                        (D)
      ansys/CFX/v170                        biology/Trinity/2.12.0                   matlab/R2021b
      ansys/CFX/v182                        biology/arcasHLA/arcasHLA                molpro/2021.2
      ansys/CFX/v192                        biology/aria2c/1.36.0                    nvidia/cuda/10.0
      ansys/CFX/v2019r3              (D)    biology/bcftools/1.13                    nvidia/cuda/11.0                      (D)
      ansys/Fluent/v162                     biology/bonito/0.4.0                     nvidia/hpc_sdk/20.11
      ansys/Fluent/v170                     biology/bowtie2/2.4.2                    nvidia/hpc_sdk/21.5                   (D)
      ansys/Fluent/v182                     biology/fastp/0.22.0                     pkg/Anaconda3
      ansys/Fluent/v192                     biology/hap.py/0.3.15                    pkg/Python/3.9.7
      ansys/Fluent/v2019r3           (D)    biology/htslib/1.13                      pkg/R/4.1.2
      ansys/ICEMCFD/v162                    biology/jvarkit/jvarkit                  qchem/5.4.1-omp
      ansys/ICEMCFD/v170                    biology/kmersGWAS/0.2                    rcec/cmake/3.16.3-intel18
      ansys/ICEMCFD/v182                    biology/kraken2/2.1.2                    rcec/cmake/3.16.3-intel19b
      ansys/ICEMCFD/v192                    biology/parabricks/3.6.0                 rcec/cmake/3.16.3-intel19             (D)
      ansys/ICEMCFD/v2019r3          (D)    biology/parabricks/3.7.0          (D)    rcec/cmake/3.20.0
      ansys/workbench_APDL/v162             biology/pepper/0.7.5                     rcec/gcc/9.4.0.bak
      ansys/workbench_APDL/v170             biology/pigz/2.6                         rcec/gcc/9.4.0
      ansys/workbench_APDL/v182             biology/tabix/0.2.5                      rcec/gcc/2020u4                       (D)
      ansys/workbench_APDL/v192             biology/yicheng/ALLPATHS-LG/52488        rcec/hpcx-ompi/4.1.1a1-intel18
      ansys/workbench_APDL/v2019r3   (D)    biology/yicheng/VCFtools/0.1.16          rcec/hpcx-ompi/4.1.1a1-intel19a       (D)
      biology/ABySS/52488                   biovia/ds21                              rcec/hpcx-ompi/4.1.1a1-intel19b
      biology/BEDTOOLS/2.29.1               biovia/ms21                       (D)    rcec/hpcx-ompi/4.1.1a1-intel19
      biology/BWA/0.7.17                    compiler/aocc/2.3.0                      rcec/lapack/3.8.0-intel19
      biology/CD-HIT/4.8.1                  compiler/gcc/4.8.5                (D)    rcec/lapack/3.9.0-intel19
      biology/FASTX-Toolkit/0.0.14          compiler/gcc/6.3.0                       rcec/lapack/3.9.1-intel19             (D)
      biology/GATK/3.8.1.0                  compiler/gcc/7.5.0                       rcec/libncomp/20200827
      biology/GATK/4.0.3.0                  compiler/gcc/8.3.0                       rcec/mvapich/2.3.5-intel19
      biology/GATK/4.2.0.0                  compiler/gcc/9.4.0                       rcec/ncl/6.6.2
      biology/GATK/4.2.1.0                  compiler/gcc/10.2.0                      rcec/python/ufs_env
      biology/GATK/4.2.3.0           (D)    compiler/intel/2018u4                    rcec/python/3.5.10-intel19            (D)
      biology/GEMMA/0.98.5                  compiler/intel/2020u2                    rcec/time/1.9
      biology/HLA-HD/1.4.0                  compiler/intel/2020u4             (D)    rcec/tools
      biology/Jellyfish/2.3.0               compiler/intel/2021                      rcec/udunits/2.1.24-intel19-mpich
      biology/Kallisto/0.44.0               compiler/nvhpc/20.11                     rcec/udunits/2.1.24-intel19-ompi      (D)
      biology/Kallisto/0.46.1               compiler/nvhpc/21.5               (D)    rcec/ufs-ext/bbc872c-intel18-ompi
      biology/Kallisto/0.46.2        (D)    compiler/pgi/2018                        rcec/ufs-ext/bbc872c-intel18
      biology/LEfSE/1.1.2                   coventor/v10.5                           rcec/ufs-ext/bbc872c-intel19b-ompi
      biology/MEFFT/7.490                   gaussian/g09                             rcec/ufs-ext/bbc872c-intel19-mpich
      biology/MEME/5.3.2                    gaussian/g16                      (D)    rcec/ufs-ext/bbc872c-intel19-mvapich
      biology/Manta/1.6.0                   libs/GSL/2.6                             rcec/ufs-ext/bbc872c-intel19-mvapicha
      biology/NetMHCpan/4.0                 libs/OFI/libfabric/1.11.2                rcec/ufs-ext/bbc872c-intel19-ompi     (D)
      biology/NetMHCpan/4.1          (D)    libs/boost/1.67.0                        rcec/ufs-ext/bbc872c-intel19
      biology/OpenJDK/17.0.2+8              libs/gdal/3.4.1                          rcec/ufs-ext/2.0.0-intel18
      biology/OptiType/1.3.2                libs/geos/3.9.2                          rcec/ufs-libs/1.3.0-intel18
      biology/Perl/perl-log-log4perl        libs/hwloc/2.1.0                         rcec/ufs-libs/1.3.0-intel19-mpich
      biology/Perl/5.28.1            (D)    libs/hwloc/2.5.0                  (D)    rcec/ufs-libs/1.3.0-intel19-mvapich
      biology/Python/2.7.18                 libs/mkl/2020                            rcec/ufs-libs/1.3.0-intel19-ompi      (D)
      biology/Python/3.6.10                 libs/pmix/3.2.3                          rcec/ufs-libs/1.3.0-intel19
      biology/Python/3.7.10          (D)    libs/proj/7.2.1                          schrodinger/sch2021-4
      biology/R/4.0.0                       libs/singularity/3.7.1                   tools/automake/1.16.4
      biology/R/4.1.2                (D)    libs/sqlite/3.37.2                       tools/cmake/3.21.2
      biology/Rclone/1.59.0-DEV             libs/szip/2.1.1                          tools/git/2.33.0
      biology/SPAdes/3.15.3                 libs/tcl/tk/8.6.11                       tools/grads/2.2.1
      biology/SRAToolkit/2.9.6              libs/ucx/1.11.0

      Where:
      D:  Default Module

      Use "module spider" to find all possible modules.
      Use "module keyword key1 key2 ..." to search for all possible modules matching any of the "keys".



## slurm commands
- [slurm](https://zh.wikipedia.org/wiki/Slurm工作调度工具)是全球超級電腦或叢集電腦常用的資源調度工具，也為國網所採用。
- [簡易指令](https://www2.nsysu.edu.tw/gpu/submit.html) screen類似tmux可以設置特定slurm環境

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
- $1=200
- $2=run.cctm.03.csh

```bash
#sinotec2@lgn301 ~/cmaq_recommend/1901
#$ cat ~/bin/gorun.sh 

pro="ENT111046"
queue="ct224"

sbatch --get-user-env --account=$pro --job-name=cmaqruns --partition=${queue} --ntasks=${1} --cpus-per-task=1 --nodes=5 --ntasks-per-node=40  ${2}
```
### SQUEUE

```bash
squeue|grep 'NAME|$USERNAME'
```

    $ squeue|H
      JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
    1403160      ct56 st_archi minhuilo PD       0:00      1 (Dependency)
    1403488      ct56       C1 ericente  R       0:30      1 cpn3605
    1386477      ct56     vasp u9576505  R   17:07:56      1 cpn3166
    1376874      ct56 Sheet-A1 bnbmax00  R 2-19:40:55      1 cpn3014
    1370483      ct56 StraL7e- jimmy081  R 3-21:18:00      1 cpn3185
    1372350      ct56  noP.txt jimmy081  R 3-16:12:19      1 cpn3062
    1385787      ct56     vasp percy097  R   20:10:41      1 cpn3168
    1376233     ct224 testGoPa u8926524  R 2-22:08:57      3 cpn[3493-3495]
    1403119      ct56 config-S u5411358  R    1:23:47      1 cpn3020

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


### slurm-$JOB_ID.out
- 為執行檔的standard output，會從一開始執行就累積
  - 相對的CTM*只會記錄每日的print_out，檔案較小
  - 可以用grepDDD檢視進度

```bash
#$ cat ~/bin/grepDDD
grep -n DDD $(ls -rt CTM*|tail)|tail -n1
```

