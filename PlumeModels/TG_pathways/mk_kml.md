---
layout: default
title: 全島1X1網格模擬結果之連結
parent: RE & TG Pathways
grand_parent: Plume Models
nav_order: 99
date: 2024-04-13
last_modified_date: 2024-04-13 20:39:05
tags: plume_model sed gdal AERMAP
---

# 全島1X1網格模擬結果之連結
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

這段程式碼是一個 Python 腳本，名為 `mk_kml.py`，用於生成 KML 文件以可視化地面資料。以下是程式碼的說明：

### 腳本說明

1. **引入模組及設置**

   - 引入了必要的模組，包括 `Proj`、`pandas`、`twd97` 和 `os`。
   - 定義了 Lambert Conformal Conic 投影的參數，以及台灣地區的中心經緯度。

2. **讀取資料**

   - 從 CSV 檔案中讀取了地面資料和點的資料。
   - 定義了一些資料的 URL 和檔案擴展名。

3. **處理地面資料**

   - 對每個地面資料進行迴圈處理，檢查其是否存在於點的資料中。
   - 將每個地面資料的經緯度、名稱和描述添加到相應的列表中。
   - 將列表轉換為 DataFrame，並將其輸出為 CSV 檔案。
   - 使用外部命令 `csv2kml.py` 將 CSV 檔案轉換為 KML 檔案。

4. **處理地面資料的四個點**

   - 對每個地面資料進行迴圈處理，對於每個地面資料的四個點進行處理。
   - 將每個點的經緯度、名稱和描述添加到相應的列表中。
   - 將列表轉換為 DataFrame，並將其輸出為 CSV 檔案。
   - 使用外部命令 `csv2kml.py` 將 CSV 檔案轉換為 KML 檔案。

### 使用方式

執行此腳本，將生成地面資料的 KML 文件和四個點的 KML 文件。要執行此腳本，只需在終端中進入腳本所在的目錄，然後運行以下命令：

```bash
python mk_kml.py
```

這將生成 `terrTWN_1X1.csv` 和 `terrTWN_1X1P.csv` 兩個 CSV 檔案，然後使用 `csv2kml.py` 將它們轉換為對應的 KML 檔案。