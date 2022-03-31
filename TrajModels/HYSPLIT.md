---
layout: default
title: HYSPLIT
nav_order: 2
parent: Trajectory Models
last_modified_date: 2022-03-31 15:20:02
---

# HYSPLIT分析
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
###   地面二維軌跡分析程式的困難
1. 以地面測站觀測的風速風向數據為主，沒有高空及山區的數據。山區、海面上則必須要數值模式產生。
2. 分析模式僅適用在台灣局部地區，沒有中國大陸與其他地區的數據，軌跡線超過範圍即沒有數據，需要國際研究機構的支援。
3. 模式作業化程度需較高，並套用高解析度地圖，以應付經常性之解析需求。

### HYSPLIT簡介
1. 美國海洋與大氣總署空氣資源研究室(NOAA ARL)所發展的HYSPLIT(Hybrid Single Particle Lagrangian Integrated Trajectory Model )模式，為國內外學術及作業單位經常應用的軌跡模式，
2. 應用NOAA或NCEP再分析模式之輸出結果，不必另外再執行數值模式。
3. 解析度可以到1度x1度、範圍則為全球。
4. 其GIS結果(包括.shp與.kmz)可與高解析度地圖套疊，以解析大氣邊界層運動與可能的跨國污染現象。

## 執行步驟

