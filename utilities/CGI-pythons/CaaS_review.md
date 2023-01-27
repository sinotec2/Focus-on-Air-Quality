---
layout: default
title: 網頁計算服務軟體系統的建置
parent: CGI-pythons
grand_parent: Utilities
date: 2023-01-26
last_modified_date: 2023-01-26 19:24:35
tags: CGI_Pythons review
---
# 網頁計算服務軟體系統的建置

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

## 前言

### 背景

近年來因搭上氣象預報服務的網路化，空氣污染的網路服務蓬勃發展，具有查詢、計算、繪圖、互動功能的網站也有如雨後春筍，工程上切割成下列模組：

    高強度計算核心模組：如氣象預報、光化模式、計算量大、時間長、計算成果圖資量龐大，需要簡化。
        此類服務網站如各（學術）計算中心對外的資料倉儲服務、資料加值應用服務（windy、Earth Nullschool、pm25.jp)等等。
        使用者不可能自由應用(如Amazon的EC2)中心的計算資源進行個案的計算。只能下載數據、查詢、應用成果。由於有存取權限管理，需要會員制度。
    微量或無計算、資料呈現模組：讀取opendata進行簡單內插、統計等之服務網站，如果測站密度觀測頻度夠高，也可以呈現足夠解析度之時空變化。
        也是屬於伺服器端一次計算之結果展現，展現程式之運作即使很複雜，也是在客戶端運作。伺服器只需要定期更新數據與少量簡單計算即可。
        如環保單位、或結合民間提供之查詢、展示系統、不需會員管理。
    介於前述二者之間的少量計算系統，即使不是複雜的模式，然而因為模式規模、或計算所需數據過於龐雜、成果無法單獨下載，系統無法單獨在客戶端實現，須借重遠端工作站之運作，但又因個案太多，不能一一事先算好等候使用者調用。
        如NOAA之HYSPLIT系統。
        雲端知識庫系統、協同作業平台、筆記系統等，基本上也是屬於此類架構。需要會員管理，但也可以不必。
        此類網頁計算服務系統有其發展潛力：
            適合公部門程式之運作，如標準（環境評估、許可程序）模式之應用、環境數據之加值計算模式等等，由官方發展之模式，
            需要計算資源不多，可與人共享，
            官方有提供之義務或道義責任。
            此一架構具有向前、後發展的彈性，逐步併入複雜的模式、或（及）併入一般的數據服務網站。
        相較於雲端運算的IaaS/SaaS/PaaS，此處提出的計算服務，算是小眾市場的CaaS（Computation as a Service網頁計算服務）。

### 界定軟硬體平台範圍與資源方案

除上述以計算多寡的角度、以下著眼更全面角度：

    計算機型式、模式軟體與作業環境
        無痛升級、進版；
        針對短期、簡單計算提供服務；
        利用遠端多核多工之工作站，減省個人電腦之計算資源
    伺服器與IP管理
        遠端工作站LAN：master、node03、DEVP：全時服務
        外部（IMacKuang）： 7~19時服務
    資料儲存
        歷史數據量龐大
        無法（也無必要）在個人電腦上都存放一份
        客戶所產生之數據：只需暫存，一定時間後予以刪除。
    網路傳輸：以文字檔案為主之傳輸、不需要太大頻寬，
    圖形顯示：在客戶端顯示、伺服器不產生、也不儲存。
    體軟串聯：由於需要伺服器端的協同運作，考慮以html(js)+cgi_python+工作站OS 組合來協力完成

### 目標

    模式標準化
    讓更多使用者運作工作站程式

