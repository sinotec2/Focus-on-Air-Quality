---
layout: default
title:  按日拆分m3.nc檔案
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2021-12-18 20:50:01
---
# 按日拆分m3.nc檔案(brk_day2.cs)
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

- 雖然CCTM的執行批次範圍是數日，但CCTM腳本常將所需的輸入檔切割成逐日檔，其考量可能是：
  - 方便進行批次範圍的組合，如果要拆散再另行組合成其他起訖日期的批次(如CCTM的邊界條件 之bld_19.cs)，有逐日檔案勢必方便許多
  - **MM5**/**WRF**以來的IO習慣，很多也是逐日儲存。
  - 檔案管理維護比單一大檔容易，壞了某一天檔案只須修復該日檔案即可
- 但是對於系統性修改，**逐月**檔案會比**逐日**檔案方便。這2個面向如果要同時滿足，勢必需要有轉換的程式。
  - 合併：可以將全月範圍的檔案放在同一目錄，有足夠的月前、月後日期，如此就可以應用[ncrcat]()一次整併。
  - 拆分：雖然可以用`ncks -d`來做，但其中還需少許的日期計算、確認等等。

## brk_day2.cs腳本程式

### 引數

- 需拆分的檔案名稱
- 檔案命名規則
  - 檔案必須以`dot`做為間隔
  - 年月必須在第2個`dot`間格位置，用以開啟目錄、判斷前後月份、
  - 「年月」將被「年月日」替換掉，檔名其餘部分不會更動
  - 範例：teds10.**1601**.timvar.nc、ind_EAsia_81K.**1601**.nc

### 數據所在路徑

- (無約定)
- 腳本會在數據所在位置下開設yymm的目錄。

### 日期的計算

- 按照**WRF**執行[批次的約定](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/#%E6%89%B9%E6%AC%A1%E7%9A%84%E5%AE%9A%E7%BE%A9)，前月15日為起始日，run5為當月CCTM執行開始日
- 將檔案內容所有時間都予以拆分，總小時數由[ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump)得知
- 每一天筆數`HRPD` ：24小時與`TSTEP`的商數，`TSTEP`由[ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump)得知
- 還要修正逐日檔的`SDATE`屬性(`yrj`)，CCTM會檢查
- 給定日期(`ymd`)做為新檔名```newfn=${fn/$yrmn/$ymd} ```
- yrj、ymd由`date`計算而得，才有一致性不會出錯。 

### brk_day2.cs腳本程式內容

{% include download.html content="[brk_day2.cs](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2bc.py)" %}


### 平行運作

- ncks可以平行運做，但不見得有較高的效率，涉及檔案存取的速度瓶頸、以及工作站的記憶體。
- 此腳本一次處理一整個月，如果有跨月、大小月問題，應俟全年處理完後，執行[ln_run12.cs][ln_run12cs]來連結修正

## brk_day3.cs腳本程式

- 由於m3nc檔的時間步階有逐時、逐3小時、逐6小時等等不一而足，也不見得一律從0時開始，因此要設定統一的日數規則實屬不易。
- 這個版本的特色在於將m3nc檔案切割成每一個timeframe檔案、以日期作為檔名規則之一，再用ncrcat予以整併成逐日檔。此法應較前述版本具有實用性。

### 引數

- (同上brk_day2.cs腳本)

### 外部程式

- 列印m3.nc的時間標籤[pr_tflag.py][pr_tflag]
- NCO程式：ncks、ncatted、ncrcat

### 陣列語法之應用

- 記錄所有[pr_tflag.py][pr_tflag]的結果：雙數為yyyyjjj、單數為hh0000
- 將前述結果陣列改成ymd(YYYYMMDD)、hrs(HH)、以及yms(yymm)，分別用作逐日標籤、timeframe辨識、以及月份目錄。

### ncks及ncatted

- 將檔案切割成一個個timeframe檔案，將時間標籤記錄在檔案名稱規則之中。
- 因每日檔案長度可能不同，全域屬性SDATE及STIME不知要加在哪一個檔案。因此最保險的做法就是每個檔案都將SDATE及STIMEdou用ncatted改成正確，如此怎麼串連都會是正確的結果。

### ncrcat之啟動

- 整併迴圈可以就檔案的日數、或timeframe個數(換日則處理前日檔案)等等2種方式
  - 每日檔案可能有不同時間，也不見得從0時開始，因此按日數迴圈的程式設計會太複雜。
  - 換日時執行：此方案雖然可行，但最後日需特別處理
- ncrcat執行完畢後，每個timeframe暫存檔案即可刪除

### 目錄之創建與管理

- 檔案如果跨月，應按照各timeframe所屬的月份儲存，而不是按照起始日之月份。這樣後續檔案才有覆蓋、更新的可能。
- 如果逐月執行需要前後月檔案，再另行連結即可。
- 最直覺的創建目錄方式，是從每個timeframe時間標籤中讀取年月時，就一併創建。(mkdir -p會略過已經存在的目錄)


[pr_tflag]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pr_tflag/> "列印m3.nc的時間標籤"
[ln_run12cs]: <https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/PTSE/3.pt_timvarWork/#ln_run12cs> "ln_run12.cs"