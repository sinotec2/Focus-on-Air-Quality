---
layout: default
title: "dowrf"
parent: "REAL"
grand_parent: "wind models"
nav_order: 3
date:               
last_modified_date:   2021-11-29 16:48:48
---

# dowrf

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

## 背景
- WRF主程式(`wrf.exe`)的執行和REAL是在同一個工作目錄下進行(run)，因所有的初始化(`wrfinput_d01`~`wrfinput_d04`)、邊界條件(`wrfbdy_d01`)、底層條件(`wrflow_d01`~`wrflow_d04`)、FDDA相關檔案都已經產生或連結好，因此可以直接在run目錄執行wrf。
- `wrf.exe`是整個過程最耗時的程序，因此其平行化需仔細安排。
-

## dowrf



## Reference
- akuox, **linux date 指令用法@ 老人最愛碎碎念:: 隨意窩Xuite日誌**, [Xuite](https://blog.xuite.net/akuox/linux/23200246-linux+date+%E6%8C%87%E4%BB%A4+%E7%94%A8%E6%B3%95), 2009-04-06
- Terry Lin, **Linux 指令SED 用法教學、取代範例、詳解**, [terryl.in](https://terryl.in/zh/linux-sed-command/),	2021-02-11 
- weikaiwei, **Linux教學：cat指令**, [weikaiwei.com](https://weikaiwei.com/linux/cat-command/), 2021
- G. T. Wang, **Linux 計算機bc 指令用法教學與範例**, [gtwang](https://blog.gtwang.org/linux/linux-bc-command-tutorial-examples/), 2018/08/23
- G. T. Wang, **Linux 的nohup 指令使用教學與範例，登出不中斷程式執行**, [gtwang](https://blog.gtwang.org/linux/linux-nohup-command-tutorial/), 2017/09/12
