---
layout: default
title: local Jekyll Webblog
parent: Markdown
grand_parent: Utilities
last_modified_date: 2022-11-15 10:21:23
---

# 本地git系統與部落格之發布
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景

- 地端git有其必要與特殊性，在機敏程式的發展與協作歷程有其特定的腳色功能。
- 進一步要問的就是：可否像GithubPage一樣，用git來執行jekyll的編譯，將md檔案也編成美美的部落格頁面?答案是肯定的。

## Jekyll、Gitea、Drone 和 Docker

- Josh Illes(2020) [Deploying a Jekyll Site with Drone and Gitea](https://joshilles.com/server/jekyll/gitea-drone-docker/)這個實例是用docker來布建所有的系統，包括[Gitea](https://about.gitea.com/)伺服器與[Drone](https://www.drone.io/)環境設定。  
- 這個網頁是一篇教學文章，介紹如何使用 **Jekyll**、**Gitea**、**Drone** 和 **Docker** 來建立一個個人的部落格平台。文章的主要內容如下：
  - **Jekyll** 是一個靜態網站生成器，可以將 Markdown 檔案轉換成 HTML 網頁，並提供多種主題和插件。
  - **Gitea** 是一個輕量級的 Git 服務，可以讓使用者在自己的伺服器上建立和管理 Git 倉庫，並提供網頁介面和 API。
  - **Drone** 是一個持續整合和持續交付的平台，可以自動化 Jekyll 網站的建置和部署，並支援 Docker 容器。
  - **Docker** 是一個開源的容器平台，可以讓使用者將應用程式和相關的環境打包成一個可移植的單元，並在任何支援 Docker 的系統上執行。
  - 文章詳細說明了如何安裝和設定這些工具，並提供了相關的程式碼和截圖，以及一些常見的問題和解決方法。
  - 文章還提供了一些參考資料，包括官方文件、教學影片和相關的部落格文章。  

## GitHub Pages 与 Gitee Pages 上的 Jekyll

