---
layout: default
title: TMUX 終端機多工器
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 背景
- WHAT：
  -`tmux`是幾乎每個unix家族OS系統都會有的指令。
  - 全名是terminal([終端機](https://zh.wikipedia.org/wiki/%E7%B5%82%E7%AB%AF)) multiplex([多工](https://en.wikipedia.org/wiki/Multiplex))
  - 
- WHY：
  - 用來開啟、分割、切換、管理終端機的畫面、工作目錄、作業環境等等。
  - 在終端機上進行的程式、tmux會負責其持續進行，不會讓程式在使用者離開終端機後就結束，因此完全取代傳統[nohup](https://zh.wikipedia.org/wiki/Nohup)的類似功能
- WHO/WHERE/WHICH
  - 檔案在/usr/local/bin/tmux，每個使用者都可以使用
-WHEN：
  - 工作目錄繁雜，常常要切換、遊走在各目錄間。
  - 切換特定環境變數情況，如程式路徑、LD_LIBRARY_PATH等
  - 偶爾要切換整個作業環境系統，如csh/bash、bash/zsh等等，
  -   

## 基本指令
- `tmux`：開啟一個「新的」多工分支界面，畫面底下會反白、顯示現在界面的名稱（或編號）
- `tmux ls` ：檢查目前開了那些多工分支，名稱（或編號）

```bash
$ tmux ls
0: 1 windows (created Wed Dec 29 21:59:00 2021)
```
- session 狀態依序按下Control-b,d 2個動作：離開、回到原來的OS畫面
- `tmux rename-session -t 0 wrf`：將session 0命名為**wrf**
- `tmux a -t wrf`：再次回到多工分支**wrf**
