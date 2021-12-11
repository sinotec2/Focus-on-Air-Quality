---
layout: default
title: "MOZART"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 1
date:               
last_modified_date:   2021-12-11 22:21:03
---

# MOZART模式結果之讀取及應用
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

## 前言
- MOZART模式全名為臭氧及相關化學成分模式(Model for OZone and Related chemical Tracers)。
- MOZART模式為NCAR、NOAA轄下 Geophysical Fluid Dynamics Laboratory (GFDL)與德國漢堡大學 Max Planck Institute for Meteorology (MPI-Met)多年來合作發展應用的全球3維大氣化學成分模式，除了應用在對流層之外，平流層及中氣層範圍亦涵括在內。 
  - 氣象場部分，MOZART可以接受包括NWS的NCEP (National Centers for Environmental Prediction)、歐洲的ECMWF(European Centre for Medium-Range Weather Forecasts)、NASA GMAO(Global Modeling and Assimilation Office ) 的GCM等模式輸出。
  - 其空品模擬結果多年來也用在WRF-CHEM模式的邊界與初始條件。
- MOZART數值產品過去也經常應用在地區模擬之邊界與初始條件，詳如下述。

### MOZART結果之解析度
- MOZART 的水平空間解析度視不同機器平台略有差異，一般而言介於2.5~2.8度之間，
- 高度為Non_Hydrostatic SIGMA-P座標從最底層(1000HPa到模式頂層0) 有57層，
- 檔案儲存的時間解析度則為6小時。(UTC0/6/12/18)
- 化學機制方面
  - 標準的MOZART-4有85個氣態污染物，12個氣膠成分，39條光化反應以及157條氣態反應，
  - 碳鍵機制採lump法，VOCs包括3個烯烴與烷烴類物質，以及4個碳以上與芳香烴類物質(BIGALK, BIGENE及TOLUENE)。

### MOZART模擬結果之下載
MOZART針對空氣品質模式使用者設有提供資料之網站(http://www.acom.ucar.edu/wrf-chem/mozart.shtml ) ，給定內容：
1. 基本資料。用做通訊用。
1. 模擬範圍大致的座標 
如下列ncdump內容南北-2~47度、東西80~160度，須涵蓋氣象檔東亞d1範圍)，每個檔案「必須」有相同的範圍，以便進行檔案的合併
1. 指定之年月日(每日以0600UTC開始以隔日0000UTC結束共4筆間隔6小時)，即會將下載連結寄到指定電子郵件地址，另行以wget或其他方式下載檔案。 日數擷取策略： 
- 5個檔案方案： 
  - 前月最後10~11天、本月3個檔、下個月1~10日檔案沒有重疊，ncrcat可以自由搭配這是因為mozart結果檔案儲存是以當天0600UTC當啟始，以隔天0000UTZ為結束，與一般定義有別，因此在整併全月資料時會出現缺漏。
- 3個檔案方案 ： 
  - 較前述前後略為增加一些，以使跨月計算可以順利進行。如
    - 2016123106~2017011100(前一年的最後一天6:00開始~1/10結束在1/11/0:00)、
    - 2017011106~2017012100、2017012106~2017020200(下個月第一天)... 。
  - file1:  2016_12_31 ~ 2017_01_10
  - file2:  2017_01_11 ~ 2017_01_20file3:  2017_01_21 ~ 2017_02_01
    - 注意：選單順序：因為日的選單比較難選(有31日)，建議按照file1(每一月)→file2(每一月) →file3進行(每一月)，以加快速度。
    - file1要注意大、小月注意潤年檔案會重疊，只能針對同一月份進行ncrcat這樣做法雖然前後檔案會大一些，日期也不具規律性，但在後續處理時3個檔案合併總是比較小，可以減省讀取的時間。

## 程式說明

## 程式之執行
- 依月份呼叫即可
- machine-dependancy
  - 如要改寫成`uamiv`檔案，系統必須要有`pncgen`程式
  - 因pandas及no.tensordot會自己啟動多工運作，同時執行3個月份node01~03尚能消化(CPU~4500%)，如太多月份同時運作，系統資源將會耗盡。不但拖慢速度，結果也不正確

```bash
for m in {01..04};do sub python area_YYMM.py 19$m >&/dev/null;done
for m in {05..08};do sub python area_YYMM.py 19$m >&/dev/null;done
for m in {09..12};do sub python area_YYMM.py 19$m >&/dev/null;done
```
  
## 檔案下載
- `python`程式：[area_YYMMinc.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/area_YYMMinc.py)。

## Reference
