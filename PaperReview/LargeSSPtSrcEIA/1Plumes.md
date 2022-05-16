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

## 煙流受建築物尾流影響

| ![The-notation-and-the-flow-regimes-considered-in-the-modelling-of-downwash.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/The-notation-and-the-flow-regimes-considered-in-the-modelling-of-downwash.png)|
|:--:|
| <b>煙流的煙囪頂下洗、建築物下洗現象([Kukkonen 1997][1])</b>|


- 污染源附近建築物造成煙流擴散行為的改變非常劇烈，煙流中心向下移動造成地面嚴重燻煙，稱之為Plume Downwash煙流下洗。
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

[1]: <https://www.researchgate.net/publication/264396988_A_DISPERSION_MODELLING_SYSTEM_FOR_URBAN_AIR_POLLUTION> "Kukkonen, J. (1997). A DISPERSION MODELLING SYSTEM FOR URBAN AIR POLLUTION. Finnish Meteorological Institute, Helsinki, Finland."


