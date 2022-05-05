---
layout: default
title: 濃度預報系統之實現
nav_order: 5
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
---
# 本土化CALPUFF濃度預報系統之實現
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
Leed大學[CEMAC中心](https://www.cemac.leeds.ac.uk/)建置了Masaya 火山噴發SO<sub>2</sub>/SO4造成地面濃度的[預報模式](https://www.cemac.leeds.ac.uk/home/project-summaries/unresp/)，範例如圖所示。由於氣象預報數據、大氣擴散模式等皆為官方作業系統與優選模式，因此具有高度的參考價值。

此處將其進行本土化，應用於空氣品質預報、緊急應變作業系統中。

該系統自動下載未來48小時MAM氣象數值預報的結果，轉成CALMET的輸入檔，進入CALPUFF模式進行地面空氣品質的模擬。

由於CALPUFF模式具有考慮3D風場、地形變化、化學反應等模擬能力，曾被美國環保署列為大氣擴散中的優選模式，用於大型固定污染源原生污染物以及二次氣膠長程傳輸的模式。

## 挑戰任務與成果
### 挑戰任務
系統工作流程由[Run.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/Run.sh)批次檔所控制，重要節點及困難如下：
1. 自動下載我國中央氣象局（CWB）數值預報（WRF）結果，並進行解讀。
	1. CWB會員登錄、檔案網址之定位與確認
	2. 氣象與空品模式的模擬範圍與解析度之決定
	3. 自動下載與儲存空間之預備
	4. 美國MAM預報內容與台灣WRF模式預報內容的差異與對照、
2. 解讀程式（Create3DDAT.py）的安裝與修改
	1. Python環境之設定（內設為3.6版）
	2. grib-api模組之安裝（wasg不能import的問題）
	3. 座標系統的調整轉換（經緯度twd97 vs LCP）
3. CALMET模式的偵錯
	1. Fortran程式編譯（內設使用pgf90，與ifort、gfortran版本的差異）
	2. 輸入資料間隔6小時程式的偵錯
4. 排放量的設定
5. CALPUFF模式輸出的修改
	1. Calpuff.inp中離散點的設定
	2. output.f 離散點之輸出
	3. PM<sub>2.5</sub> 的計算（結合銨鹽重量的計算）
6. 等濃度圖與網站設定
	1. 模擬污染物項目、小時數、動畫、濃度等級的修改
	2. 指定外部IP（內設是本機）

### 執行方式
1. 切換目錄到UNRESPForcastingSystem
2. 編輯[Run.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/Run.sh)打開要執行的程式

```bash
# Defaults that can be overwritten by editing HERE:
# Command line option m switches all to false
runTERREL=false (地形)
runCTGPROC=false（土地使用）
runMAKEGEO=false（綜合地理設定）
run3DDAT=false（下載WRF grib files）
runCALMET=false(執行calmet)
runCALPUFF=false（執行calpuff）
runmodel=true
```
3. 將conda環境設成grippy: source ~/conda_ini grippy
4. sh Run.sh -p -d yyyymmdd
	- -d 指定起始日期（之後48小時）
	- -p 繪製所有物質的圖形
 
### 排放位置等參數之改變
1. 檔案模板：[calpuff.inp](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff.inp)
2. 修改位置
	- 模式採用Lambert 投影座標系統，原點位在台灣中心點，北緯24.61，東經120.99.
	- (Taizhong PP)<    1 ! X =  -49.873, 63.288,  150,      4.7,    11.00,  19.8, 363.0,   .0,   5.440,
	- (Tongxiao PP)>    1 ! X =  -32.064, 97.505,  150,      4.7,    11.00,  19.8, 363.0,   .0,   5.440,

### 成果比較
- https://homepages.see.leeds.ac.uk/~earunres/
- http://114.32.164.198:8000/UNRESP_VIZ/index.html?v=1

| ![unresp1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp1.png)|
| <b>leed大學火山SO<sub>2</sub>預報結果畫面</b>|
|:--:|
|![unresp2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp2.png)|
| <b>台中電廠PM<sub>2.5</sub>預報結果畫面</b>|

## 氣象數據下載與解讀
### 氣象數值預報的選擇
  - 雖然國際間公開的數值預報成果有很多，覆蓋台灣地區範圍也不在少數，然而經比較其解析度不足以模擬大型固定源，且對局部地形及海陸風現象亦不足以解析。
  - 經比較分析選擇以CWB WRF 模式3KM模擬結果最為恰當。
  - CWB WRF 3KM預報的作業方式、演進與評估，可以參考
    - 陳依涵、戴俐卉、賴曉薇、陳怡儒、林伯勳、黃小玲、江琇瑛、江晉孝、陳白榆、洪景山、馮欽賜（2017）[中央氣象局區域模式2017 年更新 (OP41)](https://conf.cwb.gov.tw/media/cwb_past_conferences/106/2017_ppt/A2/A2-26-中央氣象局區域模式2017年更新_陳依涵.pdf)，中央氣象局氣象資訊中心
- 風場範例如MeteoInfo圖，在島內範圍有較高的解析度。

| ![unresp3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp3.png)|
|:--:|
| <b>CWB WRF 模式3KM預報結果風場</b>|

### 氣象與空品模式的模擬範圍與解析度之決定
- WRF 3KM雖然模擬範圍東西有較大的跨距（如圖），但對於空品模式（煙流可能影響範圍）而言，並無必要。
### 自動下載
- 自動下載我國中央氣象局（CWB）數值預報（WRF）結果，並進行解讀。
  - CWB會員登錄、檔案網址之定位與確認
  - CWB要求先成為會員，才允許進行下載。
  - 其會員帳號為電子郵件、密碼為包括大小寫、數字、特殊字元（shift 1～0）
- 檔案網址的資訊，寫在`xml`檔案內容內，範例如下：
  - 2021/10/12前舊址：
    - `https://opendata.cwb.gov.tw/fileapi/opendata/MIC/M-A006${dom}-0$i.grb2`
  - 新址：
    - `https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MIC/M-A006${dom}-0$i.grb2`
    - 舊版`wget`(1.12)會需要加上選項`--no-check-certificate`
- [公開資料內容項目](https://opendata.cwb.gov.tw/opendatadoc/MIC/A0061.pdf)

| ![unresp4.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp4.png)|![unresp5.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp5.png)|
|:--:|:--:|
| <b>CWB_WRF 3維變數之高度分布</b>|<b>CWB_WRF數值預報地面項目</b>|	


- 自動下載與儲存空間之預備
	- Bash 中使用for 即可，但在間隔的設定上，centos和MacOS有所差異，前者可以接受{00..84..06}，後者不能接受數字及文字混用。
	- 解決方式，直接將 15個小時數寫出來：
```bash  
for i in 000 006 012 018 024 030 036 042 048 054 060 066 072 078 084 ;do
  wget https://opendata.cwb.gov.tw/fileapi/opendata/MIC/M-A0064-$i.grb2
done
```  
- 美國MAM預報內容與台灣WRF模式預報內容的差異與對照、
	- GRIB2 格式可以用wgrib2程式進行解讀
	- 也可以轉成nc檔案，用python來解讀
	- convert2nc必須在 ncl_stable 環境中運作，參[bairdlangenbrunner.github.io](https://bairdlangenbrunner.github.io/python-for-climate-scientists/conda/setting-up-conda-environments.html)
	- 經比較結果，只有格點的經緯度變數名稱不同，前者為lat/lon、後者為gridlat_0/gridlon_0，在Create3DDAT.py之前須先準備好內容。
- 格點lat/lon之讀取
  - 先將GRIB轉成NC格式

```bash
conda activate ncl_stable
convert2nc M-A0064-000.grb2
  Python nc2db.py#將每一個格點的座標寫成csv檔案。
```
### nc2db.py內容

```python  
import netCDF4
from pandas import *
import argparse
import numpy as np
parser = argparse.ArgumentParser(description="read NetCDF data and transform to DataFrame csvs. ",\
   epilog="Example of use: pythonb nc2df NC_FILENAME")
parser.add_argument("nc_filename", help="nc filebname",type=str)
args = parser.parse_args()
fname = args.nc_filename
nc = netCDF4.Dataset(fname)
cols=list(nc.variables)           #note 1
d={}
for c in ['gridlon_0','gridlat_0']:
    a=list(np.array(nc.variables[c]).flatten())           #note 3
    d.update({c: a})
df=DataFrame(d)
df.to_csv(fname+'.csv')
```
- 路徑檔名存成：data/M-A0064.nc2.csv
- 檔案大小
  - 一個grb2檔案大小約183~187MB，1天份共15個檔案計3.1G
  - 一天圖檔共約360M。

## Create3DDAT.py的安裝與修改
### Python環境之設定（內設為3.6版）
  - `conda env create -f environment.yml`
- Centos 6執行安裝並無困難，也可順利執行
- Mac上執行有困難
  - Gcc/gfortran/c++等無法安裝指定的版本
  - 將yml檔案內相對應的指標去掉，雖可通過，但執行仍然有誤，swig無法
  `import ModuleNotFoundError: No module named '_gribapi_swig'`
  - 解決方式：將環境套件整體升級到py37之gribby
	  - `conda create -n gribby -c conda-forge python-eccodes`
	  - (Grib2 with python 3.7)
	  - see [stackoverflow](https://stackoverflow.com/questions/39787578/importerror-when-using-python-anaconda-package-grib-api)      

### 模擬範圍之選取
- 濃度場的模擬範圍、輸出入檔的目錄位置、高度氣壓座標
- 程式差異

```bash  
193,200c197,206
< latMinCP = 11.7  # Min lat of CALPUFF grid
< latMaxCP = 12.2  # Max lat of CALPUFF grid
< lonMinCP = 273.2  # Min lon of CALPUFF grid
< lonMaxCP = 274.1  # Max lon of CALPUFF grid
< inDir = '../NAM_data/raw/'+date  # Directory containing GRIB files
< nfiles = 17 #Number of GRIB files (files are 3 hourly, so 48 hours is 17 files including hours 0 and 48)
< outFile = '../NAM_data/processed/met_'+date+'.dat' #Output file path
< levsIncl = [1000,950,925,900,850,800,700,600,500,400,300,250,200,150,100,75,50,30,20,10,7,5,2] #pressure levels to include in output
---
> latMinCP = 21.4    # Min lat of CALPUFF grid
> latMaxCP = 25.7   # Max lat of CALPUFF grid
> lonMinCP = 119.4   # Min lon of CALPUFF grid
> lonMaxCP = 122.4   # Max lon of CALPUFF grid
> inDir =  '/home/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/raw/'+date  # Directory containing GRIB files
> nfiles = 15 #Number of GRIB files (files are 6 hourly, so 84 hours is 15 files including hours 0 and 48)
> outFile ='/home/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/processed/met_'+date+'.dat' #Output file path
> if os.path.isfile(outFile):
>     sys.exit('exist outFile: '+outFile)
> levsIncl = [1000,925,850,700,500,400,300,250,200,150,100] #pressure levels to include in output
```
### 座標系統的調整轉換（經緯度twd97 VS LCP）
-  原程式是以gribapi模組中的grib_get_array來解讀格點經緯度與格點數，解讀的對象是任意的2維變數(如海平面氣壓PRMSL)
- 求取不同經緯度：適用在以經緯度為座標軸的等度數網格系統
- 然在小範圍的空品模式模擬一般是以等距離、正交之直角座標系統，其座標點的經、緯度將會是2個2維陣列
- 由於格點位置及格點數並不會每一次改變，由固定檔案來提供似乎比較單純合理。(csv檔詳前述[nc2db.py](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/Forecast/#nc2dbpy內容)。修改程式gribapi似更複雜)

```bash
< lats = gribapi.grib_get_array(gidPRMSL,'distinctLatitudes')
< lons = gribapi.grib_get_array(gidPRMSL,'distinctLongitudes')
< Ni = gribapi.grib_get(gidPRMSL,'Ni')
< Nj = gribapi.grib_get(gidPRMSL,'Nj')
---
> ishp=2
> CSV='/home/kuang/MyPrograms/UNRESPForecastingSystem/data/M-A0064nc2.csv'
> df=read_csv(CSV)
> #lats = gribapi.grib_get_array(gidPRMSL,'distinctygrid')#Latitudes')
> #lons = gribapi.grib_get_array(gidPRMSL,'distinctLongitudes')
> lats = np.array(list(df.gridlat_0))
> lons = np.array(list(df.gridlon_0))
> Ni = 1158
> Nj = 673
```
### 濃度場模擬範圍在氣象場中相對位置與切割
-  原來的網格是等間距經緯度系統，因此網格對照過程是1維線性切割、四角經緯度只是其向量中之某一值
-  而在直角座標中4角落的定位，也只需按照最接近該4點位置的網格點決定之。
```bash
< for i in range(len(lats)-1):
<     if lats[i+1] >= latMinCP:
<         iLatMinGRIB=i
<         break
< for i in range(len(lats)-1):
<     if lats[i+1] > latMaxCP:
<         iLatMaxGRIB=i+1
<         break
< for i in range(len(lons)-1):
<     if lons[i+1] >= lonMinCP:
<         iLonMinGRIB=i
<         break
< for i in range(len(lons)-1):
<     if lons[i+1] > lonMaxCP:
<         iLonMaxGRIB=i+1
<         break
---
> XY=np.array([twd97.fromwgs84(i,j) for i,j in zip(lats,lons)],dtype=int)
> twd97X,twd97Y=(XY[:,i] for i in [0,1])
          > XminCP,YminCP=(int(i) for i in twd97.fromwgs84(latMinCP,lonMinCP))
> XmaxCP,YmaxCP=(int(i) for i in twd97.fromwgs84(latMaxCP,lonMaxCP))
> DIST =(twd97X-XminCP)**2+(twd97Y-YminCP)**2
> minD=min(DIST)
> ji=list(DIST).index(minD)
> ijLLMinGRIB = ji
> iLatMinGRIB = int(ji/Ni)
> iLonMinGRIB = ji - Ni * iLatMinGRIB
> DIST =(twd97X-XmaxCP)**2+(twd97Y-YmaxCP)**2
> minD=min(DIST)
> ji=list(DIST).index(minD)
> ijLLMaxGRIB = ji
> iLatMaxGRIB = int(ji/Ni)
> iLonMaxGRIB = ji - Ni * iLatMaxGRIB
```

### 格點座標值由1維增加為(實質)2維

```bash
78,81c80,83
<     RXMIN = lons[iLonMinGRIB]  # W-most E longitude
<     RXMAX = lons[iLonMaxGRIB]  # E-most E longitude
<     RYMIN = lats[iLatMinGRIB]  # S-most N latitude
<     RYMAX = lats[iLatMaxGRIB]  # N-most N latitude
---
>     RXMIN = lons[ijLLMinGRIB]  # W-most E longitude
>     RXMAX = lons[ijLLMaxGRIB]  # E-most E longitude
>     RYMIN = lats[ijLLMinGRIB]  # S-most N latitude
>     RYMAX = lats[ijLLMaxGRIB]  # N-most N latitude
97c99
<         XLATDOT = lats[iLatMinGRIB+j]  # N latitude of grid point
---
>         XLATDOT = lats[ijLLMinGRIB+j*Ni]  # N latitude of grid point
100c102
<             XLONGDOT = lons[iLonMinGRIB+i]  # E longitude of grid point
---
>             XLONGDOT = lons[ijLLMinGRIB+i]  # E longitude of grid point
```

### 檔案名稱系統
- 舊檔名系統是逐3小時。修改為6小時間隔之檔名系統。
```bash
< filePrefix = 'nam.t00z.afwaca'
< fileSuffix = '.tm00.grib2'
---
> filePrefix = 'M-A0064-0'
> fileSuffix = '.grb2'
209c215
<     filenames.append(filePrefix+'{:02d}'.format(i*3)+fileSuffix)
---
>     filenames.append(filePrefix+'{:02d}'.format((i)*6)+fileSuffix)
```

## 即時排放數據
### 數據來源及處理
- 臺灣地區最大型的點污染源非火力發電機組莫屬。由於臺灣天然資源缺乏，又因地狹人稠不適發展核能發電，因此火力發電佔了發電量的大宗。目前即時運轉與排放等相關訊息包括：
	- 各發電機組發電量(運轉率)即時資訊。已經在[opendata網站](https://data.gov.tw/dataset/8931)公開，每分鐘更新，除此之外，
	- 亦有每分鐘[CEMS數據](https://data.gov.tw/dataset/31969)
- 如何引用相關考慮條列如下

|項目|發電量即時資訊|CEMS數據|選擇考量|
|-|-|-|-|
|污染源完整性|所有發電機組都有|有的污染源沒有(可能因為規模太小未列管)|沒有數據就無從推估|
|污染項目|無(只有**運轉率**%)|煙氣流量、溫度、SOX、NOX及不透光率|後者太過複雜還有待QCQA|
|時間頻率|10min|15min|此處作業只需要逐時|
|資料穩定性|穩定|不甚穩定(CEMS允許一定時數之離線)||

- 有鑒於數據的涵概面及穩定性，此處選則以**運轉率**進行排放推估。
	- 排放量 = 2019 [TEDS11資料庫]((https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx))中之小時排放 &times; 該小時平均**運轉率**
	- 污染物：適用TEDS資料庫中所有排放項目(PM<sub>2.5</sub>、PM<sub>10</sub>)
	- 煙氣量：*CALPUFF* 可以接受逐時的排氣速度，也是平均值乘上**運轉率**得之
- 數據時間點：
	- 由於預報自前一日開始，因此排放數據也引用前一日之24小時數據
	- 預報期間排放量：假設與前一日24小時相同，不做修正預報。

### 前日運轉率之彙整與應用
- 逐時*wget*下載前述[opendata運轉率數據](https://data.gov.tw/dataset/8931)存檔備用
- 逐日(*crontab*控制凌晨運作)將前一日所有24小時檔案合併彙整。
	- 每日運轉的機組數可能會有差異，*calpuff* 不允許排放量全為0的狀況，同時也非常耗費模式計算時間，因此需將未運轉的污染源予以剔除。
- 開啟檔案：names.csv
	- 檔頭 `CP_NO,C_NO,All_In_One,CO_GPS,DIA,EnergyForm,HEI,NMHC_GPS,NOX_GPS,NO_S,PM25_GPS,PM_GPS,PlantName,`
	`SOX_GPS,SUM_EMI,TEMP,UnitName,VEL,UTM_N,UTM_E`
	- 分別是`管編+煙道(**管煙**)、管編、集合否(T/F)、CO、DIA、發電形態、煙囪高、NMHC、NOX、管道編號、PM25、PM、廠名、SOX、總量、溫度、機組名稱、流速、座標`
		- 由於部分電廠以所有機組陳報，其運轉率只有一個，All_In_One會是True，按照過去該廠排放量之分布，正比分配到每一個污染源。
	-	此一檔案為[TEDS11]((https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx))之小時排放率(全年總量/總運轉時數)，排放單位為g/s
	- 流速單位為m/s，為最大排氣量計算而得
- 輸出排放量檔案(檔名字頭為'g')，範例如下。此檔案有24小時序列。
	- **管煙**、溫度、流速(已經乘上運轉率)、各污染物之g/s排放量、時間標籤

```
$ head g20220412.csv
CP_NO,TEMP,VEL,CO_GPS,NMHC_GPS,NOX_GPS,PM25_GPS,PM_GPS,SOX_GPS,DateHr
F1700736P601,114,16.57785,0.0,0.0,21.48246822694089,1.1103541221509972,1.882682180377493,19.653922323336385,2022041200
F1700736P701,108,16.575588,0.0,0.0,16.499618542048232,1.1976660590277777,2.0307950954861114,12.677973511904762,2022041200
```
- 輸出排放量檔案(檔名字頭為'p')，範例如下。此檔將在逐時排放量之檔頭
	- **管煙**、高度、內徑、溫度、流速(最大值)、座標值

```
kuang@master /home/sespub/power
$ head p20220412.csv
CP_NO,HEI,DIA,TEMP,VEL,UTM_E,UTM_N
C1400170P301,202.0,6.4,127,20.0,321548.0,2777220.0
C1400170P401,205.0,6.4,118,20.0,321548.0,2777220.0
E5400878P001,60.0,6.2,150,9.1,180595.0,2503815.0
```
- 彙整前日24小時之程式(在Run.sh內每日執行)

```python
kuang@master /home/sespub/power
$ cat rd_today.py
#!/cluster/miniconda/envs/unresp/bin/python
from pandas import *
import subprocess, os
from pypinyin import pinyin, lazy_pinyin
cole=['CO_EMI', 'NMHC_EMI', 'NOX_EMI', 'PM25_EMI', 'PM_EMI', 'SOX_EMI']
colg=[i.replace('EMI','GPS') for i in cole]
hdtv=[ 'HEI', 'DIA', 'TEMP', 'VEL']

date=subprocess.check_output('date -d "-1 day" +%Y%m%d',shell=True).decode('utf8').strip('\n')
df=read_csv('names.csv')
unit2={}
col=['CP_NO']+hdtv+colg
for c in col:
  dd= {i:j for i,j in zip(list(df.UnitName),list(df[c]))}
  unit2.update({c:dd})

td=DataFrame({})
for t in range(24):
  tt='{:02d}'.format(t)
  fname='b'+date+tt+'.txt'
  if not os.path.exists(fname):continue
  with open(fname,'r') as f:
    lines=[i.strip('\n') for i in f]
  a=[i.split(',')[2] for i in lines[1:]]
  b=[]
  for i in a:
    ll=lazy_pinyin(i)
    s=''
    for ii in ll:
        s+=ii
    b.append(s)
  perc=[i.split(',')[5] for i in lines[1:] ]
  dft=DataFrame({'Name':b,'Perc':perc})
  dft=dft.loc[dft.Name.map(lambda x:x in set(df.UnitName))].reset_index(drop=True)
  dft.Perc=[float(i[:-1])/100. for i in dft.Perc]
  dft['DateHr']=[date+tt for i in range(len(dft))]
  dft['CP_NO']=[unit2['CP_NO'][i] for i in dft.Name]
  dft=dft.loc[dft.Perc>0]
  td=td.append(dft,ignore_index=True)
for c in colg:
  c0=np.array([unit2[c][i] for i in td.Name])
  td[c]=c0*td.Perc
for c in hdtv:
  c0=np.array([unit2[c][i] for i in td.Name])
  if c=='VEL':
    td[c]=c0*td.Perc
  else:
    td[c]=c0
td[col[:1]+col[3:]+['DateHr']].set_index('CP_NO').to_csv('g'+date+'.csv')

df=read_csv('names.csv')
df=df.loc[df.CP_NO.map(lambda x:x in set(td.CP_NO))].reset_index(drop=True)
df[col[:5]+['UTM_E','UTM_N']].set_index('CP_NO').to_csv('p'+date+'.csv')
```

### *CALPUFF*逐時排放量檔案之準備
- *CALPUFF* 允許輸入逐時之排放量，由外部檔案提供，calpuff.inp內只需對點源個數、排放量檔案名稱等予以率定。
- 產生程式
	- 目前仍以舊的[fortran檔案](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/ptem_PWR.f)先暫代之
	- 該程式會讀取命令列輸入的3個日期，分別開啟前述p與g開頭的2個逐日檔案、輸出所需之起迄時間範圍的逐時排放量檔案。
- calpuff.inp內
	- 逐時排放量檔案名稱為固定值：ptemarb_pwr.dat
	- NPT2為變數，每日以*sed*指令進行更換
- [Run.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/Run.sh)相關的內容

```bash
...
echo ${rundate} ${prevdate} ${enddate}> ptem_PWR.inp
/home/cpuff/2018/ptem/ptem_PWR<ptem_PWR.inp
if ! [ -e ptemarb_pwr.dat ]; then echo -n "fail ptemarb_PWR !";exit 0;fi
NPT2=$(head -n11 ptemarb_pwr.dat|tail -n1| awk '{print $1}')
...
  sed   -e ...
        -e "s/?NPT2?/$NPT2/g"  \
    ./CALPUFF_INP/calpuff_template.inp > ./CALPUFF_INP/calpuff.inp
```
## *CALPUFF*系統的更新
### *CALMET*模式的偵錯
1. Fortran程式編譯（內設使用ifort、gfortran版本的差異）
	- dec舊式fortran可以接受未定寬度的輸出格式，如(i)、(f)等
	- 如`read(cfver,'(f)') cfdataset`
	- ifort/pgi皆可接受，但gfortran無法接受
	  - 過去可以使用-fdec-format-defaults選項控制，但新版gfortran已經取消這個選項，不能接受未定寬度的輸出格式，詳[gcc官網](https://gcc.gnu.org/onlinedocs/gfortran/Fortran-Dialect-Options.html)
	  - 解決方法：因錯誤並不多，直接將程式碼中未定長度格式，改成自由格式(*)
2. 輸入資料間隔(nlevag11)6小時程式的偵錯
- 基本版本：CALMET_v6.5.0_L150223
- ifort 新舊版本的差異

```bash
(unresp)
kuang@master /cluster/CALPUFF6/CALMET
$ diff CALMET_v6.5.0_L150223/CALMET.FOR new/calmet.for
21043c21045
<       save it1,it2,isec1,isec2
---
>       save it1,it2,isec1,isec2,nlevag11
```    
- mac gfortran與centos6 gfortran的差異

```bash
kuang@master ~/MyPrograms/UNRESPForecastingSystem/CALPUFF_MODS/CALMET
$ diff calmet.for /cluster/CALPUFF6/CALMET/new/calmet.for
21045c21045
<       save it1,it2,isec1,isec2,nlevag1,msec
---
>       save it1,it2,isec1,isec2,nlevag11
```

### *CALPUFF*模式輸出的修改
1. Fortran程式編譯（內設使用ifort、gfortran版本的差異）
	- 與前述*CALMET*相同，也具有未定寬度的輸出格式的問題
		- dec舊式fortran可以接受未定寬度的輸出格式，如(i)、(f)等
		- in readcf.f and runsize.f 
	  `read(cfver,'(f)') cfdataset`
	- 解決方法：直接將未定長度格式改成自由格式(*)
2. calpuff.inp中離散點的設定
	- 研究團隊並沒有使用CALPOST做為後處理程式，而是利用CALPUFF模式逐時輸出離散點濃度的做法，將各污染物的逐時濃度逐一開啟檔案輸出。
	- CALPUFF.INP須輸入所有接受點的總數，以及各點的座標(LCP)，
	- 先由前述csv檔讀入lat/lon值，經由twd97模組將經緯度轉成twd97座標，扣除Xcent、Ycent之offset即成為LCP座標
	- *CALPUFF*為KM單位
	- 檔案另輸出成data/xy_taiwan3.dat

```python	
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
```		

3. output.f 離散點之輸出

```bash
$ diff CALPUFF_v7.2.1_L150618/output.f new/output.f
125a126
>       character*150 infile
373a375,392
> c--------------------------------------------------------------
> ckuang
> c --- Sara 08/10/2004: Just to have an output of the concentration
> c --- directly readable.
> c --- Concentration in g/m^3 is written for each receptor
>             do ispec=1,nspec
>               write(infile,10000) ispec, istep
> c     &                     I2.2,I4.4,'.vtk')
> 10000         format('concrec',I2.2,I4.4,'.dat')
> c             print *, nspec,',',ispec,',',nn,',',infile,',',
> c     +       nrec,',',chirec(1,ispec)
>               open(50,file=infile)
>               do i=1,nrec
>                 write(50,*) chirec(i,ispec)
>               end do
>               close(50)
>             end do
``` 
4. PM<sub>2.5</sub> 的計算（結合銨鹽重量的計算）
	- CALPUFF之CSPEC共有8種，利用其中的成份計算總PM<sub>2.5</sub>，包括結合銨鹽
	- 以DataFrame架構整理檔案名稱(spec, hour)，再讀入個別檔案的內容成為3維矩陣C。
	- 輸出檔案為00-hhhh.dat。
	- 程式下載點[conc2pm25.py](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/conc2pm25.py)

```python
kuang@master ~/MyPrograms/UNRESPForecastingSystem/Python
$ cat conc2pm25.py
import numpy as np
import os,sys,subprocess
from pandas import *
CSPEC='SO2 SO4 NOX HNO3 NO3 PMS1 PMS2 PMS3'.split()
fnames=list(subprocess.check_output('ls concrec*dat',shell=True).split(b'\n'))
fnames=[i.decode('utf8') for i in fnames if len(i)>0 ]
if len(fnames)==0:sys.exit('concrec not found')
wc=int(subprocess.check_output('cat '+fnames[0]+'|wc -l',shell=True).split(b'\n')[0])
jt=[int(fname.split('/')[-1].replace('.dat','')[-4:]) for fname in fnames if len(fname)>0]
js=[int(fname.split('/')[-1].replace('.dat','')[-6:-4]) for fname in fnames if len(fname)>0]
df=DataFrame({'hr':jt,'spec':js,'fname':fnames})
df=df.loc[df.spec>0].reset_index(drop=True)
C=np.zeros(shape=(max(js)+1,max(jt)+1,wc))
for i in range(len(df)):
  with open(df.loc[i,'fname'],'r') as f:
    tmp=[float(l.strip('\n')) for l in f]
  C[df.loc[i,'spec'],df.loc[i,'hr'],:]=tmp[:]
so4 =C[1,:,:]
hno3=C[3,:,:]
no3 =C[4,:,:]
p25 =C[5,:,:]
nh4=so4*(36./96.)+no3*(18./62.)+hno3*(18./63.)
total=so4+no3+hno3+nh4+p25
fnRoot=fnames[0].replace('.dat','')[:-6]+'00'
for it in range(1,max(jt)+1):
  fname=fnRoot+'{:04d}'.format(it)+'.dat'
  with open(fname,'w') as f:
    for ic in range(wc):
      f.write(str(total[it,ic])+'\n')
```
## 等濃度圖與網站設定(格柵底圖方案)
- 模擬污染物項目、小時數、動畫、濃度等級的修改，
### Python/genmaps.py
-  主要修改污染物項目，
-  由SO<sub>2</sub>/SO<sub>4</sub>→PM<sub>2.5</sub>/NOX/SO<sub>2</sub>/SO<sub>4</sub>等四項，
-  成份變數SOX→SPEC
-  檔案個數(總時數)
```bash  
100c109
<     nconc = 48
---
>     nconc = 83
```    
### Python/maptoolkit.py
-  除上述污染項目之外，尚有：
  - 指定PMF及NOX concrec的file name前2碼
  - 座標系統的計算方式

```bash
32d31
< import utm
35a35,36
> import twd97
123,128c128,131
>     Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
>     Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
>     ll = np.array([twd97.towgs84(i*1000+Xcent,j*1000+Ycent) for i, j in zip(x, y)])
>     lat, lon = (ll[:, i] for i in [0, 1])
166,169c169,172
>     Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
>     Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
>     ll = np.array([twd97.towgs84(i*1000+Xcent,j*1000+Ycent) for i, j in zip(x2, y2)])
>     lat, lon = (ll[:, i] for i in [0, 1])
```
- 濃度等級(ug/m<sup>3</sup>)

```bash
273,274c276,277
<         self.binLims = [10, 350, 600, 2600, 9000, 14000]  # SO2 bin limits
<         self.binLimsSO4 = [1E-8, 12, 35, 55, 150, 250]  # SO4 bin limits from:
---
>         self.binLims = [1E-3,1E-2,1,5, 10, 350]  # SO2 bin limits
>         self.binLimsSO4 = [1E-3, 1E-2,1E-1, 1, 5, 15]  # SO4 bin limits from:
```
- XYFILE:xy_masaya.da→xy_taiwan3.dat
- 圖框之tic

```bash
399,400c403,404
>         latTicks = np.arange(round(latMin, 1), round(latMax, 1) + 0.1, 0.5)
>         lonTicks = np.arange(round(lonMin, 1), round(lonMax, 1) + 0.1, 0.5)
```
- 指定外部IP（內設是本機）
- 網址：http://200.200.12.191:8030/UNRESP_VIZ/index.html

```bash
cd /home/cpuff/UNRESPForecastingSystem/VIZ_SITE_CODE/public_html
/cluster/anaconda3/bin/python3.7/python -m http.server --bind 200.200.12.191 8030 >&/dev/null &
```

## VERDI向量底圖方案
### 向量底圖
- 前述格柵底圖結果檔案過於龐大(84小時的gif檔約80\~150MB)，終究拖累網站而告失敗。
- 解決方案就是以VERDI批次作業，以向量底圖來降低檔案容量。過程與設定可以詳見[程式外批次檔(CALPUFF結果時間序列圖檔展示)](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_batch/#程式外批次檔CALPUFF結果時間序列圖檔展示)的說明。
- 向量底圖採五都升等前的縣市界線，對污染集中的範圍有較多的空間資訊。
- 結果
	- [PMF.gif](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/PMF.gif)，檔案大小約6\~7MB
	- 外部網址
		- [https://sinotec2.github.io/cpuff_forecast](https://sinotec2.github.io/cpuff_forecast/index.html)(較快)
		-	[http://114.32.164.198/LC-GIF-Player/demo.html](http://114.32.164.198/LC-GIF-Player/demo.html)(較慢)
	- 內部網址：[http://200.200.12.191/LC-GIF-Player/demo.html](http://200.200.12.191/LC-GIF-Player/demo.html)(最快)


### 網站與播放器
- 不論python網站方案、或是瀏覽器內設GIF播放器方案，不是相容性較低、要平移到不同平台的衝突較大，就是控制程度較低，不能暫停、前後微調、放大等等。都需要進一步改善。
- 播放器修改過程及成果詳見[]()說明

- 參考網友[sexyoung](https://medium.com/進擊的-git-git-git/從零開始-用github-pages-上傳靜態網站-fa2ae83e6276)的指引，將網站平移到github.io ([https://sinotec2.github.io/cpuff_forecast](https://sinotec2.github.io/cpuff_forecast/index.html))，並且使用*git*指令[每日更新](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/git/#定期上載)，可以大幅降低對家用電腦頻寬的佔用，並且開放服務時間到24-7-365。
## Download Run.sh
- github: [Run.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPUFF/Run.sh)
## TODO
1. crontab自動每天執行(已完成)
1. 解決自動下載問題(Today目錄下檔案多達366MB)。
	1. 掛網、加速網站速度流量：委託專業網址。
	1. 降低圖檔容量：不論背景是topo或者是衛星照片，單一jpg檔案均為0.7~1.2M，如僅有縣市界線應可有效降低。
	1. (已使用[VERDI批次檔案](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_batch/#程式外批次檔calpuff結果時間序列圖檔展示)解決)
2. 點、線、面源模擬分析
3. 重要點污染源分析
	1. (已採用opendata之所有火力發電機組運轉實況數據)
4. 測站時間序列
6. 臭氧煙陣軌跡
7. 縮小範圍、增加污染源
8. 教學用

## Reference
- cemac, [UNRESPForecastingSystem on GitHub](https://github.com/cemac/UNRESPForecastingSystem), last modifed on 30 Sep 2021.
- sexyoung, [從零開始-用github-pages-上傳靜態網站](https://medium.com/進擊的-git-git-git/從零開始-用github-pages-上傳靜態網站-fa2ae83e6276), Sep 4, 2017
- 陳依涵、戴俐卉、賴曉薇、陳怡儒、林伯勳、黃小玲、江琇瑛、江晉孝、陳白榆、洪景山、馮欽賜（2017）[中央氣象局區域模式2017 年更新 (OP41)](https://conf.cwb.gov.tw/media/cwb_past_conferences/106/2017_ppt/A2/A2-26-中央氣象局區域模式2017年更新_陳依涵.pdf)，中央氣象局氣象資訊中心

