---
layout: default
title: TEDS Python
nav_order: 6
has_children: true
permalink: /EmisProc/
last_modified_date:   2021-12-01 11:24:33
tags: CAMx emis ptse REAS TEDS
---

# TEDS排放處理相關程式

除了準備光化模式所需要的排放檔案，此處也介紹排放數據的展示、檢視等等經驗。
- 處理對象以全臺範圍的[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)。臺灣地區以外的東亞範圍，此處以[REAS](https://www.nies.go.jp/REAS/)資料庫為分析對象，另見[隔壁](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/REAS)。
- 程式以2018年以來持續發展之`python`平行處理程式為主。

## 背景

### 相依性處理策略原則及目標
由於環保署提供數據僅有年度總量，並非光化模式所需之逐時數據，因此須考慮各細類污染源的時間特性，而該特性也有行政區的空間性質，因此資料庫維度之間有著非常高的相依性，需逐一展開。
- 考慮因素：電腦記憶體限制。如果資料太長(全年處理)將會使電腦停擺無法計算。
- 計算效率：應用矩陣將可啟動[平行計算](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/#numpyscipy的平行運作)減少計算時間，資料越長越省事
- 檔案儲存：減少檔案存取的次數及規模。此處以**一月儲存一檔**為原則(直接適用CAMx模式)。

### 解決方案比較
目前可行、營運中之系統方式包括使用[SMOKE](https://www.cmascenter.org/smoke/)(`fortran`)、自行撰寫`fortran`、與`python`程式等系統方式，比較如下：
- 程式可讀性、模組化、長遠發展可維護性：`fortran`不如`python`
- 平行運作：理論上`fortran`應有最好的平行計算特性，但目前尚未發展這一方面，反倒是`python`可以啟動單機之平行計算(`smp`)。
- [TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)適應性：[SMOKE](https://www.cmascenter.org/smoke/)為美國系統，編碼方式修改、適應不易、事倍功半，如遇改版將遭遇困難。
  - 每年版本的[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)仍會有少部分不一樣，排放模式系統應有調適的能力
  - 行政區代碼、排放類別代碼、碳鍵機制物種等等，都有更新的需求
  - `fortran`無法直接讀取`dbf`檔案，只能讀取`sdf`檔案，[TEDS11](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)以後環保署不再提供詳細面源資料庫之`sdf`檔案格式，`sdf`只有網格加總結果。還是需要轉檔。

## 處理程序總綱
- 資料庫[轉檔](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，`dbf` to `csv`。
- 應用[資料表與矩陣的互換](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/#資料表與矩陣的互換)工具，整理全年時間變化係數(**時變係數**)矩陣、存檔備用。
- 讀取排放總量檔案、污染項目之彙總、展開形成**總量**`TPY[nSP, nCNTY,nNSC, nYX]`矩陣
- 時間之展開：**總量**`X`**時間係數**(`numpy.tensordot`)
- 空間之整併：按照模式的網格系統進行**加總**(`pandas.pivot_table`)
- 填入nc檔案

## numpy/scipy的[平行運作](https://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html)
- 基本上numpy使用“BLAS”（基本線性代數副程式）來獲得優化。這通常是一個經過精心調整的程式庫，通過利用個別電腦高速緩存和組合，實現計算速度的提升。
- 現在許多電腦架構本身都有自己的 BLAS，它會利用了多核機器。如果 numpy/scipy 是使用其中之一編譯的，則矩陣計算(如`dot`)將採平行計算（如果速度確實更快），**使用者無需執行任何操作**。
- 類似的其他矩陣運算，如反矩陣、張量內積、奇異值分解、行列式等。
- 此外如開源庫 ATLAS 允許在編譯時選擇平行級別（線程數）。英特爾專有的 MKL 庫亦提供了在運行時選擇並行級別的可能性。還有 GOTO 庫，允許在運行時選擇並行級別。這些有部分是商業產品，但向學術界可免費提供程式碼。

{: .fs-6 .fw-300 }

---

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1
- National Institute for Environmental Studies, **Regional Emission inventory in ASia (REAS) Data Download Site**,  [nies](https://www.nies.go.jp/REAS/), 29-October-2020
- AMArchibald, Unknown[153], Unknown[154], Unknown[155], MartinSpacek, Pauli Virtanen, **Parallel Programming with numpy and scipy**, [scipy-cookbook](https://scipy-cookbook.readthedocs.io/items/ParallelProgramming.html), 2015-10-30