---
layout: default
title:  環保專案成果書目之下載
parent: 環保專案報告之下載
grand_parent: Crawlers
nav_order: 1
last_modified_date: 2023-12-01 22:01:33
tags: Crawlers pdf
---

# 環保專案成果書目之下載
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

- 環保專案成果報告查詢系統有基本的分類，分別是01水質保護～19國際環保議題。
- 點進去之後，會出現20～50條的書目，依序每頁另存即可。
- 總共有幾頁的頁數，會出現在第一頁，用bs4讀出來就行。

## 程式說明

Python 這個[腳本](get_links.py)使用 Selenium 和 BeautifulSoup 庫從一個特定的網站（「https://epq.moenv.gov.tw/Query/ResultList」）提取數據，並保存到本地 HTML 文件中。以下是腳本的詳細步驟：

1. **導入所需的庫**：
   - 匯入了 Selenium 和 BeautifulSoup 庫，以及必要的功能，如 `WebDriverWait` 和 `expected_conditions`。

2. **定義點選等待函數** (`click_wait`)：
   - 此函數用於點擊頁面元素，並等待頁面更新後再繼續執行。

3. **瀏覽分類**：
   - 使用`for`循環遍歷不同的類別`cat`（編號從02到19）。

4. **設定無頭模式的Firefox瀏覽器驅動程式**：
   - 建立一個無頭 Firefox 瀏覽器實例（不顯示介面的瀏覽器）。

5. **造訪網站並等待元素載入**：
   - 造訪特定類別的頁面。
   - 使用 `WebDriverWait` 等待頁面中的特定元素載入完成。

6. **選擇每頁顯示的出境數**：
   - 找到並顯示選擇下拉式選單來改變每頁的條目數。

7. **儲存目前頁面的內容**：
   - 把目前頁面的 HTML 原始碼儲存到一個本機檔案。

8. **使用BeautifulSoup解析HTML，取得總頁數**：
   - 解析已儲存的頁面內容，找到表示頁碼的元素，從而決定總頁碼。

9. **瀏覽所有頁面**：
   - 對於每一頁，使用前面定義的 `click_wait` 函數點擊頁面上的頁面代碼鏈接，切換到對應的頁面。
   - 將每個頁面的 HTML 原始碼儲存到本機檔案。

10. **關閉瀏覽器**：
   - 完成資料摘要後，關閉瀏覽器。

此主要腳本用於自動化從網站上提取分頁數據，將每一頁的內容保存為本地 HTML 文件，然後進行後續的數據處理和分析。