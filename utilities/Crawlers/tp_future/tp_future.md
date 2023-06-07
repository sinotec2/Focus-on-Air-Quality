---
layout: default
title:  Download Hiway Forecasting Data
parent: Crawlers
grand_parent: Utilities
has_children: true
last_modified_date: 2023-06-07 16:17:56
permalink: /utilities/Crawlers/tp_future
tags: Crawlers tp_future
---

# 高公局車行時間預測數據之批次下載
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

- 高速公路局對外提供未來任意日時、10條路線、共228個匝道出入口作為起、起端之行車時間預測([高速公路1968](https://1968.freeway.gov.tw/tp_future))。
- 該預測時間與路況相關，具有未來交通量之參考依據。唯數據並未提供批次下載，須一一選單後執行「立即規劃行程」，方能得知。
- 此處以selenium(4.9.1版)與BeautifulSoup(4.12.2版)作為下載與解析之模組，並將結果存成csv檔案。
- 程式見於[github]()