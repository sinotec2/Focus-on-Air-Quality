---
layout: default
title: 增量濃度分析程序與檢討
parent: Post Processing
grand_parent: CMAQ Model System
nav_order: 5
last_modified_date: 2022-06-21 15:16:03
---

# 增量濃度分析程序與檢討
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

## 前言/背景
- 計算不同排放情境模擬結果的濃度差異，是執行空品模式常見的作業。如CMAQ這樣有nc檔案輸出的模式，以[dNC][dNC]就可以簡單解決。但因為CMAQ的粒狀物定義同時有i,j,k濃度與其重量比例等2個場同時介入，因此造成非常高度之非線性結果。
- 由於目前還沒有找到CMAQ用在電廠個案計畫PM<sub>2.5</sub>/PM<sub>10</sub>增量比例的期刊文章，整體計算方式值得詳細討論。

### 傳統作法
- 由於CCTM_ACONC檔案的化學物質多達200餘種，需先進行整併才方便進行相減，因此大多數處理流程會先進行個案模擬的[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/),再進行增量的計算。

### 結果

1. 在看似非關連之區域出現微幅的濃度擾動。如圖1在某一時間之山區、西南海域出現增量、而在海面則出現負值之增量(空白處為無法取log值之負值增量區域)。
2. PM2.5增量高於PM10的增量(圖2)，圖中只顯示負值部分。顯示電廠為起點之煙流範圍有負值之最大值，約與上圖NO3負值增量濃度分布相同。
3. 營運前後粗細粒比例(CCTM_APMDIAG檔)具有差異性，如圖3a以營運前為1.0，營運後[PM25AC][PM25AC]月均值的增加幅度，圖3b則為PM10AC的增加幅度。因電廠運轉造成煙流範圍細粒比例增加約1%，洽與上2圖NO3負值增量及PM<sub>2.5</sub>與PM<sub>10</sub>增量之差值負值分布相同


[dNC]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/dNC/> "2個nc檔案間的差值"
[PM25AC]: <https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/#粒狀物之定義> "Aitken mode濃度在PM2.5部分之重量比例，詳見CMAQ綜合空品項目之計算(combine)->粒狀物之定義->PM2.5的定義"
[PM10AC]: <https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/#粒狀物之定義> "Aitken mode濃度在PM10部分之重量比例，詳見CMAQ綜合空品項目之計算(combine)->粒狀物之定義->PM10的定義"

| ![圖1a-N3G_NO3.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_NO3.png){:width="360px"} |![圖1b-N3G_NO3.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_NO3T.png){:width="360px"}
|:--:|:--:|
| <b>圖1a 2019/01/01/00Z 興達新3氣機組PM<sub>2.5</sub>中NO3濃度值之增量。</b>|<b>圖1b 同左但為月平均值</b>|
| ![圖2a-N3GPMdiff.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3GPMdiff.png){:width="360px"} |![圖2b-N3GPMdiffT.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3GPMdiffT.png){:width="360px"} |
| <b>圖2a 同圖1a時間PM<sub>2.5</sub>與PM<sub>10</sub>增量之差值</b>|<b>圖2b 同左但為月平均值</b>|
| ![圖3a-PM25ACdiffT.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM25ACdiffT.png){:width="360px"} |![圖3b-PM10ACdiffT.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM10ACdiffT.png){:width="360px"} |
| <b>圖3a 計畫營運前後Aitken mode濃度在PM<sub>2.5</sub>部分之比例(PM25AC)之月均值增加率。</b>|<b>圖2b 同左但為PM<sub>10</sub>部分比例(PM10AC)。電廠造成附近PM10AC月均值增加0.01%</b>|

### 檢討
- 影響結果的2項因素
  - 增量中含有之負值、且/或
    - 即使使用同一組CCTM_APDIAG（不論營運前或營運後），因一般NO<sub>3</sub><sup>-</sup>在粗顆粒佔比較大，負值則將造成粗顆粒的減少，因此造成PM<sub>10</sub>增量小於PM<sub>2.5</sub>。
  - PM25AC、PM10AC之增加
    - 即便ATOT<sub>i</sub>為正值，營運後乘上較大的PM25AC比例得到較高的PM<sub>2.5</sub>，是有可能大於乘上增加比例不太多的PM10AC的結果。
