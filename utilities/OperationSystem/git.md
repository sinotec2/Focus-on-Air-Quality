---
layout: default
title: git and github
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-06-13 09:02:53
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
### 定期更新cmaq執行進度
- 基本上只是個`grepDDD=grep DDD $(ls -rt CTM_LOG_000*|tail -n1)|tail -n1)`指令，顯示CTM_LOG的最後日期標籤。
- 運用crontab每分鐘執行GT.cs(如下)、以及html的autorefresh功能，將其內容PO在[https://sinotec2.github.io/cmaqprog/](https://sinotec2.github.io/cmaqprog/)
  - wildcard (` -e *`)用來研判是否檔案存在容易出錯，[可以用](https://www.itread01.com/p/1372201.html)`-n ls`指令取代。
  - 夜間github將會被防火牆擋住，因此需將檔案另存至外部硬碟，由該機直接git上傳。

```bash
#kuang@DEVP /nas2/cmaqruns/2019N3G
$ cat GT.cs
cwd=$PWD
GT=/usr/bin/git
PTH=/nas2/cmaqruns/2019N3G
if [ -n "ls $PTH/CTM_* > /dev/null 2>&1" ];then
  cd ~/GitHubRepos/sinotec2.github.io
  itm=$(ls -rt $PTH/CTM_LOG_000.v532*|tail -n1)
  echo $itm $(grep DDD $itm|tail -n1) >cmaqprog/progres.txt
  HM=$(date -d now +"%H%M")
  if [ $HM -gt 800 ] && [ $HM -lt 1730 ];then
    TOKEN=$(cat ~/bin/git.token)
    DATE=$(date -d now +"%Y%m%d%H%M")
    itm=$(ls -rt $PTH/CTM_LOG_000.v532*|tail -n1)
    echo $itm $(grep DDD $itm|tail -n1) >cmaqprog/progres.txt
    $GT pull
    $GT add cmaqprog/progres.txt
    $GT commit -m "update cmaqprog/progres.txt $DATE"
    $GT push https://sinotec2:$TOKEN@github.com/sinotec2/sinotec2.github.io.git
  else
    /usr/bin/sshpass -f ~/.ssh/.pw scp -q cmaqprog/progres.txt centos8:~/GitHubReps/sinotec2.github.io/cmaqprog/progres.txt
  fi
fi
cd $cwd
```
### Off-Duty-Hour Version GT.cs
- 離線時間（<800 or > 1750）必須透過外部主機進行git上載
- 多了文字檔大小的判斷，如果為空白檔案，則停止執行crontab
- crontab的實際檔案存在/var/spool/cron目錄下，必須root身分才能修改
- 如果還需要再執行GT.cs，還是需要手動開啟crontab.
```bash
#kuang@centos8 /data/cmaqruns/2019base
#$ cat GT.cs
cwd=$PWD
GT=/opt/anaconda3/bin/git
HM=$(date -d now +"%H%M")
if [ $HM -le 800 ] || [ $HM -ge 1730 ];then
  cd ~/GitHubRepos/sinotec2.github.io
  siz=$(wc cmaqprog/progres.txt|~/bin/awkk 2)
  if [ $siz -gt 0 ];then
    TOKEN=$(cat ~/bin/git.token)
    DATE=$(date -d now +"%Y%m%d%H%M")
    $GT pull
    $GT add cmaqprog/progres.txt
    $GT commit -m "update cmaqprog/progres.txt $DATE"
    $GT push https://sinotec2:$TOKEN@github.com/sinotec2/sinotec2.github.io.git
  else
    echo 'no CMAQ is running'
    /usr/bin/sudo sed -i '/GT.cs/s/\*/\#\*/' /var/spool/cron/kuang
  fi
  cd $cwd
fi
```

## 不定期上載
### [update_whnew](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/update_whnew)
- 每次更新FAQ之後，會需要更改首頁的`News at`連結，這個bash的批次檔就是幫助這個過程。
- 因為macOS鎖住~/Documents讓終端機進入的權限（無關使用者權限），必須在Finder的目錄點選【新增位於檔案夾位置的終端機視窗】、或在VisualCode的目錄點選【在整合式終端機中開啟】
- 進入命令列狀態後，將工作目錄移到Focus-on-Air-Quality.git所在根目錄
- 直接執行批次檔`update_whnew`，不需引數。

```bash
#kuang@114-32-164-198 ~/Documents/jtd
#cat update_whnew 
d=~/Documents/jtd
line=$(grep News $d/index.md)
oldDate=$(echo $line|cut -c10-19)
newDate=$(date "+%Y-%m-%d")
lastMD=$(echo $line|cut -d'(' -f2|cut -d')' -f1)
newsMD=https://sinotec2.github.io/Focus-on-Air-Quality$(ls -rt $(findc "*.md")|grep -v index|tail -n1|cut -c 2-)
newsMD=${newsMD/.md//}
if [ $lastMD != $newsMD ]; then
  sed -ie 's#'${lastMD}'#'${newsMD}'#' $d/index.md
  sed -ie '/News/s#'${oldDate}'#'${newDate}'#' $d/index.md
  TOKEN=$(cat ~/bin/git.token)
  git add index.md
  git commit -m "revised index.md"
  git push https://sinotec2:$TOKEN@github.com/sinotec2/Focus-on-Air-Quality.git
fi
if [ -e $d/index.mde ];then rm $d/index.mde;fi
```
- What'sNew 的hyperlink 不是指定到.md檔，.md檔案在另外的github位置，github.io已經將其內容編譯成github.io的index.html，成為該.md檔案專屬特定的目錄。
- index.md單獨上載，比較單純，前提是要將所有的上下載都已經完成。
- dos系統不能適用
- `sed`如果要置換含有`/`(slash)的字串，可以將deliminator轉成其他(任何接在s指令之後的字元，如此處的`#`)，詳見[Unix & Linux：find and replace with sed with slash in find and replace string][1]

[1]: <https://unix.stackexchange.com/questions/378990/find-and-replace-with-sed-with-slash-in-find-and-replace-string> "Not sure if you know, but sed has a great feature where you do not need to use a / as the separator. So, your example could be written as: sed -i 's#/var/www#/home/lokesh/www#g' lks.php It does not need to be a # either, it could be any single character. For example, using a 3 as the separator: echo 'foo' | sed 's3foo3bar3g' bar"

## Reference
- wiki, [git](https://zh.wikipedia.org/wiki/Git), 页面最后修订于2022年3月23日 (星期三) 22:58。
- wiki, [github.com](https://zh.wikipedia.org/zh-tw/GitHub)，頁面最後修訂於2022年3月3日 (星期四) 06:07。
-  高見龍、[使用 GitHub 免費製作個人網站](https://gitbook.tw/chapters/github/using-github-pages)
- 唯鹿、[使用personal access token進行Github認證](https://iter01.com/611911.html) 發表於 2021-08-16
