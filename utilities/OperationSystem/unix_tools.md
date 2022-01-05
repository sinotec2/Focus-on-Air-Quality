---
layout: default
title: unix系統小工具
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 檔案查詢
### ls查詢

|alias|usage|full command|arguments|
|----|----|----|----|
|lst|list and sort by **time**察看最新檔案|`ls $1 --show-control-chars -hF --color=tty -lrt\|tail`|目錄、檔案群組(需double quotes)|
|lsS|list and sort by **size**察看最大檔案-自小到大|`ls $1 --show-control-chars -hF --color=tty -lrS\|tail`|目錄、檔案群組(需double quotes)|
|lS|list and sort by **size**察看最大檔案-自大至小|`ls -alhS --color|head`|無引數|
|lsd|list the directories察看目錄|`ls $1 --show-control-chars -hF --color=tty -l|grep "^d"`|目錄、檔案群組(需double quotes)|
|lsr|recursive list跨越目錄察看尋找結果|`ls --show-control-chars -hF --color=tty -ltd $(findc $1)`|檔案群組(需double quotes)|
|lsf|list the finded results察看尋找結果/按時間排序|`ls -lrt $(find . -name "$1")`|檔案群組，不需double quotes|
|lsk|list with certain library|`/usr/local/glibc-2.16/lib/ld-linux-x86-64.so.2 --library-path .:/lib64 /bin/ls`|無引數|

### 尋找檔案
- locate、find見[程式前沿](https://codertw.com/前端開發/392150/)
- findc(find current directory)=`find . -name "$1"`
- lsr、lsf

## 執行程式
- sub
   - 在for迴圈內要將程式放在背景執行，須使用第三個腳本來吸收所有指令，在腳本內把所有指令放在背景執行，再跳回呼叫的腳本或console，否則for loop會突然中斷，回不到呼叫迴圈
   - 類似早期mainframe電腦的submit指令
   - sub=`$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} &`
- mpirun
   - 執行多工程式之管理程式
   - `-np #`指定核心個數，核心數不能多於模式維度之一半。
   - `--use-hwthread-cpus`使用硬體所能提供所有的核心數。視mpirun版本而定。
   - `-machinefile`指定主機與核心數。如網路速度不夠快，終會成為速度瓶頸。
   - eg
   ```bash
   mpirun --mca pls_rsh_agent ssh -np 2 -machinefile machines.LINUX -x OMP_NUM_THREADS ./hello
   $ cat /home/backup/sino4/kuang/MM5v3/MM5/Run/machines.LINUX
   # Change this file to contain the machines that you want to use
   # to run MPI jobs on.  The format is one host name per line, with either
   #    hostname
   # or
   #    hostname:n
   # where n is the number of processors in an SMP.  The hostname should
   # be the same as the result from the command "hostname"
   localhost:4
   sino2:4
   sino3:4
   ```
- nohup/disown/tmux：詳見[FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/tmux/)說明
