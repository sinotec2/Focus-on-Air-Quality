---
layout: default
title: iscParser
parent: SO Pathways
grand_parent: Plume Models
nav_order: 5
last_modified_date: 2022-03-08 17:46:18
---
# 污染源空間解讀器
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
### 既有作法與更新構想
- 一般煙流模式(ISCST/aermod等)使用直角座標系統，台灣地區以twd97為主，需要先行整理一底圖(bmp+座標定位或DWG/geoTIFF/SHP檔)、特別進入surfer軟體，貼上背景圖、才能確認其座標系統。在嘗試錯誤作業過程中並不方便。
- 此作業乃針對污染源設定文字(檔案)進行解析，並轉換成經緯度之KML檔案，進行google map或[open streat map][3]貼圖，可做為階段性之成果。
### 本項作業之需求：
- 解析煙流模式污染源空間設定、也包括建築物位置的設定
- 更動污染源設定時，有最快的反應速度。如：
  - 切割面源、
  - 將面源改換成體源(或相反)
- 模式設定需確認事項：
  - 污染源位置(相對於既有地圖)、(離散)接受點位置是否正確
  - 面源之旋轉角度是否正確
  - 面源(長、寬)、體源(長)的尺寸是否正確
  - 面源、體源是否重疊(有高估濃度可能)、或太分散無法覆蓋區域範圍(低估之嫌)
  - [建築物頂點位置][2]的確認

[3]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#地圖貼板> "詳見【地圖貼板】、與 【Leaflet Filelayer on iMacKuang】(http://114.32.164.198/Leaflet/docs/index.html)】的連結"

[2]: <https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/> "有關建築物效應的前處理方式，可以參考【建築物煙流下洗現象之模擬設定】及【BPIPPRM之遠端計算服務】"
### 作業進路方法之考慮
- 過去SURFER作法
  - 如上所述，雖然有最高的解析度、有最佳的底圖、還能加入中文說明文字、貼上相關計畫線條等等好處，
  - 但是缺點就是：作業流程冗長、反應不及、超出底圖範圍時無法因應、底圖不能平移、底圖無法縮放、解析度無法增減
