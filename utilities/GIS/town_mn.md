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

- 雖然檔案是網格化之nc檔，卻不必然是網格模式需要的前後處理程序(雖然[公版模式](../../GridModels/TWNEPA_RecommCMAQ/post_process/4.Air_Increment.md)之[Air_Increment][Air_Increment]確實有處理這題)，也不隸屬於某個特定的模式(標籤將所有的類網格模式都標上去)，看來這項工作不適合放在哪一項網格模式項下。
- 而就GIS而言，網格模式的格距解析度似乎又太大，不是一般GIS軟體處理的題目。
- 引此類工作在網格系統改變、行政區域劃分更新等等狀況，都會需要更新計算程式，所以放在GIS項下應該比較容易找到。

### 策略選擇

- 直覺上選擇以矩陣來解決網格的樞紐問題似乎是一個最好的選項。因此過去(2021/10)如[town_mn.py][town_mn.py]使用np.dot。
  - 好處是使用網格分率計算精確、使用np.dot有其平行計算的強處。使用與CMAQ/ISAM之[gridmask](../../GridModels/ISAM/run_isamMM_RR_DM.md)相同檔案。
  - 壞處是網格系統或行政區改變時，其用網格模板儲存的行政區分率就必須重作，而該模板因變數多達380餘項，有點難度。
- 將2為網格線性化後，直接使用pandas.pivot_table進行樞紐計算。
  - 好處：配合geopandas的[前處理](mk_gridLL)結果就是以線性化儲存的格式。[該程式][mk_gridLL]預設的結果不需要也不會產生nc之模板。程式([nc2town.py][nc2town.py])也較精簡。
  - 壞處：(同一網格沒有不同行政區之分率)

## [town_mn.py][town_mn.py]使用說明

### IO_town_mn

- 引數：網格濃度nc檔案名稱
- nc檔案：變數的維度需有4階，程式只會處理第1個變數，nc檔案的網格系統需與前處理TWN_TOWN_3X3.nc一致。
- TWN_TOWN_3X3.nc(ISAM gridmask版本)
  - 見[mk_town.py][1]及[mk_town][mk_town]的說明
  - 與20160101.ncT(CAM-chem處理版本)是同一個檔案
- 結果csv檔案

## [nc2town.py][nc2town.py]程式說明

### IO_nc2town

- 引數：網格濃度nc檔案名稱
- nc檔案：變數的維度需有4階，程式只會處理第1個變數，nc檔案的網格系統需與前處理[mk_gridLL][mk_gridLL]一致。
- gridLL.csv：見[mk_gridLL][mk_gridLL]的說明
- 結果csv檔案

```csv
kuang@master /nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001
$ head A2019.ncT.csv
TOWNCODE,var,COUNTYCODE,COUNTYNAME,TOWNNAME
64000060,26.294521,64000,高雄市,新興區
64000080,26.263927,64000,高雄市,苓雅區
66000010,26.109589,66000,臺中市,中區
64000100,25.98767,64000,高雄市,旗津區
64000050,25.822897,64000,高雄市,三民區
64000090,25.459818,64000,高雄市,前鎮區
64000120,25.421614,64000,高雄市,鳳山區
64000110,25.276712,64000,高雄市,小港區
66000050,25.225832,66000,臺中市,北區
```

### 計算細節

- 負值之篩除
  - 一般模式並不會有負值的濃度，但LGHAP只分析陸地上濃度，海上值則將其遮蔽。
  - 處理過程中將其令為負值，因此平均時需將其剔除。
- 沒有網格分率
  - 網格落在哪一個行政區是0/1的差異，並不像[town_mn.py][town_mn.py]有計算分率(解析度1公里)，因此計算結果會有差異。

### 程式原始碼下載

{% include download.html content="網格濃度在行政區範圍內之平均[town_mn.py][town_mn.py]" %}
{% include download.html content="網格濃度在行政區範圍內之平均[nc2town.py][nc2town.py]" %}

[Air_Increment]:  "空品增量模擬工具(Air_Increment_tool)-縣市最大值分析"
[town_mn.py]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/town_mn.py "網格濃度在行政區範圍內之平均"
[mk_gridLL]: mk_gridLL "行政區範圍格點化"
[nc2town.py]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/GIS/nc2town.py "網格濃度在行政區範圍內之平均nc2town.py"
[1]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/mk_town.py "mk_town.py"