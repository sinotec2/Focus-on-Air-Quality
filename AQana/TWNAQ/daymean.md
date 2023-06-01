---
layout: default
title: 日均值計算
parent: Taiwan AQ Analysis
grand_parent: AQ Data Analysis
last_modified_date: 2022-02-08 13:46:05
tags: python
---

# 環保署測站數據日均值之計算
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

- 環保署測站檔案是個以日為單位的文字檔案，過去如果要計算日均值，需以迴圈計算。如果還遇到要計算風速風向的向量平均，分屬檔案不同段落，須逐一檢視。
- 本程式的特色是將數據以`np.array`型式批次處理，並且只有在計算向量平均值時，才對日的時間軸進行迴圈計算。
- 測站日均值計算結果可作為地區整併之基礎，如[鄉鎮區平均值計算](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/stn_dot/)、空品區極值之計算等等。

## 程式基本

### IO's

- 引數
  - 需要1個引數：年代(4碼)
- 測項名稱(及順序)
  - `/home/backup/data/epa/item2.txt`
- 輸出
  - YYYY.csv
  - 表頭除了日期與測站外，所有環保署測站的測項均放在欄位上

```python
In [415]: df.columns
Out[415]:
Index(['ymd', 'stn', 'SO2', 'CO', 'O3', 'PM10', 'NOx', 'NO', 'NO2', 'THC',
       'NMHC', 'WIND_SPEED', 'WIND_DIREC', 'SIGMA', 'WD_GLOBAL', 'AMB_TEMP',
       'DEW_POINT', 'SHELT_TEMP', 'PRESSURE', 'GLIB_RADIA', 'UBV_RADIA',
       'NET_RADIA', 'PH_RAIN', 'RAIN_COND', 'RAINFALL', 'CH4', 'RAIN_INT',
       'PM2.5', 'UVB', 'UBA'],
      dtype='object')
```

### 使用模組

- `math`模組是為計算向量平均的風速風向

```python
from pandas import *
import sys, os, subprocess
import numpy as np
import math
```

### 基本設定

```python
root='/home/backup/data/epa/'
marks=['      ','******']
fname=root+'item2.txt'#items of EPA monitoring stations
with open(fname,'r') as ftext:
  itm=[line.strip('\n') for line in ftext]
ditm={i:itm[i] for i in range(len(itm))}
nitm={ditm[i]:i for i in ditm if ditm[i] !='dum'}
wswd=[nitm['WIND_SPEED'],nitm['WIND_DIREC']]
```

### 檔案管理

- 檔案以月分及測站來命名並分開儲存。
- 年度則為不同目錄的區別。
- 因此需以檔名來進行迴圈讀取、解析、再予以累積成為全年檔案。

```python
yr=sys.argv[1]
fnames=subprocess.check_output('ls '+root+yr+'/HS*.???',shell=True).decode('utf8').split('\n')[:-1]
fnames=[f for f in fnames if f[-3] in '01']

df=DataFrame({'ymd':[],'stn':[]})
for c in itm:
  if c=='dum':continue
  df[c]=0
for fname in fnames:
  with open(fname,'rb') as f:
    fn=[line for line in f]
  if len(fn)==0:continue
  fn=[str(i).replace('r','').replace('n','').replace('\\','').replace("'","") for i in fn]
```

1. 以`subprocess`執行`ls`指令，納入所有當年度的檔案
2. 由於延伸檔名為測站編號，只能是以0或1開頭的數字，其餘排除。
3. 先開啟一個空白的資料表，包括了日期、測站編號、以及各個測項名稱之欄位。
4. 經測試，雖然原始檔是各文字格式檔案，似乎只有簡單跳行指令，但實際上可能會有其他內碼無法辨識，因此以`'rb'`格式讀取較為妥當。

## 程式重點說明

### 原始檔資料表化

- 原始檔案的特性
  - 以日期與測項為縱軸、以小時為橫軸的24小時值表
  - 行內以逗號或空格分開(前者為大多數)，再沒有其他分隔方式。
- 策略上除了保持縱軸的順序之外，橫軸須先進行平均，以簡化表格。

```python
  if ',' in fn[0]:
    itms,ymds=(np.array([int(line.split(',')[j]) for line in fn],dtype=int) for j in [2,3])
    cons=np.array([np.array([i.strip('\n') for i in line.split(',')[4:]], dtype=str) for line in fn])
  else:
    itms,ymds=(np.array([int(line.split()[j]) for line in fn],dtype=int) for j in [1,2])
    cons=np.array([np.array([i.strip('\n') for i in line.split(',')[3:]], dtype=str) for line in fn])
  if ymds.mean()<20000000:ymds+=20000000
  for m in marks:
    cons=np.where(cons==m,'-999',cons)
```

- `itms,ymds`為測項序位、日期等2欄位
- `cons`為監測成果，為2維矩陣。因監測成果可能會有缺值、也有以全形空白、星號(`mark`)等來替代者。需先挑出替換。並加上遮罩(mask)，以避免在平均時造成錯誤。
- 此處即以`np.ma.mean`平均的方式，消除其第二個維度，成為形狀與`itms,ymds`一樣的向量。

```python
  cons=np.array(cons,dtype=float)
  masked = np.ma.masked_where(cons< 0, cons)
  cons=masked.mean(axis=1)
```

- 將其整理成為一個全新的資料表`dd`

```python
  dd=DataFrame({'ymds':ymds,'itms':itms,'con':cons})
```

### 向量平均的風速風向

- 環保署測站的風向紀錄會出現**888**的錯值
- 應為靜風測值、不具代表性
- 此處將該小時的風速設為0，將不會對平均值產生影響

```python
def vec_mean(ws,wd):
  idx=np.where(wd==888)
  if len(idx[0]>0):ws[idx]=0
  wd_rad = np.radians(wd)
  wx = ws * np.cos(wd_rad)
  wy = ws * np.sin(wd_rad)
  wx_avg = np.mean(wx)
  wy_avg = np.mean(wy)
  mean_wd_rad = math.atan2(wy_avg, wx_avg)
  mean_wd_deg = np.degrees(mean_wd_rad)
  if mean_wd_deg < 0: mean_wd_deg+=360
  mean_ws = np.mean(ws)
  return mean_ws, mean_wd_deg
```

- 因風速、風向數據分別位在原始檔案的不同位置，可以用`.loc[]`將其位置予以標定

```python
  for ymd in s_ymds:
    iws,iwd=(dd.loc[(dd.ymds==ymd) & (dd.itms==i)].index.values for i in wswd)
    dd.loc[iws,'con'],dd.loc[iwd,'con']=vec_mean(masked[iws,:],masked[iwd,:])
```

### 逐月結果之轉軸與累計

- 前述dd的縱軸隱含了2個維度(日期與測項序)，須逐一將其拆解。
- 以`dd.loc[]`篩選出特定測項，再將其存到資料表`di`指定欄位處
- 此處尚未確認缺值
- 將此月檔案累加到全年檔案之後

```python
  di=DataFrame({'ymd':s_ymds})
  di['stn']=int(fname[-3:])
  for c in itm:
    if c=='dum':continue
    val=list(dd.loc[dd.itms==nitm[c],'con'])
    if len(val)!=len(di):continue
    di[c]=val
  df=df.append(di,ignore_index=True)
```

### 輸出

```python
df.set_index('ymd').to_csv(yr+'.csv')
```

## 程式下載

{% include download.html content="[daymean.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/TWNAQ/day_mean.py)" %}