---
layout: default
title:  python解析KML檔
parent: GIS Relatives
grand_parent: Utilities
last_modified_date:   2021-12-17 14:44:41
---

# python解析KML檔
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

### 緣起
- 網格模式在進行污染來源分析時，經常需要排放區域的分區定義，一個網格化的[點陣圖(raster)](https://zh.wikipedia.org/wiki/%E4%BD%8D%E5%9B%BE)：
  * 不論是**CAMx-OSAT**、**CAMx-PSAT**或者是
  * [CMAQ-ISAM模組](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ISAM/withinD1/)，都需要這樣的raster檔案。
  * 具體問題：因為缺乏大陸方面的地理分區定義資料，在反軌跡計算時無法歸因於省份、排放區域等定性標籤。
- 然而一般網路公開的GIS檔案多是向量圖檔，是省界的polygon檔案，不正好是raster檔案。
  - 造成這種網路現象主要的理由，是因為raster檔案有其解析度的限制，提供者不知該提供到什麼樣的解析度才恰當，畢竟使用者定義的範圍解析度樣態真的太多樣了。
- 本作業聚焦在省界shape(或KML)檔，轉成模式解析度(d1)的raster檔案。
  * [KML](https://zh.wikipedia.org/wiki/KML)(Keyhole markup language)是Google發展的地理資訊語言檔案格式，經常使用在google地圖、open street 地圖平台上。

### 目標
- 建立範圍解析度(d1) raster的值(整數分區代碼)
- 除此之外，此次作業的重點在建立合理的分區方式。
  - 這是因為大陸地區現行的省、市、自治區等，有57個之多，超過合理的處理範圍，需要進一步整併。  

### 方案與檢討
- 向量檔案轉成點陣圖檔的方式有很多種，除了在[GIS內操作](https://www.youtube.com/watch?v=REEoiWhnOC4)，也有獨立的軟體如[Corel](http://product.corel.com/help/CorelDRAW/540240626/Main/CT/Doc/wwhelp/wwhimpl/common/html/wwhelp.htm?context=CorelDRAW_Help&file=CorelDRAW-Converting-vector-graphics-to-bitmaps.html)，也有業者提供[網站服務](https://mygeodata.cloud/converter/)。
  * 而在我們的應用中，2個檔案的座標系統也並非是完全一樣，不能直接套用。
- 而一般的GIS軟體(`gdal`程式)也可以做到`shape to raster`轉換，然而不知道是大陸方面檔案格式(層次或資料庫)的差異、或者數據太多(約有170個polygon)，**QGIS無法作動**!
- `python`可以直接讀取向量檔(`shape`及`KML`)，然而因為對`KML`格式較為熟悉，因此選擇以`KML`轉`raster`之進路。
  * `shape`檔案之讀取及處理詳參[shape_to_raster](https://www.evernote.com/shard/s125/sh/80584516-ae2c-e301-5128-0d45e49b97c1/abd5919c278850a9fc0273cf90324ce3)應用在d4範圍、d5解析度案例。
- 大陸行政區之整併方式，除了考量地理氣候方面的特徵，因為是空氣污染領域，除了文獻中常見的京津冀、長三角、珠三角 之外，也有人用華北、華中、華南來分大區。
  * 如果分區越細，軌跡機率就越少、排放量分配也較少。
  * 此外因為距離台灣很遠，d1範圍的解析度也有限(81K)，如果超過10區，每區網格數會太少。
  * 以美國而言，有所謂**climate region**，臺灣地區也有所謂空品區的概念。 建議還是以大陸官方空氣質量管理之分區方式為宜。

## 檔案來源與解壓縮
- chn_admbnda_adm1_ocha.kmz
  - [CSISS GeoBrain Cloud, George Mason University](https://cloud.csiss.gmu.edu/uddi/th/dataset/china-administrative-boundaries)
  - [The Humanitarian Data Exchange](https://data.humdata.org/dataset/china-administrative-boundaries)
  - [github](https://github.com/edwenger/2019-nCoV/find/master)
- `kmz`是個`zip`檔，`unzip`後可以得到其`kml`檔案(將其更名為`doc.kml`以利程式讀取)
- `doc.kml`部分內容(`Placemark=ID_00000`安徽省)

```html
...
    <Placemark id="ID_00000">
      <name>Anhui Province</name>
...
      <styleUrl>#PolyStyle00</styleUrl>
      <MultiGeometry>
        <Polygon>
          <extrude>0</extrude><altitudeMode>clampToGround</altitudeMode>
          <outerBoundaryIs><LinearRing><coordinates> 
               116.935206535,34.08702338100009,0 
               116.930544829,34.08849598800008,0 
               116.918619955,34.09428245300003,0                
...               
```

## [rd_kml.py](https://github.com/sinotec2/cmaq_relatives/blob/master/land/gridmask/rd_kml.py)

### 程式分段說明
- 模組之調用
  - 此處使用到[pykml](https://pythonhosted.org/pykml/)的`parser`

```python
1	from pykml import parser
2	from os import path
3	from pandas import *
4	
```
- 讀取`doc.kml`：來源見前述。

```python
5	kml_file = path.join('doc.kml')
6	with open(kml_file) as f:
7	  doc = parser.parse(f).getroot()
```
- 讀取所有的位置標籤(`Placemark`)，及其名稱(`names`)
  - 名稱`names`(會出現在`KML`檔案的`Placemark`(`plms`)的名稱標籤)，此名稱與網站提供的`xls`資料表名稱一致。共57筆，有重複。(line 8~9)

```python
8	plms=doc.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
9	names=[i.name for i in plms]
10	
```
- `pykml`並未內設一制式的從屬關係層次，而是用`getparent` 方法找出來物件之間的親子關係。
  - 在本案例中`MultiGeometry`與`Polygon`之間是有關係的，而`MultiGeometry`與`Placemark`的順序相同，可以引用相同的名稱，因此就可以由下向上，串連找到每一個`Polygon`的名稱。
  1. 先找到MultiGeometry物件，以及其個別的標籤(MultiGeometry 沒有名稱，只有標籤) (line 11~12)
  2. 找到Polygon物件，及其上層MultiGeometry 物件的標籤(line 14~15)
- 讀取幾何形狀(`mtgs`)與其標籤(`mtg_tag`)

```python
11	mtgs=doc.findall('.//{http://www.opengis.net/kml/2.2}MultiGeometry')
12	mtg_tag=[str(i.xpath).split()[-1][:-2] for i in mtgs]
13	
```
- 讀取多邊形(`plgs`)與其來源(`plg_prt`)

```python
14	plgs=doc.findall('.//{http://www.opengis.net/kml/2.2}Polygon')
15	plg_prt=[str(i.getparent().values).split()[-1][:-2] for i in plgs]
16	
```
- 使用`pyval`指令收集多邊形頂點的座標值
  - 參考[pykml.parser.fromstring函數](https://vimsky.com/zh-tw/examples/detail/python-ex-pykml.parser---fromstring-function.html)及[Python fromstring Examples](https://python.hotexamples.com/examples/pykml.parser/-/fromstring/python-fromstring-function-examples.html)
  - 因為MultiGeometry的順序和Placemark是一樣的，因此只要知道tag在MultiGeometry 序列中的序號，就可以知道它的名稱。(line 21~22)  

```python
17	lon,lat,num,nam=[],[],[],[]
18	n=0
19	for plg in plgs:
20	  iplg=plgs.index(plg)
21	  imtg=mtg_tag.index(plg_prt[iplg])
22	  name=names[imtg]
23	  coord=plg.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
24	  c=coord[0].pyval.split()
25	  for ln in c:
26	    if n%3==0:
27	      lon.append(ln.split(',')[0])
28	      lat.append(ln.split(',')[1])
29	      num.append('n='+str(n))
30	      nam.append(name)
31	    n+=1
```
- 將結果寫進`csv`檔案(`txt.write`版本)

```python
32	#with open('doc.csv','w') as f:
33	#  for i in range(len(num)):
34	#    f.write(str(lon[i])+','+str(lat[i])+','+str(num[i])+','+nam[i]+'\n')
35	#   if n%100==0:print(n)
```
- `DataFrame.to_csv`版本
  - 功能主要在將每一個座標點輸出成`csv`檔，而將其名稱寫在**點位**的說明欄，可以應用[csv2kml.py]()程式再次轉成`kml`檔案，檢視其**多邊形**及**名稱**解析是否正確。

```python
36	df=DataFrame({'lon':lon,'lat':lat,'num':num,'nam':nam})
37	df.set_index('lon').to_csv('doc.csv')
```
## 程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/land/gridmask/rd_kml.py)

## 應用
- 除了此處
## Reference
- google,**KML Tutoria**,[developers.google.com](https://developers.google.com/kml/documentation/kml_tut), Last updated 2021-09-07 UTC.
- wiki, **Keyhole標記語言**, [wiki](https://zh.wikipedia.org/wiki/KML), 2021年2月7日.
- Tyler Erickson, **pyKML v0.1.0 documentation**,[pythonhosted](https://pythonhosted.org/pykml/), 2011
- 純淨天空, **pykml.parser.fromstring函數**,[vimsky](https://vimsky.com/zh-tw/examples/detail/python-ex-pykml.parser---fromstring-function.html)
- contributors, **Python fromstring Examples**, [python.hotexamples](https://python.hotexamples.com/examples/pykml.parser/-/fromstring/python-fromstring-function-examples.html)