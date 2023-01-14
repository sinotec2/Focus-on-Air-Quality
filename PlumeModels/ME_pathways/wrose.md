---
layout: default
title: 風花圖之繪製_wdrose.py
parent: ME Pathways
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2022-03-21 16:43:46
tags: plume_model graphics
---
# 風花圖之繪製_wdrose.py
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
### 目標：
- 熟悉python的語法，從範例中找到如何應用的連結方式。
- 建立ISCST氣象檔的風花圖繪圖程式，以做為檢核之用。
### 資源：
- 程式位置 /Users/cybee/bin/wrose.py
  執行方式(範例)：
	- ISC 氣象檔：wrose.py FNAME 
	- aermod 氣象檔：wrose_mm.py FNAME 
	- csv自由格式檔案：wrose_csv.py FNAME
- 風花圖套件([pypi](https://pypi.python.org/pypi/windrose)
- [有關pandas的快速入門](https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html)
- 有關python的入門課程
  - [工具介面ipython簡介](https://blog.csdn.net/qq_27825451/article/details/84320859)
  - [tutorial by catapillar](https://openhome.cc/Gossip/CodeData/PythonTutorial/)
  - [python課綱總集](http://www.evernote.com/l/AH30OmUntodEqYJyeIF1AreK8Z508_MHWCI/)

## 範例程式

```python
from windrose import WindroseAxes 
import numpy as np 
# Create wind speed and direction variables 
ws = np.random.random(500) * 6 
wd = np.random.random(500) * 360 
ax = WindroseAxes.from_ax() 
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white') 
ax.set_legend()
ax.figure.savefig(fname+'.png')
```

1~4行程式碼說明如下：
- import輸入需要的模組(程式庫)。什麼程式需要什麼模組，需由範例得知。模組程式庫如何呼叫，在ipython內以dir(...)詢問。
- ws, wd為隨機產生、長度為500的陣列，6、360為其最大值
5~8為繪圖程式之應用
- ax.bar產生wd及ws之際座標條狀圖
- ax.set_legend產生風速的表示圖例
- figure.savefig儲存檔案


### 應用(修改)策略
- ws wd須另行產生，套用真實的數據

## ISCST氣象檔之讀取
- 氣象檔為具有格式的文字檔，不能用簡單的split來切割欄位，必須按照欄位數精確定位。
- 可以用mobaXterm的內設編輯軟體(MobaTextEditor)打開如下圖，
  第1行為站名、年代名，第2行以後則為逐時數據，
  黃色螢光筆部分為風去的方向(度)，與風向差異180度。藍色底線部份則為風速，單位為公尺每秒。



- 將游標移到風向及風速的前面，由MobaTextEditor下方的位置數字可以得知(如下圖)，分別自第9及第18欄位置開始，各為9格的長度。


- 程式寫法如下:
  - 使用with來開啟檔案的好處是，不必再做關閉的動作。
  - python內設輸入及輸出都是字串，這樣才沒有精度有損失的問題。
  - 每行的內容進行切割，再存成一個序列(list)

```python
from pandas import  *
import  sys
fname=sys.argv[1]               #python是從第0開始計算註標，第0個引數是程式本身的名稱，第1個則令為氣象檔的檔名。
with open(fname,'r') as f:
    l=[i for i in f]
l=l[1:]                         #去掉第1行，從第2行開始到最後
wd=[float(i[8:18]) for i in l]     #切割出風向。注意python是從第0開始計算註標，最後1個註標不計入。
ws=[float(i[18:28]) for i in l]     #切割出風速。並且從字串轉成實數
aermod氣象檔之讀取
wd=[float(i.split()[16]) for i in l]
ws=[float(i.split()[15]) for i in l]
```
### 任意自由格式csv檔之氣象檔
1. 刪除型態為字元的欄位
2. 如果最大值超過360度，不論是什麼，也不會是風速風向數據，刪除
3. 剩下欄位來做級值的排序，最大者為風向，其次則為風速

```python
    20  if ',' in l[0]: 
    21    df=read_csv(fname) 
    22    col=df.columns 
    23    for c in col: 
    24      if type(df.loc[0,c])==str: 
    25        del df[c] 
    26      else: 
    27        if max(list(df[c]))>360.: 
    28          del df[c] 
    29    smx=mxv=[max(list(df[c])) for c in df.columns] 
    30    smx.sort() 
    31    iwd,iws=(mxv.index(smx[i]) for i in [-1,-2]) 
    32    wd,ws=(list(df[df.columns[i]]) for i in [iwd,iws])
```


## 計算結果
(46744.ASC， 台南站2017年數據)


(46777.ASC， 梧棲站2017年數據)


749 台中    



### 討論：
- 全年最多風向為北風～東北風，是東北季風的特色，風速較大。
- 台南的風向較為複雜，梧棲較為單純，因前者風速較低，近市區風系複雜。
- 西南季風的特性，台南有西南與東南風，梧棲則為東南風，可能受到陸風的干擾。
### TODO:
- 部分方向的頻率超低，如何確認？
- 分時、分季的特性如何？
### BUGs
- 由於windrose模組內的指令大多會呼叫系統的視窗程式，如jupyter在browser上產生畫面，如果ssh登入與主機登入的使用者不同，系統不知如何出現畫面，因而提出警訊。
- 本案採savefig因此即使沒有畫面顯示，依然可以執行。

```bash
$ wrose.py b.asc
_RegisterApplication(), FAILED TO establish the default connection to the WindowServer, _CGSDefaultConnection() is NULL.
```


