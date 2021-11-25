---
layout: default
title: "中央氣象局日報表下載及轉檔"
parent: "氣象模式"
nav_order: 1
date:               
last_modified_date:   2021-11-25 17:13:11
---

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

# 中央氣象局日報表下載及轉檔 

## 背景
中央氣象局數據每天公開其自動站觀測結果在[CODiS](https://e-service.cwb.gov.tw/HistoryDataQuery/)網站，其數據過去曾應用在風場的產生、軌跡之追蹤等等作業化系統。
此處介紹台灣地區中央氣象局自動站數據之內容、下載作業方式、以及轉成MM5/WRF之[little_r](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式，以備應用在WRF模式的4階同化模擬。
- 更新頻率時間：每日12(L)時更新，更新至前一日24時。
- 日報(總)表之內容
  - 以每站報表格式
  - 格式：為csv格式
  - 表頭：包括站名、觀測時間、氣壓、海面氣壓、溫度、濕球溫度、相對濕度、風速、風向、陣風等數據，其中風速風向即用以計算軌跡線所需。
- 檔案範例
```
stno_name,ObsTime,StnPres,SeaPres,Temperature,Td dew point,RH,WS,WD,WSGust,WDGust,Precp,PrecpHour,SunShine,GloblRad,Visb,UVI,Cloud Amount
466880_板橋,2020061901.0,1006.1,1007.3,27.7,24.6,83.0,1.1,200.0,3.0,190.0,0.0,0.0,,0.00,,,
466880_板橋,2020061902.0,1006.0,1007.2,27.6,24.9,85.0,1.1,210.0,3.3,190.0,0.0,0.0,,0.00,20.0,,2.0
466880_板橋,2020061903.0,1006.2,1007.4,26.9,24.6,87.0,1.4,200.0,3.8,190.0,0.0,0.0,,0.00,,,
466880_板橋,2020061904.0,1006.3,1007.5,26.8,24.5,87.0,0.8,210.0,2.2,180.0,0.0,0.0,,0.00,,,
466880_板橋,2020061905.0,1006.2,1007.4,26.7,24.3,87.0,0.6,210.0,2.8,210.0,0.0,0.0,,0.00,20.0,,4.0
466880_板橋,2020061906.0,1006.6,1007.8,26.9,23.3,81.0,1.0,190.0,2.9,240.0,0.0,0.0,0.2,0.06,,,
466880_板橋,2020061907.0,1007.0,1008.2,29.7,22.4,65.0,2.1,200.0,4.8,190.0,0.0,0.0,1.0,0.73,,,
466880_板橋,2020061908.0,1007.2,1008.4,30.6,21.4,58.0,2.8,230.0,7.2,210.0,0.0,0.0,1.0,1.11,30.0,,8.0
466880_板橋,2020061909.0,1007.2,1008.4,31.6,21.5,55.0,3.1,220.0,7.5,200.0,0.0,0.0,1.0,1.32,30.0,,8.0
...
```

## 爬蟲程式
- 原始碼公開於[github](https://github.com/sinotec2/rd_cwbDay/blob/master/rd_cwbDay.py)
- 需要外部檔案[stats_tab.csv]()為測站位置座標等內容輸出檔案


## Reference

- disscusion on **About Convert csv data file format to little_r format** [WRF & MPAS-A Support Forum](https://forum.mmm.ucar.edu/phpBB3/viewtopic.php?t=483), Mon Dec 03, 2018 6:23 am.
- University of Waterloo, [WRF Tutorial](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial),  27 June 2019, at 14:53.
- Andre R. Erler, WRF-Tools/Python/wrfrun/[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py), Commits on Nov 23, 2021.
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)

