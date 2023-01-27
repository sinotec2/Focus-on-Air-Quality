---
layout: default
title: 空品測站正/反軌跡kml檔案產生系統
parent: CGI-pythons
grand_parent: Utilities
date: 2023-01-26
last_modified_date: 2023-01-26 19:24:35
tags: CGI_Pythons mmif
---
# 空品測站正/反軌跡kml檔案產生系統

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

或參自動版：[臺灣地區高解析度軌跡產生/自動分析系統](surf_trajLL2.md)

五、traj
網頁計算服務網址：http://125.229.149.182/traj.html @iMacKuang[^9]
畫面：

    畫面左側的5個物件，主要是3個下拉選單(selectmenu)、一個日期選單(datepicker)、以及一個button submit物件做為整體提交並呼叫cgi_python(traj/surf_traj3.py)的觸發。右方則為一典型範例，說明模式計算能力(軌跡會繞山)。
    選單都是jquery套件，其中測站較為複雜，是連動下拉選單，主要應用append方法，按照前一選擇結果，依序帶出後一選單的內容。
    提供cgi_python的變數：dirFB(正/反軌跡的方向選擇)、AQSname(測站代碼)、date(日期)、number(小時)，4項變數。

### traj.html
11.5 KB

```html
$ cat -n traj.html
    1  <!doctype html>
    2  <html lang="en">
    3  <head>
    4    <meta charset="utf-8">
    5    <title>TRAJ Selectmenu</title>
    6    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    7    <link href="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    8    <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
    9    <link rel="stylesheet" href="/resources/demos/style.css">
    10    <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/themes/smoothness/jquery-ui.css">
    11    <style>
    12      fieldset {
    13        border: 0;
    14      }
    15      label {
    16        display: block;
    17        margin: 30px 0 0 0;
    18      }
    19      .overflow {
    20        height: 200px;
    21      }
    22    </style>
    23    <script src="https://code.jquery.com/jquery-1.11.1.min.js"></script>
    24    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    25    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    26    <script>
    27    $( function() {
    28      $( "#dirFB" ).selectmenu();
    29      $( "#KPQname" )
    30        .selectmenu( "menuWidget" )
    31          .addClass( "overflow" );
    32      $( "#CNTname" ).selectmenu();
    33      $( "#AQSname" ).selectmenu();
    34      $( "#number" )
    35        .selectmenu()
    36        .selectmenu( "menuWidget" )
    37          .addClass( "overflow" );
    38      $( "#emailadd" ).selectmenu();
    39    } );
    40    </script>
    41  <style>
    42  #SIDE {
    43
    44      width:900px; /* <div> 要設定寬度，才能配合 float 做水平靠左或靠右排列 */
    45
    46      float:right; /* 使用 float 讓這個 <div> 做水平靠左排列 */
    47  }
    48  </style>
    49  </head>
    50  <body>
    51
    52      <header class="subhead" id="overview">
    53        <div class="container">
    54          <h1>空品測站正/反軌跡kml檔案產生系統</h1>
    55          <p class="lead">
    56  選取正/反軌跡、環保署空氣品質測站、以及到達(起始)之時間，系統將在遠端工作站進行計算。
    57  點選檔案下載到使用者電腦即可進行google map/OSM繪圖。(恕僅保留24小時)
    58          </p>
    59  <h6>
    60  <p>觀測數據：中央氣象局逐時自動站(2016/1/1至昨日) </p>
    61  <p>內插網格：臺灣本島範圍、解析度1公里 </p>
    62  <p>軌跡點時間間距：15秒(曲線)、1小時(圓點) </p>
    63  </h6>
    64        </div>
    65      </header>
    66  <div id="SIDE"> <img src="chaozhou.PNG" width="600" height="400"        >      </div>
    67  <div class="container">
    68  <div class="col-md-4">
    69  <form enctype="multipart/form-data" action="/cgi-bin/traj/surf_traj3.py" method="post">
    70
    71    <fieldset>
    72      <label for="dirFB">正/反軌跡</label>
    73      <select name="dirFB" id="dirFB">
    74        <option value="btrj">反軌跡</option>
    75        <option value="ftrj">正軌跡</option>
    76      </select>
    77
    78      <label for="KPQname"> 空氣品質區及測站 </label>
    79      <select name="KPQname" id="KPQname">
    80          <option value="0">請選擇</option>
    81          <option value="1">北部空品區</option>
    82          <option value="2">竹苗空品區</option>
    83          <option value="3">中部空品區</option>
    84          <option value="4">雲嘉南空品區</option>
    85          <option value="5">高屏空品區</option>
    86          <option value="6">宜蘭花東</option>
    87          <option value="7">離島</option>
    88      </select>
    89      <select name="CNTname" id="CNTname"></select>
    90      <select name="AQSname" id="AQSname"></select>
    91
    92      <label for="date">到達(起始)日期(昨天以前) </label><p> <input type="text" name="date" id="dt1"></p>
    93      <label for="number">到達(起始)時間 </label>
    94      <select name="number" id="number">
    95        <option value="01">1</option>
    96        <option value="02">2</option>
    97        <option value="03">3</option>
    98        <option value="04">4</option>
    99        <option value="05">5</option>
  100        <option value="06">6</option>
  101        <option value="07">7</option>
  102        <option value="08">8</option>
  103        <option value="09">9</option>
  104        <option value="10">10</option>
  105        <option value="11">11</option>
  106        <option value="12" selected="selected">12</option>
  107        <option value="13">13</option>
  108        <option value="14">14</option>
  109        <option value="15">15</option>
  110        <option value="16">16</option>
  111        <option value="17">17</option>
  112        <option value="18">18</option>
  113        <option value="19">19</option>
  114        <option value="20">20</option>
  115        <option value="21">21</option>
  116        <option value="22">22</option>
  117        <option value="23">23</option>
  118        <option value="24">24</option>
  119      </select>
  120
  121    </fieldset>
  122  <p style="text-align:left;"> <input type="submit" value="OK and Run TRAJ remotely..." /></p>
  123  <h6><p>Contact: Dr. Yungchuan Kuang, sinotec2@gmail.com</p></h6>
  124  </form>
  125
  126  </div>
  127  </div>
  128
  129          <script>
  130          $("#KPQname").change(function(){
  131    switch (parseInt($(this).val())){
  132    default:
  133    case 0:
  134        $("#CNTname option").remove();
  135        break;
  136    case 1:
  137        $("#CNTname option").remove();
  138        var array = [  "請選擇",  "基隆市", "台北市", "新北市", "桃園市"    ];
  139        var CNTva = [ "0", "1", "3", "2", "4" ];
  140        $.each(array, function(i, val) {
  141          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + array[i] + "</option>"));
  142        });
  143        break;
  144    case 2:
  145        $("#CNTname option").remove();
  146        var CNTnm = [ "請選擇",  "竹苗" ];
  147        var CNTva = [ "0", "5", ];
  148        $.each(CNTnm, function(i, val) {
  149          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + CNTnm[i] + "</option>"));
  150        });
  151        break;
  152    case 3:
  153        $("#CNTname option").remove();
  154        var CNTnm = [  "請選擇",  "台中市", "彰化南投"  ];
  155        var CNTva = [ "0", "6", "7" ];
  156        $.each(CNTnm, function(i, val) {
  157          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + CNTnm[i] + "</option>"));
  158        });
  159        break;
  160    case 4:
  161        $("#CNTname option").remove();
  162        var CNTnm = [  "請選擇",  "雲林縣", "嘉義縣市", "台南市"  ];
  163        var CNTva = [ "0", "8", "9", "10" ];
  164        $.each(CNTnm, function(i, val) {
  165          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + CNTnm[i] + "</option>"));
  166        });
  167        break;
  168    case 5:
  169        $("#CNTname option").remove();
  170        var CNTnm = [ "請選擇",  "高雄市","(原高雄縣)", "屏東縣" ];
  171        var CNTva = [ "0", "12", "11", "13"];
  172        $.each(CNTnm, function(i, val) {
  173          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + CNTnm[i] + "</option>"));
  174        });
  175        break;
  176    case 6:
  177        $("#CNTname option").remove();
  178        var CNTnm = [ "請選擇",  "宜蘭花東" ];
  179        var CNTva = [ "0", "14" ];
  180        $.each(CNTnm, function(i, val) {
  181          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + CNTnm[i] + "</option>"));
  182        });
  183        break;
  184    case 7:
  185        $("#CNTname option").remove();
  186        var CNTnm = [ "not available" ];
  187        var CNTva = [ "0" ];
  188        $.each(CNTnm, function(i, val) {
  189          $("#CNTname").append($("<option value='" + CNTva[i] + "'>" + CNTnm[i] + "</option>"));
  190        });
  191        break;
  192  }
  193  });
  194          </script>
  195          <script>
  196          $("#CNTname").change(function(){
  197    switch (parseInt($(this).val())){
  198    default:
  199    case 0:
  200        $("#AQSname option").remove();
  201        break;
  202    case 1:
  203        $("#AQSname option").remove();
  204        var AQSnm = [ "基隆"  ];
  205        var AQSva = [ "1" ];
  206        $.each(AQSnm, function(i, val) {
  207          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  208        });
  209        break;
  210    case 2:
  211        $("#AQSname option").remove();
  212        var array = [ "汐止","萬里","新店","土城","板橋","新莊","菜寮","林口","淡水","三重","永和"  ];
  213        var AQSva = [ "2","3","4","5","6","7","8","9","10","67","70" ];
  214        $.each(array, function(i, val) {
  215          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + array[i] + "</option>"));
  216        });
  217        break;
  218    case 3:
  219        $("#AQSname option").remove();
  220        var AQSnm = [ "士林","中山","萬華","古亭","松山","大同","陽明" ];
  221        var AQSva = [  "11","12","13","14","15","16","64" ];
  222        $.each(AQSnm, function(i, val) {
  223          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  224        });
  225        break;
  226    case 4:
  227        $("#AQSname option").remove();
  228        var AQSnm = [  "桃園","大園","觀音","平鎮","龍潭","中壢"    ];
  229        var AQSva = [  "17","18","19","20","21","68"];
  230        $.each(AQSnm, function(i, val) {
  231          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  232        });
  233        break;
  234    case 5:
  235        $("#AQSname option").remove();
  236        var AQSnm = [  "湖口","竹東","新竹","頭份","苗栗","三義"  ];
  237        var AQSva = [ "22", "23","24","25","26","27" ];
  238        $.each(AQSnm, function(i, val) {
  239          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  240        });
  241        break;
  242    case 6:
  243        $("#AQSname option").remove();
  244        var AQSnm = [ "豐原","沙鹿","大里","忠明","西屯"  ];
  245        var AQSva = ["28","29","30","31","32" ];
  246        $.each(AQSnm, function(i, val) {
  247          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  248        });
  249        break;
  250    case 7:
  251        $("#AQSname option").remove();
  252        var AQSnm = ["彰化","線西","二林","南投","竹山","埔里"  ];
  253        var AQSva = [ "33","34","35","36","69","72" ];
  254        $.each(AQSnm, function(i, val) {
  255          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  256        });
  257        break;
  258    case 8:
  259        $("#AQSname option").remove();
  260        var AQSnm = [ "斗六","崙背","台西","麥寮"  ];
  261        var AQSva = [  "37","38","41","83"];
  262        $.each(AQSnm, function(i, val) {
  263          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  264        });
  265        break;
  266    case 9:
  267        $("#AQSname option").remove();
  268        var AQSnm = [ "新港","朴子","嘉義"  ];
  269        var AQSva = [ "39","40","42" ];
  270        $.each(AQSnm, function(i, val) {
  271          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  272        });
  273        break;
  274    case 10:
  275        $("#AQSname option").remove();
  276        var AQSnm = ["新營","善化","安南","台南"  ];
  277        var AQSva = [ "43","44","45","46" ];
  278        $.each(AQSnm, function(i, val) {
  279          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  280        });
  281        break;
  282    case 11:
  283        $("#AQSname option").remove();
  284        var AQSnm = ["美濃","橋頭","仁武","鳳山","大寮","林園","楠梓"  ];
  285        var AQSva = ["47","48","49","50","51","52","53"  ];
  286        $.each(AQSnm, function(i, val) {
  287          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  288        });
  289        break;
  290    case 12:
  291        $("#AQSname option").remove();
  292        var AQSnm = [ "左營","前金","前鎮","小港","復興"  ];
  293        var AQSva = [ "54","56","57","58","71" ];
  294        $.each(AQSnm, function(i, val) {
  295          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  296        });
  297        break;
  298    case 13:
  299        $("#AQSname option").remove();
  300        var AQSnm = [ "屏東","潮州","恆春"  ];
  301        var AQSva = [ "59","60","61"  ];
  302        $.each(AQSnm, function(i, val) {
  303          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  304        });
  305        break;
  306    case 14:
  307        $("#AQSname option").remove();
  308        var AQSnm = ["花蓮","宜蘭","冬山","關山","臺東"  ];
  309        var AQSva = [ "63","65","66","80","62"  ];
  310        $.each(AQSnm, function(i, val) {
  311          $("#AQSname").append($("<option value='" + AQSva[i] + "'>" + AQSnm[i] + "</option>"));
  312        });
  313        break;
  314  }
  315  });
  316          </script>
  317      <script>
  318          $(function () {
  319              $("#dt1").datepicker({
  320                  dateFormat: "yymmdd",
  321                  onSelect: function () {
  322                      var startDate = $(this).datepicker('getDate');
  323                          }
  324                  });
  325          });
  326          </script>
  327
  328  </body>
  329  </html>
```

