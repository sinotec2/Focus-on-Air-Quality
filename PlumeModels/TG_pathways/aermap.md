---
layout: default
title: Exec. and Effects of AERMAP
parent: RE & TG Pathways
grand_parent: Plume Models
nav_order: 2
date: 2023-01-28
last_modified_date: 2023-01-28 16:53:44
tags: plume_model AERMAP
---

# AERMAP之執行與效果
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


## 結果比較

### 林口電廠範例貼圖結果

| ![kml_demo.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/kml_demo.png) |
|:--:|
| <b>圖 林口電廠周邊地形KML檔案輸出結果範例</b>|  

### 檢查項目

- [範圍]()：是否以污染源排放為中心、是否符合設定範圍(海面範圍可視情況減少)
- [高值]()部分：是否符合地圖（鄉鎮區界線、稜線道路、山峰位置等）
  - 煙流大致會在2倍煙囪高度之等高線，產生高值。
  - 有群峰之地形範圍，煙流會在第一個碰觸點產生高值。
- [解析度]()：太低→地形特徵會消失。煙流本身會模糊化，解析度太高會增加執行時間，沒有必要。
- 等高線：一般公路設計會平行於等高線，可藉地圖中公路的走向，檢視地形數據結果的正確性
- 低值位置：一般地圖上是河流、住家村落、陂塘、農地等。
- 海岸線：等高線是否與地圖之海岸線平行

### 林口電廠周邊地形檔輸入aermod模擬結果範例

- mmif氣象1/21\~31
- 有建築物

| ![noterr.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/noterr.png) |![withterr.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/withterr.png)|
|:--:|:--:|
| <b>無地形，煙流偏西南方，為東北季風影響</b>|有地形，煙流方向偏南，擴散範圍受到限制，集中在河谷低地。受限於80\~100M等高線範圍。最大值較高51\~754&mu;/M<sup>3</sup>|
