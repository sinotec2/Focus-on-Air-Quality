---
layout: default
title: git and github
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
# git and github
## 背景

- WHAT
  - [git](https://zh.wikipedia.org/wiki/Git)(the stupid content tracker)是分散式版本控制、備份系統、多線同步程式發展等等領域常用的指令
  - [github.com](https://zh.wikipedia.org/zh-tw/GitHub)是一個透過Git進行版本控制的軟體原始碼代管服務平台，同時提供付費帳戶和免費帳戶。這兩種帳戶都可以建立公開或私有的代碼倉庫，但付費使用者擁有更多github.page功能。
  - 做為軟體開發者的共同平台，github除代管軟體原始碼，也提供了軟體說明文件管理的功能(github.io)，或做為例行性公布數據的網站，github內部的分支稱為[github.pages](https://gitbook.tw/chapters/github/using-github-pages)。而git則是與該網站溝通的程式。
- WHY
  - 除了使用命令列的git方式，github也發展了[GitHub Desktop](https://desktop.github.com/)介面軟體，應用在window及mac作業環境，以使不熟悉命令列git的使用者也可以很方便地與其交換檔案。
  - 對於定期上/下載作業，還是得依賴工作站crontab以及命令列的git指令。目前[GitHub Desktop]()並沒有定期上下載功能。
  - 有關github.io網站的優缺點，在[這篇](https://gitbook.tw/chapters/github/using-github-pages)有詳細的討論，雖然不接受複雜的PHP或ASP技巧，但是基本的JS還是可以接受的。頻寬也蠻理想的，符合此處之需求。


## git定期上載
- 這項作業的需求是每一天將工作站模式預測模擬結果上載到github.io特定目錄下。此處以[cpuff_forecast](https://sinotec2.github.io/cpuff_forecast/)為例。

### 困難點
- [github page](https://pages.github.com/)的創設：太多可行的方案，讓人無所適從。目前最流暢方案：
  1. 登入github.com網站以其網站對話框界面開設repository(先不要上傳檔案)
  1. 回到本機使用desktop將新的repository在本機(透過網路磁碟機連到工作站)clone一份(空的)，**注意**要指定到PC及工作站可以同時存取的目錄位置。
  1. 在[GitHub Desktop]()開啟編輯器(經推薦以[Visual Studio Code](https://code.visualstudio.com/) VSC較為輕量好用)、以VSC進行目錄及檔案管理
  1. 陸續將工作站網頁內容複製到本機repository、貼在VSD目錄下
  1. 使用[GitHub Desktop]()將網頁內容及js程式推(push)到github
  1. 因網頁內容可能還有需要局部檢查、調整，使用VSC+[GitHub Desktop]()有其方便優勢
  1. 定期更新：交給crontab+命令列git指令
- 定期更新檔案之大小：雖然github.io沒有檔案大小限制，但是檔案太大對使用者、對來訪者都會是流量的負擔。這點更換為VERDI及其向量底圖之後，檔案只剩4~6MB，在可接受範圍。
- 命令列帳密的輸入：幾經改版，很多網友的訊息都是過時、錯誤的指引
  - passwd:2021-08-14 GitHub已經改版，命令列git提交的密碼不再是github網站的登入密碼，而是另外申請的[token](https://iter01.com/611911.html)。
  - https網址組合：也有很多錯誤，必須寫成
  - https://$USERNAME:$TOKEN@github.com/$USERNAME/$DEPOSITORY.git
    - $USERNAME=sinotec2
    - $TOKEN為40碼的字串，需另外在github網頁申請
    - $DEPOSITORY在此次範例為sinotec2.github.io

### [Run.sh](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/Forecast/#網站與播放器)中有關git的部分
- 須至repository目錄下執行
- 先登記此次的更新內容：新增檔案(git add path/file)
- 此次更新的標題訊息：git commit -m "..." (注意必須是**雙引號**)
- 上傳檔案：git push https:...

```bash
#upload to github
TOKEN=$(cat ~/git.token)
if [ -e PMF.gif ];then
  cwd=$PWD
  gtd=/home/kuang/GitHubRepos/sinotec2.github.io
  cp PMF.gif $gtd/cpuff_forecast/example_gifs/
  cd $gtd
  git add cpuff_forecast/example_gifs/PMF.gif
  git commit -m "revised PMF.gif"
  git push https://sinotec2:$TOKEN@github.com/sinotec2/sinotec2.github.io.git
  cd $cwd
fi
```


## Reference
- wiki, [git](https://zh.wikipedia.org/wiki/Git), 页面最后修订于2022年3月23日 (星期三) 22:58。
- wiki, [github.com](https://zh.wikipedia.org/zh-tw/GitHub)，頁面最後修訂於2022年3月3日 (星期四) 06:07。
-  高見龍、[使用 GitHub 免費製作個人網站](https://gitbook.tw/chapters/github/using-github-pages)
- 唯鹿、[使用personal access token進行Github認證](https://iter01.com/611911.html) 發表於 2021-08-16
