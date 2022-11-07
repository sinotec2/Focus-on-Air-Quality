---
layout: default
title: 三維軌跡分析
nav_order: 1
parent: btraj_WRFnests
grand_parent: Trajectory Models
last_modified_date: 2022-03-31 15:20:02
---

# WRF三維軌跡分析
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

## WRFOUT三維軌跡主程式
### wrfout檔案之彙整、連結
- 由於所需歷年來之wrfout，可能分散在不同目錄、磁碟機檔案系統、需要先做好連結。['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]：各層wrfout檔案(連結)
- 時間規格：每天一個檔，檔案為逐時，自UTC 0時開始，結束於隔天0時。
- wrf版本：不限、不檢查

### bt2_DVP.py
- 3維軌跡程式參考2維程式進行增修，2維(CWB觀測值內插)軌跡程式公開於[github](https://github.com/sinotec2/rd_cwbDay/blob/master/traj2kml.py)
- arguments:
  - \-t daliao (測站名稱)
  - \-d 20171231 (軌跡起始的年月日時)
  - \-b T (是否為反軌跡 T/F)
- 輸入檔
  - sta_list.json：測站編號名稱
  - path+'sta_ll.csv：測站經緯度
  - ['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]：各層wrfout檔案(連結)
- 輸出檔：'trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
- 軌跡點時間間距：15S
- 程式內掛後處理(不執行不影響主要結果)
  - [csv2kml.py][csv2kml]：繪製google map
  - [csv2bln.cs](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/traj/#csv2bln)：bln file is used for surfer plotting

### download bt2.py

- {% include download.html content="三維軌跡模式（超微工作站版本）[bt2_DVP.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/bt2_DVP.py)" %}

### do_bt1.cs 動態執行批次檔
- 每（小時，測站）反軌跡線的計算彼此之間是互相獨立的作業，不會彼此干擾、彼此需要，因此非常適合平行運作。可以在OS層次就可以控制。
- 控制邏輯：
  - 不止盡的`while true`迴圈。
    - 設定當運轉中核心數低於下限（如工作站總核心數的9成）時執行下一條軌跡線、並且挑脫迴圈。
    - 核心數高於下限值時，休息5秒。5秒後取得執行核心之個數。
- [bt2.py][bt2]引數
  1. $1=station name
  2. $2=month(2 digits)
  3. $3=day

```bash
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat do_bt1.cs
#do_bt1 station mm dd
st=$1
for y1 in {16..16};do
y=20$y1
#for m in {02..03};do
m=$2
ym=$y1$m
#for d in {01..31};do
d=$3
  h=00
  if ! [ -e links/wrfout_d04_${y}-${m}-${d}_${h}:00:00 ];then continue;fi
  for h in {00..23};do
    if [ -e trj_results${ym}/trj${st}${y}${m}${d}${h}.csv ];then continue;fi
    n=$(psg bt2.py|wc -l)
    while true;do
      if [ $n -lt 90 ];then
        touch trj_results${ym}/trj${st}${y}${m}${d}${h}.csv
        sub python bt2.py -t $st -d ${y}${m}${d}${h} -b True >& dum
        sleep 5s
        break
      else
        sleep 5s
        n=$(psg bt2.py|wc -l)
      fi
    done
  done
#done
#done
done
```

## 叢集分析
### choose10 .py(前處理)
- 從前述[bt2.py](#bt2_DVP_py)所得之軌跡點L.csv檔案，選取其中10個點，將20個維度之矩陣進行k_means分析
- 輸入檔案：
  - tmplateD1_3km.nc：讀取網格設定，以簡化軌跡點
  - fnames.txt(檔案路徑名稱之listing)
- 輸出檔案：
  - *10.csv

## km.py
- 這支程式讀取choose10.py結果，以K-means方式取其代表性叢集。

### 程式IO
- arguments:
  - *10.csv檔案路徑名稱之文字檔
  - nclt: number of clusters
- 輸入檔
  - *10.csv：choose10.py的結果
  - tmplateD1_3km.nc：由JI轉換成網格化座標位置
- 輸出檔
  - lab.csv：逐時的叢集編號
  - 'res'+str(l)+'.csv' ：各叢集的代表性軌跡
- 內掛後處理（[csv2kml.py][csv2kml]）：
  - 由csv產生kml檔案
  - 可以google map、leaflet套件等等進行繪圖

### download km.py

- {% include download.html content="三維軌跡線之k-means叢集分析程式：[km.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/km.py)" %}

## google map繪圖、軌跡命名
- 由於叢集分析結果為數字，需建立名稱對照表，以便在繪圖時(google map上軌跡點之說明內容、參考筆記繪製逆軌跡圖流程[csv2kml][csv2kml])顯示結果。
- 定義數字與文字(區域方向)之對照(path.txt)如下。

```bash
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests/kmean_spr
$ cat n_clusters6/path.txt
1SH     5 Shang Hai and northwestern China
2BJ     3 Bei Jing
3SW     1 South Western of stations
4LOCAL  2 Local Circulations
6BH     0 Bo Hai
7SC     4 Southern China
```

## 其他後處理
### acc_prob.py
- 從軌跡點L.csv檔案，統計網格通過機率，以便進行繪圖
- 輸入檔案：
  - fnames.txt(檔案路徑名稱之listing)
- 輸出檔案：
  - probJ.nc
  - 單位：crossing time/total time

- {% include download.html content="三維軌跡線之網格通過機率分析程式：[acc_prob.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/acc_prob.py)" %}

[csv2kml]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/> "點狀資訊KML檔之撰寫(csv2kml.py)"
[bt2]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests#bt2_dvppy> "3維軌跡程式"