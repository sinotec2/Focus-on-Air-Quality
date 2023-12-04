---
layout: default
title:  環保專案成果摘要之解讀
parent: 環保專案報告之下載
grand_parent: Crawlers
nav_order: 4
last_modified_date: 2023-12-01 22:01:33
tags: Crawlers pdf
---

# 環保專案成果中英文摘要之解讀
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

- 環保專案的基本資訊下載及解讀可以參照[環保專案基本資訊之解讀](./rd_detail.md)的說明。
- 雖然是同一個網頁，但摘要與基本資訊的資訊量差異還蠻大的，如果儲存在同一個檔案處理起來會不太方便，此處就另外存一個新檔案，中間用`'proj_id'`將其連結即可。
- 注意`'proj_id'`重複問題。此處也未將其整併，以保持df.index的一致性。

## 程式說明

這個腳本([rd_Abs.py](./rd_Abs.py))的目的是從一系列HTML檔案中提取摘要信息，並將其添加到一個 `Pandas DataFrame`中。 以下是腳本的主要步驟：

1. **導入必要的庫**：
    - 匯入了一些用於資料處理和網路請求的函式庫，如`os`、`sys`、`time`、`requests`、`BeautifulSoup`、`pandas` 和 `numpy`。

2. **載入已有的 DataFrame**：
    - 從名為 `'df0WithBasic.csv'` 的 `CSV` 檔案中載入一個 `DataFrame`（`df0`）。

3. **初始化新的 DataFrame**：
    - 建立一個新的 DataFrame（`df`），其中包含了一些列，如 'proj_id', 'chiAbs' 和 'engAbs'。

4. **遍歷 HTML 檔案清單**：
    - 從 `'proj_link.txt'` 檔案讀取 `HTML` 內容，並使用 `BeautifulSoup` 進行解析。

5. **解析 HTML 內容**：
    - 從每個 `HTML` 內容中找到包含 'proj_id' 的連結。
    - 提取 `'proj_id'`，並建立實際的請求 `URL` 。

6. **發起 HTTP 請求取得頁面內容**：
    - 使用 `requests.get()` 方法向目標 `URL` 發起 `HTTP` 請求，取得頁面內容。

7. **檢查請求是否成功**：
    - 檢查回應狀態碼是否為200，如果不是，則輸出錯誤訊息並退出腳本。

8. **解析詳細資訊**：
    - 使用 `BeautifulSoup` 解析頁面內容，擷取中文和英文摘要資訊。

9. **更新 DataFrame**：
    - 根據 `'proj_id'` 定位到 `DataFrame` 中的對應行，將摘要資訊加入 `DataFrame` 中。

10. **將 DataFrame 儲存到 CSV 檔案**：
     - 將更新後的 `DataFrame` 寫入 `'df0WithAbs.csv'` 檔案。

腳本中使用了一些用於控制請求頻率的時間間隔，以避免過於頻繁的請求。 如果在執行腳本時遇到問題，請檢查網路連線和目標網站的反爬蟲策略。