---
layout: default
title: 特定位置排放量之敏感性
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 5
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 特定位置排放量之敏感性
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
- 點源簡化以高空網格型式輸入是公版背景基準排放量特色之一。
  - 由於單一點源年排放量可能有千噸以上，為各界所關注，此一作法會造成什麼樣的效果值得探討。

## 特定高度、特定位置排放量之敏感性
- 此處範例探討自背景排放量檔案中剔除特定點污染源造成的濃度差異，即為該廠之關閉敏感性。此處以臺中電廠為例。
- 由[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI)中找到臺中電廠(滑鼠滑過在下方會出現(i,j)座標位置)
  - 位置(fortran notation)為(40,87,5)及(40,88,5)
  - 位置並沒有時間變化。排放量沒有時間變化。
- 使用下列程式自背景基準排放(BASE)中予以剔除、另存新檔(dTZPP)、執行cctm
- TZPP = BASE - dTZPP

### 剔除特定位置之排放量
- 注意python的空間索引順序與fortran相反、標籤自0開始。

```python
fname='cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_0-8NoTZPP'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
for v in V[3]:
    nc[v][:,4,87,39]=0.
    nc[v][:,4,86,39]=0.
nc.close()
```
### 排放差異
- 將公版模式1月份排放量加總結果與[add_tzpp.py](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis/#直接選取teds11點源資料庫add_tzpppy)結果排放量比較如下表
  - 時間範圍都以1/1/00~1/31/23
  - 空間範圍：公版條件如上述2個網格之內容。[add_tzpp.py]()則為符合管編及高度2個條件之內容。
- 排放單位：gmole/s(gas)、g/s(P*)  

|Spec|somke|add_tzpp.py|
|:-:|-:|-:|
|CO|324.92383|272.7862|
|NO|5726.74|5965.1284|
|NO2|636.30457|662.79205|
|PAL|772.9443||
|PCA|446.67633||
|PCL|8.143751||
|PEC|554.1376||
|PFE|378.05652||
|PK|60.13299||
|PMC|3100.6912||
|PMN|3.6705146||
|PMOTHR|7558.5415 (+P*=16048.072)|17837.893|
|PNCOM|164.42868||
|PNH4|45.004257||
|PNO3|7.3863435||
|POC|409.12964||
|PSI|1166.5374||
|PSO4|1316.7242||
|PTI|55.866913||
|SO2|3240.5608|3389.6604|

- 除CO外，其餘項目公版排放量略低於[add_tzpp.py]()。二者總量差異有限
- 公版有較完整的PM分率，
  - 因各PM物質的水溶性、化學特性都有差異，可能會因詳細計算結果而有較低的濃度。
  - 相對而言PMOTHR較為惰性，應為偏僻原生性污染物之保守設定。

### 結果分析
- 公版排放量模擬臺中電廠燃煤機組關閉後之空品敏感性(TZPP = BASE - dTZPP)
- [add_tzpp.py]()排放量之增量(TZPP' = aTZPP- dTZPP)

| ![TZPP_pmfM.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/TZPP_pmfM.PNG) |![TZPP_pmfT.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/TZPP_pmfT.PNG) |
|:--:|:--:|
| <b>PM<sub>25</sub>濃度差異之月最大值</b>|<b>PM<sub>25</sub>濃度差異之月均值</b>|