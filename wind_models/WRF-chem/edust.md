---
layout: default
title: 輸出揚沙排放量
parent: WRF-chem
grand_parent: WRF
nav_order: 5
date: 2022-01-07 09:49:07
last_modified_date: 2022-01-07 09:49:12
---

# 輸出揚沙排放量
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
- 揚沙排放量在東亞乃至臺灣地區(細)懸浮微粒的模擬是非常重要的數據，不單隨時間、區域而變遷，也具有粒徑之特性。揚沙排放量之推估，目前並沒有某一單位長期投注、持續更新、惶論有作業化、逐時之推估結果可供引用。
- 過去推估方式
  - 個案方式：以WRF/chem模式進行推估：全月、全年作業須耗費計算資源
  - 總量推估：以年度或其他時間期程衛星照片的差異推估：應用在個案時仍需另建排放模式
- 推估之不確定性與困難
  - 現場確認：較單純但數據少
  - 下游長程輸送結果確認：數據多，但其間影響源更多
  - 初步驗證還可接受

## 程式說明
### 編譯
- WRF/chem模式內設是不輸出揚沙排放量的，須由Registry/registry.chem中打開設定，重新編譯。
- 詳見[輸出變數項目之管理](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WRF-chem/configure_compile/#輸出變數項目之管理)及[namelist.input](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/namelist.input/#wrfout輸出變數項目之增減)

### emis_dust單位的版本差異
- v4.0為**DUST emissions bin1~5**，單位為&mu;**g m<sup>-2</sup>s<sup>-1</sup>**
- V4.3.2 為**Accumulated DUST emissions bin1~5**，單位為**kg m<sup>-2</sup>**

### namelist.input設定及執行
- (無需特別指定)

### 後處理
- 此處不需累計所有的揚沙粒徑，只需從wrfout檔案中抽出另存。
- 如欲以[VERDI]()處理
  - 因有時間及空間的維度，要記得加上`Times,XLAT,XLONG`等變數讓[VERDI]()知道時間與位置
  - EDUST的垂直維度不是傳統`bottom_top`，而是`klevs_for_dust`，雖其長度為1，還是需先[去除](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#維度刪除ncwa)或[更名](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#維度更名(ncrename))其垂直軸名稱，否則[VERDI]()不能解析。

```bash
for d in 03-3{0..1} 04-0{1..9};do nc=wrfout_d01_2018-${d}_00:00:00;ncks -O -v EDUST1,EDUST2,EDUST3,EDUST4,EDUST5,Times,XLAT,XLONG $nc EDUST_$d.nc;done
for d in 03-3{0..1} 04-0{1..9};do nc=EDUST_$d.nc;ncrename -O -d klevs_for_dust,bottom_top $nc a;mv a $nc;done
```

## 結果檢核
- 2018/3/30~4/9東亞沙塵暴之模擬結果

| ![edust1_xy.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/edust1_xy.PNG) |
|:--:|
| <b>圖1 模擬期間最大揚沙排放量之分布，單位為&mu;g m<sup>-2</sup>s<sup>-1</sup></b>|
| ![edust1_t.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/edust1_t.PNG) |
|:--:|
| <b>圖2 模擬期間地區排放量之時序變化，單位為&mu;g m<sup>-2</sup>s<sup>-1</sup></b>|
  
## Reference
