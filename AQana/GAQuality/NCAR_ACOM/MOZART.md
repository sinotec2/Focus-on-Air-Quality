---
layout: default
title: "MOZART"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 1
date: 2021-12-12 16:29:31              
last_modified_date:   2021-12-12 16:29:36
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
- MOZART模式全名為臭氧及相關化學成分模式([Model for OZone and Related chemical Tracers](https://en.wikipedia.org/wiki/MOZART_(model)))。
- MOZART模式為NCAR、NOAA轄下 Geophysical Fluid Dynamics Laboratory (GFDL)與德國漢堡大學 Max Planck Institute for Meteorology (MPI-Met)多年來合作發展應用的全球3維大氣化學成分模式，除了應用在對流層之外，平流層及中氣層範圍亦涵括在內。 
  - 氣象場部分，MOZART可以接受包括NWS的NCEP (National Centers for Environmental Prediction)、歐洲的ECMWF(European Centre for Medium-Range Weather Forecasts)、NASA GMAO(Global Modeling and Assimilation Office ) 的GCM等模式輸出。
  - 其空品模擬結果多年來也用在WRF-CHEM、[CAMx](https://www.camx.com/download/support-software/)等模式的邊界與初始條件。
- MOZART數值產品過去也經常應用在地區模擬之邊界與初始條件，詳如下述。

### MOZART結果之解析度
- MOZART 的水平空間解析度視不同機器平台略有差異，一般而言介於2.5~2.8度之間，
- 高度為Non_Hydrostatic SIGMA-P座標從最底層(1000HPa到模式頂層0) 有57層，
- 檔案儲存的時間解析度則為6小時。(UTC0/6/12/18)
- 化學機制方面
  - 標準的MOZART-4有85個氣態污染物，12個氣膠成分，39條光化反應以及157條氣態反應，
  - 碳鍵機制採lump法，VOCs包括3個烯烴與烷烴類物質，以及4個碳以上與芳香烴類物質(BIGALK, BIGENE及TOLUENE)。

### MOZART模擬結果之下載
**MOZART**針對空氣品質模式使用者設有提供資料之[下載網站](http://www.acom.ucar.edu/wrf-chem/mozart.shtml)(`http://www.acom.ucar.edu/wrf-chem/mozart.shtml`) ，給定內容：
![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/mozart_download.png)
1. 基本資料。用做通訊用。
1. 模擬範圍大致的座標 
如下列`ncdump`內容
  - 南北-2~47度、東西80~160度，
  - 須涵蓋氣象檔東亞d1範圍)，每個檔案「必須」有相同的範圍，以便進行檔案的合併
1. 指定之年月日(每日以0600UTC開始以隔日0000UTC結束，共4筆，間隔6小時)，即會將下載連結寄到指定**電子郵件地址**，另行以`wget`或其他方式下載檔案。 日數擷取策略： 
- **5個檔案**方案，每個檔案約為**10日**： 
  - 前月最後10~11天、本月3個檔、下個月1~10日。
  - 檔案**沒有重疊**，`ncrcat`可以自由搭配
  - 因為**MOZART**結果檔案儲存是以當天0600UTC當啟始，以隔天0000UTZ為結束，與一般定義有別，因此在整併全月資料時，此方案會出現缺漏。
- **3個檔案**方案，每個檔案的日期較前述前後**略為增加**一些，以使跨月計算可以順利進行。如
  - 2016123106~2017011100(前一年的最後一天6:00開始~1/10結束在1/11/0:00)，存檔名稱file1:  2016_12_31 ~ 2017_01_10
  - 2017011106~2017012100，存檔名稱file2:  2017_01_11 ~ 2017_01_20
  - 2017012106~2017020200(下個月第一天)，存檔名稱file3:  2017_01_21 ~ 2017_02_01 
- 注意：
  - 選單順序：因為日的選單比較難選(有31日)，建議按照file1(每一月)→file2(每一月) →file3進行(每一月)，以加快速度。
  - file1要注意大、小月、注意潤年檔案會重疊，只能針對同一月份進行`ncrcat`
  - 這樣做法雖然前後檔案會大一些，日期也不具規律性，但在後續處理時3個檔案合併總是比較小，可以減省讀取的時間。
1. Submit之後，等待系統寄來下載網址，約<1~2小時之久。雖然網址只在48小時內有效，此一期間已足夠下載全年數據。 
- 網址內容之萃取
  - 全選系統寄來信件之內容、貼在工作站系統成為一文字檔(如`EMAIL.TXT`)
  - 使用GREP指令：`grep http EMAIL.TXT >http.txt`
  - `wget`指令。範例如下：

```bash
  for i in $(cat http.txt);do 
  wget -q $i
  done
```
  - 由於[下載網站](http://www.acom.ucar.edu/wrf-chem/mozart.shtml)提供的檔名數字，是隨機產生，不建議一一複製貼上、同步下載時將容易錯漏。

### nc檔案更名
1. 其檔案為netCDF格式，東亞範圍1天(6小時解析度)檔案大小約**57M**(2017年後更新模擬項目增加為**65M**)。
1. 資料內容的確認方式： 

```bash
$ ncdump mozart4geos5-20160217200203502764.nc|more
netcdf mozart4geos5-20160217200203502764 
{dimensions:        time = UNLIMITED ; // (44 currently)
        lev = 56 ;
        lat = 26 ;
        lon = 33 ;
        nchar = 80 ;
        ilev = 57 ;
        …
        history="Wed Feb 17 20:02:03 2016: ncks -d lat,-2.0,47.0 -d lon,80.0,160.0 /var/www/html/acd/wrf-chem/archive/mozart4geos5_20121231.nc /var/www/html/acd/wrf-chem/temp/20160217200203502764-20121231.nc" ;
        :NCO = "4.0.5" ;
```
- 注意：檔案的**維度**必須完全一樣，才能進行檔案的合併`ncrcat`
1. 由於檔名為下載檔案的時間序列資訊，並沒有檔案內容時間資訊，這些資訊會寫在檔頭(**history**)裏，可以用下列指令將其讀出並以起始時間命名之： 
  - 按照`history`內容更名方式

```bash
for i in $(ls moz*.nc);do 
nc=`ncdump $i|head -n 500|grep history|awkk 9|cut -d'-' -f3`
mv $i $nc
done
```
- 按照`date`內容更名方式

```bash
for i in $(ls *3?.nc);do 
nc=`ncdump -v date $i|tail|grep date|awkk 7|cut -c-8`
mv $i $nc.nc
done
```
- 按照`ncks`指令內容更名方式

```bash
for nc in $(ls *nc);do 
i=$(ncdump -h $nc|grep ncks|cut -d'/' -f10|cut -d '.' -f11|cut -c -10)
mv $nc $i.nc
done
```

## Reference
- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- Ramboll, **mozart2camx**,  |[6apr22](https://camx-wp.azurewebsites.net/getmedia/mozart2camx.6apr22.tgz), 4/6/2022
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.