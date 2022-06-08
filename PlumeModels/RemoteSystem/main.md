---
layout: default
title: ISCST/AERMOD 主程式
parent: Remote Processing
grand_parent: Plume Models
nav_order: 6
last_modified_date: 2022-03-07 15:17:07
---
# ISCST/AERMOD 主程式
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
### instance
- 煙流模式主程式的[遠端計算](http://114.32.164.198/AERMOD.html)網頁。
- 主要服務那些已經準備好各項輸入檔案的使用者，Javascripts將會讀取使用者提供的檔案存到伺服器上(至少2個檔案、最多4個檔案)，並啟動CGI_Python程式進行煙流模式的遠端計算與監看。
  - 如果需要前處理([氣象](http://114.32.164.198/mmif.html)、[地形](http://114.32.164.198/terrain.html)等)、或後處理([kml](http://114.32.164.198/Leaflet/docs/index.html)、[NCL](http://114.32.164.198/NCLonOTM.html))，可以回到[遠端模擬首頁](http://114.32.164.198/aermods.html)
  - 監看網頁位置
    - aermod：[http://114.32.164.198/isc_results/arem_RAND/prog.html](http://114.32.164.198/isc_results/arem_RAND/prog.html)
    - iscst：[http://114.32.164.198/isc_results/isc3_RAND/prog.html](http://114.32.164.198/isc_results/isc3_RAND/prog.html)
  - 服務僅限模式計算，後處理部分讓使用者視需要自行下載結果檔案，再啟動其他程式進行處理、繪圖。
- 服務僅限模式計算，後處理部分讓使用者視需要自行下載結果檔案，再啟動其他程式進行處理、繪圖。

### 計算時間超過網頁停等容許時間的策略。
- 此處不採取bash scripts定期檢視郵寄結果策略，一般郵件伺服器會認為沒有domain name的ip是垃圾信。而是
- 直接限制總執行緒
  - 讓工作站優先服務先提出submit的使用者，
  - 使用者可以經由短暫的等待得到結果、或由網頁提供的連結，自行檢視工作站的執行進度。
### 檔案架構
- $web/AERMOD.html
- $cgi/isc/AERMOD.py
- models:
  - `AERMOD='/Users/1.PlumeModels/AERMOD/aermod_source/aermod.exe'`
  - `ISCST3='/Users/1.PlumeModels/ISC/short_term/src/iscst3.exe'`
  - `DAT2KML=/opt/local/bin/dat2kml.py`
- wait and see
  - $web/isc_results/waitc.cs
  - $web/isc_results/demo/
    - refresh.html
    - done.html
- working directories
  - aermod: $web/isc_results/arem_ **RAND**
  - iscst: $web/isc_results/isc3_ **RAND**

## HTML
### 設計
- 以表格方式整理模擬過程、各程序之程式版本、內容、IO及範例、檢核方式以及筆記。
- 提交CGI_python物件
  - `4個檔案`：依序為run stream、氣象檔(AERMOD會需要獨立的高空數據檔)、以及(或)複雜地型時需要的地形檔。
  - `model`：模式之選項，ISCST或AERMOD二擇一

| ![isc_aermod.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/isc_aermod.png)|
|:--:|
| <b>isc_aermod主程式[遠端執行](http://114.32.164.198/AERMOD.html)界面</b>|


### Coding
- [AERMOD.html](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/AERMOD.html)
- [autorefresh.html](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/HTML/autorefresh/)

## CGI_PYTHON
- [AERMOD.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/AERMOD.py)
- [程式設計說明](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/AERMOD/)
