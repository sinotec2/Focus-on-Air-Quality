---
layout: default
title:  快速掌握程式的執行狀況
parent: HTML
grand_parent: Graphics
last_modified_date: 2022-06-10 23:38:03
---

# 快速掌握程式的執行狀況

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

## 背景與資源方案
- 對大型程式而言，這一題是再普通不過了。工作站上有top指令、有ps指令、linux透過httpd也可以有[ganlia](https://www.796t.com/p/141385.html)、但是對macOS的網路計算服務（CaaS）而言，這些資源似乎沒有這麼方便了。
- 這裏提供一個結合crontab、ps、以及html 3者之合作，將特定程式在遠端工作的情形做一輪播（每分鐘更新）。

### instance
- [http://114.32.164.198/status.html](http://114.32.164.198/status.html)
- 不使用github.io的理由(...還沒時間完成。)

| ![status.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/status.png)|
|:-:|
| <b>iMacKuang模式遠端計算執行監看畫面</b>|


## [status.html](https://github.com/sinotec2/CGI_Pythons/blob/main/status/status.html)
- 定期自動更新
- 讀取特定文字檔案([status.txt](https://github.com/sinotec2/CGI_Pythons/blob/main/status/status.txt))

## [status.cs](https://github.com/sinotec2/CGI_Pythons/blob/main/status/status.cs)
- 因為是網頁要讀取的內容，所有人是_www，必須由root來執行
- 依序執行ps指令
- 將結果輸出到[status.txt](https://github.com/sinotec2/CGI_Pythons/blob/main/status/status.txt)

```bash
ST=/Library/WebServer/Documents/status.txt
date > $ST
for mdl in python mmif aermap aermod iscst cpuff;do
  n=$(ps -ef|grep $mdl|grep -v grep|wc -l)
  echo $n'\t'$mdl'\tjobs are running...' >> $ST
  if [ $n != 0 ]; then
    echo ' '>>$ST
    echo $(ps -ef|head -n1) >>$ST
    ps -ef|grep $mdl|grep -v grep >>$ST
    echo '\t'>>$ST
  fi
done
```
## crontab設定
- 每分鐘執行
```
#status of remote modeling system
*/1 * * * * /Library/WebServer/Documents/status.cs
```