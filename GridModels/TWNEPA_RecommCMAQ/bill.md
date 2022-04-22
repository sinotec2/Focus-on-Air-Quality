---
layout: default
title: 費用估算
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 99
date: 2022-04-18 12:26:47
last_modified_date: 2022-04-18 12:26:50
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
|曠永銓|計畫建立者|	8.5714| 	5.3424| 	0| 	13.9138|
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

## 相機掃描與瀏覽器擴充功能
- OTP的輸入需要在30秒內執行點選(double click)、Ctrl-C複製、切回ssh登入界面、Ctrl-V貼上，過程還蠻緊張的，貼慢一點就得重來。
- [教材](https://drive.google.com/drive/mobile/folders/1_GdUsRXQU1p8QhwwDbhz-nVhgUQBbftX?usp=sharing)中提到國網OTP的相機掃描功能(設定如下圖1)，是利用瀏覽器自動填入密碼提供的方便門
  - 有Microsoft會員帳號的用戶，使用[Edge]()及Authenticator for Microsoft Edge
  - 使用google帳戶及Chrome者，下載[authenticator擴充套件](https://chrome.google.com/webstore/detail/authenticator/bhghoamapcdpbohphigoooaddinpkbai)  
- 下載Authenticator後、在瀏覽器設定處(右上方選單)啟用該延伸功能
  - 點選圖2的icon後會告知還沒有設定使用者帳號，點選[-]方塊將國網右上方二維條碼納入(內容為登入使用者名稱、只需執行一次)
  - 點選右上方二維條碼icon(圖2)便可隨時顯示6位數OTP(圖3)，點一次即複製。
    - 藍色數字表示正常
    - 如果出現紅字表示時限快到、可以等等再點一次
  - 再到ssh登入對話框貼上即可
  
| ![OTP_iphone.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/OTP_iphone.PNG) |
|:--:|
| <b>圖1以手機相機取得國網OTP並由Edge自動填入</b>|

| ![chrome_extend.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/chrome_extend.PNG) |
|:--:|
| <b>圖2啟動Chrome Authenticator擴充套件後右上方出現icon </b>|

| ![6digit.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/6digit.PNG) |
|:--:|
| <b>圖3Chrome顯示6位數OTP，只需在數字上點1次即複製到剪貼簿</b>|