---
layout: default
title: ndown
parent: REAL & WRF
grand_parent: WRF
nav_order: 3
date: 2022-02-19 17:56:16               
last_modified_date: 2022-02-19 17:56:21
---

# ndown

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
- 除了雙向巢狀網格的模擬方式，[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)當然也可以接受循序、單向之巢狀網格模擬，亦即將上層母網格結果，作為下層子網格的初始即邊界條件，所使用的讀取程式，即為[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)。
- 適合單向巢狀網格模擬方式的條件狀況
	- 次網格範圍較小、獨立、不會造成上次網格明顯的差異
	- 開啟FDDA，模擬不會與觀測有太大的偏差
	- 雙向巢狀網格太過耗費計算資源，無法進行
	- 需要時間間距較密的wrfbdy檔案
- 中文筆記可以參考[博客園](https://www.cnblogs.com/jiangleads/articles/12825970.html)
- 注意事項
	1. coarse-to-fine grid ratio is only restricted to be an integer. An integer less than or equal to 5 is recommended
	1. 一次只能讀一層的wrfout，產生下一層domain所需的IC/BC

## namelist.input 修改重點
- 執行雙向巢狀網格的[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)、上層單層的[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)之後。將namelist.input進行備份、修改。
- &time_control下
	1. interval_seconds = 21600 → 3600。這個值是邊界檔的時間間距，原來最外層的邊界檔只有每6小時1筆(配合GFS)，現在則是按照wrfout的結果：每小時1筆。
	1. 新增io_form_auxinput2 = 2
- &domains
	- max_dom=1 → 2。執行2層網格，上層為剛剛結束[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)的母網格、下層為則需要wrfbdy的子網格
	- e_we、e_sn、dx、dy、(不動)保持母、子網格的設定與執行[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)時一樣
	- time_step = 240  → 80 。時間步階適度調整，以方便子網格wrf之執行。

### 當[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)同時run了超過2層
- [ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)一次只能執行一層，只能將上層移轉第下層，namelist.input只能接受d01及d02，不能接受d03、d04...
- 因此原本的namelist.input必須修改只留存2層，如果要[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)第三層到第四層，必須將第三層命名為**d01**，第四層即為**d02**
- 注意除了網格起始點位置、網格點數之外，也要修改網格間距、time_step等。

## 執行
- 準備wrfndi_d02：Rename the wrfinput_d02 file to wrfndi_d02
	- wrfinput_d02必須是執行[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)所產生下一層子網格的初始條件。
	- 不能是單層[real]()的rfinput_d01
- 將母網格wrfout檔案，連結成wrfout_d01檔案(時間標籤必須保持一樣)
- 執行[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)
	- 將產生wrfinput_d02 and wrfbdy_d02 file.
	- 將wrfinput_d02重新命名為wrfinput_d01（準備執行子網格[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/))
		- 將wrfbdy_d02命名為wrfbdy_d01
		- [ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)之後要執行子網格的wrf，也要修改namelist.input。(~.nest4only)注意其他檔案順序，如wrffdda_d04與wrfsfdda_d04等，也必須改成d01
- 執行子網格[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)

## ndown and OBS_domain 的比較 
- 初期和三天後模擬結果都還算蠻接近的
- ndown結果的規則性與系統性較高，OBSdomain在局部則較為紛亂，
- avrgvsobss-k結果
	- ndown 62.4%,OBSdomain73.0% 
	- 主要因為風速高估比較嚴重。可能原因: 
		1. 缺乏domain外作用力的牽制，sfdda比fdda更差，OBS_DOMAIN又較sfdda更差，d4only又更差，
		1. 調整機制是否有錯!可否直接用EPAst之obs_domain
- Attainment Comparison
 
|Case|Overall Attainment|OB_TMP|GE_TMP| OB_WS|GE_WS|OB_WD|GE_WD|
|-|-|-|-|-|-|-|-|
|obs_domain|73.0%  | 46.6% |  89.7% |  34.5% |  81.0%  | 89.7%  | 96.6%|
|ndown|62.4%  |   48.3%  |  89.7% | 13.8%  | 46.6%  |   79.3%  |   96.6%|

- only nest 4 所需時間(2013/10/08~10共72hr)
	- Oct  6 21:23 namelist.output
	- Oct  8 10:13 wrfout_d01_2013-10-08_00_00_00
- 原4層雙向共37hr50min
- 約2:1。可見約一半的時間在d4的計算

## Reference
- chinagod, **WRF学习之 ch5 WRF模式（三）运行WRF（d, e）：（双向嵌套，单向嵌套）**, [博客园](https://www.cnblogs.com/jiangleads/articles/12825970.html)posted @ 2020-05-04 23:39 
