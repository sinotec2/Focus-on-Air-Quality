---
layout: default
title: Abundant NoG Runs
parent: CMAQ Model System
nav_order: 9
has_children: true
permalink: /GridModels/Abundant_NoG_Runs
last_modified_date:   2022-03-18 16:24:20
tags: CMAQ CWBWRF
---

# 東亞地區高網格數之CMAQ模擬分析
{: .no_toc }

**CMAQ**模式合理的網格數理論上應越多越好，然仍受到電腦資源的限制。

以NOAA執行[美國本土臭氧指引預報](https://airquality.weather.gov/sectors/conusLoop.php#tabs)的規格而言，其網格解析度為**12Km**，美國本土東西向約4500Km、南北向約2700Km，因此網格數：
- 東西向=4500/12=375\~400
- 南北向=2700/12=225\~250

而以[中央氣象局數值天氣預報](https://conf.cwb.gov.tw/media/cwb_past_conferences/106/2017_ppt/A2/A2-26-中央氣象局區域模式2017年更新_陳依涵.pdf)的規格
- 15Km解析度：東西向662、南北向386
-  3Km解析度：東西向1161、南北向676

此處即參照此一水準，嘗試增加東亞地區之模擬之網格數進行CMAQ模擬(Abundant Number_of_Grid Runs)。

{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---