- isc/aermode breeze(view)套裝軟體
  - 能夠接受廠區周界線，並將接受點去除。
  - 能提供適當解析度之接受點網格。提供衛星照片為底圖。
  - 無文字說明。
  - 新版的[aermode breeze](https://www.youtube.com/watch?v=v9iNIzWruqA)有自動定位(georeferencing)的功能，
    - 然而是經緯度座標系統、也是不能無限制panning/zooming
    - 無法接受twd97系統座標，與工程圖有落差。
    - 工作底圖仍以google map有資訊體軟版權限制。
    - 不能每一台機器使用
- 顧問機構[Air Sciences Inc](https://airsci.com/about/)提供的免費計算服務-排放源之立體空間解析([AEREarth Processor][ASI])
  - 提供KMZ檔、供Google Earth貼圖
  - 沒有UTM 51N之解析、無法符合TWD97座標系統
- kml檔案之編撰
  - 已有[csv2kml.py][0]、[dat2kml.py][1]為基礎，稍加整理運用即可、
  - 無版權問題、kml檔案已有許多顯示軟體、界面、插件
  - 輕量作業，不損失資源
  - 可與前述作業平行不影響原來作業方式

[ASI]: <https://aerearth.airsci.com/> "Upload input files to receive 3D renderings of your model setup to view in Google Earth"
[0]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/> "詳見【點狀資訊KML檔之撰寫(csv2kml.py)】"
[1]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/#dat2kml> "詳見【等值圖KML檔之撰寫】、【dat2kml遠端計算服務】"

## 服務網頁
- CaaS位置：[ISC/AERMOD 座標點位之KML轉檔系統](http://114.32.164.198/iscParser.html)
- 畫面

| ![iscParser.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/iscParser.png)|
|:--:|
| <b>[http://114.32.164.198/iscParser.html](http://114.32.164.198/iscParser.html)畫面</b>|


### 輸入範例
- form內包括2項傳遞訊息：
  - iscinp(優先執行)：LOCATION及SRCPARAM等設定文字。同一污染源必須配對，如

```bash    
SO LOCATION Cg01 AREA 296192.7 2764060.0 13.4
SO SRCPARAM Cg01 3.46E-04 2.0 12 166.7 63
RE DISCCART 296123 2764056 15.3 1.5
RE DISCCART 294911 2762966
```

  - filename：含有上述文字之文字檔。如為多污染源系統，必須嚴格按照污染源順序給定。如範例groupA.txt
  - 不論文字內容、或文字檔，每行之間有enter(\n或\r)、空行、*為首的說明行，都無所謂，程式會予以剔除。

### HTML
- $web/[iscParser.html](https://github.com/sinotec2/CGI_Pythons/tree/main/drawings/isc_parser)
  - 使用[filepicker](https://github.com/sinotec2/CGI_Pythons/tree/main/utils/filepicker)開啟使用者指定上傳的檔案
  - 以POST方式呼叫$cgi/isc/[isc_parser.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parser.py)，傳送變數：iscinp（或）filename


```html
<form id="upload" name="upload" method="POST" enctype="multipart/form-data" action="/cgi-bin/isc/isc_parser.py">
        <input type="text" id='iscinp' name="iscinp" /><br />
          <p><input data-label="File:" class="filepicker-jquery-ui" type="file"
                  placeholder="Select a file..." multiple="multiple"
                  name="filename"/> </p>
                  <p style="text-align:center;"> <input type="submit" value="Upload and Run parser remotely" /></p>
                </form><p>      </p><p>        </p>
```
### submit及預期結果
- 啟動cgi-bin/isc/[isc_parser.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parser.py)(詳下述)
- 輸入範例文字內容：將會產生Cg01.csv.kml(1個面源多邊形kml)、Cg01R.csv.kml(接受點位置kml)
- 輸入範例檔案：將會產生As010.csv.kml(多個多邊形kml)
- [isc_parser.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parser.py)程式會按照輸入內容分別呼叫
  - [isc_parserBP.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parserBP.py)解析建築物前處理的輸入檔內容
  - [sc_parserSO.py]解析ISCST/AERMODrunstream檔案中有關排放源位置的內容

```python
if LBPIP: 
  os.system(CGI+'isc_parserBP.py '+'"'+STR+'"')
else:
  os.system(CGI+'isc_parserSO.py '+'"'+STR+'"')
```

## [isc_parserSO.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parserSO.py)程式
程式將會解讀下列特性之污染源，並將其空間資訊輸出到KML檔案

### 面源
- 因為ISC/AERMOD的面源可以旋轉方向，因此程式的主要功能在求取旋轉後的矩形頂點座標。(函數rotate_about_a_point line 11~15)
- 原來座標P(line 42)、角度angl(line 43)，代入函數得到旋轉後的座標(line 44~45)
- 應用[csv2kml.py](https://raw.githubusercontent.com/sinotec2/python_eg/master/csv2kml.py)將頂點座標輸出為多邊形kml(csv2kml.py有相應進版，詳下)

### 體源
- 與前述面源類似，只是體源沒有寬度，只有長度及高度，因此假設為一四方形(長=寬)
- 體源也沒有角度，假設y軸為指北方向
### 點源
- 只有輸出位置
- 呼叫[csv2kml.py](https://raw.githubusercontent.com/sinotec2/python_eg/master/csv2kml.py)，將位置輸出成kml檔案

```python
os.system('/usr/kbin/csv2kml.py -n P -g TWD97 -f '+fname+'>> /tmp/isc.out')
```

### 結果之輸出
- 最後在cgi html當中調用data-auto-download，將結果下載到客戶硬碟。


### CGI_python引用的檔頭
- header.txt

```html
kuang@114-32-164-198 /Library/WebServer/CGI-Executables
$ cat header.txt
  <html>
  <head>
    <title>ISC_setting KML results</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
        $(function() {
                $('a[data-auto-download]').each(function(){
                        var $this = $(this);
                        setTimeout(function() {
                        window.location = $this.attr('href');
                        }, 10000);
                });
        });
    </script>
  </head>
  <body>
```

### csv2kml.py修正
- [csv2kml.py][0]程式位置：`CSV2KML='/opt/local/bin/csv2kml.py -g TWD97 -f '`
- 新增多個Polygons的作法：每個p0就重新寫kml的head
- csv內容（範例）

```bash
kuang@114-32-164-198 /Library/WebServer/Documents/isc_results
$ more Cg01.csv
X,Y,lab,nam
296192.7,2764060.0,Cg01_p0,Cg01_p0
296198.147886,2764049.30792171,Cg01_p1,Cg01_p1
296346.678674,2764124.9881380163,Cg01_p2,Cg01_p2
296341.230788,2764135.6802163064,Cg01_p3,Cg01_p3
296192.7,2764060.0,Cg01_p4,Cg01_p4
```

- kml撰寫

```python
$ cat -n $(which csv2kml.py)
...
   115    else: #Polygon case
   116      headP = '</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>'
   117      tailP = '</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
   118      ps=[i[-2:] for i in list(df[col[3]])]
   119      npoly,i0,i1=1,[0],[len(df)]
   120      if 'p0' in ps:
   121        npoly=ps.count('p0')
   122        if npoly>1:
   123          i1=[]
   124          for i in range(npoly-1):
   125            i0.append(i0[-1]+1+ps[i0[-1]+1:].index('p0'))
   126            i1.append(i0[-1])
   127          i1.append(len(df))
   128      for ip in range(npoly):
   129        level=int(np.random.rand()*10)
   130        line.append('<Placemark><name>level:' + str(level) + '</name><styleUrl>#level' + str(level) + headP)
   131        print (i0[ip],i1[ip])
   132        for i in range(i0[ip],i1[ip]):
   133          line.append(lonlat[i])
   134        line.append(tailP)
   135    line.append('</Document></kml>')
   136    with open(fname+'.kml','w') as f:
   137      [f.write(l+'\n') for l in line]
```   

## [isc_parserBP.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/isc_parserBP.py)
- 輸入[BPIP]()的輸入檔，程式將會解析建築物相關的座標位置
- 基本上本程式是[rotate_KML](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML/)的反寫。
  - [rotate_KML](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML/)是讀入一個kml檔案、解讀檔案、旋轉角度、將建築物頂點座標寫成bpip的輸入檔（fort.10）
  - [isc_parserBP.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/isc_parserBP.py)做的是正好相反，讀入一個fort.10檔案（與標題文字中的原點位置），將前旋轉、寫成kml檔案。
  - KML檔案的輸入、輸出，可以參考[python解析KML檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/)、[點狀資訊KML檔之撰寫(csv2kml.py)](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/)

### 建築物之設定
- 由於建築物設定為直角座標之工廠地圖系統，與背景地圖之間需要有夾角及原點座標值。
- **夾角D**在fort.10檔案中已經登錄，因此設計[rotate_KML](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML/)在產生fort.10時，順便將KML檔中的第1個點設為原點，並將其座標寫在[檔頭](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，以利[iscParser]()讀取應用。
- 因前述污染源對象已經太過複雜了，因此另將解析寫在程式[isc_parserBP.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/isc_parserBP.py)中。


## 結果
### 檢視
- 使用[Leaflet FileLayer](http://114.32.164.198/Leaflet/docs/index.html)

### 圖檔
- [isc_parserSO.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parserSO.py)結果

| ![iscParser1.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/iscparser1.png)|
|:--:|
| <b>面源及體源空間位置之解析結果</b>|
| ![iscParser2.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/iscparser2.png)|
| <b>敏感接受點及污染源相對位置</b>|

- [isc_parserBP.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/isc_parserBP.py)結果

| <b>圖1實例廠區數位化結果，雖然數位板點選結果有些歪斜，[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式會將其均化修正</b>|
| ![BPIP4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP4.png)|
|:--:|
| <b>實例廠區[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)旋轉後之[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，經[ISCPARSER](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)解讀結果</b>|

## Reference

- Google Developer Groups, [KML Tutorial ](https://developers.google.com/kml/documentation/kml_tut),Last updated 2021-09-07 UTC.