---
layout: default
title: Redistribution of Ship Emissions
parent: EDGAR Emission Processing
grand_parent: Global/Regional Emission
nav_order: 2
date: 2022-03-17 18:42:30
last_modified_date: 2022-03-17 18:42:34
---

# EDGARv5船隻排放空間分布之重分配
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
- 雖然EDGAR解析度0.1度與HUADON_3k的解析度已經相差無幾，然而模擬結果仍然顯示出濃度分布的奇異點，當風向與船隻路線有顯著交角是，突高的面源產生類似點源的效應，圖面上呈現出平行的煙流，而不是均勻的片狀線源貢獻之濃度分布。
- 造成此一結果的主要原因是EDGAR在同一路線上的排放量本身就具有很大的差異性，當程式進行內插時就很難避免加深此一差異而造成路線上的不連續結果。
- 解決方式
  - 以照片處理技巧拉大路線及非路線排放量的差距([Noise Removal of a Raster Data](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/noise_removal/))。
  - [Extracting Road Vector Data from Raster Maps](https://www.researchgate.net/publication/227067853_Extracting_Road_Vector_Data_from_Raster_Maps)
  - 重新以高解析度數據進行排放量的空間分配。


## 
### 程式下載
- [EDGAR2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR2cmaqD2.py)

## Results

| ![NOx_EastAsia.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NOx_EastAsia.PNG) |![NO2_D6.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NO2_D6.PNG) |
|:--:|:--:|
| <b>圖 Ding(2017) 衛星反衍東亞地區NOx排放之分布</b>|<b>圖 HUADON_3k範圍EDGARv5 NO2排放之分布(log gmole/s)</b>|  

## Reference
- Ding, J., Miyazaki, K., van der A, R.J., Mijling, B., Kurokawa, J., Cho, S., Janssens-Maenhout, G., Zhang, Q., Liu, F., and Levelt, P.F. (2017). **Intercomparison of NOx emission inventories over East Asia.** Atmos. Chem. Phys. 17 (16):10125–10141. [doi:10.5194/acp-17-10125-2017](https://acp.copernicus.org/articles/17/10125/2017/acp-17-10125-2017.pdf).

