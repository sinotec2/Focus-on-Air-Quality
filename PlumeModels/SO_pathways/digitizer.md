---
layout: default
title: 地圖數位板
parent: SO Pathways
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-03-08 10:16:34
---
# 地圖數位板
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
- 空品模式建構過程中，有個好用的數位板（digitizer）是有幫助且必要的。
- Google Map雖然可以點取經緯度值，但需個別儲存，無法批次作業，不甚理想。

### 數位板的用處：
- 沒有DTM情況下描繪等高線圖以取得高程數據。
- 點取污染源位置
- 沒有工程平面圖情況下讀取廠房、計畫範圍、海岸線等

### 執行方案
- 人工紙本方案：影印目標地圖（平面圖）委請CAD人員應用數位板，將所要的點、線予以數位化。再由工程師進行座標平移、旋轉計算。
- Google Map數位方案：
  - 在Google map上進行少數座標點的讀取。
  - Google可以更換背景（街道、地形圖、衛星航照圖）、對點選過程提供不少參考。
  - 單點運作、沒有輸出檔案不能配合批次作業。
- Leaflet數位方案：[單點點選](https://github.com/stefanocudini/leaflet-locationpicker)、[多邊形](https://github.com/banmedo/LeafletDigitizer)範例
  - 可以搭配open streetmap、open topomap等，版權較無問題。
  - 直接輸出成KML檔案，方便檢核、讀取、以及後續之計算。

### 必要之修改
- 前述banmedo網友提供的範本（[多邊形範例](https://github.com/banmedo/LeafletDigitizer)）中，功能還有待開啟或擴充：
  - 只有google Image，還需要有open street、open topomap，方便參考並出圖。(Google Map影像具有版權)
  - 只有開啟Polygon、還需要開啟Marks功能，以利選取個別點位座標。

## 成果應用說明
- CaaS成果位置：[http://114.32.164.198/LeafletDigitizer/](http://114.32.164.198/LeafletDigitizer/)
- 圖層：
  - 為加速網頁的服務速度，並未內設圖層。使用者必須在左側面版中自選圖層
  - openstreet 街道圖、中文顯示
  - Google Image 衛星航照圖、沒有文字
  - Open topomap街道+等高線地形圖、中文顯示、不同等級縮放比例顏色會有差異。
- 按下五邊形進行多邊形的點選：
  - 「逆時針」輸入、回到第一點單擊後才算完成
  - 在對話窗輸入名稱（含建築物高度，如b1 30m、Plant1/30）
  - 不接受中文字、全形
  
| ![digitizer1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/digitizer1.png)|
|:--:|
| <b>啟動多邊形的點選、逆時針輸入回到第1點</b>|
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
