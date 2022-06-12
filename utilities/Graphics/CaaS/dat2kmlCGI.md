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
  - 使用[引數](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/#引數說明)還不少，造成困擾。
  - 程式更新的需求
- dat2kml的程式設計詳見[等值圖KML檔之撰寫](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)，此處詳細介紹遠端服務系統的架構、運作、以及可能的問題。

### instance
- [http://114.32.164.198/dat2kml.html](http://114.32.164.198/dat2kml.html)
- 畫面

| ![dat2kml.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/dat2kml.png)|
|:--:|
| <b>[http://114.32.164.198/dat2kml.html](http://114.32.164.198/dat2kml.html)畫面</b>|

## 檔案結構
### HTML
- $web/dat2kml.html