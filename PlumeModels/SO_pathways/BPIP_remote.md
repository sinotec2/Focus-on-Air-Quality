---
layout: default
title: BPIP遠端執行
parent: SO Pathways
grand_parent: Plume Models
nav_order: 3
last_modified_date: 2022-06-08 11:33:42
---
# BPIPPRM之[遠端計算服務](http://114.32.164.198/BPIPPRIM.html)範例
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
- 由於[BPIPPRM]()並沒有長時間的積分計算，因此其計算對工作站而言較為容易。
- 比較繁雜的程序是座標、夾角的量測、旋轉平移的計算。
  - 然其描圖、座標平移則需依賴許多python模組，以及Fortran的編譯，都會需要與作業系統持續保持更新。
- 細部CGI-python程式設計詳見[bpipprim.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/bpipprim/)之說明。

### CaaS的作業方式
  1. 先在地圖[數位板](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/digitizer)上點選煙囪及建築物頂點位置、存成[kml檔案](http://114.32.164.198/isc_results/ZhongHuaPaper/paper.kml)(大致上取代前述[步驟1-4][步驟1-4]，結果詳下圖1)
  1. 利用[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式將kml檔案旋轉成廠區座標系統，並另存[BPIPPRM]()的[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，即為前述[步驟5-7][步驟5-7]，確認如下圖2。
  1. 執行[BPIPPRM](http://114.32.164.198/BPIPPRIM.html)計算([步驟8][步驟8])
  1. [ISCPARSER](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)解讀器會將BPIP.INP內容讀成圖像(kml檔案)，然須在輸入檔的第一行(標題說明)找到廠區的原點位置，座標系統為TWD97，單位為m，詳見[污染源空間解讀器-建築物之設定](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser/#建築物之設定)說明，範例如：

```
'BPIP input file with 1 bldg and 1 stacks,originated at [170249.3,2531503.5](TWD97m).'	
```

| ![BPIP3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP3.png)|
|:--:|
| <b>圖1實例廠區數位化結果，雖然數位板點選結果有些歪斜，[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式會將其均化修正</b>|
| ![BPIP4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP4.png)|
| <b>圖2實例廠區[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)旋轉後之[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，經[ISCPARSER](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)解讀結果</b>|



### [遠端計算服務](http://114.32.164.198/BPIPPRIM.html)實例

| ![BPIPPRIME.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIPPRIME.PNG)|
|:--:|
| <b>圖3建築物前處理(BPIPPRIME)遠端計算服務實例之畫面</b>|


## 檔案架構
- EXE：`BPIP='/Users/1.PlumeModels/ISC/BPIPPRM/bpipprm'`
- HTML：$web/[BPIPPRIM.html](https://github.com/sinotec2/CGI_Pythons/blob/main/bpipprim/BPIPPRIM.html)
- CGI-PY：$cgi/isc/[bpipprim.py](https://github.com/sinotec2/CGI_Pythons/blob/main/bpipprim/bpipprim.py)、詳[說明](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/bpipprim/)。
- 輸入檔
  - BPIP input file：BPIP.INP (from html, filename not limited)
  - CGI wabpage header：$cgi/isc/[header.txt](https://github.com/sinotec2/CGI_Pythons/blob/main/bpipprim/header.txt)
- 輸出檔
  - 工作目錄：$web/isc_results/bpip__ **RAND**/
  - build.txt(SO listings, used to paste into the runstream INP file)
  - fort.12(Process results)
  - fort.14(Execution Summary, GEP checking)
- **RAND**為隨機產生之6碼文字

## 結果&討論
- 執行結果檔案連結(範例)
  - 
```
filename given and save as: fort.10

BPIPPRIN_results: The download process should start shortly. If it doesn't, click:

build.txt fort.12 fort.14
```

- [BPIPPRM]()計算結果詳見[build.txt](http://114.32.164.198/isc_results/ZhongHuaPaper/build.txt)，貼在模式輸入檔的[範例](http://114.32.164.198/isc_results/ZhongHuaPaper/paper1pa_NOX.inp)內([步驟9][步驟9]))
- TODO
  - BPIPPRIME即將被[PRIME2][Petersen and Guerra 2018]所[取代][官方立場]，其前處理方式、AERMOD內之設定方式等，尚待進一步瞭解。

## Reference
- Petersen, R. L. and Guerra, S. A., (2018). PRIME2: [Development and evaluation of improved building downwash algorithms for rectangular and streamlined structures](https://www.sciencedirect.com/science/article/abs/pii/S0167610517306669). Atmospheric Environment, 173, 67-78.
- USEPA, [Building Downwash Alpha Options in AERMOD](https://www.epa.gov/scram/aermod-modeling-system-development-documents), www.epa.gov, downwash_alpha_options_white_paper, 05-13-2019

[Petersen and Guerra 2018]: <https://www.sciencedirect.com/science/article/abs/pii/S0167610517306669> "Petersen, R. L. and Guerra, S. A., (2018). PRIME2: Development and evaluation of improved building downwash algorithms for rectangular and streamlined structures. Atmospheric Environment, 173, 67-78."

[官方立場]: <https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/2Building/#建築物下洗模擬的官方立場> "Building Downwash Alpha Options in AERMOD, www.epa.gov, downwash_alpha_options_white_paper, 05-13-2019"

[步驟1-4]: <https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容> "步驟1找到平面配置圖。步驟2定義局部座標軸、夾角角度D。步驟3~4量測頂點座標之X,Y值。"

[步驟5-7]: <https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容> "步驟5量測建築物及煙囪基地高程E。步驟6量測離地高度H。步驟7按照模板輸入數據、存檔、上傳。"

[步驟8]: <https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容> "步驟8執行BPIP批次檔run_bpip.sh A1P.INP A1P.OUT A1P.SUM"

[步驟9]: <https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容> "步驟9、將OUT檔案中的SO路徑及參數，貼在ISCST或AERMOD的執行控制檔內。ISCST不接受BPIPPRM結果之BUILDLEN、XBADJ、YBADJ等參數，必要時在結果檔中去除之，重新執行BPIPPRM但將設定P改為ST(short time)，或重新執行BPIP"