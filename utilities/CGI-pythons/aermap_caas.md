---
layout: default
title:  煙流模式地形前處理
parent: CGI-pythons
grand_parent: Utilities
last_modified_date: 2022-06-07 20:21:17
tags: CGI_Pythons plume_model sed gdal AERMAP
---
# 煙流模式地形前處理-AERMAP之遠端執行
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

### 遠端執行

- **遠端執行**顧名思義就是不是在使用者(客戶端)的電腦執行，而是透過網路、在遠端工作站執行作業，給予簡單的設定及要求，啟動遠端程式，執行完畢再將結果檔案下載至使用者電腦。
- 遠端執行的好處及必要性
  - 同時具有SaaS(Software as a Service)的好處，避免程式的散佈版權
  - 避免使用者更動設定造成程式執行的錯誤、或不一致
  - 減省使用者電腦資源的耗費
  - 適合公眾領域程式之推廣應用
- 此處**遠端執行**有別於一般小規模計算
  - 使用客戶端瀏覽器執行的java程式、顯示軟體
  - 轉檔服務、翻譯、
- 更多討論詳見[網頁計算服務軟體系統的建置](CaaS_review.md)，此處專注AERMAP之部分。

### 地形前處理自動執行遭遇的問題

- 完整之地形前處理，詳見[AERMAP](../../PlumeModels/TG_pathways/gen_inp.md)。
  - 此處因在伺服器執行，因此仍然維持[eio](https://pypi.org/project/elevation/)下載數據、
  - 此外，[gdal_translate](https://gdal.org/programs/gdal_translate.html)改變格式，準備好aermap.inp執行aermap等程序，與[AERMAP](../../PlumeModels/TG_pathways/gen_inp.md)一樣。
- html及cgi_python的設定，詳見[網頁計算服務軟體系統的建置](CaaS_review.md)。此處說明因應caas所做的重要更動。

### 主要的問題

1. 發生在網頁使用者的身份，與平常一般用ssh登入的使用者，二者在環境的設定上有著很大的差異，
   - 造成可以登入執行流程，卻不能由cgi_python操縱流程。
   - 理論上cgi_python是由root之分身www(Mac是_www)，其權限能力是很高的，但是實際執行時環境變數仍然不能自動設定，執行外部其他程式時會發生錯誤。
2. cgi_python的standard output or error (stdout, stderr)
   - cgi_python所有產生的standard output，都會是html的內容，因此，
   - 如果呼叫os中的其他程式如果有輸出，也將會干擾正常的html功能，發生AH02429誤錯(contains invalid characters)
   - 解決方案就是將所有stdout/err都導向檔案、或者是/dev/null，讓html保持乾淨。

- 由於本系統的外部批次檔內容較為複雜，此一經驗將可以作為未來發展的重要參考。

### 成果

- terrain.py建置結果與使用者界面、詳計算服務網址：[http://125.229.149.182/terrain.html][1][^1]

|![terr_html.png](https://drive.google.com/uc?id=1-dYmAoM5i5sXt3sf1FFVnnSNMli7f0Rt)|
|:-:|
| [煙流模式地形前處理][1]之網頁計算服務系統畫面 |

- 與[iscParser](isc_parser.md)雷同，但多出結果表格之說明

## 客戶身份的問題與解決

### 定義

- 客戶：經由網頁來讀取網頁、(由www或_www代為)執行工作站程式者
- 一般使用者：可以登入工作站的作業人員
- 管理者：root

### 方案一：以絕對路徑執行程式

- 適用在較單純的程式，相依性較低的批次檔
- 除了在shell之指令以外，所有的程式(包括在/usr/bin、/usr/local/bin等等)，客戶都是沒有辦法透過網頁來使用的。
  - 可以用which 指令來確認程式位置
  - terrain.py中之範例

```python
...
    32  geninp='/opt/local/bin/gen_inp.py' 
    33  aermap='/opt/local/bin/aermap'
...
    36  cmd+='/usr/bin/zip '+fname+' *out *OUT aermap.inp>&/dev/null;'
```

### 方案二：每次宣告路徑之環境變數($PATH)

- 每次跳到os都宣告環境變數真的很不方便，因此不是常態，只在程式是個批次檔，會呼叫同系列的其他程式，其絕對路徑無從指定。
- 或程式的相依性很高，除了其他程式外，還包括了其他必要數據檔之路徑
- 在gen_inp.py中的範例：
  - eio是個python檔，不是包裝好的執行檔
  - eio還會呼叫gdal_translate
  - 系列程式都需要搜尋地理座標系統定義檔，路徑由環境變數GDAL_DATA指定
  - gd_data同時定義PATH及GDAL_DATA等2個環境變數

```python
$ cat -n /opt/local/bin/gen_inp.py|grep '/'
...
   183  pth1='/opt/anaconda3/bin/' 
   184  pth2='/opt/anaconda3/envs/ncl_stable/bin/' 
   186  gd_data=';export PATH='+pth1+':'+pth2+':$PATH;GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
...
```

- 組合結果
  - 每次都要執行gd_data內容
  - 因為有PATH，因此執行程式不必再另加絕對路徑了。

```python
  185  eio='eio'
...
   187  cmd='cd '+dir+gd_data+eio+' --cache_dir '+tmp+' clip -o '+TIF+' --bounds '+smin+NUL 
   188  os.system('echo "'+cmd+'"'+NUL) 
   189  os.system(cmd) 
   190  os.system('echo "before gdal"'+NUL) 
   191  gd='gdal_translate' 
   192  cmd='cd '+dir+gd_data+gd+' -of USGSDEM -ot Float32 -projwin '+llNE+' '+TIF+' '+DEM+NUL 
   193  os.system('echo "'+cmd+'"'+NUL) 
   194  os.system(cmd)
```

### gdal暫存檔儲存與取用的議題

- 這個問題是增進gdal效率過程中所引起的，嚴格講不是問題，但也是因應客戶身份所必須的特殊處理方式。
- 一般使用者eio數據暫存位置內設是在/Users/NAME/Library/Caches/elevation，是在個人家目錄(/Users/NAME/)下的次目錄，
  - 因此如果好幾個人下載同一區數據時，系統將會儲存好幾份相同的數據，
  - 因個人目錄別人是無法分享的，形成資源的浪費。
- 管理者(www，_www亦同)eio暫存位置內設是在/var/root/Library/Caches/elevation，更是深不見底，一般使用者是絕對用不到。
- 折衷方案用eio的option cache_dir，將暫存目錄放在/tmp/gdal下，如此客戶、管理者、一般使用者就都可以用得到了。

```python
$ cat -n /opt/local/bin/gen_inp.py
...
13  tmp='/tmp/gdal
...
   187  cmd='cd '+dir+gd_data+eio+' --cache_dir '+tmp+' clip -o '+TIF+' --bounds '+smin+NUL 
   188  os.system('echo "'+cmd+'"'+NUL) 
   189  os.system(cmd)
```

## 標準輸出(stdout, stderr)干擾之解決

- cgi_python的輸出將轉成(暫存的)html來讓客戶瀏覽，因此執行過去若有stdout/stderr，將會造成html的錯誤。
- 最典型的錯誤訊息(AH02429)：

```bash
[Fri Jan 29 08:48:08.954271 2021] [http:error] [pid 83793] [client 114.45.83.32:46685] AH02429: Response header name '  adding' contains invalid characters, aborting request
```

- 網路上討論不多，只有提供`cgitb`記錄錯誤訊息的方式，間接解決這個問題。

```python
cgitb.enable(display=1, logdir='/tmp/isc', context=5, format="html")
```

- 事實上，解決方式很單純，就是將所有呼叫到的程式、執行檔、批次檔等，所有的輸出都必須導向檔案或/dev/null，保持cgi_python std out/err只有html部分訊息，此一問題就可迎刃而解。
- 容易被忽略的是zip，zip也會有stdout，也必須有所導引，範例中導引到/dev/null(line 45)

```python
$ cat -n terrain.py|grep \>
    20    os.system('echo "'+reg+' not in STR!">> '+out) 
    35  cmd+='sed s/test/'+snamo+'/g aermap.inp_template>aermap.inp;' 
    38  cmd+= geninp+' '+web+'trj_results/'+snamo+' '+inp+'>>geninp.out;' 
    42  cmd+= aermap+'>> '+out+';' 
    45  cmd+='/usr/bin/zip '+fname+' '+snamo+'.* *out *OUT aermap.inp>&/dev/null;'
```

- 呼叫gen_inp.py時，程式用NUL來簡化。eio、gdal_translate等程式都會有stdout輸出，也必須有所導引，範例為導引到geninp.out檔案。

```python
$ cat -n $(which gen_inp.py)|grep NUL
   181  TIF,DEM,NUL=fname+'.tiff',last+'.dem',' >>'+dir+'geninp.out' 
   182  os.system('echo "before eio"'+NUL) 
   187  cmd='cd '+dir+gd_data+eio+' --cache_dir '+tmp+' clip -o '+TIF+' --bounds '+smin+NUL 
   188  os.system('echo "'+cmd+'"'+NUL) 
   190  os.system('echo "before gdal"'+NUL) 
   192  cmd='cd '+dir+gd_data+gd+' -of USGSDEM -ot Float32 -projwin '+llNE+' '+TIF+' '+DEM+NUL 
   193  os.system('echo "'+cmd+'"'+NUL)
```

## 程式下載

### terrain.py

{% include download.html content="煙流模式地形前處理CGI主程式：[terrain.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrain.py)" %}

### terrainTXT.py

- 類似獨立執行之控制程式。

{% include download.html content="地形前處理文字解析與執行控制程式：[terrainTXT.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/TG_pathways/terrainTXT.py)" %}，程式說明詳[執行控制程式](../../PlumeModels/TG_pathways/terrainTXT.md)

### terrainXYINC.py

{% include download.html content="地形前處理座標計算副程式：[terrainXYINC.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrainXYINC.py)" %}

### terrainLOCAT.py

{% include download.html content="地形前處理位置解析副程式：[terrainLOCAT.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrainLOCAT.py)" %}

## Reference

[^1]: 煙流模式的地形處理，提供ISCST3/AERMOD等煙流模式所需地型數據之[前處理][1]。

[1]: http://125.229.149.182/terrain.html "煙流模式的地形處理 "