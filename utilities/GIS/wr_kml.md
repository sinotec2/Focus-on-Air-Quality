---
layout: default
title:  撰寫等值線之KML檔
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-02-11 13:39:55
---

# python撰寫等值線之KML檔
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
- [KML](https://zh.wikipedia.org/wiki/KML)檔案格式可以參考[範例](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/#檔案來源與解壓縮)及google[官網](https://developers.google.com/kml/documentation/kml_tut)。
- 等值線的座標，可以經由`cntr`套件計算。
  - python2包裹在`matplotlib`之內
  - python3版需使用第3方軟件[legacycontour](https://github.com/matplotlib/legacycontour)。
  - 安裝：`python3 -m pip install --index-url https://github.com/matplotlib/legacycontour.git legacycontour`

## 程式碼
- grid_z2：2維實數矩陣
- 輸出檔名：fname+'.kml'
- 等值線層數：N = 10

```python
import numpy as np
import legacycontour._cntr as cntr

# levels size,>10 too thick, <5 too thin
N = 10
mxgrd=max([10.,np.max(grid_z2)])
levels = np.linspace(0, mxgrd, N)
col = '#00FF0A #3FFF0A #7FFF0A #BFFF0A #FFFF0A #FECC0A #FD990A #FC660A #FB330A #FA000A'.replace('#', '').split()
if len(col) != N: print ('color scale not right, please redo from http://www.zonums.com/online/color_ramp/')
aa = '28'  # ''28'~ 40%, '4d' about 75%
rr, gg, bb = ([i[j:j + 2] for i in col] for j in [0, 2, 4])
col = [aa + b + g + r for b, g, r in zip(bb, gg, rr)]

# round the values of levels to 1 significant number at least, -2 at least 2 digits
i = int(np.log10(levels[1])) - 1
levels = [round(lev, -i) for lev in levels]

#the Cntr method is valid only in previous version of matplotlib
c = cntr.Cntr(lon, lat, grid_z2)
# the tolerance to determine points are connected to the boundaries
tol = 1E-3
col0 = '4d6ecdcf'
col_line0 = 'cc2d3939'


#writing the KML, see the KML official website
head1 = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.2"><Document><name><![CDATA[' + last + ']]></name>'
st_head = ''
st_med = '</color><width>1</width></LineStyle><PolyStyle><color>'
st_tail = '</color></PolyStyle></Style>'
for i in range(N):
  st_head += '<Style id="level' + str(i) + '"><LineStyle><color>' + col[i] + st_med + col[i] + st_tail
head2 = '</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>'
tail2 = '</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
line = [head1 + st_head]
# repeat for the level lines
e, w, s, n = np.max(lon), np.min(lon), np.min(lat), np.max(lat)
for level in levels[:]:
  nlist = c.trace(level, level, 0)
  segs = nlist[:len(nlist) // 2]
  i = levels.index(level)
  for seg in segs:
    line.append('<Placemark><name>level:' + str(level) + '</name><styleUrl>#level' + str(i) + head2)
    leng = -9999
    for j in range(len(seg[:, 0])):
      line.append(str(seg[j, 0]) + ',' + str(seg[j, 1]) + ',0 ')
      if j > 0:
        leng = max(leng, np.sqrt((seg[j, 0] - seg[j - 1, 0]) ** 2 + (seg[j, 1] - seg[j - 1, 1]) ** 2))
    leng0 = np.sqrt((seg[j, 0] - seg[0, 0]) ** 2 + (seg[j, 1] - seg[0, 1]) ** 2)
    ewsn = np.zeros(shape=(4, 2))
    j = -1
    # end points not closed, add coner point(s) to close the polygons.
    if leng0 > leng and leng0 / leng > 5:
      if abs(seg[j, 0] - e) < tol: ewsn[0, 1] = 1
      if abs(seg[0, 0] - e) < tol: ewsn[0, 0] = 1
      if abs(seg[j, 0] - w) < tol: ewsn[1, 1] = 1
      if abs(seg[0, 0] - w) < tol: ewsn[1, 0] = 1
      if abs(seg[j, 1] - s) < tol: ewsn[2, 1] = 1
      if abs(seg[0, 1] - s) < tol: ewsn[2, 0] = 1
      if abs(seg[j, 1] - n) < tol: ewsn[3, 1] = 1
      if abs(seg[0, 1] - n) < tol: ewsn[3, 0] = 1
      if sum(ewsn[1, :] + ewsn[2, :]) == 2: line.append(str(np.min(lon)) + ',' + str(np.min(lat)) + ',0 ')
      if sum(ewsn[1, :] + ewsn[3, :]) == 2: line.append(str(np.min(lon)) + ',' + str(np.max(lat)) + ',0 ')
      if sum(ewsn[0, :] + ewsn[3, :]) == 2: line.append(str(np.max(lon)) + ',' + str(np.max(lat)) + ',0 ')
      if sum(ewsn[0, :] + ewsn[2, :]) == 2: line.append(str(np.max(lon)) + ',' + str(np.min(lat)) + ',0 ')
    # TODO: when contour pass half of the domain,must add two edge points.
    line.append(tail2)
line.append('</Document></kml>')
with open(fname + '.kml', 'w') as f:
  [f.write(i) for i in line]
```

## 結果範例
### KML檔案
- level0~9的樣式
- 各層的多邊形頂點座標

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<Document><name><![CDATA[Hsinzhu]]></name>
<Style id="level0"><LineStyle><color>280AFF00</color><width>1</width></LineStyle>
  <PolyStyle><color>280AFF00</color></PolyStyle></Style>
<Style id="level1"><LineStyle><color>280AFF3F</color><width>1</width></LineStyle>
  <PolyStyle><color>280AFF3F</color></PolyStyle></Style>
<Style id="level2"><LineStyle><color>280AFF7F</color><width>1</width></LineStyle>
  <PolyStyle><color>280AFF7F</color></PolyStyle></Style>
...
<Style id="level9"><LineStyle><color>280A00FA</color><width>1</width></LineStyle>
  <PolyStyle><color>280A00FA</color></PolyStyle></Style>
<Placemark><name>level:4.2</name><styleUrl>#level3</styleUrl>
  <Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate>
    <coordinates>
      120.96411757783031,24.837148398246857,0 
      120.96411517775208,24.83714862491851,0 
      120.96411757779468,24.837149157475046,0 
...      
      120.97579154085555,24.839629777483797,0 
    </coordinates>
  </LinearRing></outerBoundaryIs></Polygon>
</Placemark>
</Document>
</kml>
```
### Google Map 貼圖結果
#### 林口電廠範例
| ![kml_demo.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/kml_demo.png) |
|:--:|
| <b>圖 林口電廠周邊地形KML檔案輸出結果範例</b>|  

#### 檢查項目：
- [範圍]()：是否以污染源排放為中心、是否符合設定範圍(海面範圍可視情況減少)
- [高值]()部分：是否符合地圖（鄉鎮區界線、稜線道路、山峰位置等）
  - 煙流大致會在2倍煙囪高度之等高線，產生高值。
  - 有群峰之地形範圍，煙流會在第一個碰觸點產生高值。
- [解析度]()：太低→地形特徵會消失。煙流本身會模糊化，解析度太高會增加執行時間，沒有必要。
- 等高線：一般公路設計會平行於等高線，可藉地圖中公路的走向，檢視地形數據結果的正確性
- 低值位置：一般地圖上是河流、住家村落、陂塘、農地等。
- 海岸線：等高線是否與地圖之海岸線平行

## Reference
- wiki, **Keyhole標記語言**, [wiki](https://zh.wikipedia.org/wiki/KML), 2021年2月7日.
