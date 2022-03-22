---
layout: default
title: 濃度預報系統之實現
nav_order: 3
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
---
# CALPUFF濃度預報系統之實現
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
Leed大學CEMAC中心建置了Masaya 火山噴發SO2/SO4造成地面濃度的預報模式，範例如圖所示。由於氣象預報數據、大氣擴散模式等皆為官方作業系統與優選模式，因此具有高度的參考價值。

此處將其進行本土化，應用於緊急應變作業系統中。改系統自動下載未來48小時MAM氣象數值預報的結果，轉成CALMET的輸入檔，進入CALPUFF模式進行地面空氣品質的模擬，由於CALPUFF模式具有考慮3D風場、地形變化、化學反應等模擬能力，為美國環保署列為大氣擴散中的優選模式，用於大型固定污染源原生污染物以及二次氣膠長程傳輸的模式。

## 挑戰任務
系統工作流程由Run.sh批次檔所控制，重要節點及困難如下：
1. 自動下載我國中央氣象局（CWB）數值預報（WRF）結果，並進行解讀。
	1. CWB會員登錄、檔案網址之定位與確認
	2. 氣象與空品模式的模擬範圍與解析度之決定
	3. 自動下載與儲存空間之預備
	4. 美國MAM預報內容與台灣WRF模式預報內容的差異與對照、
2. 解讀程式（Create3DDAT.py）的安裝與修改
	1. Python環境之設定（內設為3.6版）
	2. grib-api模組之安裝（wasg不能import的問題）
	3. 座標系統的調整轉換（經緯度twd97 VS LCP）
3. CALMET模式的偵錯
	1. Fortran程式編譯（內設使用ifort、gfortran版本的差異）
	2. 輸入資料間隔6小時程式的偵錯
4. CALPUFF模式輸出的修改
	1. Calpuff.inp中離散點的設定
	2. output.f 離散點之輸出
	3. PM2.5 的計算（結合銨鹽重量的計算）
5. 等濃度圖與網站設定
	1. 模擬污染物項目、小時數、動畫、濃度等級的修改
	2. 指定外部IP（內設是本機）

## 執行方式
1. 切換目錄到UNRESPForcastingSystem
2. 編輯Run.sh打開要執行的程式

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
 
## 排放位置等參數之改變
1. 檔案模板：
2. 修改位置
	- 模式採用Lambert 投影座標系統，原點位在台灣中心點，北緯24.61，東經120.99.
	- (Taizhong PP)<    1 ! X =  -49.873, 63.288,  150,      4.7,    11.00,  19.8, 363.0,   .0,   5.440,
	- (Tongxiao PP)>    1 ! X =  -32.064, 97.505,  150,      4.7,    11.00,  19.8, 363.0,   .0,   5.440,

## 成果比較
- https://homepages.see.leeds.ac.uk/~earunres/
- http://114.32.164.198:8000/UNRESP_VIZ/index.html?v=1

| ![unresp1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp1.png)|
| <b>leed大學火山SO2預報結果畫面</b>|
|:--:|
|![unresp2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp2.png)|
| <b>台中電廠PM2.5預報結果畫面</b>|

