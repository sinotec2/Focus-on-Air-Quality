---
layout: default
title:  dat2kml遠端計算服務
parent: CaaS to Graphs
grand_parent: Graphics
last_modified_date: 2022-06-11 22:00:06
---
# dat2kml遠端計算服務
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
- dat2kml.py跨平台執行的困難、以及提供遠端服務的必要性
  - 需要特殊模組`legacycontour._cntr`，在python3為第3方提供的軟體，並不屬`matplotlib`內容，需另行自[githup](https://github.com/matplotlib/legacycontour.git)安裝，如果安裝不成就不能執行。
  - 使用[引數][arg]還不少，造成困擾。
  - 程式更新的需求
- 除了快速的KML方案，使用者也可以選擇速度較慢一些的[NCL][NCL]方案([NCLonOTM on iMacKuang](http://125.229.149.182/NCLonOTM.html))。
- dat2kml的程式設計詳見[等值圖KML檔之撰寫](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)，此處詳細介紹遠端服務系統的架構、運作、以及可能的問題。

[arg]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/#引數說明> "usage: dat2kml.py [-h] -f FNAME [-d DICTR]"
[NCL]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/NCLonOTM/> "NCL(NCAR Command Language)是美國大氣研究中心出台的繪圖軟體，目前已經出到6.6.2版。"

### instance
- [http://125.229.149.182/dat2kml.html](http://125.229.149.182/dat2kml.html)
- 畫面

| ![dat2kml.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/dat2kml.png)|
|:--:|
| <b>[http://125.229.149.182/dat2kml.html](http://125.229.149.182/dat2kml.html)畫面</b>|

## 檔案結構
### HTML
- $web/[dat2kml.html](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/dat2kml/dat2kml.html)
  - 使用[filepicker](https://github.com/sinotec2/CGI_Pythons/tree/main/utils/filepicker)開啟使用者指定上傳的檔案
  - 啟動CGI-python程式
  - 提供[isc_results/case_SOX_Y.PLT](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/dat2kml/case_SOX_Y.PLT)AERMOD模擬結果範例檔案

### CGI-python
- $cgi/isc/[dat2kmlCGI.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/dat2kml/dat2kmlCGI.py)，詳見[有關繪圖的CGI-pythons](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/drawings/#dat2kmlcgipy)的說明
- 提供[地圖貼板](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#地圖貼板)([Leaflet Filelayer on iMacKuang](http://125.229.149.182/Leaflet/docs/index.html))的連結

### EXE
- `DAT2KML='/opt/local/bin/dat2kml.py'`，詳見[等值圖KML檔之撰寫](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)

### 工作目錄
- `pth=WEB+'isc_results/kmls_'+ran+'/'`，**ran**為隨機產生之6碼文字