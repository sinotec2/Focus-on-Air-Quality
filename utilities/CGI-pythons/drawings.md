---
layout: default
title:  drawings CGI-pythons
parent: CGI-pythons
grand_parent: Utilities
last_modified_date: 2022-06-11 21:21:57
---
# 有關繪圖的CGI-pythons
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
- 這些繪圖相關的計算平台、包括整個系統的架構、檔案配置、運作方式、成果等等都放在[繪圖及前處理程式-有關繪圖的CaaS平台](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/)進一步說明。此處著重個別python程式設計的說明。

## [dat2kmlCGI.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/dat2kml/dat2kmlCGI.py)
- 相關類似程式
  - [dat2kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/#dat2kml) 的程式設計，因與GIS有關係，跟其他地圖處理放在一起說明。
  - [PLOTFILE to KML](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/OU_pathways/PLT2kml/)，事實上[PLT2kml.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/OU_pathways/PLT2kml.py)是前者的一項應用。
- 煙流模式模擬結果(PLOTFILE)，轉成kml形式的等值線。計算與檔案處理都還算單純。沒有需要監看的必要。
### 程式呼叫與檔案儲存
- CaaS
  - 位置：[http://125.229.149.182/dat2kml.html](http://125.229.149.182/dat2kml.html)
  - 說明：[dat2kml遠端計算服務](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/CaaS/dat2kmlCGI/)
- EXE
  - `DAT2KML='/opt/local/bin/dat2kml.py'`
- 工作目錄
  - `pth=WEB+'isc_results/kmls_'+ran+'/'`、ran是6碼亂數文字。
### 檢視
- 工作完成提示網頁中提醒可以使用免費的[Leaflet](http://125.229.149.182/Leaflet/docs/index.html)服務(詳[地圖貼板](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#地圖貼板))
- 事實上 Visual Code也提供了預覽KML檔案的[插件](https://marketplace.visualstudio.com/items?itemName=jumpinjackie.vscode-map-preview)，效果也還不錯。

## [isc_parser.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parser.py)程式
- 同一支CGI-python導入後，會依照輸入內容呼叫不同的CGI-python（[isc_parserSO.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parserSO.py)以及[isc_parserBP.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/isc_parserBP.py)）
- 詳見[污染源空間解讀器](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser/)的說明
### 程式呼叫與檔案儲存
- CaaS
  - 位置：[http://125.229.149.182/dat2kml.html](http://125.229.149.182/dat2kml.html)
  - 系統說明：[污染源空間解讀器](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser/)
- EXE
  - `CSV2KML='/opt/local/bin/csv2kml.py -g TWD97 -f '`
- 工作目錄
  - `pth=WEB+'prsr_results/kmls_'+ran+'/'`、ran是6碼亂數文字。
### 檢視
- 工作完成提示網頁中提醒可以使用免費的[Leaflet](http://125.229.149.182/Leaflet/docs/index.html)服務(詳[地圖貼板](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#地圖貼板))
- Visual Code[插件](https://marketplace.visualstudio.com/items?itemName=jumpinjackie.vscode-map-preview)，也可以考慮。
