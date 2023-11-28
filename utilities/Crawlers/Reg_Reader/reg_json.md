---
layout: default
title:  環境法規之下載
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 3
last_modified_date: 2023-06-12 08:56:43
tags: Crawlers pdf
---

# 環境法規之下載
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

這個 Python 腳本用於從網頁中提取法律文本並保存為 JSON 檔案。 以下是腳本的主要步驟：

1. **讀取 HTML 內容**：
    - 從 'href_n.txt' 檔案讀取 HTML 內容。

2. **解析 HTML**：
    - 使用 BeautifulSoup 程式庫解析 HTML 內容。

3. **取得法律文件的連結和標題**：
    - 找到 `<a>` 標籤以取得法律文件的 URL 和標題。

4. **檢查文件是否已存在**：
    - 檢查是否已經下載了對應的 HTML 檔案。 如果沒有，則執行下載。

5. **下載法律文檔頁面**：
    - 使用 `wget` 指令下載法律文件的頁面。
    - 使用 `os.system` 執行命令列操作。

6. **解析法律文件頁**：
    - 再次使用 BeautifulSoup 解析下載的 HTML 檔案。
    - 提取法律名稱、日期和具體條款。

7. **提取並保存法律條文**：
    - 遍歷所有法律條文的 `<a>` 標籤。
    - 提取法律條文的編號和內容。
    - 將提取的資訊保存在字典 `result` 中。

8. **將結果儲存為 JSON 檔案**：
    - 將 `result` 字典轉換為 JSON 格式並儲存到檔案中。

此腳本適用於自動化提取和儲存特定格式的網頁上的法律文件信息，但它依賴於特定 HTML 結構的網頁，可能需要針對不同的網站進行調整。
