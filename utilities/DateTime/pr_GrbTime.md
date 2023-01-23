---
layout: default
title:  grib2的時間標籤
parent: Dates and Times
grand_parent: Utilities
last_modified_date:   2022-10-26 13:31:34
tags: CWBWRF  CAMS GFS datetime
---

# grib2的時間標籤
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

### 背景
- [grib2][GRIB2]是WMO會員國交流觀測與模擬結果氣象數據的重要協定格式。
- 常用grib2檔案格式包括
  - NCEP之檔案如
    - 再分析數據[FNL](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/NCEP/ff.py/)檔與
    - 全球氣象預報模式[GFS](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/GFS/)之輸出檔案
  - CWB之WRF模擬結果，詳[中央氣象局WRF_3Km數值預報產品之下載](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/1.get_M-A0064)
  - ECMWF之
    - [EAC4](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF_rean)及
    - [CAMS][CAMS]空品預報數據檔格式、
- grib2格式有許多parser，此處以最簡單的pygrib來提供時間標籤  

### 程式設計及注意事項
- 因為grib2檔案大多是一個timeframe一個檔案，而其grbs.message屬性(數據檔筆數)卻可能很多，因此需小心設計。
- 原本設計
  - `dates=list(set([grbs[i].validDate for i in range(1,grbs.messages+1)]))`
  - 全部讀完每一筆數據的validDate時間，再由其集合來找出相異值，原則是沒有錯，但因為grib不像netCDF是層級且有壓縮設計、且是循序讀取，因此如果筆數多一點，讀取的速度會非常慢。
- 修正設計
  - 一般想瞭解檔案的時間標籤大多為起、迄時間，因此只需執行最先與最後之筆數即可
  - `dates=list(set([grbs[i].validDate for i in [1,grbs.messages]]))`

### 程式碼

```python
#$ cat ~/bin/pr_GrbTime.py
#!/opt/anaconda3/envs/gribby/bin/python
import sys
import pygrib
fname=sys.argv[1]
grbs = pygrib.open(fname)
m=grbs.messages
if m <=100:
  dates=list(set([grbs[i].validDate for i in range(1,m+1)]))
else:
  dates=list(set([grbs[i].validDate for i in [1,m]]))
n=len(dates)
if n>1:
  dates.sort()
for i in range(n):
  print(i,dates[i])
```  

[GRIB2]: <https://zh.wikipedia.org/zh-tw/GRIB> "GRIB是通常用在氣象學中儲存歷史的和預報的天氣資料的簡明資料格式。它由世界氣象組織的基本系統委員會於1985年標準化，描述於WMO編碼手冊，最初編號為FM 92-VIII Ext. GRIB。 第一版GRIB被世界範圍內的多數氣象中心業務化使用，用於數值天氣預報輸出。"
[CAMS]: <https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview> "CAMS每天2次進行全球大氣成分的5天預報，包括50多種氣狀物和7種顆粒物(沙漠塵埃、海鹽、有機物、黑碳、硫酸鹽、硝酸鹽和銨氣溶膠)。初始條件為衛星及地面觀測數據同化分析結果，允許在地面觀測數據覆蓋率低、或無法直接觀測到的大氣污染物進行估計，除此之外，它還使用到基於調查清單或觀測反衍的排放估計，以作為表面的邊界條件。"

