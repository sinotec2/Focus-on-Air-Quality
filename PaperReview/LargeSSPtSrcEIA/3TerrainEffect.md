---
layout: default
title: 高斯模式及大氣穩定度
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
- 季節變化

- 日夜變化

| ![Pendergast1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Pendergast1.PNG)|
|:--:|
| <b>日夜加熱差異造成的環流與空污現象([Pendergast 1984][Pendergast 1984] in [Atmospheric science and power production][Randerson 1984])</b>|

[Pendergast 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Malcolm M. Pendergast, 1984, Chap. 2, METEOROLOGICAL FUNDAMENTALS, in Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."

[Randerson 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Randerson, D. (1984). Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."
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

### Plume Rise Model Enhancements (PRIME)

| ![PRIME1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/PRIME1.PNG)|
|:--:|
| <b>受建物尾流影響的煙流與未受影響煙流側面分布之比較([Schulman et al. 2000][Schulman et al. 2000])，空腔區渦流將煙流質心向下移動，其影響隨下游距離減少</b>|



[Schulman et al. 2000]: <https://www.tandfonline.com/doi/full/10.1080/10473289.2000.10464017> "Schulman, L.L., Strimaitis, D.G., and Scire, J.S. (2000). Development and Evaluation of the PRIME Plume Rise and Building Downwash Model. Journal of the Air & Waste Management Association 50 (3):378–390. doi:10.1080/10473289.2000.10464017.
"

| ![uawm_a_1279088_f0002_b.jpeg](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/uawm_a_1279088_f0002_b.jpeg)|
|:--:|
| <b>PRIME及PRIME2對紊流空間性質之概念比較([Petersen and Guerra 2018][Petersen and Guerra 2018])，上：PRIME的概念圖，簡單、尚有未交代區域。下：PRIME2，增加漸變段、按實際情況減少紊流增強區之範圍</b>|

| ![uawm_a_1279088_f0005_b.jpeg](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/uawm_a_1279088_f0005_b.jpeg)|
|:--:|
| <b>PRIME及PRIME2之比較([Petersen and Guerra 2018][Petersen and Guerra 2018])，上：上視圖，BPIP前處理之簡化作法與實際寬幅建物。下：BPIP與PRIME的側面分區概念與實際之差異。</b>|

[Petersen and Guerra 2018]: <https://www.sciencedirect.com/science/article/abs/pii/S0167610517306669> "Petersen, R. L. and Guerra, S. A., (2018). PRIME2: Development and evaluation of improved building downwash algorithms for rectangular and streamlined structures. Atmospheric Environment, 173, 67-78."

### 模式模擬方式
1.  使用[BPIPPRM](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/)進行前處理
  - 將複雜的建築物平面座標系統予以簡化
  - 解析出以煙囪為中心、36個方位建築物的長、寬、高
2. 進行AERMOD/PRIME或ISC/PRIME等煙流模式模擬
3. 模擬方式細節、範例、遠端執行系統詳[建築物煙流下洗現象之模擬設定](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/)


### 建築物下洗模擬的官方立場
- USEPA, Issues Related to Building Downwash in AERMOD,  [www.epa.gov, downwash_overview_white_paper](https://www.epa.gov/sites/default/files/2021-01/documents/downwash_overview_white_paper.pdf), 05-13-2019.
  - BPIPPRM-AERMOD模式系統係2005年架構
  - 依據近年研究結論，目前適用情況：
    - 實心、矩形、單一高度(無樓裙)之建築物
    - 過寬、過長、流線、鏤空建築物有可能造成嚴重高/低估
    - 短時間的模擬(如NO<sub>2</sub>小時值)差異會更大
- 近年發現(AERMOD/PRIME低估情況)
  - [Olesen, et al., 2009][3]指出1.5倍建物高的煙囪在超寬建物尾流效應中AERMOD/PRIME將造成**嚴重低估**。
  - [Perry, et al., 2016][4]在這項EPA委託的風洞模擬計畫中發現AERMOD對於煙流質量的散布傾向高估、對於煙流有效高隨下游距離的降低斜率也傾向低估(將會有較高的煙流中心高度)、因此對地面最大濃度值造成**低估**
- Building Downwash **Alpha Option**s in AERMOD, [www.epa.gov, downwash_alpha_options_white_paper](https://www.epa.gov/sites/default/files/2021-01/documents/downwash_alpha_options_white_paper.pdf), 05-13-2019

[1]: <https://www.researchgate.net/publication/264396988_A_DISPERSION_MODELLING_SYSTEM_FOR_URBAN_AIR_POLLUTION> "Kukkonen, J. (1997). A DISPERSION MODELLING SYSTEM FOR URBAN AIR POLLUTION. Finnish Meteorological Institute, Helsinki, Finland."
[2]: <https://www.epa.gov/sites/default/files/2021-01/documents/downwash_overview_white_paper.pdf> "USEPA, Issues Related to Building Downwash in AERMOD, 2021,01"
[3]: <https://link.springer.com/article/10.1007/s10546-009-9355-9> "Olesen, H.R., Berkowicz, R., Ketzel, M., Lofstrom, P. (2009). Validation of OML, AERMOD/PRIME and MISKAM using the Thompson wind tunnel data set for simple stack-building configurations. Boundary-Layer Meteorol. 131, 73-83."
[4]: <https://www.sciencedirect.com/science/article/abs/pii/S1352231016305829> "Perry, S.G., Heist, D.K., Brouwer, L.H., Monbureau, E.M., and L.A. Brixley (2016). Characterization of pollutant dispersion near elongated buildings based on wind tunnel simulations, Atmospheric Environment, Vol. 42, 286-295."

## 煙流受地形效應之影響
