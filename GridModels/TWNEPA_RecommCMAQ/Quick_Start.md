---
layout: default
title: 快速啟動
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 1
date: 2022-04-18 11:07:14
last_modified_date: 2022-04-18 11:07:17
tags: CMAQ nchc_service
---

# 公版模式快速啟動
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

## 國網帳戶設定
- [註冊](https://iservice.nchc.org.tw/nchc_service/index.php?lang_type=#secondPage)
- 申請新計畫/加入既有計畫
  - [申請新計畫](https://iservice.nchc.org.tw/nchc_service/nchc_account_verify.php?return_address=767786f8-66fc-40e9-8c15-351a48c8ad2c)
  - 加入既有計畫[會員中心>計畫管理>申請加入計畫](https://iservice.nchc.org.tw/module_page.php?module=nchc_service#nchc_service/nchc_service.php?action=join_apply_list)    

## 上傳模式及檔案
- 位址
  - 台灣杉1號
    - 140.110.148.11\~12 
    - 小型計算、無平行計算
  - 台灣杉3號
    - twnia3.nchc.org.tw(lgn1~4共4個節點共用一個domain name)
    - 平行計算功能
- 儲存空間  
    - /home/$USERNAME (跨節點、100G、不能更改群組gid)
    - /**work**/$USERNAME (跨節點、100G、可提供群組使用)
    - 節點lgn301~4:/tmp/(arbitary) (100G、不能做為Slurm執行之IO、連同一節點也不能)
- OTP(one-time password)認證碼[顯示](https://iservice.nchc.org.tw/module_page.php?module=nchc_service#nchc_service/nchc_service.php?action=nchc_motp_unix_account_edit)、使用瀏覽器延伸功能[快速複製OTP](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/module_slurm/#快速取得OTP的作法)
- scp -r $USERNAME:$HOSTNAME_1:$PATH/$FILE $USERNAME:$HOSTNAME_2:$PATH

## 執行模擬

1. 由lgn303:/tmp/sinotec2複製所有內容到家目錄(\~)
1. 工作目錄：~/cmaq_recommend/*yymm*
1. 設定起訖時間：~/cmaq_recommend/*yymm*/[project.config](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#模擬案例與時間projectconfig)
1. setting IO path and files(主程式):~/cmaq_recommend/*yymm*/[run.cctm.03.csh](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#主程式runcctm03csh)
1. setting LD_LIBRARY_PATH:[~/cmaq_recommend/exec.sh](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#effective-libs)
1. prepare ocean.ncf:~/cmaq_recommend/work/2019-01/grid03/ocean/[run.ocean.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/run.ocean.sh.TXT))
1. Start mpirun：[~/bin/gorun.sh](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/module_slurm/#sbatch) 200 [run.cctm.03.csh](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#主程式runcctm03csh)，(詳見[[module_slurm#SBATCH]]
1. Link daily and combine：~/cmaq_recommend/[combine.sh](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#combine-腳本)
1. 查驗執行情形
1. Compression：`ncrcat -4 --cnk_map nc4 --cnk_plc all -L3 $RAWFILE $CMPRSFILE`

## 後處理
1. 讀出combine.sh逐日檔其中之法規污染項目：[shk.cs](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs)、ncrcat整合全月結果
1. 啟用python模組：[module](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/module_slurm/#usage-of-module-commands) load pkg/Python/3.9.7 
1. 計算濃度差異：[dNC](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/dNC/) old.nc out.demo.conc.nc old-new.nc &
1. 時間空間的最大值：[mxNC](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/mxNC/) old-new.nc 

## Reference and Material
- 台灣杉3號lgn303:/tmp/sinotec2
- [教育訓練教材](https://drive.google.com/drive/mobile/folders/1_GdUsRXQU1p8QhwwDbhz-nVhgUQBbftX?usp=sharing)