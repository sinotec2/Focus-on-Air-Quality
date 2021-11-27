---
layout: default
title: "計算距離反比加權值"
parent: "CODiS"
grand_parent: "wind models"
nav_order: 3
date:               
last_modified_date:   2021-11-26 14:11:53
---

# 計算距離反比加權值

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

### 空間尺度之界定
逆(反)軌跡圖是空氣污染來源追蹤、溯源解析過程中經常使用的圖像工具。按照污染源與受體空氣品質關係的遠近，分析的尺度有：
- 近距離、~10公里範圍，高斯煙流擴散模式可以應用之範圍，時間約在小時解析度範圍。可以用代表性地面測站之風向直接進行(統計)解析研判。
- 城市~地區尺度，中距離約數10~百公里範圍，受海陸風影響的平坦~平緩地區，時間範圍約在1日~3日之間。可以用地面站網、氣象模式進行解析。
- 地區~長程傳輸現象，約數百~7千公里範圍，除前述現象外，也受到天氣現象的顯著影響，時間範圍約3日~週之間。須以氣象模式、[HYSPLIT](https://www.arl.noaa.gov/hysplit/hysplit/)等模式進行**三維**風場與軌跡解析。
此處要處理的是城市~地區尺度，因此需應用全臺自動站的風速風向數據。

### 軌跡正確性與風場模式
軌跡正確性的關鍵在於風場，因此有以：
- 高解析度觀測站數據內插、由於風場的正確性與測站所函蓋的範圍有關，密度較高的平地範圍，會有較高的正確性，而在海上或山區等測站密度較低範圍，可能有較低的正確性。
- 數值氣象預報模式產品、如WRF，有解析度與範圍的限制。一般WRF最高解析度為3公里
- 客觀分析等不同方式產生風場。(介於前2者之間)

### 策略方案
- CODiS提供的數據至少有300個測站是有風速、風向數據
  - 全台面積36,193平方公里，平均一站分攤119平方公里，約為11公里X11公里之解析度，平地還有更高的密度
  - 用以內插建立風場，應有其充分性與正確性
- CWB提供有WRF_3KM預報風場，亦足以代表海上、山區等測站較少範圍
- 建立內插方法
  - 有測站範圍地區則以測站值為主
  - 海上則以模式分析結果，做為3公里X3公里之虛擬測站，納入相同機制進行計算。
- 全區風場計算儲存的必要性
  - 全區風場事先計算儲存看似方便，然佔用空間龐大，因電腦速度提高了，因此在實際計算時似乎也沒有提高太多效率。
  - 主要由於軌跡線經過網格數有限，實在沒有必要進行全臺風場之計算或儲存。
- 發展路徑
  - 直接內插觀測值
  - 直接內插模擬值、[FDDA](https://documen.site/download/wrffddadudhia_pdf)模擬值
  - 以[WRFDA](https://ral.ucar.edu/solutions/products/wrfda)或其他模式合併觀測及模式  

## 內插程式說明
- twn_cwbInverDist.py為準備CODiS測站與網格點間距離反比權重之程式，可以在[github](https://raw.githubusercontent.com/sinotec2/cwb_Wind_Traj/master/twn_cwbInverDist.py)下載。
- 所謂某一點的**內插**值，則將會是所有測站觀測值對該點之**加權平均**值。
- 引用模組。此處會用到[twd97](https://pypi.org/project/twd97/)模組，會需要先安裝好。

```python
kuang@node03 /home/backup/data/cwb/e-service/surf_trj
$ cat -n twn_cwbInverDist.py
     1  #!/cluster/miniconda/envs/py37/bin/python
     2  from pandas import *
     3  import twd97, sys
     4  import numpy as np
     5  from scipy.io import FortranFile
```

- 準備測站資料表
  - 測站表中有845站，然而有些測站已經關閉、有些是雨量站沒有風速風向數據，如前所述，實際上大約只有300~400站。

```python
     7  dir = '/home/backup/data/cwb/e-service/read_web/'
     8  dfS = read_csv(dir + 'stats_tab.csv')
     9  # drop the closed station
    10  dfss = dfS.loc[dfS.END.map(lambda x: x == '\u3000')]
    11  # drop the precipitation stations
    12  dfS = dfss.loc[dfss.stno.map(lambda x: x[:2] != 'C1')]
    13  no_data=['466850', '467550', '467790']
    14  dfS = dfS.loc[dfS.stno.map(lambda x: x not in no_data)].reset_index(drop=True)
```
- 經緯度轉換直角座標系統，以計算直線距離
```python
    15  # coordinate transformation of stations
    16  lat, lon = np.array(dfS.LAT), np.array(dfS.LON)
    17  xy = np.array([twd97.fromwgs84(i, j) for i, j in zip(lat, lon)])
    18  x, y = (xy[:, i] for i in [0, 1])
    19  dfS['xy'] = x // 1000 * 10000 + y // 1000
    20  dfS['twd97_x'] = x
    21  dfS['twd97_y'] = y
    22  col='stno,stat_name,twd97_x,twd97_y'.split(',')
    23  dfS[col].set_index('stno').to_csv('stat_wnd.csv')
    24  # sys.exit('OK')
```

- 產生風場之格點
  - 其範圍與空品模擬的d4一樣，解析度則為1公里，網格數由程式自行計算。(`len(y_mesh), len(x_mesh)=414, 252`)
  - 為提高程式計算效率，實際內插應用時，只會考慮軌跡點周圍1公里網格之風場。

```python
    25  # grid_generation
    26  Longitude_Pole = 120.9900
    27  Latitude_Pole = 23.61000
    28  nx, ny, delta_xy = 83, 137, 3000
    29  x0_LCP, y_LCP = -124500, -205500
    30  xcent, ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    31  x0, y0 = np.array([x0_LCP, y_LCP]) + np.array([xcent, ycent])
    32  xe, ye = np.array([x0, y0]) + [nx * delta_xy, ny * delta_xy]
    33  x_mesh = [i for i in range(int(x0 / 1000) - 1, int(xe / 1000) + 2)]
    34  y_mesh = [i for i in range(int(y0 / 1000) - 1, int(ye / 1000) + 2)]
    35  x_g, y_g = np.meshgrid(x_mesh, y_mesh)
    36
```

- 逐點計算與觀測站位置的差值(`xm`, `ym`)、平方值倒數、加總、產生權重值

```python
    37  # distance square inverse as a weighting
    38  R2 = np.zeros(shape=(len(y_mesh), len(x_mesh), len(dfS)))
    39  for s in range(len(dfS)):
    40    xm = x_g - x[s]/1000.
    41    ym = y_g - y[s]/1000.
    42    R2[:, :, s] = 1. / (xm * xm + ym * ym)
    43  for j in range(len(y_mesh)):
    44    for i in range(len(x_mesh)):
    45      sR2 = sum(R2[j, i, :])
    46      R2[j, i, :] = R2[j, i, :] / sR2
    47

```
- 儲存檔案
```python
    48  # store the matrix
    49  fnameO = 'R414_252_431.bin'
    50  with FortranFile(fnameO, 'w') as f:
    51    f.write_record(R2)
    52  with FortranFile('x_mesh.bin', 'w') as f:
    53    f.write_record(x_mesh)
    54  with FortranFile('y_mesh.bin', 'w') as f:
    55    f.write_record(y_mesh)
```

## next
- [軌跡程式](https://sinotec2.github.io/jtd/docs/wind_models/CODiS/traj/)說明
- 軌跡程式碼可以由[githup](https://raw.githubusercontent.com/sinotec2/cwb_Wind_Traj/master/traj2kml.py)下載，此處分段說明如下


## Reference
- MM5/WRF之[little_r](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式
- Brendan Arnold, **FORTRAN format interpreter for Python**, [fortranformat 1.0.1](https://pypi.org/project/fortranformat/), Released: Apr 6, 2021
- NOAA, [HYSPLIT](https://www.arl.noaa.gov/hysplit/hysplit/)
- Jimy Dudhia， **WRF Four Dimensional Data Assimilation (FDDA)**, [documen.site](https://documen.site/download/wrffddadudhia_pdf),  May 12, 2018 
- Tom.Chen, **Python converter between TWD97 and WGS84**, [pypi.org](https://pypi.org/project/twd97/), Oct 22, 2014

