---
layout: default
title: 高斯模式及穩定度
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 1
last_modified_date: 2022-05-16 09:42:56
tags: review plume_model
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

### 垂直穩定度在空間中的不均勻特性

- Shoreline Internal Boundary Layer
  - Convective-internal-boundary-layer-formed-by-advection-of-cool-marine-air-over-a-warm.png

| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Convective-internal-boundary-layer-formed-by-advection-of-cool-marine-air-over-a-warm.png)|
|:-:|
|<b>海岸地區對流內部邊界層[Hsu , 1988][Hsu , 1988]</b>|

[Hsu , 1988]: <https://www.biblio.com/9780123579553> "Hsu, S. A., Coastal Meteorology, 260 pp., Academic, San Diego,Calif., 1988."

### 混合層日變化與污染擴散現象

- 混合層與地面污染
  - [Yamada and Mellor 1975][Yamada and Mellor 1975], A Simulation of the Wangara Atmospheric Boundary Layer Data, Atmos Sci, 32 2309-2329

| ![Yamada1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Yamada1.PNG)|
|:-:|
|<b>混合層與地面空氣污染日變化概念圖([Yamada and Mellor 1975][Yamada and Mellor 1975])</b>|

| ![Yamada2.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Yamada2.PNG)|
|:-:|
|<b>大氣垂直混合層及地面逆溫層之日變化([Yamada and Mellor 1975][Yamada and Mellor 1975])</b>|

[Yamada and Mellor 1975]: <https://journals.ametsoc.org/view/journals/atsc/32/12/1520-0469_1975_032_2309_asotwa_2_0_co_2.xml?tab_body=pdf> "Yamada, T and G Mellor, 1975, A Simulation of the Wangara Atmospheric Boundary Layer Data, / Atmos Sci, 32 2309-2329"

- [臺灣中部地區東西向垂直截面之PM<sub>2.5</sub>動態分布](https://sinotec2.github.io/PM2.5CrossSect)
  - 2019/1/30/0~6 污染物累積地面有限範圍，待日間向上擴散
- [高空污染源對地面濃度之影響](https://sinotec2.github.io/cpuff_forecast/)
  - 夜間 ~ 清晨煙流對地面沒有影響，
  - 6 ~ 8時突然出現煙流形狀之地面濃度分布

## 煙流模式的架構流程

### [USEPA SCRAM](https://www.epa.gov/scram)模式種類架構

- Dispersion Modeling
  - Preferred/Recommended Models 
    - AERMOD Modeling System ([**AER**MIC][AERMIC] **MOD**el)
    - [CTDMPLUS][CTDMPLUS]：複雜地形模式。作法詳[後述](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/3TerrainEffect/#ctdmplus)。
    - [OCD][OCD]：近海污染源在陸地的濃度分析。需海上及陸上氣象數據
  - [Alternative Models](https://www.epa.gov/scram/air-quality-dispersion-modeling-alternative-models)
    -  ADAM, ADMS, AFTOX, ASPEN, BLP, CAL3QHC/CAL3QHCR, CALINE3, [CALPUFF](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF), DEGADIS, HGSYSTEM, HOTMAC/RAPTAD, HYROAD, ISC3, ISC-PRIME, OBODM, OZIPR, Panache, PLUVUEII, SCIPUFF, SDM, and SLAB.
  - [Screening Tools](https://www.epa.gov/scram/air-quality-dispersion-modeling-screening-models)
    - AERSCREEN, CAL3QHC, COMPLEX1, CTSCREEN, RTDM3.2, SCREEN3, TSCREEN, VALLEY, and VISCREEN.
  - [Related Programs](https://www.epa.gov/scram/air-quality-dispersion-modeling-related-model-support-programs)
    -  AERCOARE, [AERMAP](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/REnTG_pathways/), AERPLOT, AERSURFACE, [BPIP, BPIPPRM](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/), BPIPPRM-Draft, CALMET2NCF, CALMPRO, CHAVG, CONCOR, EMS-HAP, [MMIF](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/ME_pathways/mmif/), and MMIFstat.
- Photochemical Modeling
  - Community Multiscale Air Quality ([CMAQ](https://github.com/USEPA/CMAQ), 2021) 
  - Comprehensive Air quality Model with extensions ([CAMx](https://www.camx.com/), 2022)
  - Regional Modeling System for Aerosols and Deposition ([REMSAD](http://remsad.icfconsulting.com/), 2005)
  - Urban Airshed Model Variable Grid ([UAM-V ®](http://uamv.icfconsulting.com/), 1991)
- Receptor Modeling
  - Chemical Mass Balance (CMB)
  - Positive Matrix Factorization (PMF)

[AERMIC]: <https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#aermod> "American Meteorological Society/Environmental Protection Agency Regulatory Model Improvement Committee"
[CTDMPLUS]: <https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#ctdmplus> "Complex Terrain Dispersion Model Plus Algorithms for Unstable Situations"
[OCD]: <https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#ocd> "Offshore and Coastal Dispersion Model Version 5"

### AERMOD執行流程

|![Modeling-system-of-Aermod-View-software-Source-Lakes-Environmental-2017.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Modeling-system-of-Aermod-View-software-Source-Lakes-Environmental-2017.png)|
|:-:|
|<b>AERMOD模式系統與設定流程([Cerqueira et. al 2019][Cerqueira et. al 2019])</b>|

[Cerqueira et. al 2019]: <https://www.researchgate.net/publication/328505586_Atmospheric_pollutants_modeling_with_Aermod_software> "Cerqueira, J., Albuquerque, H., and Sousa, F. (2019). Atmospheric pollutants: modeling with Aermod software. Air Quality, Atmosphere & Health 12. doi:10.1007/s11869-018-0626-9."

### AERMOD在臺灣之應用

- 有關AERMOD在臺灣應用的實務討論，可以參考[環工技師會訊11007pp39-55(pdf)](http://www.tpeea.org.tw/upload/news/files/7eea35bc4c7a4189b42566fffe2f2fee.pdf)
- [Markdown format](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/AERMODinTWN/)