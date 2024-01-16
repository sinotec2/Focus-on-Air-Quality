---
layout: default
title:  按照計畫類別下載環評書件書目表
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 2
last_modified_date: 2023-06-12 08:56:43
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

### IO's

這段程式碼主要是使用`Selenium`來自動控制瀏覽器,從環評書件網站爬取資料。

主要參數說明:

1. `driver`: 控制Chrome瀏覽器的對象
2. `bb`: 從proj_class.json檔案讀取的分類資料
3. `cat`: 分類代號,用來在網站篩選資料
4. `fname`: 儲存網頁原始碼的檔案名稱
5. `last、npage`: 計算總頁數
6. `fnames`: 所有頁面的檔案名稱列表 

主要邏輯:

1. 開啟瀏覽器,進入環評委員會網站
2. 循環讀取proj_class.json的分類
3. 根據分類在網站篩選資料 
4. 分頁抓取資料,並存成原始碼檔案
5. 使用`BeautifulSoup`解析,提取表格轉成DataFrame
6. 計算總頁數,根據頁數抓取每頁原始碼

輸出結果:
以分類名稱命名的多個網頁原始碼檔案

### 詳細解釋

這段程式碼是用Python編寫的`Selenium`和`BeautifulSoup`結合的自動化網頁抓取腳本。 其主要功能是從特定的網站（`https://eiadoc.epa.gov.tw/eiaweb/`）上自動取得分頁表格數據，並將每一頁的資料儲存為HTML檔案。 下面是程式碼的詳細解釋：

1. **初始化Selenium Webdriver**:
    - 使用Chrome瀏覽器。

2. **造訪特定網頁**:
    - 開啟網頁 `https://eiadoc.epa.gov.tw/eiaweb/`。

3. **讀取JSON檔**:
    - 從`proj_class.json`檔案讀取類別資料。

4. **循環處理每個類別**:
    - 對於`bb`列表中的每個類別（此處只處理列表的第一個元素）:
      - 使用`Select`類別選擇ID為`cphContent_dlFtrDECAL`的下拉框，並依照類別選擇對應的選項。
      - 點選ID為`cphContent_lnkFtrAbstract`的查詢按鈕。

5. **處理分頁**:
    - 點擊「前進」按鈕(`>`)以訪問最後一頁並取得其HTML原始碼。
    - 使用BeautifulSoup解析HTML並提取表格數據，然後建立一個Pandas DataFrame。
    - 基於DataFrame中最後一行的編號計算總頁數。

6. **儲存所有頁面資料**:
    - 返回第一頁並儲存HTML。
    - 對於每個頁碼，使用`click_wait`函數點擊連結並儲存頁面的HTML原始碼。

7. **錯誤處理**:
    - 如果在抓取過程中遇到錯誤，則設定預設的頁數和頁碼。

8. **休眠**:
    - 在載入頁面和點擊操作之間使用`time.sleep(10)`確保頁面有足夠時間載入。

這個腳本充分利用了`Selenium`的網頁自動化能力和`BeautifulSoup`的HTML解析功能，有效地從動態網頁中提取分頁資料。 由於涉及網路操作和頁面加載，腳本包含了一些休眠時間來確保資料可以正確加載和處理。 這種類型的腳本特別適用於需要從多頁動態內容中提取資料的情況。

### 迴圈詳解

與[rd_allPages.py](./download_EIA_report.md#迴圈詳解)最後一個 for 迴圈一樣，目的是遍歷網頁並保存每個頁面的內容。 