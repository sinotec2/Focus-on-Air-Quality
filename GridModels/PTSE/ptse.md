---
layout: default
title: Elev. Point Sources
parent: CMAQ Model System
nav_order: 6
has_children: true
permalink: /GridModels/PTSE/
date:               
last_modified_date:   2021-12-02 11:08:53
---

# 高空點源排放檔案
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
- CMAQ高空排放檔案與CAMx最大不同在於不隨時間改變的排放條件(HDTVXY)是另成一檔儲存。可能是為減少檔案的大小，然CMAQ此舉增加很多錯誤的機會。
  - 常數部分：以[pt_const.py](https://github.com/sinotec2/cmaq_relatives/blob/master/ptse/pt_const.py)轉接CAMx格式之REAS與TEDS點源數據
  - 時間變化部分：以[pt_timvar.py]()，逐月轉換後再以[brk_day2.cs](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/brk_day/)裁剪成逐日檔案

## Reference


{: .no_toc }

{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
