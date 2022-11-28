---
layout: default
title: MMIF Remote Excution System
parent: ME Pathways
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2022-03-28 11:04:39
---
# MMIF之遠端執行系統
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

遠端系統的建置，包括站台設置、html(js)程式、CGI_python程式、以及OS批次檔，前3者詳見[網頁計算服務軟體系統的建置](https://www.evernote.com/shard/s125/sh/cbdd416f-d96e-54c0-819e-eb022ebd452d/ea45d6252fe57992d284ac8109f2f035)之說明，此處集中在批次執行說明。

由於mmif時間範圍經年，執行時間會超過瀏覽器停等時間(造成瀏覽器time out)，CGI及mmif程式都會停擺。mmif程式必須轉到背景執行與CGI脫勾才能順利完成。因應此一需求，有以下3個作法：

1. 以自動執行之批次檔案承接，結束後以email通知
	- 此一版本的背景執行交由crontab來管控
	- 適用在頻繁呼叫、頻繁起、停的情況(課堂習作)
2. 直接在cgi_python內啟動背景執行，由使用者自行上網確認結果
3. 預先以工作站完成各年度WRF在各網格之MMIF轉檔，再由網頁或(及)CaaS系統提供

CaaS網址為：[http://125.229.149.182/mmif.html](http://125.229.149.182/mmif.html)

## 自動執行搭配版本

除了伺服器端的CGI程式之外，實際執行分2個伺服器身份進行，cybee為計算執行者，root則為檔案管理者，由crontab進行自動執行之管控。使用者只需將準備好的mmif.inp上傳到伺服器，填寫正確的回函    email 信箱，系統就會將執行結果的連結寄給使用者。

### 系統元件

1. 網址為：http://125.229.149.182/mmif.html，屬於個人負責營運維護的伺服器系統。
	- select a file:選擇要執行的mmif.inp檔案。檔名必須是小寫、名字完全相符，不接受壓縮檔。設定方式詳下述。
	- EMAIL:輸入回函email 信箱。系統不會寄發檢核信件。
	- Upload and Run mmif remotely:上傳檔案到伺服器上、並等候crontab來執行mmif。
2. 回函：
	- 系統寄件者名稱為cybee、主旨分別為MMIF ACCEPTED及MMIF RESULT。
	- 第一封回函會在開始執行程式之前寄到信箱，視伺服器壅塞的程度而異，內設執行批次個數少於6時，會接受新的批次。
	- 第二封回函會在完成執行後寄達。視指定mmif執行模擬的時間長短而異，時間長、批次多，等候的時間就會很久。
	- 點選連結會自動下載到使用者的“下載”目錄，只要用一般解壓縮軟體就能打開。
	- 如果沒有收到回函，有可能：
		1. 前述正常的等候時間
		2. 被當成垃圾信
		3. 如果垃圾箱沒有，請確認email是否有誤
3. 特色及好處：
	- 不需在使用者電腦上編譯mmif的執行檔。USEPA並無義務提供任意平台的程式執行檔。
	- 不需登入主機、不用登記會員、不做cookie紀錄追蹤、不佔用電腦資源。
	- 輕量化系統。由於潛在使用者並不多，系統沒有經常性的執行壓力。
	- 使用CWB的WRF結果（中央氣象局WRF_3Km數值預報產品之下載及轉檔），有一定的公信力。
4. 待改進處：
	- 目前只有2020年WRF數據、且CWB有缺漏情形。
	- 目前只提供台灣本島範圍的經緯度座標，外島部分尚待開發。
	- mmif.inp 的準備，尚涉及aermod模式模擬時間、空間範圍的設定，有待建置互動界面以減少錯誤。
	- 伺服器計算速度以及網路頻寬有待提升。

### cybee crontab contents:
- 執行頻率
	- doing per min..
```
*/1 * * * * /Users/cybee/mmif_cron.cs >& /Users/cybee/mmif_cron.out
```
- 執行內容(計算啟動之檢查、控制、執行、郵寄)
	- /Users/cybee/mmif_cron.cs contents
		- 執行邏輯
			1. 電腦負荷太多時、跳開不執行（設定為6個mmif工作）(line 6)
			2. 使用者開了目錄（隨機產生名字），才能執行。開了目錄的2天後將不會存在。
			3. 依照目錄順序進行檢查、執行：(line 11)
				1. 如果有email但是還沒有寄過ACCEPTED第一封信，則執行寄信動作。指標為emai_bak檔案是否存在(line 14~22)。
				2. 目錄下如果有mmif.inp檔案、卻沒有mmif.out檔案，則開始執行程式、製作成果壓縮檔、寄發第二封信RESULT。(line 24~39)
				3. 下一個目錄

```bash
  1	
  2	#ensure not to many mmif are running
  3	n=$(ps -ef|grep /opt/local/bin/mmif|wc -l)
  4	n=$(( $n - 1 ))
  5	if [ $n -le 6 ];then
  6	
  7	#ensure mmif.inp was put to the directory
  8	m=$(ls /tmp|grep mmif_|wc -l)
  9	if [ $m -gt 0 ];then
10	
11	for dr in $(ls /tmp|grep mmif_);do
12	dir=/tmp/$dr
13	#ensure email was given
14	if ! [ -e $dir/mmif.email_bak ] && [ -e $dir/mmif.email ];then
15	#send first email     
16	    emailadd=$(cat $dir/mmif.email)
17	    echo "Hello MMIF user:\n Your mmif submit was accepted, please wait and check this email.\
18		since $n mmif are running    
19		The resultant tgz file will send to you and the file will be erased after 24 hrs! \n \
20		(sent by machine do not reply)" | mail -s "MMIF ACCEPTED" $emailadd
21	    cp $dir/mmif.email $dir/mmif.email_bak
22	fi
23	
24	#ensure mmif.inp exist and perform mmif
25	if [ -e $dir/mmif.inp ];then
26	    if ! [ -e $dir/mmif.out ];then
27	    	cd $dir
28	    	cp mmif.inp mmif.recieved
29	    	/opt/local/bin/mmif>mmif.out
30	    	/usr/bin/zip result.zip *
31		emailadd=$(cat $dir/mmif.email)
32	    	echo "Hello MMIF user:\n Your mmif result was at http://125.229.149.182$dir/result.zip\n \
33			Please fetch the file as soon as possible,\n \
34		    	The file will be erased after 24 hrs!\n \
35			(sent by machine do not reply)" | mail -s "MMIF RESULT" $emailadd
36	#        for i in $(ls|grep -v result.zip);do rm -f $i;done
37	#    	rm -f $dir/result.zip|at now+24 hours
38	    fi
39	fi
40	done
41	fi
42	fi
```

### root crontab contents

- 執行頻率
	-  doing per day.
- 執行內容(檔案管理)
		- 執行成果、設定必須定期清理，避免硬碟消耗。此處設定為24小時後，考慮到時間差，最長為2日。
		- 必須由root來清理的理由是使用者(_www)開啟的目錄、檔案，即使由CGI_python程式宣告屬性為777，仍然不能被其他一般使用者（如mmif的實際執行者cybee）刪除。
		- macOS的ls沒有ISO格式，必須使用gls (詳[參](https://apple.stackexchange.com/questions/15170/how-do-i-change-the-time-format-used-by-ls-command-line-on-osx))
		- MacOS的date也有差異。
```
#remove the mmif_* 2 days ago
0 0  *  *  * cd /tmp;dd=$(/bin/date -j -v-2d +"%Y-%m-%d");for i in $(/usr/local/bin/gls -l --time-style=full-iso|grep mmif_|grep $dd|/opt/local/bin/awkk 9);do rm -fr $i;done
```

## cgi_python內啟動背景執行

此版本適用在少數零星之mmif作業，此時如果維持一固定(高度)頻率的檢查、由系統自動執行批次、似無理由。只要使用者不離開網頁、或保留連結資訊，只待程式執行完後自行上網下載成果，也十分方便自在。

### mmif.inp之準備

此版本允許使用者輸入kml檔案，以指定欲執行mmif位置之經緯度，因此需要一模版，用sed來置換其內的經緯度、檔案名稱等重要訊息。

模版內容：

```bash
$ cat -n mmif.inp_blank20|more
  1  start      2020 01 01 08
  2  stop       2021 01 01 08 
  3  TimeZone   +8
  4  grid       IJ -5,-5 -5,-5
  5  layers top 20 40 80 160 320 640 1200 2000 3000 4000
  6  stability  GOLDER
  7  PBL_recalc FALSE
  8  aer_min_speed 0.5
  9  aer_min_mixht 1.0
10  aer_min_obuk  1.0
11  POINT  LL         LATI LONG
12  AER_layers        1        4
13  Output aermet     useful   run_aermet_xiehe.csh
14  Output aermet     onsite   xiehe.dat
15  Output aermet     upperair xiehe.fsl
16  Output aermet     aersfc   xiehe.aersfc.dat
17  FSL_INTERVAL      6
18  POINT  latlon     LATI LONG      8
19  Output aermet     FSL      'Upper_air_at_xiehe.FSL'
20  POINT  latlon     LATI LONG      8
21  AER_layers        0        0
22  Output aermod     useful   xiehe.info.txt
23  Output aermod     sfc      xiehe.sfc
24  Output aermod     PFL      xiehe.pfl
25  INPUT /nas1/backup/data/CWB_data/raw/20191231/wrfout_d04_2019-12-31_06:00:00
26  INPUT /nas1/backup/data/CWB_data/raw/20200101/wrfout_d04_2020-01-01_06:00:00
27  INPUT /nas1/backup/data/CWB_data/raw/20200102/wrfout_d04_2020-01-02_06:00:00
28  INPUT /nas1/backup/data/CWB_data/raw/20200103/wrfout_d04_2020-01-03_06:00:00
29  INPUT /nas1/backup/data/CWB_data/raw/20200104/wrfout_d04_2020-01-04_06:00:00
...
```

其中

1. 經緯度(LATI、LONG)(line 11, 18, 20 )：後續在執行CGI_python時以sed修改
2. 結果檔案名稱(line 23~24)：後續執行時以sed修改

### CGI_Python程式
- 客戶如果提供的是mmif.inp，複製一份到工作目錄下。(line 31~32)
- 如客戶提供的是kml檔，先讀取個案名稱與座標，以sed由模版複製一份，並以sed置換其中經緯度與檔名，準備好mmif.inp。(line 33~42)
- 在背景執行mmif(line 43~49)
- 提供結果檔案之網址，待執行完成後由客戶自行下載。

```python
kuang@114-32-164-198 /Library/WebServer/CGI-Executables/isc 
$ cat -n mmif.py 
  1  #!/opt/anaconda3/envs/py27/bin/python 
  2  # -*- coding: UTF-8 -*- 
  3 
  4  import cgi, os, sys 
  5  import cgitb; cgitb.enable() 
  6  import tempfile as tf 
  7  import subprocess 
  8  from pykml import parser 
  9  from rd_kmlLL import rd_kmlLL 
10 
11  form = cgi.FieldStorage() 
12 
13  mmif_parm=['AER_MIN_OBUK', 'POINT', 'AER_LAYERS', 'AER_MIN_MIXHT', 'INPUT', 'GRID', 'TIMEZONE', 'PBL_RECALC', 'AER_MIN_SPEED', 'OUTPUT', 'STOP', 'FSL_INTERVAL', 'LAYERS', 'STABILITY', 'START'] 
14  mmif_parm=set(mmif_parm) 
15  ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','') 
16  # 獲取檔名 
17  fileitem = form['filename'] 
18  MMIF='/opt/local/bin/mmif' 
19  WEB='/Library/WebServer/Documents/' 
20  CGI='/Library/WebServer/CGI-Executables/isc/' 
21  pth=WEB+'isc_results/mmif_'+ran+'/' 
22  OUT='>> '+pth+'isc.out' 
23  SED='/usr/bin/sed -ie' 
24  os.system('mkdir -p '+pth) 
25  print 'Content-Type: text/html\n\n' 
26  print open(CGI+'header.txt','r') 
27 
28  # 檢測檔案是否上傳 
29  if fileitem.filename: 
30    # 設定檔案路徑 
31    fn = os.path.basename(fileitem.filename) 
32    open(pth+fn, 'wb').write(fileitem.file.read()) 
33    if 'kml' in fn: 
34      case,lon,lat=rd_kmlLL(pth+fn) 
35      print case+(' {:f} {:f} </body></html>').format(lon,lat) 
36      cmd ='cd '+pth+';' 
37      cmd+='cp ../mmif.inp_blank mmif.inp;' 
38      cmd+=SED+' "s/LATI/{:f}/g" mmif.inp'.format(lat)+';' 
39      cmd+=SED+' "s/LONG/{:f}/g" mmif.inp'.format(lon)+';' 
40      cmd+=SED+' "s/xiehe/{:s}/g" mmif.inp'.format(case) 
41      os.system('echo "'+cmd+'"'+OUT) 
42      os.system(cmd) 
43    sfc=subprocess.check_output('grep " sfc " '+pth+'mmif.inp|awk "{print \$NF}"',shell=True).decode('utf8').strip('\n').strip('\r') 
44    ext=sfc.split('.')[-1] 
45    case=sfc.replace(ext,'') 
46    cmd ='cd '+pth+';' 
47    cmd+=MMIF+'|grep Hourly|grep written>'+case+'out &' 
48    os.system('echo "'+cmd+'"'+OUT) 
49    os.system(cmd) 
50  if not os.path.exists(case+'sfc') or not os.path.exists(case+'pfl'): 
51    r=os.system(cmd) 
52    if r!=0: 
53      print """Something wrong in AERMOD excutions, see <a data-auto-download href="%s">%s</a> 
54      <body></html> 
55      ename=pth+case+'out' 
56      """  % (ename.replace(WEB,'../../../'),ename.split('/')[-1]) 
57      sys.exit() 
58 
59  pid=subprocess.check_output('ps -ef|grep aermod|head -n1|/opt/local/bin/awkk 2',shell=True).decode('utf8').strip('\n') 
60  print 'mmif is running at pid= '+pid+'</br>' 
61  os.system('sleep 30s') 
62  fnames=subprocess.check_output('ls '+pth,shell=True).decode('utf8').strip('\n').split() 
63  print """\ 
64    MMIF_results: The MMIF process will take hours. You may check them during program excution:</br> 
65    DO NOT RELOAD this web-page !!!</br> 
66    """ 
67 
68  for fn in fnames: 
69    fname=pth+fn 
70    print """\ 
71    <a data-auto-download href="%s">%s</a></br> 
72    """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1]) 
73  print '</body></html>' 
74  sys.exit()
```

### 副程式rd_kmlLL.py

此副程式應用pykml之parser模組，由kml檔案中讀取Points的名稱及位置。詳[rd_kmlLL.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/#rd_kmlpy)

## 全台網格預處理版本

有鑒於在macOS上執行mmif需時較長(主要受限gfortran與netcdf的能力不佳)，考慮以工作站批次執行mmif(ifort版本)網格轉檔，以減省macOS的執行時間。

### 執行構想

- WRF年代：以工作站目前已有成果為基準。由於風險評估所需模擬至少需要完整的5年，恰等於目前2016~迄今之5年。
- 空間範圍與解析度：
	- 考量TWN_3X3 (D4範圍解析度)
	- 台灣地區並非所有地方均能(適合)開發污染源，此處就已經開發工廠之地區為考量，自TEDS10點源資料庫中讀取點位。其它點位則由使用者啟動MMIF來轉檔。
	- 由於一般AERMOD模擬範圍約3~30Km範圍，在D4範圍內有1~10格，只能取一處氣象數據做為代表。就此而言，3Km之解析度應屬充分足夠。
	- 在WRF系統內，小於此一空間範圍亦無其他訊息，無法提供更小解析度之數據。
- 平行運作：
	- mmif雖然沒有平行計算的能力，但如能將執行批次分開創建目錄，將程式的IO檔案分目錄存放，批次之間將不會彼此干擾可以平行作業。
	- 運用動態控制執行緒數的原理(詳entry linux*)，可以在os平台上實現平行運作。

### 空間點位之歸納

自point_QC.csv(詳read_point.py(*))中歸納出台灣地區已設有工廠的網格位置，另存成point_ij.csv，其表頭如下：

```python
kuang@114-32-164-198 /Users/1.PlumeModels/AERMOD/mmif/TWN_3X3 
$ head point_ij.csv 
IJ,X,Y,lon,lat 
7152,-102000.0,252000.0,119.936,25.961 
7159,-102000.0,273000.0,119.934,26.157 
8159,-99000.0,273000.0,119.965,26.157 
11048,-90000.0,-60000.0,120.082,23.047 
12048,-87000.0,-60000.0,120.112,23.047 
12054,-87000.0,-42000.0,120.111,23.215 
13047,-84000.0,-63000.0,120.142,23.019 
13048,-84000.0,-60000.0,120.142,23.047 
13053,-84000.0,-45000.0,120.141,23.187
...
```
- IJ = I*1000 + J，為東西、南北向網格標籤的組合
	- 每網格分開、分批作業，具有獨立性
	- 將可作為檔案目錄、命名之依據
- X,Y：lambert projection座標值，原點在台灣中心點

### 使用整併程式如下：
- 先求出點源所在位置的IJ(整數化)、再以pivot_table取平均。因同一網格中心的XY值都相同，平均值即為取集合之代表值。
- 經緯度取3位截尾，以使在mmif.inp檔案內置換後有較佳的可讀性
- (83,137)為d4範圍之網格數

```python
kuang@114-32-164-198 /Users/1.PlumeModels/AERMOD/mmif/TWN_3X3 
$ cat point_ij.py 
from pyproj import Proj 
import numpy as np 
from pandas import * 
Latitude_Pole, Longitude_Pole = 23.61000, 120.990 
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, 
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0) 
df=read_csv('point_QC.csv') 
df['II']=[int(i/3000+83/2) for i,j in zip(df.UTM_E,df.UTM_N)] 
df['JJ']=[int(j/3000+137/2) for i,j in zip(df.UTM_E,df.UTM_N)] 
boo=(df.II>=0) & (df.JJ>=0) 
dfij=df.loc[boo].reset_index(drop=True) 
dfij['IJ']=dfij.II*1000+dfij.JJ 
dfij['X']=(dfij.II- 83/2)*3000+1500 
dfij['Y']=(dfij.JJ-137/2)*3000+1500 
pv=pivot_table(dfij,index='IJ',values=['X','Y'],aggfunc=np.mean).reset_index() 
X,Y=np.array(pv.X),np.array(pv.Y);lon, lat= pnyc(X,Y, inverse=True) 
pv['lon']=[round(i,3) for i in lon] 
pv['lat']=[round(i,3) for i in lat] 
pv.set_index('IJ').to_csv('point_ij.csv')
```
### mmif.inp樣版之準備

與前述樣版一致，作法略異

1. 年度起迄時間(line 1~2)：手工修改
2. 經緯度(LATI、LONG)(line 11, 18, 20 )：後續執行批次以sed修改
3. 結果檔案名稱(line 23~24)：後續執行批次以sed修改
4. 各年度WRF檔案路徑之收集(line 25~)
	- 先將各批次執行成果蒐集在各月份的wrfout下，再彙總到$btn/links下(詳WRF三維軌跡與叢集分析*)
	- 由於2020年係來自CWB WRF_3Km(中央氣象局WRF_3Km數值預報產品之下載及轉檔*)結果，有不同目錄，須分別處理。
	- 形成fname.txt_yy之後，再手工加入前後跨年度檔案路徑。
	- 將fname.txt_yy貼在mmif.inp_blank之後即可

```bash
for y in {16..19};do for i in {01..12};do for j in $(ls /nas1/backup/data/cwb/e-service/btraj_WRFnests/links/wrfout_d04_20${y}-${i}*);do echo INPUT $j;done;done>fname.txt_$y done
for i in {01..12};do for j in $(ls /nas1/backup/data/CWB_data/raw/*/wrfout_d04_2020-${i}*);do echo INPUT $j;done;done>fname.txt_20
```

### 平行運作之批次檔(do_mmif.cs)

運用動態控制執行緒數的原理(詳[entry linux]())，讓工作站所有CPU同時進行各格點MMIF的轉檔工作。批次檔內容及說明如下：

```bash
kuang@master /nas1/aermruns/mmif 
$ cat -n do_mmif2.cs 
  1 
  2  MMIF=/nas1/aermruns/mmif/src/mmif 
  3  for y in {16..20};do 
  4  for LINE in $(cat point_ij.csv|grep -v IJ);do 
  5    IJ=$(echo $LINE|cut -d',' -f1) 
  6    LONG=$(echo $LINE|cut -d',' -f4) 
  7    LATI=$(echo $LINE|cut -d',' -f5) 
  8    n=$(psg $MMIF|wc -l) 
  9    while true;do
10      if [ $n -lt 90 ];then 
11        mkdir -p 20$y/$IJ 
12        cd 20$y/$IJ 
13        cp ../../mmif.inp_blank$y mmif.inp 
14        for cmd in 's/xiehe.sfc/IJ'$IJ'.sfc/g' 's/xiehe.pfl/IJ'$IJ'.pfl/g' \ 
15          's/LONG/'$LONG'/g' 's/LATI/'$LATI'/g';do 
16          sed -i $cmd mmif.inp 
17        done 
18        sub $MMIF >& dum 
19        cd ../.. 
20        sleep 5s 
21        break 
22      else 
23        sleep 5s 
24        n=$(psg $MMIF|wc -l) 
25      fi 
26    done 
27  done 
28  done 
29
```
- 主要3層迴圈，由外而內依序為：WRF年代(y line3\~28)、每格點(LINE line4\~27)、與動態檢核CPU執行緒數n之while迴圈(keep n<90, line 9\~26)
- 網格IJ、經緯度等訊息藉由echo cut來傳到批次檔內
- 每執行批次所需的mmif.inp，以sed來替換(line 13~17)，置換之邏輯與前述版本CaaS相同。
- 啟動背景執行後隨即關閉while迴圈

### 執行成果

- 放在$web/mmif_results/20yy下，以供使用者在[uMap下載](https://umap.openstreetmap.fr/zh-tw/map/mmif-resultstwn_3x3_grids_588696#9/24.2983/121.8186)(詳[地圖上貼連結](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/UMAP/))、及(或)其他應用調用(主要是aermods.html或AERMOD.html)。
- 降雨量：
	- 降雨量是HRA評估必須要有的項目
	- 一般wrfout有降雨量，但在CWB_WRF須注意另外讀取([rd_grbCubicA.py](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/3.rd_grbCubicA/#rd_grbcubicapy分段說明)、[fil_grb_nc.py](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/fil_grb_nc/))。
- CWB_WRF資料缺漏補遺(mod_Times.py)

### 點位選取方式

1. 傳統輸入mmif.inp檔案。直接寫在檔案內。
2. 以uMap上點選，直接下載成果。
3. 輸入工廠建築物煙囪之KML檔案，由電腦選取結果供下載。

## Reference

- CGI(Common Gateway Interface，CGI)程式([通用网关接口](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3))
- [crontab](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/)
- Ask Difference, [How do I change the time format used by ls command line on osx?](https://apple.stackexchange.com/questions/15170/how-do-i-change-the-time-format-used-by-ls-command-line-on-osx)
- browser timeout
	- [请问chrome浏览器的默认超时时间是多久？](https://segmentfault.com/q/1010000011041316)
		- 测试时间：2019/02/26
		- MacOS 环境下，timeout在各浏览器默认值为（以下浏览器都为当前时间最新版本）
		- chrome 72.x 为4min
		- safari 12 为8min
		- firefox 65 貌似没有超时时间(編按：非然也，約3min)
	- [如何在 Internet Explorer 中變更預設的 keep-alive 超時值](https://docs.microsoft.com/zh-tw/troubleshoot/browsers/change-keep-alive-time-out)
	- [網站Time Out時自動轉到指定頁面告知使用者解決方法](https://ithelp.ithome.com.tw/questions/10185433)

### Family

- [中央氣象局WRF_3Km數值預報產品之下載及轉檔](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/1.get_M-A0064/)
- 地圖上貼連結*
- 
