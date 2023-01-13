---
layout: default
title: 費用估算
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 99
date: 2022-04-18 12:26:47
last_modified_date: 2022-04-18 12:26:50
tags: CMAQ nchc_service
---

# 公版模式執行費用估算
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

## 用量統計網址
- [會員中心->計畫管理->我的計畫->計畫資訊->用量統計->區間類型-日區間](https://iservice.nchc.org.tw/module_page.php?module=nchc_service#nchc_service/nchc_service.php?action=nchc_service_usage_statistic&uuid=33b3eda2-480b-40aa-97cc-5dddec5540c5&searchs_type=member&searchs_date=day&searchs_str=111/04/15&searchs_end=111/04/17&service_type=&detail_search=)

|姓名| 	狀態|	111/04/15| 	111/04/16| 	111/04/17| 	小計|
|-|-|-|-|-|-|
|曠博士|計畫建立者|	8.5714| 	5.3424| 	0| 	13.9138|
|小計| 	  	|8.5714| 	5.3424| 	0| 	13.9138| 

## 單價
- 13.9/(5218/200)=0.53元/min@200CPU
- [表列單價](https://iservice.nchc.org.tw/module_page.php?module=nchc_service#nchc_service/nchc_service.php?action=su_apply_step_1&prj_uuid=33b3eda2-480b-40aa-97cc-5dddec5540c5&prj_mode=personal) 0.16元/核心小時 *200/60
  - = 0.53 元/min

- 台灣杉三號運算費
  - Reserved Queue, RQ有優先性
  - Reserved Time Slot Queue, RTSQ最貴
  - Non-Reserved Queue最便宜


|類別| 費率(元/核心小時) |租用期限|
|-|-|-|
|RQ|0.8 |7≤租期≤30|
||0.64| 30<租期≤90|
||0.56| 90<租期≤180|
||0.48| 180<租期≤365|
|RTSQ |RQ對應費率3倍| 比照QR期程|
|NRQ| 0.16| 無|


## 複價
### file-time estimates
- (datetime(2022,2,24,16,1)-datetime(2022,2,16,21,34)).days/11 * 12 * 24 * 60 * 0.53 元/min
  - = **7.63** days * 24 * 60 * 0.53 元/min
  - = **5828.07**元
- （12個月似乎不是連續操作）

### job-time estimates
- 4/15~16 共run了（5+3=8）次，每次約26min/8~3min,全年應約～1200min
- 全年job billing=1200*0.53～600元

## 儲存空間
- 免費空間
  - 台灣杉1/3號(計算/暫存位置)：
  - /home/$USERNAME (100G)
  - /tmp/(arbitary) (100G、但不能用做為Slurm執行之IO、連結也不能)
- 台灣杉一號儲存費用：5000 NTD/TB/年
  - 1.5T\~4.5T 約需7.5K\~22.5K NTD/yr
- 台灣杉三號(HFS)：4 NTD/GB/月

## 批次運作規劃
- job sequence
  - 上載->解壓縮
  - sbatch執行CCTM、combine
    - 每日結果刪除只剩CCTM_A*
  - ncks -v and ncrcat
  - 刪除、壓縮、下載
- 每月至少(輸入30G+CCTM_A 33G~)60G。
  - 免費額度(200GB)可同時做3個批次
  - input放在/tmp，輪流複製到$HOME進行模擬
  - ncks結果暫時放在/tmp，再慢慢scp回到local

