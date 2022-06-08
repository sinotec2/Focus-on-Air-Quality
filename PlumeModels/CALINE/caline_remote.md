---
layout: default
title: caline3遠端計算服務
parent: CALINE
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-04-08 15:30:32
---
# *caline3*遠端計算服務
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
- 
## caline3遠端計算服務
- 網址[http://114.32.164.198/CALINE3.html](http://114.32.164.198/CALINE3.html)
- 選取本地的[輸入檔案]()、按下Run鍵即可。

| ![CALINE_remote.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CALINE_remote.PNG)|
|:--:|
| <b>CALINE[遠端計算網頁](http://114.32.164.198/CALINE3.html)畫面</b>| 



### KML 輸入方式
- 輸入檔也接受.kml的形式，也算是有圖形界面的功能。約定如下：
  - 以[數位板Digitizer](http://114.32.164.198/LeafletDigitizer/index.html)建立路段與接受點的空間及屬性資料
  - 接受點與路段的順序不限
  - 一條路可接受最多50個折點（49個路段）
  - 範例如[example.kml](http://114.32.164.198/caline_results/example.kml)(如下圖)
  - 氣象與現場條件設定如下：
    - BRG:0, 45, 90, 135, 180, 225, 270, 315 等8個風向
    - U, CLAS, MIXH: 1.0m/s, 6, 100m
    - ATIM, Vs, Vd, Z0, AMB: 60min, 0, 0, 100cm, 1.0PPM
- 物件屬性的順序（在數位板上有提示）
  - 接受點：名稱、高度
  - 路線(折線)：名稱、路型、交通量、排放係數、路高及路寬
  - 屬性間的間隔可以是：`,;_/ |-(`

| ![atts.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/atts.png)|
|:--:|
| <b>數位板提示鍵入物件名稱與屬性</b>| 

| ![sanchong.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/sanchong.png)|
|:--:|
| <b>數位板所建立的範例檔案</b>| 