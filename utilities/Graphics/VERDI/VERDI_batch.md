---
layout: default
title:  VERDI的批次作業
parent: VERDI
grand_parent: Graphics
last_modified_date: 2022-06-07 11:12:04
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
- 由於JAVA在執行時可以接受命令列所輸入的引數，因此不論是linux或者是PC上，原本就是以**批次檔**方式開啟程式。
- 運用此一特性，可以用批次檔的方式執行重複性的繪圖與計算作業，可以大幅節省工作時間。
- 除命令列的操作之外，VERDI程式內也提供了script editor可以在**程式內執行批次**。
- 此二者命令相同，然而
  - 前者具有完整的script功能(變數設定、迴圈及判斷)，缺點是重複啟動JAVA的[jvm](https://zh.wikipedia.org/wiki/Java虚拟机)，浪費作業時間，而
  - 後者雖然在程式內執行批次作業減省JAVA的進出時間，然而該script的設計不接受變數迴圈或判斷。
- 使用者可以視需求自行選用二者之一。

各項批次檔命令(script command)可以詳參[手冊](https://github.com/CEMPD/VERDI/blob/master/doc/User_Manual/VERDI_ch17.md)。

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
- 由201002181.avrg（CAMx模擬結果）中讀取O<sub>3</sub>、產生濃度分布圖(使用臺灣縣市界地圖)，存成20100218.png檔案

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
- 基本批次檔

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
- 循環操作範例：將前述CAMx逐時臭氧結果分別另存png檔案

```bash
export VERDI_HOME=/opt/VERDI_2.1.3
DIR=$VERDI_HOME
VERDI=/opt/VERDI_2.1.3/verdi.command
BATCHFILE=$DIR/temp.bat
for t in {00:23}:
  INP='/Users/4139/MyPrograms/VERDI_1.4.1/201002181.avrg -s O3[1]:$t'
  OUT='PNG /Users/4139/MyPrograms/VERDI_1.4.1/20100218$t.png'
  TWN=/Users/4139/MyPrograms/VERDI_1.4.1/plugins/bootstrap/data/TWN_COUNTY.bin
  TMS=/Users/4139/MyPrograms/VERDI_1.4.1/toms.cfg
  echo '-configFile $TMS -f $INP -g tile -mapName $TWN -saveImage $OUT -quit' > $BATCHFILE
  $VERDI -b $BATCHFILE
  echo $t
done
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

## 程式外批次檔
### 命令列執行VERDI(CALPUFF結果時間序列圖檔展示)
- /home/cpuff/UNRESPForecastingSystem/Run.sh有關VERDI批次作業的內容

```bash
today=$(date +%Y%m%d)
rundate=$(date -d "$today - 1 day" +%Y%m%d)
...
export DISPLAY=:0.0 #Keep login from Console
  VERDI=/cluster/VERDI/VERDI_1.5.0/verdi.sh
...
  ln -sf ../../CALPUFF_OUT/CALPUFF/${rundate}/calpuff.con .
  ln -sf ../../CALPUFF_INP/calpost.inp .
  if [ -e calpuff.con.S.grd02 ];then rm calpuff.con.S.grd02*;fi
  /usr/kbin/con2nc >& /dev/null
  if ! [ -e calpuff.con.S.grd02.nc];then echo con2avrg fail!; exit 0;fi
  python ../../Python/join_nc.py
  python ../../Python/mxNC
  # link the basemap of VERDI
  BIN1=/cluster/VERDI/VERDI_1.5.0/plugins/bootstrap/data/twn_county.bin
  BIN2=/cluster/VERDI/VERDI_1.5.0/plugins/bootstrap/data/map_world.bin
  ln -sf ${BIN1} ${BIN2}
  for s in PMF SO2 SO4 NOX;do
    ss=$s
    test $s == SO2 && n=1
    test $s == SO4 && n=2
    test $s == NOX && n=3
    test $s == PMF && n=0
    test $s == PMF && ss=PM10 #total PM25
    static=_static_topoconcrec0${n}00
    for ((i=1;i<${numhours};i+=1));do
      ii=`printf "%02d" $i`
      i8=$(( $i + 7 ))
      OUT=${s}${static}$ii
      TSMP=$(date -d "${rundate} +${i8}hours" +"%Y-%m-%d_%H:00_LST")
      cp ../../CALPUFF_INP/batch_template.cmd bat.cmd
      for cmd in "s/TS/"$ii"/g" "s/SPEC/"$ss"/g"  "s/RUNDATE/"$rundate"/g" "s/OUT/"$OUT"/g" "s/TIMESTAMP/"$TSMP"/g";do
        sed -i $cmd bat.cmd
      done
      $VERDI -b bat.cmd>&/dev/null
    done
    convert ${s}${static}??.jpg ${s}.gif
    cp ${s}.gif /var/www/html/LC-GIF-Player/example_gifs
...
  BIN1=/cluster/VERDI/VERDI_1.5.0/plugins/bootstrap/data/map_world.bin_old
  ln -sf ${BIN1} ${BIN2}
```
### $DISPLAY的設定
- 當**命令列**狀態批次執行VERDI時，因為*putty*已經設定了DISPLAY的環境變數，所以沒有出現問題。
- 但在*crontab*自動執行批次檔時，沒有設定$DISPLAY，會造成VERDI的錯誤與終止。
  - 事實上，正常狀態下批次執行並沒有任何螢幕的輸出。
  - 如批次檔有誤，會在$DISPLAY的X window畫面出現錯誤訊息。
  - 此乃程式內設，無法更改。
- 此處將$DISPLAY設到本機 [:0.0]()
  - 但不能指定實際的機器、hostname或IP、localhost等等、且
  - **console** 必須保持**登入**狀態、使用者須與*crontab*相同
  - 即使其他終端機未開機，至少還有console可以作為VERDI的螢幕輸出。

## 輸入檔(.nc)的準備
### [con2nc.f](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPOST/con2nc.f)
- *calpuff*輸出檔案是calpuff.con檔，目前只有calpost程式可以讀取。[con2nc.f](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPOST/con2nc.f)即是以calpost.f為基底的轉接程式。
  - 程式版本為CALPOST_v7.1.0_L141010
- 因為是連續執行，*calpuff*需要讀取初始煙陣濃度(**restart**)，避免煙流從新計算、濃度瞬間歸0。
  - 而隔日執行可能遇到機組個數的差異，無法順利接續，只得放棄**restart**。

### [join_nc.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPOST/join_nc.py)
- 此處改採跨日濃度檔案漸變連接的方式([join_nc.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/join_nc.py))，降低*calpuff*從0啟動時的誤差，得到較合理的結果。
  - 漸變採24小時(`nt=24`)、新、舊檔案照小時數正比線性加權方式進行

```python
kuang@master /home/cpuff/UNRESPForecastingSystem/Python
$ cat join_nc.py
#!/cluster/miniconda/envs/unresp/bin/python
...
nt=24
for v in V[3]:
  for t in range(nt):
    var0=nc0[v][t+nt,:,:,:]*(nt-t)/nt
    var1=nc[v][t,:,:,:]*t/nt
    nc[v][t,:,:,:]=var0+var1
```  

## 濃度等級(.cfg)之調整
- 同一批次的圖面，只能有一個最大值、同一組的濃度等級，以避免gif檔圖面跳動不穩定。
- .cfg可以參考VERDI提供的樣版檔案，如：
  - ./data/configs/modis_.5_0.cfg
  - ./data/configs/o3_Calif_4km.cfg
  - ./data/configs/o3_10bin.cfg
  - 範例都是以Newton RGB (AVS)約10層來顯示。
  - 經證實在`<ColorMap> </ColorMap>`內指定的內容，會被後面`<Step> </Step>`覆蓋，即使ColorMap指定是線性等值區間、最大及最小值，後面的Step數字還是可以作用。

### [mxNC.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/VERDI/mxNC.py)
- 因為濃度等級與nc檔中的最高濃度有關，此處參考[mxNC.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/VERDI/mxNC.py)來進行修改，找到最大濃度值之後，產生各個濃度等級的值，寫在`<Step> </Step>`區段內。
- 最大濃度(`mxv[]`)
  - 經試誤取時間**75%最大值**、再取log值的等間距值，可以避免圖面太偏向低濃度、訊息量太少。
  - VERDI會**自動**在Footer加註各小時的最大濃度，可以提供足夠的訊息。

```python
...
mxv={}
if len(V[3])>0:
  for v in V[3]:
    mxv.update({v:np.max((np.mean(nc0[v][:,:,:,:],axis=0)+np.max(nc0[v][:,:,:,:],axis=0))/2)})
...
```
- 濃度等級(`line[10]~line[20]`內容)
  - 由於煙流濃度空間變化很大，如果採用線性等級大多數面積處於低濃度狀態而沒有差異。
  - 此處選擇以log10方式、在最大濃度與0.01之間切割成10等分。
  - 最後輸出到Step內容時，將其還原成正常值

```python
...
  #min=0.01
  dc=(np.log10(mxv[ss])+2)/10
  lines[10]='<Step>0</Step>\n'
  for i in range(1,11):
    lines[10+i]='<Step>'+str(10**(dc*i-2))+'</Step>\n'
...    
```
- Footer內容的設定(`lines[38]`)
  - Footer 第1行內設會寫出nc檔案的時間標籤(UTC)，為避免干擾，此處將其關閉，替代以calpuff的模擬日期
  - 內容在cfg檔案`anl.verdi.plot.config.PlotConfiguration.footer_line_1`的value(`lines[38]`)
  - 開關在`anl.verdi.plot.config.PlotConfiguration.footer_line_1_auto_text`
    - true為程式自動刊列UTC時間
    - false則將列出前述內容。在模版中一次關閉即可。

```python
...
line38=lines[38] #footer_line_1 value
date=subprocess.check_output('date -d "-1 day" +"%Y-%m-%d"',shell=True).decode('utf8').strip('\n')
if 'footer1' not in line38:
  sys.exit(line38)
line38=line38.replace('footer1','Based on '+date+' Operation Rate%')
...
```

### 底圖的修改與應用
- 幾經改版，VERDI已經放棄在批次檔層級指定底圖了，亦即mapName不再作用。
  - 固定的內設檔名就是map_world.bin(前述批次檔Run.sh中的變數$BIN2)，
  - 因此如果要更換，只能從外部將其暫時對調，待批次執行完畢再換回原來檔案。
- bin檔案的準備可以詳見[底圖的選擇與自行增加底圖](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/#底圖的選擇與自行增加底圖)
- 此處刻意選擇較舊的縣市界版本($BIN1)，留存舊台中及高雄市範圍，以增加圖面的解釋資訊。

| ![PMF_static_topoconcrec000055.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/PMF_static_topoconcrec000055.PNG)|
|:-:|
| <b>verdi批次繪圖結果範例</b>|   
   

### 批次檔模版
- 此處以sed指令置換模版中的特定變數
- 模版參照[程式內之批次檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_batch/#程式內之批次檔script-editorbatchfile)撰寫
- imageWidth及imageHeight：如不設定將會有大量範圍是空白。適當調整可以放大圖面、減少空白。
- 新版VERDI可接受時間步階(ts)直接寫在批次檔內，而不接受將ts寫在物種之後(s:ts)
- 變數及範圍範例
  - RUNDATE：20220331
  - SPEC：SO2、NOX、SO4、PMF
  - TS：1\~84
  - OUT：輸出檔名(不必加註附加檔.jpg)
  - TIMESTAMP：時間標籤。2022-03-31_12:00_LST


```bash
kuang@master /home/cpuff/UNRESPForecastingSystem
$ cat CALPUFF_INP/batch_template.cmd
                <Global>
                configFile=/home/cpuff/UNRESPForecastingSystem/vis/RUNDATE/SPEC.cfg
                dir=/home/cpuff/UNRESPForecastingSystem/vis/RUNDATE
                #pattern=*CCTM46*
                f=calpuff.con.S.grd02.nc
                saveImage=jpg
                gtype=tile
                imageDir=/home/cpuff/UNRESPForecastingSystem/vis/RUNDATE
                imageWidth=600
                #imageHeight=500
                </Global>
                <Task>
                s=SPEC[1]
                ts=TS
                imageFile=OUT
                subTitle1=TIMESTAMP
                </Task>
```
### 時間標籤
- VERDI的時間標籤在Footer，但批次檔不能修改Footer的內容、只能在cfg檔案中關閉、或指定Footer顯示的內容。
- 不論nc檔案內容的ITZON為何，VERDI的標準時間固定為UTC，因此，如果要以Footer來顯示nc檔的時間標籤，只能遷就UTC。
- 此處就批次檔能修改的範圍(titleString、subTitle1~2)註明當地時間，而關閉Footer之UTC內容，避免干擾。
  - sed不接受空格，因此以橫線、底線及冒號填滿
  - 模擬自`${rundate}`0時UTC開始，因此LST為`$i+7`。
```bash
i8=$(( $i + 7 ))
TSMP=$(date -d "${rundate} +${i8}hours" +"%Y-%m-%d_%H:00_LST")
```

### Parallel Execution of VERDI 
- 如前所述，重複進入java、產生圖檔、退出、再進入，實為一耗費資源的過程，但似乎目前也沒有更好的解決方案。(如果要在每一張圖面上標上特定的時間標籤)
- java程式本身具有多工的能力，經觀察，單一java程式可以使用到2個核心的CPU。
  - 如果工作站核心數較多，可以考慮同步進行VERDI，以節省時間。

### demo gif
- [http://114.32.164.198/LC-GIF-Player/demo.html](http://114.32.164.198/LC-GIF-Player/demo.html)
- [PMF.gif](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/PMF.gif)
- [github.io](https://sinotec2.github.io/cpuff_forecast/index.html)

| ![calpuff_PMF.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/calpuff_PMF.PNG)|
|:-:|
| <b>CALPUFF模擬結果GIF檔展示畫面</b>|

## 存檔格式(png OR jpg)的選擇
- jpg的檔案會小很多，如果只考慮靜態應用，可以選擇jpg格式
- 在合併成gif檔案時，jpg在計算時會失真很多，圖面變得模糊、縣市界出現疊影。因此還是png較保險。

## Reference
- lizadams, [VERDI User Manual](https://github.com/CEMPD/VERDI/blob/master/doc/User_Manual/README.md), 1 Oct 2019