### surf_traj3.py

    主要為地面軌跡計算程式負責計算(traj2kml.py)，在程式中以os.system()呼叫，立即執行。主要理由是因為:
        程式執行時間較短，很快會有結果，再加上...
        系統會尋找過去執行成果，如果已經計算過了，將會直接提交結果，不再另行計算，以減省需要時間。
    此處以測站代碼，而非測站名稱進行計算，traj2km.py有因而進版。
    調用jquery的data-auto-download，直接下載成果檔案到客戶端的「下載」目錄。
    提供Leaflet連結，讓客戶可以馬上檢視成果，自行研判是否合理。
        Leaflet的設定在index.js裏(詳下)
        surf_traj3.py
        2.1 KB

```html
$ cat -n surf_traj3.py
    1  #!/usr/bin/python
    2  # -*- coding: UTF-8 -*-
    3
    4  import cgi, os, sys
    5  import cgitb
    6  import tempfile as tf
    7  import json
    8
    9  form = cgi.FieldStorage()
    10  dirTJ={'b':'T','f':'F'} #back->true; foreward->false
    11  nam = form.getvalue('AQSname')
    12  try:
    13    ist=int(nam)
    14  except:
    15    AQ=nam
    16  else:
    17    fn = open('/Users/Data/cwb/e-service/surf_trj/sta_list.json')
    18    d_nstnam = json.load(fn)
    19    AQ=d_nstnam[nam]
    20  os.system('echo '+AQ+'>&/tmp/trj.out')
    21  DIR = form.getvalue("dirFB")
    22  TF=dirTJ[DIR[0]]
    23  num = form.getvalue("number")
    24  dat = form.getvalue("date")
    25  message='../../trj_results/'+DIR+AQ+dat+num+'.csv'
    26  print """\
    27  Content-Type: text/html\n\n
    28    <html>
    29    <head>
    30      <title>TRAJ KML result</title>
    31      <meta name="viewport" content="width=device-width, initial-scale=1">
    32          <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    33          <script>
    34          $(function() {
    35                  $('a[data-auto-download]').each(function(){
    36                          var $this = $(this);
    37                          setTimeout(function() {
    38                          window.location = $this.attr('href');
    39                          }, 2000);
    40                  });
    41          });
    42          </script>
    43    </head>
    44  """
    45  if os.path.isfile('/Library/WebServer/Documents/'+message[6:]):
    46    print """\
    47    <body>
    48    <p>The assigned KML file has been created and maybe downloaded in your Downloads directory.</p>
    49    <p>You may re-download by clicking this <a href="%s">link</a>, or...</p>
    50    <p> submit the KML file at Google Maps or OpenStreet interface at the
    51    <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
    52    <p> return to the previous page and redefine the trajectory.</p>
    53    </body>
    54    </html>
    55    """  % (message+'.kml')
    56  else:
    57    os.system('cd /Library/WebServer/Documents; \
    58    /Users/Data/cwb/e-service/surf_trj/traj2kml.py -t '+AQ+' -d '+dat+num+' -b '+TF+ '>>/tmp/trj.out')
    59    print """\
    60    <body>
    61    <p>The KML download should start shortly. If it doesn't, click
    62    <a data-auto-download href="%s">here</a>.</p>
    63    <p>The KML may be posted on google map or OpenStreet interface:
    64    <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
    65    </body>
    66    </html>
    67    """  % (message+'.kml')
```

