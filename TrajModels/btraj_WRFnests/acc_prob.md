---
layout: default
title: acc_prob.py程式說明
nav_order: 5
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

- 從軌跡點L.csv檔案，統計網格通過機率，以便進行繪圖
- 輸入檔案：
  - fnames.txt(檔案路徑名稱之listing)
- 輸出檔案：
  - probJ.nc
  - 單位：crossing time/total time

## NCL繪圖

| ![cluster_results.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/7f55203a-04c9-4cc9-8f37-3544f9373392.png)|
|:-:|
| <b>反軌跡線叢集分析結果</b>|

## 程式下載

- {% include download.html content="三維軌跡線之網格通過機率分析程式：[acc_prob.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/acc_prob.py)" %}


