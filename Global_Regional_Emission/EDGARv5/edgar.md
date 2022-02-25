---
layout: default
title: EDGAR
parent: Global/Regional Emission
grand_parent: CMAQ Model System
nav_order: 6
date: 2022-02-25 15:04:48
last_modified_date: 2022-02-25 15:04:52
---

# EDGARv5之下載與處理
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
- 當3公里解析度模擬範圍擴大到境外，就會需要較高解析度的排放數據。[REAS](/Focus-on-Air-Quality/REASnFMI/REAS/reas_download/)與傳統上，全球排放數據大多以0.25度為合理的解析度，然在臺灣附近，約為25~27Km，與3Km差異頗大的。
- [Ding et al(2017)](https://acp.copernicus.org/articles/17/10125/2017/acp-17-10125-2017.html)比較了9種排放清冊，從其中可以發現由bottom-up方式的推估成果並不多，除了[REAS](/Focus-on-Air-Quality/REASnFMI/REAS/reas_download/)之外以[EDGAR(Emissions Database for Global Atmospheric Research)](https://edgar.jrc.ec.europa.eu/)較為活躍，其餘如[MEIC(Multi-resolution Emission Inventory for China)](http://meicmodel.org/)並沒有穩定持續的更新。
- [EDGAR](https://edgar.jrc.ec.europa.eu/)污染項目雖然不多(9樣，詳批次檔)，也沒有點源詳細數據，然而其0.1度解析度確實較[REAS](/Focus-on-Air-Quality/REASnFMI/REAS/reas_download/)更加符合需要。


## 下載方式及格式
- 直接到[EDGAR](https://edgar.jrc.ec.europa.eu/)官網點選下載nc連結，製做批次檔如下。

```bash

for i in BC CO NH3 NMVOC NOx OC PM10 PM2.5 SO2;do
  https=https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v50_AP/${i}/TOTALS
  filez=v50_${i}_2015.0.1x0.1.zip
  zz=${https}/${filez}
  wget -q --no-check-certificate zz
  unzip ${filez}
done  
```
- 其經緯度的起始點及點數為：
  - 經度：0.05 (3600點)
  - 緯度：-89.5 (1800點)



## Results

| ![NOx_EastAsia.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NOx_EastAsia.PNG) |
|:--:|
| <b>圖 CWBWRF_3k範圍NOx排放之分布(log gmole/s)</b>|  


## Reference
- Ding, J., Miyazaki, K., van der A, R.J., Mijling, B., Kurokawa, J., Cho, S., Janssens-Maenhout, G., Zhang, Q., Liu, F., and Levelt, P.F. (2017). **Intercomparison of NOx emission inventories over East Asia.** Atmos. Chem. Phys. 17 (16):10125–10141. [doi:10.5194/acp-17-10125-2017](https://acp.copernicus.org/articles/17/10125/2017/acp-17-10125-2017.pdf).

