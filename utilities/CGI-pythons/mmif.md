---
layout: default
title: MMIF計算服務
parent: CGI-pythons
grand_parent: Utilities
date: 2023-01-26
last_modified_date: 2023-01-26 19:24:35
tags: CGI_Pythons mmif
---
# MMIF計算服務

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

網頁計算服務網址：http://200.200.31.47/mmif.html
畫面：


(一)mmif.html
此網頁提供了MMIF的計算服務。除了提供檔案選擇、讀取、email之記錄等功能之外，mmif.html也會啟動CGI程式(/cgi-bin/save_file.py)，並在os.system(...)函數的功能運作下，誘發工作站上的批次檔，進行模式計算、成果打包與寄發信件等流程。

    mmif.html調用了jquery的filepicker模組(line 10、14~15、17~20、22~28、66~68)，進行檔案讀取，物件名稱為filename
        參考網友提供的filepicker、併入itread01逐步教學的text input寫成。
    button物件則讀取客戶所鍵入之emailadd文字
    此二元素將會在後面觸發的cgi_python(save_file.py)讀取，進行mmif計算的準備

```html
$ cat -n mmif.html
    1  <!DOCTYPE HTML>
    2  <html>
    3    <head>
    4      <meta charset="utf-8"/>
    5      <title>MMIF</title>
    6      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    7      <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    8
    9
    10      <script src="http://codeorigin.jquery.com/jquery-1.10.2.min.js"></script>
    11
    12      <script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    13
    14      <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"></script>
    15      <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/themes/smoothness/jquery-ui.css">
    16
    17      <script src="jquery.example.js"></script>
    18      <!script src="../../mugen.js/src/mugine.js"></script>
    19      <script src="../src/js/jquery.filepicker.js"></script>
    20      <link rel="stylesheet" href="../src/css/filepicker.default.css">
    21
    22      <script>
    23        $(document).ready(function() {
    24          $("input[type='file'].filepicker-jquery-ui").filepicker({
    25            style: 'jquery-ui'
    26          });
    27        });
    28      </script>
    29
    30      <style>
    31        .filepicker-preview .thumbnail {
    32          max-width: 100px;
    33          display: inline-block;
    34        }
    35        .filepicker-preview .thumbnail img {
    36          max-width: 100%;
    37        }
    38      </style>
    39      <script>
    40      $(document).ready(function(){
    41      // Get value on button click and show alert
    42          $("#myBtn").click(function(){
    43              var str = $("#myInput").val();
    44              alert(str);
    45          });
    46      });
    47      </script>
    48
    49    </head>
    50
    51    <body>
    52
    53      <header class="subhead" id="overview">
    54        <div class="container">
    55          <h1>mmif 遠端執行系統</h1>
    56          <p class="lead">上傳準備好的mmif.inp，遠端執行mmif程式結束後會由系統電郵結果網址給您(恕僅保留24小時)。
    57          </p>
    58        </div>
    59      </header>
    60
    61      <div class="container">
    62
    63        <div class="row">
    64          <div class="col-md-4">
    65                  <form enctype="multipart/form-data" action="/cgi-bin/save_file.py" method="post">
    66            <p><input data-label="File:" class="filepicker-jquery-ui" type="file"
    67                    placeholder="Select a file..." multiple="multiple"
    68                    name="filename"/> </p>
    69            <p> 您的 EMAIL:
    70                    <input type="text" id="myInput" name="emailadd"> <button type="button" id="myBtn">check</button></p>
    71                    <p style="text-align:center;"> <input type="submit" value="Upload and Run mmif remotely" /></p>
    72                  </form><p>      </p><p>        </p>
    73                  <p>Introduction of AERMOD, AERMET, MMIF etc, please visit <a href="https://www.epa.gov/scram/air-quality-dispersion-modeling-related-model-support-programs#mmif"> USEAP SCRAM</a>. </p>
    74                  <p>MMIF  <a href="https://www3.epa.gov/ttn/scram/models/relat/mmif/MMIF_Guidance.pdf">User Guide</a> </p>
    75                  <p>Contact: Dr. Yungchuan Kuang, sinotec2@gmail.com</p>
    76          </div>
    77        </div>
    78
    79      </div>
    80
    81    </body>
    82
    83  </html>
```

