---
layout: default
title: NDOWN
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
- 除了雙向巢狀網格的模擬方式，wrf當然也可以接受循序、單向之巢狀網格模擬，亦即將上層網格結果，作為下層網格的初始即邊界條件，所使用的讀取程式，即為[ndown]()。

1. coarse-to-fine grid ratio is only restricted to be an integer. An integer less than or equal to 5 is recommended
2. 一次只能讀一個wrfout，產生下一層domain所需的IC/BC，
   如果同時run了3層,還是只有由第一層移轉第二層，因此原本的namelist.input必須修改(→~.ndown3to4)如果要ndown第三層到第四層，必須將第三層命名為「第一層」，第四層即為「第二層」注意除了網格起始點位置、網格點數之外，也要修改網格間距。
3. 其他修改重點
	1. io_form_auxinput2 = 2 in the &time_control section of namelist.input
	2. interval_seconds                    = 21600 → 3600這個值是邊界檔的時間間距原來最外層的邊界檔只有每6小時1筆，現在則是按照wrfout的結果：每小時1筆。
4. 執行
   準備wrfndi_d02
		- Edit the namelist.input file, changing ‘max_dom = 2’, and making surecolumns 1 and 2 are set-up for a 2 domain run, editting the correct start time and grid dimensions.
		- Run real.exe. This will produce a wrfinput_d01 file, a wrfinput_d02file, and a wrfbdy_d01 file.(useless)
		- Rename the wrfinput_d02 file to wrfndi_d02(essential).
	執行ndown
		-將wrfout連結成wrfout_d01_...
		-執行ndown將產生wrfinput_d02 and wrfbdy_d02 file.
		- 將wrfinput_d02重新命名為wrfinput_d01，
		- 將wrfbdy_d02命名為wrfbdy_d01
		- ndown之後要跑WRF也只有一層，也要修改namelist.input。(~.nest4only)注意其他檔案順序，如wrffdda_d04與wrfsfdda_d04等，也必須改成d01
	執行wrf
		- 2015/10/06~08在kuang@61-556 /cygdrive/e/WrfRuns/201310執行的是WRF V3.6.1 MODEL
		- 用以比較OBS_DOMAIN+sfdda+fdda的單向巢狀處理，
		- 有少部分啟動LES還未用到V3.7 high-res版本
	Ndown and OBS_domain 的比較 
初期和三天後模擬結果都還算蠻接近的NDOWN結果的規則性與系統性較高，OBSdomain在局部則較為紛亂，
avrgvsobss-k結果：NDown 62.4%,OBSdomain73.0% 
主要因為風速高估比較嚴重。可能原因: 
缺乏domain外作用力的牽制，sfdda比fdda更差，OBS_DOMAIN又較sfdda更差，d4only又更差，調整機制是否有錯!可否直接用EPAst之obs_domainobs_domain:Attainment OB_TMP  GE_TMP  OB_WS   GE_WS   OB_WD   GE_WD
                                                              73.0%   46.6%   89.7%   34.5%   81.0%   89.7%   96.6%
		1. ndown:Attainment        OB_TMP  GE_TMP  OB_WS   GE_WS   OB_WD   GE_WD
                                                              62.4%     48.3%    89.7%  13.8%   46.6%     79.3%     96.6%
- only nest 4 所需時間(2013/10/08~10共72hr)Oct  6 21:23 namelist.outputOct  8 10:13 wrfout_d01_2013-10-08_00_00_00共37hr50min ,約2:1原1:1。可見約一半的時間在d4的計算

## Reference
