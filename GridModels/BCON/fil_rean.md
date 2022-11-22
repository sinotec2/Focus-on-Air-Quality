---
layout: default
title: EAC4再分析濃度之填入
parent: Boundary Condition
grand_parent: CMAQ Model System
nav_order: 4
date: 2022-11-22 13:36:46
last_modified_date: 2022-11-22 13:36:51
---

# EAC4再分析濃度之填入(fil_rean)
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

- 此項作業主要針對既有的BCON檔案進行特定濃度項目的修改。
  - 數據來源為ECMWF的再分析濃度(詳[歐洲中期天氣預報中心再分析數據之下載](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF_rean))
  - 目的在於降低邊界條件造成的模式錯誤

## 程式設計

### IO

- 引數
  - 年月、物質名稱
  - `ym,sp=(sys.argv[i] for i in [1,2])`
- 輸入檔
  - `fname='/nas1/ecmwf/reanalysis/gribs19/'+sp+ym+'D2.m3.nc'`