---
layout: default
title: geoplot行政區範圍等值圖
parent: matplotlib Programs
grand_parent: Graphics
date: 2023-05-30
last_modified_date: 2023-05-30 09:34:02
tags: geoplot graphics choropleth
---

# geoplot繪製行政區範圍等值圖
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

- 以行政區為等值圖範圍的數據圖稱之為[choropleth](https://en.wikipedia.org/wiki/Choropleth_map)，為模式重要的後處理形式之一。
- 以[NCL（NCAR Command Language）](https://www.ncl.ucar.edu/)的網站服務方式([CaaS](http://125.229.149.182/chrpleth.html))，提供之解決方案如[NCL/choropleth](../NCL/choropleth.md)所示，仍有不足之處:
  1. 系統複雜，維護困難
  2. NCL語言難以接近、且不再更新版次令人擔憂
  3. 圖面顏色與畫質不佳
- 此處方案以[geoplot](https://ithelp.ithome.com.tw/articles/10204839)模組呼叫matplotlib、geopandas等一般性之python模組進行繪製
- 以下範例為逐日鄉鎮區平均之PM2.5濃度，程式繪製第一天為範例

```bash
In [101]: !head /nas2/cmaqruns/2019TZPP/output/Annual/LGHAP.PM25.D001/LGHAP2000.csv
YMD,TOWNCODE,PM25,COUNTYCODE,COUNTYNAME,TOWNNAME
20000101,00000000,33.14068672605491,00000,海,海
20000101,09020060,39.95062808936716,09020,金門縣,烏坵鄉
20000101,10002010,38.522622542882246,10002,宜蘭縣,宜蘭市
20000101,10002020,36.53720380192809,10002,宜蘭縣,羅東鎮
20000101,10002030,29.987197758109986,10002,宜蘭縣,蘇澳鎮
20000101,10002040,30.892525514286056,10002,宜蘭縣,頭城鎮
20000101,10002050,33.41653338736951,10002,宜蘭縣,礁溪鄉
20000101,10002060,37.81242251930676,10002,宜蘭縣,壯圍鄉
20000101,10002070,33.260458754091715,10002,宜蘭縣,員山鄉
```

|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-05-30-10-51-07.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-05-30-09-47-27.png)|
|:-:|:-:|
|<b>NCL版本之等值圖</b>|<b>geoplot版本之等值圖</b>|


## geoplot安裝

- 可以參考[官網](https://residentmario.github.io/geoplot/installation.html)下載說明
- 經測試
  - conda未成功，猜測公司會擋conda-forge網站
  - pip 可以安裝，但須較高階版本python，此處是3.11.3版(官網只要求>=3.7)
- 程式還需要其他如shapely、geopandas等

## 程式設計重點

### IO's

- 2個引數
  1. 要繪製的項目名稱(在csv中的欄位名稱)，會認大小寫
  2. csv檔案名稱
     1. 一般的pandas.DataFrame。
     2. 必須有TOWNCODE欄位。其內容可以是整數，程式會自動轉成8碼的字串
- 內政部鄉鎮區分界檔
- 輸出
  - 目前程式只提供圖面檢視

### shape檔的切割

- 因此次繪圖只限本島範圍，外島、離島等予以篩除，此處直接以within函數刪除框限範圍外的內容。
- 詳見[matplot 中文化問題#鄉鎮區名稱及邊界之繪製](https://sinotec2.github.io/FAQ/2023/05/29/matplotlib_ttf.html#鄉鎮區名稱及邊界之繪製)的討論。

```python
# domain of figure
x,y=[119.9,122.4,122.4,119.9,],[21.5,21.5,25.5,25.5,]
Frame=shapely.geometry.Polygon([shapely.geometry.Point(i,j) for i,j in zip(x,y)])

#town_moi shape file loading and screening
shp_path = '/nas1/Data/GIS/TWN_town/TOWN_MOI_1120317.shp'
twn=gpd.read_file(shp_path)
twn=twn.loc[twn.geometry.map(lambda p:p.within(Frame))]
```

### 資料檔合併

- geoplot只會讀取geopandas檔案。
- 經考慮最後鄉鎮區對照關係，內政部檔案較新，使用者提供csv檔案可能有些鄉鎮區會對照不到，因此以前者為準，將後者的內容正確附在表格最右欄。
- 使用dict技巧，不逐一比對

```python
lastTwn=sTOWNCODE & set(df.TOWNCODE)
twn=twn.loc[twn.TOWNCODE.map(lambda s:s in lastTwn)]
df=df.loc[df.TOWNCODE.map(lambda s:s in lastTwn)].reset_index(drop=True)
if len(df)>len(lastTwn):
  df=df[:len(lastTwn)]
df_itm={i:0 for i in twn.TOWNCODE}
df_itm.update({i:j for i,j in zip(list(df.TOWNCODE),list(df[itm_nam]))})
twn[itm_nam]=[df_itm[i] for i in twn.TOWNCODE]
```

### 繪圖

- geoplot.choropleth函數需要geopandas的2個欄位，shape檔中的(眾)多邊形、以及對應的數值
  - 顏色cmap
  - 是否有色標(legend)
  - 其他選項詳官網[說明](https://residentmario.github.io/geoplot/api_reference.html?highlight=choropleth#geoplot.geoplot.choropleth)

```python
#plotting
proj = gcrs.AlbersEqualArea(central_latitude=24.5, central_longitude=120)
f=plt.figure(figsize=(15, 13))
ax=plt.axes(projection=proj)
if '/' in fname:
  fname=fname.split('/')[-1]
plt.title(itm_nam+' in '+fname, fontsize=16)
gplt.choropleth(
        twn.loc[:, [itm_nam, 'geometry']],
        hue=itm_nam, cmap='rainbow', #cmap='Blues',
        linewidth=0.0, ax=ax,
        legend=True,
    )
gplt.polyplot(
        twn, edgecolor='black', linewidth=0.5, ax=ax,
    )
plt.show()
```

## 程式下載

{% include download.html content="[csv_choro.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/matplotlib/csv_choro.py)" %}
