---
layout: default
title:  計劃類別碼與名稱之對照
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 1
last_modified_date: 2023-06-12 08:56:43
tags: Crawlers pdf
---

# 計劃類別碼與名稱之對照
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

- 「計畫類別」是環評書件書目的重要項目，此處建立其代碼與名稱的對照表。

## 程式說明

[proj_class.py](./proj_class.py)程式碼主要是處理 `proj_class.html` 這個網頁原始碼檔,提取特定內容生成 `proj_class.json` 這個 JSON 檔。

主要邏輯說明如下:

1. 從 `proj_class.html` 讀取所有行到 lines 列表
2. 過濾出所有有 `"value="` 和 `'B'` 的行到 a 列表  
   (可能是某些分類選項)
3. 從 `a` 再過濾出有 '<' 和 '>' 標籤的行到 b 列表,b 應該就是分類名
4. 從 `a` 列表提取 value 的值到 cat_Bnum,應該是分類代碼
5. 從 `b` 列表解析出中文字提取到 cat_CNnam,就是分類名稱
6. 生成分類資料字典 `dd`,`key` 是分類代碼,值是名稱
7. dd 寫入 `proj_class.json`
8. 讀回 `proj_class.json` 驗證是否一致

輸入:
`proj_class.html` - 原始網頁資料 

輸出: 
`proj_class.json` - 經提取處理的分類資料

重要變數:
`dd` - 分類資料字典

