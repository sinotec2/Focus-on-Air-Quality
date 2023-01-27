---
layout: default
title: Crawlers
parent: Utilities
has_children: true
permalink: /utilities/Crawlers/
last_modified_date:   2022-10-13 09:06:38
tags: crontab Crawlers CODiS
---

{: .fs-6 .fw-300 }

# 批次下載作業相關程式

## 基本說明

- [網路爬蟲][crawler]是一類越來越普及的資訊技術[^1]，此處使用此一名詞稱呼批次下載作業技術，僅為[網路爬蟲][crawler]部分功能，此處不涉及無特定目標的[索引作業](https://en.wikipedia.org/wiki/Search_engine_indexing)。
- 下載或上傳
  - 包括定期或不定期，前者是運用電腦的排程控制、定期執行特定程式上網進行驗證、搜尋、畫面截取、下載等，「合理流量」的作業。
    - 數據檔案之下載一般使用wget或cURL[^4]
    - 後者雖為手動批次進行，也可能因無約束而造成網路攻擊事件。
  - 至於上網填報、上傳檔案等上載作業，除非對方網站允許，一般是不接受機器人作業方式的。
  - 無目標、通用性目標之爬蟲行為，此處並不加以討論。
- 此處之作業對象包括：
  1. 官方網頁提供之公開數據、文件、圖片、或文字
  2. 官方或商務網頁提供之畫面、影片
- 下載頻度與流量之控制
  - 雖然大多數具有管理的網站，都會設定訪問頻率與下載流量的門檻，對不同需要的使用者提供不同程度的應對與資源分配，但下載者還是需要合理管理自己的程式與設定，避免造成遠端網站的拒絕或傷害。
  - 除此之外，因下載數據量很龐大，也需在本地儲存、處理、品管、應用等等，有良好的管理。
- 由於是專案性質的應用，因此詳盡的技術細節、設定說明、與應用實證，見諸專案筆記，此處僅就一般或共同部分加以彙總。
  1. 網站特性之解析與應對策略
  2. 電腦排程之設定[^3]
  3. 下載工具與程式
  4. 後續應用及發展

## 定期爬蟲專案簡介

- 自2016年以來陸續建置自動數據下載的專案條列如下。

### 氣象數據方面

- 觀測與再分析數據
  1. 中央氣象局(CWB)每天公開其自動站觀測結果在[CODiS(CWB Observation Data Inquire System)網站](https://e-service.cwb.gov.tw/HistoryDataQuery/)，此處每日12時執行全國昨日監測結果的下載，詳[CODiS筆記](../../wind_models/CODiS/codis.md)。
  2. 美國[NCEP數據之每日下載](../../wind_models/NCEP/NCEP.md)：為氣象模式起始與邊界、同化等等所需要之觀測(或再分析)數據檔案，包括[再分析結果](../../wind_models/NCEP/ff.py.md)、[地面](../../wind_models/NCEP/ss.py.md)及[高空](../../wind_models/NCEP/uu.py.md)觀測、以及[海溫](../../wind_models/SST.md)。
- 氣象模式產品
  1. 中央氣象局數[值預報產品之下載](../../wind_models/cwbWRF_3Km/1.get_M-A0064.md)：每日逐6小時下載，應用在[軌跡模式預報](https://sinotec2.github.io/cpuff_forecast/)、[網格空品模式預報](../../GridModels/ForecastSystem/10.fcst.cs.md)等等即時性的需求、同時也因應[MMIF](../../PlumeModels/ME_pathways/mmif_caas.md)、[歷史軌跡分析](../../TrajModels/btraj_WRFnests/traj3Dnew.md)等等年度分析。  
  2. 美國國家氣象局(NWS)全球尺度氣象數值預報模式和變分分析([GFS](https://en.wikipedia.org/wiki/Global_Forecast_System))逐日預報檔案之[自動下載](../../wind_models/GFS/2.GFS2WRF.md)：用在驅動每日的東亞、南中國等地區氣象場的模式模擬，用以進行[網格空品模式預報][fcst]@iMacKuang[^2]
- 天氣報告與天氣圖
  1. 中央氣象局逐6小時天氣預報(文字稿)及天氣圖
  2. 逐6小時NOAA天氣圖下載：[6-Hourly NCEP/NCAR Reanalysis Data Composite](https://psl.noaa.gov/data/composites/hour/)，提供東亞範圍之天氣圖。

### 空氣品質部分

- 環保署空品監測數據下載
  1. 逐時aqi數據之下載
  1. 逐月全台空品測站數據之下載
- 特殊性工業區空品監測數據下載
- [CAMS預報數據](../Graphics/earth/wind_ozone.md)
- [日本大氣污染情報網站圖面之下載](../../AQana/RegAQ/pm25.jp.md)

### 排放活動部分

- CEMS
- 電廠運轉率
- 交通量

## 批次爬蟲專案

### 全球空品模擬數據

- [CAMS近實時空品數據之下載](../../AQana/GAQuality/ECMWF_NRT/1.NRTdownload.md)
- [CAM-chem模擬結果之下載](../../AQana/GAQuality/NCAR_ACOM/CAM-chem.md)
- [MOZART(WACCM)](../../AQana/GAQuality/MOZART.md)

### 空品畫面之截取

- earth.nullschool.net
- Windy網頁畫面
- airvisual

### 其他

- 癌症數據之下載
- 同仁發表文獻資料庫之建立

## Reference

[^1]: wiki、網路爬蟲（英語：web crawler），也叫網路蜘蛛（spider），是一種用來自動瀏覽全球資訊網的網路機器人。其目的一般為編纂網路索引。"
[^2]: 運用GFS/CWB/CAMS數值預報數進行台灣地區CMAQ模擬實例、[http://125.229.149.182:8084/](http://125.229.149.182:8084/)@iMacKuang[^9]
[^3]: G. T. Wang, Linux 設定 crontab 例行性工作排程教學與範例,[G. T. Wang, 2019/06/28](https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/)
[^4]: [知乎](https://www.zhihu.com/question/19598302)：cURL 和 Wget 的优缺点各是什么？
[^9]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。敬請逕洽作者：sinotec2@gmail.com.

[crawler]: <http://200.200.12.191/?c=SinoTech&m=load_one&r=hour&s=by%20name&hc=4&mc=2> "網路爬蟲（英語：web crawler），也叫網路蜘蛛（spider），是一種用來自動瀏覽全球資訊網的網路機器人。其目的一般為編纂網路索引。"
[fcst]: <http://125.229.149.182:8084/> "運用GFS/CWB/CAMS數值預報數進行台灣地區CMAQ模擬實例"
[crontab]: <https://blog.gtwang.org/linux/linux-crontab-cron-job-tutorial-and-examples/> "G. T. Wang, Linux 設定 crontab 例行性工作排程教學與範例,G. T. Wang, 2019/06/28"
[w_c]: <https://www.zhihu.com/question/19598302> "知乎：cURL 和 Wget 的优缺点各是什么？"