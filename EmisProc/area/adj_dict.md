---
layout: default
title:附近行政區之定位
parent: "Area Sources"
grand_parent: TEDS Python
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

### adj_dict.py

- 這支[程式](adj_dict.py)的目的是找出每個鄉鎮區旁邊的其他鄉鎮區名稱，建立對照的關係，以便後續的應用。
- 因早期並不孰悉shapely模組的使用，因此採用較原始的boolean判斷方式。相同功能應存在有更好的做法。
- 輸入：前述`dict_xy.csv`
- 輸出：`adj_dict.json`

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

### shapely版本adj_dict.py 

```python
kuang@master /home/QGIS/Data/TWN_town
$ cat adj_dict.py

from shapely.geometry import Polygon
from pandas import *
import numpy as np
import sys
import os
import json

fname='/home/QGIS/Data/TWN_town/polygons.csv'
df=read_csv(fname,encoding='big5')
df['lonlats']=[j.replace(',','').replace(')','').replace('(','').replace('[','').replace(']','').split() for j in df.lonlats]
df['lonlats']=[[float(i) for i in j] for j in df.lonlats]
df['lonlats']=[[(j[i],j[i+1]) for i in range(0,len(j),2)] for j in df.lonlats]
df['polygon']=[Polygon(i) for i in df.lonlats]
adj_dict={}
for i in range(len(df)):
  touched=[]
  for j in range(i+1,len(df)):
    if df.polygon[i].touches(df.polygon[j]):touched.append(df.twnid[j])
  if len(touched)==0:touched=[0]
  s=''
  for t in touched:
   s+=str(t)+';'
  adj_dict.update({str(df.twnid[i]):s})
fname='adj_dict.json'
fn=open(fname,'w')
json.dump(adj_dict,fn)
```

|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-09-12-14-31-58.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-09-12-14-39-32.png)|
|:-:|:-:|
|<br>buffer=0.1 deg</br>|<br>buffer=0.15 deg</br>|