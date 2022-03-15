---
layout: default
title:  鏈結資訊之地圖展現(uMap)
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-03-11 15:46:30
---

# 鏈結資訊之地圖展現(uMap)
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
- 點狀資訊之地圖展現，即按照地圖上地標來尋找標的物，是最接近直覺的互動體驗。除了提供地圖上的參考物件之外，所欲提供的物件（Points Of Interest POI's）也必須清楚有效的呈現，以便使用者點選、下載、或其他進一步動作。
- POI應用實例有2種，包括簡單的點狀資訊、以及格狀之鏈結資訊。此處介紹後者，應用在MMIF與AERMAP結果的提供。

### 方案比較
- 傳統做法
	- 以ftp層級提供：為最簡便之方案。然而由於網格點是空間相對意義的一組數字，作為ftp的檔名難以對使用者產生意義。
	- 提供行政區位之網頁界面，以工廠所在行政區階層下拉選單點選：選單太多選取不易、選錯空間位置會差很大。
	- 以個別點URL提供，利用Google 地圖或OSM平台：格式如[openstreetmap說明](https://www.openstreetmap.org/?mlat=51.107686&mlon=17.062196&zoom=8#map=6/51.014/17.556)
- GIS作法
	- QGIS
		- 將連結的內容寫成shapefile的某個屬性，
		- 藉由qgis2web (qgis2leaflet)外部插件，將地圖寫在index.html內，也可供外界瀏覽（自行架設網站，見[範例](http://www.qgistutorials.com/zh_TW/docs/leaflet_maps_with_qgis2leaf.html)）。
	- ARCGIS
		- arcGIS Platform是一個免費PaaS，且支援豐富的UI，可將地圖做成各種平台的API形式以供查閱
		- 需要Token 才能修改，具有較高的安全性
		- 加入會員是免費，但是底圖瀏覽超過基本量（2百萬）以上，需要收費。
- 開放地圖做法
	- 以傳統kml檔案批次提供：在粗比例尺情況下格點太過密集，無法分辨，無從點選
	- [OpenLinkMap](https://wiki.openstreetmap.org/wiki/OpenLinkMap)
    - 這項2016～2017推出的專案構想很大、也很具有啟發性，但是後續沒有人繼續應用。
    - 最初的想法是在地圖上顯示wiki的連結，提供使用者想快速了解時，可以點選下去。
    - 可能不適合手機上的操作方式，連結也受限於其他網站的速度。
	- [FacilMap](https://facilmap.org/) 
    - 對具合作性質的工作團隊而言，讓彼此都知道設施的位置清單是很重要的，因此這項服務就順利承接了openLinkMap的構想，繼續發展成為共同協作的動態地圖。
		- 他們提供的不是連結，而是清單、滑鼠滑過或點選時就出現訊息，而不是進入另個網址連結。
		- FacilMap目前是已經進到第2版。
		- 除了使用者端的程式碼之外，開發者還提供了自行維運伺服器所需的程式與指引。對具有機密性質的協作地圖，有自己的伺服器是很有必要的。
	- [uMap](https://umap.openstreetmap.fr/)
    - 與FacilMap的功能很接近，FasilMap是js方案，uMap是django方案，同樣以圖層的方式來營運共同協作的動態地圖。
		- 最大的差別uMap有縮放的叢集（解散）能力，在圖示上較FacilMap清爽，對點數多的情況會有較佳的效果。
		- django伺服器方案有較快的速度
		- 有較完整說明、逐步教學、容易上手。
    - uMap完全是[opensource](https://github.com/umap-project/umap)，可以在自己的網站上重製修改

## 資料之準備與上載

### uMap的規格與選項
- uMap可以接受上傳檔案、URL連結、或者是直接在對話框貼上POI之文字。
	- 末者應為少量資訊、測試過程提供的界面，不適用在大量的數據
	- URL可以在讓使用者隨時更動客戶端的內容保持協作地圖上的資訊是最新的、減少圖層更新的作業。應適用更新頻率較高的情況
	- 由於年度MMIF的執行屬於低頻度的批次作業，此處選擇上傳檔案。
- 除KML之外，uMap也可以接受GeoJSON、csv、gpx、osm、georss、umap(即umap的輸出檔、除POI內容外還包括圖層的設定)
	- csv適用在點狀資料，KML有點、線、多邊形較為彈性。
	- 由於5年5000多點數據還是需要有格式比較容易偵錯，此處以csv為優選。
	- [csv2kml](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/)為已經開發的小工具，因此kml也可以考慮。
	- 本次作業網格分布之位置如以點狀似嫌呆板，以網格邊界4方形較符合實際，然數據量也將擴增5倍，過去google map對上千點的kml速度降低很多、且有拒絕服務的限制，不知uMap是否也會(經證實不會)，因此以kml點狀先行測試，最終仍以4邊形來展示POI內容為目標。

### 資料之準備
- 自point_QC.csv(詳[read_point.py]()))中歸納出台灣地區已設有工廠的網格位置，另存成point_ij.csv，使用python程式如下：

```python
kuang@114-32-164-198 /Users/1.PlumeModels/AERMOD/mmif/TWN_3X3
$ cat -n point_ij.py
     1    from pyproj import Proj
     2    import numpy as np
     3    from pandas import *
     4    
     5    Latitude_Pole, Longitude_Pole = 23.61000, 120.990
     6    pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
     7            lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
     8    df=read_csv('point_QC.csv')
     9    df['II']=[int(i/3000+83/2) for i,j in zip(df.UTM_E,df.UTM_N)]
    10    df['JJ']=[int(j/3000+137/2) for i,j in zip(df.UTM_E,df.UTM_N)]
    11    boo=(df.II>=0) & (df.JJ>=0)
    12    dfij=df.loc[boo].reset_index(drop=True)
    13    dfij['IJ']=dfij.II*1000+dfij.JJ
    14    dfij['X']=(dfij.II- 83/2)*3000+1500
    15    dfij['Y']=(dfij.JJ-137/2)*3000+1500
    16    pv=pivot_table(dfij,index='IJ',values=['X','Y'],aggfunc=np.mean).reset_index()
    17    X,Y=np.array(pv.X),np.array(pv.Y);lon, lat= pnyc(X,Y, inverse=True)
    18    pv['lon']=[round(i,3) for i in lon]
    19    pv['lat']=[round(i,3) for i in lat]
    20    pv.set_index('IJ').to_csv('point_ij.csv')
```

其表頭如下：
```bash
kuang@114-32-164-198 /Users/1.PlumeModels/AERMOD/mmif/TWN_3X3
$ head point_ij.csv
IJ,X,Y,lon,lat
7152,-102000.0,252000.0,119.936,25.961
7159,-102000.0,273000.0,119.934,26.157
8159,-99000.0,273000.0,119.965,26.157
11048,-90000.0,-60000.0,120.082,23.047
12048,-87000.0,-60000.0,120.112,23.047
12054,-87000.0,-42000.0,120.111,23.215
13047,-84000.0,-63000.0,120.142,23.019
13048,-84000.0,-60000.0,120.142,23.047
13053,-84000.0,-45000.0,120.141,23.187
```
- IJ = I*1000 + J，為東西、南北向網格標籤的組合
- X,Y：lambert projection座標值，原點在台灣中心點
- 貼上連結位置之說明descriptions

```python
kuang@114-32-164-198 /Users/1.PlumeModels/AERMOD/mmif/TWN_3X3
$ cat mk_kml.py
from pandas import *
import os
pth='/Users/1.PlumeModels/AERMOD/mmif/TWN_3X3/'
df=read_csv(pth+'point_ij.csv')
A=[]
a='http://114.32.164.198/mmif_results/'
for ij in df.IJ:
    i=str(ij)
    s=''
    for y in range(16,21):
        yr='20'+str(y)
        for ext in ['.sfc ','.pfl ']:
            s+=a+yr+'/'+i+'/IJ'+i+ext
                     s+=a+yr+'/IJ'+i+'Y'+str(y)+ext 
    A.append(s)
df['lab']=A
df['IJ']=['IJ'+str(ij) for ij in df.IJ]
col=['lon','lat','IJ','lab']
df[col].set_index('lon').to_csv('mmifTWN_3X3.csv')
os.system('/opt/local/bin/csv2kml.py -f mmifTWN_3X3.csv -n N -g LL')
```
### kml成果

```html
$ head mmifTWN_3X3.csv.kml
<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">
<Document><name>mmifTWN_3X3.csv</name><description>mmifTWN_3X3.csv</description>
<Style id="normalPlacemark"><IconStyle><Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href> </Icon> </IconStyle></Style>
<Placemark><name>IJ7152</name><description>
http://114.32.164.198/mmif_results/2016/7152/IJ7152.sfc 
http://114.32.164.198/mmif_results/2016/7152/IJ7152.pfl 
http://114.32.164.198/mmif_results/2017/7152/IJ7152.sfc 
http://114.32.164.198/mmif_results/2017/7152/IJ7152.pfl 
http://114.32.164.198/mmif_results/2018/7152/IJ7152.sfc 
http://114.32.164.198/mmif_results/2018/7152/IJ7152.pfl 
http://114.32.164.198/mmif_results/2019/7152/IJ7152.sfc 
http://114.32.164.198/mmif_results/2019/7152/IJ7152.pfl 
http://114.32.164.198/mmif_results/2020/7152/IJ7152.sfc 
http://114.32.164.198/mmif_results/2020/7152/IJ7152.pfl 
</description><styleUrl>#normalPlacemark</styleUrl>
<Point><coordinates>
119.936,25.961,0</coordinates></Point></Placemark>
...
```
### 網格4邊形之製作

```python
kuang@114-32-164-198 /Users/1.PlumeModels/AERMOD/mmif/TWN_3X3
$ cat -n point_ijP.py
...
11 df=read_csv('mmifTWN_3X3.csv')
 12 lon2,lat2,nam2,lab2=([] for i in range(4))
 13 for ind in range(len(df)):
 14     ij=int(df.loc[ind,'IJ'][2:])
 15     xg,yg=(int(ij/1000)-83/2)*3000,(ij%1000-137/2)*3000
 16     s=0
 17     for j in range(2):
 18         for i in range(2):
 19             ii=i
 20             if j==1:ii=1-i
 21             xgl,ygl=xg+3000*ii,yg+3000*j
 22             lon,lat=pnyc(xgl, ygl, inverse=True)
 23             lon2.append(lon)
 24             lat2.append(lat)
 25             nam2.append(df.loc[ind,'IJ']+'p'+str(s))
 26             lab2.append(df.loc[ind,'lab']+'p'+str(s))
 27             s+=1
 28 df2=DataFrame({'lon':lon2,'lat':lat2,'nam':nam2,'lab':lab2})
 29 df2.set_index('lon').to_csv('mmifTWN_3X3P.csv')
 30 os.system('/opt/local/bin/csv2kml.py -f mmifTWN_3X3P.csv -n P -g LL')
...
```
- 說明：多邊形與點狀資料進入csv2kml.py需要給定重要識別引數，即-n選項。多邊形為-n P。

## uMap的設定
- 為鼓勵應用，uMap貼圖並不需要登記/登入會員，只要擁有編輯頁面網址的人，都可以進行編輯。
- 目前還找不到中文的操作說明

### 設定步驟
* 在[uMap家網頁](https://umap.openstreetmap.fr/zh-tw/)上勾選創建地圖
* 點選右側**Manage Layers**圖層(圓餅疊)，按下增加圖層、建入名稱、描述、圖層類型(選擇**clustered**，圖面會歲縮放比例合併點狀資訊筆數)
* 點選右側導入數據(向上箭頭)，選擇KML檔案、確認導入到前述圖層，按下導入。
* 點選右側**Manage Layers**圖層(圓餅疊)，選取圖層來編輯(白筆)，
  * 由**Shape Propertise**進行頁面展示方式的選項
    * 顏色：內設為深藍，如要其他顏色需在此設定
    * 不透明度：向右則完全不透明
    * 多邊形Placemark的填滿。內設是不填滿，只有線條
    * 填滿顏色：內設為深藍，
    * 明度透： 向右為完全透明
  * 由**Interaction action**分頁中進行使用者介面(滑鼠動作)的選項
    * **popup shape**：sidepanel(右側會出現POI內、詳圖示)
    * **popup content**：確認有name及descriptions(連結是在descriptions)
* 儲存→保存→不可編輯→點選任一格點來測試看看，是否右側會出現連結
* 點選鑰匙符號，會出現編輯網址token，複製儲存，以備下次編修。
* 點選連結：
    * 瀏覽器會另開分頁展示檔案內容。
    * 成果如圖示
### 中文
- uMap介面可以接受中文輸入與顯示，但無法批次上載具有中文字形的檔案(包括kml或csv檔案)，原因不明。

## uMap成果範例
- [mmif成果鏈結](https://umap.openstreetmap.fr/zh/map/3km_590688#11/22.6676/120.5557)
- TEDS 點源位置及煙囪條件
  - [teds10](https://umap.openstreetmap.fr/zh/map/teds10-point-data-pm25_594438#7/24.062/120.822)
  - [teds11(含aermap package)](https://umap.openstreetmap.fr/zh/map/teds11-point-data-pm25_728979#8/24.172/120.086)
- AERMAP執行成果
  - [teds10 1X1解析度位置，煙囪高假設100m](https://umap.openstreetmap.fr/zh/map/twn1x1-aermap-results_593832#8/23.675/121.278)
  - [teds11個別廠位置、各廠最高煙囪高度](https://umap.openstreetmap.fr/zh/map/taiwan-aermap_11-points_730878#7/23.671/121.084)

## Reference
