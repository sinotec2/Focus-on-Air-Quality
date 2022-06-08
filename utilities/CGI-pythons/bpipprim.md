---
layout: default
title: bpipprim.py
parent: CGI-pythons
grand_parent: Utilities
last_modified_date: 2022-06-08 14:05:20
---
# bpipprim
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
- bpip的CGI作業相對單純很多。
  - 複雜的是讀圖與量測前處理過程，詳[bpip設定與執行步驟實例示範](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定與執行步驟實例示範)。
  - 監看程式
    - 如有錯誤，會直接寫在fort.12、fort.14，build.txt內容也會是空白
    - 如無錯誤，程式計算很快，不需要(無從)監看。
- CaaS整體的架構、檔案與結果範圍詳見[BPIPPRM之遠端計算服務範例](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP_remote/)。
- 此處著重說明[bpipprim.py](https://github.com/sinotec2/CGI_Pythons/blob/main/bpipprim/bpipprim.py)(CGI-PY)的程式設計細節。
- 程式更新需求：因USEPA不再發展BPIP，轉到[PRIME2][Petersen and Guerra 2018]之應用，因此預期將不會需要更新。

## 輸入
- 程式可以接受貼上字串與檔案上傳2種輸入方式，以方便測試階段，減少上下載、重新命名與檔案管理的麻煩。
  - 如果是給定檔名，在BPIP.INP空格處要留空白(重新整理網頁)，讓`STR`的長度為0。
  - BPIP程式並不會讀取檔案名稱，寫出結果檔名也是固定名稱，因此使用者需要自行管理檔案(或目錄)。

```python
form = cgi.FieldStorage()
STR = str(form.getvalue("iscinp"))
os.system('echo "'+STR+'"'+OUT)
if len(STR)<=4: #in case of input a SO/RE file
  fileitem = form['filename']
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
else:	
    fn='fort.10'
    with open(pth+fn,'w') as ftext:
      ftext.write(STR)
```

## 輸出
### grep的問題
- 除了BPIPPRIM正常輸出的檔案之外，此處又以grep取出路徑為**SO**的所有內容，另存新檔，所以grep如為alias有內設顏色，將會出錯，必須取消顏色設定。

```python
...
GREP='/usr/bin/grep --color=never'
...
cmd ='cd '+pth+';'
cmd+= BPIP+NULL+';'
cmd+= GREP+" ' SO ' fort.12 >build.txt"
os.system(cmd)
```

### 執行結果檔案連結(範例)
  - 每次執行的檔名皆相同，使用者自行下載管理。

```
filename given and save as: fort.10

BPIPPRIN_results: The download process should start shortly. If it doesn't, click:

build.txt fort.12 fort.14
```

[Petersen and Guerra 2018]: <https://www.sciencedirect.com/science/article/abs/pii/S0167610517306669> "Petersen, R. L. and Guerra, S. A., (2018). PRIME2: Development and evaluation of improved building downwash algorithms for rectangular and streamlined structures. Atmospheric Environment, 173, 67-78."