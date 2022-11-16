---
layout: default
title: km.py程式說明
nav_order: 4
parent: WRF三維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-16 10:33:28
---

# acc_prob.py程式說明

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



- 這支程式讀取choose10.py結果，以K-means方式取其代表性叢集。

#### 程式IO

- arguments:
  - *10.csv檔案路徑名稱之文字檔
  - nclt: number of clusters
- 輸入檔
  - *10.csv：choose10.py的結果
  - tmplateD1_3km.nc：由JI轉換成網格化座標位置
- 輸出檔
  - lab.csv：逐時的叢集編號
  - 'res'+str(l)+'.csv' ：各叢集的代表性軌跡
- 內掛後處理（[csv2kml.py][csv2kml]）：
  - 由csv產生kml檔案
  - 可以google map、leaflet套件等等進行繪圖
