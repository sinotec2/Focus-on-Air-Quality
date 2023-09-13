---
layout: default
title:附近行政區之定位
parent: cnty/town processing
grand_parent: Area Sources
nav_order: 1
date: 2019-10-10
last_modified_date: 2023-09-11 08:41:09
tags: TEDS
---

# 附近行政區之定位
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

- 這支[程式](adj_dict_Rect.py)的目的是找出每個鄉鎮區旁邊的其他鄉鎮區名稱，建立對照的關係，以便後續的應用。

## 矩形範圍之判別

- 因早期並不孰悉shapely模組的使用，因此採用較原始的boolean判斷方式。相同功能應存在有更好的做法。

### IO's  

- 輸入：前述`dict_xy.csv`
- 輸出：`adj_dict.json`

### 程式說明

- 應用模組與數據輸入

```python
#kuang@master /nas1/TEDS/teds10_camx/HourlyWeighted/area/adj_dict.py
import json
from pandas import *

fname='dict_xy.csv'
df=read_csv(fname)
ddict=set(df['name'])
```

- 每個鄉鎮區逐一迴圈執行判別
  - 先找出鄉鎮區範圍網格座標的極值，並向外擴展1公里、以涵蓋鄰近鄉鎮區。
  - 先框出矩形內部點(含邊界)之資料表

```python
adj_dict={}
for c in set(ddict):
    adj_c=set()
    a=df[df['name']==c].reset_index()
    xm=max(list(a['x']))+1000
    ym=max(list(a['y']))+1000
    xn=min(list(a['x']))-1000
    yn=min(list(a['x']))-1000
    boo=(df['x']<=xm) & (df['y']<=ym) & (df['x']>=xn) & (df['y']>=yn)
    b=df[boo]
```

- 鄉鎮區範圍內部點逐一檢查
  - 點的鄰近9宮格範圍是否有其他名稱之鄉鎮區
  - 如有，則儲存起來、更新對照關係。

```python
    for i in xrange(len(a)):
        x=a.loc[i,'x']
        y=a.loc[i,'y']
        for ix in [x-1000,x,x+1000]:
            for iy in [y-1000,y,y+1000]:
                boo=(b['x']==ix) & (b['y']==iy)
                if len(b[boo])==0:continue
                c_add=list(b[boo]['name'])[0]
                if c_add==c:continue
                adj_c.add(c_add)
    adj_c=list(adj_c)
    adj_dict.update({c:adj_c})
```

- 對新的分區進行局部微調、輸出結果備用

```python
adj_dict.update({'xinzhushineiqu':['xinzhushibeiqu','xinzhushidongqu','xinzhushixiqu']})
adj_dict.update({'tainanshizhongqu':['tainanshidongqu','tainanshinanqu','tainanshixiqu','tainanshibeiqu']})
adj_dict.update({'jiayishizhongqu':['jiayishidongqu','jiayishixiqu']})
adj_dict.update({'xinzhuxianxiangshanqu':['xinzhushibeiqu','xinzhushidongqu','xinzhuxianbaoshanxiang','sea','miaolixianzhunanzhen','miaolixiantoufenzhen']})
fname='adj_dict.json'
fn=open(fname,'w')
json.dump(adj_dict,fn)
```

### 程式下載

{% include download.html content="[adj_dict_Rect.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/adj_dict_Rect.py)" %}

## shapely版本adj_dict.py

### touches版本

- 這個版本使用shapely的模組功能polygon.touches來判斷2個行政區多邊形是否相鄰。
- 可能的問題
  - 行政區邊界如果是在河川的中央、港區海域等等，有可能無法緊鄰相接，會有落差
- 程式下載

{% include download.html content="[adj_dict_Touch.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/adj_dict_Touch.py)" %}

- touches的用法如下

```python
...
adj_dict={}
for i in range(len(df)):
  touched=[]
  for j in range(len(df)):
    if df.polygon[i].touches(df.polygon[j]):touched.append(df.twnid[j])
  if len(touched)==0:touched=[0]
  s=''
  for t in touched:
   s+=str(t)+';'
  adj_dict.update({str(df.twnid[i]):s})
...  
```

### intersects與buffer(最後版本)

- 這個版本用了2個shapely的模組，分別是intersects與buffer
- 使用buffer
  - 將多邊形向外擴張一些，以便確定會有交集，且向
  - 外擴張代表範圍。如下例，拓展0.15度約15公里。效果如圖所示。

```python
df['polygon']=[Polygon(i).buffer(0.15) for i in df.lonlats] #0.1deg~10Km
```

|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-09-12-14-31-58.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-09-12-14-39-32.png)|
|:-:|:-:|
|<br>buffer=0.1 deg</br>|<br>buffer=0.15 deg</br>|

- 使用intersects與前述touches一樣用法。

```python
...
  for j in range(len(df)):
    if df.polygon[i].intersects(df.polygon[j]):touched.append(df.twnid[j])
...
```

{% include download.html content="[adj_dict_IntersectBuff.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/dictProc/adj_dict_IntersectBuff.py)" %}
