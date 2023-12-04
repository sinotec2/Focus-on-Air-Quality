---
layout: default
title:  環保專案成果書目之解讀
parent: 環保專案報告之下載
grand_parent: Crawlers
nav_order: 2
last_modified_date: 2023-12-01 22:01:33
tags: Crawlers pdf
---

# 環保專案成果書目之解讀
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

這個 Python 腳本（[rd_title.py](rd_title.py)）是用來從 HTML 檔案中提取特定的專案訊息，並將其儲存為一個 CSV 檔案。 這裡是腳本的主要步驟：

1. **定義來源目錄和搜尋 HTML 檔案**：
    - 設定 `source_directory` 為目前目錄 (`"./"`)。
    - 使用 `glob.glob` 函數來尋找目前目錄下的所有 HTML 檔案。

2. **初始化 Pandas DataFrame**：
    - 建立一個空的 DataFrame `df0`。
    - 建立一個空的字典 `gp_cat` 用於儲存項目類別。

3. **遍歷 HTML 檔案**：
    - 遍歷每個 HTML 檔案。
    - 使用 BeautifulSoup 解析 HTML 內容。

4. **提取資料**：
    - 在每個 HTML 檔案中尋找所有帶有類別 `download_icon` 的 `<a>` 標籤。
    - 對於每個鏈接，提取 `href` 屬性，進而提取 `proj_id` 和 `group_id`。
    - 從連結的 `title` 屬性中提取項目標題。
    - 將擷取的資料儲存在一個字典中，並加入到 `data_list` 清單中。

5. **轉換資料到 DataFrame 並合併**：
    - 將 `data_list` 轉換為一個新的 DataFrame `df`。
    - 將 `df` 合併到初始的 `df0` DataFrame 中。

6. **新增類別資訊並儲存 CSV 檔案**：
    - 對於 `df0` 中的每個 `group_id`，從 `gp_cat` 字典中尋找對應的類別 `cat` 並加入 DataFrame 中。
    - 設定 `proj_id` 為 DataFrame 的索引。
    - 將 DataFrame 儲存為 CSV 檔案 `env_prj.csv`。

這個腳本主要用於從多個 HTML 文件中提取相關的連結信息，並將這些資訊匯總和格式化為一個結構化的 CSV 文件，以便於進一步的數據分析和處理。