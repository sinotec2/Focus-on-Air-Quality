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
- CaaS的作業方式：
  1. 先在地圖[數位板](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/digitizer)上點選煙囪及建築物頂點位置、存成[kml檔案](http://114.32.164.198/isc_results/ZhongHuaPaper/paper.kml)(大致上取代前述[步驟1\~4](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容)，結果詳下圖1)
  1. 利用[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式將kml檔案旋轉成廠區座標系統，並另存[BPIPPRM]()的[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，即為前述[步驟5\~7](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容)，確認如下圖2。
  1. 執行[BPIPPRM]()計算([步驟8](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容))
- 細部操作方式與CaaS程式設計詳見[bpipprim.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/bpipprim/)之說明。

| ![BPIP3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP3.png)|
|:--:|
| <b>圖1實例廠區數位化結果，雖然數位板點選結果有些歪斜，[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)程式會將其均化修正</b>|
| ![BPIP4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIP4.png)|
| <b>圖2實例廠區[rotate_kml](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/rotate_KML)旋轉後之[輸入檔](http://114.32.164.198/isc_results/ZhongHuaPaper/fort.10)，經[ISCPARSER](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)解讀結果</b>|

- [BPIPPRM]()計算結果詳見[build.txt](http://114.32.164.198/isc_results/ZhongHuaPaper/build.txt)，貼在模式輸入檔的[範例](http://114.32.164.198/isc_results/ZhongHuaPaper/paper1pa_NOX.inp)內(步驟9.)

### [遠端計算服務](http://114.32.164.198/BPIPPRIM.html)實例

| ![BPIPPRIM.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/BPIPPRIM.PNG)|
|:--:|
| <b>圖3遠端處理實例之畫面</b>|