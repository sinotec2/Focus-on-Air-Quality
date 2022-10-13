---
layout: default
title: "CAMS Global Forecast"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
has_children: true
nav_order: 5
date: 2022-08-02 14:19:20
last_modified_date:   2022-08-02 14:19:24
permalink: /AQana/GAQuality/ECMWF_CAMS
---

# 歐洲中期天氣預報中心CAMS全球空品預報場之下載
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


### 數據庫基本資訊

item|content
-|-
Data type|Gridded
Horizontal coverage|Global
Horizontal resolution|0.4°x0.4°
Vertical coverage|Surface, total column, model levels and pressure levels.
Vertical resolution|60 model levels before July 7 2019 00UTC, then 137 model levels. Pressure levels: 1000, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1 hPa
Temporal coverage|2015 to present
Temporal resolution|1-hourly (single-level), 3-hourly (multi-level)
File format|GRIB (optional conversion to netCDF)
Versions|Only one version, but with occasional model upgrades
Update frequency|New 00UTC and 12UTC forecasts added each day(每半天進行一次預報計算). Model upgrades made approximately once a year

### names of all AQ variables
- 氣狀物/粒狀物混合比單位：kg kg**-1

```
1 Carbon monoxide
2 Dust Aerosol (0.03 - 0.55 um) Mixing Ratio
3 Dust Aerosol (0.55 - 0.9 um) Mixing Ratio
4 Dust Aerosol (0.9 - 20 um) Mixing Ratio
5 Ethane
6 Formaldehyde
7 Hydrogen peroxide
8 Hydrophilic Black Carbon Aerosol Mixing Ratio
9 Hydrophilic Organic Matter Aerosol Mixing Ratio
10 Hydrophobic Black Carbon Aerosol Mixing Ratio
11 Hydrophobic Organic Matter Aerosol Mixing Ratio
12 Hydroxyl radical
13 Isoprene
14 Methane (chemistry)
15 Nitrate coarse mode aerosol mass mixing ratio
16 Nitrate fine mode aerosol mass mixing ratio
17 Nitric acid
18 Nitrogen dioxide
19 Nitrogen monoxide
20 GEMS Ozone
21 Peroxyacetyl nitrate
22 Propane
23 Sea Salt Aerosol (0.03 - 0.5 um) Mixing Ratio
24 Sea Salt Aerosol (0.5 - 5 um) Mixing Ratio
25 Sea Salt Aerosol (5 - 20 um) Mixing Ratio
26 Sulphate Aerosol Mixing Ratio
27 Ammonium aerosol mass mixing ratio
28 Sulphur dioxide
```