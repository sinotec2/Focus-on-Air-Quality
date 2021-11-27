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
將CODiS數據整併成全台一天一檔之後，適合進行全島的分析。但仍然需要一有效率的內插工具，讓沒有測站的外海、高山，也有內插或外插值。
此處以空氣品質最相關的風速、風向為分析主題，檢討如下：
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

## next steps
- 加權值是風場內插計算時需使用到的基本數據。內插風場時計算軌跡的重要依據。
- 軌跡程式碼可以由[githup](https://raw.githubusercontent.com/sinotec2/cwb_Wind_Traj/master/traj2kml.py)下載，詳見[分段說明](https://sinotec2.github.io/jtd/docs/wind_models/CODiS/traj/)。


## Reference

