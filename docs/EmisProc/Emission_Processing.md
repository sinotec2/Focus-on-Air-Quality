---
layout: default
title: Emission Processing
nav_order: 5
has_children: true
permalink: /docs/EmsProc/
last_modified_at:   2021-12-01 11:24:33
---

# 排放處理相關程式

除了準備光化模式所需要的排放檔案，此處也介紹排放數據的展示、檢視等等經驗。
- 處理對象以全臺範圍的[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)、以及東亞範圍的[REAS](https://www.nies.go.jp/REAS/)為主。
- 程式除早期發展的`fortran`(無平行化)，以及持續發展之`python`平行處理程式。

## 背景

### 解決方案比較
目前可行、皆為營運中之系統方式包括使用[SMOKE](https://www.cmascenter.org/smoke/)(`fortran`)、自行撰寫`fortran`、與`python`程式等系統方式，比較如下：
- 程式可讀性、模組化、長遠發展可維護性：`fortran`不如`python`
- 平行運作：理論上`fortran`應有最好的多工運作特性，但目前尚未發展這一方面，反倒是`python`可以多工
- [TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)適應性：[SMOKE](https://www.cmascenter.org/smoke/)為美國系統，編碼方式修改、適應不易、事倍功半，如遇改版將遭遇困難。
  - 每年版本的[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)仍會有少部分不一樣，排放模式系統應有調適的能力
  - 行政區代碼、排放類別代碼、碳鍵機制物種等等，都有更新的需求
  - fortran無法直接讀取dbf檔案，只能讀取sdf檔案，[TEDS11](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)以後環保署不再提供詳細面源資料庫之sdf檔案格式，sdf只有網格加總結果。還需轉檔。

### 相依性處理策略原則
- 考慮因素：電腦記憶體限制。如果資料太長將會使電腦停擺無法計算。
- 計算效率：應用矩陣將可啟動平行計算減少計算時間
- 檔案儲存：減少檔案存取的次數及規模。此處以一月儲存一檔為原則。

### 處理程序總綱
- 整理時間變化係數檔案(形成fac[nCNTY,nNSC, NTm]矩陣)
- 讀取排放總量檔案、污染項目之彙總、展開形成TPY[nSP, nCNTY,nNSC, nYX]矩陣
- 時間之展開：總量X時間係數(numpy.tensordot或pandas.pivot_table)
- 空間之整併：按照模式的網格系統進行
- 填入nc檔案

{: .fs-6 .fw-300 }

---

## Reference
-行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1

