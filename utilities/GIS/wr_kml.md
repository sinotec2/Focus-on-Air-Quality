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
  - python3版需使用第3方軟件`legacycontour`。
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

## Reference
- wiki, **Keyhole標記語言**, [wiki](https://zh.wikipedia.org/wiki/KML), 2021年2月7日.
