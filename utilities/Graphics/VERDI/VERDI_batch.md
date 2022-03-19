---
layout: default
title:  VERDI的批次作業
parent: VERDI
grand_parent: Graphics
last_modified_date: 2022-03-19 20:13:11
---

# VERDI的批次作業
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
- 由於JAVA在執行時可以接受命令列所輸入的引數，因此不論是linux或者是PC上，原本就是以批次檔方式開啟程式。
- 運用此一特性，可以用批次檔的方式執行重複性的繪圖與計算作業，可以大幅節省工作時間。
- 除命令列的操作之外，VERDI程式內也提供了script editor可以在**程式內執行批次**。
- 此二者命令相同，然而
  - 前者具有完整的script功能(變數設定、迴圈及判斷)，缺點是重複執行JAVA程式，浪費作業時間，而
  - 後者雖然在程式內執行批次作業減省JAVA的進出時間，然而該script的設計不接受變數迴圈或判斷。
- 使用者可以視需求自行選用二者之一。

各項批次檔命令(script command)可以詳參手冊。


注意在命令列上，各command之前要加負號，之後是以空格隔開，command之間沒有順序，但是-configFile要先給定，-quit必須在最後。

在程式script editor之內，各command之前沒有負號，之後是以=(等號)隔開，command之間也沒有順序，

## 設定組態檔(-configFile configuration file)
可以儲存各種圖形介面組態(Configure)的設定內容，包括
- 圖面的主標題、次標題、
- 色階、色階的單位、
- 下標題、各軸的名稱、字型與大小等等圖面設定。

VERDI並未約定檔案的字尾，基本上，組態檔是一個文字檔，也可以從外部進行編輯。

一般VERDI會將變數名稱(-s)列為主標題(titleString)，而將檔案名稱(通常含有地域及時間項-f)列為次標題(-subTitle1, -subTitle2)，而變數的時刻與最大值則會出現在下標題，這些是可以在批次檔中控制，將內容傳給VERDI寫在圖面上，其餘不必改變的，可以按照configuration file的內容。

## 命令列預設控制(範例)

### PC ms Window 版本
- 由201002181.avrg（CAMx模擬結果）中讀取O3、產生濃度分布圖(使用臺灣縣市界地圖)，存成20100218.png檔案

```bash
@ECHO OFF
SET BATCHFILE=%~f2
CD .\plugins\bootstrap
SET JAVA=..\..\jre1.6.0\bin\java
SET JAVACMD=%JAVA% -Xmx512M –classpath "./bootstrap.jar; ./lib/saf.core.runtime.jar; ./lib/commons-logging.jar;./lib/jpf-boot.jar;./lib/jpf.jar;./lib\log4j-1.2.13.jar" saf.core.runtime.Boot
IF "%1" == "-b" GOTO scripting
IF "%1" == "-batch" GOTO scripting
%JAVACMD% %*
GOTO end
:scripting
rem %JAVACMD% %1 %BATCHFILE%
SET INP=C:\Users\4139\MyPrograms\VERDI_1.4.1\201002181.avrg -s O3[1]
SET OUT=PNG C:\Users\4139\MyPrograms\VERDI_1.4.1\20100218.png
SET TWN=C:\Users\4139\MyPrograms\VERDI_1.4.1\plugins\bootstrap\data\TWN_COUNTY.bin
SET TMS=C:\Users\4139\MyPrograms\VERDI_1.4.1\toms.cfg
%JAVACMD% -configFile %TMS% -f %INP% -g tile -mapName %TWN% -saveImage %OUT% -quit %BATCHFILE%
:end
CD ..\..\
```
### shell 版本

```bash
$ cat /opt/VERDI_2.1.3/verdi.command
#!/bin/sh

export VERDI_HOME=$(cd "$(dirname "$0")"; pwd)
export VERDI_HOME=/opt/VERDI_2.1.3

DIR=$VERDI_HOME
cd $VERDI_HOME/plugins/bootstrap

JAVA=java
JAVAMAXMEM="-Xmx4096M"

# Limit the number of default spawned threads (eca):
JAVAOPTS="--illegal-access=permit -XX:+UseParallelGC -XX:ParallelGCThreads=1 -Dlog4j.debug=false -Djava.ext.dirs=" 

JAVACMD="$JAVA $JAVAOPTS $JAVAMAXMEM -classpath ./bootstrap.jar:./lib/saf.core.runtime.jar:./lib/jpf.jar:./lib/jpf-boot.jar:./lib/:../core/lib/MacOSX/*:../core/lib/org.apache.xalan_2.7.1.v201005080400.jar:../core/lib/org.apache.xml.serializer_2.7.1.v201005080400.jar:../core/lib/* saf.core.runtime.Boot"

export PATH=$VERDI_HOME/jre/Contents/Home/bin:$PATH

BATCHCMD=$1

if [ ! -e "$2" ]; then
   BATCHFILE="$DIR""/""$2"
else
   BATCHFILE="$2"
fi

if [ "$BATCHCMD" = "-b" -o "$BATCHCMD" = "-batch" ]; then
   if [ "$#" -eq 1 ]; then
        $JAVACMD $1
   else
        $JAVACMD $1 $BATCHFILE
   fi
else
  $JAVACMD ${1+"$@"}
fi
```

## 程式內之批次檔(script editor、%BATCHFILE%)
- 前述命令列的設定一次只能產生一張圖，然而若資料檔案很大，每次啟動VERDI程式只畫一個圖就離開，似乎效益太低了一些，此時就必須使用程式內的批次檔。
- 程式內批次檔的格式有其基本架構，
  - <Global> </Global>只出現在檔頭，其範圍的內容是「預設值」，與前述命令列控制類似，而無關每次的讀寫動作。
  - 而<Task></Task>可能重復很多次，但不接受變數及迴圈。
- 沒有一個指令是繪圖的動作，只要在script中給定圖形的檔名(imageFile=…)，程式即會寫出檔案。

### 注意事項
- -mapName：必須指向.bin檔，不接受其餘shape檔、tif檔。
- -g與-gtype作用相同
- -saveImage若不指定圖檔的目錄，將會存在啟動JAVA程式的最後目錄
- Script指令s=???:ttt的用法不能作用，但ts=ttt可以作用
- Editor內=之後的內容可以不必引號。imageFile不必再加延伸檔名，系統會自行加上。
- 從命令列啟動editor script file: `run.bat –b [dir][script file]`。不必指定-quit，執行完會自己跳出JAVA程式。
- **命令列預設**和**editor script**二者無法同時作用。
