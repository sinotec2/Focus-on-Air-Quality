---
layout: default
title:  save_wrose
parent: CGI-pythons
grand_parent: Utilities
date: 2023-01-26
last_modified_date: 2023-01-27 08:07:42
---
# 繪製煙流模式氣象檔案之風花圖
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

- 此處為wrose.py的CaaS版本，獨立程式詳見[風花圖之繪製_wdrose.py](../../PlumeModels/ME_pathways/wrose.md)

網頁計算服務網址：[http://125.229.149.182/wrose.html][1][^1]

- 雖然風花圖的程式已經有很多軟體套件，但是為了檢查煙流模式目的而寫的界面，目前應該是沒有。
- 為了通用在不同的模式之間、也為了打開格式限制，wrose.py加進了輸入檔案格式的辨識，同時也在網頁上貼上範例，讓使用者可以檢視檔案內容，經由比較來了解模式。

### wrose.html

與前述MMIF雷同，但多出範例表格之說明、減省email的詢問。

### save_wrose.py

- 與前述terrain.py雷同（data-auto-download），啟動wrose.py。
- 因應cgi的套件是python 2 的平台，wrose.py也必須改成python 2

### 程式下載

{% include download.html content="風花圖製作之CGI版本[save_wrose.py]" %}


[^1]: 繪製煙流模式氣象檔案之風花圖。上傳準備好的氣象檔案，遠端執行wrose程式結束後，系統會自動下載結果給您(恕僅保留24小時)。[http://125.229.149.182/wrose.html][1][^2]
[^2]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。使用者敬請見諒，逕洽作者：sinotec2@gmail.com.

[1]: http://125.229.149.182/wrose.html "繪製煙流模式氣象檔案之風花圖。上傳準備好的氣象檔案，遠端執行wrose程式結束後，系統會自動下載結果給您(恕僅保留24小時)。"