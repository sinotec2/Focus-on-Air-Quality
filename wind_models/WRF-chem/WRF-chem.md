---
layout: default
title: "WRF-chem"
parent: "WRF"
has_children: true
nav_order: 4
date: 2021-12-27 16:40:05
last_modified_date:   2021-12-27 16:39:57
permalink: /wind_models/WRF-chem/
---

# WRF-chem

WRF-chem模式的編譯、設定與應用案例

因粒狀物或大氣成分改變，造成大氣輻射的差異，因而影響溫度、壓力及流場，如此偶合情況嚴重的現象需要以**WRF-chem**模式進行模擬。
- 一般來說，其濃度等級要非常高、影響範圍要足夠大、時間也要足夠長
- 因統御方程式或參數化模組的差異，雙向巢狀網格的運作可能無法順利進行。
- 濃度模擬結果將作為子網格系統的初始及邊界濃度條件

{: .fs-6 .fw-300 }
