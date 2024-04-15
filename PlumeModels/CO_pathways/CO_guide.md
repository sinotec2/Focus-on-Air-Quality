---
layout: default
title: AERMOD模式執行之控制
parent: CO Pathways and Compilation
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2024-04-12 16:02:23
tags: plume_model
---

# AERMOD模式執行之控制

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

- 環境部空氣品質模式支援中心
  - [高斯擴散模式AERMOD使用規範(2023.11.20).pdf](https://aqmc.moenv.gov.tw/download/AERMOD/01/高斯擴散模式AERMOD使用規範(2023.11.20).pdf)
  - [AERMOD 模式中文操作手冊(2022.12.30)](https://aqmc.moenv.gov.tw/download/AERMOD/01/AERMOD模式中文操作手冊(2022.12.22).pdf)

## CO設定說明

|範例|說明
:-|:-
CO STARTING|段落開始(須)
CO TITLEONE A Simple Example...|不接受中文字
CO **MODELOPT** DFAUT CONC ELEV|法規使用(DFAUT)、CONC/DEPOS、ELEV/FLAT
CO AVERTIME 3 24 PERIOD|平均時間區間
CO POLLUTID SO2|汙染物名稱(須)、表列名稱以外：OTHER
CO RUNORNOT RUN|是否執行或僅初步檢查
CO FLAGPOLE 1.5|離地高度
CO ERRORFIL ERROR.OUT|錯誤訊息檔名
CO FINISHED|段落結束(須)

### MODELOPT

在AERMOD模型中，`MODELOPT` 是一個重要的關鍵字，用於設定模型的運作控制和擴散選項。以下是`MODELOPT`的一些主要設定方式：

1. **DFAULT**：使用模式的預設值。
2. **CONC**：計算濃度。
3. 沉降量計算
  - **DEPOS**：計算總沉降通量，包括乾沉降和濕沉降。
  - 是否計算削減量
    - **DRYDPLT** 和 **WETDPLT**：分別計算乾沉降和濕沉降所致的煙流消減。
    -  **NODRYDPLT** 和 **NOWETDPLT**：停用計算乾沉降和濕沉降所致的煙流消減。
4. 地形設定
   - **ELEV**：假設複雜地形、需要讀取地形設定。
   - **FLAT**：假設平坦地形。
5. **SCREEN**：在篩選模式下運行AERMOD。
6. **VECTORWS**：輸入風速是向量平均風速，不是純量平均風速。

### FLAGPOLE

- 在AERMOD模型中，`FLAGPOLE`關鍵字用於設定受體點的高度，這是指受體點離地面的高度。
- 這個設定允許模型考慮地面以上一定高度的空氣品質，這對於建築物或其他結構附近的空氣品質評估尤為重要。
- 具體來說，當您使用`FLAGPOLE`關鍵字時，您可以設定一個數值代表受體點離地面的高度（單位為公尺）。
- 如果沒有提供具體的數值，則默認值為0.0m，即受體點位於地面。這個參數的設定是在輸入控制檔中的`FLAGPOLE`條目後，直接跟隨高度值來進行的。

GTPs by yachun chiao [AERMOD Helper](https://chat.openai.com/g/g-REsU1hWpG-aermod-helper)