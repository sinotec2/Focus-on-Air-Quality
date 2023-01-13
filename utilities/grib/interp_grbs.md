---
layout: default
title: CWB_WRF grib數據檔的時間內插
parent: grib Relatives
grand_parent: Utilities
nav_order: 1
date: 2022-08-10 11:29:26
last_modified_date: 2022-08-10 11:29:30
tags: CWBWRF
---

# CWB_WRF grib數據檔的時間內插
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
- [CWB_WRF數據][CWB_WRF]偶會發生檔案喪失(data missing)的情形。原因不明，或許在下載時正好遇到電腦正在更新檔案，還是什麼環節出問題，總之，會有需要進行補遺的情況。
- 幸好大多喪失情況是缺少某一個特定時間的預報檔案。經由前後時間的內插即可解決此一問題。
- 雖然CWB_WRF數據並沒有統一的維度、雨量也是累加值，所幸前後時間的平均尚能符合定義。
- 一般使用[pygrib][pygrib]來進行讀取[grib][grib]檔案，但不能用在寫出檔案，pygrib.open也沒有控制讀寫的選項，一律唯讀。必須另外寫出binary檔，這部分可以參考[網友jiangleads][jiangleads]的範例。
- 由於每個grib檔案的內涵多有差異，本程式無法適用所有的grib格式檔，還是需一一檢視。

### grib與netCDF格式之比較

項目|grib|netCDF|說明
:-:|-|-|-
版本|2|4|
字元|binary|binary|
主要應用|氣象模式|氣象、大氣化學、</br>地球科學|
順序|循序讀寫|階層讀寫|
檔頭|無|有|
python模組|[pygrib][pygrib]|[netCDF4](https://pypi.org/project/netCDF4/)|
讀寫|唯讀|可讀寫|前者另開binary檔案
官網|[WMO Guide](https://web.archive.org/web/20201213173506/http://www.wmo.int/pages/prog/www/WMOCodes/Guides/GRIB/GRIB2_062006.pdf)|[www.unidata.ucar.edu</br>/software/netcdf](https://www.unidata.ucar.edu/software/netcdf)|

## [interp_grbs.py][interp_grbs.py]程式說明
### IO
- 引數：前後正常下載之檔案名稱(間隔12小時)，喪失檔案為其中間時間
  - 如`interp_grbs.py M-A0064-054.grb2 M-A0064-066.grb2`，54與66為正常下載(間隔12小時) 之時間，中間的60則為喪失檔時間。
- 結果：`M-A0064-060.grb2`
### 重要參數
1. `grbs[0].messages`：grib可以視為傳統的binary檔案，也是循序一批批寫入的檔案，每一批grib的習慣稱之為message。因此有總批次筆數，就是messages。(相對netCDF為階層式讀寫檔案，netCDF從來不需要、也不知道有rewind，grib就需要[rewind][jswhit])
1. `range(1,grbs[0].messages+1)：`每一批message的批號數是其內容之一，批號自1開始編號，一直到最後再加1(python習慣)。
1. `grbs[0].message(i)`：呼叫(抽取)批號`i`的message，不是序列也不是字典，而是函數關係。
1. `grb.analDate`：grib檔案的分析時間(模式的起始時間)。這個時間在不同的預報輸出檔內都是一樣，在於區分預報執行的批次。因此不需要變動。
1. `grb.validDate`：這個時間標籤不能修改，似乎是grb方法自行計算出來的，從`grb.analDate`以及以下要介紹的`grb['forecastTime']`計算而得。
1. `grb['dataDate']`：grb是方法，也是個dict，有幾個索引(keys)，然而與我們此次需要修改的項目只有時間。dataDate是8碼的整數，似乎沒有其他作用，後續程式也不會用到，還是參照[網友][jiangleads]範例將其修正。
1. `grb['forecastTime']`：預報時間，單位為小時，非負整數。這項需要修改。
1. `grb.values[:]`：此一方法的結果是個numpy.array。類似方法`grb.data()`的結果是個tuple。同樣是取值為什麼需要2種方法，不是很瞭解，只知道`grb.data()`目前還沒有看到實際的範例就是了。
1. `grb.tostring()`：此方法結果是個很長的字串，類似dump的作用，也是grib檔案message的意涵。將其按照批次順序寫進binary檔案就好了。

### 批次內插並寫進檔案之迴圈

```python
grbout = open(fnames[0].replace(fcst_hrA[0],s),'wb')

for i in range(1,grbs[0].messages+1):
  grb=grbs[0].message(i)
  s=(grb.validDate+datetime.timedelta(hours=6)).strftime("%Y%m%d")
  grb['dataDate']=int(s)
  grb['forecastTime']=fcst_hr
  grb.values[:]=(grbs[0][i].values+grbs[1][i].values)/2.
  msg = grb.tostring()
  grbout.write(msg)
  ```

### 程式下載

{% include download.html content="grib數據的時間內插@github：[interp_grbs.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/grib/interp_grbs.py)" %}

## Reference

- sinotec2(2022) [中央氣象局WRF_3Km數值預報產品](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/) at Github/Focus-on-Air-Quality
- Jeff Whitaker(2021), [pygrib官網](https://pypi.org/project/pygrib) at pypi.org
- jiangleads(2018)， [pygrib学习](https://www.cnblogs.com/jiangleads/p/9705787.html) @博客園，posted @ 2018-09-26 12:04.
- Jeff Whitaker(2021), [Matplotlib/Basemap and pygrib example](https://nbviewer.org/gist/jswhit/8635665) @nbviewer


[CWB_WRF]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/> "中央氣象局WRF_3Km數值預報產品"
[pygrib]: <https://pypi.org/project/pygrib/> "官網：Provides a high-level interface to the ECWMF ECCODES C library for reading GRIB files. There are limited capabilities for writing GRIB files (you can modify the contents of an existing file, but you can't create one from scratch)"
[grib]: <https://zh.wikipedia.org/zh-tw/GRIB> "GRIB（GRIdded Binary或通用定期發布的二進位形式資訊）是通常用在氣象學中儲存歷史的和預報的天氣資料的簡明資料格式。它由世界氣象組織的基本系統委員會於1985年標準化，描述於WMO編碼手冊。 第一版GRIB被世界範圍內的多數氣象中心業務化使用，用於數值天氣預報（NWP）輸出。第二版是2003年發表的GRIB2，各國氣象資料發布逐步更新到這個格式與版次。"
[jiangleads]: <https://www.cnblogs.com/jiangleads/p/9705787.html> "pygrib学习@博客園"
[interp_grbs.py]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/grib/interp_grbs.py> "grib數據檔的時間內插程式@github"
[jswhit]: <https://nbviewer.org/gist/jswhit/8635665> "jswhit：Matplotlib/Basemap and pygrib example@nbviewer"
