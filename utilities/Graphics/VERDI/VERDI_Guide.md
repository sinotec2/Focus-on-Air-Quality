---
layout: default
title:  VERDI使用說明
parent: VERDI
grand_parent: Graphics
last_modified_date: 2022-03-18 14:02:50
---

# VERDI使用說明
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

此處簡介VERDI的使用方式

## PAVE(VERDI前身)
### PAVE簡述：
PAVE(Package for Analysis and Visualization of Environmental data)顧名思義為一環境數據的顯示軟體，當時因為主要的平台為工作站以上的機器，沒有適合的軟體，因此USEPA特別委託開發檢視軟體 (Rhyne et al. 1993, Thorpe et al. 1996) 。
PAVE功能也較當時述軟體為多，且為空氣品質模式專門設計，因此在應用上也較其他軟體普遍，因此USEPA也持續投入發展，以符合當代軟應體的環境需求。當時主要特性包括：
- 提供基本的圖形展示並可將圖形輸出至高階之商用軟體；
- 具有處理遠端工作站資料的能力；
- 可支援多重(不同物種、面向等組合)同時之圖形顯示；
- 可由外部進行程序控制；
- 計算資源需求非常低；
- 為一免費軟體。

### PAVE的功能包括：
- 繪製tile plot, 3D mesh plot, 時間序列之線條與柱狀圖；
- 繪製垂直剖面圖、風速向量圖、以及離散點xy圖；
- 進行資料之計算，包括四則運算、三角、對數、基本統計(極值、總合、平均)、選擇區域、以及條件選擇等；繪製特定較小時間與空間範圍內之資料(放大縮小功能)；
## VERDI
### VERDI簡述及快速起動：
由於PAVE只能在Linux上執行，同時也不再持續維護，因此美國環保署委請Argonne國家實驗室及UNC發展java based之VERDI (Visualization Environment for Rich Data Interpretation ) ，做為社群共用的顯示軟體。

