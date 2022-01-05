---
layout: default
title: unix系統小工具
parent:   Operation System
grand_parent: Utilities
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 檔案查詢
### ls查詢
|alias|usage|full command|arguments|
|----|----|----|----|
|lst|list and sort by **time**察看最新檔案|`ls $1 --show-control-chars -hF --color=tty -lrt\|tail`|目錄、檔案群組(需double quotes)|
|lsS|list and sort by **size**察看最大檔案-自小到大|`ls $1 --show-control-chars -hF --color=tty -lrS\|tail`|目錄、檔案群組(需double quotes)|
|lS|list and sort by **size**察看最大檔案-自大至小|`ls -alhS --color|head`|無引數|
|lsd|list the directories察看目錄|`ls $1 --show-control-chars -hF --color=tty -l|grep "^d"`|目錄、檔案群組(需double quotes)|
|lsr|recursive list跨越目錄察看尋找結果|`ls --show-control-chars -hF --color=tty -ltd $(findc $1)`|檔案群組(需double quotes)|
|lsf|list the finded results察看尋找結果/按時間排序|`ls -lrt $(find . -name "$1")`|檔案群組，不需double quotes|
|lsk|list with certain library|`/usr/local/glibc-2.16/lib/ld-linux-x86-64.so.2 --library-path .:/lib64 /bin/ls`|無引數|

### 尋找檔案
- locate、find見[程式前沿](https://codertw.com/前端開發/392150/)
- findc(find current directory)=`find . -name "$1"`
- lsr、lsf


