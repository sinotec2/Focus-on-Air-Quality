---
layout: default
title:  save_wrose
parent: CGI-pythons
grand_parent: Utilities
date: 2023-01-26
last_modified_date: 2023-01-28 15:01:18
tags: CGI-python graphics wrose PlumeModels
---
# 繪製煙流模式氣象檔案之風花圖
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

- 雖然風花圖的程式已經有很多軟體套件，但是為了檢查煙流模式目的而寫的界面，目前應該是沒有。
- 此處為wrose.py的CaaS版本，獨立程式詳見[風花圖之繪製_wdrose.py](../../PlumeModels/ME_pathways/wrose.md)
- 為了通用在不同的模式之間、也為了打開格式限制，這裡所引用的外部程式[wrose.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/matplotlib/wrose.py)，加進了輸入檔案格式的辨識，可以接受：
  1. ISCST氣象檔案格式
  2. AERMOD地面、或高空氣象檔案格式([mmif](../../PlumeModels/ME_pathways/mmif.md)結果)
  3. csv自由格式檔案
- 同時也在網頁上貼上範例，讓使用者可以檢視檔案內容，經由比較來了解模式。

### 界面

網頁計算服務網址：[http://125.229.149.182/wrose.html][1][^1]

![wrose_caas.png](https://drive.google.com/uc?id=1x2KtpcwwV8zzomMuRiiKMecMLy4_4TYt)

## wrose.html

- 與前述MMIF雷同，但多出範例表格之說明、減省email的詢問。
- 執行cgi-python save_wrose.py,引數則是檔名`name=filename`,filepicker之結果

```html

<div class="container">
  <div class="row">
    <div class="col-md-4">
      <form enctype="multipart/form-data" action="/cgi-bin/save_wrose.py" method="post">
        <p><input data-label="File:" class="filepicker-jquery-ui" type="file" 
		   placeholder="Select a file..." multiple="multiple"
		   name="filename"/> </p> 
		   <p style="text-align:center;"> <input type="submit" value="Upload and Run wrose remotely" /></p>
		  </form><p>	 </p><p>	 </p>
		<p>Contact: Dr. Yungchuan Kuang, sinotec2@gmail.com or <a href="https://www.evernote.com/shard/s125/sh/12eaea92-0fcc-4f54-9782-cb16f5a91be8/4653be8827311800fd1e237da43af3df">Dr. Kuang's Evernotes</a></p> 
    </div>
  </div>
</div>
```

## save_wrose.py

### 讀取檔案

```python
import cgi, os, sys
import cgitb; cgitb.enable()


form = cgi.FieldStorage()

pth='/tmp/wrose/'
fileitem = form['filename']
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
```

### 執行外部風花圖製作程式

- 與前述[terrain.py](aermap_caas.md)雷同（data-auto-download），
- 啟動外部程式[wrose.py](../../PlumeModels/ME_pathways/wrose.md)。
- 因應cgi的套件是python 2 的平台，wrose.py也必須改成python 2

```python
wrose='/opt/local/bin/wrose.py'  
cmd='cd '+pth+';export PATH=/opt/anaconda3/bin/:$PATH;'+wrose+' '+pth+fn+' >>/tmp/wrose/wrose.out'
os.system('echo "'+cmd+'">>/tmp/wrose/wrose.out') 
os.system(cmd)
```

### 備份結果

```python

cmd='cp '+pth+fn+'.png /Library/WebServer/Documents/wrose_png;'
cmd+='cp '+pth+fn+'.png /Library/WebServer/Documents/wrose_png/example.png'
os.system('echo "'+cmd+'">>/tmp/wrose/wrose.out') 
os.system(cmd)
```

### 程式下載

{% include download.html content="風花圖製作之CGI版本[save_wrose.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/save_wrose.py)" %}

{% include download.html content="風花圖製作之CGI版本[save_wrose.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/save_wrose.py)" %}


[^1]: 繪製煙流模式氣象檔案之風花圖。上傳準備好的氣象檔案，遠端執行wrose程式結束後，系統會自動下載結果給您(恕僅保留24小時)。[http://125.229.149.182/wrose.html][1][^2]
[^2]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。使用者敬請見諒，逕洽作者：sinotec2@gmail.com.

[1]: http://125.229.149.182/wrose.html "繪製煙流模式氣象檔案之風花圖。上傳準備好的氣象檔案，遠端執行wrose程式結束後，系統會自動下載結果給您(恕僅保留24小時)。"