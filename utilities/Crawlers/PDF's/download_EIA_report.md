---
layout: default
title:  環評書件書目表之全部下載與整理
parent: PDF檔案大綱之讀取與整理
grand_parent: Crawlers
last_modified_date: 2023-06-12 08:56:43
tags: Crawlers pdf
---

# 環評書件之下載與整理
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

- 環境部環評書件共儲存了7500多版中央與地方審查的環評相關文件，為環評過程的重要參考依據。
- Sizing
  - 下載一本報告約需10分鐘、全部下載約需52天。
  - 一本報告約230MB，全部估計1.7T
- 由於報告索引的建立並不是很完整，最直覺的「計畫類別」不單有前後對照不一的問題，也有很多案件並未給定類別，導致搜尋時的嚴重落差。需自行重建索引。
  - 按照各個「計畫類別」分別下載的[程式](./get_html.py)[說明](./get_html.md)
- 位詳細介紹在此分兩個段落說明。此處先介紹索引表格的建立，再進一步介紹下載的爬蟲程式。
- 因網頁設有防爬蟲的隨機驗證碼，只能藉由`selenium`的點擊動作來觸發網站程式。還好一頁有10條報告內容，經重複750次可以完整下載索引表。

## 程式說明

### IO's

- 這支程式使用到`chromedriver`來訪問網站
- 網頁內容(`Id`、選項、`LINK_TEXT`等等)是否一致，每次使用時還是需要再次確認
- 將畫面全部傳回本機，命名為`all_pageNNN.html`，NNN由1~750。

### 主程式邏輯

[rd_allPages.py](./rd_allPages.py)程式碼使用了 `Selenium WebDriver` 來自動化地瀏覽和抓取一個網頁的內容。 它的主要功能是遍歷指定網站的多個頁面，並將每個頁面的 HTML 內容儲存到本機檔案中。 以下是這段程式碼的詳細解釋：

1. **導入必要的庫**：
    - 從 `selenium` 庫匯入 `webdriver`，用於控制瀏覽器。
    - 導入 `Select`，用於處理下拉選擇選單。
    - 導入 `time` 和 `os`，用於處理時間和作業系統相關的功能。
    - 匯入 `WebDriverWait` 和 `expected_conditions`（別名 `EC`），用於等待頁面元素達到某種狀態。

2. **定義點選等待函數 (`click_wait`)**：
    - 這個函數接受一個元素路徑和項，執行點擊操作，然後等待直到頁面重新整理。
    - 使用 `WebDriverWait` 來確保點擊操作後頁面已經更新。

3. **初始化 WebDriver 和開啟網頁**：
    - 使用 `webdriver.Firefox()` 建立一個 Firefox 瀏覽器實例。
    - 開啟指定的 URL（台灣環境部的環境影響評估文件頁面）。

4. **選擇項目類別**：
    - 透過 `Select` 物件選擇頁面上的一個下拉式選單，這裡的目標是選定「計畫類別」為「null」。

5. **準備檔案名稱清單和頁面遍歷**：
    - 建立一個檔案名稱列表，用於儲存不同頁面的內容。
    - 檢查文件是否已存在，如果不存在則抓取頁面內容。
    - 使用循環遍歷網站的多個頁面，頁數上限設定為 `npage`（750）。
    - 對於每一頁，使用 `click_wait` 函數點擊頁面上的連結或按鈕，然後抓取並儲存目前頁面的 HTML 內容。
    - 詳下述說明

6. **儲存頁面內容**：
    - 將每個頁面的 HTML 內容寫入對應的文件中。
    - 在抓取每個頁面後暫停 10 秒，以減少對伺服器的壓力。

### 迴圈詳解

最後一個 for 迴圈中，目的是遍歷網頁並保存每個頁面的內容。 以下是這段程式碼的詳細解釋：

```python
for i in range(2,npage):
    ii=str(i);pth=By.LINK_TEXT
    if (i-1)%5==0:
        if i<=6:
            ii="...";pth=By.LINK_TEXT
        else:
            pth=By.XPATH;ii='(//a[text()="..."])[2]'
    else:
        if os.path.exists(fnames[i]):continue
    result=click_wait(pth,ii)
    if os.path.exists(fnames[i]):continue
    with open(fnames[i], "w") as f:
        f.write(driver.page_source)   
    time.sleep(10)
```