mmif.html
2.8 KB
(二)save_file.py
程式設計重點

    CGI的基本功能，在於儲存、傳遞html的內容(line 9、15~16)，並產生新的html提交執行程果(print內容 line 51~62)
    隨機檔名在使用者存檔時就產生，以目錄型態存在，可供後續（前述）macOS 批次檔進行辨識。
        取代會員制度、cookie偵測、等繁瑣過程、減輕系統負荷。
    如果html有emailadd及檔案名稱filename傳上來：
        判斷檔名是否準確
            判斷目錄是否有已經簽收執行的mmif.recieved，以避免重複。（雖然隨機重複的機會很小，但還是需提防）
            用集合判斷mmif每行的第1個keyword是否都有
                (TIMEZONE似乎沒有也可以執行，但因為WRF是GTM，有8小時時差，在日均值的判定上將會造成誤差)
                上傳的mmif.inp檔案將被刪除(CGI似乎不允許整個目錄一次刪除，但還好這會在root的crontab中執行)
        檔名不對、跳出不執行。
        沒有email(空白)或email內中沒有@字元，也跳出不執行。

save_file.py
1.9 KB

```bash
kuang@114-32-164-198 /Library/WebServer/CGI-Executables
$ cat -n save_file.py
    1  #!/usr/bin/python
    2  # -*- coding: UTF-8 -*-
    3
    4  import cgi, os, sys
    5  import cgitb; cgitb.enable()
    6  import tempfile as tf
    7
    8
    9  form = cgi.FieldStorage()
    10
    11  mmif_parm=['AER_MIN_OBUK', 'POINT', 'AER_LAYERS', 'AER_MIN_MIXHT', 'INPUT', 'GRID', 'TIMEZONE', 'PBL_RECALC', 'AER_MIN_SPEED', 'OUTPUT', 'STOP', 'FSL_INTERVAL', 'LAYERS', 'STABILITY', 'START']
    12  mmif_parm=set(mmif_parm)
    13  ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
    14  # 獲取檔名
    15  fileitem = form['filename']
    16  emailadd = form.getvalue('emailadd')
    17  pth='/tmp/mmif_'+ran+'/'
    18  os.system('mkdir -p '+pth)
    19  os.system('chmod og+w '+pth)
    20  open(pth+'/mmif.email', 'wb').write(emailadd+'\n')
    21  # 檢測檔案是否上傳
    22  if fileitem.filename:
    23    # 設定檔案路徑
    24    fn = os.path.basename(fileitem.filename)
    25    if fn == 'mmif.inp':
    26      if os.path.exists(pth+'mmif.recieved') or os.path.exists(pth+'mmif.inp'):
    27        message = 'mmif is running, please wait...'
    28      else:
    29        open(pth+fn, 'wb').write(fileitem.file.read())
    30  #checking the parameters in file are all correct
    31        with open(pth+fn,'r') as ftext:
    32          d=[line.strip('\n').split() for line in ftext if line[0] not in ['#', ';','\n'] and len(line)>0]
    33        s=set([i[0].upper() for i in d if len(i)>0])
    34        mms=list(mmif_parm-s)
    35        if len(mms)>0:
    36          ss=mms[0]
    37          if len(mms)>1:
    38            for i in mms[1:]:
    39              ss+=', '+i
    40          os.system('/bin/rm -fr '+pth+fn)
    41          message = 'mmif parameter not right, please check the parameters of '+ss+'.'
    42        else:
    43          message = '檔案 "' + fn + '" 上傳成功please check your email...'
    44    else:
    45      message = '\"'+fn+'\" was not uploaded, only "mmif.inp" is permitted'
    46  else:
    47    message = '檔案沒有上傳'
    48
    49  if len(emailadd)==0 or '@' not in emailadd:
    50    message='please enter your email address correctly!'
    51  print """\
    52  Content-Type: text/html\n
    53  <html>
    54  <head>
    55  <meta charset="utf-8">
    56  <title>MMIF respond</title>
    57  </head>
    58  <body>
    59    <p>%s</p>
    60  </body>
    61  </html>
    62  """ % (message,)
```

### 批次執行說明

