---
layout: default
title: linux entry
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-12-03 05:34:22
---

# linux快速入門

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 工作站的優點與必要性

1. 降低平台作業的相容性問題：多人、多機、多工、平行作業。
1. 資料參考與比較。考核容易。
1. 方便應用fortran/python/java/C等進行平行計算、大量數據資料處理、繪圖Linux, bash, python …
1. 為進入資訊領域的重要門檻，有利未來職涯發展。

## 認識環境

### 硬體

- 伺服器機器的位置是在公司內部
  1. 主機(console: master、DEVP)、
  1. 局部網路計算節點(node: node01~node03)、
  1. NAS(nas1、nas2)、
  1. 寬頻控制器、UPS等設備
- 外部測試機(IMacKuang@125.229.149.182)

### 遠端登入(ssh)軟體

- PC 軟體界面
  - [putty](https://www.putty.org)(文字界面)
  - [mobaXterm](https://mobaxterm.mobatek.net)(文字界面、X window圖形界面)
- 軟體提供之好用工具
  - 雙擊選取字串
  - 反白即選取複製
  - tab鍵補滿檔名或
  - 指令PageUP(或↑)補滿上個指令
  - 顏色區別工作環境

![entry1.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry1.png)

![entry2.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry2.png)

![entry3.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry3.png)

![entry4.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry4.png)

{% include download.html content="[登入工作站與下載全球任何範圍的數值地型高程數據之作業方式.doc](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/OperationSystem/登入工作站與下載全球任何範圍的數值地型高程數據之作業方式.doc)" %}

### 檔案交換軟體(目錄)

- samba網路磁碟機
  1. 登入(\\200.200.12.191\LX1)權限(與master上相同、nas1目前只開放進入讀取)
  2. 使用filezilla(sftp)
- sshfs

### 作業環境指令

- OS版本 `uname -a`
- 磁碟機檔案系統 `df -h`
- 目前有誰在線上 `who`, `finger`
- 最近有誰登入 `last`
- 目前有哪些程式在執行
  - `top` (table of process),  
  - `ps` (process),
    - `psg`(=`ps -ef|grep $1`, ps and grep)
- 最近1000個打過的指令
  - `history`
  - `his`(=`history |grep -i "$1" |grep -i "$2" |grep -i "$3`
- 離開或關閉ssh連線 `exit`
- 背景執行程式
- 執行程式時，最後面加上 `&`
- 即使登出程式也不會中斷`nohup` CMD & (no hang up)
- 在批次檔迴圈內執行背景工作 `sub` (=$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ...${20} &)

## 權限管理

- 工作站因為需要服務的人很多，需要完善的使用者權限管理制度。
  - unix的權限管理相對簡單、完整，管理對象只涉及目錄與檔案。
  - 身分（地位）只有3種，檔案屬性也只管3種
- 3層權限管理圈
  - user:擁有者、用`chown` (change ownner)指令修改
  - group:群組、用`chgrp` (change group)指令修改
  - other:他人
- 3種檔案屬性
  - r:read(讀)
  - w:write(寫)
  - x:excution(執行)
  - 修改屬性(change mode) `chmod -R og+w *`
- 更改別人擁有之唯讀檔案，須由原擁有者、或管理者才能做。

![entry5.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry5.png)

## 檔案管理

- 早期電腦的速度還不是很快，不太容許使用者提供錯誤、模糊的指令，所以界面也較死板，使用打字卡、終端機命令列等方式進行檔案管理。
- 隨後電腦可以接受滑鼠的訊息、將命令藏在滑鼠的動作中，現在的視窗[IDE][ide]還會提供隨打隨選之命令提示、記住使用者的習慣，讓使用者不必記住所有的指令細節。
- 雖然電腦軟體提供了非常強大的功能，但總不如使用者自行開發小工具來得實用，因此命令列指令終究不會消失。如果再加上pipeline[串接指令](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/entry_linux/#指令串接)，那就完全沒有限制了。


### 命令列指令

1. ls (list)
   - `ll` (=`ls -alh --color|more`, list in lengthy and more_mode),
   - `lst` (=`ls $1 --show-control-chars -hF --color=tty -lrt|tail`, list and sorted by time-the tail part),
   - `lsh` (=`ls $1 --show-control-chars -hF --color=tty -lrt|head` , list and sorted by time-the head part),  
   - `lsd`(=`ls $1 --show-control-chars -hF --color=tty -l|grep "^d"`, list dir. names),
   - `lsS`(=`ls $1 --show-control-chars -hF --color=tty -lrS|tail` , list and sorted by filesize),
   - `lsr`(=`ls --show-control-chars -hF --color=tty -lrtd $(findc $1)`, list $1 recursively),
2. 檔案行數與目錄總容量
   - `wc` (word count)
   - `du` (disk usage)
3. 尋找檔案
   - `which` (環境路徑中哪一個執行檔)
   - `find` (在某個目錄下找符合名稱的檔案)
   - `findc`=`find . -name "$1"`(find current directory)
   - `locate` (資料庫中尋找，太新的檔案還來不及更新可能找不到)
4. `cp` (copy), `mv` (move), `rm` (remove)
   - 前2者必須(只能)有2個檔案名稱，後者可以有很多檔名。
   - -f (force) -r (recursive) -v (verify)
   - 沒有垃圾桶可以復原，請小心使用此3指令。
5. 顯示文字檔案
   - 全文顯示`cat FILE`
   - 分頁顯示 `more FILE`
   - 頭3行 `head -n3 FILE`
   - 尾5行 `tail -n5 FILE`
   - 顯示有字串 STR的那一行:`grep STR FILE`
   - 顯示文字檔的第1列  `awk '{print $1}'` (`awkk`=awk '{print $'$1'}')
6. 目錄檔名之特殊及萬用卡
   - 現在所在的目錄 `.`
   - 現在所在的上層目錄 `..`
   - 個人本家目錄 `~`
   - 不論長度之萬用卡 `*`
   - 單一字元的萬用卡 `?`
   - 輪轉使用單一字元A~C `[ABC]`

### 軟體介面

- mobaXterm
  - 點選Session後連到遠端工作站，隨即在左側出現遠端的目錄與檔案瀏覽器，如果沒有，可以選擇sftp頁面或按下綠色微笑小圓點重新整理。
  - 雙擊黃色檔案夾可以進入目錄、雙擊檔案可以開啟檔案。如果要使用Moba內設的編輯軟體(有行號)，可以點選檔案後按右鍵選單(第二個Open with default editor)

![entry6.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry6.png)

- FileZilla（遠端管理）
- [IDE][ide]（本地管理，詳參[VS Code安裝使用](https://sinotec2.github.io/FAQ/2022/11/10/code_ug.html)）

## 指令串接

### pipeline(\|) and substitude($)

1. pipeline(\|)
   - 將pipeline(\|) 左邊指令的結果傳到右邊，進一步處理。
   - 必須分段也可以執行、
   - 並不是每一個指令都可以做為pipeline(\|)
   - (\|)右邊指令，有一定範圍，常用包括more, tail, head, grep, wc, awk, cut, sort
2. substitude($)
   - $接環境變數名稱，是呼叫出環境變數的引數
   - 後面如果接數字，是輸入批次檔的引數
   - 如果後面接(cmd)，是代表執行cmd的結果
   - 如果指令不能使用pipeline(\|) 可以考慮使用substitude($)
3. 範例
  - 前述findc、awkk、lst等等
  - gf
    - 從所在目錄位置尋找含有特定字串(\$1)的某一類(字尾為\$2)檔案：`grep 50m $(findc "*.js")`
    - `grep --color=auto -ni $1 $(findc "*.$2")`
 
### 其他指令

- Gong Yong, 2014, [50個最常用的Unix/Linux命令](https://gywbd.github.io/posts/2014/8/50-linux-commands.html)
- UNIX 常見指令教學 - 交大資工資訊中心 - [交通大學](https://cscc.cs.nctu.edu.tw/unix-basic-commands)
- [Basic-Linux-command@monash.edu.my](https://www.monash.edu.my/__data/assets/pdf_file/0006/1186098/Basic-Linux-command.pdf)

### 批次檔(bash)

- linux上可以執行的指令文字檔，稱之為批次檔(scripts)
   為直譯式的程式，語法跟OS環境是哪一個shell(C shell, Bourn Again shell, Tshell Bean shell)有關。以下bash為例必須能通過分段測試
- 判別
  - if [...]; then; else; fi;
    - 注意空格數字和文字不能混用
  - 條件式(case VAR in ; var1) done;;... esac;
- 迴圈
  - for VAR in RANGE ;do ...;done
  - VAR會按照RANGE的內容依序疊代
  - RANGE可以明列各項次、數字範圍{01..99}、英文字母範圍{Z..a}=Z , [ , ] , ^ , _ , ` , a 或混合
  - while COND;done (要搭配if指令) 
  - COND可以是 true (永不停止執行)、或者是
  - 判別式[...]
  - 中斷迴圈用break(搭配if指令)
  - 跳開不執行迴圈剩下指令用continue(搭配if指令)
- 批次檔暫時停止執行： sleep
- 變數序列
  - 定義VAR=(var0,var1 var2 ... varn)
  - 呼叫var=\${VAR[\$i]}
  - 其中的$i=0,1,...n)

- 範例：在node01~03同時執行高雄市CEMS固定源逐月的calpuff模式模擬
kuang@master /home/cpuff/2018

![entry7.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry7.png)

![entry8.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/entry8.png)

[ide]: <https://zh.wikipedia.org/zh-tw/集成开发环境> "集成开发环境、整合開發環境"
