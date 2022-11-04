---
layout: default
title: daily_traj.cs
nav_order: 3
parent: 地面二維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-04 14:43:02
---

# daily_traj.cs程式說明
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
- 這支程式每天凌晨進行北中南測站反軌跡的計算，並將結果更新到[GitHub Pages](https://sinotec2.github.io/traj/)網頁畫面。

### 發展歷程
- 2維反軌跡程式由來已久，自張老師研究室時代即發展了變分分析風場與動力風場模式所推動的軌跡模式。張老師過世後，繼續發展成以[CODiS](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/)高密度觀測數據之反軌跡程式(2019/06)。
- 2019/11因發展逐日預報之calpuff系統，使用到中央氣象局的[WRF預報結果][get_M-A0064]。經穩定使用後，將其繼續加值轉成wrfout形式，也應用在mmif與aermod的模擬(2020.02)。
- 2020.08發展了自wrfout讀取3維風場的[反軌跡模式](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/traj3D/)，其網格套疊的概念也延續到2維軌跡之計算。
- [臺灣地區高解析度2維軌跡分析系統](http://125.229.149.182/traj2.html)最早開始(2021/01)先是發展產生的功能，分析過去個案，包括地面觀測與過去執行的wrfout，且將linux命令列的程式寫成html對話方式，而在畫面的右側，貼一個北、中、南測站反軌跡完成圖作為示意，讓使用者可以先預覽一下可能的結果。
- 其後(2021/06/23)發展電腦自動分析系統，預設反軌跡的時間、測站，並按照中央氣象局預報的天數，套用實際之風場，逐日由crontab自動執行，進行圖面的更換。
- 2022/04仿照疫情數據公開也使用github.io的平台，乃將在imac上的html自動分析的成果部分放在gitjub pages上，使用者自行產生部分仍然留在imac上。營運迄今。

### 重要選項考量與未來可能發展
- python或fortran的選擇
  - 早期張老師研究室的程式都是fortran撰寫，主要因為當時並沒有python的背景，而fortran也是為風場模式與光化模式所需要，軌跡模式為順便發展，所以就用了fortran。
  - 由於軌跡模式只有簡單的位置計算，並沒有太多浮點運算，因此似沒有必要再以fortran來撰寫。
- 2維或3維的選擇
  - 此處應用以測站周邊、高解析度、範圍以臺灣地區為主。需有強烈的因果關係解釋能力。
  - 如以3維風場在強力垂直混合的風場(山坡、都市加熱區)中，會造成滯留的錯覺，不利解釋。
  - 遠距離之長程傳輸，可以考慮使用3維風場，以避免高低風切造成的錯誤預估，且符合實際。
- 預報風場
  - 每天獨立執行數值預報並不是一件容易的作業。主要因為風場模式具有發散的可能，需要完整的邊界條件、地面及高空的強迫條件的預報。
  - 此處僅使用到地面風場、最多用到行星邊界層，其餘風場模式預報的物理量，在此並未使用到，這點也降低重新模擬的動機。
  - 使用wrfout格式有其方便性，可以彈性接受自行執行wrf或接收CWBWRF轉檔結果。
  - 由於GFS有10天的預報，以其結果做為wrf之邊界與FDDA數據，將可以得到10天高密度的地面風場，屆時不必修改主要軌跡程式，只需修改數據來源即可順利接收。
   
### 程式分段
  1. 接收[get_M-A0064.cs][get_M-A0064]之下載與轉檔結果。
  1. 執行[ftuv10.py][ftuv10]
  1. 執行[csv_to_geojson]()
  1. 執行[addVI.py]()
  1. git更新上傳

## 程式說明
### [get_M-A0064.cs][get_M-A0064]結果之接收
- 即使有舊檔(昨日、前日的預報結果)，也將其覆蓋。

```bash
#!/bin/bash
yesd=$(date -v-1d +%Y%m%d)
for i in 0 1 2 3;do
  ymd=$(date -v+${i}d -j -f "%Y%m%d" "${yesd}" +%Y%m%d)
  y=$(date -v+${i}d -j -f "%Y%m%d" "${yesd}" +%Y)
  ddd=$(date -v+${i}d -j -f "%Y%m%d" "${yesd}" +%Y-%m-%d)
  for d in 1 3;do
    fn=U10V10_d0${d}_${ddd}_06:00:00
#   if ! [ -e /Users/Data/cwb/e-service/btraj_WRFnests/CWB_forecast/$fn ];then
      cp /Users/Data/cwb/WRF_3Km/${y}/${ymd}/$fn /Users/Data/cwb/e-service/btraj_WRFnests/CWB_forecast/$fn
#   fi
  done
done
```

### 執行[ftuv10.py][ftuv10]


```bash
for d in $today $Tomorr $AftTmw;do
cd /Library/WebServer/Documents
for t in zhongshan zhongming jiayi qianjin;do
  $PY -t $t -d ${d}12 -b True
  fn=trj_results/btrj${t}${d}12_mark.csv
  rm -f trj_results/today_$t.csv
  if [ -e $fn ];then cp $fn trj_results/today_$t.csv;fi
done
done
```

[get_M-A0064]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/get_M-A0064/> "中央氣象局WRF_3Km數值預報產品之下載、空間內插與轉檔"
[ftuv10]: <> ""