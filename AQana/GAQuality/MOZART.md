---
layout: default
title: "MOZART"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 1
date: 2021-12-12 16:29:31              
last_modified_date:  2022-06-30 11:18:35
tags: mozart2camx
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
  - 其空品模擬結果多年來也用在WRF-CHEM、CMAQ、[CAMx](https://www.camx.com/download/support-software/)等模式的邊界與初始條件。
- MOZART數值產品過去也經常應用在地區模擬之邊界與初始條件，詳如下述(歷史)。
- MOZART程式版本目前為第4版，已無繼續更新的計畫。原本對外提供執行結果的服務也在2022年3月[正式停止][mz_stop]，目前提供全球作業化模式模擬結果的模式是[CAM-chem](https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)(2001~2020再分析)及[WACCM](https://www.acom.ucar.edu/waccm/download.shtml)(近實時再分析及預報)。

### MOZART結果之解析度
- MOZART 的水平空間解析度視不同機器平台略有差異，一般而言介於2.5~2.8度之間，
- 高度為Non_Hydrostatic SIGMA-P座標從最底層(1000HPa到模式頂層0) 有57層，
- 檔案儲存的時間解析度則為6小時。(UTC0/6/12/18)
- 化學機制方面
  - 標準的MOZART-4有85個氣態污染物，12個氣膠成分，39條光化反應以及157條氣態反應，
  - 碳鍵機制採lump法，VOCs包括3個烯烴與烷烴類物質，以及4個碳以上與芳香烴類物質(BIGALK, BIGENE及TOLUENE)。

## MOZART模擬結果之下載(deprecated)
**MOZART**針對空氣品質模式使用者設有提供資料之[下載網站](http://www.acom.ucar.edu/wrf-chem/mozart.shtml)(`http://www.acom.ucar.edu/wrf-chem/mozart.shtml`) ，給定內容：
](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/mozart_download.png)
1. 基本資料。用做通訊用。
1. 模擬範圍大致的座標 
如下列[ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump)內容
  - 南北-2~47度、東西80~160度，
  - 須涵蓋氣象檔東亞d1範圍)，每個檔案「必須」有相同的範圍，以便進行檔案的合併
1. 指定之年月日(每日以0600UTC開始以隔日0000UTC結束，共4筆，間隔6小時)，即會將下載連結寄到指定**電子郵件地址**，另行以`wget`或其他方式下載檔案。 

### 日數擷取策略
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

### 下載全年數據
- Submit之後，等待系統寄來下載網址，約<1~2小時之久。雖然網址只在48小時內有效，此一期間已足夠下載全年數據。 
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

## MOZART2CAMx

- 雖然NCAR不再繼續發展Mozart模式，然而其檔案格式仍然是全球大氣成分模式所採用，也因此Ramboll公司也會持續維護MOZART2CAMx程式，目前是6apr22版本。
- 未來是否更新，還需持續關注其官網公告內容。

### 應用情形

- MOZART2CAMx(與其前處理程式[ncf2ioapi][ncf2ioapi])應用在下列情況
  - [CAM-chem模式結果之讀取及應用](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/1.CAM-chembasic/)
  - [WACCM模式結果之下載、讀取及應用](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/3WACCM/)
  - [REASv3.1地面排放檔案之處理](https://sinotec2.github.io/Focus-on-Air-Quality/CAMx/emis/4.3REASgrnd/)
  - [全球船隻排放量之處理_CAMx](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/FMI-STEAM/old/)

### 程式下載

- 下載點：[官網](ttps://camx-wp.azurewebsites.net/getmedia/mozart2camx.6apr22.tgz)

### 程式內容架構

- 下載包裏包括了
  1. mozart2camx程式：主要進行水平網格切割、垂直網格對應、物質名稱之對應。ncf2ioapi則為其**前處理程式**，分別針對類似程式的大氣成分輸出檔案
  2. ncf2ioapi_am3：NOAA [AM3](https://www.gfdl.noaa.gov/am3-model/)模式
  3. ncf2ioapi_mozart：NCAR [mozart][mzr]模式
  4. ncf2ioapi_waccm：NCAR [WACCM][waccm]模式

### 編譯

- 前處理程式
  - 選取正確版本
  - 準備[netCDF][nc]及[ioapi][ioapi]程式庫
  - 開啟[SMP][SMP]平行運算
  - 詳[ncf2ioapi][ncf2ioapi]的[編譯](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ncf2ioapi/#ncf2ioapi的編譯)
- 主程式編譯
  - 連結正確版本的物質對照表到`G2Lconv.EXT`
  - 檔名規則G2Lconv_MECH_PART_from_MODEL_%D%b%y.EXT
    - MECH反應機制，包括：CB05/CB6/CB6r2/CB6r4
    - PART粒狀物計算方法：CF/AE5/AE6
    - MODEL大氣模式：GEOS5/NCEP/AM3/WACCM
    - 時間：日(2碼)、月(jan~dec)、年(2碼)
  - Makefile修改
    - compiler設定
    - 連結程式庫與包括檔：需完全與前處理一致

```bash
...
F90 = ifort
...
LIBS =    -L/cluster/bld/ioapi3.1/Linux2_x86_64ifort -lioapi \
          -L/cluster/netcdf/lib -lnetcdf -lnetcdff \
         $(OMPLIBS) $(ARCHLIB) $(ARCHLIBS)
INCLUDE = -I/cluster/bld/ioapi3.1/ioapi \
          -I/cluster/netcdf/include
```

## Reference

- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- Ramboll, **mozart2camx**,  [6apr22](https://camx-wp.azurewebsites.net/getmedia/mozart2camx.6apr22.tgz), 4/6/2022
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.

[mz_stop]: <https://www.acom.ucar.edu/wrf-chem/mozart.shtml> "MOZART-4 results are no longer available as of March 18, 2022. We are no longer running MOZART-4, so please use CAM-chem output instead, which is available for 2001 to present: https://www2.acom.ucar.edu/gcm/cam-chem-output"
[mzr]: <https://en.wikipedia.org/wiki/MOZART_(model)> "MOZART: (Model for OZone And Related chemical Tracers) is developed jointly by the (US) National Center for Atmospheric Research (NCAR), the Geophysical Fluid Dynamics Laboratory (GFDL), and the Max Planck Institute for Meteorology (MPI-Met) to simulate changes in ozone concentrations in the Earth's atmosphere. "
[waccm]: <https://www2.acom.ucar.edu/gcm/waccm> "The Whole Atmosphere Community Climate Model (WACCM) is a comprehensive numerical model, spanning the range of altitude from the Earth's surface to the thermosphere"
[ncf2ioapi]: <https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ncf2ioapi/> "全球模式結果檔案的轉換(nc2m3)"
[ioapi]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ioapi/> "IOAPI的編譯"
[nc]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/lib_comp/> "NC相關程式庫之編譯"
[SMP]: <https://zh.wikipedia.org/wiki/对称多处理> "對稱多處理（英語：Symmetric multiprocessing，縮寫為 SMP），也譯為均衡多處理、對稱性多重處理、对称多处理机[1]，是一種多處理器的電腦硬體架構，在對稱多處理架構下，每個處理器的地位都是平等的，對資源的使用權限相同。"