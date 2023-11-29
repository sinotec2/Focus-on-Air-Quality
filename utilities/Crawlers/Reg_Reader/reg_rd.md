---
layout: default
title:  Regulation Reader
parent: Crawlers
grand_parent: Utilities
has_children: true
last_modified_date: 2023-11-28 04:55:25
permalink: /utilities/Crawlers/Reg_Reader
tags: Crawlers pdf
---

# Reg_Reader
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

- 這系列的爬蟲工作是針對法務部[全國法規資料庫](https://law.moj.gov.tw/Index.aspx)中與環境相關的內容，進行自動下載。
- 因為內容全部都是文字，下載量很少，就沒有特別用停等來間隔下載工作。
- 同樣的，下載區分2個階段，先下載法規的位置，從中讀取法規的編號，再由編號進到個別法規的網頁、進行下載與解析。
- 解析結果：
  - 目前只有區分條序及其內容的json檔、並未區分每條條文中的項、目，先試行送進AI作為前提進行解讀。
  - 未來是否要繼續解析、甚而在地端複製該查詢系統，還可以再行考慮。
