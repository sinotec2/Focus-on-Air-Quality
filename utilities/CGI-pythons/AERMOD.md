---
layout: default
title: AERMOD
parent: CGI-pythons
grand_parent: Utilities
last_modified_date: 2022-06-07 20:21:17
---
# AERMOD遠端模擬控制程式
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
- 作業目標：給定AERMOD/ISC runstream檔、氣象及地形檔案，啟動遠端執行程式，並提供結果檔案之連結。
- 考量及優勢
  1. 避免本地執行檔之編譯、前後處理程式系統之建置
  1. 使用遠端計算資源
  1. 快速上手、有助進行模式設定敏感性之測試
- 整體架構詳見[ISCST/AERMOD 主程式](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/RemoteSystem/main/)之說明，此處著眼於CGI程式的說明。

## 
