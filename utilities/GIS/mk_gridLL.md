---
layout: default
title: 行政區範圍格點化
parent: GIS Relatives
grand_parent: Utilities
date: 2023-02-06
last_modified_date: 2023-02-06 10:55:57
tags: choropleth GIS
---

# 行政區範圍格點化
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

- 嚴格來說，這一篇應該不是放在GIS而是繪圖區(Graphics/NCL)，因為所處理的檔案(gridLL.csv)只是為NCL繪製[choropleth](../Graphics/NCL/choropleth.md)圖所需要的一個前處理檔。使用的程式[mk_gridLL.py][mk_gridLL.py]及產生公版模式格點鄉鎮名稱檔，也是放在NCL目錄下。
- 然因為使用了shapely模組，所以技術上會歸併在GIS類別，與[shape_to_raster](shape_to_raster.md)是很類似的作業，只是靠著geojson資料庫與shapely模組，大大提升了程式碼的簡潔特性。
- 簡言之，之前式直接處理shape檔案，而這個版本是處理geojson檔，有較多的支援。
- 過去相關程式如[mk_town.py][1]、[mk_townNew.py][2]詳[shape_to_raster](shape_to_raster.md)及[CAM-chem模式結果之校正](../../AQana/GAQuality/NCAR_ACOM/2.correct.md)應用
- 同樣是前處理，將2維點陣線性化成為1維的工作表、以CSV儲存，似乎較符合直覺。

## 程式說明

### IO's

- 作業目錄：`/nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001`
- 引數：無
- 網格模板
  - 不限制是哪個範圍區位或解析度，只是要能夠與geojson檔匹配
  - 如此處為tempTW.nc，為公版台灣範圍，然解析度為1公里
- geojson檔案：為內政部TOWN_MOI_1090727.shp轉成之geo.json檔。
- 輸出檔案：gridLL.csv(如下)

```bash
            LAT         LON                                          Point  TOWNCODE COUNTYCODE COUNTYNAME TOWNNAME
3746  21.896349  120.859967   POINT (120.85996721123759 21.89634893493374)  10013040      10013        屏東縣      恆春鎮
4021   21.90574  120.850031   POINT (120.85003131220148 21.90574036131661)  10013040      10013        屏東縣      恆春鎮
```

### 網格設定

- 將(y,x)之經緯度拉成1維的資料表，在用shapely的Point定義備用。

```python
name='tempTW.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
X=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
Y=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x,y=np.meshgrid(X, Y)
x=x.flatten();y=y.flatten()
lon, lat = pnyc(x, y, inverse=True)
df=pd.DataFrame({'LAT':lat,'LON':lon})
df['Point']=[Point(i,j) for i,j in zip(lon,lat)]
ndf=len(x)
```

- 此處的模板檔案並未限定解析度、因此適用於任何網格座標系統。但是前提是座標參數之相關屬性必須是正確的。
- 因為IO都沒有網格名稱、解析度等等標記，使用者必須自行紀錄
  - LGHAP的解析度是1 Km
  - 公版模式解析度是3Km

### 行政區邊界線與ID之定義

- geopandas能將複雜的shape檔內容，簡化成資料表，不論是單一或多個多邊形，在其資料表中只是一個單元gdf.geometry[:]。
- 其內容如下

```python
root='/nas1/Data/GIS/TWN_town/'
gdf = gpd.read_file(root+'TOWN_MOI_1090727_geo.json')
ngdf=len(gdf);ndf=len(df)
```

```bash
In [524]: gdf.head()
Out[524]:
  TOWNID  TOWNCODE COUNTYNAME TOWNNAME             TOWNENG COUNTYID COUNTYCODE                                           geometry
0    V02  10014020        臺東縣      成功鎮  Chenggong Township        V      10014  POLYGON ((121.40996 23.21351, 121.40988 23.213...
1    T21  10013210        屏東縣      佳冬鄉    Jiadong Township        T      10013  POLYGON ((120.57660 22.45775, 120.57655 22.457...
2    P13  10009130        雲林縣      麥寮鄉    Mailiao Township        P      10009  POLYGON ((120.29898 23.74093, 120.29898 23.741...
3    V11  10014110        臺東縣      綠島鄉      Ludao Township        V      10014  MULTIPOLYGON (((121.49155 22.67746, 121.49171 ...
4    V16  10014160        臺東縣      蘭嶼鄉      Lanyu Township        V      10014  MULTIPOLYGON (((121.61180 21.94290, 121.61236 ...
```

### 串連搜尋

- 使用網格點之迴圈一一找出正確的行政區代碼(此處為gdf.TOWNCODE)
- shapely的點Point本身就帶有within()的[函數](https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html)，其引數為(單一或多個)多邊形

```python
townid=[]
for i in range(ndf):
  found=0
  for j in range(ngdf):
    if df.Point[i].within(gdf.geometry[j]):
      townid.append(gdf.TOWNCODE[j])
      found=1
      break
  if found==0:townid.append('00000000')
df['TOWNCODE']=townid
```

### 整併與輸出

```python
tn={i:j for i,j in zip(gdf.TOWNCODE, gdf.TOWNNAME)}
cn={i:j for i,j in zip(gdf.COUNTYCODE, gdf.COUNTYNAME)}
cn.update({'00000':'海'})
tn.update({'00000000':'海'})
df['COUNTYCODE']=[i[:5] for i in df.TOWNCODE]
df['COUNTYNAME']=[cn[i] for i in df.COUNTYCODE]
df['TOWNNAME']=[tn[i] for i in df.TOWNCODE]
df.set_index('LAT').to_csv('gridLL.csv')
```

### 程式下載

{% include download.html content="行政區範圍格點化前處理程式[mk_gridLL.py][mk_gridLL.py]" %}

[mk_gridLL.py]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/mk_gridLL.py

[1]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/mk_town.py "mk_town.py"
[2]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/mk_townNew.py "mk_townNew.py"