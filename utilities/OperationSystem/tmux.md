---
layout: default
title: TMUX 終端機多工器
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-03-11 15:46:30
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
# TMUX 終端機多工器
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
  - 偶爾要切換整個作業環境系統，如csh/bash、bash/zsh等等
  - 切換使用者如root，雖然sudo很好用但是macOS不能設定免密的sudoers，`tmux`就是很好的替代方式。
- WHO(`tmux`的限制，使用者必須要習慣或有辦法接受)
  - `tmux`不會大量儲存螢幕輸出，可能為節省記憶體或其他技術因素。如果螢幕輸出對使用者很重要，建議以接引到檔案方式較保險，如果在偵錯階段、又不能輸出到檔案，`tmux`就不太適用了。
  - `tmux`的`session`間是不能互相呼叫，必須回到OS，再切換到另一`session`。`tmux`不能再呼叫`tmux attach`指令，只能接受`tmux ls`。
  - `tmux`間的`history`不能互用，高度倚賴`history`的使用者會受到很大限制。

## 6個基本的tmux指令
1. `tmux`：開啟一個「新的」多工分支界面，畫面底下會反白、顯示現在界面的名稱（或編號）
1. `tmux ls` ：檢查目前開了那些多工分支，名稱（或編號），範例結果類似
  ```bash
  $ tmux ls
  bcon: 1 windows (created Wed Oct 20 08:20:43 2021) [158x44]
  cctm: 1 windows (created Sun Oct 10 15:17:16 2021) [158x44]
  compile: 1 windows (created Tue Oct 19 10:43:49 2021) [158x44]
  enkf3D: 1 windows (created Tue Oct 19 11:08:54 2021) [158x44]
  find_run.csh: 1 windows (created Wed Oct 20 13:03:28 2021) [158x44]
  post: 1 windows (created Wed Oct 20 17:15:48 2021) [158x44]
  wrf: 1 windows (created Sat Dec 25 16:30:28 2021) [158x44]
  ```
1. `tmux rename-session -t 0 wrf`：將session 0命名為**wrf**
1. `tmux a -t wrf`：再次回到多工分支**wrf**
1. session 狀態依序按下Control-b,d 2個動作：「暫時」離開、回到原來的OS畫面
1. session 狀態下鍵入`exit`：正常關閉一個分支畫面

## nohup and disown
- 雖然很多新的OS版本不再支援nohup，但對很多傳統使用者，nohup還是丟不掉的老習慣。
- 開啟NO_HUP

```bash
% setopt NO_HUP
```
- nohup+dosown 背景執行命令，並放棄控制

```bash
nohup <command> & disown
```
- 背景執行之pid掌握
  - 如果將多個、同名、長時間執行的程式放在背景執行，要辨認哪個作業的pid是幾號(例如呼叫CGI程式)，還蠻困擾的。
  - 此時在submit(sub、nohup...)之後，隨即將$!記錄下來，這樣追蹤該項作業的進行狀態就容易很多
```bash
nohup $EXE &
n=$!
top -pid $n
echo $n
psg $n
```


## Reference
- wiki, **tmux**, [wikipedia](https://zh.wikipedia.org/wiki/Tmux), 最后修订于2021年6月10日
- pityonline, **tmux-Productive-Mouse-Free-Development_zh**, [gitbooks](https://aquaregia.gitbooks.io/tmux-productive-mouse-free-development_zh/content/index.html)
- **Exit zsh, but leave running jobs open?**, [stackoverflow](https://stackoverflow.com/questions/19302913/exit-zsh-but-leave-running-jobs-open)
- John Perkins, **How to Run Bash Commands in the Background in Linux**, [maketecheasier](https://www.maketecheasier.com/run-bash-commands-background-linux/),Jan 15, 2021
- slovyz [Shell脚本中$0、$?、$!、$$、$*、$#、$@等的意義](https://blog.csdn.net/slovyz/article/details/47400107)
