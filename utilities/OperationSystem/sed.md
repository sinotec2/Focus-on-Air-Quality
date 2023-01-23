---
layout: default
title: sed
parent: Operation System
grand_parent: Utilities
last_modified_date: 2023-01-23 16:19:14
tags: sed 
---

{: .no_toc }

# sed

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 背景

- sed（意為流編輯器，源自英語「stream editor」的縮寫）是一個使用簡單緊湊的程式語言來解析和轉換文字Unix實用程式。 sed由貝爾實驗室的李·E·麥克馬洪於1973年至1974年開發， 並且現在大多數作業系統都可以使用。 sed基於互動式編輯器ed和早期qed的指令碼功能。sed是最早支援正規表示式的工具之一，至今仍然用於文字處理，特別是用於替換命令。 [維基百科](https://zh.wikipedia.org/zh-tw/Sed)

## 置換含有`/`(slash)的字串

[sed](sed.md)如果要置換含有`/`(slash)的字串，可以將deliminator轉成其他(任何接在s指令之後的字元，如此處的`#`)，詳見[Unix & Linux：find and replace with sed with slash in find and replace string][1]

[1]: <https://unix.stackexchange.com/questions/378990/find-and-replace-with-sed-with-slash-in-find-and-replace-string> "Not sure if you know, but sed has a great feature where you do not need to use a / as the separator. So, your example could be written as: sed -i 's#/var/www#/home/lokesh/www#g' lks.php It does not need to be a # either, it could be any single character. For example, using a 3 as the separator: echo 'foo' | sed 's3foo3bar3g' bar"

- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 