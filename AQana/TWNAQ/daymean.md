---
layout: default
title: 日均值計算
parent: Taiwan AQ Analysis
grand_parent: AQ Data Analysis
last_modified_date: 2022-02-08 13:46:05
tags: python
---

# 環保署測站數據日均值之計算
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

- 環保署測站檔案是個以日為單位的文字檔案，過去如果要計算日均值，需以迴圈計算。如果還遇到要計算風速風向的向量平均，分屬檔案不同段落，須逐一檢視。
- 本程式的特色是只有在計算向量平均值時，才對日的時間軸進行迴圈計算。

### 大要