- 此二者同時作用：PM<sub>2.5</sub>增量大於PM<sub>10</sub>雖不合理，但其乃為必然之數學結果。

## 因應策略方案
### 先相減再過濾
- 雖然負值增量是合理與必然的結果，但是在法規應用上為trivial solution。
- 且在時間平均過程中負值會造成干擾、降低平均結果而不保守。
- 建議在[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)之前就將其排除。

```bash
#kuang@DEVP /nas2/cmaqruns/2019force/output/2019-01/grid03/cctm.XindaN3G-BASE_withFilter0
d1=../../cctm.BASE/daily
d2=../../cctm.XindaN3G/daily
for i in {01..31};do dNC $d1/CCTM_ACONC$i.nc $d2/CCTM_ACONC$i.nc CCTM_ACONC$i.nc ;done
```
- 使用簡單的np.where即可完成過濾的動作。

```python
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
for v in V[3]:
  var=np.where(nc[v][:]>0,nc[v][:],0)
  nc[v][:]=var[:]
```
### 先過濾再相減
- 如果在相減前要進行過濾(nc為營運後、nc0為營運前之背景)，條件需改成「營運後濃度是否大於背景」

```python
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
for v in V[3]:
  var=np.where(nc[v][:]>nc0[v][:],nc[v][:],nc0[v][:])
  nc[v][:]=var[:]
```

### 必須使用同一組粒徑分率(CCTM_APMDIAG)進行[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)
- 如果在[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)前先進行濃度差值的計算，增加的濃度應該適用營運後的CCTM_APMDIAG比較合理。

```bash
#kuang@DEVP /nas2/cmaqruns/2019force/output/2019-01/grid03/cctm.XindaN3G-BASE_withFilter0
ln -s ../../cctm.XindaN3G/daily/APDIAG_b_n3g/* .
```
### 計算程序比較

|順序|傳統作法|新計算程序建議|比較說明|
|:-:|-|-|-|
|1|進行[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)|營運前後CCTM_ACONC相減|後者檔案較大、需要較大磁碟空間進行作業、妥善檔案管理、平行運作|
|2|營運前後CCTM_COMBINE檔案再進一步篩減項目([shk.cs](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs))|連結營運後之CCTM_APMDIAG檔案到同一目錄|前者可以再進一步縮小檔案容量|
|3|營運前後[shk.cs](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs)結果相減、分析、繪圖|進行[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)|前者完工|
|4|(無)|進行[shk.cs](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs)、分析、繪圖|後者完工|

## 結果及討論
- PM<sub>2.5</sub>：最大值變動不大，但臺灣本島中北部、東部的增量變多了。海面上、電廠附近的負值增量消失了。
- PM<sub>10</sub>：山區低濃度範圍更擴大一些
- PM<sub>2.5</sub>/PM<sub>10</sub>：月均值的比例，未過濾前的振盪很大、包括在外海、北部地區及山區，電廠附近也有負值之振盪。經過濾後模擬範圍的比例在0.35~0.95之間，山區約在0.7上下，平地範圍較高約在0.8~0.9，越遠越高。電廠附近與煙流也較高。

| ![圖4a-N3G_PM25.png.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_PM25.png){:width="360px"} |![圖4b-cctm.XindaN3G-BASE.nc_Filtered_PM25.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cctm.XindaN3G-BASE.nc_Filtered_PM25.png){:width="360px"}
|:--:|:--:|
| <b>圖4a 2019年1月份平均PM<sub>2.5</sub>增量濃度 </b>|<b>圖4b 同左但為新計算程序</b>|
| ![圖5a-N3G_PM10.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_PM10.png){:width="360px"} |![圖5b-cctm.XindaN3G-BASE.nc_Filtered_PM10.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cctm.XindaN3G-BASE.nc_Filtered_PM10.png){:width="360px"}｜
| <b>圖5a 2019年1月份平均PM<sub>10</sub>增量濃度 </b>|<b>圖5b 同左但為新計算程序</b>|
| ![圖6a-N3G_rat.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3G_rat.png){:width="360px"} |![圖6b-cctm.XindaN3G-BASE.nc_Filtered_rat.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cctm.XindaN3G-BASE.nc_Filtered_rat.png){:width="360px"}｜
| <b>圖6a 2019年1月份平均PM<sub>2.5</sub>增量濃度與PM<sub>10</sub>之比值 </b>|<b>圖6b 同左但為新計算程序</b>|