---
layout: default
title:  環保專案成果檔案之下載
parent: 環保專案報告之下載
grand_parent: Crawlers
nav_order: 5
last_modified_date: 2023-12-05 05:33:40
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

- 連結網頁、截圖、解讀、填入空格、下載檔案、重新命名。
  
![](IAgree.png)

- 「成果下載」分頁：https://epq.moenv.gov.tw/ProjectData/ResultDetail?proj_id=1111161182&proj_recno=6&keyword=水質保護&group_id=5407&log=C#
- 由「成果下載」分頁中目標檔案之連結網址：https://epq.moenv.gov.tw/ProjectDoc/FileDownload?proj_id=1111161182&group_id=5407
- 點進後下載圖像

![](../../../attachments/2023-12-01-16-56-54.png)

Current source:	https://epq.moenv.gov.tw/ProjectDoc/GetCaptchaImage/

```html
<form method="post" action="/ProjectDoc/FileDownload">
    
    <input type="hidden" id="proj_id" name="proj_id" value="1111161182">
    <input type="hidden" id="group_id" name="group_id" value="5407">
    <input type="hidden" data-val="true" data-val-required="The fid field is required." id="fid" name="fid" value="0">
    <input type="hidden" data-val="true" data-val-required="The doc_kind field is required." id="doc_kind" name="doc_kind" value="0">
    <div class="input-group">
        <label for="CaptchaCode">驗證碼(點擊驗證碼可重新產生驗證碼)</label>
    </div>
    <div class="input-group">
        <a href="javascript:void(0);" title="重新顯示新的驗證碼" onclick="resetCaptchaImage()"><img title="重新顯示新的驗證碼" id="img-captcha" src="./g3_files/saved_resource" alt="重新顯示新的驗證碼" style="width: 100%; height: 100%;"></a>
        <button style="border:0;background:none;text-align:center" title="驗證碼語音播放" onclick="VoicePlay()" type="button">
            <i class="lnr lnr-volume-high" style="font-size: 1.3rem; line-height: 2rem; vertical-align: middle;"></i><span>播放</span>
        </button>
        <input type="text" class="form-control" placeholder="請輸入驗證碼" maxlength="4" data-val="true" data-val-length="驗證碼(點擊驗證碼可重新產生驗證碼)超過字數4" data-val-length-max="4" id="CaptchaCode" name="CaptchaCode" value="">
        <span class="text-danger field-validation-valid" data-valmsg-for="CaptchaCode" data-valmsg-replace="true"></span>
    </div>
    <div class="form-group">
        <input type="submit" value="我同意" class="btn btn-primary" title="我同意，下載檔案" style="background-color: #2351e8;"/>
    </div>
    <input name="__RequestVerificationToken" type="hidden" value="CfDJ8FcpIWJ4KcdOpTwzRpJW0LMApSTsXE44DRdry4qwrFf0HMhzgwnArmNKNxEyiI8zyogUSfpLJssfBUKyKLGRb8t1elGrulKqhQik9eW_OqhJUmOeYjl8XRTWfrPUZqEoGeuPovyH0BfNURvaRj7jpZE" />
</form>
```

### get the keys and values

您可以使用 BeautifulSoup 库来解析 HTML 并提取 `<form>` 元素内部的 `<input>` 标签的 `name` 属性和 `value` 属性。以下是一个示例代码：

```python
from bs4 import BeautifulSoup

html_content = """
<form method="post" action="/ProjectDoc/FileDownload">
    ...
</form>
"""

soup = BeautifulSoup(html_content, 'html.parser')

# 找到所有的 <input> 元素
input_elements = soup.find_all('input')

# 创建一个空的字典用于存储键值对
payload = {}

# 遍历每个 <input> 元素，提取 name 和 value，并存储到字典中
for input_element in input_elements:
    input_name = input_element.get('name')
    input_value = input_element.get('value')
    if input_name is not None and input_value is not None:
        payload[input_name] = input_value

# 打印提取的键值对
print(payload)
```

此代码将在字典 `payload` 中存储每个 `<input>` 元素的 `name` 和 `value`。请注意，对于没有 `name` 或 `value` 属性的 `<input>` 元素，将不会包含在结果字典中。

