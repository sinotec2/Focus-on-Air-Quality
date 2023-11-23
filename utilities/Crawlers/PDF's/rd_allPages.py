'''
這段 Python 程式碼使用了 Selenium WebDriver 來自動化地瀏覽和抓取一個網頁的內容。 它的主要功能是遍歷指定網站的多個頁面，並將每個頁面的 HTML 內容儲存到本機檔案中。 以下是這段程式碼的詳細解釋：

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
'''

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_wait(pth,itm):
    # 点击元素
    element = driver.find_element(pth,itm)
    element.click()
# 等待直到页面更新
    wait = WebDriverWait(driver, 10)  # 设置至少等待时间
    wait.until(EC.staleness_of(element))  # 等待直到元素变为陈旧，即页面更新
    return 0

driver = webdriver.Firefox()
driver.get("https://eiadoc.epa.gov.tw/eiaweb/")

# 选择计划类别为"工厂的设立"
select = Select(driver.find_element(By.ID,"cphContent_dlFtrDECAL"))
select.select_by_value("")
npage=750
fnames=['all_page'+str(i)+'.html' for i in range(0,npage)]
if not os.path.exists(fnames[1]):
    with open(fnames[1], "w") as f:
        f.write(driver.page_source)   
    time.sleep(10)
for i in range(2,npage):
    ii=str(i);pth=By.LINK_TEXT
    if i<=4: #skip the meeting pages selection
        pth=By.XPATH;ii='(//a[text()="'+ii+'"])[2]'
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

'''
迴圈詳解
這段程式碼位於一個 for 迴圈中，目的是遍歷網頁並保存每個頁面的內容。 以下是這段程式碼的詳細解釋：

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
'''