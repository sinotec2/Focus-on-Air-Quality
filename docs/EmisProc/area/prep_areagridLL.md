---
layout: default
title: "prep_areagridLL.py"
parent: "Area Sources"
grand_parent: "Emission Processing"
nav_order: 1
date:               
last_modified_date:   2021-12-01 14:16:46
---

# 重新計算網格座標
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
- 此處針對面源的空間位置進行重新計算，理由如下：
  - 有直角座標位置可以快速繪圖，確認數據的正確性
    - 如外島、船舶、重要PM排放源等。
  - 因二度分帶`twd97`系統無法應用在外島，須重新由經緯度計算
  - 資料筆數較多，每次執行主程式須重新計算，太浪費時間。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[面源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/area/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，亦為此處之前處理。  

### 程式說明
- 使用[pyproj](https://pyproj4.github.io/pyproj/stable/)進行座標系統的轉換
- 座標原點採臺灣島的中心`(23.61000, 120.9900)`，以[twd97](https://pypi.org/project/twd97/)模組進行該點絕對值之計算。
- 合併面源的2層分類代碼，以利後續的計算。

```python
kuang@114-32-164-198 /Users/TEDS/teds11/area
$ cat prep_areagridLL.py
from pandas import *
import twd97
from pyproj import Proj
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

df=read_csv('TEDS11_AREA_WGS84.csv')
lon,lat=np.array(df.WGS84_E),np.array(df.WGS84_N)
x,y=pnyc(lon,lat, inverse=False)
df['UTME']=x+Xcent
df['UTMN']=y+Ycent
df.loc[df.NSC_SUB.map(lambda x:isna(x)),'NSC_SUB']='b'
df['nsc2']=[str(i)+j for i,j in zip(list(df.NSC),list(df.NSC_SUB))]
df.set_index('UTME').to_csv('areagrid11LL.csv')
```

## Reference
- alan.d.snow and jswhit, **pyproj 3.3.0**, [pypi.org](https://pypi.org/project/pyproj/), Released: Nov 18, 2021
- Tom.Chen, **Python converter between TWD97 and WGS84**, [pypi.org](https://pypi.org/project/twd97/), Oct 22, 2014