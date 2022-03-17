---
layout: default
title:  python解析GML檔
parent: GIS Relatives
grand_parent: Utilities
last_modified_date:   2021-12-21 16:51:07
---
# python解析GML檔
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
- **GML**([Geography Markup Language](https://zh.wikipedia.org/wiki/地理标记语言)是臺灣地區的鄉鎮區界檔案格式，也是[Open GIS社群](https://zh.wikipedia.org/wiki/开放地理空间协会)通用的格式。
- 此處目標設定將GML檔案轉寫成raster檔。raster檔案在空品模擬系統之功用詳見[python解析KML檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/)之背景說明。
- 目標raster解析度範圍為`d4`，`GML`雖然跟`KML`有很大的差別，但處理程序有很高的相似性。

### 目標
- 建立範圍解析度(d4) raster的值(整數分區代碼)

### 樣式範例
- 檔案來源：[鄉鎮市區界線(TWD97經緯度)](https://data.gov.tw/dataset/7442))

```html
<行政區域界線 xmlns="http://standards.moi.gov.tw/schema/pub" xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ngis_primitive="http://standards.moi.gov.tw/schema/ngis_primitive" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:gco="http://www.isotc211.org/2005/gco" xmlns:utility="http://standards.moi.gov.tw/schema/utility" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://standards.moi.gov.tw/schema/pub pub.xsd">
  <gml:metaDataProperty>
    <ngis_primitive:NGIS_Primitive>
      <ngis_primitive:資料描述>鄉鎮市區界線(TWD97經緯度)</ngis_primitive:資料描述>
      <ngis_primitive:坐標參考系統識別碼>
        <gmd:RS_Identifier>
          <gmd:code>
            <gco:CharacterString>EPSG:3824</gco:CharacterString>
          </gmd:code>
        </gmd:RS_Identifier>
      </ngis_primitive:坐標參考系統識別碼>
      <ngis_primitive:坐標參考系統定義 xlink:herf="http://standards.moi.gov.tw/schema/epsg/3824.xml" />
      <ngis_primitive:資料內容對應時間>
        <gml:TimeInstant>
          <gml:timePosition indeterminatePosition="after">109-07-21</gml:timePosition>
        </gml:TimeInstant>
      </ngis_primitive:資料內容對應時間>
    </ngis_primitive:NGIS_Primitive>
  </gml:metaDataProperty>
  <gml:featureMember>
    <PUB_行政區域>
      <名稱>臺東縣成功鎮</名稱>
      <涵蓋範圍>
        <gml:MultiPolygon>
          <gml:polygonMember>
            <gml:Polygon>
              <gml:outerBoundaryIs>
                <gml:LinearRing>
                  <gml:coordinates>121.40981573700003,23.213692785000092 121.40984267700003,23.213661019000085 ...</gml:coordinates>
                </gml:LinearRing>
              </gml:outerBoundaryIs>
            </gml:Polygon>
          </gml:polygonMember>
        </gml:MultiPolygon>
      </涵蓋範圍>
      <行政區域代碼>10014020</行政區域代碼>
      <比例尺分母>5000</比例尺分母>
      <行政區域設置時間 />
    </PUB_行政區域>
  </gml:featureMember>
  <gml:featureMember>
    <PUB_行政區域>
      <名稱>屏東縣佳冬鄉</名稱>
      <涵蓋範圍>
        <gml:MultiPolygon>
          <gml:polygonMember>
...
 120.99327470700021,24.780576327000048</gml:coordinates>
                </gml:LinearRing>
              </gml:innerBoundaryIs>
            </gml:Polygon>
          </gml:polygonMember>
        </gml:MultiPolygon>
      </涵蓋範圍>
      <行政區域代碼>10004100</行政區域代碼>
      <比例尺分母>5000</比例尺分母>
      <行政區域設置時間 />
    </PUB_行政區域>
  </gml:featureMember>
</行政區域界線>
```

### 方案與檢討
- `python`並沒有針對`GML`發展特殊的**parser**，如果用**eTree**來解讀，還算方便。但因為多邊形多達1036筆(群島)，再加上d4高解析度(由1公里加總成3公里)，因此須解決迴圈太多的問題。

## GML檔案之讀取
- `GML`是open GIS的共通語言，但相關軟體和討論似乎並不是很普遍。
- 以下為應用`etree`解讀的範例

### GML檔案來源
- 檔案`TOWN_MOI_1090727.gml`：由[TGOS](https://www.tgos.tw/TGOS/Web/Metadata/TGOS_MetaData_View.aspx?MID=DA2C058E0BB0C85B80938EE2671C4453&SHOW_BACK_BUTTON=false&keyword=TW-07-301000100G-614001)網站下載。
- **中文**問題：此處為方便並沒有直接使用**中文**來搜尋，而是用嘗試錯誤法找出下列標籤。
  - xzqy：「**行政區域**」(為字串序44以後)
  - xzqudm：行政區域代碼(為新的8碼)，為序列中第2項。

### [rd_gml.py](https://github.com/sinotec2/cmaq_relatives/blob/master/land/gridmask/rd_gml.py)程式說明
- GML雖然是open GIS的共通語言，但相關軟體和討論似乎並不是很普遍。還好etree還可以讀取。
  - 獲取檔案的`rootElement`

```python
     1  import xml.etree.cElementTree as ET
     2  from pandas import *
     3
     4  rootElement = ET.parse("TOWN_MOI_1090727.gml").getroot()
```
- 次元件標籤中含有「**行政區域**」(`xzqy`)4個中文字，如果字串中有此4個中文字，則讀取「**行政區域代碼**」6個中文字(`xzqydm`)

```python
     5  s=set()
     6  for subelement in rootElement.getiterator():
     7    for subsub in subelement:
     8      s=s|set([subsub.tag])
     9  s=list(s)
    10  s.sort()
    11  xzqy=s[5][44:]
    12  xzqydm=[i for i in s if xzqy in i][1]
```
- 讀取所有鄉鎮區的代碼`all_town`

```python
    13  all_town=set()
    14  for subelement in rootElement.getiterator():
    15    for subsub in subelement:
    16      if xzqydm == subsub.tag:
    17        all_town=all_town|set([subsub.text])
    18  all_town=list(all_town)
    19  all_town.sort()
```
- 20~31：將多邊形座標讀出，存到`wkt`序列，共1036筆。
- 

```python    
    20  twnid={}
    21  isq=0
    22  wkt=[]
    23  for subelement in rootElement.getiterator():
    24    for subsub in subelement:
    25      if xzqydm == subsub.tag:tid=subsub.text
    26      if subsub.tag == "{http://www.opengis.net/gml}coordinates":
    27        x = subsub.text
    28        point_for_pol =[(float(i.split(',')[0]),float(i.split(',')[1])) for i in x.split()]
    29        wkt.append(point_for_pol)
    30        twnid.update({isq:tid})
    31        isq+=1
    32
```
- 鄉鎮區名稱`TOWN_MOI_1090727E.csv`：由[開放平台](https://data.gov.tw/dataset/7441)下載，去掉中文字以簡化過程，用代碼勾串。

```python
    33  df_twn=read_csv('TOWN_MOI_1090727E.csv')
    34  ii=[int(twnid[i]) for i in range(len(twnid))]
```
- 儲存：存成`csv`檔，序列存在`csv`中會變成很長的字串，要調用會有一點麻煩(詳下)，但因為概念架構上比較方便，也就將就了。

```python
    35  df=DataFrame({'twnid':ii,'lonlats':wkt})
    36  TOWNENG={i:j for i,j in zip(df_twn.TOWNCODE, df_twn.TOWNENG)}
    37  df['TOWNENG']=[TOWNENG[i] for i in df.twnid]
    38  df.set_index('twnid').to_csv('polygons.csv')
```

### str2lst
- DataFrame儲存格如果是一個字串，要改成序列，可以參考下列片段：

```python
def str2lst(A):
    return [float(i) for i in A[1:-1].split(',')]
```

## 程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/land/gridmask/rd_kml.py)

## Reference
- wiki, **地理标记语言**, [wiki](https://zh.wikipedia.org/wiki/%E5%9C%B0%E7%90%86%E6%A0%87%E8%AE%B0%E8%AF%AD%E8%A8%80), 2021年3月1日