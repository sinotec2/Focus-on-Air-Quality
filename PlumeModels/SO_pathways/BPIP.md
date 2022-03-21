---
layout: default
title: BPIP程式
parent: SO Pathways
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2022-03-08 10:16:34
---
# 建築物煙流下洗現象之模擬設定
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
- 污染源附近建築物造成煙流擴散行為的改變非常劇烈，煙流中心向下移動造成地面嚴重燻煙，稱之為Plume Downwash煙流下洗，其現象、原因及模擬、可以參考[Reference](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#reference)之介紹。
- 目的：計算煙囪附近建築物的長、寬、高等尺寸，以便ISCST3/AERMOD等模式可以引用。
  - 參數之定義為每座煙囪為中心、360度每10度方向所遇到的建築物高度、寬度及長度。可以由污染源廠區平面配置逐一量測而得。
  - 廠房建築物如果過於複雜，需要有前處理程式協助產生這些輸入參數
- 建築物下洗的啟動與必須性
  - 在SO路徑段落中提供建築物參數，煙流模式會自行**視需要**啟動下洗之計算
  - 當煙囪高度在所有建築物高的2.5倍以上時，模式就不會計算下洗，即使提供了建築物參數。
  - **保守**起見，個案輸入建築物參數，讓程式自行決定，是比較完整的作法。
- [BPIP]()全名為Building Profile Input Program。[BPIPPRIME]()則是專為ISC-PRIME模組及AERMOD之預備。
- USEPA官網之說明
	- [BPIP]()是一個PC/Linux 上的應用程式，旨在納入煙囪設計之「良好工程實務(GEP)」精神內涵（詳技術支援文檔《確定良好工程實務準則之煙囪高度（PDF）》101 pp，1985年，建築物下沖計算指南以及其他相關參考）。
  - 經由此一程式，使用者可以正確計算簡單、多層或多組結構的建築物高度((BUILDHGT)和建築物橫向的寬度（BUILDWID）或煙流方向切建築物的長度（BUILDLEN）。 
  - 該程序通常與ISC3模型一起使用。[BPIP]()的最新版本4/21/2004已使用fortran可分配陣列進行了升級，提高了程式維度的自由，同時保持了原有程式的基本功能。
	- [BPIPPRIME]()與[BPIP]()相同，但包括特別升級的算法（P），應用於產生PRIME算法計算煙流下沖之輸入條件，PRIME模組目前已經包含在AERMOD等模型中。
  - [BPIPPRIME]()的輸入結構與[BPIP]()的輸入結構相同，後者則經常與ISC3模型一起使用。 有關更多信息，請參見《BPIP用戶手冊》。

## 設定步驟與內容
### 設定與執行步驟實例示範
1. 由Google地圖（衛星）中找到研究對象包括煙囪、及其「**附近**」建築物之平面配置圖。
  - 「**附近**」的定義為煙囪高度**5倍**水平距離範圍的最大聯集範圍。
1. 找到適合做為廠區配置之**局部座標軸**（廠區道路、管線）、原點（特殊位置點）。
  - 以原點為中心，從地圖**真北**開始、
  - 沿著**順時針方向**轉到局部座標**正Y方向**的**夾角角度D**。
  - 夾角D = 1～360度，為大於0的整數
1. 量測建築物頂點到X軸的距離（頂點座標的Y值）以及到Y軸的距離（頂點座標之Y值）
1. 重複上一動作，量測所有建築物頂點座標及煙囪基地座標值，(X,Y)單位為公尺
1. 開啟Google地圖的地形圖，量測建築物及**煙囪基地高程E**，單位為公尺
1. 建築物與煙囪頂端的**離地高度H**，單位為公尺，可以用陰影長度的比例關係粗略推估。一般工廠辦公室為2層樓建築高度為6公尺。
1. 按照範例之模板輸入D, (X,Y), E, H等數據，存檔、(上傳工作站或[CaaS](http://114.32.164.198/BPIPPRIM.html))。
1. 執行[BPIP]()批次檔[run_bpip.sh]() A1P.INP A1P.OUT A1P.SUM
1. 將OUT檔案中的SO路徑及參數，貼在[ISCST]()或[AERMOD]()的執行控制檔內
  - ISCST不接受[BPIPPRIME]()結果之`BUILDLEN`、`XBADJ`、`YBADJ`等參數
  - 必要時在結果檔中去除之，重新執行[BPIPPRIME]()但將設定`P`改為`ST`(short time)，或重新執行[BPIP]()

| ![BPIP1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP1.png)|
|:--:|
| <b>從航照圖中定義實例廠區座標軸系統、量測夾角、與廠房頂點XY值</b>|

### L形建築物(USEPA提供範例EG1)輸入檔內容說明
- [A1P.INP](http://114.32.164.198/isc_results/BPIP_EG1/A1P.INP)為一L形建築物的範例，另有4座煙囪stk100~3(如下圖)
- 所有的字串輸入需有引號。其餘為自由格式
- 1~4行為整體設定
  1. 個案之文字說明，(原點座標應用在[iscParser]](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser/)之繪圖過程)
  1. 'P'：啟動PRIM機制，如為ISCST，則設定為'ST'
  1. 'METERS' 1.00：單位及(轉換為公尺之)比例
  1. 'UTMN', 210：地圖座標系統(沒有作用)與廠區系統局部座標軸之旋轉角度(地圖正北到正Y方向之順時針夾角)
- 第2段落是每個建築物頂點座標(廠區系統)
  1. 1：建築物個數
  1. 'L-Shape' 1 13.0：	建築物名稱、圈數及地表高程(m)。圈數>1為裙樓狀況。
  1. 6 26：	頂點個數及建築高(m)
  1. -10. -20.  建築物6個頂點相對廠區系統的座標值。不特定方向。不回到第1點閉合。
  1. -10.  80.
  1. 40.  80.
  1. 40.  30.
  1. 90.  30.
  1. 90. -20.	
- 第4段落是有關煙囪的設定
  1.	4：煙囪個數
  1. 'Stk100'  11.00  25.00     -10.00    -20.00 :煙囪名稱、地表高程、煙囪高度及相對廠區系統的座標值(不是UTM或TWD絕對值)
  1. (每座煙囪逐一設定)

| ![A1PINP.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/A1PINP.png)|
|:--:|
| <b>USEPA提供範例(EG1)L形建築物輸入檔</b>|

### BPIP之執行
- [BPIP(PRIME)]()的執行會需要3個檔，以連結方式執行如下列批次檔：
  - 第1個檔約定為fort.10，為前述準備好的輸入檔。
  - 第2個檔為輸出檔，約定為fort.12。SO路徑之建築物參數將會出現在此檔內。
  - 第3個檔為摘要檔，約定為fort.14。會將輸入檔之座標旋轉成真北系統，以供檢查。

```bash
kuang@114-32-164-198 /Users/cybee/bin
$ cat run_bpip.sh
ln -sf $1 fort.10
ln -sf $2 fort.12
ln -sf $3 fort.14
bpipprm
```

### BPIP結果範例
- 每根煙囪都要輸入附近的建築物尺寸，包括360度每10度方向的建築物高度（BUILDHGT）和建築物橫向的寬度（BUILDWID）
- PRIME需要煙流方向切建築物的長度（BUILDLEN）、以及XBADJ、YBADJ參數。
- 排版時SO必須靠左、不留空格或內縮。

| ![A1POUT.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/A1POUT.png)|
|:--:|
| <b>L形建築物之BPIP輸出結果</b>|

## BPIPPRIME之[遠端計算服務](http://114.32.164.198/BPIPPRIM.html)範例
- 由於[BPIPPRIME]()並沒有長時間的積分計算，因此其計算對工作站而言較為容易。
- 比較繁雜的程序是座標、夾角的量測、旋轉平移的計算。
  - 然其描圖、座標平移則需依賴許多python模組，以及Fortran的編譯，都會需要與作業系統持續保持更新。
- CaaS的作業方式：
  1. 先在地圖[數位板](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/digitizer)上點選煙囪及建築物頂點位置、存成[kml檔案](http://114.32.164.198/isc_results/ZhongHuaPaper/paper.kml)(大致上取代前述步驟1\~4.，結果詳下圖1)
  1. 利用[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式將kml檔案旋轉成廠區座標系統，並另存[BPIPPRIME]()的[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，即為前述步驟5\~7.，確認如下圖2。
  1. 執行[BPIPPRIME]()計算(步驟8)
- 細部操作方式與CaaS程式設計詳見[BPIP_CaaS](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP_CaaS)之說明。

| ![BPIP3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP3.png)|
|:--:|
| <b>圖1實例廠區數位化結果，雖然數位板點選結果有些歪斜，[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式會將其均化修正</b>|
| ![BPIP4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP4.png)|
| <b>圖2實例廠區[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)旋轉後之[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，經[ISCPARSER](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)解讀結果</b>|

- [BPIPPRIME]()計算結果詳見[build.txt](http://114.32.164.198/isc_results/ZhongHuaPaper/build.txt)，貼在模式輸入檔的[範例](http://114.32.164.198/isc_results/ZhongHuaPaper/paper1pa_NOX.inp)內(步驟9.)

## Reference and Resource
- 有關煙流下洗的現象、原因、以及如何避免，可以參考下列網址
  - [BREEZE AERMOD 7: Gridded Plume Downwash](https://www.youtube.com/watch?v=bgoU9GTNYHs)
  - [Plume characteristics for three different stack scenarios](https://www.youtube.com/watch?v=qQJRSrfv8eQ)
  - [FDS Simulation](https://www.youtube.com/watch?v=UkV2JHg9CX8)
  - [www.cppwind.com：Building Downwash – Problems, Solutions and Next Generation](ftp://newftp.epa.gov/Air/aqmg/SCRAM/conferences/2015_11th_Conference_On_Air_Quality_Modeling/Presentations/3-6_Building_Downwash-CPP-11thMC.pdf)
- BPIP/BPIPPRIM美國環保署[官方網址](https://www.epa.gov/scram/air-quality-dispersion-modeling-related-model-support-programs#bpip)
- 原始碼
  - [BIPI原始碼](https://www3.epa.gov/ttn/scram/models/relat/bpip.zip)
  - [BPIPPRIME原始碼](https://www3.epa.gov/ttn/scram/models/relat/bpipprime.zip)
- 使用手冊
  - [bpipd.pdf](https://www3.epa.gov/ttn/scram/userg/relat/bpipd.pdf)
  - [bpipdup.pdf](https://www3.epa.gov/ttn/scram/userg/relat/bpipdup.pdf)
- 工作站（cybee@114.32.164.198 PW=cybee123）
  - 執行檔 
    - /Users/1.PlumeModels/ISC/Building_Profile_Input_Program/src/ Bpip.exe
    -  /Users/1.PlumeModels/ISC/BPIPPRM/bpipprm
  - 批次檔
    -  /Users/cybee/bin/run_bpip.sh
  - 範例
    - /Users/1.PlumeModels/ISC/Building_Profile_Input_Program/eg1、eg2
    - /Users/1.PlumeModels/ISC/BPIPPRM/eg1、eg2