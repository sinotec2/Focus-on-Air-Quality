---
layout: default
title: daily_traj.cs
nav_order: 3
parent: 地面二維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-04 14:43:02
tags: trajectory CWBWRF CODiS geojson
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

- 這支[程式(腳本)][daily_traj]每天凌晨進行北中南測站反軌跡的計算，並將結果更新到[GitHub Pages](https://sinotec2.github.io/traj/)網頁畫面。

### 發展歷程

- 2維反軌跡程式由來已久，自張老師研究室時代即發展了變分分析風場與動力風場模式所推動的軌跡模式。張老師過世後，繼續發展成以[CODiS](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/)高密度觀測數據之反軌跡程式(2019/06)。
- 2019/11因發展逐日預報之calpuff系統，使用到中央氣象局的[WRF預報結果][get_M-A0064]。經穩定使用後，將其繼續加值轉成wrfout形式，也應用在mmif與aermod的模擬(2020.02)。
- 2020.08發展了自wrfout讀取3維風場的[反軌跡模式](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/traj3D/)，其網格套疊的概念也延續到2維軌跡之計算。
- [臺灣地區高解析度2維軌跡分析系統](http://125.229.149.182/traj2.html)最早開始(2021/01)先是發展產生的功能，分析過去個案，包括地面觀測與過去執行的wrfout，且將linux命令列的程式寫成html對話方式，而在畫面的右側，貼一個北、中、南測站反軌跡完成圖作為示意，讓使用者可以先預覽一下可能的結果。(詳見[	surf_trajLL2][1]及[^1])
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
- 程式執行者的設定
  - 在2022/04之前，網頁是直接設在imac的httpd服務範圍，為避免遭到駭客的修改、讀取等等不當行為攻擊，會將$web目錄的所有人設成root，限制其他人的讀取。
  - 因此每日程式的讀取、計算及儲存，必須由root執行。
  - 這項設定雖然也讓程式、腳本等等的修改增加不少困擾，但似乎也沒有更好的方式可選擇。
   
### [daily_traj.cs][daily_traj]程式分段重點

  1. 接收[get_M-A0064.cs][get_M-A0064]之下載與轉檔結果。
  1. 執行軌跡模式[ftuv10.py][ftuv10]
  1. 執行檔案轉換[csv_to_geojson][cj]
  1. 執行通風指數程式[addVI.py][VI]
  1. [git][git]更新上傳

## 程式說明

### [get_M-A0064.cs][get_M-A0064]結果之接收

- 即使有舊檔(昨日、前日的預報結果)，也將其覆蓋。
- 此處為macOS版本之`date`指令

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

- 4個空品測站：北部(中山站)、中部(忠明站)、南部(嘉義及前金站)
- 時間：今日、明日、後日之中午12時
  - 每天的today_*.csv經處理後會儲存在對應之目錄下

```bash
for d in $today $Tomorr $AftTmw;do
cd /Library/WebServer/Documents
for t in zhongshan zhongming jiayi qianjin;do
  $PY -t $t -d ${d}12 -b True
  fn=trj_results/btrj${t}${d}12_mark.csv
  rm -f trj_results/today_$t.csv
  if [ -e $fn ];then cp $fn trj_results/today_$t.csv;fi
done
...
test $d == $today && dir=00
test $d == $Tomorr && dir=p1
test $d == $AftTmw && dir=p2
cat header.txt today.csv > $dir/today_marks.csv
done
```

### 執行[csv_to_geojson][cj]

- csv_to_geojson是網友[miquel-vv][cj]提供的套件，可以將csv檔案中的經緯度位置，轉成[geojson檔案格式][geojson]的線格式，以順利讓leaflet地圖可以讀取。

```bash
CJ=/opt/anaconda3/bin/csv_to_geojson
...
#geojson for leaflet-ajax
cat headLL2.txt today.csv > today${today}12.csv
$CJ today${today}12.csv
```

### 執行[addVI.py][VI]

- [通風指數(Ventilation Index, VI)](https://www2.gov.bc.ca/gov/content/environment/air-land-water/air/air-pollution/smoke-burning/ventilation-index#:~:text=The%20Ventilation%20Index%20is%20a,will%20mix%20into%20the%20air.)：系指一個地區的平均風速、與其混合層高度之乘積。
  - 一般用在與空氣污染有關的行為管制，VI值多少時，不能從事特定的污染行為。
  - 也是一項重要的預報參數。
- 此處將軌跡線上的地面風速與行星邊界層高度相乘後，列在csv中，在繪圖時可以引用。
- 程式內自行呼叫$CJ，不另行呼叫。

```bash
VI=/Users/kuang/bin/addVI.py
...
for dir in 00 m1 m2 p1 p2;do
  cd $dir
  $VI today_marks.csv
  cd ..
done
```

### git更新上傳

- git過程會需要有一致的檔案屬性。如前所示，程式是root在執行，因此複製到repo目錄下的檔案會需要改變其屬性或所有權人。
- 每天更新軌跡線之後，還會有8：00更新的calpuff預報結果（from DEVP），因此會需要在imac複製更新部份(`git pull`)
- 其餘運作方式按照一般git的作業：add、commit、push 

```bash
cd /Users/kuang/GitHub/sinotec2.github.io/traj/trj_results
for i in 00 m1 m2 p1 p2;do cp -r /Library/WebServer/Documents/trj_results/$i .;done
chmod -R o+r ??
cd /Users/kuang/GitHub/sinotec2.github.io
su kuang
GT=/usr/local/bin/git
$GT pull origin main
$GT add traj
$GT commit -m "update traj"
TOKEN=$(cat /Users/kuang/bin/git.token)
$GT push https://sinotec2:$TOKEN@github.com/sinotec2/sinotec2.github.io.git main
```

### 自動執行

```bash
## trajectories update
#MIN HOUR DOM MON DOW CMD
0    4    *   *   *   /Library/WebServer/Documents/trj_results/daily_traj.cs >& /Library/WebServer/Documents/trj_results/daily_traj.out
```

## 程式下載

- {% include download.html content="軌跡線上通風指數之計算[daily_traj.cs][daily_traj]" %}


[get_M-A0064]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/1.get_M-A0064/> "中央氣象局WRF_3Km數值預報產品之下載、空間內插與轉檔"
[ftuv10]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/ftuv10/ftuv10/> "ftuv10.py程式說明"
[cj]: <https://github.com/miquel-vv/csv-to-geojson> "Takes a csv which contains at least the columns named 'lat' and 'lng', and converts it to geojson points. The additional columns are passed as attributes of the points."
[geojson]: <https://zh.wikipedia.org/wiki/GeoJSON> "GeoJSON是一種基於JSON的地理空間數據交換格式，它定義了幾種類型JSON對象以及它們組合在一起的方法，以表示有關地理要素、屬性和它們的空間範圍的數據。2015年，網際網路工程任務組（IETF）與原始規範作者組建了一個GeoJSON工作組，一起規範GeoJSON標準。在2016年8月，推出了最新的GeoJSON數據格式標準規範(RFC 7946)。GeoJSON使用唯一地理坐標參考系統WGS1984和十進位度單位，一個GeoJSON對象可以是Geometry, Feature或者FeatureCollection.其幾何對象包括有點（表示地理位置）、線（表示街道、公路、邊界）、多邊形（表示國家、省、領土），以及由以上類型組合成的複合幾何圖形。TopoJSON基於GeoJSON作了擴展，使得文件更小。"
[VI]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/ftuv10/addVI/> "addVI.py程式說明"
[git]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/git/#git-and-github> "Utilities -> Operation System -> git and github"
[daily_traj]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/ftuv10/daily_traj_csMac.txt> "MacOS版本每日執行3日軌跡預報之腳本程式"
[1]: https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/surf_trajLL2/ "臺灣地區高解析度軌跡產生/自動分析系統cgi程式"

[^1]:  臺灣地區高解析度軌跡產生/自動分析系統cgi程式，(外部參照[FAQ][1]、內部參考點[[surf_trajLL2.md]])