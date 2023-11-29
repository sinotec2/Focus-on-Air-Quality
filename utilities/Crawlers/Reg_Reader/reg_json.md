---
layout: default
title:  環境法規之下載
parent: Regulation Reader
grand_parent: Crawlers
nav_order: 2
last_modified_date: 2023-11-29 04:45:34
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

- 這個 Python 腳本（[reg_json.py](reg_json.py)）用於從法務部[全國法規資料庫](https://law.moj.gov.tw/Index.aspx)(下稱**系統**)個別法規網頁中提取法律文本、並保存為 JSON 檔案備用。
- 同樣是url字串存在著問號及等號的情況，**系統**不接受`requests`、不接受browser的`driver.get`，甚至也不接受`os.system`執行`wget`。
- 只接受將url寫在執行腳本中、透過bash來執行。
- 詳細原因不明，GPT暗示可能是網站的防爬策略，但是**系統**卻對簡易批次的`wget`開放，這點似乎不符邏輯。
- 此腳本適用於自動化提取和儲存**系統**特定格式的網頁上的法律文件信息，但它依賴於該**系統** HTML 結構的網頁，針對不同的網站會需要進行調整。

## 程式說明

以下是腳本的主要步驟：

1. **讀取 HTML 內容**：
    - 從 'href_n.txt' 檔案讀取 HTML 內容。

2. **解析 HTML**：
    - 使用 BeautifulSoup 程式庫解析 HTML 內容。

3. **取得法律文件的連結和標題**：
    - 找到 `<a>` 標籤以取得法律文件的 URL 和標題。

4. **檢查文件是否已存在**：
    - 檢查是否已經下載了對應的 HTML 檔案。 如果沒有，則執行下載。

5. **下載法律文檔頁面**：
    - 將url中的問號(?)及等號(=)加上反斜線，形成新的字串`url2`以正確傳遞程式引數。
    - 將 `url2`及`wget` 指令寫在`a.cs`內，下載法律文件的頁面。
    - 使用 `os.system` 執行命令列操作。

```python
    url = a_tag['href'].split('&')[0].split('=')[1]
    url="https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode="+url
    title = a_tag['title']
...
        url2=url.replace('?','\\?').replace('=','\\=')
        with open('a.cs','w') as f:
            f.write('url='+url2+'\n/usr/bin/wget -q $url -O '+title+'.html\n')
        os.system('chmod u+x ./a.cs;./a.cs' )
```

6. **解析法律文件頁**：
    - 再次使用 BeautifulSoup 解析下載的 HTML 檔案。
    - 提取法律名稱、日期和具體條款。

7. **提取並保存法律條文**：
    - 遍歷所有法律條文的 `<a>` 標籤。
    - 提取法律條文的編號和內容。
    - 將提取的資訊保存在字典 `result` 中。

8. **將結果儲存為 JSON 檔案**：
    - 將 `result` 字典轉換為 JSON 格式並儲存到檔案中。

