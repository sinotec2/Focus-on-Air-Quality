---
layout: default
title:  Surfer IO Programs
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-02-08 15:23:39
---

# Surfer IO Programs
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
- SURFER是工程界常用的繪圖軟體，然而SURFER並不能直接讀取模式網格輸出檔案內容，還是需要進行grid內插動作，來形成另一個網格系統，似是多此一舉。
- 經查python領域也還未有人發展讀/寫SURFER GRD檔案的通用模組。似應用有限。
  - 近年來SURFER也發展以python執行其自動化程序，取代其VB程式。然該模組也未有提供直接轉換成GRD檔之功能。
  - [PVGeo](https://pvgeo.org/examples/grids/read-surfer.html)提供了快速讀取SurferGrid檔案的模組，以應用其顯示功能，然未有寫出模組。
- 此處以簡易的ASCII GRD檔案格式為平台，撰寫python的讀/寫程式，以應用SURFER細膩之繪圖功能。

## [save_surfer](https://github.com/sinotec2/cmaq_relatives/blob/master/post/save_surfer.py) 程式說明
### 引數
- fname：檔名
- (nx,ny)：X/Y方向網格數
- (x0,y0)：X/Y方向原點座標
- (xn,yn)：X/Y方向最大值
- grd：2維矩陣(Y,X)

### 處理
- 使用reshape將2維矩陣線性化，一次寫出即可
- 分為實數(save_surfer)及整數(save_surferi)2個版本，可以避免過多的有效位數，增加ASCII檔案的可讀性

### 檔案下載
- [GIT](https://github.com/sinotec2/cmaq_relatives/blob/master/post/save_surfer.py)

## [load_surfer](https://github.com/sinotec2/cmaq_relatives/blob/master/post/load_surfer.py) 程式說明
### 引數
- fname：檔名

### 輸出
- x, y：座標值
- grd2：維矩陣(Y,X)
- (ny,nx)：Y/X方向網格數

### 處理
- 只適用在ASCII格式之GRD檔案

### 檔案下載
- [GIT](https://github.com/sinotec2/cmaq_relatives/blob/master/post/load_surfer.py)

## Reference
