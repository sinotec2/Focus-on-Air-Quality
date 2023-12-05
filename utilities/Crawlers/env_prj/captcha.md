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

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_captcha:
    from PIL import Image

    # 打开截图文件
    screenshot_path = "screenshot.png"
    screenshot = Image.open(screenshot_path)

    # 设置裁剪区域的位置和大小
    x = 100  # 距左边界的像素
    y = 750  # 距顶部的像素
    w = 80  # 宽度
    h = 50  # 高度

    # 裁剪图像
    cropped_image = screenshot.crop((x, y, x + w, y + h))

    # 保存裁剪后的图像
    cropped_image.save("cropped_image.png")
    return CaptchaCode

# 设置 Chrome 驱动器的路径
chrome_driver_path = '/path/to/chromedriver'

# 创建 Chrome 驱动器
driver = webdriver.Firefox()

# 打开网页
url = "https://epq.moenv.gov.tw/ProjectDoc/FileDownload?proj_id=1111564042&group_id=22357"
driver.get(url)
driver.save_screenshot("screenshot.png")

try:
    # 输入验证码（如果需要）
    captcha_input = driver.find_element(By.ID, "CaptchaCode")
    captcha_input.send_keys("ccQ1")

    # 点击 "我同意"
    agree_button = driver.find_element(By.XPATH, "//input[@value='我同意']")
    agree_button.click()

    # 等待文件下载完成，您可能需要根据实际情况调整等待时间
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("YourDownloadedFileName"))

finally:
    # 关闭浏览器
    driver.quit()
```

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