雖然PAVE的功能已經被美國模式社群所廣泛接受，然而其linux的專屬特性，以及X-window介面軟體的限制，讓許多使用者卻步，因此美國環保署發展java的版本，可以直接掛在MS window、MAC OS上或linux等不同平台上，具有最大的相容性，並增加讀取CAMx、CMAQ、IOAPI、wrf.nc等檔案的格式。
1.    下載安裝：
- 裝置之執行檔可以由美國環保署CMAS網站註冊會員後下載 。( https://www.cmascenter.org/verdi/)
- 程式不需要安裝，放在OS路徑可以抓到執行檔的地方即可。
2.    執行：
- linux的指令為verdi.sh、PC為verdi.bat
- linux系統需要有DISPLAY環境變數的設定
  - 這不會在披次檔案內設定(因為使用者很多)
  - 使用者每次開啟新的OS界面後，須按照自己本機的IP位置自行在OS設定，範例如下：
  1. finger可以知道現在有誰在線上活動，如範例中kuang的主機(本機)是pc556，pc556是公司對每個pc的稱謂代碼，
  1. 到底IP是多少呢？可以用ping(測試連線狀態)來檢查本機的IP，如範例中ping pc556的結果，OS就會引導去連200.200.31.182，這便是pc556的IP了，
  1. 將IP代入xxx.xxx.xxx.xxx位置即可設定VERDI在這個OS作業要求下，要顯示在哪一台機器的螢幕上。

```bash
kuang@node03 ~
$ finger
Login     Name       Tty      Idle  Login Time   Office     Office Phone   Host
kuang                pts/0          Aug 29 12:38                           (pc556)

kuang@node03 ~
$ ping pc556
PING pc556 (200.200.31.182) 56(84) bytes of data.
64 bytes from pc556 (200.200.31.182): icmp_seq=1 ttl=128 time=0.606 ms
64 bytes from pc556 (200.200.31.182): icmp_seq=2 ttl=128 time=0.305 ms
64 bytes from pc556 (200.200.31.182): icmp_seq=3 ttl=128 time=0.715 ms
64 bytes from pc556 (200.200.31.182): icmp_seq=4 ttl=128 time=0.705 ms
^C
kuang@node03 ~
$ export DISPLAY=xxx.xxx.xxx.xxx:0.0
$ verdi.sh&
```
- 隨即在本機的X window軟體便可以發現VERDI的歡迎畫面。
- 如果要離開，按下File → Exit 即可   
3.     線上求助：
- [官網](https://www.airqualitymodeling.org/index.php/VERDI_1.5_User_Manual)

### VERDI注意事項

1.    記憶體

- 由於java程式佔用記憶體非常可觀，未讀入資料即耗用近500MB記憶體，1.5版甚至需1G的記憶體，因此PC必須有足夠的硬體方能順利運作。如果程式出現「沒有回應」只是還在讀檔計算，不是真的死當，等一下即可。
- 在讀取CALMET2netCDF結果檔案，製作4階向量圖時，系統會出現錯誤：OutOfMemoryError_verdi可能是因為時間太長，檔案太大所致，減少檔案的長度之後，即可應用verdi來開該等nc檔案。
- 不論PC或工作站，VERDI無法開啟3G以上的大型檔案，必須先減少時間、變數或維度。>700MB的檔案不能同時呈現兩個變數的tile圖。即使關閉變數或檔案並不會恢復(java heap space)，必須關閉程式與視窗，重新開始。

2.    座標轉換

- VERDI可以接受多種座標系統，包括常用的WGS系統經緯度、Lambert投影系統、UTM座標等。
- 如果是nc檔、IOAPI或WRF檔，VERDI會抓檔案內的設定值。因此如要修正，要從nc檔案的內容著手，在VERDI本身或其他外部檔案都沒有可以調整的。
- nc.XCENT、nc.YCENT、nc.ALP、nc.BET、nc.GAM、nc.XORIG、nc.YORIG、nc.XCELL、nc.YCELL 等等由於模式內設為美國本土地區，CAMx模式輸出檔中的座標系統若使用UTM/Lambert，將無法順利貼上其內設的底圖。
- 須在「與濃度檔同一目錄下」之camxproj.txt檔內予以指定範例如下，相關設定方式可以詳見CMAS網站說明(https://www.cmascenter.org/ioapi/documentation/3.1/html/BINIO.html) 。

```bash
kuang@master /home/camxruns/2019/outputs/con09
$ cat camxproj.txt
# Projection parameters are based on IOAPI.  For details, see www.baronsams.com/products/ioapi
GDTYP=2
P_ALP=10.0
P_BET=40.0
P_GAM=120.99
XCENT=120.99
YCENT= 23.61
```

|項目|UTM投影設定(範例)|LAMBERT投影設定(camxproj.txt內容)|
|-|-|-|
|!內設為LAMBERT|GDTYP=2|GDTYP=2|
|T1 lat|P_ALP=30.0|P_ALP=10.0|
|T2 lat|P_BET=40.0|P_BET=40.0|
|deg, origin for offset (136km)|P_GAM=118.586|P_GAM=120.99|
|meridian deg, same as P_GAM|XCENT=118.586|XCENT=120.99|
|meridian deg, origin for offset (2414km)|YCENT=1.823|YCENT= 23.61|

- #數字後面不可以有空格，必須馬上接carriage return
- 座標系統的誤差
  - 經緯度轉換為LCC(如MM5系統)的誤差有限。
  - UTM(twd97)及LCC之間的轉換則會發生誤差。
  - 先以台灣地區中心點(120.99, 23.61)的UTM值為準，各點UTM與中心點UTM差值，
    - 東西向要乘scaleX=66/69 (!east-west grid number correction factor)，
    - 南北向要乘scaleY = 123 /128，
    - 否則會向東、西、南、北各方向伸張超過土地範圍 (詳參master:/home/backup/sino4/kuang/mm5camx6/merge_lulai)。
	- 可以利用土地分類檔、或者點源位置檔，以及底圖的相對差異，進行微調修正。
- TODO：
	- 可能係T1、T2設定的問題，如果domain範圍較小，可以適度減少T1、T2範圍，以增加圖面之線性，如T1=21.61、T2=25.61
	- 如果domain的原點(中心點)有變更時，才需要更換camxproj.txt，否則不需要變數。
3.   底圖的選擇與自行增加底圖
- 台灣地區的縣市界或鄉鎮界GIS檔案，可以由政府官網(如內政部、運研所)下載 ，座標系統請選擇「經緯度」，VERDI看不懂twd97座標系統官網提供的是GIS套件，包括.shp、.dbf、等，但是VERDI要讀的是.bin檔案由VERDI軟體包中的shape2bin(.exe)執行轉換，用法如下：選擇正確的機器版本目錄執行完，以head -4指令確認結果。如twn_county.bin有769個多邊形，有216323 個頂點。

```bash
kuang@master /cluster/VERDI_1.5.0/shape2bin/bin/Linux.x86_64
$ shape2bin

shape2bin - Convert Shapefile *.shp to map_*.bin file.
usage:   shape2bin file.shp > map_file.bin
example: shape2bin NCA.shp > map_estuaries.bin
head -4 map_estuaries.bin

Email questions and comments to: plessel.todd@epa.gov

kuang@master /cluster/VERDI_1.5.0
$ head -4 ./plugins/bootstrap/data/twn_county.bin
Content-type: application/octet-stream; charset=iso-8859-1
# Dimensions: polyline_count vertex_count
769 216323
# IEEE-754/MSB 32-bit int counts[polyline_count]; float vertices[vertex_count][2=lon,lat]:
```

- 1.4版：放在VERDI資料目錄下 ，不必與其他底圖放在一起，可以由browser選擇。
- 1.5版以後：須以「現有圖檔名稱」取代
5.   底圖與版本選擇
- 1.4版可自由選擇要疊加的底圖，並無問題困難。
- 雖然CMAS網站提供了1.5版，主要是為了java版本的更新，然而更新後對非美國以外地區，不再提供向量底圖檔案的選項，需要使用者自行裝置底圖、以現有圖名替代。
  - world(內設，如左圖)
  - USA Counties→大陸地區的省份、直轄市自治區界(右圖)
  - HUC→台灣地區縣市分區圖(右圖)
  - Roads→台灣地區鄉鎮區分區圖

| ![VERDI1.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/VERDI1.png)|![VERDI2.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/VERDI2.png)|
|:--:|:--:|
| <b>D2模擬結果。VERDI內設海岸線| <b>加上大陸省份及臺灣縣份行政區底圖</b>|

### 軟體使用說明
1.    開啟檔案(Datasets/Formula/Area)：


按+號選取檔案。
- 讀進檔案後會在變數區(Variables)出現檔案內的變動名稱及單位。
- 如果只想顯示檔案中某段時間、某個高度或空間範圍，亦可以在Time step、Layer、Domain等處選擇要檢視的範圍。
- 可以雙擊變數名稱或按右鍵選擇成為「公式」(Formulas)。VERDI可以接受多種數學函數。常用的包括絕對值abs()、根號sqrt()、以及平方sq()、**等，可以在Formula 的edit line內編修，成為新的變數(如風速、Ox=O3+NO2...)，詳見手冊內容。點選變數之後會在上方選單列的最右邊出現「Selected Formula: XXX[n]」n=1,2,3…視開啟檔案的順序而定。


- Areas只用在計算行政區域平均值(Area Interp)在此輸入所需要區域界線的向量圖檔(.shp，可以由內政部官網或opendata網站下載行政區界圖檔，如下圖中的縣市TWN_COUNTY及鄉鎮區TOWN_NOI...檔案)下一步選變數名稱，這是為了方便選擇將要內插的行政區範圍名稱中文字→無法辨識代碼→太長無法記憶，但為「唯一」不會出錯英文→容易辨認，但可能非「唯一」(如很多市都有「東區」「北區」)，計算出錯會出現無值 「空格」




2.    Fast Tile Plot：
- 一般水平的濃度分布(raster plot)，VERDI叫做”Fast Tile Plot”，沒有內插或平緩化(smoothing)，只是簡單的class-post，因此失真的可能性最低，這也是VERDI最為CMAS所愛用的原因之一。
- 圖形的設定在Tile視窗上的選單列進行，點選後會在右邊的圖框顯示等值色塊圖，Tile圖層的下拉指令包括：File(列印及輸出)、包括圖形設定值的輸出(不必每次重新設定)Configure(圖面的細部設定，說明如下)、Control(滑鼠所拉出的範圍是要放大Zoom、還是要看指定範圍的數值Prob)、Plot(指定點、極值的時序圖、輸出動畫(很有用)等)、GIS Layers則為底圖圖層(只接受線條向量圖)之管理。
(1)    色階設定
- 色階在Configuration->Configure Plot->Color Map處設定。
- 內設為8層色階其解析度有限，無法用做報告呈現，但可以加上文字Title，製做個別圖檔及動畫檔，其處理速度較快。一般以10項為原則，太多也無法辨識其內容差異。
- 若色階夠多(最多可以接受64階)，或可以消除鋸齒狀，增加平緩度。須選連續漸層之色階，以顯示污染物連續分布的特性。
- 階數越多，提供顏色的選項就較少。Newton RGB(AVS)與(Inklet)的差異在前者最低濃度會是空白，比較沒有壓迫感。
- 色階可以選擇線性(可以是非等間距，如左圖)、或對數(可呈現較低值之分布，避開極端值所造成的干擾、會有較多的訊息_右圖)。


(2)    底圖設定
- 正常狀態下，系統會自動套上世界地圖之底圖(world為解析度約9公里的國界圖)，但不包括：台灣的縣市、鄉鎮區、大陸的省份、直轄市自治區界如要套用詳細的分區圖，須另準備，詳見前述「注意事項」
- 如果點選Fast Tile沒有世界地圖之國界，可能原因：CAMx 檔案：無正確的camxproj.txt在同一目錄nc檔案：檔案內的座標資訊不足或錯誤
- 如果要高解析度的底圖：VERDI 1.4：GIS Layers→Add Layer→(browser pick up)→NextOutline Color→(Pannel pick up)→確定→Finish


- VERDI 1.5版以後的GIS layer並沒有加入其他底圖之功能。見前注意事項，可以由現有底圖名稱替代成所要的高解析度底圖。
- 底圖要放縣市或到鄉鎮層級，主要視線條的多寡而定，如果同時有縣市與鄉鎮的底圖，可以用VERDI1.4給予不同顏色以茲識別(如黑色及灰色)。

3.    行政區域內插(Area Interp)
- 可以計算行政區域範圍內空間之平均值、「或」內插值。視行政區範圍與網格的相對大小如果網格較小→平均值如果網格較大→內插值
- 須先在Datasets處輸入行政區的shp檔(詳前述)。
- Area Interp的下拉選單與Tile圖類似，只有多出一項功能Option：展示範圍的平均值(Averages)、或加總值(Totals)、或網格數據(Gridded、與前述Fast Tile完全一樣)被選擇的行政區，或所有的行政區
- 注意：由於程式需要時間計算，如果電腦計算能力不夠強大，建議只針對少數時間平均結果進行區域之詳細解析減少區域的個數減少嘗試。

(1)    Show 選項：
- 前2項的性質都是一個行政區一個值，第3項則包括範圍內所有網格值，即為Fast Tile
(2)    區域選項：
- 滑鼠停留在Area Interp圖面上，會在左下方出現Area的名稱、面積、相關數值

- 可以在Areas控制盤用滾輪及control鍵來挑選，但名稱或代碼的排序並不能在軟體內運作，並不容易操作。




4.    垂直剖面(Vertical Cross Section)
給定X或Y值(網格點)，VERDI會畫垂直剖面的等值圖，雖然不如Tile Plot功能齊全，對於3維變數而言(尤其是煙流的解析)，有其必要之處。

5.    時間序列(Time Series、Bar Plot)
- 此處的時間序列為全部2維範圍的平均值，
- 範圍可以在Datasets處設定，
- 若需要滑鼠拉出的指定範圍或特定點的時間序列，可以：在Tile plot的下拉選單列先將滑鼠設定為Probe(在Controls下指定)拉出所要範圍的值回到Tile Plot的Plot下，則會出現Time Series...，可以指定是柱狀圖或線形圖(如下)


6.    散布圖與向量圖，需要指定2個變數。並沒有特別優秀，不推薦使用。
7.    contour plot：
為立體的濃度分布呈現(3-D plot)，除了經由顏色以外，經由垂直高度的差異，讓讀者可以更體會濃度的高低。然而此圖適合在平坦地區濃度的展示，因為VERDI並沒有2個高度座標，不會進行地形變化的相對位置校正。
8.    VERDI可以接受的輸入格式、提供的輸出檔案格式：
- 主要以Models-3的IOAPI(netCDF)為主，也可以接受CAMx avrg格式，包括濃度、沉降及排放量等通用格式(新版CAMx6+亦將其氣象格式改成avrg格式)
- 輸出格式：靜態圖片：包括png、jpeg、tif、tiff、eps、asc、GIS shp檔(ver1.14)及動畫：gif與mov。
(1)     png檔：由圖面上按右鍵Save Image As...之外，也可以在Tile圖框的功能鍵File下拉出Export as Image存png檔。
(2)     GIF/mov檔：從Plot -> Animate Plot做。

### Linux上執行VERDI
由於程式在Linux上執行，因此後處理與繪圖(至少品質確認工作)在Linux上執行，避免大型檔案在網路上傳送，是最合理的方式。

1.    由CMAS網站下載VERDI for linux(注意32或64位元)約380mb，下載完後在linux上解開壓縮檔(目前在master:/cluster/VERDI_1.5.0目錄)執行時亦須下到該目錄執行。

2.    準備視窗環境
- 在遠端PC啟動X window環境(如mi/x Xwindow、mobaXterm等)
- 在工作站執行：

```bash
- export DISPLAY='xxx.xxx.xxx.xxx:0.0'(顯示器位置，ip可以由finger/who或X win的banner找到，後者可能不太準)
- export LC_ALL="en_US.UTF-8"(關閉中文顯示，開啟英文顯示,或en_US要看/usr/share/locale目錄下提供哪些字型。
- xclock&(測試並啟動必要的X11程式)
```
3.    準備台灣地區的地圖檔(詳上述，所有GIS的檔名都要同樣大小寫)

4.     如果要開啟CAMx檔案，要記得

- 先準備好的原點(中心點)設定，camxproj.txt必須要和濃度檔同一目錄。
- 如果忘了先準備好camxproj.txt→
  - 先關閉CAMx檔案，因為系統會先寫一個內設的camxproj.txt，並且讀進記憶體不必關閉VERDI跳回到OS，
  - 在檔案所在的目錄，準備好camxproj.txt
    - (用對的檔案、覆蓋掉VERDI產生的內設camxproj.txt)
  - 回到VERDI、重新開啟CAMx檔案即可。

5.    確定X win已經可以作用，移動到VERDI目錄下執行verdi.sh&

6.    VERDI執行檔與linux作業系統版本、GNU版本無關，不須重新編譯。但要有java 1.7以上版本。必要時要更新工作站的java程式(sudo yum install java)
- 其實verdi有自帶的jre/bin/java，每個版本也會分別呼叫自己的java，與系統的java無關，因此也不需另外另建或更新java，
- 最新版本VERDI搭配的java版本會在CMAS網頁公布。    

7.    VERDI的設定檔與輸出結果內設目錄，是在登入機器的$HOME目錄下。產生圖檔後，可用filezilla至該處下載。

## VERDI的批次作業
由於JAVA在執行時可以接受命令列所輸入的引數，因此不論是linux或者是PC上，都是以批次檔方式開啟程式。運用此一特性，可以用批次檔的方式執行重複性的繪圖與計算作業，可以大幅節省工作時間。

除命令列的操作之外，VERDI程式內也提供了script editor可以在程式內執行批次。此二者命令相同，然而前者具有完整的script功能(變數設定、迴圈及判斷)，缺點是重複執行JAVA程式，浪費作業時間，而後者雖然在程式內執行批次作業減省JAVA的進出時間，然而該script的設計不接受變數迴圈或判斷。使用者可以視需求自行選用二者之一。

各項批次檔命令(script command)可以詳參手冊。

注意在命令列上，各command之前要加負號，之後是以空格隔開，command之間沒有順序，但是-configFile要先給定，-quit必須在最後。

在程式script editor之內，各command之前沒有負號，之後是以=(等號)隔開，command之間也沒有順序，

### 設定組態檔(-configFile configuration file)
可以儲存各種圖形介面組態(Configure)的設定內容，包括
- 圖面的主標題、次標題、
- 色階、色階的單位、
- 下標題、各軸的名稱、字型與大小等等圖面設定。

VERDI並未約定檔案的字尾，基本上，組態檔是一個文字檔，也可以從外部進行編輯。

一般VERDI會將變數名稱(-s)列為主標題(titleString)，而將檔案名稱(通常含有地域及時間項-f)列為次標題(-subTitle1, -subTitle2)，而變數的時刻與最大值則會出現在下標題，這些是可以在批次檔中控制，將內容傳給VERDI寫在圖面上，其餘不必改變的，可以按照configuration file的內容。

### 命令列預設控制(範例)
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
### 程式內之批次檔(script editor、%BATCHFILE%)
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
- 從命令列啟動editor script file: run.bat –b [dir][script file]。不必指定-quit，執行完會自己跳出JAVA程式。
- 命令列設定和editor script二者無法同時作用。

## 參考網頁
- Rhyne, T.-M., Bolstad, M., Rheingans, P., Petterson, L., and Shackelford, W. (1993). Visualizing environmental data at the EPA. Computer Graphics and Applications, IEEE 13:34–38. doi:10.1109/38.204964.
- Thorpe, S., Ambrosiano, J., Balay, R., Coats, C., Eyth, A., Fine, S., Hils, D., Smith, T., and Tray, A. (1996). The Package for Analysis and Visualization of Environmental Data. Presented at the CRAY USER GROUP, CUG, Speeding by Design, Charlotte, North Carolina, pp. 46–50. https://cug.org/5-publications/proceedings_attendee_lists/1997CD/F96PROC/46_50.PDF
- https://www.cmascenter.org/ioapi/documentation/3.1/html/BINIO.html

### Map projection type
```bash
INT4 GDTYP: map projection type
LATGRD3=1 (Lat-Lon),
LAMGRD3=2 (Lambert conformal conic),
MERGRD3=3 (general tangent Mercator),
STEGRD3=4 (general tangent stereographic),
UTMGRD3=5 (UTM, a special case of Mercator),
POLGRD3=6 (polar secant stereographic),
EQMGRD3=7 (equatorial secant Mercator), or
TRMGRD3=8 (transverse secant Mercator)
```
- 軟體：http://www.cmascenter.org/verdi/；
- 手冊檔案：https://www.cmascenter.org/verdi/documentation/1.4.1/VerdiUserManual1.4.1.htm
- 官網： https://www.airqualitymodeling.org/index.php/VERDI_1.5_User_Manual
- Relatives
  - VERDI使用說明
  - VERDI圖面解析度之改善
  - VERDI的script