## 氣象數據下載與解讀
- 氣象數值預報的選擇
  - 雖然國際間公開的數值預報成果有很多，覆蓋台灣地區範圍也不在少數，然而經比較其解析度不足以模擬大型固定源，且對局部地形及海陸風現象亦不足以解析。
  - 經比較分析選擇以CWB WRF 模式3KM模擬結果最為恰當。
  - CWB WRF 3KM預報的作業方式、演進與評估，可以參考
    - [20161005_高解析區域模式預報系統之發展](http://photino.cwb.gov.tw/conf/history/105/2016_ppt_all/Session/Session6/6-2-20161005_高解析區域模式預報系統之發展.pdf)
    - 陳依涵、戴俐卉、賴曉薇、陳怡儒、林伯勳、黃小玲、江琇瑛、江晉孝、陳白榆、洪景山、馮欽賜（2017）[中央氣象局區域模式2017 年更新 (OP41)](https://conf.cwb.gov.tw/media/cwb_past_conferences/106/2017_ppt/A2/A2-26-中央氣象局區域模式2017年更新_陳依涵.pdf)，中央氣象局氣象資訊中心
- 風場範例如MeteoInfo圖，在島內範圍有較高的解析度。

| ![unresp3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/unresp3.png)|
|:--:|
| <b>CWB WRF 模式3KM預報結果風場</b>|

- 氣象與空品模式的模擬範圍與解析度之決定
  - WRF 3KM雖然模擬範圍東西有較大的跨距（如圖），但對於空品模式（煙流可能影響範圍）而言，並無必要。
- 自動下載我國中央氣象局（CWB）數值預報（WRF）結果，並進行解讀。
  - CWB會員登錄、檔案網址之定位與確認
  - CWB要求先成為會員，才允許進行下載。
  - 其會員帳號為電子郵件、秘密為包括大小寫、數字、特殊字元（shift 1～0）
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
	- Bash 中使用for 即可，但在間隔的設定上，centos和MacOS有所差異，前者可以接受{00.84..06}，後者不能接受數字及文字混用。
	- 解決方式，直接將 15個小時數寫出來：
```bash  
for i in 000 006 012 018 024 030 036 042 048 054 060 066 072 078 084 ;do
  wget     https://opendata.cwb.gov.tw/fileapi/opendata/MIC/M-A0064-$i.grb2;done
```  
- 美國MAM預報內容與台灣WRF模式預報內容的差異與對照、
	- GRIB2 格式可以用wgrib2程式進行解讀
	- 也可以轉成nc檔案，用python來解讀
	- convert2nc必須在 ncl_stable 環境中運作
	- https://bairdlangenbrunner.github.io/python-for-climate-scientists/conda/setting-up-conda-environments.html
	- 經比較結果，只有格點的經緯度變數名稱不同，前者為lat/lon、後者為gridlat_0/gridlon_0，在Create3DDAT.py之前須先準備好內容。
- 格點lat/lon之讀取
  - 先將GRIB轉成NC格式

```bash
conda activate ncl_stable
convert2nc M-A0064-000.grb2
  Python nc2db.py#將每一個格點的座標寫成csv檔案。
```
- nc2db.py內容

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
  - 一個grb2檔案大小約183~187MB,15個檔案（1天分）約3.1G
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
- 然在小範圍模擬一般是以等距離、正交之直角座標系統，其座標點的經緯度將會是2個2維陣列
-  由於格點位置及格點數並無會每一次不一樣，由固定的一個檔來提供似乎比較單純合理。(修改程式gribapi似更複雜)

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
-  原來的網格是等間距經緯度系統，因此其取網格是1維線性切割、四角經緯度為其向量中之某一值
-  直角座標4角經緯度，為所有點中，最接近該4點位置的點座標中得知。
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
- 舊檔名系統是逐3小時。修改為6小時間隔之˙檔名系統。
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
## CALMET模式的偵錯
1. Fortran程式編譯（內設使用ifort、gfortran版本的差異）
	- dec舊式fortran可以接受未定寬度的輸出格式，如(i)、(f)等
	  read(cfver,'(f)') cfdataset
	  ifort/pgi皆可接受，但gfortran無法接受
	  使用-fdec-format-defaults新版gfortran不能接受
	- 解決方法：直接將未定長度格式改成自由格式(*)
2. 輸入資料間隔6小時程式的偵錯
- 基本版本：CALMET_v6.5.0_L150223
- ifort 與centos6 的差異
		(unresp)
		kuang@master /cluster/CALPUFF6/CALMET
		$ diff CALMET_v6.5.0_L150223/CALMET.FOR new/calmet.for
		21043c21045
		<       save it1,it2,isec1,isec2
		---
		>       save it1,it2,isec1,isec2,nlevag11
- mac gfortran與centos6 gfortran的差異
		kuang@master ~/MyPrograms/UNRESPForecastingSystem/CALPUFF_MODS/CALMET
		$ diff calmet.for /cluster/CALPUFF6/CALMET/new/calmet.for
		21045c21045
		<       save it1,it2,isec1,isec2,nlevag1,msec
		---
		>       save it1,it2,isec1,isec2,nlevag11
		
CALPUFF模式輸出的修改
1. Fortran程式編譯（內設使用ifort、gfortran版本的差異）
	- dec舊式fortran可以接受未定寬度的輸出格式，如(i)、(f)等 in readcf.f and runsize.f 
	  read(cfver,'(f)') cfdataset
	  ifort/pgi皆可接受，但gfortran無法接受
	  使用-fdec-format-defaults新版gfortran不能接受(https://gcc.gnu.org/onlinedocs/gfortran/Fortran-Dialect-Options.html )
	- 解決方法：直接將未定長度格式改成自由格式(*)
2. Calpuff.inp中離散點的設定
	- 研究團隊並沒有使用CALPOST做為後處理程式，而是利用CALPUFF模式逐時輸出離散點濃度的做法，將各污染物的逐時濃度逐一開啟檔案輸出。
	- CALPUFF.INP須輸入總接受點的總數，以及各點的座標(LCP)，
	   先由前述csv檔讀入lat/lon值，經由twd97模組將經緯度轉成twd97座標，扣除Xcent、Ycent之offset即成為LCP座標(CALPUFF為KM單位)
	  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
	  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
	  檔案另輸出成data/xy_taiwan3.dat
3. output.f 離散點之輸出
	- $ diff CALPUFF_v7.2.1_L150618/output.f new/output.f
	- 125a126
	- >       character*150 infile
	- 373a375,392
	- > c--------------------------------------------------------------
	- > ckuang
	- > c --- Sara 08/10/2004: Just to have an output of the concentration
	- > c --- directly readable.
	- > c --- Concentration in g/m^3 is written for each receptor
	- >             do ispec=1,nspec
	- >               write(infile,10000) ispec, istep
	- > c     &                     I2.2,I4.4,'.vtk')
	- > 10000         format('concrec',I2.2,I4.4,'.dat')
	- > c             print *, nspec,',',ispec,',',nn,',',infile,',',
	- > c     +       nrec,',',chirec(1,ispec)
	- >               open(50,file=infile)
	- >               do i=1,nrec
	- >                 write(50,*) chirec(i,ispec)
	- >               end do
	- >               close(50)
	- >             end do
	- 
4. PM2.5 的計算（結合銨鹽重量的計算）
	- CALPUFF之CSPEC共有8種，利用其中的成份計算總PM2.5，包括結合銨鹽
	- 以DataFrame架構整理檔案名稱(spec, hour)，再讀入個別檔案的內容成為3維矩陣C。
	- 輸出檔案為00-hhhh.dat。
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

等濃度圖與網站設定
模擬污染物項目、小時數、動畫、濃度等級的修改，
- Python/genmaps.py
  主要修改污染物項目，
  由SO2/SO4→PM2.5/NOX/SO2/SO4等四項，
  成份變數SOX→SPEC
  檔案個數(總時數)
		100c109
		<     nconc = 48
		---
		>     nconc = 83
- Python/maptoolkit.py
  除上述污染項目之外，尚有：
  指定PMF及NOX concrec的file name前2碼
  座標系統的計算方式
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
	- 濃度等級(ug/m3)
		273,274c276,277
		<         self.binLims = [10, 350, 600, 2600, 9000, 14000]  # SO2 bin limits
		<         self.binLimsSO4 = [1E-8, 12, 35, 55, 150, 250]  # SO4 bin limits from:
		---
		>         self.binLims = [1E-3,1E-2,1,5, 10, 350]  # SO2 bin limits
		>         self.binLimsSO4 = [1E-3, 1E-2,1E-1, 1, 5, 15]  # SO4 bin limits from:
- XYFILE:xy_masaya.da→xy_taiwan3.dat
- 圖框之tic
		399,400c403,404
		>         latTicks = np.arange(round(latMin, 1), round(latMax, 1) + 0.1, 0.5)
		>         lonTicks = np.arange(round(lonMin, 1), round(lonMax, 1) + 0.1, 0.5)
- 指定外部IP（內設是本機）
  python -m http.server --bind 200.200.12.191 8030&
TODO
1. crontab自動每天執行
2. 點、線、面源模擬分析
3. 重要點污染源分析
4. 測站時間序列
5. 掛網：與天氣小編整合、鼎環或其他
6. 臭氧煙陣軌跡
7. 縮小範圍、增加污染源
8. 教學用


<HOME>