## 計算流程規劃

    由於網頁計算服務的潛在對象非為一般大眾，乃屬專業、為數不多、但礙於資訊能力屏障，對操作工作站有困難者。此處採取策略：
        不登記會員、只記錄使用者IP備查
        計算由網頁動作觸發，由系統自行管理分派，只在系統有空檔時依序進行客戶之計算
        計算結果自動寄發(需時較久者)、或自動下載至客戶端(需時較短者)
        提供成果研判(繪圖)工具，由客戶自行研判計算成果的合理性
    HyperText Markup Language(html)是客戶端瀏覽器 開啟並執行的文本格式。HTML可以嵌入如JavaScript(js)的脚本语言，它们会影响HTML网页的行为。网页浏览器也可以引用层叠样式表（CSS）来定义文本和其它元素的外观与布局。
    除了js之外，html亦可由使用者觸發cgi_python程式，呼叫(或誘發)系統其他後端程式，讓網頁計算服務的運作更加彈性多元。
    cgi_python(Common Gateway Interface)程式可以：
        產生新的html界面，將成果提交客戶。
        呼叫伺服器上的批次檔，進行計算批次，適用於較為單純迅速之計算、或
        準備好檔案，交由系統crontab自動執行計算批次，適用需時較久，需進行排程管理之計算。
        有關CGI python可以參考itread01 網友的逐步教學(macOS必要之調適過程則詳見python CGI）。
    工作站系統的作業能力
        可以單獨進行計算服務
        亦可透過工作站間的協同作業，調用其他工作站進行作業並將成果回報客戶

## 伺服器端站台之管理

    一般網站的站台事實上就是某個遠端伺服器的某一個特定的目錄，是httpd指定公開的位置，任何對此目錄的讀取、檔案或程式的呼叫都會被記錄下來。複雜的輸入內容，還可以在伺服器端以資料庫系統(如sql)來儲存。網頁計算服務所需的httpd並無特別。
    使用者將透過其本身的瀏覽器開啟伺服器所公開的檔案，因而造成資料的讀取、作業的形成、啟動伺服器上所預設的計算工作，再透過CGI產生新的html，將成果提交使用者，完成串聯作業。
    由此可見，站台管理(管制)為使用者互動的第一手經驗，也是穩定度需求最高之界面。有關WWW伺服器的介紹可以參閱鳥哥的說明。

### apache(hpptd)安裝架設

centos
sudo  yum -y  install  httpd httpd-tools

    Linux從零開始(12/30): CentOS 7安裝 Apache Web Server 網頁伺服器 https://ithelp.ithome.com.tw/articles/10194699?sc=iThelpR
    Apache Web Server on CentOS 6 https://www.linode.com/docs/web-servers/apache/apache-web-server-on-centos-6/
    CentOS 6 Web Server 架站設定 https://blog.xuite.net/bravo.tw/profession/63349520-CentOS+6+Web+Server+架站設定
    CENTOS 6.4中Apache 安裝與設定 http://kirby86a.pixnet.net/blog/post/101076957
    httpd的設定檔：/etc/httpd/conf/httpd.conf

在 macOS 安裝 Apache HTTP Server
用brew就可以了。
httpd的設定檔：/usr/local/etc/httpd/httpd.conf
window系統
sinoic：目前尚不開放
家用電腦（PC）：因涉後端模式計算與作業系統，多以unix環境，考慮相容性、長遠發展、運作穩定性等，並不建議。

### 位置

- 視平台apache所指定之目錄，相關程式要在指定目錄下發展、測試及上線。
- 都需要管理者權限才能修改。任何人及群組可以讀取、執行。注意要關閉覆寫，以避免被駭。
- centos
- 
```bash
    /var/www/html為html程式所在位置，(撰寫內容討論如後)。
    /var/www/cgi-bin為cgi程式所在位置，(撰寫內容討論如後)。
```

```bash
kuang@node03 /var/www
$ lsd
drwxr-xr-x. 4 root root 4.0K Jan 21 16:01 cgi-bin/
drwxr-xr-x. 5 root root 4.0K Jan 21 16:00 html/
```

- macOS
  - mac沒有一個/var/www目錄。是放在/Library/WebServer/Documents及/Library/WebServer/Executables  。
  - macOS：/Library/WebServer

```bash
$ lsd
drwxr-xr-x  18 root  wheel  576 Jan 12 11:34 CGI-Executables 
drwxr-xr-x  63 root  wheel  2016 Jan 21 15:41 Documents
```

### 伺服器啟動與停止

以管理者權限執行，伺服器程式啟動後，不論何人都可以從遠端讀取、執行前述平台之html、cgi程式。
centos
以centos而言，服務的名稱為"httpd"

```bash
sudo service httpd start
sudo service httpd stop
sudo service httpd restart
```

macOS
macOS的服務名稱為apachectl， 開啟內建 Apache 網站伺服器與PHP環境設定

```bash
sudo apachectl start
sudo apachectl stop
sudo apachectl restart
```

夜間關閉的理由：避免駭客無謂之訪問、避免無人照顧狀況下運作工作站

```bash
sudo crontab -l
#stop and start of apache
0 19 *  *  * /usr/sbin/apachectl stop
0  7 *  *  * /usr/sbin/apachectl start
```

### 伺服器讀取(access)及錯誤(error)記錄

httpd會將外界的讀取、訪問等過程，寫在log目錄下，由此管理者可以從當中取得重要的訊息，包括訪問者的ip、時間、動作、以及錯誤相關訊息。
centos
sudo tail /var/log/httpd/access_log
sudo tail /var/log/httpd/error_log
macOSX

```bash
$ tail /var/log/apache2/access_log
3.83.221.198 - - [26/Jan/2021:11:46:52 +0800] "GET /Leaflet/docs/index.js HTTP/1.1" 200 1687
18.232.131.38 - - [26/Jan/2021:11:47:07 +0800] "GET /Leaflet/docs/index.html HTTP/1.1" 200 913
54.85.218.152 - - [26/Jan/2021:11:47:29 +0800] "GET /trj_results/btrjdouliu2021012412.csv.kml HTTP/1.1" 200 24768
35.173.246.154 - - [26/Jan/2021:11:48:17 +0800] "GET /Leaflet/docs/menu.js HTTP/1.1" 200 405
172.105.234.247 - - [26/Jan/2021:11:58:39 +0800] "GET / HTTP/1.1" 200 45
58.213.215.154 - - [26/Jan/2021:12:03:50 +0800] "SSH-2.0-libssh2_1.4.2" 400 226
220.119.177.89 - - [26/Jan/2021:12:34:09 +0800] "GET / HTTP/1.0" 200 45
23.129.64.231 - - [26/Jan/2021:12:43:51 +0800] "GET / HTTP/1.1" 200 45
5.40.162.193 - - [26/Jan/2021:12:52:24 +0800] "GET / HTTP/1.1" 200 45
89.248.170.31 - - [26/Jan/2021:13:09:35 +0800] "POST /tools.cgi HTTP/1.1" 403 218
```

- 26/Jan/2021:11:46:52 ~11:48:17  +0800為正常之應用。其後為駭客之活動。

```bash
$ cat -n /var/log/apache2/error_log |tail
53491  [Mon Jan 25 21:03:50.758588 2021] [cgi:error] [pid 34671] [client 186.33.122.245:40010] AH02809: Options ExecCGI is off in this directory: /Library/WebServer/Documents/setup.cgi
53492  [Mon Jan 25 21:14:21.097720 2021] [php7:error] [pid 34706] [client 45.155.205.108:46482] script '/Library/WebServer/Documents/index.php' not found or unable to stat
53493  [Mon Jan 25 21:50:55.713811 2021] [mpm_prefork:notice] [pid 1579] AH00169: caught SIGTERM, shutting down
53494  [Tue Jan 26 10:40:15.256431 2021] [mpm_prefork:notice] [pid 68343] AH00163: Apache/2.4.34 (Unix) PHP/7.1.23 mod_perl/2.0.9 Perl/v5.18.4 configured -- resuming normal operations
53495  [Tue Jan 26 10:40:15.256508 2021] [core:notice] [pid 68343] AH00094: Command line: '/usr/sbin/httpd -D FOREGROUND'
53496  [Tue Jan 26 13:09:35.240056 2021] [cgi:error] [pid 70181] [client 89.248.170.31:38770] AH02809: Options ExecCGI is off in this directory: /Library/WebServer/Documents/tools.cgi, referer: http://114.32.164.198:80/tools.cgi
[Mon Jan 25 21:50:55.713811 2021 ... caught SIGTERM, shutting down →關閉httpd程式(line 53493  )
[Tue Jan 26 10:40:15.256431 2021 ... resuming normal operations→開啟httpd程式 (line 53494   )
[Tue Jan 26 13:09:35.240056 2021]→駭客搜尋的檔案不存在，發生錯誤。(line  53496  )
```

### tomcat及mysqld等其他伺服器

    html當中如果有簡單的JavaScript(js)程式，在客戶端就可以執行，不需要存在伺服器。然而完整的java功能，就必須由伺服器端的tomcat來提供。
        tomcat提供了Java Servlet, JavaServer Pages, Java Expression Language and Java WebSocket technologies的作業環境，功能非常強大。
        因此，如果系統有較為完整的java程式，就必須同時提供tomcat環境，來執行客戶所誘發的作業，例如在知識庫系統(openKM)中，除了httpd之外，還必須有tomcat運作。
    客戶在伺服器端存放的資料，往往也是駭客最有興趣的部分，必須由資料庫系統保管，
        目前一般最常用mysqld系統，其他如mango、SQlite等也都非常活躍(詳見List of wiki software、wikipedia)。
        諸如會員系統之管理、知識庫系統、協同作業等等，都需要此類資料庫系統保持運作。



六、iscParser
iscParser.html
網頁計算服務網址：http://200.200.31.47/iscParser.html
畫面：



iscParser.html
2.3 KB

    有二個物件，就是貼上文字+檔案上傳。

isc_parser.py

    因為ISC/AERMOD的面源可以旋轉方向，因此程式的主要功能在求取旋轉後的矩形頂點座標。(函數rotate_about_a_point line 11~15)
        原來座標P(line 42)、角度angl(line 43)，代入函數得到旋轉後的座標(line 44~45)
    應用csv2kml.py將頂點座標輸出為多邊形kml(csv2kml.py有相應進版)
    調用data-auto-download將結果下載到客戶硬碟。

isc_parser.py
3.0 KB
cat -n isc_parser.py
    1  #!/usr/bin/python
    2  # /cluster/miniconda/envs/py37/bin/python
    3  # -*- coding: UTF-8 -*-
    4
    5  import cgi, os, sys
    6  import cgitb
    7  import tempfile as tf
    8  import math
    9  import numpy as np
    10  from pandas import *
    11  def rotate_about_a_point(target_point,center_point,angle_rs):
    12    cp=np.subtract(target_point,center_point)
    13    px=cp[0]*math.cos(math.radians(angle_rs))+cp[1]*-math.sin(math.radians(angle_rs))
    14    py=cp[0]*math.sin(math.radians(angle_rs))+cp[1]*math.cos(math.radians(angle_rs))
    15    return(np.add([px,py],center_point))
    16
    17
    18  form = cgi.FieldStorage()
    19  STR = str(form.getvalue("iscinp"))
    20  os.system('echo "'+STR+'"> /tmp/isc.out')
    21  #read the origins
    22  loc='SO LOCATION'
    23  iorg=STR.index(loc)
    24  inp=STR[(iorg+len(loc)):].split()
    25  snamo=inp[0]
    26  pav=inp[1] #POINT/AREA/VOLUME tag
    27  orig=[float(inp[i]) for i in range(2,4)]
    28
    29  #read the area sources
    30  par='SO SRCPARAM'
    31  ipar=STR.index(par)
    32  inp=STR[(ipar+len(par)):].split()
    33  snamp=inp[0]
    34  if snamo!=snamp:
    35    os.system('echo "names of LOC/PAR not right: '+snamo+' vs '+snamp+'">> /tmp/isc.out')
    36    sys.exit('') #premature error
    37  fname='/var/www/html/trj_results/'+snamp+'.csv'
    38  fnames=[]
    39  if pav=='AREA':
    40    lab=['p'+str(i) for i in range(4)]
    41    X,Y=[float(inp[i]) for i in range(3,5)]
    42    P=[ [0,0],[X,0],[X,Y],[0,Y] ]
    43    angl=-float(inp[5])
    44    Pn=[rotate_about_a_point(pnt,P[0],angl) for pnt in P]
    45    ttt=np.array(Pn)+np.array(orig*4).reshape(4,2)
    46    df=DataFrame({'X':ttt[:,0],'Y':ttt[:,1],'nam':lab,'lab':lab})
    47    df.set_index('X').to_csv(fname)
    48    os.system('/usr/kbin/csv2kml.py -n P -g TWD97 -f '+fname+'>> /tmp/isc.out')
    49    fnames.append(fname)
    50
    51  rec='RE DISCCART'
    52  if rec in STR:
    53    fname='/var/www/html/trj_results/'+snamp+'R.csv'
    54    nrec=STR.count(rec)
    55    lab=['p'+str(i) for i in range(nrec)]
    56    jrec=0
    57    X,Y=[],[]
    58    for r in range(nrec):
    59      irec=STR[jrec:].index(rec)+jrec
    60      inp=STR[(irec+len(par)):].split()
    61      Xi,Yi=[float(inp[i]) for i in range(2)]
    62      X.append(Xi);Y.append(Yi)
    63      jrec+=irec+1
    64    df=DataFrame({'X':X,'Y':Y,'nam':lab,'lab':lab})
    65    df.set_index('X').to_csv(fname)
    66    os.system('/usr/kbin/csv2kml.py -n N -g TWD97 -f '+fname+'>> /tmp/isc.out')
    67    fnames.append(fname)
    68
    69  print """\
    70  Content-Type: text/html\n\n
    71    <html>
    72    <head>
    73      <title>ISC_setting KML results</title>
    74      <meta name="viewport" content="width=device-width, initial-scale=1">
    75          <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    76          <script>
    77          $(function() {
    78                  $('a[data-auto-download]').each(function(){
    79                          var $this = $(this);
    80                          setTimeout(function() {
    81                          window.location = $this.attr('href');
    82                          }, 2000);
    83                  });
    84          });
    85          </script>
    86    </head>
    87    <body>
    88    <p>The KML download should start shortly. If it doesn't, click
    89    """
    90  for fname in fnames:
    91    print """\
    92    <a data-auto-download href="%s">%s</a>
    93    """  % (fname.replace('/var/www/html','../..')+'.kml',fname.split('/')[-1])
    94  print """\
    95    </p><p>The KML may be posted on google map or OpenStreet interface:
    96    <a href=http://114.32.164.198/Leaflet.FileLayer/docs/index.html>Leaflet.FileLayer</a>.</p>
    97    </body>
    98    </html>
    99    """

Reference

Articles

    Wiki 
    Computing as a Service By Melissa Rudy Updated: May 15, 2012 https://www.comparebusinessproducts.com/cloud/who-needs-computing-as-a-service 

Sites
CaaS examples:

    LookToTheRight LTTR

Links
Here:網頁計算服務軟體系統的建置(*)
Relatives
terrain_caas
