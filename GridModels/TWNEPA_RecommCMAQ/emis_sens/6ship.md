---
layout: default
title: 船舶排放之敏感性分析
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 6
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 船舶排放之敏感性分析
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
- TEDS11並沒有公開更新後的船舶排放量。
- 公版基準排放量檔案中船舶的空間分布，與TEDS10很類似，缺乏海峽中線西方與公海部分排放量，這非常可能是低估SO<sub>2</sub>濃度的原因。
- 要探討這個課題，首先必須要能將基準排放量中開放水域的部分予以歸零，才能探討次部分排放量的影響程度。
- 公版模式提供了ocean.ncf，其中的MASK有3個數字，分別率定：
  - 2:開放水域
  - 1:海岸線
  - 0:其他
- 程式需要將開放水域位置予以標定，將所有該等位置的排放量歸零，即可。

## dSHIP.py
- 使用np.where將開放水域位置予以標定（`idx`）
- 事先先複製一份基準排放量檔案當成模版
- 注意nc檔案並不適用np.array的fancy indexing
  - 詳[NC檔案多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)

```python
In [24]: pwd
Out[24]: '/data/cmaqruns/2019simen/input/201901/grid03/smoke'

In [25]: !cat dSHIP.py
import numpy as np
import netCDF4
fname='/data/cmaqruns/2019simen/output/2019-01/grid03/ocean/ocean.ncf'
nc = netCDF4.Dataset(fname,'r')
v='MASK'
mask=nc[v][0,0,:,:]
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
idx=np.where(mask==2)
fname='/data/cmaqruns/2019simen/output/2019-01/grid03/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_dSHIP'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
var=np.zeros(shape=(nt,nrow,ncol))
for v in V[3]:
  var[:,:,:]=nc[v][:,0,:,:]
  var[:,idx[0],idx[1]]=0
  nc[v][:,0,:,:]=var[:,:,:]
nc.close()
```

## 船舶與基準排放量之比較
- 月均值排放量，單位：gmole/s(氣狀物)或g/s(粒狀物)
  - 粒狀物定義：`p=[v for v in V[3] if v[0]=='P' and v!='PAR']`，共20項。
- 船舶排放量
  - N/P階遠小於基準排放量
  - S在同一數量級、僅1/2.1

|K|m above ground|depth(m)|SO2|NOx|particulates|
|:-:|:-:|:-:|:-:|:-:|:-:|
|0|0~19.85|39.775|4.646|9.116|165.170|

- 基準排放量
  - 粒狀物以粗顆粒(PMC)為主，佔了2163.085g/s   
  - K0~1為影響地面污染的主要原因
    - K0為船舶的2.1倍
    - K1排放量約與船舶相當
  - K4(電廠煙囪)排放也僅為船舶1.8倍

|K|m above ground|depth(m)|SO2|NOx|particulates|
|:-:|:-:|:-:|:-:|:-:|:-:|
|0|0~19.85|39.775|10.033|139.385|3523.392|
|1|19.85~59.62|59.821|4.522|13.901|74.911|
|2|59.62~119.4|120.357|4.23|20.157|58.309|
|3|119.4~239.8|203.458|6.975|24.744|47.174|
|4|239.8~443.2|291.484|8.792|15.76|36.317|
|5|443.2~734.7|345.108|0.427|0.621|1.809|
|6|734.7~1079|403.888|0.001|0.002|0.033|
|7|1079~1483|471.907|0.000|0.000|0.003|

## 船舶排放造成的空氣品質增量
- 基準空氣品質扣除去除船舶排放後之模擬空氣品質，即為船舶排放所造成的增量。2019年1月份月均值模擬結果比較如圖所示。

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SO2SHIP_JanT.PNG)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SO2_JanT.PNG)|
|:-:|:--:|
| <b>船舶排放所造成的濃度差異(增量)</b>| <b>一月份SO2月平均濃度</b>|

## Actions
- 船舶SO2排放總量不及背景基準，模擬濃度占比更低，可能是SO2低估原因  
  - 由全球AIS數據推估船舶排放量、參[船隻排放空間分布之重分配](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/EDGARv5/ShipDensity/)
  - [EDGAR](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/EDGARv5/Ed2CMAQ/)
- 人為污染源所造成SO2濃度不及雲雨洗滌效應，大多地區濃度偏低。
  - BC及背景污染源(火山、生物源)仍有待補充
    - [Sulfur Emission](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/sulfur-emission)
    - [Biogenic Sulfur Emissions](https://pubs.acs.org/doi/pdf/10.1021/bk-1989-0393.ch001)
    
