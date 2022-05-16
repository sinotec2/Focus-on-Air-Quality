---
layout: default
title: 煙流在大氣中的行為
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 1
last_modified_date: 2022-05-16 09:42:56
---

# 煙流在大氣中的行為
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

## 煙流下洗現象、模擬與限制
污染源附近建築物造成煙流擴散行為的改變非常劇烈，煙流中心向下移動造成地面嚴重燻煙，稱之為[Plume Downwash](https://solareis.anl.gov/glossacro/dsp_wordpopup.cfm?word_id=5080)煙流下洗。
- 煙流擴散行為受到附近大氣紊流及渦流影響甚劇，而渦流的產生，除了垂直溫度梯度的熱力紊流之外，就屬氣流受到阻體所產生的機械紊流(渦流)最為嚴重
- 污染源附近最重要的阻體即是煙囪本身，以及鄰近的煙囪、廠房設備、建築物等等。
- 2維圖示如下：

| ![The-notation-and-the-flow-regimes-considered-in-the-modelling-of-downwash.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/The-notation-and-the-flow-regimes-considered-in-the-modelling-of-downwash.png)|
|:--:|
| <b>煙流的煙囪頂下洗、建築物下洗現象([Kukkonen 1997][1])</b>|

### 建築物尾流
- 其現象、原因及模擬、可以參考下列視頻及文章
  - [FDS Simulation](https://www.youtube.com/watch?v=UkV2JHg9CX8)
    - [FDS](https://pages.nist.gov/fds-smv/)是個微尺度、大渦流紊流模式，除了模擬室內火災、空品之外，戶外情況下之煙流細部行為特色亦能有所掌握。
    - 視頻中以FDS模擬穩定大氣情況、建築物頂部排放的三維煙流行為。
  - [Plume characteristics for three different stack scenarios](https://www.youtube.com/watch?v=qQJRSrfv8eQ)
    - 在模式無法預期的特殊條件，風洞模擬試驗是一個直觀的解決方案。這個英文旁白的視頻介紹了大致上風洞模擬煙流在格柵狀與實心建築物尾流的行為、以及模式高估的可能性。
  - [www.cppwind.com：Building Downwash – Problems, Solutions and Next Generation](ftp://newftp.epa.gov/Air/aqmg/SCRAM/conferences/2015_11th_Conference_On_Air_Quality_Modeling/Presentations/3-6_Building_Downwash-CPP-11thMC.pdf)
    - 這篇[CPP wind](https://cppwind.com/)公司2015年的研討會論文，檢討了多孔(鏤空)建築物、流線形、極寬或極長建築物的尾流效應。
  - [BREEZE AERMOD 7: Gridded Plume Downwash](https://www.youtube.com/watch?v=bgoU9GTNYHs)
    - 這是一家商用軟體([BREEZE AERMOD](https://www.trinityconsultants.com/software/dispersion/aermod))的介紹短片，雖然是模式輸出的結果，卻也可以略略描繪煙流受到建築物尾流影響的推估概念。  

### 模式模擬方式
1.  使用[BPIPPRM](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/)進行前處理
  - 將複雜的建築物平面座標系統予以簡化
  - 解析出以煙囪為中心、36個方位建築物的長、寬、高
2.  進行AERMOD/PRIME或ISC/PRIME等煙流模式模擬
3. 模擬方式細節、範例、遠端執行系統詳[建築物煙流下洗現象之模擬設定](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/)

### 建築物下洗模擬的[官方立場][2]
- USEPA, Issues Related to Building Downwash in AERMOD,  [www.epa.gov, downwash_overview_white_paper](https://www.epa.gov/sites/default/files/2021-01/documents/downwash_overview_white_paper.pdf), 2021,01.
  - BPIPPRM-AERMOD模式系統係2005年架構
  - 依據近年研究結論，目前適用情況：
    - 實心、矩形、單一高度(無樓裙)之建築物
    - 過寬、過長、流線、鏤空建築物有可能造成嚴重高/低估
    - 短時間的模擬(如NO<sub>2</sub>小時值)差異會更大
- 近年發現(AERMOD/PRIME低估情況)
  - [Olesen, et al., 2009][3]指出1.5倍建物高的煙囪在超寬建物尾流效應中AERMOD/PRIME將造成**嚴重低估**。
  - [Perry, et al., 2016][4]在這項EPA委託的風洞模擬計畫中發現AERMOD對於煙流質量的散布傾向高估、對於煙流有效高隨下游距離的降低斜率也傾向低估(將會有較高的煙流中心高度)、因此對地面最大濃度值造成**低估**

[1]: <https://www.researchgate.net/publication/264396988_A_DISPERSION_MODELLING_SYSTEM_FOR_URBAN_AIR_POLLUTION> "Kukkonen, J. (1997). A DISPERSION MODELLING SYSTEM FOR URBAN AIR POLLUTION. Finnish Meteorological Institute, Helsinki, Finland."
[2]: <https://www.epa.gov/sites/default/files/2021-01/documents/downwash_overview_white_paper.pdf> "USEPA, Issues Related to Building Downwash in AERMOD, 2021,01"
[3]: <https://link.springer.com/article/10.1007/s10546-009-9355-9> "Olesen, H.R., Berkowicz, R., Ketzel, M., Lofstrom, P. (2009). Validation of OML, AERMOD/PRIME and MISKAM using the Thompson wind tunnel data set for simple stack-building configurations. Boundary-Layer Meteorol. 131, 73-83."
[4]: <https://www.sciencedirect.com/science/article/abs/pii/S1352231016305829> "Perry, S.G., Heist, D.K., Brouwer, L.H., Monbureau, E.M., and L.A. Brixley (2016). Characterization of pollutant dispersion near elongated buildings based on wind tunnel simulations, Atmospheric Environment, Vol. 42, 286-295."

## 煙流受地形效應之影響
