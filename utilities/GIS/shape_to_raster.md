---
layout: default
title:  shape_to_raster
parent: GIS Relatives
grand_parent: Utilities
last_modified_date:   2021-12-21 14:46:36
---

# shape files convert to rasters
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
### 目標
- 本次作業的目標在於將內政部([MOI](https://data.moi.gov.tw/MoiOD/Data/DataContent.aspx?oid=CD02C824-45C5-48C8-B631-98B205A2E35A)鄉鎮區界的`shape`檔，讀成`d5`範圍**1公里**解析度的`raster`檔(`ioapi nc`格式)備用。

### 方案考量
- `shape file`的讀取方式有很多種(詳參[GIS Stack Exchange](https://gis.stackexchange.com/questions/113799/how-to-read-a-shapefile-in-python))，大多藉由[gdal程式庫](https://ithelp.ithome.com.tw/articles/10215163)。
  - 然而因`gdal`套用其他軟體相依性太高，太過複雜，裝設不易，且有記憶體容量之限制。
  - 一般寫出方法以`tiff`為主，目前尚沒有`nc`的現成套件。
- 此處選擇直讀式的[PyShp](https://pypi.org/project/pyshp/)，其裝置、使用範例可以參考[PyPi官網](https://pypi.org/project/pyshp/)。
  - [PyShp](https://pypi.org/project/pyshp/)的弱點在沒有現成的寫出方法可以套用，必須另外自行撰寫。
  - 然因作業所要求格式對GIS領域而言過於冷僻，因此勢必無法規避自行撰寫。
  - **vector to raster**的核心是網格點是否在多邊形之內的判定(`within`)，可以調用[shapely](https://shapely.readthedocs.io/en/stable/manual.html)的程式庫，詳官網說明及及[python解析KML(GML)檔](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/)範例。
- `kml`也可以轉成`raster`，一般`shp`向量檔也有`kml`形式儲存備用的。然而`kml`的轉檔需執行[rd_kml](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/)及[withinD1]()等檔案讀取與寫出2個步驟，似過於繁瑣。此處予以整併。

### 檔案IO及格式說明
- `shape` 檔：（輸入）`TOWN_MOI_1090727.shp` 來自[MOI官網](https://data.moi.gov.tw/MoiOD/Data/DataContent.aspx?oid=CD02C824-45C5-48C8-B631-98B205A2E35A)
- `nc`檔：（輸入及輸出）模版`template_d5_1x1.nc`及最終結果(同名)
- `csv`檔：（輸出）鄉鎮區屬性內容

## [withinD5.py](https://github.com/sinotec2/cmaq_relatives/blob/master/land/gridmask/withinD5.py)程式設計重點

### shape檔屬性內容之讀取與紀錄
- 基本上`shape`檔的骨幹也是以`dict`型式儲存多邊形座標點，其屬性內容儲存在`fields`內，如下所示。
- 以[MOI](https://data.moi.gov.tw/MoiOD/Data/DataContent.aspx?oid=CD02C824-45C5-48C8-B631-98B205A2E35A)檔案而言，共有7個`fields`，將其作成`DataFrame`的`columns(col)`，
  - 每個鄉鎮區紀錄(`rec`)前7項記住了各區的名稱代碼等。
  - 雖然是`dict`，但`shape`檔案的`fields`紀錄仍然是按照順序排列的。

```python
    28  shp='TOWN_MOI_1090727.shp'
    29  shape = shapefile.Reader(shp)
    30  f=shape.fields
    31  rec=shape.records()
    32  col=[i[0] for i in f[1:]]
    33  df=DataFrame({col[ic]:[rec[i][ic] for i in range(len(rec))] for ic in range(7)})
    34  df.to_csv('record.csv')
```

### 多邊形**個數**之區分
- 由於鄉鎮區範圍可能是接壤的**單一多邊形**、或者不連續、**多個多邊形**，
  - **單一多邊形**處理較為單純且佔多數，**多個多邊形**較為複雜但個數較少。在迴圈的設計上分別處理。
  - 先記錄前者(調用`shape.__geo_interface__['coordinates']`)及`multi`標籤。
  - `plgs`順序必須保持跟`df`相同，`multi`則不必。
- 在`multi`之24個個案中，[MOI](https://data.moi.gov.tw/MoiOD/Data/DataContent.aspx?oid=CD02C824-45C5-48C8-B631-98B205A2E35A)格式略有不同，原因不明。
  - 經嘗試錯誤發現，有的是2層套疊`list`，有的是單層，必須探究哪一層才是經緯度`tuple`，以此來判別。
  - 先將多個多邊形`lump`成一個序列(第46~48行)、保持正確的格式、能夠計算`Polygon.bounds`就好，後面會再依照多邊形個數依序讀取、判別`within`。

```python
    36  plgs,multi=[],[] #(lon,lat)
    37  for i in range(len(df)):
    38    tp=shape.shapeRecords()[i].shape.__geo_interface__['type']
    39    cr=shape.shapeRecords()[i].shape.__geo_interface__['coordinates']
    40    if len(cr)!=1:
    41      multi.append(i)
    42      if type(cr[0][0][0])==tuple:
    43        crs=[cr[ic][0][:] for ic in range(len(cr))]
    44      else:
    45        crs=[cr[ic][:] for ic in range(len(cr))]
    46      plg=[]
    47      for cr in crs:
    48        plg+=cr
    49      plgs.append(plg)
    50    else:
    51      plgs.append(cr[0])
```

### 經緯度轉置與邊界範圍
- [MOI](https://data.moi.gov.tw/MoiOD/Data/DataContent.aspx?oid=CD02C824-45C5-48C8-B631-98B205A2E35A)座標是(經度、緯度)，`shaple`約定是(緯度、經度)，順序相反

```python
    52  Dplg=[] #(lat,lon)
    53  for plg in plgs:
    54    lon=[i[0] for i in plg[:]]
    55    lat=[i[1] for i in plg[:]]
    56    crd=[(i,j) for i,j in zip(lat,lon)]
    57    Dplg.append(crd)
```

- 記錄多邊形邊界經緯度的範圍

```python
    58  mnLat,mnLon,mxLat,mxLon=[np.array([Polygon(plg).bounds[i] for plg in Dplg]) for i in range(4)]
```

### 單一多邊形within之判別
- 對每一個網格點進行判別，共有(414, 252)點，大多為海上點。
- 由於鄉鎮區總數368，很多是在多邊形範圍外，因此必須進行座標的篩選，
- 經測試，`np.where`會比`within`更快
  - 此處做緯度、經度2次`np.where`判別
  - 如果n屬於`multi`多個多邊形個案，必須每一個多邊形判別，不在此處理。

```python
    59  nplgs=len(df)
    60  DIS=np.zeros(shape=(nrow2,ncol2))
    61  for j in range(nrow2):
    62    for i in range(ncol2):
    63      p1=Point((Plat[j,i],Plon[j,i]))
    64      idx=np.where((Plat[j,i]-mnLat)*(Plat[j,i]-mxLat)<=0)
    65      if len(idx[0])==0: continue
    66      idx2=np.where((Plon[j,i]-mnLon[idx[0][:]])*(Plon[j,i]-mxLon[idx[0][:]])<=0)
    67      if len(idx2[0])==0: continue
    68      for n in list(idx[0][idx2[0]]):                                              #loop for each polygons
    69        if n in multi:continue
    70        poly = Polygon(Dplg[n])
    71        if p1.within(poly):        #boolean to check whether the p1 coordinates is inside the polygon or not
    72          DIS[j,i]=float(n)
    73          break
```

### 多個多邊形within之判別
- 此處以鄉鎮區為主要的迴圈，針對網格點進行篩選，符合邊界範圍條件網格才進行within判別
  - 3層迴圈順序、由外而內分別為：鄉鎮區->多邊形->網格點
  - 因前述plgs將所有多邊形lump在一起，within判別會出錯，必須重新讀取shape檔、依序判別同一鄉鎮區的多個多邊形。
  - 同樣進行層次的確認（78~81行）、與經緯度的轉置(83~85行)

```python  
    74  for n in multi:
    75    idx=np.where((Plat-mnLat[n])*(Plat-mxLat[n])<=0)
    76    idx2=np.where((Plon[idx[0][:],idx[1][:]]-mnLon[n])*(Plon[idx[0][:],idx[1][:]]-mxLon[n])<=0)
    77    cr=shape.shapeRecords()[n].shape.__geo_interface__['coordinates']
    78    if type(cr[0][0][0])==tuple:
    79      plgs=[cr[ic][0][:] for ic in range(len(cr))]
    80    else:
    81      plgs=[cr[ic][:] for ic in range(len(cr))]
    82    for plg in plgs:
    83      lon=[i[0] for i in plg[:]]
    84      lat=[i[1] for i in plg[:]]
    85      crd=[(ii,jj) for ii,jj in zip(lat,lon)]
    86      for ij in range(len(idx2[0])):
    87        j=idx[0][idx2[0][ij]]
    88        i=idx[1][idx2[0][ij]]
    89        p1=Point((Plat[j,i],Plon[j,i]))
    90        poly = Polygon(crd)
    91        if p1.within(poly):  #boolean to check whether the p1 coordinates is inside the polygon or not
    92          DIS[j,i]=float(n)
```

### 模版製作並輸出檔案
- 由於nc檔案只能變動`unlimited dimension`，因此必須先將`rec_dmn`設成`ROW`及`COL`，
- 第一次要在各維度依序展開(107~110行)
  - 以後只要維度相同，可以一次倒入數據，但是bound要設好(112行)
  - 只要一個變數及`TFLAGS`，其餘變數不必留存
  - 使用`ncrename`程式將變數`NO`成`NUM_TOWN`

```python  
    94  #ncks -O --mk_rec_dmn ROW template_d5_1x1.nc a.nc
    95  #ncks -O --mk_rec_dmn COL b.nc c.nc
    96  #ncks -O -v NO,TFLAG -d TSTEP,0 c.nc template_d5_1x1.nc
    97  #ncrename -v NO,NUM_TOWN $nc
    98  nc = netCDF4.Dataset('template_d5_1x1.nc', 'r+')
    99  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  100  nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
  101  nc.NCOLS=ncol2
  102  nc.NROWS=nrow2
  103  nc.NVARS=1
  104  nc.NSTEPS=1
  105  nc.XCELL=RESm
  106  nc.YCELL=RESm
  107  if nrow!=nrow2 or ncol!=ncol2:
  108    for j in range(nrow2):
  109      for i in range(ncol2):
  110        nc.variables['NUM_TOWN'][0,0,j,i]=DIS[j,i]
  111  else:
  112    nc.variables['NUM_TOWN'][0,0,:nrow,:ncol]=DIS[:,:]
  113  nc.close()
```

## ToDo
- 空間模版改變時注意事項
  - 中心點位置：(YCENT及XCENT)程式（line 9）與nc檔案都會有，應以後者為主，須調整line 9與line 13讀取的順序
  - 此處以模版範圍為主，沒有其他定義
  - 網格數：由程式自行計算，也無需另外定義。
  - 解析度：@line 20~23, 105~106
- shape檔結構、格式的Try and Err
  - 同一序號，多個多邊形。不見得其他的shape檔也是此一結構。
  - 多個多邊形、不同序列層次套疊。

## codes
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/land/gridmask/withinD5.py)

## Resource
### links
- disscussion, **How to read a shapefile in Python?**, [Stack Exchange](https://gis.stackexchange.com/questions/113799/how-to-read-a-shapefile-in-python), Sep 28 2018.
- jlawhead, **PyShp 2.1.3**, [pypi](https://pypi.org/project/pyshp/), Jan 14, 2021
- Henrikki Tenkanen, **Point in Polygon & Intersect**, [github.io](https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html), Jan 17, 2018.
- Sean Gillies, **Shapely 1.8.0** [pypi](https://pypi.org/project/Shapely/), Oct 26, 2021
- Sean Gillies, **The Shapely User Manual**, [readthedocs](https://shapely.readthedocs.io/en/stable/manual.html), 
Dec 10, 2021

### notes
- [python解析KML(GML)檔案](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/)