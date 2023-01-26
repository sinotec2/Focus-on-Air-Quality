---
layout: default
title: 行政區範圍等值圖
parent: NCL Programs
grand_parent: Graphics
has_children: true
date: 2023-01-26
last_modified_date: 2023-01-26 19:14:20
tags: NCL graphics choropleth
---

# 行政區範圍等值圖
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

### 前言

- 以行政區為等值圖範圍的數據圖稱之為[choropleth](https://en.wikipedia.org/wiki/Choropleth_map)，為模式重要的後處理形式之一。
- 繪製等值圖的方式不是很多，其中還涉及繪圖品質、互動方式、輸入檔案格式、以及支援資源是否充分等因素，此處以[NCL（NCAR Command Language）](https://www.ncl.ucar.edu/)的網站服務方式(CaaS)，提供解決方案。
(一) 應用需求與目標
等值圖的應用包括：

    行政區域平均值與標準之比較：來源可能是行政區內的測站值、內插值、模式模擬結果等，
    等值線圖之行政區範圍平均：模式網格解析度太高、或解析度不足時，轉以行政區為空間代表特性。模式輸出檔案一般以netCDF格式最為常見。（客戶較少）
    表列行政區特性值之空間展示：來源可能是含有行政區代碼、與特性數值之csv檔案（潛在客戶較多）
    鄉鎮區代碼：
        舊碼為4碼（縣市代碼2碼01～51、2碼該縣市下之鄉鎮區碼01～）
        新碼為8碼（縣市代碼5碼09007~68000、該縣市下之鄉鎮區碼3碼001～）

作業要求包括：

    報告品質
    重複性高，作業流程需程式化
    避免繁雜設定

(二) 解決方案比較
目前製作等值圖的軟體並不多，檢討如下：

    VERDI：品質不高，可接受CAMx/IOAPI 之nc檔案，不能接受csv檔案。可流程化、但不能相容於CaaS。
    SURFER：高品質。舊版mapviewer 可以製作等值圖，目前surfer必須執行basic程式，每個多邊形元素著色。能相容於CaaS。
    NCL：高品質。因為沒有介面軟體，為獨立的執行程式，因此作業流程、設定均為最複雜。然而也是最能相容於CaaS之系統。
        NCL容許較大的截尾錯誤，8碼的行政區代碼(偶)會讀錯，解決方案：
            大數必須先行減少有效位數、且以字元形式，才能正確進行比較。
            內設是32bit，因此8碼會有問題(4*8=32)，網友建議宣告成64bit整數
        因行政區代碼只用於比較，並沒有其他計算，且事先切分也較符合作業邏輯。

(三) 解決方案規劃

    由網頁獲知客戶要處理的檔案路徑名稱
    執行cgi_python進行新舊代碼之辨識、對照、執行NCL程式、將結果自動下載到客戶端的Downloads目錄
    ncl腳本：參考DKRZ的作法，在shape檔範圍內填入彩虹色階。