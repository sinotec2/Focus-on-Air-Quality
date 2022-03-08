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
- 目的：計算煙囪附近建築物的長、寬、高等尺寸，以便ISCST3/AERMOD等模式可以引用。
- [BPIP]()全名為Building Profile Input Program。[BPIPPRM]()則是專為ISC-PRIME模組及AERMOD之預備。
- USEPA官網之說明
	- [BPIP]()是一個PC/Linux 上的應用程式，旨在納入煙囪設計之「良好工程實務(GEP)」精神內涵（詳技術支援文檔《確定良好工程實務準則之煙囪高度（PDF）》101 pp，1985年，建築物下沖計算指南以及其他相關參考）。
  - 經由此一程式，使用者可以正確計算簡單、多層或多組結構的建築物高度((BUILDHGT)和建築物橫向的寬度（BUILDWID）或煙流方向切建築物的長度（BUILDLEN）。 
  - 該程序通常與ISC3模型一起使用。[BPIP]()的最新版本4/21/2004已使用fortran可分配陣列進行了升級，提高了程式維度的自由，同時保持了原有程式的基本功能。
	- [BPIPPRM]()與[BPIP]()相同，但包括特別升級的算法（P），應用於產生PRIME算法計算煙流下沖之輸入條件，PRIME模組目前已經包含在AERMOD等模型中。
  - [BPIPPRM]()的輸入結構與[BPIP]()的輸入結構相同，後者則經常與ISC3模型一起使用。 有關更多信息，請參見《BPIP用戶手冊》。

## 設定步驟與內容

### 步驟
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
1. 按照範例之模板輸入D, (X,Y), E, H等數據，存檔、上傳工作站。
1. 執行[BPIP]()批次檔run_bpip.sh A1P.INP A1P.OUT A1P.SUM
1. 將OUT檔案中的SO 參數，貼在AERMOD的執行控制檔內

| ![BPIP1.png](/Focus-on-Air-Quality/raw/main/assets/images/BPIP1.png)|
|:--:|
| <b>從衛星圖中找到廠區座標軸、夾角、與廠房頂點XY值</b>|

## Reference
- BPIP/BPIPPRIM美國環保署[官方網址](https://www.epa.gov/scram/air-quality-dispersion-modeling-related-model-support-programs#bpip)
- 原始碼
  - [BIPI原始碼](https://www3.epa.gov/ttn/scram/models/relat/bpip.zip)
  - [BPIPPRM原始碼](https://www3.epa.gov/ttn/scram/models/relat/bpipprime.zip)
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
- 有關煙流下洗的現象、原因、以及如何避免，可以參考下列網址
  - https://www.youtube.com/watch?v=bgoU9GTNYHs
  - https://www.youtube.com/watch?v=qQJRSrfv8eQ
  - https://www.youtube.com/watch?v=UkV2JHg9CX8
  - https://www3.epa.gov/ttn/scram/11thmodconf/presentations/3-6_Building_Downwash-CPP-11thMC.pdf