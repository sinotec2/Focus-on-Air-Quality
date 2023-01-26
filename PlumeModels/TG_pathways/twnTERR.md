---
layout: default
title: 全臺AERMAP之執行
parent: RE & TG Pathways
grand_parent: Plume Models
nav_order: 3
last_modified_date: 2022-03-14 16:04:28
tags: CGI_Pythons plume_model
---
# 全臺點源AERMAP之執行
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
- 為快速累積複雜地形中煙流模式的執行經驗，建立相應之執行規範，此處針對TEDS中所有點源進行AERMAP之模式模擬。
- 使用之程式即為前述[AERMAP之遠端執行](../../utilities/CGI-pythons/aermap_caas.md)之python程式，應用SuperMicron工作站，以bash腳本控制同步計算。
- 計算結果檔案
  - 以uMap提供[鏈結](http://umap.openstreetmap.fr/zh/map/taiwan-aermap_11-points_730878#7/23.671/121.084)下載。
  - 有關uMap的使用方法，可以詳見[鏈結資訊之地圖展現(uMap)](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/UMAP/)

## 整體執行與同步控制
- 此次作業的特性為多個aermap同時進行，雖然aermap程式並沒有多工性質，然而經由bash腳本可以控制同時運作的aermap作業數，在工作站總核心數上限之下。範例如下
- 類似作業方式亦可以應用在任何沒有多工性質的執行檔

```bash
AMAP=aermap
TERR=/nas1/aermruns/terrByC_NO/terrainTXT2.py
python wr_inptxt.py
while read STR; do
  n=$(psg $AMAP|wc -l)
  while true;do
    if [ $n -lt 90 ];then
      echo "${STR}">inp.txt
      sub $TERR
      sleep 1s
      break
    else
      sleep 1s
      n=$(psg $AMAP|wc -l)
    fi
  done
done < a.txt
```
- 詳見[sub](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/unix_tools/#sub)及[psg](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/unix_tools/#psg)OS之小工具內容

### 逐行提供引數的方式
- 由於bash腳本內的環境變數，以命令列伺入python程式時無法正確傳遞其內容(含空格)，必須尋求其他方式。
- while read ... done <a.txt 
  - 將a.txt逐行內容利用echo另存成文字檔(固定檔名)inp.txt，由python進行讀取，取代由命令列直接讀入。
  - 可參考 [How to read file line by line in Bash script](https://linuxhint.com/read_file_line_by_line_bash/)
  - 雖然此處仍為循序執行方式，在腳本中特別設定2次前後python中間停等1秒，可以確保不會造成多個python讀取同一文字檔的問題。

### 同步執行的控制方式
- 以`ps -ef|grep aermap|wc -l`($n值)結果來控制
  - 此值如果小於90(工作站核心數)，則開始一項新的aermap作業，結果此次循環(跳到下個aermap作業之準備)。
  - 如果大或等於90，則休息1秒、再執行ps指令，再行檢視

### 記憶體之控管
- 因為aermap作業的記憶體大小差異甚巨、不一而足，但即使同時執行90項作業，尚在工作站能力允許，因此不另行管控。

### 結果之管理
- 除以批次腳本[WAITM='/nas1/aermruns/terr_results/wait_map.cs']()進行時間管控之外，
- 在python程式內自行開設目錄單獨存放aermap的輸入、輸入檔案、後處理結果等等
- 各個aermap作業結果目錄與設定方式，另存在TWN_1X1REC.csv檔案內，其表頭如下：

```bash
kuang@master /nas1/aermruns/terrByC_NO
$ head TWN_1X1REC.csv
pathIJ,centIJ,dx,dy,inp,nx,ny,path,x0,y0
190364,190364,1250,1250,290700_40_1250_2746400_40_1250,40,40,xieh1xie,290700,2746400
158346,158346,728,728,268900_40_728_2738900_40_728,40,40,shulinIn,268900,2738900
180237,180237,321,321,299300_40_321_2638100_40_321,40,40,paper1pa,299300,2638100
180352,180352,439,439,296300_40_439_2750300_40_439,40,40,muzhaInc,296300,2750300
66258,66258,1062,1062,169700_40_1062_2643800_40_1062,40,40,twsteel,169700,2643800
69080,69080,1384,1384,165500_40_1384_2458500_40_1384,40,40,kandingI,165500,2458500
199279,199279,100,100,322350_50_100_2684250_50_100,50,50,hep1hp2,322350,2684250
160349,160349,240,240,281100_40_240_2751100_40_240,40,40,shulinIn,281100,2751100
68110,68110,60,60,191120_50_60_2514370_50_60,50,50,S2100741P004,191120,2514370
...
85266,85266,40,40,208860_50_40_2672640_50_40,50,50,B23B1135P101,208860,2672640
48142,48142,20,20,171880_50_20_2547780_50_20,50,50,R14A1497P201,171880,2547780
```
- 各欄數據分別為
  - pathIJ,centIJ：在TWN_3X3(d04)網格系統中的i,j值。  
  - dx,dy：aermap接受點之格距(m)
  - inp：接受點XYINC文字串
  - nx,ny：aermap接受點之格數
  - path：點源名稱
  - x0,y0：西南角TWD97座標值
- 等候所有aermap作業全部完成，另行產生kml檔，以將鏈結位置上載到uMap以供查詢下載。

## KML之輸出
- 為利結果之空間檢索，需將aermap作業之輸入、輸出與後處理成果（**作業包下載點鏈結網址**），賦予經緯度座標，貼在地圖上。
- 此處先將前述結果寫成csv檔案，再使用[csv2kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/#點狀資訊kml檔之撰寫csv2kmlpy)將其寫成kml檔案。
- 除了點狀資訊外，為使aermap模擬範圍可以呈現在圖面上，另外產生以點源為中心、模擬範圍的多邊形KML檔，貼在uMap圖層，方便快速掌握資料檔案的範圍。

### mk_kml.py
#### 按照模擬範圍邊長反向排序的用意：
- 面積大的作業先出現在uMap圖面，會形成底圖，較容易點選其後（範圍較小）的其他作業。
- 如果面積大的作業在uMap圖面的上層，則會遮蔽較小的結果，致無法點選。

#### terrTWN_1X1.csv之產生與後處理
- 讓df.desc的內容就是該點aermap作業結果的網址鏈結，這樣在uMap上點選有興趣的點，則會出現該點源周邊aermap**作業包**的下載點。
- 產出後隨即呼叫[csv2kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/#點狀資訊kml檔之撰寫csv2kmlpy)
  - 檔案選項-f後輸入csv檔名
  - 點狀選項-n，不論選N/H/R/B/D都會一樣，因為這些差異只在Google Map上有作用。uMap上的形狀顏色是另外設定的，不跟著KML內容走。

#### 陪襯4邊形的產生與輸出
- 以模擬範圍（RE XYINC格式順序）的西南角座標開始，畫出模擬範圍的四邊形，輸出格點座標成為csv檔案
- 多邊形在uMap中可以選擇顏色、填滿與否、線條粗細、透明度等等。
- 呼叫[csv2kml.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/#點狀資訊kml檔之撰寫csv2kmlpy):
  -n 選項選擇**P**，輸出多邊形之KML。

| ![twnTERR.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/twnTERR.png)|
|:--:|
| <b>uMap結果範例</b>|

### 程式碼
- [github/sinotec2](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/REnTG_pathwaysways/mk_kml.py)


## Reference

[token4]: <http://umap.openstreetmap.fr/zh/map/anonymous-edit/730878:5iVuLBTmsNc5G3KzIN90KKRkbfM> "http://umap.openstreetmap.fr/zh/map/anonymous-edit/730878:5iVuLBTmsNc5G3KzIN90KKRkbfM"