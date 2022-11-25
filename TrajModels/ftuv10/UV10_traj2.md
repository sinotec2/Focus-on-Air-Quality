---
layout: default
title: 地面二維軌跡分析
nav_order: 5
parent: Trajectory Models
has_children: true
permalink: /TrajModels/ftuv10
last_modified_date: 2022-03-31 15:20:02
---

# 地面uv10二維軌跡分析
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

- 有別於觀測站地面風速之軌跡分析([由CWB數據計算軌跡][traj])，[ftuv10.py][ftuv10]乃讀取wrfout中的地面10m風速(U10)變數，來進行正/反軌跡計算。
- 因其格式的特性，可以讀取過去分析或未來預報之風場，更能靈活應用。
- 讀取的是模式結果，在外海、山區等地，會比內(外)插風場有較為合理的結果。然而在測站代表性較高的地方，模式模擬不見得會比觀測來得準。
- 假設空氣質點沒有高度的位移，可以顯示整體地面風場的平移效果，因此使用在風速較為顯著的天候。對於靜風、垂直擴散強烈之天候，會有過於保守的評估。3維軌跡線的分析可以詳見[WRF三維軌跡分析](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests)系列筆記的說明。

[ftuv10]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/ftuv10/ftuv10/> "地面uv10二維軌跡分析程式"
[traj]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/traj/> "由CWB數據計算軌跡"