### fill the input and get file

您可以使用 Python 的 requests 模块来模拟提交表单的请求。以下是一个简单的示例代码：

```python
import requests

url = "https://epq.moenv.gov.tw/ProjectDoc/FileDownload"  # 替换成实际的目标网址

# 替换成实际的参数值
payload = {
    "proj_id": "1111161182",
    "group_id": "5407",
    "fid": "0",
    "doc_kind": "0",
    "CaptchaCode": "nPPq",
    "__RequestVerificationToken": "CfDJ8FcpIWJ4KcdOpTwzRpJW0LMApSTsXE44DRdry4qwrFf0HMhzgwnArmNKNxEyiI8zyogUSfpLJssfBUKyKLGRb8t1elGrulKqhQik9eW_OqhJUmOeYjl8XRTWfrPUZqEoGeuPovyH0BfNURvaRj7jpZE"
}

response = requests.post(url, data=payload)

# 检查请求是否成功
if response.status_code == 200:
    print("表单提交成功")
else:
    print("表单提交失败，HTTP 状态码：", response.status_code)
    print("服务器响应内容：", response.text)
```

请确保替换 `url` 变量中的网址和 `payload` 变量中的参数值为实际的值。此外，如果目标网站使用了验证码保护，您可能需要查看网站的相关规则，并使用适当的方法来处理验证码。

## main.py37


## OCR methods

```python
#!/home/anaconda3/envs/py37/bin/python
import cv2
import pytesseract
from PIL import Image

# 读取图像
image = cv2.imread('./input.png', 0)

# 二值化
_, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

# 使用 Tesseract 进行 OCR
text = pytesseract.image_to_string(Image.fromarray(binary_image))

print(text)
```

## 程式說明

這個 Python 腳本是用來從 HTML 檔案中提取特定的專案訊息，並將其儲存為一個 CSV 檔案。 這裡是腳本的主要步驟：

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

這個腳本主要用於從多個 HTML 文件中提取相關的連結信息，並將這些資訊匯總和格式化為一個結構化的 CSV 文件，以便於進一步的數據分析和處理。 這個腳本的目的是從特定網站下載 PDF 文件，並根據驗證碼進行驗證。 以下是腳本的主要步驟：

1. **導入必要的庫**：
    - 使用 Selenium 進行網頁自動化。
    - 使用 pytesseract 和 OpenCV 進行驗證碼識別。
    - 使用 Pandas 處理資料。
    - 使用 glob 和 os 處理檔案。

2. **定義驗證碼取得函數**：
    - `get_captcha(i)` 函數用來取得驗證碼。
    - 使用 Pillow 庫裁剪和儲存螢幕截圖。
    - 使用 pytesseract 進行 OCR 識別驗證碼。

3. **載入已有的 DataFrame**：
    - 從名為 'df0.csv' 的 CSV 檔案中載入一個 DataFrame（`df0`）。

4. **建立 Chrome 驅動器**：
    - 使用 Firefox 磁碟機啟動 Selenium。

5. **循環遍歷資料集**：
    - 對 `df0` 中的每一行執行下列步驟。

6. **開啟網頁並下載 PDF 檔案**：
    - 使用 Selenium 開啟目標網頁。
    - 截取螢幕截圖，並呼叫驗證碼取得函數以取得驗證碼。
    - 將驗證碼輸入網頁。
    - 點擊 "我同意" 按鈕。
    - 檢查是否出現 "OK" 按鈕，如果是，則點擊 "OK" 按鈕，重新進行循環。
    - 否則，等待一段時間，然後將下載的 PDF 檔案移至指定目錄。

7. **關閉瀏覽器**：
    - 在循環結束後，關閉瀏覽器。

請注意，此腳本假設驗證碼輸入框的id 為"CaptchaCode"，同意按鈕的XPath 為"//input[@value='我同意']"，OK 按鈕的XPath 為"//button[text() ='OK']"。 確保這些元素在網頁中存在且正確。 如果有任何網頁結構的變化，可能需要相應地調整腳本中的元素選擇器。