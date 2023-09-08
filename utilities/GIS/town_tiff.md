---
layout: default
title: 鄉鎮行政區多邊形轉1公里tiff檔
parent: GIS Relatives
grand_parent: Utilities
date: 2023-02-14
last_modified_date: 2023-02-14 10:18:47
tags: geotiff GIS netCDF
---

# 鄉鎮行政區多邊形轉1公里解析度tiff檔

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

- GeoTiff在GIS領域中是個常見的檔案格式，運用python來進行解析、轉檔的方式也有很多實例，可以詳見[python解析GeoTiff檔][geotiff]文中的各個連結。此處特別針對GML解析的多邊形轉tiff的程式設計進行說明
- 應用案例為台灣地區轉成d4範圍一公里解析度的鄉鎮區tiff檔案。

## 模組及IO

- 此處使用shapely模組來解讀

### 模板輸入

- 模板`'d4_twn1x1.tiff'`。可以由taiwan2020.tiff([2020全臺20M_DTM](https://data.gov.tw/dataset/138563))或類似(更新)資料整理而得。此處只有讀取其矩陣之形狀。
- 模板`'20160101.ncT'`是鄉鎮區範圍數據處理過程需要的網格化參考檔，如[網格濃度在行政區範圍內之平均](town_mn.md)。此處讀取座標設定值。

```python
import numpy as np
from pandas import *
import netCDF4
from libtiff import TIFF
import twd97
from shapely.geometry import Point, Polygon
import sys

tiff=TIFF.open('d4_twn1x1.tiff',mode='r')
image = tiff.read_image()
nrow3,ncol3=image.shape
nc = netCDF4.Dataset('20160101.ncT','r')
```

### 多邊形csv檔

- 可以由gml檔案整理而得。詳見[python解析GML檔](rd_gml.md)。
- 先去掉不成形的離散點
- 解開經緯度值
- 取各個多邊形的極大值，便於篩選時可以取用(要小心離島可能會差異很大如旗津區含有東沙島)。

```python
df=read_csv('polygons.csv')
df.drop(df.loc[df.lonlats.map(lambda x:len(x)<=2)].index, inplace=True)
df['lonlats']=[j.replace(',','').replace(')','').replace('(','').replace('[','').replace(']','').split() for j in df.lonlats]
df['lonlats']=[[float(i) for i in j] for j in df.lonlats]
df['lonlats']=[[(j[i],j[i+1]) for i in range(0,len(j),2)] for j in df.lonlats]
df['lonn']=[min([i[0] for i in j]) for j in df.lonlats]
df['latn']=[min([i[1] for i in j]) for j in df.lonlats]
df['lonx']=[max([i[0] for i in j]) for j in df.lonlats]
df['latx']=[max([i[1] for i in j]) for j in df.lonlats]
```

### 輸出檔

- 將會覆蓋原來的`'d4_twn1x1.tiff'`模板

## 座標系統之定義

- 將netCDF檔案的網格點，都轉成經緯度的`Point`，便於使用shapely的`within`函數

```python
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
xmin=Xcent+nc.XORIG+500
xmax=Xcent-nc.XORIG+500
ymin=Ycent+nc.YORIG+500
ymax=Ycent-nc.YORIG+500
x = np.arange(xmin, xmax, 1000)
y = np.arange(ymin, ymax, 1000)
if len(x)!=ncol3 or len(y)!=nrow3:sys.exit('wrong dimension')
X, Y = np.meshgrid(x, y)
ll=np.array([[twd97.towgs84(i,j) for i,j in zip(X[i,:], Y[i,:])] for i in range(nrow3)])
p1=[Point(i,j) for i,j in zip(ll[:,:,0].flatten(),ll[:,:,1].flatten())]
```

## within判斷與檔案輸出

- 輸出值為鄉鎮區代碼(town_id)
- 逐點進行判別。先進行鄉鎮區範圍極值的篩選
- tiff的原點在西北角。這與其他系統不同，要注意y軸index的設定(`image[nrow3-j-1,:]=twnji[j,:]`)。
```python
twnji=np.zeros(shape=image.shape).flatten()
isq=0
for pi in p1:
  n=int(5300)
  boo=(df.latn<=pi.x)&(df.lonn<=pi.y)&(df.latx>=pi.x)&(df.lonx>=pi.y)
  a=df.loc[boo].reset_index(drop=True)
  if len(a)!=0:
    for j in range(len(a)):
      plg=Polygon([(i[1],i[0]) for i in a.loc[j,'lonlats']])
      if pi.within(plg):
        n=int(a.loc[j,'twnid'])
        break
  twnji[isq]=n
  isq+=1
twnji=twnji.reshape(image.shape)
for j in range(nrow3):
    image[nrow3-j-1,:]=twnji[j,:]
tiff=TIFF.open('d4_twn1x1.tiff',mode='w')
tiff.write_image(image)
tiff.close()
```

[geotiff]: https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/ "python解析GeoTiff檔"