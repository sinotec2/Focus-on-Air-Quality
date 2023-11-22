---
layout: default
title:  按照計畫類別下載環評書件書目表
parent: Crawlers
grand_parent: Utilities
has_children: true
last_modified_date: 2023-06-12 08:56:43
permalink: /utilities/Crawlers/PDF\'s
tags: Crawlers pdf
---

# 按照計畫類別下載環評書件書目表
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

- 「計畫類別」是環評書件書目的重要項目，然而必須要點進個別書件才能顯示，這將會大大降低資訊蒐集的速度。
- 此處用`selenium`點擊「計畫類別」的下拉選單、每種計畫類別的書目分開儲存。雖只有其中的2000多本，不能完整下載全部書目，也算是補充不少、且提升不少速度。
- [get_html.py](./get_html.py)的程式邏輯將在底下詳細說明。全部書目(不分類)的下載則見於[rd_allPages.py](./rd_allPages.py)與[說明](./download_EIA_report.md)

## 程式說明

這段程式碼使用Selenium和BeautifulSoup庫從一個網頁上爬取並保存表格資料。 以下是程式碼的詳細解釋：

1. **初始化Selenium Webdriver**:
    - 使用Firefox瀏覽器開啟特定網址（`https://eiadoc.epa.gov.tw/eiaweb/`）。

2. **選擇特定選項**:
    - 透過`Select`類別選擇具有特定ID的下拉框，並選擇一個特定的值（"B02"）。

3. **點選查詢按鈕**:
    - 找到並點選ID為`cphContent_lnkFtrAbstract`的按鈕。

4. **儲存最後一頁結果**:
    - 呼叫`click_wait(">")`函數來點選「前進」按鈕，載入最後一頁，並儲存頁面原始碼。

5. **解析HTML並擷取表格資料**:
    - 使用BeautifulSoup解析保存的HTML頁面。
    - 找到特定ID的表格，並提取表頭和行資料。
    - 使用擷取的資料建立一個Pandas DataFrame。

6. **計算頁碼**:
    - 根據表中的資料計算出總頁數。

7. **返回第一頁並儲存結果**:
    - 使用`click_wait("<")`函數傳回第一頁，並儲存第一頁的HTML原始碼。

8. **遍歷並儲存所有頁面**:
    - 循環遍歷每一頁，點擊對應的頁碼連結（或「...」連結來跳到更多頁碼），並儲存每一頁的HTML原始碼。

9. **儲存資料到HTML檔案**:
    - 對於每一頁的HTML內容，建立一個文件，並將原始碼寫入文件中。

這個腳本主要用於自動化地從網頁上爬取分頁的表格數據，並保存每一頁的數據以便進一步處理。 這對於處理那些需要與網頁互動才能獲取資料的情況非常有用。 需要注意的是，這個腳本在運行時可能需要一些時間，因為它包含了時間延遲（`time.sleep(10)`），以確保頁面載入完成。 此外，對於網頁結構或元素ID的任何更改，腳本可能需要更新才能繼續正常運作。