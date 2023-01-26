---
layout: default
title: Markdown
parent: Utilities
has_children: true
permalink: /utilities/Markdown/
last_modified_date: 2022-06-17 10:21:23
---

{: .fs-6 .fw-300 }

# Markdown Language and System

## md檔案中植入圖片

### 一般情況

```bash
![...(picture name, will shown if link is missing)](https... location of picture)
```

### 加入檔案是谷歌雲圖片

- see reference [^1]
  - 將圖檔設定「檢視者」為「知道連結的任何人」
  - 複製連結
  - 從連結中取得ID (`https://drive.google.com/file/d/<ID of image>/view?usp=sharing`)
  - 將ID代人下式

```bash
![...(picture name, will shown if link is missing)](https://drive.google.com/uc?id=...)
```

- 如`ID=1bXzYeegauqB2M6-VZwitEeXHmMiYZIUY`，markdown語言寫法則為：

```bash
![Example Image](https://drive.google.com/uc?id=1bXzYeegauqB2M6-VZwitEeXHmMiYZIUY)
```

結果

![Example Image](https://drive.google.com/uc?id=1bXzYeegauqB2M6-VZwitEeXHmMiYZIUY)

- 文中還介紹了html語言的圖片設定範例

```bash
<img src="https://drive.google.com/uc?id=1bXzYeegauqB2M6-VZwitEeXHmMiYZIUY"
     alt="sample image"
     style="display: block; margin-right: auto; margin-left: auto; width: 90%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)" />
```


## Reference

[^1]: Embedding images in google drive to markdown, [intodeeplearning.com][1](2011)

[1]: https://www.intodeeplearning.com/embedding-images-in-google-drive-to-markdown/ "Embedding images in google drive to markdown, May 11, 2022 • 1 min read "