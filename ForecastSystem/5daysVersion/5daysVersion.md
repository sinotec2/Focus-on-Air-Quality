---
layout: default
title: 5 days version
parent: Forecast Systems
nav_order: 1
date: 2022-08-20
last_modified_date: 2022-09-16 15:02:14
has_children: true
permalink: /ForecastSystem/5daysVersion
mermaid: true
tags: CWBWRF forecast CMAQ GFS wrf CAMS wrf-python REAS crontab m3nc2gif
---

# 5 天預報版本
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

- 這個初期的版本整合了CAMS 5天預報、CWBWRF 3天預報，來進行wrf及CMAQ模擬。因為預報時間較短，計算需求較小，作為預報系統初期建立的版本，有其必要性與適當性。
- 這個階段要(已)解決的問題
  - 東亞ICBC之建立(詳見另目錄)
  - GFS數據下載與應用
  - CWBWRF數據之應用
  - mcip轉接
  - 逐日CMAQ之模擬與nest down
  - 後處理的問題(詳見另目錄)
- 因為時間太短，初始濃度的影響太大，東亞地區3天的現象不夠完整，因此這個版本就沒有繼續營運。轉到[10天預報](../10daysVersion/10daysVersion.md)的版本。


{: .no_toc .text-delta }

{:toc}

---
