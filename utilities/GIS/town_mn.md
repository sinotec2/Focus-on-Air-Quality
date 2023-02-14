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

- 雖然檔案是網格化之nc檔，卻不必然是網格模式需要的前後處理程序(雖然[公版模式](../../GridModels/TWNEPA_RecommCMAQ/post_process/Air_Increment.md)之[Air_Increment][Air_Increment]確實有處理這題)，也不隸屬於某個特定的模式(標籤將所有的類網格模式都標上去)，看來這項工作不適合放在哪一項網格模式項下。
- 而就GIS而言，網格模式的格距解析度似乎又太大，不是一般GIS軟體處理的題目。
- 引此類工作在網格系統改變、行政區域劃分更新等等狀況，都會需要更新計算程式，所以放在GIS項下應該比較容易找到。

### 策略選擇

- 直覺上選擇以矩陣來解決網格的樞紐問題似乎是一個最好的選項。因此過去如[mk_town.py][mk_town.py]使用np.dot。
  - 好處是使用網格分率計算精確、使用np.dot有其平行計算的強處
  - 壞處是網格系統或行政區改變時，其用網格模板儲存的行政區分率就必須重作，而該模板因變數多達380餘項，有點難度。
- 將2為網格線性化後，直接使用pandas.pivot_table進行樞紐計算。
  - 好處：配合geopandas的[前處理](mk_gridLL)結果就是以線性化儲存的格式。[該程式][mk_gridLL]預設的結果不需要也不會產生nc之模板。程式([])也較精簡。
  - 壞處：(尚未發生)

## [mk_town.py][mk_town.py]使用說明

[Air_Increment]:  "空品增量模擬工具(Air_Increment_tool)-縣市最大值分析"
[mk_town.py]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/town_mn.py "網格濃度在行政區範圍內之平均"
[mk_gridLL]: mk_gridLL "行政區範圍格點化"