執行分2個伺服器身份進行，cybee為計算執行者，root則為檔案管理者，由crontab進行自動執行之管控。以crontab管控而非硬式之批次檔的理由：

    由於模式執行時間較久，且模式程式無法多工進行，有可能造成系統計算資源的耗竭與壅塞
    由系統掌控，而非客戶觸發，增加系統穩定度
    執行時間較為彈性，可以同時接受多項要求且不至當機

1.cybee crontab contents:

    執行頻率
        doing per min..

*/1 * * * * /Users/cybee/mmif_cron.cs >& /Users/cybee/mmif_cron.out

    執行內容(計算啟動之檢查、控制、執行、郵寄)
        /Users/cybee/mmif_cron.cs contents
            執行邏輯
                電腦負荷太多時、跳開不執行（設定為6個mmif工作）(line 6)
                使用者開了目錄（隨機產生名字），才能執行。開了目錄的2天後將不會存在。
                依照目錄順序進行檢查、執行：(line 11)
                    如果有email但是還沒有寄過ACCEPTED第一封信，則執行寄信動作。指標為emai_bak檔案是否存在(line 14~22)。
                    目錄下如果有mmif.inp檔案、卻沒有mmif.out檔案，則開始執行程式、製作成果壓縮檔、寄發第二封信RESULT。(line 24~39)
                    下一個目錄

```bash
    1
    2 #ensure not to many mmif are running
    3 n=$(ps -ef|grep /opt/local/bin/mmif|wc -l)
    4 n=$(( $n - 1 ))
    5 if [ $n -le 6 ];then
    6
    7 #ensure mmif.inp was put to the directory
    8 m=$(ls /tmp|grep mmif_|wc -l)
    9 if [ $m -gt 0 ];then
    10
    11 for dr in $(ls /tmp|grep mmif_);do
    12 dir=/tmp/$dr
    13 #ensure email was given
    14 if ! [ -e $dir/mmif.email_bak ] && [ -e $dir/mmif.email ];then
    15 #send first email   
    16     emailadd=$(cat $dir/mmif.email)
    17     echo "Hello MMIF user:\n Your mmif submit was accepted, please wait and check this email.\
    18 since $n mmif are running   
    19 The resultant tgz file will send to you and the file will be erased after 24 hrs! \n \
    20 (sent by machine do not reply)" | mail -s "MMIF ACCEPTED" $emailadd
    21     cp $dir/mmif.email $dir/mmif.email_bak
    22 fi
    23
    24 #ensure mmif.inp exist and perform mmif
    25 if [ -e $dir/mmif.inp ];then
    26     if ! [ -e $dir/mmif.out ];then
    27     cd $dir
    28     cp mmif.inp mmif.recieved
    29     /opt/local/bin/mmif>mmif.out
    30     /usr/bin/zip result.zip *
    31 emailadd=$(cat $dir/mmif.email)
    32     echo "Hello MMIF user:\n Your mmif result was at http://114.32.164.198$dir/result.zip\n \
    33 Please fetch the file as soon as possible,\n \
    34     The file will be erased after 24 hrs!\n \
    35 (sent by machine do not reply)" | mail -s "MMIF RESULT" $emailadd
    36 #        for i in $(ls|grep -v result.zip);do rm -f $i;done
    37 #    rm -f $dir/result.zip|at now+24 hours
    38     fi
    39 fi
    40 done
    41 fi
    42 fi
```

2.root

    執行頻率
        doing per day.
    執行內容(檔案管理)
        執行成果、設定必須定期清理，避免硬碟消耗。此處設定為24小時後，考慮到時間差，最長為2日。
        必須由root來清理的理由是使用者(_www)開啟的目錄、檔案，即使由CGI_python程式宣告屬性為777，仍然不能被其他一般使用者（如mmif的實際執行者cybee）刪除。
        macOS的ls沒有ISO格式，必須使用gls (詳參)
        MacOS的date也有差異。

```bash
#remove the mmif_* 2 days ago
0 0  *  *  * cd /tmp;dd=$(/bin/date -j -v-2d +"%Y-%m-%d");for i in $(/usr/local/bin/gls -l --time-style=full-iso|grep mmif_|grep $dd|/opt/local/bin/awkk 9);do rm -fr $i;done
```
