---
layout: default
title: 網格濃度在行政區範圍內之平均
parent: GIS Relatives
grand_parent: Utilities
date: 2023-02-14
last_modified_date: 2023-02-14 10:18:47
tags: choropleth GIS CMAQ CAMS CAM-chem LGHAP MOZART
---

# 網格濃度在行政區範圍內之平均

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

> 在網格濃度前後處理過程中，常常會需要計算行政區(鄉鎮、縣市、空品區)空間範圍內之平均值。

### 從屬與歸併

- 雖然檔案是網格化之nc檔，卻不必然是網格模式需要的前後處理程序(雖然[公版模式][Air_Increment]確實有處理這題)，也不隸屬於某個特定的模式(標籤將所有的類網格模式都標上去)，看來這項工作不適合放在哪一項網格模式項下。
- 而就GIS而言，網格模式的格距解析度似乎又太大，不是一般GIS軟體處理的題目。
- 引此類工作在網格系統改變、行政區域劃分更新等等狀況，都會需要更新計算程式，所以放在GIS項下應該比較容易找到。

### 策略選擇

- 直覺上選擇以矩陣來解決網格的樞紐問題似乎是一個最好的選項。因此過去如[mk_town.py][mk_town.py]、

[Air_Increment]: ../../GridModels/TWNEPA_RecommCMAQ/post_process/Air_Increment.md "空品增量模擬工具(Air_Increment_tool)-縣市最大值分析"
[mk_town.py]: 