---
layout: default
title: Works on NCHC
parent: Forecast Systems
nav_order: 6
date: 2023-03-24
last_modified_date: 2023-03-24 09:37:04
has_children: true
permalink: /ForecastSystem/WorkOnNCHC
mermaid: true
tags: forecast CMAQ nchc_service m3nc2gif
---

# 國網上預報系統的運作方式

## 背景

- 將系統移轉到[國網][nchc]似乎是個不能避免的趨勢與抉擇，[國網][nchc]與本地超微工作站的比較考量如下：

項目|[國網][nchc]|超微|說明
-|-|-|-
供電及網路穩定性|高|低|後者受到大樓內外主客觀因素干擾
軟硬體維護|專人負責|自行負責|前者含在費用之中
費用負擔|按使用收費|批次採購|後者折舊分攤沈重
儲存裝置|不提供自行備份|自行備份|前者增加傳輸困難
運維人力需求|低|高|前者只需自行負責專案部分

- 統移轉到[國網][nchc]遭遇到的困難與解決方案考量
  - pnetcdf格式相容性問題：
    - mcip的[問題](#序列運作方案)與[解決方案][trans]
  - 磁碟機使用上限
    - wrf執行需要近80G、cmaq執行一個domain也會需要近200G。
    - 目前以手動方式一面執行、一面清理方式進行。如果要自動連續執行，需有外部磁碟機連線(如aws s3)或[其他方案][fs]才行。
  - crontab的替代
    - 國網並未開放crontab的使用
    - 目前似乎還沒有好的替代方案，或許只能手動啟動、tmux + while true方案。


{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

[nchc]: https://iservice.nchc.org.tw/nchc_service/nchc_service_twn3_hpc.php "國研院國網中心台灣杉三號(Taiwania 3)為國內提供開放服務申請的最大CPU高速計算主機(2021年)，擁有900個計算節點。"
[trans]: ../../wind_models/WRFOUT/2.TransWrfout.md "因應intel MPI轉換wrfout格式"
[fs]: ../../GridModels/TWNEPA_RecommCMAQ/IO_Files.md#公版模式輸入輸出檔案及傳輸管理 "公版模式輸入輸出檔案及傳輸管理"
