---
layout: default
title: ncl_convert2nc的應用
parent: grib Relatives
grand_parent: Utilities
nav_order: 2
date: 2023-07-01 11:01:42
last_modified_date: 2023-07-01 11:01:46
tags: grib ecmwf eccodes
---

# ncl_convert2nc的應用
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

## 應用場景

- 202306之前ECMWF CAMS全球每日2次預報grib檔案之轉換（詳見[CAMS_ic](../../AQana/GAQuality/ECMWF_CAMS/4.CAMS_ic.md)）
- ECMWF[再分析空品數據之轉換](../../AQana/GAQuality/ECMWF_rean/EC_ReAna.md)
- GFS再分析數據檔之[轉換](../../wind_models/EARR/7-3.gfs2csv.md)
- [中央氣象局WRF_3Km數值預報產品之下載](../../wind_models/cwbWRF_3Km/1.get_M-A0064.md)

## 應用的限制

- 對於高斯網格檔案無法轉換（如ECMWF NRT檔案）
- 對於202306之後CAMS預報檔案無法轉換