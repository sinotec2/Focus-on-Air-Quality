---
layout: default
title: m3nc2gif
parent: wrf-python
grand_parent: Graphics
last_modified_date: 2022-06-09 20:55:11
---

# m3nc檔案轉GIF
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
- USEPA Model3 的nc檔案格式([IOAPI](https://cmascenter.org/ioapi/documentation/all_versions/html/))雖然可以用VERDI或其他軟體打開、檢視，但還是不夠簡潔，尤其在公版模式、自動執行、遠端計算服務的過程中，如果能在模式計算完、後處理都結束後，自動產出GIF檔案，公布在網站上，會非常有幫助。
- 畫等值線圖對matploglib不是問題，但因為座標投影的問題，很容易發生位置扭曲的情形，還是需要用經緯度來校正。這也是wrf-python的強項。麻煩的是必須從wrf_out來讀取座標系統的轉換參數。
- matplotlib等值圖並不是raster圖檔，而是有內插效果的，不會像VERDI一樣鋸齒狀。
- 此處也同時解決了環保署提供公版後處理工具的缺失：
  - 直接座標系統改成蘭伯投影系統
  - 256色階改成10～15階
  - 取消白色～淡藍色之間的漸層
  - 線性色階改成彈性判斷
    - 最大/最小比值高於15:非線性、對數色階，適用在煙流增量分布，
    - 低於15:線性色階，適用在濃度變化不大的空品項目。

## 輸入及輸出
### 引數
- m3nc檔案名稱
  - 檔名會寫在Title上，雖會去掉路徑，但字數長度還是有限，
  - 最好控制在10個字元之內。

### 輸入檔案
- m3nc檔案
- wrfout_d04：需存在同一工作目錄下

### 輸出檔案
- *v*_**NN**.png、*v*為模擬空氣品質項目，*NN*為00～99的時間序列。
- *v*.gif：最後整併結果

## [m3nc2gif.py](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/utilities/Graphics/wrf-python/m3nc2gif.py)
- 
## 結果比較
- 公版後處理工具、VERDI、m3nc2gif