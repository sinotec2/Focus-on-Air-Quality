---
layout: default
title: Boundary Condition
parent: CMAQ Model System
nav_order: 2
has_children: true
permalink: /GridModels/BCON/
---

# 邊界條件之準備
{: .no_toc }

**CMAQ**模式的邊界條件有3種給定方式：
1. 由全球模式模擬結果檔案解讀(`REGRID`)，如MOZART或由ecwmf之[再分析濃度檔直接產生](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2bc/)
1. 由巢狀網格**CMAQ**執行成果解讀(`REGRID`)
1. 以一組觀測值或符合化學平衡的模擬結果設定(`PROFILE`)。敏感測試時使用。
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---