index.js

    此js檔為調用D3js(Leaflet提供)的橋梁，主要使用者設定都在此一檔案內，包括了：
        起始值中心點的位置(line 11)
        起始地圖的縮放比例(line 12)
        貼圖的顏色、透明度等(line 15~17)
        起始站的標籤與文字內容(line 37~45)，由layer第1個物件中提取。

```java
$ cat -n index.js 
    1  (function (window) { 
    2      'use strict'; 
    3      var L = window.L; 
    4 
    5      function initMap() { 
    6          var control; 
    7          var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
    8              attribution: 'Map data &copy; 2013 OpenStreetMap contributors' 
    9          }); 
    10          var map = L.map('map', { 
    11              center: [23.6, 120.9,], 
    12              zoom: 7 
    13          }).addLayer(osm); 
    14          var style = { 
    15            color: 'blue', 
    16              opacity: 0.5, 
    17              fillOpacity: 0.3, 
    18              weight: 1, 
    19              clickable: false 
    20          }; 
    21          L.Control.FileLayerLoad.LABEL = '<img class="icon" src="https://upload.wikimedia.org/wikipedia/commons/f/fe/Gnome-folder.svg" alt="file icon"/>'; 
    22          control = L.Control.fileLayerLoad({ 
    23              fitBounds: true, 
    24              layerOptions: { 
    25                  style: style, 
    26                  pointToLayer: function (data, latlng) { 
    27                      return L.circleMarker( 
    28                          latlng, 
    29                          { style: style } 
    30                      ); 
    31                  } 
    32              } 
    33          }); 
    34          control.addTo(map); 
    35          control.loader.on('data:loaded', function (e) { 
    36              var layer = e.layer; 
    37                          var kk=Object.keys(layer._layers); 
    38                          var i=kk[0]; 
    39                          var lat0=layer._layers[i]["_latlng"]["lat"]; 
    40                          var lon0=layer._layers[i]["_latlng"]["lng"]; 
    41                          var ymd=layer._layers[i]["feature"]["properties"]["description"]; 
    42              console.log(layer._layers[i]["feature"],layer._layers[i]["_latlng"]); 
    43                  L.marker([lat0, lon0]).addTo(map) 
    44      .bindPopup(ymd) 
    45      .openPopup(); 
    46          }); 
    47      } 
    48 
    49      window.addEventListener('load', function () { 
    50          initMap(); 
    51      }); 
    52  }(window));
```

[^9]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。敬請逕洽作者：sinotec2@gmail.com.
