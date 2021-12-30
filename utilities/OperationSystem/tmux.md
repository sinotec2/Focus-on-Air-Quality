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
  - `tmux`是幾乎每個unix家族OS系統都會有的指令。
  - 全名是terminal([終端機](https://zh.wikipedia.org/wiki/%E7%B5%82%E7%AB%AF)) multiplex([多工](https://en.wikipedia.org/wiki/Multiplex))
  - 此處的「工」不是指特定的某一個程式，分給不同CPU、不同電腦來執行的「工」，而是終端機界面上的**互動作業**，如檔案查詢整理、程式編輯測試執行、等等目的，環境包括工作目錄、作業環境變數與系統等等，在`tmux`來看，為一「分支」，類似研討會有大會、有各個領域主題的分支會議**session**的概念。`tmux`則是各個分支會議**session**的總管理者。
- WHY
  - 用來開啟、分割、切換、管理終端機的畫面、工作目錄、作業環境等等，同一個終端機程式(如[putty](https://zh.wikipedia.org/wiki/PuTTY)、[mobaXTerm](https://ithelp.ithome.com.tw/articles/10220846))即可遊走各環境，減省本地電腦記憶體負荷)。
  - 在終端機上進行的程式、tmux會負責其持續進行，不會讓程式在使用者離開終端機後就結束，因此完全取代傳統[nohup](https://zh.wikipedia.org/wiki/Nohup)的類似功能。
  - 使用`tmux`後再也不必使用`nohup`、`disown`、再也不必擔心終端機會因為time-out被主機切斷連線。
- WHERE/WHICH
  - 檔案在/usr/local/bin/tmux，每個使用者都可以使用
- WHEN
  - 工作目錄繁雜，常常要切換、遊走在各目錄間。
  - 切換特定環境變數情況，如程式路徑、LD_LIBRARY_PATH等
  - 偶爾要切換整個作業環境系統，如csh/bash、bash/zsh等等，
- WHO(`tmux`的限制，使用者必須要習慣或有辦法接受)
  - `tmux`不會當量儲存螢幕輸出，可能為節省記憶體或其他技術因素。如果螢幕輸出對使用者很重要，建議以接引到檔案方式較保險，如果在偵錯階段、又不能輸出到檔案，`tmux`就不太適用了。
  - `tmux`的`session`間是不能互相呼叫，必須回到OS，再切換到另一`session`。`tmux`不能再呼叫`tmux attach`指令，只能接受`tmux ls`。
  - `tmux`間的`history`不能互用，如果使用者倚賴`history`，會受到很大限制。

## 6個基本的tmux指令
1. `tmux`：開啟一個「新的」多工分支界面，畫面底下會反白、顯示現在界面的名稱（或編號）
2. `tmux ls` ：檢查目前開了那些多工分支，名稱（或編號），範例結果類似

```bash
$ tmux ls
0: 1 windows (created Wed Dec 29 21:59:00 2021)
```
3. `tmux rename-session -t 0 wrf`：將session 0命名為**wrf**
4. `tmux a -t wrf`：再次回到多工分支**wrf**
5. session 狀態依序按下Control-b,d 2個動作：「暫時」離開、回到原來的OS畫面
6. session 狀態下鍵入`exit`：正常關閉一個分支畫面


## Reference
- wiki, **tmux**, [wikipedia](https://zh.wikipedia.org/wiki/Tmux), 最后修订于2021年6月10日
- pityonline, **tmux-Productive-Mouse-Free-Development_zh**, [gitbooks](https://aquaregia.gitbooks.io/tmux-productive-mouse-free-development_zh/content/index.html)