---
layout: default
title:  環保專案基本資訊之解讀
parent: 環保專案報告之下載
grand_parent: Crawlers
nav_order: 3
last_modified_date: 2023-12-04 16:26:05
tags: Crawlers pdf
---

# 環保專案基本資訊之解讀
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

- 在每個專案成果的介紹畫面中，有5個分頁，分別是基本資訊(本文處理)、中、英文摘要(詳見[rd_Abs](./rd_Abs.md))、成果下載(見[captcha](captcha.md)說明)及友善列印。
- GPT建議直接使用`requests`即可，事實上也比較快速、直接。
- 雖然處理還算快速，但為避免佔用頻寬，每隔100次連線還是設定休息10秒鐘。
- `'proj_link.txt'` 檔案的產生：直接對各個類別所有的html檔案一次進行`grep`擷取即可。
- 系統歸檔錯誤(同一計畫`'proj_id'`重複歸類在不同的類別)，總計約有600~700件之多，可能會重複下載。此階段因下載量不大也就任其重複下載，也重複給值。往後下載檔案時需要設計跳開機制。

![](../../../attachments/2023-12-04-16-54-50.png)

## 程式說明

這個腳本([rd_detail.py](./rd_detail.py))的目的是從一系列 `HTML` 檔案中提取基本訊息，並將其添加到一個包含其他資訊的 `Pandas DataFrame` 中。 以下是腳本的主要步驟：

1. **導入必要的庫**：
    - 匯入了一些用於資料處理和網路請求的函式庫，如`os`、`sys`、`time`、`requests`、`BeautifulSoup`、`pandas` 和 `numpy`。

2. **載入已有的 DataFrame**：
    - 從名為 'df0.csv' 的 CSV 檔案中載入一個 DataFrame（`df`）。

3. **初始化新的 DataFrame**：
    - 建立一個新的 DataFrame，其中包含了一些列，如 '項目計劃編號'、'經費年度'、'計劃經費' 等。

4. **遍歷 HTML 檔案清單**：
    - 從 `'proj_link.txt'` 檔案讀取 HTML 內容，並使用 BeautifulSoup 進行解析。

5. **解析 HTML 內容**：
    - 從每個 HTML 內容中找到包含 `'proj_id'` 的連結。
    - 提取 `'proj_id'`，並建立實際的請求 `URL。`

6. **發起 HTTP 請求取得頁面內容**：
    - 使用 `requests.get()` 方法向目標 `URL` 發起 `HTTP` 請求，取得頁面內容。

7. **檢查請求是否成功**：
    - 檢查回應狀態碼是否為200，如果不是，則輸出錯誤訊息並退出腳本。

8. **解析基本資訊**：
    - 透過解析 `HTML` 頁面，提取基本資訊的表格資料。

9. **更新 DataFrame**：
    - 根據 `'proj_id'` 定位到 `DataFrame` 中的對應行，將基本資訊加入 `DataFrame` 中。

10. **將 DataFrame 儲存到 CSV 檔案**：
     - 將更新的 `DataFrame` 寫入 `'df0WithBasic.csv'` 檔案。

腳本中使用了一些用於控制請求頻率的時間間隔，以避免過於頻繁的請求。 如果在執行腳本時遇到問題，請檢查網路連線和目標網站的反爬蟲策略。