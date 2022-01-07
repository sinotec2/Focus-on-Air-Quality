---
layout: default
title: 輸出揚沙排放量
parent: WRF-chem
grand_parent: "WRF"
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
- WRF/chem模式內設是不輸出揚沙排放量的，須由Registry/registry.chem中打開設定，重新編譯，詳見[]()
```bash
for d in 03-3{0..1} 04-0{1..9};do nc=wrfout_d01_2018-${d}_00:00:00;ncks -O -v EDUST1,EDUST2,EDUST3,EDUST4,EDUST5,Times,XLAT,XLONG $nc EDUST_$d.nc;done
for d in 03-3{0..1} 04-0{1..9};do nc=EDUST_$d.nc;ncrename -O -d klevs_for_dust,bottom_top $nc a;mv a $nc;done
```
### 程式I/O檔案

### 程式說明


## 結果檢核
- 2018/4/5~4/7東亞沙塵暴傳播之模擬結果
  - [Youtube](https://youtu.be/kvF1gLMlE0Q)
  - [GIF](http://114.32.164.198/soong/20180405WRFchem.gif)
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/)
  
## Reference