1. **循環遍歷**:
    - `for i in range(2, npage):` 循環從 2 開始，直到 `npage`（定義為 750），用於遍歷網站的多個頁面。

2. **確定如何選擇頁面**:
    - `ii` 和 `pth` 變數用於決定如何選擇頁面連結。
    - `ii=str(i); pth=By.LINK_TEXT`：預設情況下，使用頁面上的連結文字來定位元素。
    - 如果 `(i-1) % 5 == 0`，表示每隔五頁，頁面的選擇邏輯會改變。
      - 如果 `i <= 6`，則 `ii` 設定為 `"..."`（通常用於網頁中的「下一批」連結），`pth` 保持為 `By.LINK_TEXT`。
      - 如果 `i > 6`，則 `pth` 改為 `By.XPATH`，以適應同時有「上一批」「下一批」連結，都是用省略符號("...")，並且選取第2個省略符號，使用特定的 XPath 來點擊正確的物件。

3. **檢查文件是否已存在**:
    - `if os.path.exists(fnames[i]): continue`：這行程式碼檢查對應的檔案是否已經存在。 如果存在，那麼跳過目前迭代，不再重新下載該頁面。

4. **點擊並等待頁面更新**:
    - `result = click_wait(pth, ii)`：呼叫 `click_wait` 函數，根據上述邏輯決定的元素（透過連結文字或 XPath），點選頁面上的連結或按鈕。

5. **再次檢查文件是否已存在**:
    - 點擊操作後，再次檢查檔案是否存在。 這是為了確保不重複寫入同一頁內容。

6. **儲存頁面內容**:
    - 如果文件尚未存在，使用 `with open(fnames[i], "w") as f` 開啟文件，並寫入 `driver.page_source`的內容，即目前瀏覽器頁面的原始碼。
    - `time.sleep(10)`：處理完一個頁面後暫停 10 秒。 這是一種防止過快請求網站而可能被伺服器封鎖的措施。

### 後處理解讀程式

- 下載完成後，將所有`all_page*.html`檔名存成`fnames.txt`(用`ls all_page*.html >fnames.txt` 指令)
- 以下這支程式([all_page*.html](./all_page*.html))將`html`轉成`csv`資料表

本程式使用了Pandas和Beautiful Soup函式庫來解析一系列HTML文件，並從中擷取表格數據，最後將這些資料合併為一個Pandas DataFrame。 以下是對程式碼的詳細解釋：

1. **導入所需庫**:
    - 導入Pandas（用於資料處理）、Beautiful Soup（用於解析HTML）和os（用於作業系統功能，如檔案路徑）。

2. **初始化DataFrame**:
    - `df0 = pd.DataFrame({})`：建立一個空的DataFrame，用於之後儲存所有合併的資料。

3. **定義列名**:
    - `col = ['cat', 'id', 'gov', 'name', 'book', 'prog', 'desc']`：定義了一個列名列表，但在後續代碼中並未直接 使用。

4. **讀取檔名列表**:
    - 從"fnames.txt"檔案讀取HTML檔案的名稱，存入清單`fnames`。

5. **遍歷並解析每個HTML檔**:
    - 透過循環`for fname in fnames:`遍歷檔案清單。
    - 使用`with open(fname, 'r') as html`開啟每個HTML檔案。
    - `soup = BeautifulSoup(html, 'html.parser')`：使用Beautiful Soup函式庫解析HTML內容。

6. **擷取並解析表格**:
    - `table = soup.find('table', {'id': 'cphContent_gvAbstract'})`：在HTML中找到具有特定ID的表格。
    - `header = [th.text.strip() for th in table.find_all('th', {'class': 'gridHeader'})]`：擷取表頭資訊。
    - 在每一行中提取單元格資料並加入`data`清單。

7. **建立DataFrame並合併資料**:
    - `df1 = pd.DataFrame(data, columns=header)`：使用擷取的資料和表頭建立一個新的DataFrame。
    - `combined_df = pd.concat([df0, df1], ignore_index=True)`：將新建立的DataFrame與先前的DataFrame合併。
    - `df0 = combined_df`：更新df0為合併後的DataFrame。

程式碼的最終結果是一個包含所有HTML檔案表格資料的Pandas DataFrame，其中每個檔案的資料都會附加到這個DataFrame中。 需要注意的是，這段程式碼假設每個HTML檔案中的表格結構和列名是一致的。 如果結構不一致，可能需要額外的邏輯來處理不同的情況。

## 給定計畫類別索引

### 