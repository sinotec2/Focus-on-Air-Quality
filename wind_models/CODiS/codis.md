---
layout: default
title: CWB Obs. Data Inquire Sys.
parent: "wind models"
nav_order: 1
has_children: true
permalink: /wind_models/CODiS/
last_modified_date:   2021-11-28 22:04:23
---

{: .fs-6 .fw-300 }

# CODiS
中央氣象局數據每天公開其自動站觀測結果在[CODiS](https://e-service.cwb.gov.tw/HistoryDataQuery/)(CWB Observation Data Inquire System)網站，其數據過去曾應用在風場的產生、[軌跡](https://github.com/sinotec2/cwb_Wind_Traj)之追蹤、以及轉換成little_r格式以進行4階同化等等作業過程。

## What's Learned
- 資料處理[pandas](https://hackmd.io/@wiimax/10-minutes-to-pandas)、網頁[爬蟲程式](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)、自動執行[排程](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/)、下載程式[wget](https://blog.gtwang.org/linux/linux-wget-command-download-web-pages-and-files-tutorial-examples/)及[curl](https://blog.techbridge.cc/2019/02/01/linux-curl-command-tutorial/)
- [twd97座標轉換](https://pypi.org/project/twd97/)、
- 檔案格式：[FortranFile](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.FortranFile.html)、[fortranformat](https://pypi.org/project/fortranformat/)、[KML](https://en.wikipedia.org/wiki/Keyhole_Markup_Language)