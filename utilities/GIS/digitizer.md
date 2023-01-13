---
layout: default
title: 地圖數位板
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-03-15 10:41:25
tags: GIS KML
---
# 地圖數位板_座標之讀取
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

- 空品模式建構過程中，有個好用的數位板（digitizer）是有幫助且必要的。相對於傳統圖紙上量測的作業方式，地圖數位板的優勢在於：
  - 精確計算與修正，消除估計值的誤差
  - 減省輸入的工作，降低大規模作業的困難度
  - 便於檢視、偵錯
- Google Map雖然可以也可以點取經緯度值，但需個別儲存，無法批次作業，不甚理想。其餘進一步比較如下。

### 數位板的用處

- 沒有DTM情況下描繪等高線圖以取得高程數據，這在離島、軍事地區、或者在CTDM的前處理過程，是非常必要的。
- 點取污染源位置
- 沒有工程平面圖情況下讀取廠房、計畫範圍、海岸線等
- 數位板也可用於檢查KML檔案之轉換結果，see [[csv2kml]]、[[dat2kmlCGI]]、[[wr_kml]]

### 執行方案比較

- 人工紙本方案：影印目標地圖（平面圖）委請CAD人員應用數位板，將所要的點、線予以數位化。再由工程師進行座標平移、旋轉計算。
- Google Map數位方案
  - 在Google map上進行少數座標點的讀取。
  - Google可以更換背景（街道、地形圖、衛星航照圖）、對點選過程提供不少參考。
  - 單點運作、沒有輸出檔案不能配合批次作業。
- SURFER digitizer
  - SURFER亦有數位板工具，將平面圖照像、輸入軟體成為底圖，再開啟數位板工具，點選座標軸後，依然可以逐一點選需要的位置，經後處理計算座標值。
  - 應用於不存在背景地圖的新建築物、計畫設施等情況
  - 其結果為直角座標的文字檔，需自行撰寫程式進行旋轉平移。還需設定參考點、同時有該點的經緯度與直角座標值，方能與既有地圖系統重疊。
