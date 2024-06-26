---
layout: default
title: 新增點源檔案
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 2
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
tags: CMAQ CCTM emis ptse mcip 
---

# 新增點源檔案
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
- 環保署公版模式並沒有單獨背景點源排放量的檔案，而是以高空面源的方式，整併在5度空間的面源檔案中。
  - 這個作法的好處是不必另外整理點源檔案，檔案系統單純。
  - 壞處是
    1. 如果要進行點源的減量模擬，那就必須重做整個排放量檔案。而且
    1. 逐時的5度空間檔案非常龐大，一個月需要近60G。耗用國網中心的儲存空間、與存取時間。
    1. 大型點源並沒有開啟PinG模擬，對近距離範圍會造成氮氧化物的衝擊。
- 好在環評、許可需要的是點源增量模擬，
  1. 可以另外增添點源排放檔案，檔案較小，隨時可以提交檢查
  1. 可以個別開啟PinG模組，對新污染源有較好的處理。
- 處理程式可以運用既有的[pt_timvar.py](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/PTSE/#pt_timvarpy)與[pt_const.py](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/PTSE/#pt_constpy)

### 程式邏輯
- 程式仍以CAMx點源檔案為主要運作的平台，理由有幾：
  - 與過去環評接軌
  - 背景點源資料庫已經整理成該格式檔案，大多數計畫是基於既有廠，由既有資料庫中汲取數據還是比較方便可靠。
  - 處理結果也可以給CAMx模式執行
  - 程式只需稍加修改即可、既有程式仍然可用

### 輸入輸出與執行順序
- 輸入檔案：
  - 環評CAMx點源檔案`fortBE.14.hsinda.1.h80.n5.09Mp`
  - TEDS11背景點源檔案`'../twn/fortBE.413_teds11.ptse'+mo+'.nc‘`
- OS程式：`ncks`
- 暫存檔：單一點源空白模版（CAMx格式）：`New3G.ptse00.nc`  
- 結果：`'New3G.ptse'+mo+'.nc'`
- 後續處理：
  1. 由CAMx點源檔案讀取煙囪條件，存成CCTM點源常數檔案：`../twn/pt_constLL.py `
  1. 由CAMx點源檔案讀取逐時排放，存成CCTM點源暫態檔案：`../twn/pt_timvarLL.py `

### 程式碼  

```python
kuang@114-32-164-198 ~
$ cat mk_ptAdd3G.py
import PseudoNetCDF as pnc
import numpy as np
import sys,os, subprocess, netCDF4
from calendar import monthrange
import datetime
import twd97
from pyproj import Proj
from dtconvertor import dt2jul, jul2dt

pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
python=subprocess.check_output('which python',shell=True).decode('utf8').strip('\n')
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
ncatted=subprocess.check_output('which ncatted',shell=True).decode('utf8').strip('\n')
v1_xinda=[168616.09,2527230.05,80.,-11.0,363.0,19.8*3600.,1]
Xcent,Ycent= 248417-333.33*5,   2613022-3000. #tuning the coordinates
v1_xinda[0:2]=[v1_xinda[0]-Xcent,v1_xinda[1]-Ycent]


#read the new 3G parameters
fname1='/nas1/camxruns/2013_6.40/ptse/fortBE.14.hsinda.1.h80.n5.09Mp'
pt=pnc.pncopen(fname1,format='point_source')
for j in range(1,4):
  exec('v'+str(j)+'=list(filter(lambda x:pt.variables[x].ndim=='+str(j)+', [i for i in pt.variables]))')
nhr,nvar,dt=pt.variables[v3[0]].shape
nt,nopts=pt.variables[v2[0]].shape
d={}
for v in 'XYHDTV':
  var=v+'STK'
  d.update({v:np.array(list(pt.variables[var][:]))})
d.update({'I':np.array([i for i in range(nopts)])})
idx=np.where(abs(d['X']-v1_xinda[0])<3000)
idy=np.where(abs(d['Y'][idx[0]]-v1_xinda[1])<3000)
idh=np.where(abs(d['H'][idx[0]][idy[0]]-80)<5)
I=d['I'][idx[0]][idy[0]][idh[0]]
parms={v:d[v][I] for v in 'XYHDTV'}
emiss={v:np.array(pt.variables[v][0,I]) for v in v2 if pt.variables[v][0,I]>0}

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
lonm,latm=(120.20560197059724, 22.84382911621353)
x,y=pnyc(lonm,latm, inverse=False)
parms.update({'X':x,'Y':y})
xingda='S3200688'
names={7:['xcoord','ycoord','stkheight','stkdiam','stktemp','stkspeed']}
PRM='XYHDTV'
n2v={names[7][i]:PRM[i] for i in range(6)}
spec_old='CCRS CPRM FCRS FPRM NO NO2 SO2'.split()

mo='01'
fname='../twn/fortBE.413_teds11.ptse'+mo+'.nc'
nc = netCDF4.Dataset(fname,'r')
print(fname)
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v='CP_NO'
npts,dum=nc.variables[v].shape
dd =[ ''.join([str(i, encoding='utf-8') for i in list(nc.variables[v][c, :])]) for c in range(npts)]
idx=np.array([dd.index(i) for i in dd if xingda in i])
fnameO='New3G.ptse00.nc'
os.system(ncks+' -O -d COL,'+str(idx[0])+' '+fname+' '+fnameO)
os.system(ncatted+' -a NCOLS,global,o,i,1 '+fnameO)
for m in range(12):
  mo='{:02d}'.format(m+1)
  fnameO='New3G.ptse'+mo+'.nc'
  os.system('cp New3G.ptse00.nc '+fnameO)
  nc = netCDF4.Dataset(fnameO,'r+')
  for v in spec_old:
    nc.variables[v][:]=0.
  for n in n2v:
    nc.variables[n][0]=parms[n2v[n]]
  for v in [i for i in emiss if i in spec_old]:
    nc.variables[v][:,0]=emiss[v][0]*3.
  nc.close()
#  os.system(python+' ../twn/pt_constLL.py '+fnameO)
#  os.system(python+' ../twn/pt_timvarLL.py '+fnameO)
```

### 移轉到公版座標系統與時間標籤
- 援引一個smoke的結果檔案，從中讀取座標系統設定、以及時間標籤值
- const、timvar 二個檔案都必須修改檔案屬性
  - 使用`exec`指令以迴圈修改
  - const檔案有點源的位置、COL/ROW值，也必須按照新的座標系統定位
  - timvar檔案則需修改TFLAG時間標籤的內容與長度
- 注意
  1. 點源檔案的NCOLS及NROWS 2屬性與面源檔案有不一樣的定義，不能被一般檔案覆蓋過去。
    - NCOLS必須為1
    - NROWS為點源個數
  1. COL、ROW是整數，而不是實數

```python
import netCDF4
from pyproj import Proj
import numpy as np
atts=['SDATE','STIME', 'P_ALP', 'P_BET', 'P_GAM', 'XCELL', 'XCENT', 'XORIG', 'YCELL', 'YCENT', 'YORIG']

fname='cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf'
nc0 = netCDF4.Dataset(fname,'r')
tflag0=nc0['TFLAG'][:,0,:]
nt0=len(tflag0[:,0])

# time-variable data
fname='New3G.1901.timvar.nc'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]

#update the attributes
for i in atts:
  if i not in dir(nc0):continue
  exec('nc.'+i+'=nc0.'+i)

#change/lengthen the time flags
for t in range(nt0):
  for dt in range(2):
    nc['TFLAG'][t,:,dt]=tflag0[t,dt]
#also the values of emissions    
for v in V[3]:
  nc[v][:,0,0,0]=nc[v][0,0,0,0]
nc.close()

#stack parameters
fname='New3G.1901.const.nc'
nc = netCDF4.Dataset(fname,'r+')
for i in atts:
  if i not in dir(nc0):continue
  exec('nc.'+i+'=nc0.'+i)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
lat,lon=nc['LATITUDE'][0,0,:,0],nc['LONGITUDE'][0,0,:,0]
x0,y0=pnyc(lon,lat, inverse=False)
nc['XLOCA'][0,0,:,0]=x0[:]
nc['YLOCA'][0,0,:,0]=y0[:]
nc['COL'][0,0,:,0]=np.array((x0[:]-nc.XORIG)/nc.XCELL,dtype=int)
nc['ROW'][0,0,:,0]=np.array((y0[:]-nc.YORIG)/nc.YCELL,dtype=int)
nc['TFLAG'][0,:,0]=nc.SDATE
nc['TFLAG'][0,:,1]=nc.STIME
nc.close()
```

## 點源增量成果檢核
- 因2點源檔案沒有空間顯示軟體可供檢核，只能以[ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump)直接打開檢查內容數字。
- 也可使用下列程式讀成json檔案

### pt2json.py
- 將CCTM點源檔案讀成json的程式
- 引數：const/timvar前之ROOT(含年月,eg `'New3G.1901'`)

```python
import os,sys, json
import netCDF4

ROOT=sys.argv[1]

dd={}
fnames=[ROOT+i+'.nc' for i in ['.const','.timvar']]
fnameO=ROOT+'.json'
for fname in fnames:
  nc = netCDF4.Dataset(fname,'r')
  V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  for v in V[3]:
    if nc[v][0,0,0,0]==0.:continue
    dd.update({v:str(nc[v][0,0,0,0].flatten()[0])})

with open(fnameO,'w',newline='') as jsonfile:
  json.dump(dd, jsonfile)
```
- 得到結果如下

```json
{"COL": "30", "IFIP": "1000", "ISTACK": "1", "LATITUDE": "22.843828", "LMAJOR": "1", "LONGITUDE": "120.205605", "ROW": "38", "STKCNT": "1", "STKDM": "11.0", "STKFLW": "7.6913733", "STKHT": "80.0", "STKTK": "363.0", "STKVE": "-22.721462", "XLOCA": "20405.605", "YLOCA": "-230769.28", "NO": "1.2660064", "NO2": "0.14066738", "PMOTHR": "5.680801", "SO2": "0.22570312"}
```
### 201901模擬結果差值
- 全月最大差異小時值，氣狀物單位ppb、粒狀物&mu;g/M<sup>3</sup>
- 2019force：公版N3G-base，雲雨多、擴散能力較差，原生性濃度高，臭氧低。PM<sub>2.5</sub>只在污染源所在地網格有高值。
- 2019base：不含澎湖版3G-base，臭氧較高，轉化硝酸鹽濃度較高。

|項目|2019force|2019base|
|:-:|:-:|:-:|
|CO|0.17684937|0.18530273|
|NO2|16.97881|13.252734|
|O3|1.3101196|3.1326523|
|PM10|5.6454315|3.747879|
|PM25_NO3|1.8823643|2.4882097|
|PM25_SO4|2.4017506|1.0853934|
|PM25_TOT|6.306381|5.580799|
|SO2|5.694006|2.3229647|
|VOC|1.1403809|1.1473083|

| ![N3GM_O3.PNG](../../assets/images/N3GM_O3.PNG) |![G-Bm_O3.PNG](../../assets/images/G-Bm_O3.PNG) |
|:--:|:--:|
| <b>公版模式模擬臭氧增量</b>|<b>2019base模擬臭氧增量</b>|

| ![N3GM_PMf.PNG](../../assets/images/N3GM_PMf.PNG) |![G-Bm_PMf.PNG](../../assets/images/G-Bm_PMf.PNG) |
|:--:|:--:|
| <b>公版模式模擬PMf增量</b>|<b>2019base模擬PMf增量</b>|

