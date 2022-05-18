---
layout: default
title: 高斯模式及穩定度
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 1
last_modified_date: 2022-05-16 09:42:56
---

# 高斯模式及大氣穩定度
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

## 大氣紊流的特性
### 局布尺度
- 時間
  - 瞬時 ~ 小時
  - quasi-steady state
- 空間
  - 100M ~ 10 Km  
  - homogenesis：空間中的紊流強度為定值(不隨高度、橫方向改變)
- 紊流擴散(Turbulent Diffusion)現象為主、[延散(Dispersion)](https://terms.naer.edu.tw/detail/1317622/?index=2)為輔

| ![Gaus.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Gaus.PNG)|
|:--:|
| <b>不同延時之煙流形狀與平均濃度([Slade 1968][Slade 1968])</b>|

[Slade 1968]: <https://www.osti.gov/biblio/4492043> "D. H. Slade, Meteorology and Atomic Energy—1968, USAEC Report TID-24190, 1968."

### 中尺度
  - 50 Km ~ 500 Km
  - 數小時 ~ 數日
  - 受延散現象、地區環流、地形效應控制為主

| ![calpuff_PMF.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/calpuff_PMF.PNG)|
|:-:|
| <b>CALPUFF模擬結果GIF檔展示畫面([臺灣未來3天火力機組空品影響預報](https://sinotec2.github.io/cpuff_forecast/))</b>|

## 大氣垂直穩定度與連續煙流之形狀

- 煙流形狀與大氣穩定度
  - 左側各圖分別為風速、溫度、無因次水平及垂直風速標準差(紊流強度)之垂直變化
  - 右側則為連續煙流之平面、垂直形狀
  - Source: [Pendergast 1984][Pendergast 1984] in [Atmospheric science and power production][Randerson 1984]

[Pendergast 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Malcolm M. Pendergast, 1984, Chap. 2, METEOROLOGICAL FUNDAMENTALS, in Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."

[Randerson 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Randerson, D. (1984). Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."

### 穩定大氣
- 溫度傾率 &gt; 絕熱傾率、逆溫、等溫
- 不存在高層逆溫層：Fanning

| ![plumes_1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/plumes_1.PNG)|
|:-:|
| <b>穩定大氣與Fanning</b>|

- 高層逆轉：Lofting

| ![plumes_2.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/plumes_2.PNG)|
|:-:|
|<b>穩定大氣與Lofting</b>|

### 中性大氣
- 溫度傾率 = 絕熱傾率。是否存在高層逆溫層
- 存在高層逆溫層：Fumigation


| ![plumes_3.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/plumes_3.PNG)|
|:-:|
|<b>中性大氣並高層逆溫：Fumigation</b>|

- 不存在高層逆溫層：Coning

| ![plumes_4.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/plumes_4.PNG)|
|:-:|
|<b>中性大氣無高層逆溫：Coning</b>|

### 不穩定大氣
- 溫度傾率 &lt; 絕熱傾率、逆溫、等溫
- Looping

| ![plumes_5.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/plumes_5.PNG)|
|:-:|
|<b>不穩定大氣：Looping</b>|

### 混合層日變化與煙流地面濃度

| ![Yamada1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Yamada1.PNG)|
|:-:|
|<b>混合層與空氣污染日變化概念圖([Yamada and Mellor 1975][Yamada and Mellor 1975])</b>|

| ![Yamada2.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Yamada2.PNG)|
|:-:|
|<b>大氣垂直混合層及地面逆溫層之日變化([Yamada and Mellor 1975][Yamada and Mellor 1975])</b>|

[Yamada and Mellor 1975]: <https://journals.ametsoc.org/view/journals/atsc/32/12/1520-0469_1975_032_2309_asotwa_2_0_co_2.xml?tab_body=pdf> "Yamada, T and G Mellor, 1975, A Simulation of the Wangara Atmospheric Boundary Layer Data, / Atmos Sci, 32 2309-2329"