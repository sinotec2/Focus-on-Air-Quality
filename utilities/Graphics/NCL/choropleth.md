---
layout: default
title: 行政區範圍等值圖
parent: NCL Programs
grand_parent: Graphics
has_children: true
date: 2023-01-26
last_modified_date: 2023-01-26 19:14:20
tags: NCL graphics choropleth
---

# 行政區範圍等值圖
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

### 前言

- 以行政區為等值圖範圍的數據圖稱之為[choropleth](https://en.wikipedia.org/wiki/Choropleth_map)，為模式重要的後處理形式之一。
- 繪製等值圖的方式不是很多，其中還涉及繪圖品質、互動方式、輸入檔案格式、以及支援資源是否充分等因素，此處以[NCL（NCAR Command Language）](https://www.ncl.ucar.edu/)的網站服務方式(CaaS)，提供解決方案。

### 應用需求與目標

等值圖的應用包括：

- 行政區域平均值與標準之比較，來源可能是行政區內的
  - 測站值、或其內插值、
  - 模式模擬結果等，
- 等值線圖之行政區範圍平均，模式網格解析度太高、或解析度不足時、模擬網格系統定義不同時，轉以行政區為空間代表特性。
  - 模式輸出檔案一般以netCDF格式最為常見。（客戶較少）
  - 表列行政區特性值之空間展示：來源可能是含有行政區代碼、與特性數值之csv檔案（潛在客戶較多）

台灣地區鄉鎮區代碼

- 舊碼為4碼（縣市代碼2碼01～51、2碼該縣市下之鄉鎮區碼01～）
- 新碼為8碼（縣市代碼5碼09007~68000、該縣市下之鄉鎮區碼3碼001～）

作業要求包括：

    報告品質
    重複性高，作業流程需程式化
    避免繁雜設定

### 解決方案比較

目前製作等值圖的軟體並不多，檢討如下：

- VERDI：品質不高，可接受CAMx/IOAPI 之nc檔案，不能接受csv檔案。可流程化、但不能相容於CaaS。
- SURFER：高品質。舊版mapviewer 可以製作等值圖，目前surfer必須執行basic程式，每個多邊形元素著色。或能相容於CaaS。
- NCL：高品質。因為沒有介面軟體，為獨立的執行程式，因此作業流程、設定均為最複雜。然而也是最能相容於CaaS之系統。
  - NCL容許較大的截尾錯誤，8碼的行政區代碼在netCDF檔案系統中偶會讀錯，解決方案
  1. 大數必須先行減少有效位數、且以字元形式，才能正確進行比較。
     - NCL/netCDF內設實數是32bit，因此8碼會有問題(4*8=32)，網友建議宣告成64bit整數
     - 因行政區代碼只用於比較，並沒有其他計算，且事先切分也較符合作業邏輯。
  2. 避免使用netCDF檔案存取TOWNID，改採csv檔案形式。

### 解決方案規劃

- 由網頁獲知客戶要處理的檔案路徑名稱
- 執行cgi_python進行新舊代碼之辨識、對照、執行NCL程式、將結果自動下載到客戶端的Downloads目錄
- ncl腳本：參考DKRZ的作法[^1]，在shape檔範圍內填入彩虹色階(如[下圖][tmp])。

![](https://docs.dkrz.de/_images/plot_DEU_adm3_avg_over_counties_COAST_w400.png)

## NCL程式說明

### 程式碼下載

{% include download.html content="[行政區範圍等值圖NCL程式stw.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/stw.ncl)" %}

### IO

- `input.csv`
  - 無檔頭、無行號之csv檔案
  - 以逗號區分3欄：分別為縣市、鄉鎮區、數值
  - 由cgi-python整理更名
- `TWN_adm/tas1.nc`：界定縣市代碼之經緯度座標
- shape圖檔(內政部官網提供之shape檔)
  - `/var/www/html/taiwan/TWN_adm/TOWN_MOI_1090727.shp`：鄉鎮區分界圖
  - `/var/www/html/taiwan/TWN_adm/COUNTY_MOI_1090820.shp`：縣市分界圖
- `shapefile_3.png`：將在cgi-python中予以更名成使用者供「csv檔名」.png

### 副程式avg_by_town

- 此副程式會計算個別行政區之濃度平均值。呼叫方式

```python
var_avg1 = avg_by_town(wks, map, var_regrid, shpf3, county_name(k), \
    wtowns1, levels, colors)
```

- 引數
  - wks：drawing instance
  - map: plot instance
  - var_regrid: 網格系統
  - shpf3：shape file
  - county_name：需取平均值之鄉鎮區代碼
  - wtowns1：indices of towns
  - levels：濃度等級定義
  - colors：濃度色階
- 回復值：平均值var_avg1

{% include download.html content="[行政區範圍內數據之平均avg_by_town.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/avg_by_town.ncl)" %}

### 色階設定

- 21層
- 按照最大、最小值的冪次方差異(`diffE=abs(log10(abs(var1_mx))-log10(abs(var1_mn)))`)決定
- 差異小或等於1：採線性區分
- 按照濃度大小順位設定間隔，以使各個間距的結果範圍相差不大。

## 應用

- [衍生性污染物健康風險評估之基本調查](../../../PaperReview/Disease/HRA_PMnO3/2HRA_Factors.md)
- [開發計畫衍生性污染物健康風險評估](../../../PaperReview/Disease/HRA_PMnO3/3HRA_Forecast.md)
[^1]:  NCL examples, DKRZ System, Deutsches Klimarechenzentrum GmbH.(德國氣候數據中心),  [DRKZ][DRKZ]，NCL範例詳[shapefile mean temperature change German coast example][tmp]

[DRKZ]: https://docs.dkrz.de/doc/visualization/sw/ncl/index.html "德國氣候數據中心"
[tmp]: https://docs.dkrz.de/doc/visualization/sw/ncl/examples/source_code/dkrz-ncl-shapefile-mean-temperature-change-german-coast-example.html "DKRZ NCL shapefile mean temperature change German coast example"