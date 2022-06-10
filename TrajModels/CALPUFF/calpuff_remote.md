---
layout: default
title: calpuff遠端計算
nav_order: 5
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
---

# calpuff遠端計算系統之實現
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
- calpuff執行會需要地形、氣象、臭氧濃度與排放等前處理，雖然目前有[calwrf](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALMET/calwrf/)的轉接，可以減省很多整併的工作，但也僅限地形與氣象部分。其他項目還是得一一解決(詳[calpuff.inp](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/))。
- 因為calpuff程式並沒有平行計算的設計，執行會需要較長時間，這是遠端計算系統困難的地方。其他困難還包括：
  - 氣象檔非常龐大，該如何提供？
  - 結果檔案即使以[con2nc](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2nc/)處理成nc檔案，可以用VERDI開啟，依然不是馬上可以檢視結果。後處理還有待提升。


| ![CALPUFF_remote.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_remote.PNG)|
|:-:|
| <b>CPUFF721執行進度網頁畫面</b>|

## 結果畫面與連結

### 檔案連結

```
pid= 77547(check progress)
Model_results:
calmet.dat
calpuff.con.S.grd02.nc
calpuff.inp
cpuff.out
```
### 程式進度畫面

| ![CALPUFF_prog.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_prog.PNG)|
|:-:|
| <b>CPUFF721執行進度網頁畫面</b>|
| ![CALPUFF_nc.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_nc.PNG)|
| <b>CPUFF721最終進度網頁畫面</b>|
