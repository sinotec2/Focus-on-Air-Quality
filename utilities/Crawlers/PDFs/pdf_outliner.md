---
layout: default
title:  PDF檔案大綱之讀取與整理
parent: PDF檔案之下載與整理
grand_parent: Crawlers
nav_order: 5
last_modified_date: 2023-06-12 08:56:43
tags: Crawlers pdf
---

# PDF檔案大綱之讀取與整理
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

- PDF檔案的讀取這一題有悠久的歷史，雖然早期py27時代的經驗並不是很理想，但py37的模組顯然有很大的進步。
- 此處應用的範例是從一個環評報告pdf檔案中讀取其大綱架構、建立從屬關係、並將各段文字拆解放成csv檔案，以備機器學習之用。
  
## Jupyter實例

[outliner.ipynb](outliner.ipynb)

## 個別程式

### 讀取大綱的程式

[pp.py](pp.py)

### 建立從屬關係與拆解程式

[level.py](level.py)
