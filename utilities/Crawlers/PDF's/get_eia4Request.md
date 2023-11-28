---
layout: default
title:  環評書件下載之request版
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 5
last_modified_date: 2023-11-28 10:54:12
tags: Crawlers pdf
---

# 環評書件下載之request版
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

- 因為linux的browser表現不太理想，Chrome是測試版啟動時抓不到driver、Firefox則會直接開啟pdf檔案、而不是只是下載，致使browser關閉不了。
- 經過諮詢GPT之後，改用`requests`比較直接、也比較單純。
- GPT範例

```python
import requests

pdf_url = "https://example.com/path/to/your.pdf"
response = requests.get(pdf_url)

with open("your.pdf", "wb") as pdf_file:
    pdf_file.write(response.content)
```

## 程式差異說明

### 存在C01.PDF檔案的情況

- 原有`driver.get()`改成`requests.get()`
- 原有的`try...excepts`改成`response.headers['Content-Type']`內容之判別。

```python
37,38c32,36
<             try:
<                 driver.get(url)
---
>             response = requests.get(url)
>             if response.headers['Content-Type']=='application/download':
>                 with open(pdf_file, "wb") as f:
>                     f.write(response.content)
>                 # 关闭浏览器
39a38
>                 print(url)
41c40
<             except:
---
>             else:
```

### 只存在000.PDF情況

```python
44,50c43,55
<                      if pdf_file=='C01.PDF':
<                          url=url.replace(pdf_file,'000.PDF')
<                          driver.get(url)
<                          time.sleep(random.uniform(5, 20))  # 等待加载完成，根据需要调整等待时间
<                          break #no more trying
<                      else:
<                          continue #try appendix files
---
>                     if pdf_file!='C01.PDF':continue #try appendix files
>                     url=url.replace(pdf_file,'000.PDF')
>                     pdf_file=url[-7:]
>                     if os.path.exists(os.path.join(os.path.expanduser(target_directory), pdf_file)):break
>                     response = requests.get(url)
>                     if response.headers['Content-Type']=='application/download':
>                         with open(pdf_file, "wb") as f:
>                             f.write(response.content)
>                         # 关闭浏览器
>                         # 生成5到20之间的随机秒数
>                         print(url)
>                     time.sleep(random.uniform(5, 20))  # 等待加载完成，根据需要调整等待时间
>                     break #no more trying
57,58c62
<     # 关闭浏览器
<     driver.quit()
---
```