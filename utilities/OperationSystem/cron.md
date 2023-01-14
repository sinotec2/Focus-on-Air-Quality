---
layout: default
title: unix環境中的自動排程cron
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-11-11 09:01:53
tags: crontab
---

{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

# 自動排程程式cron

## cron.d的執行
### cron.d與libc更新
- cron.d與libc及gcc版本有關，如果更新相關程式庫，需reboot以符合版本，否則出現下面錯誤。

```

...
Nov  8 08:35:01 DEVP CROND[53784]: (kuang) CMD (if ! [ -e /home/kuang/mac/do_not_delete ];then /usr/bin/fusermount -u /home/kuang/mac;/usr/bin/sshfs kuang@IMacKuang:/Users ~/mac -o password_stdin < ~/bin/PW;fi)
Nov  8 08:35:01 DEVP CROND[53785]: (kuang) CMD (if ! [ -e /nas3/do_not_delete ];then /usr/bin/fusermount -u /nas3;/usr/bin/sshfs kuang@dev2:/u01 /nas3 -o password_stdin < ~/bin/PW2;fi)
Nov  8 08:36:01 DEVP crond[55611]: (kuang) PAM ERROR (Module is unknown)
Nov  8 08:36:01 DEVP crond[55611]: (kuang) FAILED to authorize user with PAM (Module is unknown)
Nov  8 08:36:01 DEVP crond[55610]: (kuang) PAM ERROR (Module is unknown)
Nov  8 08:36:01 DEVP crond[55610]: (kuang) FAILED to authorize user with PAM (Module is unknown)
Nov  8 08:37:01 DEVP crond[55625]: (kuang) PAM ERROR (Module is unknown)
...
```
- 11/8/8:35 原還可執行crontab的內容，8:36旋即發生錯誤
- [網友](https://www.twblogs.net/a/5c03dc2bbd9eee728c16acb6)建議：

```
root@sasha-lab ~]# vim /etc/pam.d/crond
#
# The PAM configuration file for the cron daemon
#
#
# No PAM authentication called, auth modules not needed
account    required   pam_access.so
account    include    password-auth
#session    required   pam_loginuid.so
session    sufficient   pam_loginuid.so
session    include    password-auth
auth       include    password-auth
說明：session    required   pam_loginuid.so 修改爲：session    sufficient   pam_loginuid.so
```
- 經實證並無效果。reboot之後就好了。

## crontab的設定

- G. T. Wang, **Linux 設定 crontab 例行性工作排程教學與範例**,[G. T. Wang](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/), 2019/06/28
[emoji]: <https://www.webfx.com/tools/emoji-cheat-sheet/> "emoji"