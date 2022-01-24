---
layout: default
title: 近實時空品數據之下載
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 99
date: 
last_modified_date: 2022-01-11 19:52:29
---

# 近實時空品數據之下載（建構中）
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
- 歐洲中期天氣預報中心(ECMWF)之EAC4 ([ECMWF Atmospheric Composition Reanalysis 4](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview))數據下載整併後，此處將其轉成`m3.nc`檔案，以供[VERDI]()等顯示軟體、以及後續光化模式所需。




## 結果檢視
- 2018/4/5～6 大陸沙塵暴之EAC4濃度**水平**分布[mov](https://youtu.be/S3z9j7V-O0w)
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/20180405eac4H.PNG)
- 2018/4/5～6 大陸沙塵暴之EAC4濃度**垂直**分布（臺灣為中心）[mov](https://youtu.be/tiXA1L3IaEI )
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/20180405eac4V.PNG)

## 程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2D1m3.py)

## Reference
- ECMWF, **EAC4 (ECMWF Atmospheric Composition Reanalysis 4)**, [copernicus](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview),record updated 2021-12-07 16:10:05 UTC
- 純淨天空, **python numpy flip用法及代碼示例**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.flip.html)
-Python学习园, **Scipy Tutorial-多维插值griddata**, [cpython](http://liao.cpython.org/scipytutorial11.html)