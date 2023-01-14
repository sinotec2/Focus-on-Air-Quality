---
layout: default
title: calpuff遠端計算
nav_order: 5
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-06-11 19:58:12
tags: cpuff CGI_Pythons wrf-python graphics

---

# calpuff遠端計算系統之實現
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
- calpuff執行會需要地形、氣象、臭氧濃度與排放等前處理，雖然目前有[calwrf](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALMET/calwrf/)的轉接，可以減省很多整併的工作，但也僅限地形與氣象部分。其他項目還是得一一解決(詳[calpuff.inp](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/))。
- 因為calpuff程式並沒有平行計算的設計，執行會需要較長時間，這是遠端計算系統困難的地方。其他困難還包括：
  - 氣象檔非常龐大，該如何提供？
  - 結果檔案即使以[con2nc](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2nc/)處理成nc檔案，可以用VERDI開啟，依然不是馬上可以檢視結果。後處理還有待提升。

### [CPUFF721遠端計算服務](http://125.229.149.182/CALPUFF.html)
- 位置:[http://125.229.149.182/CALPUFF.html](http://125.229.149.182/CALPUFF.html)
- 畫面

| ![CALPUFF_remote.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_remote.PNG)|
|:-:|
| <b>CPUFF721執行進度網頁畫面</b>|

### 檔案系統架構
- HTML
  - $web/[CALPUFF.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/CALPUFF.html)
    - 使用[filepicker](https://github.com/benignware/jquery-filepicker)開啟使用者指定上傳的檔案
    - 開啟檔案(使用者提供的[calpuff.inp](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/calpuff.inp))
      - 使用者只能修改不涉及其他檔案的設定
      - 範例說明如後。
    - 呼叫CGI-PY：CALPUFF.py或demo.py
  - $web/cpuff_results/demo/[autorefreash.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/autorefresh.html)：每10秒報告cpuff、或m3nc2gif.py的執行進度、連結到工作站整體模式運作情況網頁[status.html](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/HTML/status/)
  - $web/cpuff_results/demo/[done.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/done.html)：執行停止的結果畫面
  - $web/cpuff_results/demo/[cpuff_gifs.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/cpuff_gifs.html)：模擬結果之gif檔案，以[LC-GIF-Player](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/HTML/gif_player/#html播放器方案)進行播放。

- CGI-PY
  - $cgi/calpuff/[CALPUFF.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/calpuff.py)：啟動cpuff主程式、啟動監看程式waitc.cs
  - $cgi/calpuff/[demo.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/demo.py)：檢視$web/cpuff_results/demo目錄下之文件。
  - CGI-PY設計說明詳見[CALPUFF.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/CALPUFF/)
- EXE
  - calpuff主程式：`CPUFF='/Users/cpuff/src/CALPUFF_v7.2.1_L150618/cpuff721 &> /dev/null 2>&1'`
  - 監看程式：`WAITC=WEB+'/cpuff_results/waitc.cs'`。cpuff執行完之後會接續執行：
    - [calpuff.con轉nc檔案](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2nc/)：`/Users/cpuff/src/CALPOST_v7.1.0_L141010/con2nc >& con2nc.out`
    - [將nc檔案讀出寫成gif檔案](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python/4.m3nc2gif)：`../demo/m3nc2gif.py cpuff.nc >& con2nc.out`
- INP
  - $web/cpuff_results/[calpuff.inp](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/calpuff.inp)
  - $web/cpuff_results/demo/[calpost.inp](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/calpost.inp)
  - $web/cpuff_results/demo/[wrfout_d04](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/wrfout_d04)(4.3M)：為[m3nc2gif.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python/4.m3nc2gif)所需要檔案。

### CALPUFF.INP 目前開放功能
- 常數之排放源相關設定、位置、排放量、排放條件
  - [INPUT GROUPS: 13 – Point source parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-groups-13--point-source-parameters)
  - [INPUT GROUPS: 14 – Area source parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-groups-14--area-source-parameters)
  - [INPUT GROUPS: 15 – Line source parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-groups-15--line-source-parameters)
  - [INPUT GROUPS: 16 – Volume source parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-groups-16--volume-source-parameters)
- 化學相關設定
  - [INPUT GROUP: 3 – Species list](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-group-3--species-list)
  - [INPUT GROUP: 11 – Chemistry Parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-group-11--chemistry-parameters)
- [INPUT GROUP: 12 – Misc. Dispersion and Computational Parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-group-12--misc-dispersion-and-computational-parameters)
### 座標系統說明
- 座標原點：（23.61N，120.99E）、[TWD97](http://ts01.gi-tech.com.tw/waterAbnormal/trancoor/trancoor.aspx?WGS84_E=121&WGS84_N=24&TWD97_X=&TWD97_Y2)（248979.464031498，2610725.45369074）
- 輸入單位為公里
- 詳細設定詳 [INPUT GROUP: 4 – Map Projection and Grid control parameters](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/#input-group-4--map-projection-and-grid-control-parameters)

## 監看程式$web/cpuff_results/[waitc.cs](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/waitc.cs)
### 執行方式
- 2個引數
  - 1.CGI-PY 給定的亂數目錄cpuf_**RAND**，**RAND**為6碼亂數文字
  - 2.PID cpuff程式的執行緒號
### 迴圈控制
- 每10秒檢查一次
- 判斷標準：PID是否仍然在執行中
  - 是：輸出執行進度之文字到檔案cpuff.out。prog.html會每10秒鐘重讀這個檔案。
  - 否：跳脫迴圈，執行calpuff後處理

```bash
#$1=pth
#$2=pid
LST=$1/CALPUFF.LST
OUT=$1/cpuff.out
touch $OUT
for ((i=0; i>=0;i+=1));do
  if [ -e $LST ];then 
    grep CONCENTRATIONS CALPUFF.LST |tail -n1 > $OUT
  else
    echo 'cpuff (pid='$2') has been executed for '${i}'0 seconds' >> $OUT
  fi
  now=$(ps -ef|grep cpuff721|grep $2 |grep -v grep|wc -l)  
  echo 'cpuff (pid='$2') has been executed for '${i}'0 seconds' >> $OUT
  all=$(ps -ef|grep cpuff721 |grep -v grep|wc -l)  
  echo 'All '${all}' cpuffs are executing' >> $OUT
  if [ $now != 1 ]; then break;fi
  sleep 10 
done
```
### calpuff 後處理
1. [calpuff.con轉nc檔案](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2nc/)
  - 需要正確路徑的python 
2. [將nc檔案讀出寫成gif檔案](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python/4.m3nc2gif)，略作調整：
  - 減少檔名的長度（控制在10碼以下）
  - 將nc檔內變數的單位予以更正
  - 複製一份GIF的播放器([LC-GIF-Player](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/HTML/gif_player/#html播放器方案))，將GIF結果移到正確的位置。

```bash
cd $1
cp ../demo/calpost.inp .
export PATH=/opt/anaconda3/envs/pyn_env/bin:$PATH
/Users/cpuff/src/CALPOST_v7.1.0_L141010/con2nc >& con2nc.out
ln -sf calpuff.con.S.grd02.nc cpuff.nc
/opt/local/bin/ncatted -a units,SO2,o,c,'ppbV'  -a units,NO2,o,c,'ppbV'  -a units,PM10,o,c,'ug/m3' -a units,SO4,o,c,'ug/m3' cpuff.nc
../demo/m3nc2gif.py cpuff.nc >& con2nc.out
cp -r /Library/WebServer/Documents/LC-GIF-Player/* .
mv *.gif example_gifs
```
### 產生結束網頁
- 複製一個模版
- 更換PID、目錄位置以及檔案大小

```bash
cp ../demo/done.html prog.html
sed -ie 's/PID/'$2'/g' prog.html 
rand=$(echo $1|cut -d'_' -f3)
sed -ie 's/RAND/'$rand'/g'  prog.html
mb=$(ls -lh calpuff.con.S.grd02.nc|awk '{print $5}')
sed -ie 's/MB/'$mb'/g' prog.html
```

## 結果畫面與連結

### 檔案連結

```
pid= 77547(check progress)
Model_results:
calmet.dat
calpuff.con.S.grd02.nc
calpuff.inp
cpuff.out
```
### 程式進度畫面

| ![CALPUFF_prog.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CALPUFF_prog.PNG)|
|:-:|
| <b>CPUFF721執行進度網頁畫面</b>|

| ![CALPUFF_nc.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_nc.PNG)|
|:-:|
| <b>CPUFF721最終進度網頁畫面</b>|

### [cpuff_gifs.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/cpuff_gifs.html)


| ![cpuff_gifs.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/cpuff_gifs.png)|
|:-:|
| <b>CPUFF721最終進度網頁畫面</b>|


## 後續發展
- 氣象個案的準備與選擇
- 沉降量之轉檔
- HRA物質的擴散及沉降