- Leaflet數位方案：[單點點選](https://github.com/stefanocudini/leaflet-locationpicker)、[多邊形](https://github.com/banmedo/LeafletDigitizer)範例
  - [Leaflet官網](https://leafletjs.com/)已經累積了許多好用的程式庫，可以在互動式地圖平台上加上圖層。
  - Leaflet可以搭配open streetmap、open topomap等，版權較無問題。
  - 也直接輸出成KML檔案，方便檢核、讀取、以及後續之計算。

### 必要之修改
- 前述banmedo網友提供的範本（[多邊形範例](https://github.com/banmedo/LeafletDigitizer)）中，已有一些基本的功能，然而還有待開啟、或擴充，項目包括：
  - 底圖只有google Image(Google Map影像具有版權)，還需要有open street、open topomap等[圖層](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#加入圖層)，方便參考並出圖，尤其是地形([OpenTopoMap](https://wiki.openstreetmap.org/wiki/OpenTopoMap))，對空氣品質的模擬有很重要的參考價值。
  - 只有開啟Polygon、還需要[開啟Marks功能](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#啟動marks點選)，以利選取個別點位之座標。

## 成果應用說明
- CaaS成果位置：[http://125.229.149.182/LeafletDigitizer/](http://125.229.149.182/LeafletDigitizer/)
- 圖層：
  - 為加速網頁的服務速度，並未內設圖層。使用者必須在左側面版中自選圖層
  - openstreet 街道圖、中文顯示
  - Google Image 衛星航照圖、沒有文字
  - Open topomap街道+等高線地形圖、中文顯示、不同等級縮放比例顏色會有差異。
- 按下五邊形進行多邊形的點選：
  - 以一定方向輸入、回到第一點單擊後才算完成
  - 在對話窗輸入名稱（含建築物高度，如b1 30m、Plant1/30）
  - 不接受中文字、全形
  
| ![digitizer1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/digitizer1.png)|
|:--:|
| <b>啟動多邊形的點選、以一定方向逐一輸入回到第1點</b>|
| ![digitizer2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/digitizer2.png)|
| <b>對話窗輸入名稱、高度</b>|

- 按下氣球點選污染源位置
  - 在對話窗輸入名稱（可以含污染源的高度，如hs1 250m、stk1;30）
  - 不接受中文字、全形

| ![digitizer3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/digitizer3.png)|
|:--:|
| <b>啟動氣球的點選、輸入污染源名稱(高度)</b>|

- 按下磁碟片儲存檔案
  - 不必打附加檔名（.kml）
  - 不接受中文字、全形
  - 正常會存到Downloads目錄
- 按下右側檔案夾、檢視檔案數位化過程是否正確

| ![digitizer4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/digitizer4.png)|
|:--:|
| <b>儲存結果在使用者電腦的Downloads目錄</b>|
| ![digitizer5.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/digitizer5.png)|
| <b>重新開啟檢視剛儲存的檔案</b>|

## JS程式修改
- Digitizer由js/、libs/（含Images）、testData/等目錄所組成，
- 主要需要修改的程式為js/main.js

### 加入圖層
- 圖層原點：修正成台灣為中心(`(23.7,121.)`)、縮放等級(`zoom`)設定為7（line 1）
- Open street:參考其他Leaflet範例設定動態連結(line 7~9)
- open topomap：從網友提供範例擷取連結URL與版權協定。(line 15~18)

```java
kuang@114-32-164-198 /Library/WebServer/Documents/LeafletDigitizer
$ cat -n js/main.js
     1    var map = new L.Map('map', { center: new L.LatLng(23.7,121.), zoom: 7}),
     2            drawnItems = L.featureGroup().addTo(map),
     3            pointLayer = L.featureGroup().addTo(map),
     4            lineLayer = L.featureGroup().addTo(map);
     5    
     6    var layercontrol = L.control.layers({},{
     7        "Open Street": L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     8            attribution: 'Map data &copy; 2013 OpenStreetMap contributors'
     9        }),
    10          "Google Image": L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
    11              attribution: 'Google',
    12              maxZoom: 20,
    13              maxNativeZoom :18
    14          }),
    15        "OpenTopoMap": L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    16              maxZoom: 17,
    17             attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
    18      }),
    19        "Digitizations ": drawnItems,
    20        "Points (GPS)": pointLayer,
    21        "Match lines": lineLayer,
    22    },{ position: 'topleft', collapsed: true }).addTo(map);
    23    
```

### 啟動Marks點選
- 同樣在js/main.js內，
  - Marks和Polygon屬於draw項下的函數，原本內設為定值false（與其他polyline、circle相同），將其選項showMarker設定為true即可啟動（line 46）
  - libs/Images目錄下須存放Marks的png（作者忘了提供），由於是常見的氣球圖像，在工作站上locate就可以找到檔案。

```java
    map.addControl(new L.Control.Draw({
        edit: {
            featureGroup: drawnItems,
            poly: {
                allowIntersection: false
            },
            rename: {
                acceptDupes: false
            }
        },
        draw: {
            polygon: {
                allowIntersection: false,
                showArea: true
            },
            polyline:false,
            rectangle:false,
            circle:false,
            marker: {
                showMarker: true  #46
            },
        }
    }));
```
### Marker圖檔
```bash
-rwxr-xr-x  1 kuang  staff   1.2K Mar  3 09:26 layers-2x.png
-rw-r--r--  1 kuang  staff   2.4K Mar  3 09:38 marker-icon-2x.png
-rw-r--r--  1 kuang  staff   1.4K Mar  3 09:41 marker-icon.png
-rw-r--r--  1 kuang  staff   618B Mar  3 09:42 marker-shadow.png
```

## Reference
- Nishanta Khanal(banmedo),[LeafletDigitizer](https://github.com/banmedo/LeafletDigitizer)
- b_b brunob, Calvin Metcalf calvinmetcalf, and Michael Lawrence Evans mlevans, [leaflet-extras](https://leaflet-extras.github.io/leaflet-providers/preview/)

# 地圖貼板
同樣是使用Leaflet模組，前面的數位版也可以作為貼板，只是專業的貼板需要有不同底圖的選項，設計上有點不太一樣。
## 前言
一個好的地圖貼板、壁貼、是科學家、建築師、工程師、企業主、甚至軍事、偵察工作時必備的工具。在現代資訊工具的輔助下，貼板具備了縮放的功能、也提供許多地圖的細節資訊，在模式領域成為檢核過程的必要程序之一。
### 既有方案與比較
* Google map
    * google提供了[KML](https://developers.google.com/kml/documentation/kml_tut)格式，讓使用者可以在google 地圖上、貼上自己的資訊，最後發展成商業APP。
    * 因為Google地圖（街道、地形、衛星）資訊豐富、對KML有最充分的支援，因此也有最高的品質效果（色階、圖像）。
    * 缺點：除了版權的問題之外、界面略嫌繁瑣、速度不佳服務不穩定、對其他格式封閉、**資料筆數**限制
* Leaflet open street map（[OSM](https://wiki.openstreetmap.org/wiki/Zh-hant:Main_Page)）
    * 程式碼開放、支援KML、json等許多格式、無版權問題、程式可客製化，資源需求較低，快速、穩定。
    * 缺點：對KML僅粗淺支援、品質未臻完全。
### 方案檢討
* Google和OSM的最大公約數是KML格式，因此發展以KML為主的輸入、輸出格式為最合理的方向。
* 雖然Google品質較佳、然而因為版權限制只能放棄，OSM雖然品質有限，然卻能快速、穩定提供檢核功能
* TODO
    * 出圖問題只能另外尋求方案（如[NCL](https://www.ncl.ucar.edu/)）。
    * KML之色階、圖像可列為遠期發展項目。
### 模版與工作
參考網友公開之[filelayer](https://makinacorpus.github.io/Leaflet.FileLayer/) 與[marker](https://leafletjs.com/)成果。

須修改項目：
1. Headlines and footlines
2. 地圖中心點、內設縮放比例
3. 圓點顏色（原版為紅色、鑑別度較低）、透明度（原版為不透明、遮蔽底圖）
4. 合併標示第一點位置與訊息之標記
## CaaS
- 位置：http://125.229.149.182/Leaflet/docs/index.html
- 貼圖成果

| ![leaflet_demo.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/leaflet_demo.png)|
|:--:|
| <b>[http://125.229.149.182/Leaflet/docs/index.html](http://125.229.149.182/Leaflet/docs/index.html)畫面</b>|


## JS
有關地圖的設定是在docs/index.js內
### 內設中心點、縮放比例、顏色與透明度
* 中心點、縮放比例在map項下的center與zoom兩個變數(line 11~12)
    * 設成台灣中心的緯度、經度[23.6, 120.9,]
    * 縮放比例經嘗試錯誤後決定為 7
* 顏色與透明度在style項下的color、opacity、fillopacity變數(line 15~17)
    * 顏色選藍色有最高的鑑別率
    * 透明度經嘗試錯誤選擇0.4~0.5

```java
$ cat -n index.js
     1    (function (window) {
     2        'use strict';
     3        var L = window.L;
     4    
     5        function initMap() {
     6            var control;
     7            var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     8                attribution: 'Map data &copy; 2013 OpenStreetMap contributors'
     9            });
    10            var map = L.map('map', {
    11                center: [23.6, 120.9,],
    12                zoom: 7
    13            }).addLayer(osm);
    14            var style = {
    15              color: 'blue',
    16                opacity: 0.5,
    17                fillOpacity: 0.4,
    18                weight: 1,
    19                clickable: false
    20            };
    21            L.Control.FileLayerLoad.LABEL = '<img class="icon" src="https://upload.wikimedia.org/wikipedia/commons/f/fe/Gnome-folder.svg" alt="file icon"/>';
    22            control = L.Control.fileLayerLoad({
    23                fitBounds: true,
    24                layerOptions: {
    25                    style: style,
    26                    pointToLayer: function (data, latlng) {
    27                        return L.circleMarker(
    28                            latlng,
    29                            { style: style }
    30                        );
    31                    }
    32                }
    33            });
    34            control.addTo(map);
    35            control.loader.on('data:loaded', function (e) {
    36                var layer = e.layer;
    37                var kk=Object.keys(layer._layers);
    38                var i=kk[0];
    39                var lat0=layer._layers[i]["_latlng"]["lat"];
    40                var lon0=layer._layers[i]["_latlng"]["lng"];
    41                var ymd=layer._layers[i]["feature"]["properties"]["description"];
    42                console.log(layer._layers[i]["feature"],layer._layers[i]["_latlng"]);
    43            L.marker([lat0, lon0]).addTo(map)
    44        .bindPopup(ymd)
    45        .openPopup(); 
    46            });
    47        }
    48    
    49        window.addEventListener('load', function () {
    50            initMap();
    51        });
    52    }(window));
```
### 標記
* 基本上是在地圖上add一項L.marker函數、貼上文字(Popup)(line 43～44)，重點是如何從kml檔案中讀取位置及訊息
    * 將loadder內涵陸續在console.log中寫出，找到kml中第一點的位置、以及第一點的標籤。
    * 經過嘗試錯誤後，第一點位置為layer._layers[i]["_latlng"]["lat”]、layer._layers[i]["_latlng"][“lng"]
    * 第一點的標籤layer._layers[i]["feature"]["properties"]["description"]
### 使用
* 由左側檔案夾開啟檔案
    * 可接受多檔案的開啟、作為圖層者比較、參照、修改等
    * 除了用小剪刀、擷取畫面之外、
    * 如為軌跡線之檔案，尚可利用NCL traj另作為輸出(服務網頁)
* 無法顯示KML元素之標記、顏色，完整功能還是需要Google Map
## 使用數位板作為貼板
數位板雖然主要功能在獲取座標資料，但因數位化過程也需要檢核，因此網友也開發了貼板的功能。
* 從右側檔案夾開啟檔案、
* 再從左側點選適合的背景圖層
* 勾掉Digitizations即暫時關閉使用者檔案圖層，只出現底圖。可作為比較、參照。
* 如要永久關閉檔案，重新調整網頁即可。

| ![leaflet_demo3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/leaflet_demo3.png)|![leaflet_demo4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/leaflet_demo4.png)|
|:--:|:--:|
| <b></b>|<b></b>|

## Links
- 開啟檔案圖層：https://makinacorpus.github.io/Leaflet.FileLayer/
- 標記文字與氣球：https://leafletjs.com/
- Relatives:
  * 軌跡線之NCL繪圖： tai and chnMarble.ncl
  * 地圖數位板

