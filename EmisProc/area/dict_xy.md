---
layout: default
title:行政區座標的整理
parent: "Area Sources"
grand_parent: TEDS Python
date: 2019-10-10
last_modified_date: 2023-09-11 08:41:09
tags: TEDS
---

# 行政區座標的整理
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

- 這一系列的工作在整理鄉鎮區所佔的網格座標。從當中得到鄉鎮區相鄰的關係、測站所在地以及其相鄰的鄉鎮區。
- 因為台灣地區行政區有合併、重局部重劃等等修改，所以這一系列的整理會循環進行(互為因果)，以保持資訊的正確性。

## 網格座標與行政區的對照

這2支程式[cnty_xy](cnty_xy.py)以及[dict_xy](dict_xy.py)是從TEDS面源檔案轉成csv(`'areagrid.csv'`)之後開始轉換的第一步。主要處理幾個問題：
  - 海上網格：海上可能會有排放量(船舶)，但是沒有行政區劃分。
  - 外島網格：外島座標適用不同分區的UTM值，因此需要平移，否則會發生錯誤。
  - 名稱：套用新的行政區名稱(`town3.csv`)
  - 結果：`cnty_xy.csv`、`dict_xy.csv`

### 縣市 cnty_xy.py

- 模組

```python
#kuang@master /nas1/TEDS/teds10_camx/HourlyWeighted/area
#$ cat cnty_xy.py
from pandas import *
import numpy as np
from pypinyin import pinyin, lazy_pinyin
```

- 輸入檔案、整理海面、外島問題
- 把座標XY值連在一起，方便去除重複值

```python
df = read_csv(fname)
df.loc[df['NSC_SUB'].map(lambda x: type(x)==float and np.isnan(x)==True),'NSC_SUB']='b'
df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
subX=['44','50','51']
df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']=[x-201500 for x in df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']]
df['YX']=[int(y)+int(x/1000) for x,y in zip(df['UTME'],df['UTMN'])]
```

- 將中文字形轉成英文拼音

```python
df_cnty=read_csv('cnty.csv')
for i in xrange(len(df_cnty)):
    cha=df_cnty.loc[i,'cnty']
    ll=lazy_pinyin(cha.decode('big5'))
    s=''
    for l in ll:
        s=s+l
    df_cnty.loc[i,'cnty']=s
df_cnty.loc[24,'no']=51
df_cnty.loc[24,'cnty']='lianjiangxian'
d_cnty={x:str(int(y)) for x,y in zip(df_cnty['cnty'],df_cnty['no'])}
d_cnty.update({'xinbeishi':'41','taoyuanshi':'32'})
d_cnty.update({'sea':'53'})
```

- 取集合以去除重複點

```python
df['YXCO']=[str(x)+str(y) for x,y in zip(df['YX'],df['CNTY'])]
s_xy=list(set(df['YXCO']))
co=[int(x[7:]) for x in s_xy]
yx=[int(x[:7]) for x in s_xy]
x=[i%1000*1000 for i in yx]
y=[int(i/1000)*1000 for i in yx]
df_xyc=DataFrame({'x':x,'xx':x,'y':y,'cnty':co})
```

- 存檔

```python
d2_cnty={x:y for x,y in zip(d_cnty.values(), d_cnty.keys())}
df_xyc['name']=[d2_cnty[str(i)] for i in df_xyc['cnty']]
df_xyc.set_index('cnty').to_csv('cnty_xy.csv')
```

### 鄉鎮區 dict_xy.py

- [這支程式](dict_xy.py)是較新編寫的程式，新的鄉鎮區名稱已經處理好了，可以直接套用(`town3.csv`)。
- 因二者程式非常相近，此處僅介紹其差異。

- 定義海面

```python
kuang@master /nas1/TEDS/teds10_camx/HourlyWeighted/area
$ diff cnty_xy.py dict_xy.py
6,8c6,7
< df.loc[df['NSC_SUB'].map(lambda x: type(x)==float and np.isnan(x)==True),'NSC_SUB']='b'
< df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
< df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
---
> df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300
> df['DICT']=[int(i) for i in list(df['DICT'])]
```

- 直接讀取處理好的鄉鎮區名稱，不再自行轉變成拼音

```python
14,26c13,15
< df_cnty=read_csv('cnty.csv')
< for i in xrange(len(df_cnty)):
<     cha=df_cnty.loc[i,'cnty']
<     ll=lazy_pinyin(cha.decode('big5'))
<     s=''
<     for l in ll:
<         s=s+l
<     df_cnty.loc[i,'cnty']=s
< df_cnty.loc[24,'no']=51
< df_cnty.loc[24,'cnty']='lianjiangxian'
< d_cnty={x:str(int(y)) for x,y in zip(df_cnty['cnty'],df_cnty['no'])}
< d_cnty.update({'xinbeishi':'41','taoyuanshi':'32'})
< d_cnty.update({'sea':'53'})
---
> df_cnty=read_csv('town3.csv')
> d_cnty={x:y for x,y in zip(df_cnty['code'],df_cnty['Name'])}
> d_cnty.update({5300:'sea'})
```

- 變數名稱與結果檔名因應修改

```python
28c17
< df['YXCO']=[str(x)+str(y) for x,y in zip(df['YX'],df['CNTY'])]
---
> df['YXCO']=[str(x)+str(y) for x,y in zip(df['YX'],df['DICT'])]
34c23
< df_xyc=DataFrame({'x':x,'xx':x,'y':y,'cnty':co})
---
> df=DataFrame({'x':x,'xx':x,'y':y,'dict':co})
38,40c27,28
< d2_cnty={x:y for x,y in zip(d_cnty.values(), d_cnty.keys())}
< df_xyc['name']=[d2_cnty[str(i)] for i in df_xyc['cnty']]
< df_xyc.set_index('cnty').to_csv('cnty_xy.csv')
---
> df['name']=[d_cnty[i] for i in df['dict']]
> df.set_index('dict').to_csv('dict_xy.csv')
```

