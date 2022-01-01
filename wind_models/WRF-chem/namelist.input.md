---
layout: default
title: namelist.input
parent: WRF-chem
grand_parent: "WRF"
nav_order: 3
date:               
last_modified_date:   2021-11-25 16:21:24
---

# namelist.input 

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
- 揚沙是WRF-chem最單純的個案，不需任何的排放量數據，由模式按照公式採線上計算產生排放量。
- namelist.input中有關&chem的設定，可以參考[tutorial](https://ruc.noaa.gov/wrf/wrf-chem/tutorialexercises/exe001/namelist.input)
- 網路公開之[手冊](https://ruc.noaa.gov/wrf/wrf-chem/Users_guide.pdf)目前只到3.9版，4版仍在撰寫中。NOAA認為版本間差異不大，[鼓勵]((https://forum.mmm.ucar.edu/phpBB3/viewtopic.php?t=9507))使用者先參閱[Release Note](https://github.com/wrf-model/WRF/releases)。

## &chem之設定
- 共有39項參數，揚沙只需打開下列15項，與[tutorial]()有差異者討論如下
  - `emiss_opt`排放機制選項：範例採`emiss_opt = 3,`會讀取radm2/MADE/SORGAM人為排放量，應無法執行。改為`emiss_opt = 0,`
  - `conv_tr_wetscav`範例採0，沒有次網格洗滌，這應該會造成高估，也非內設作法，是偵錯過程。此值改為內設值1。
  - `aer_ra_feedback`範例也採0。等於粒狀物不影響輻射、溫度、乃至於風場，應為偵錯用途。改為內設值1。

|Option|Description|Value|Meaning|
| ---- | ---- | ---- | ---- |
| kemit |number of vertical levels in the emissions input data file. | 1 | windblown dust from surface |
| emiss_opt |emission scheme| 0 |no external emission|
| chem_opt |chemical mechanism | 401 |Dust concentration only, Simple ash treatment with 10 ash size bins|
| chemdt |time step used by chemistry in minutes| 10 |small enough relative to model dt 180 min|
| aer_drydep_opt | dry depos. of part.| 1 |action|
| dust_opt |dust emiss | 1 |include GOCART dust emissions - need to provide fractional erosion map data|
| gas_bc_opt |gas boundary profile | 1 |uses default|
| gas_ic_opt |gas initial profile | 1 |uses default|
| aer_bc_opt |aer boundary profile | 1 |uses default|
| aer_ic_opt |aer initial profile | 1 |uses default|
| wetscav_onoff |turn on the wet scavenging | 0 | off |
| cldchem_onoff |turn on the cloud chemistry  | 0 | off |
| have_bcs_chem |gets lateral boundary data from wrfbdy data file| .false. |use profile|
| aer_ra_feedback |no feedback from the aerosols to the radiation schemes| 1 | feedback |
| aer_op_opt |aerosol optical properties scheme | 0 |based upon volume approximation |

## Reference
- NOAA, **WRF-Chem Version 3.9.1.1 User's Guide**, [NOAA](https://ruc.noaa.gov/wrf/wrf-chem/Users_guide.pdf)