---
layout: default
title: Redistribution of Ship Emissions
parent: EDGAR Emission Processing
grand_parent: Global/Regional Emission
nav_order: 2
date: 2022-03-17 18:42:30
last_modified_date: 2022-03-17 18:42:34
---

# EDGARv5船隻排放空間分布之重分配
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
- 雖然EDGAR解析度0.1度與HUADON_3k的解析度已經相差不大，然而原生污染物如SO2、NO2等的模擬結果卻顯示出海上具有濃度分布的奇異點。
- 當風向與船隻路線有顯著交角是，突高的面源產生類似點源的效應，圖面上呈現出平行的煙流，而不是均勻的片狀線源貢獻之濃度分布。
- 造成此一結果的主要原因是EDGAR在同一路線上的排放量本身就具有很大的差異性，當程式進行內插時就很難避免加深此一差異而造成路線上的不連續結果。
- 解決方式
  - 以照片處理技巧拉大路線及非路線排放量的差距([Noise Removal of a Raster Data](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/noise_removal/))。可以消除公海部分的零星排放量，但不能增加路線上的排放量。
  - 參考[Extracting Road Vector Data from Raster Maps](https://www.researchgate.net/publication/227067853_Extracting_Road_Vector_Data_from_Raster_Maps)的作法將raster轉變成向量檔。但全球港埠設施逾萬處，燈塔更不計其數、還有內陸河流湖泊之水路，此舉無法短時間達成。
  - 重新以高解析度數據進行排放量的空間分配，例如歐洲水路的[交通密度圖](https://emodnet.ec.europa.eu/en/traffic-density-maps-better-understanding-maritime-traffic-0)。
    - 以一定範圍內的排放總量除以該範圍交通量總數得到比例，將排放量正比分配到高解析度網格、再合併到3公里網格。
    - 經嘗試錯誤，範圍太小(如EDGAR之0.1度網格)，還是無法解決不連續的情況，EDGAR排放量差異比交通密度差異更大。必須以整個HUADON_3k範圍總量方具有最佳效果。
    - 以歐洲範圍數據為1公里解析度、時間範圍則為逐月，似乎可行。

## 全球水路交通密度數據
- 經查世界銀行(World Bank WB))在其網站公開IMF分析歷年0.005度解析度（赤道處約為500m）之[船隻總密度數據](https://datacatalog.worldbank.org/search/dataset/0037580)，具有足夠的範圍與解析度
  - 船隻種類：共有商業、油氣、娛樂、漁船、客輪、以及總和等6個檔案。其中以商業佔絕大多數。
  - 數據時間自2015/1～2021/2。時間變化上較為不足。
  - 單位為AIS顯示在網格內出現的總次數，包括移動中與固定。
- 下載方式：該網站以java程式提供使用者點選，透過瀏覽器自動將zip檔案複製到使用者的Downloads目錄。再行解壓縮。
- 檔案格式：[GeoTiff](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)

## 程式說明
- 共有3支程式依序進行資料之轉檔、拮取及輸出成CMAQ所需格式。程式雖然沒有太多新的元素，轉接時仍然有些微差異，需予以注意。
  - [dens2nc.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/dens2nc.py)這支程式負責解讀[世銀船隻密度檔](https://datacatalog.worldbank.org/search/dataset/0037580)並切出D6範圍之數據另存成nc(CF-1.0格式)檔案，用[meteoInfo]()檢視。
  - [TNR2WBDens.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/TNR2WBDens.py)讀取前述nc檔與EDGAR TNR_Ship逐月船舶排放推估結果進行0.005度解析度重新分配，同樣為CF-1.0格式檔案，用[meteoInfo]()檢視。
  - [EDGAR2cmaqD6.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/EDGAR2cmaqD6.py)將0.005度重新分配結果以合併方式納入HUADON_3k網格系統，轉成IOAPI格式以供CMAQ讀取。

### [dens2nc.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/dens2nc.py)程式說明
- 此程式可能是[GeoTiff](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/GeoTiff/)系列程式中最單純的一支。
- 調用[rasterio](https://rasterio.readthedocs.io/en/latest/)將tiff檔案讀取後，隨即取出符合D6範圍之經緯度數據，將其寫入預先準備好的模版即可。
- D6範圍：lon=100\~134，lat=15\~42，取最外圈之整數。

```python
...
mnx,mny=min([100,np.min(lon1)]),min([15,np.min(lat1)])
mxx,mxy=max([134,np.max(lon1)]),max([42,np.max(lat1)])
...
  ix=np.where((lon>=mnx)&(lon<=mxx))[0]
  iy=np.where((lat>=mny)&(lat<=mxy))[0]
  data1=data[iy[0]:iy[-1]+1,ix[0]:ix[-1]+1]
...
  try:
    nc[v][:,:]=data1[:,:]
    nc.close()
  except:
    print('fail filling '+k)
```  
- 模板使用[ncpdq與ncks](/Focus-on-Air-Quality/utilities/netCDF/ncks/#加長一個limited維度)反複交替來逐步擴大，其內容如下：

```python
netcdf DensGlobD6 {
dimensions:
  lat = UNLIMITED ; // (5400 currently)
  lon = 6800 ;
variables:
  float emi_so2(lat, lon) ;
    emi_so2:standard_name = "tendency_of_atmosphere_mass_content_of_sulfur_dioxide_due_to_emission" ;
    emi_so2:long_name = "Emissions of SO2 - " ;
    emi_so2:units = "kg m-2 s-1" ;
    emi_so2:cell_method = "time: mean (interval: 1 month,  31 days)" ;
    emi_so2:total_emi_so2 = "   9.96403e+008 kg/month" ;
    emi_so2:comment = " (see http://edgar.jrc.ec.europa.eu/methodology.php#12sou for the definitions of the single sources)" ;
  float lat(lat) ;
    lat:standard_name = "latitude" ;
    lat:long_name = "latitude" ;
    lat:units = "degrees_north" ;
    lat:comment = "center_of_cell" ;
  float lon(lon) ;
    lon:standard_name = "longitude" ;
    lon:long_name = "longitude" ;
    lon:units = "degrees_east" ;
    lon:comment = "center_of_cell" ;
```

### [TNR2WBDens.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/TNR2WBDens.py)程式說明
- 此程式進行範圍內排放量的重新分配。
- 排放量單位之處理
  - EDGAR排放量單位為Kg/s/m<sup>2</sup>
  - 由於加總範圍內的排放量過程將會使其失去intensive的特性，需考量EDGAR與WB檔案網格間距的差異，前者1個網格中可容納後者400個網格(=(0.1/0.005)<sup>2</sup>)。
  - 重新考量船隻網格密度權重後，排放量單位仍然可以保持是Kg/s/m<sup>2</sup>

```python
...
  EmsGlb=np.sum(np.array(nc[v][sJ10[0]:sJ10[-1]+1,sI10[0]:sI10[-1]+1]))*20*20
...
  nc[v1][:,:]=EmsGlb*RatDens[:,:]
  nc.close()
```
### [EDGAR2cmaqD6.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/EDGAR2cmaqD6.py)程式說明
- 此一程式與[EDGAR2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR2cmaqD2.py)很接近，但使用合併方式將0.005度小網格內之排放量予以平均，存到目標網格系統(HUADON_3k)網格內
- 與[reas2cmaqD1.py](/Focus-on-Air-Quality/Global_Regional_Emission/REAS/reas2cmaq/#reas2cmaqd1py程式說明)一樣使用使用[np.searchsorted](https://vimsky.com/zh-tw/examples/usage/numpy-searchsorted-in-python.html)找到新網格點在EDGAR座標系統的位置起迄點lat_ss及lon_ss。
- 使用np.mean而不是np.sum，是因為EDGAR排放量是intensive quantity.

```python
...
  for j in range(nrow):
    for i in range(ncol):
#Since the unit is in intensive mode, must take mean not sum
      zz=np.mean(var[ispec,lat_ss[j,i]:lat_ss[j+1,i+1],lon_ss[j,i]:lon_ss[j+1,i+1]],axis=(0,1))
      nc[vc][0,0,j,i]=zz/mw[v]*1000.*nc.XCELL*nc.YCELL
...      
```
## Results
### 比較內插與合併方式之成果

| ![EDG_Intp.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/EDG_Intp.PNG)|
|:--:|
| <b>griddata內插HUADON_3k範圍的SO<sub>2</sub>排放量（log<sub>10</sub> gmole/s/cell）</b>|
| ![EDG_Aggr.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/EDG_Aggr.PNG) |
| <b>重新分配後HUADON_3k範圍船舶的SO<sub>2</sub>排放量（log<sub>10</sub> gmole/s/cell）</b>| 

### 討論
- scipy.griddata內插應用在船舶路線這種高空間突兀性的數據，確實有其限制，原本0.1度的解析度已經不足，內插結果更出現不連續的分布奇異點。在高解析度的空品模擬時會發生嚴重的高、低估情形。
- 重新分配、以合併方式進行座標系統轉換，仍然可以維持線形的特性，即使有差異，也是段落間的差異，不會出現網格點的奇異值。
- 數量級可以保持一致、EDGAR原始數據在內陸水域、黃海、東海與日韓間海峽分布有嚴重低估、香港向南方向與巴士海峽則有高估的情形，可能引用到較舊的AIS數據。

## Reference
- Diego A. Cerdeiro, Andras Komaromi, Yang Liu, and Mamoon Saeed, **World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based Nowcasts from Scratch**, [IMF paper](https://www.imf.org/en/Publications/WP/Issues/2020/05/14/World-Seaborne-Trade-in-Real-Time-A-Proof-of-Concept-for-Building-AIS-based-Nowcasts-from-49393), May 14, 2020 

