---
layout: default
title: geoplot行政區範圍等值圖
parent: geoplot Programs
grand_parent: Graphics
has_children: true
date: 2023-05-30
last_modified_date: 2023-05-30 09:34:02
tags: geoplot graphics choropleth
---

# geoplot繪製行政區範圍等值圖
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

- 以行政區為等值圖範圍的數據圖稱之為[choropleth](https://en.wikipedia.org/wiki/Choropleth_map)，為模式重要的後處理形式之一。
- 以[NCL（NCAR Command Language）](https://www.ncl.ucar.edu/)的網站服務方式(CaaS)，提供之解決方案如[NCL/choropleth](../NCL/choropleth.md)所示，仍有不足之處:
  1. 系統複雜，維護困難
  2. NCL語言難以接近
  3. 圖面顏色與畫質不佳
- 此處方案以[geoplot](https://ithelp.ithome.com.tw/articles/10204839)模組呼叫matplotlib、geopandas等一般性之python模組進行繪製

![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-05-30-09-47-27.png)

## 程式下載

{% include download.html content="[grb2D1m3.py](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2D1m3.py)" %}
