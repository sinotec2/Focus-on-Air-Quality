---
layout: default
title: 水平內插與污染項目對照
parent: Boundary Condition
grand_parent: CMAQ Model System
nav_order: 3
date: 2021-12-16 10:59:00
last_modified_date:   2021-12-16 10:59:04
tags: CMAQ ICON BCON
---

# MOZARD/WACCM模式輸出轉成CMAQ初始條件_水平內插與污染項目對照
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
- 全球模式模擬結果要使用在地區的空品模擬，需要經過空間、時間的內插、以及空品項目的對照等作業。此處進行水平內插與污染物的對照。
- 前置作業包括
  - [數據下載](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality)、
  - 使用nc轉換成m3格式[ncf2ioapi](https://www.camx.com/download/support-software/)、[垂直層數切割](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/moz2cmaqV/)、以及
  - 逐6小時空白濃度[模版檔案之準備](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/gen_templateD1/)等。  
- 由於CMAQ濃度檔案可以使用[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/1.run_combMM_R_DM/)予以整併，(或直接)就可以用[VERDI](https://github.com/CEMPD/VERDI/blob/master/doc/User_Manual/VERDI_ch01.md)或進行檢視。
- 後續作業
  - 邊界濃度的製作，包括時間的內插、邊界框濃度的解析等，將在[bcon](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/run_bconMM_RR_DM/)程式內進行。
  - 直接以初始濃度引用：在`run_cctm.csh`內指定即可
- 有鑒於全球空品模擬結果越來越多，且Mozart模式不再維護，有更多直接轉換之程式與作業方式(如ecmwf之[EAC4](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF_rean/grb2bc/))，可以簡化程序。

## [程式](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/moz2cmaqHd1J.py)說明

### 執行方式
- (eg.)執行2018年4月1日0時之內插：`python moz2cmaqHd1J.py 1809100`

#### 引數
- `年代`+`Julian day`+`小時`共7碼

#### I/O檔案
- `mozart`等全球模式輸出結果(經[垂直內插](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/moz2cmaqV/)處理)
- `'ICON_20'+yrjulhh+'.d1'`模版：空白CMAQ濃度檔
- `cb6`對照表[cb6_new.json](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/cb6_new.json)、[cb6_newNum.json](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/cb6_newNum.json)
- 垂直網格對照表[lay2VGLEVLS.json](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/lay2VGLEVLS.json)

#### 同步執行
- 範例同時執行程式由2018/4/1~4/30日(Juian date=091\~120)之濃度內插
  - 使用`Julian day$j`和`小時$h`雙層迴圈
  - **sub**=`$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} &`

```bash
for j in {091..120};do 
  for h in 00 06 12 18;do 
    sub python moz2cmaqHd1J.py 18$j$h
  done
done
```
#### 執行成果的整合(ncrcat)
- 逐6小時的結果，需要整合成批次時間範圍內的**濃度檔序列**，此處使用`ncrcat`程式
- **濃度檔序列**可以連結到一新的目錄，然後用`ncrcat`將其整合，或使用迴圈累加檔名字串，在將字串內的檔案整合。範例如下：
  - 將**全月**檔案連結到目錄、再以`ncrcat`整合

```bash
for i in {12..12};do
  cdate=2019${i}
  pdate=`date -d "${cdate}01 -1  days" +%Y%j`
  ndate=`date -d "${cdate}01 +1 month" +%Y%j`
  mkdir -p $cdate
  cd $cdate
  for ((d=$pdate;d<=$ndate;d+=1));do
    for h in 00 06 12 18;do
      ff=../ICON_${d}${h}.d1
      if ! [ -e $ff ];then continue;fi
      ln -sf $ff .
    done
  done
  cd ..
  ncrcat -O ${cdate}/* ICON_d1_${cdate}.nc &
done
```
  - 按照執行批次的日期範圍，進行字串累加， 再以`ncrcat`整合

```bash
for mo in {01..12};do
begd=$(date -ud "2019${mo}15 - 1 month" +%Y%m%d)
for r in {5..12};do
    d0=$(( ($r-1)*4 ))
    d=d0
    II=ICON_
  for ((d=d0;d<=$(( $d0+5));d+=1));do
    j=$(date -ud "$begd + $d days" +%Y%j)
    if [ $d == $d0 ]; then
      files=$II${j}*.d1
    else
      files=${files}' '$II${j}*.d1
    fi
  done
  sub ncrcat -O ${files} ICON_d1_${y}${mo}_run${r}.nc
done
done
```

### [程式](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/moz2cmaqHd1J.py)分段說明
- 調用模組

```python
import numpy as np
import netCDF4
import os,sys, datetime, json
from pyproj import Proj
```
- 使用pyproj的Proj來進行LCC轉經緯度。此處採經緯度網格的內插(較為方便)。

```python
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, 
		lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
```
- 讀取引數與時間

```python
if (len(sys.argv) != 2):
  print ('usage: '+sys.argv[0]+' YYJJJHH(eg. 1636500)')
yrjulhh=sys.argv[1]
yrmn=datetime.datetime.strptime(yrjulhh[:-2], '%y%j').strftime('%y%m')
```
- 讀取`mozart`等全球模式輸出結果的經緯度及時間標籤字串
  - 時間標籤以字串形式，方便與引數進行比對，找到指定時間(`tM`)

```python
#read the mozart model results
fname='moz_41_20'+yrmn+'.nc'
if not os.path.exists(fname):sys.exit(fname+' not exist')
ncM = netCDF4.Dataset(fname,'r')
v4M=list(filter(lambda x:ncM.variables[x].ndim==4, [i for i in ncM.variables]))
ntM,nlayM,nrowM,ncolM=(ncM.variables[v4M[0]].shape[i] for i in range(4))
lonM=[ncM.XORIG+ncM.XCELL*i for i in range(ncolM)]
latM=[ncM.YORIG+ncM.YCELL*i for i in range(nrowM)]
tflagM=[str(i*100+j//10000)[2:] for i,j in zip(ncM.variables['TFLAG'][:,0,0],ncM.variables['TFLAG'][:,0,1])]
tM=tflagM.index(yrjulhh)
```
- 讀取對照表
  - `cb6`的物質種類對照表：[cb6_new.json](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/cb6_new.json)、
  - 碳鍵數對照表：[cb6_newNum.json](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/cb6_newNum.json)
  - 垂直網格對照表：[lay2VGLEVLS.json](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/lay2VGLEVLS.json)

```python
#load mz2cmaq map
with open('cb6_new.json','r') as f:
  mz2cm=json.load(f)
with open('cb6_newNum.json','r') as f:
  mz2cmNum=json.load(f)
with open('lay2VGLEVLS.json','r') as f:
  lay2VGLEVLS=json.load(f)
lay2VGLEVLS.update({'40':40})
```
- 讀取CMAQ濃度檔案模版
  - 讀取座標與時間標籤

```python
#read the template(s)
fname='ICON_20'+yrjulhh+'.d1'
nc = netCDF4.Dataset(fname,'r')
v4=list(filter(lambda x:nc.variables[x].ndim==4, [i for i in nc.variables]))
nt,nlay,nrow,ncol=(nc.variables[v4[0]].shape[i] for i in range(4))
X=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
Y=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
lon, lat= pnyc(X,Y, inverse=True)
lon_ss=np.searchsorted(lonM,lon)
lat_ss=np.searchsorted(latM,lat)
tflag=nc.variables['TFLAG'][:,0,:]
nc.close()
```
- 去除對照不到的項目

```python
#drop keys which values not in new CMAQ spec_list
mc=list(mz2cm)
for i in mc:
  if i not in v4M:
    mz2cm.pop(i)
    continue
  if mz2cm[i] not in v4:
    mz2cm.pop(i)
```
- 儲存全球模式濃度矩陣
  - 進行高度對照
  - 將濃度單位由**Volume Mixing Ratio**轉到CMAQ的**PPM**

```python
#save the matrix
v4M=list(mz2cm)
A5=np.zeros(shape=(len(v4M),nlayM,nrowM,ncolM))
for ix in range(len(v4M)):
  for k in range(nlayM):
    A5[ix,k,:,:]=ncM.variables[v4M[ix]][tM,lay2VGLEVLS[str(k)],:,:]*1000.*1000. #Volume Mixing Ratio to PPM
ncM.close()
```
- 清空模版的濃度值
  - 避免`netCDF4`自動[遮蔽](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/masked/)
  - 因為模版只有單一時間點，沒有時間的維度

```python
#perform the horizontal interpolation and write results
fname='ICON_20'+yrjulhh+'.d1'
nc = netCDF4.Dataset(fname,'r+')
for x in v4M:
  nc.variables[mz2cm[x]][0,:,:,:]=0
```
- 空間內插與污染項目對照
  - 使用簡單的線性內插
  - 由於不同物質可能都會貢獻到同一碳鍵項目，因此需要累加

```python
for jcrs in range(nrow):
  jmz=lat_ss[jcrs]
  for icrs in range(ncol):
    imz=lon_ss[icrs]
    rx=(lon[icrs]-lonM[imz-1])/(lonM[imz]-lonM[imz-1])
    ry=(lat[jcrs]-latM[jmz-1])/(latM[jmz]-latM[jmz-1])
    A2x=A5[:,:,jmz,imz]*rx+A5[:,:,jmz,imz-1]*(1-rx)
    A2y=A5[:,:,jmz,imz]*ry+A5[:,:,jmz-1,imz]*(1-ry)
    A2=(A2x+A2y)/2.
    for x in v4M:
      nc.variables[mz2cm[x]][0,:,jcrs,icrs]+=A2[v4M.index(x),:-1]*mz2cmNum[x]
nc.close()
```

## 程式下載
- [github](https://raw.githubusercontent.com/sinotec2/cmaq_relatives/2c9e78bf0bf268f8abc5472d928a7bc3c22decee/bcon/moz2cmaqHd1J.py)

## Reference
- lizadams, **Visualization Environment for Rich Data Interpretation (VERDI): User’s Manual**, [github](https://github.com/CEMPD/VERDI/blob/master/doc/User_Manual/VERDI_ch01.md), August 03, 2021
- sinotec2, **NC矩陣遮罩之檢查與修改**, [FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/masked/),Dec 10 2021