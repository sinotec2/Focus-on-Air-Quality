---
layout: default
title:  等值圖KML檔之撰寫
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-02-11 13:39:55
---

# 等值圖KML檔之撰寫
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
- 製作簡易的等值圖是模式模擬後處理必須的程序，讓使用者可以快速檢視模擬結果、容易調整範圍，最好是輕量化、容易、方便的套件。
  - [SURFER](https://www.goldensoftware.com/products/surfer)：雖然可以做到報告品質，但目前只在ms win平台，linux/macOS無法作動。底圖須另取得，且4點georeferencing太麻煩(適用大範圍非直角座標系統之底圖)。
  - [QGIS](https://zh.wikipedia.org/wiki/QGIS)：是相當完整、輕量化、公眾領域的GIS程式，雖然可以有完整解析度的地圖作為底圖，但同樣沒有regrid內插，只有色塊(tile)形式。
  - [VERDI](https://www.evernote.com/shard/s125/sh/e57ae550-4ee0-4417-b56b-b340f50bc43e/21f7f90a91e5ede50f228b557de1f347)：篩檢品質。沒有regrid內插。只有向量底圖(行政區界)，對小範圍缺少資訊。只能輸入nc、uamiv格式檔案。
  - [MeteoInfo](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/MeteoInfo/)：可以接受ASCII GRD檔案。但也是只有向量底圖。
  - 商業套裝軟體(如[BREEZE AERMOD](https://www.trinityconsultants.com/software/dispersion/aermod)、[AERMOD View™](https://www.weblakes.com/products/aermod/index.html)、[AERMOD Cloud<sup>R</sup>](https://www.envitrans.com/software-aermod-cloud.php)、[BEEST Suite](https://www.providenceoris.com/product/beest-suite/))：無法接受TWD97座標系統。沒有中文街道底圖。
- [KML](https://zh.wikipedia.org/wiki/KML)檔案現已經被很多網路地圖所接受成為圖層，包括[Google Map]()、OpenStreet Map([OSM](https://www.openstreetmap.org/#map=8/23.611/120.768))等等網路地圖界面。
  - 格式可以參考[範例](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/#檔案來源與解壓縮)及google[官網](https://developers.google.com/kml/documentation/kml_tut)。
- 等值圖即為等值線多邊形之重疊。等值線多邊形的座標，則可以經由`cntr`套件計算。
  - python2包裹在`matplotlib`之內
  - python3版需使用第3方軟件[legacycontour](https://github.com/matplotlib/legacycontour)。
  - 安裝：動態連結到[github](https://github.com/matplotlib/legacycontour.git)

```bash
  python3 -m pip install --index-url https://github.com/matplotlib/legacycontour.git legacycontour`
```
- or 下載完整原始碼(參考[github討論](https://github.com/badlands-model/pyBadlands_serial/issues/1))

```bash
git clone https://github.com/matplotlib/legacycontour.git
cd legacycontour
python setup.py install
```

## 程式說明
- grid_z2：2維實數矩陣
- 輸出檔名：fname+'.kml'
- 等值線層數：N = 10
- 程式碼下載[cntr_kml.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/cntr_kml.py)

### 引數說明
- grid_z2, lon, lat, fname
  - grid_z2：2維實數矩陣
  - lon, lat：2維實數矩陣
  - fname：結果檔名

### 色階與透明度之定義與調查
- 色階固定為10層，太多(>10)會無法辨識，太少(<5>)則沒有特性。
- 設定自綠色漸變至紅色，參考[Zonum Solutions色階表](http://www.zonums.com/online/color_ramp/)
- 透明度'28'約為40%，'4d'約為75%
  - 越透明就越看不到等值圖的特性
  - 越不透明就越看不到底圖內容

```python
# levels size,>10 too thick, <5 too thin
N = 10
mxgrd=max([10.,np.max(grid_z2)])
levels = np.linspace(0, mxgrd, N)
col = '#00FF0A #3FFF0A #7FFF0A #BFFF0A #FFFF0A #FECC0A #FD990A #FC660A #FB330A #FA000A'.replace('#', '').split()
if len(col) != N: print ('color scale not right, please redo from http://www.zonums.com/online/color_ramp/')
aa = '28'  # ''28'~ 40%, '4d' about 75%
rr, gg, bb = ([i[j:j + 2] for i in col] for j in [0, 2, 4])
col = [aa + b + g + r for b, g, r in zip(bb, gg, rr)]
```

### 計算等值線
- cntr.Cntr將2維矩陣分布在經緯度座標系統，形成3維立體模型
- c.trace則按照指定值(level)找到符合高度的座標位置，形成多邊形序列nlist。
- 取其中間位置為segs，準備輸出

```python
e, w, s, n = np.max(lon), np.min(lon), np.min(lat), np.max(lat)
c = cntr.Cntr(lon, lat, grid_z2)
for level in levels[:]:
  nlist = c.trace(level, level, 0)
  segs = nlist[:len(nlist) // 2]  
```

### 各層多邊形之輸出

```python
# repeat for the level lines
  i = levels.index(level)
  for seg in segs:
    line.append('<Placemark><name>level:' + str(level) + '</name><styleUrl>#level' + str(i) + head2)
    leng = -9999
    for j in range(len(seg[:, 0])):
      line.append(str(seg[j, 0]) + ',' + str(seg[j, 1]) + ',0 ')
      if j > 0:
        leng = max(leng, np.sqrt((seg[j, 0] - seg[j - 1, 0]) ** 2 + (seg[j, 1] - seg[j - 1, 1]) ** 2))
    leng0 = np.sqrt((seg[j, 0] - seg[0, 0]) ** 2 + (seg[j, 1] - seg[0, 1]) ** 2)
```
### 邊界線之閉合
- 多邊形碰到東西南北其中1邊、碰到2個邊、等等情況，逐一處理

```python
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
```

## 各種點陣圖數據檔之應用
### [dat2kml](http://114.32.164.198/dat2kml.html)遠端計算服務
- [PLT2kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/OU_pathways/PLT2kml/):讀取煙流模式之輸出檔，進行REGRID並寫成kml檔案
- Convert ISC/AERMOD PLOTFILE result to KML file and regrid to SURFER grd file ASCII TXT, csv (X,Y,C). 

### [tif2kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/#tif2kmlpy)
- GeoTiff是GIS常用的數據格式，如以KML與OSM檢視會比任何GIS程式更輕便。

## 結果範例
### KML檔案格式確認
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

### Google Map 貼圖結果(林口電廠範例)

| ![kml_demo.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/kml_demo.png) |
|:--:|
| <b>圖 林口電廠周邊地形KML檔案輸出結果範例</b>|  

## Reference
- wiki, **Keyhole標記語言**, [wiki](https://zh.wikipedia.org/wiki/KML), 2021年2月7日.
