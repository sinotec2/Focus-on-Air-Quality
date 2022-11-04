---
layout: default
title: 地面二維軌跡分析
nav_order: 5
parent: Trajectory Models
has_children: true
permalink: /TrajModels/ftuv10
last_modified_date: 2022-03-31 15:20:02
---

# 地面二維軌跡分析
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

## 原理
- 讀取地面10m高度之風場(wrfout格式)
- 自測站開始進行2維反軌跡計算
- 超過3公里解析度範圍，則繼續讀取15公里解析度檔案。
- 輸出結果(csv檔案)可以轉成geojson檔案，貼在[GitHub Pages](https://sinotec2.github.io/traj/)畫面

## Usage

```bash
PY=/Users/Data/cwb/e-service/btraj_WRFnests/ftuv10_5d.py
cd /Library/WebServer/Documents
today=$(date +%Y%m%d)
for t in zhongshan zhongming jiayi qianjin;do
  $PY -t $t -d ${today}12 -b True
```