### 選擇軌跡種類
1. 進入HYSPLIT-WEB網站(NOAA ARL網站 HYSPLIT-WEB (Internet-based) ,[http://ready.arl.noaa.gov/HYSPLIT.php](http://ready.arl.noaa.gov/HYSPLIT.php))

| ![HYSPLIT1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT1.png)|
|:-:|
| <b>HYSPLIT入口畫面</b>|   

- 點選”Run HYSPLIT Trajectory Model” 

| ![HYSPLIT2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT2.png)|
|:-:|
| <b>Run HYSPLIT Trajectory Model</b>|

2. 可以選擇計算預測軌跡(Compute forecast trajectories)或者是過去的軌跡(Compute archive trajectories): 
  - 前者可以應用在污染事件，如緊急洩漏、大火與毒性物質排放等的即時預測，可以搭配擴散模式(dispersion model)，
  - 後者則為以前的個案，用在解析污染成因探討。 

| ![HYSPLIT3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT3.png)|
|:-:|
| <b>Compute forecast trajectories</b>|

- 若是要回顧之前的執行成果，可以點選”Retrieve Previous model results”，當然ARL並不永久儲存這些網路執行的成果。

3. 進入archive之後，首先要選擇軌跡線起點的個數，最多可以接受3(中心)點。要求以緯度與經度輸入。
4. 其次為種類(Type)軌跡線的個數：有4個選項(Normal/Matrix/Ensemble/Frequency) 
  - 標準(Normal)：適用在一般點狀如測站、工廠等接受者或污染源
  - 矩陣(Matrix)：指定左下角與右上角兩點之後，模式會自動產生矩陣格點(解析度視選取的資料庫而定)，成為軌跡模式起始或終點，適用在都會區、工業區等面狀的接受者或污染源，但只限同一高度。如下圖所示。

| ![HYSPLIT4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT4.png)|
|:-:|
| <b>Trajectory Matrix</b>|
   
  - 叢集(Ensemble)：模式會自動產生指定點三度空間的前後網格共27個之軌跡起始或終點，其結果如下圖所示。 

| ![HYSPLIT5.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT5.png)|
|:-:|
| <b>Trajectory Ensemble</b>|

  - 機率(Frequency): 一定時間內每隔6小時開始一個軌跡，然後對軌跡通過網格單元的次數求和，然後除以所有質點總數，以計算通過機率。 軌跡可能與網格單元相交一次或多次（駐留時間選項為1、2或3）。 

| ![HYSPLIT6.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT6.png)|
|:-:|
| <b>Trajectory Frequency</b>|

  - 設定好個數與種類之後，即可進行下一步” Next>>”

### 位置及時間點
1. 選取氣象資料庫與起迄點： 
  - 東亞地區必須選取GDAS(Global Data Assimilation System)。此一資料庫為美國國家天氣環境預報中心(The National Weather Service's National Centers for Environmental Prediction NCEP)的模式產品，為ARL應用在空氣品質計算最主要的依據。
  - 設定軌跡起始/終點的座標。可以由圖中點選、或直接輸入座標。 

| ![HYSPLIT7.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT7.png)|
|:-:|
| <b>Source Location</b>|

  - 注意：如果直接設定緯度與經度， 注意數字之前不可以有空格。台灣地區的城市名稱、測站與機場等，均不在其資料庫中按”Continue”繼續。
  - 垂直高度解析度：第一層為1000mb(80~90m)、第二層為975mb(300m)、第三層為950mb(500m)。此一設定與空氣污染有關。

2. 選定氣象檔案的時間 
  - 以下拉選單選取最近7天或其他GDAS時間檔案(Select the GDAS1 File) 
  

| ![HYSPLIT8.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT8.png)|
|:-:|
| <b>Meteorology File</b>|

- 確認GDAS檔案的日期範圍
  - 其儲存檔名(gdas1.mmmyy.w#)以三碼月份(jan~dec)西元後兩碼、以及第幾週來區別(w1=1-7, w2=8-14, w3=15-21, w4=22-28, w5=29-最末日)選取後將進入下一畫面。

3. 模式設定(Model Run Details)：完成表格的點選 
- 軌跡移動的方向(方式)

| ![HYSPLIT9.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT9.png)|
|:-:|
| <b>Trajectory Movements</b>|

      Trajectory direction軌跡的方向(正/反) 
        Forward正軌跡，用在預報未來
        Backward反軌跡，解析污染可能成因
      Vertical Motion氣團垂直運動是肇因於： 
        Model vertical velocity模式垂直速度所帶動(小尺度)
        Isobaric等壓面高度時間變化所帶動(天氣系統)
        Isentropic等熵面高度時間變化所帶動(大尺度)

- 有關時間的設定

| ![HYSPLIT10.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT10.png)|
|:-:|
| <b>Start time</b>|


      Start time (UTC):
          year month day hourTotal run time (hours): 軌跡線的長度(延時)
          Start a new trajectory every: hrs
      Maximum number of trajectories: 模式可設定自動開始的周期 
   
- 有關空間的設定 

      經緯度 
        Start 1 latitude (degrees):Start 1 longitude (degrees):...
      高度 
        Automatic mid-boundary layer height?自動以行星邊界層中間點作為軌跡線高度
        Level 1 height:指定高度 
        meters AGL (Above Ground Level地面高)
        meters AMSL(Above mean-sea Level平均海面高)...

- 設定輸出圖面的內容，如下表 

| ![HYSPLIT11.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT11.png)|
|:-:|
| <b>Output Checking List</b>|

    結果型式
      GIS等值線輸(KMZ/SHP)_可以另存GIF/SHP/KMZ。
      軌跡的座標等其他輸出，也包括模式的設定與控制檔案，可以用在本機的計算。
    Plot resolution (dpi):  解析度
    Zoom factor: 0(含蓋範圍最小)~100
    Plot projection:地圖投影方式 
      Default(按所在緯度提供最佳投影)、
      Polar(極座標系統)、
      Lambert(直角座標、地圖中心為原點)、 
      Mercator(麥卡脫投影、赤道原點)
    Vertical plot height units:高度單位 
      Pressure、 
      Meters AGL、
      Theta(1~0無因次，與地面壓力差之比值)
    Label Interval:軌跡線上的標籤 
      No labels、 6 hours、 12 hours、 24 hours
    Plot color trajectories? (2條以上軌跡線較容易辨識)
      Yes、 No
    Plot source location symbol?顯示起迄之關係
      Yes、 No
    Distance circle overlay:(用以估計長度 )
      None、 Auto
    U.S. county borders? (國界)
      Yes、 No
    Postscript file?   Yes、 No
    PDF file?         Yes、 No
    Plot meteorological field along trajectory? (可同時與其他氣象場繪在同一張圖上) Yes、 No
    Dump meteorological data along trajectory: 
      Terrain Height (m)
      Potential Temperature (K)
      Ambient Temperature (K)
      Rainfall (mm per hr)
      Mixed Layer Depth (m)
      Relative Humidity (%)
      Downward Solar Radiation Flux (W/m**2)



| ![HYSPLIT12.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT12.png)|
|:-:|
| <b>圖HYSPLIT模式執行過程與結果</b>|   

- 提交計算(“Request trajectory”) 
- 每10秒會自動更新，不必重新整理詢問結果。
- archive會與當下時間差到1天。太靠近實際時間無法執行。
- 點選.gif、.pdf即可檢視結果

## 案例說明
### 本地污染之反軌跡線
1. 2010/1/27/14:00桃園站發生臭氧小時值超過130ppb的污染事件，
2. 由當日HYSPLIT反軌跡(48小時)走勢如下圖所示。由圖中可以發現，當天軌跡線有很大的轉折，而由高度走勢可以發現，軌跡線乃通過台北盆地南方的雪山山脈。
3. 由於HYSPLIT是三維軌跡，因此可以得知該軌跡線48小時乃源自於琉球群島西方1000公尺高空開始，由宜蘭南方進入台灣後經過雪山山脈下沉至台北盆地。 

| ![HYSPLIT13.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT13.png)|
|:-:|
| <b>圖HYSPLIT模式結果範例</b>|   
   
4. 由綜觀尺度軌跡線的走勢來看，桃園測站反軌跡線除了經過台北盆地之外，其餘並沒有經過其他人為污染地區，可以研判其主要的污染來源應為台北盆地的排放。
5. 再由其模擬結果與google map之地形與地名套疊後(如下圖)，可以進一步證實當日冬季盛行風並不旺盛，夜間氣流由雪山山脈下沉到台北盆地的中央，朝向淡水河谷方向流去，逐漸減緩其速度，
6. 然而在6:00太陽出現之後，有一顯著的轉向，沿著大漢溪和谷向西南方向移動(詳圖(a))。
7. 由於日出之後，盆地內的交通與工廠開始活動，其排放將隨著氣流沿著大漢溪河谷向桃園方向傳送，軌跡線在晨峰時間兩次經過高速公路、又通過五股工業區與新莊區西方的市區(詳圖(b))。
8. 由於午間到達桃園正好遇見靜風狀態，軌跡線在桃園市區遊走，因此造成較高臭氧濃度。
- 圖 NOAA ARL 之HYSPLIT模式模擬結果與google map之結合

| ![HYSPLIT14.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT14.png)|![HYSPLIT16a.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT16a.png)|
|:-:|:-:|
| <b>(a)北部地區範圍</b>| <b>(b)台北盆地西側範圍</b>|  


### 大陸塵霾之反軌跡線
1. 2013/12/27 3:00、9:00、及15:00分別依序在萬里、三義、橋頭發生PM10、PM2.5及SO2的高值，由環保署網站上查出各測站的座標，高值出現時間，　
2. 測站資料表

|測站|位置|高值時間|北緯|東經|
|-|-|-|-|-|
|萬里|綜合商場|12/27/3:00L 12/26/15:00 Z|25度10分46.8秒(25.1667)|121度41分23.57秒(121.6898)|
|三義|長壽俱樂部|12/27/6:00L 12/26/18:00 Z|24度22分58.59秒(24.3829)|120度45分31.80秒(120.7588)|
|橋頭|橋頭區公所|12/27/9:00L 12/26/21:00 Z|22度45分27.02秒(22.755)|120度18分20.48秒(120.3057)|

此三站高值時間的反軌跡


| ![HYSPLIT15.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT15.png)|![HYSPLIT16.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT16.png)| ![HYSPLIT17.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/HYSPLIT17.png)|
|:-:|:-:|:-:|
|萬里(2013/12/27 3:00L)|三義(2013/12/27 6:00L)|橋頭(2013/12/27 9:00L)|



- 由中北部測站之反軌跡可以發現，主要經過中國長三角一帶之污染源，為典型的大陸霧霾事件。
- 唯南部反軌跡並非直接來自中國北方，而是以一接力型式，延續大陸霧霾的影響，其軌跡乃經中國南方珠三角地區，亦為重要污染地區。
