---
layout: default
title: 背景說明
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 1
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 背景說明
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
- CCTM可以接受重疊之排放量檔案
- 公版模式目前並未提出具系統性之排放量組合。似必須待其公開SMOKE方能一致化。

## 面源

|類別|時間|檔名|層數|merged|
|-|-|-|-|-|
|生物源|Jul 18  2021|b3gts_l.20181225.38.d4.ea2019_d4.ncf|1|-|
|基準排放量|Feb 10 2022|cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf|24|yes|
|grid09內插排放量(差值)|Aug 24 2021|egts_l.20181225.38.d4.ea2019_d4.ncf|9|yes|

- 即使經merge後的排放檔案，也有下列版本的差異
```bash
<
/VERSION/ SMOKEv4.7_
/NUMBER OF VARIABLES/  53  ;
---
>
/VERSION/ SMOKEv4.7_                                                            Data interpolated from grid \"Taiwan09\" to grid \"Taiwan03\"
/NUMBER OF VARIABLES/  36" ;
```

## 新增點源檔案
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
  1. 點源檔案的NCOLS及NROWS 2屬性有不一樣的定義，不能被一般檔案覆蓋過去。
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

### 點源增量成果檢核
- 因2點源檔案沒有空間顯示軟體可供檢核，只能以ncdump直接打開檢查內容數字。
- 也可使用下列程式讀成json檔案

#### pt2json.py
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
#### 201901模擬結果差值
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

| ![N3GM_O3.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3GM_O3.PNG) |![G-Bm_O3.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/G-Bm_O3.PNG) |
|:--:|:--:|
| <b>公版模式模擬臭氧增量</b>|<b>2019base模擬臭氧增量</b>|

| ![N3GM_PMf.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/N3GM_PMf.PNG) |![G-Bm_PMf.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/G-Bm_PMf.PNG) |
|:--:|:--:|
| <b>公版模式模擬PMf增量</b>|<b>2019base模擬PMf增量</b>|

### 直接選取TEDS11點源資料庫(add_tzpp.py)
- 這個(台中電廠燃煤機組為例)方案較前述增量方案單純一些，希望程式碼控制在100行之內
- TEDS11資料庫(有管制編號CP_NO)：/nas1/cmaqruns/2019base/data/ptse/twn/目錄下之fortBE.413_teds11.ptse01.nc(CAMx nc file)
  - 按照管制編號及煙囪高度2個變數來搜尋資料庫
- 常數與時變量檔案模版：目錄下之teds11.1901.timvar.nc、及teds11.1901.const.nc
- 變量檔
  - 公版的啟動時間(0:ibeg、前月25日至月底)較長，需要填入暫用值。
  - 回存時又遇到[多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)議題
- 常數檔
  - (YLOCA, XLOCA)、(ROW, COL)需要以新的座標系統校正

```python
kuang@DEVP /nas2/cmaq2019/download/input/201901/grid03/smoke
$ cat add_tzpp.py
import PseudoNetCDF as pnc
import numpy as np
import sys,os, subprocess, netCDF4
from pandas import *
from pyproj import Proj
# read the TEDS11 databank
root='/nas1/cmaqruns/2019base/data/ptse/twn/'
fname=root+'fortBE.413_teds11.ptse01.nc'
nc = netCDF4.Dataset(fname,'r')
v='CP_NO'
nopt,ii=nc[v].shape
L='L0200473'
cp_no=[''.join([str(i, encoding='utf-8') for i in nc[v][t,:]]) for t in range(nopt)]
LL=[i for i in cp_no if L in i]
L=LL[0]
v='stkheight'
hei=nc[v][:]
df=DataFrame({'cp':cp_no,'he':hei})
tzpp=df.loc[(df.cp==L)&(df.he==250)]
l_tzpp=len(tzpp)
# time-variant part of CCMS point source file
fname='teds11.1901.timvar.nc'
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
os.system(ncks+' -O -d ROW,1,'+str(l_tzpp)+' '+root+fname+' '+fname)
nc0 = netCDF4.Dataset(root+fname,'r')
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
nv=len(V[3])

var=np.zeros(shape=(nv,nt,nlay,l_tzpp,ncol))
for v in V[3]:
  var4=nc0[v][:]
  iv=V[3].index(v)
  var[iv,:,:,:,:]=var4[:,:,tzpp.index,:]
## base emission source file, for transfer certain attributes
fname='cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_0-8'
nc00 = netCDF4.Dataset(fname,'r')
tflag0=nc00['TFLAG'][:,0,:]
sdatim=[i*100+j/100/100 for i,j in zip(tflag0[:,0],(tflag0[:,1]))]
nt0=len(tflag0[:,0])

## transfer to new timeframe
begd=nc.SDATE
begt=nc.STIME
ibeg=sdatim.index(begd*100+begt/100/100)
if nt0-ibeg>nt:sys.exit('fail cover the end of month '+str(nt0)+' '+str(ibeg))
## time flags
for t in range(nt0):
  for dt in range(2):
    nc['TFLAG'][t,:,dt]=tflag0[t,dt]
## transfer the emission rates, see [linear_fitering_NC]()    
for v in V[3]:
  iv=V[3].index(v)
  nc[v][:ibeg,:,:,:]=var[iv,:ibeg,:,:,:]
  nc[v][ibeg:nt0,:,:,:]=var[iv,:(nt0-ibeg),:,:,:]

## attributes
atts=['SDATE','STIME', 'P_ALP', 'P_BET', 'P_GAM', 'XCELL', 'XCENT', 'XORIG', 'YCELL', 'YCENT', 'YORIG']
for i in atts:
  if i not in dir(nc00):continue
  exec('nc.'+i+'=nc00.'+i)
nc.NROWS=l_tzpp
nc.close()
# constant parameter of point sources
fname='teds11.1901.const.nc'
os.system(ncks+' -O -d ROW,1,'+str(l_tzpp)+' '+root+fname+' '+fname)
nc0 = netCDF4.Dataset(root+fname,'r')
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
for v in V[3]:
  nc[v][0,0,:,0]=nc0[v][0,0,tzpp.index,0]
for i in atts:
  if i not in dir(nc00):continue
  exec('nc.'+i+'=nc00.'+i)
nc.NROWS=l_tzpp
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

## 船舶排放之敏感性分析
- TEDS11並沒有公開更新後的船舶排放量。
- 公版基準排放量檔案中船舶的空間分布，與TEDS10很類似，缺乏海峽中線西方與公海部分排放量，這非常可能是低估SO<sub>2</sub>濃度的原因。
- 要探討這個課題，首先必須要能將基準排放量中開放水域的部分予以歸零，才能探討次部分排放量的影響程度。
- 公版模式提供了ocean.ncf，其中的MASK有3個數字律定
  - 2:開放水域
  - 1:海岸線
  - 0:其他
- 程式需要將開放水域位置予以標定，將所有該等位置的排放量歸零，即可。
### dSHIP.py
- 使用np.where將開放水域位置予以標定（`idx`）
- 事先先複製一份基準排放量檔案當成模版
- 注意nc檔案並不適用np.array的fancy indexing
  - 詳[NC檔案多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)

```python
In [24]: pwd
Out[24]: '/data/cmaqruns/2019simen/input/201901/grid03/smoke'

In [25]: !cat dSHIP.py
import numpy as np
import netCDF4
fname='/data/cmaqruns/2019simen/output/2019-01/grid03/ocean/ocean.ncf'
nc = netCDF4.Dataset(fname,'r')
v='MASK'
mask=nc[v][0,0,:,:]
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
idx=np.where(mask==2)
fname='/data/cmaqruns/2019simen/output/2019-01/grid03/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_dSHIP'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
var=np.zeros(shape=(nt,nrow,ncol))
for v in V[3]:
  var[:,:,:]=nc[v][:,0,:,:]
  var[:,idx[0],idx[1]]=0
  nc[v][:,0,:,:]=var[:,:,:]
nc.close()
```
### 船舶排放造成的空氣品質增量


## 公版各層排放量增量敏感性分析
- 點源簡化以高空網格型式輸入是公版背景基準排放量特色之一。
  - 由於單一點源年排放量可能有千噸以上，為各界所關注，此一作法會造成什麼樣的效果值得探討。
  - 
### 各層排放量分布
- 取全月時間之平均值、單位：gmole/s(gas)、g/s(particle)
- 切割各層檔案、再取最大值

```bash
nc=cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf0-8
tmNC $nc
nc=${nc}T
for k in {0..8};do ncks -O -d LAY,$k $nc ${nc}.$k;done
for k in {0..8};do 
  echo $k $(mxNC ${nc}.$k|grep PMOTHR|awkk 2) \
  $(mxNC ${nc}.$k|grep PEC|awkk 2) \
  $(mxNC ${nc}.$k|grep PSO4|awkk 2) \
  $(mxNC ${nc}.$k|grep POC|awkk 2)
done
```

- 原生性粒狀物各層月均值排放量中之最大值
  - 這些項目的最大值遠較其他粒狀物為高 

|K|PMOTHR|PEC|PSO4|POC|
|---|---|---|---|---|
|0|7.575|1.311|2.932|1.983|
|1|4.108|0.372|0.549|0.28|
|2|5.288|4.364|0.789|0.99|
|3|4.315|1.950|0.666|0.444|
|4|5.235|0.383|0.912|0.28|
|5|0.238|0.017|0.04|0.01|
|6|0.009|0.000|0.000|0.000|
|7|0.001|0.000|0.000|0.0001|

### 第二層(K1)排放造成的地面污染增量
- 氣象條件：201901～31
- K1高度：地面以上39.7\~79.55m約40m厚度
- 

| ![SO2K1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SO2K1.png) |![PM25K1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM25K1.png) |
|:--:|:--:|
| <b>公版K1排放量造成SO<sub>2</sub>濃度增量(月均值)</b>|<b>公版K1排放量造成PM<sub>25</sub>濃度(月均值)</b>|

## 特定高度、特定位置排放量之敏感性
- 此處範例探討自背景排放量檔案中剔除特定點污染源造成的濃度差異，即為該廠之關閉敏感性。此處以臺中電廠為例。
- 由[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI)中找到臺中電廠(滑鼠滑過在下方會出現(i,j)座標位置)
  - 位置(fortran notation)為(40,87,5)及(40,88,5)
  - 位置並沒有時間變化。排放量沒有時間變化。
- 使用下列程式自背景基準排放(BASE)中予以剔除、另存新檔(dTZPP)、執行cctm
- TZPP = BASE - dTZPP

### 剔除特定位置之排放量
- 注意python的空間索引順序與fortran相反、標籤自0開始。

```python
fname='cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_0-8NoTZPP'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
for v in V[3]:
    nc[v][:,4,87,39]=0.
    nc[v][:,4,86,39]=0.
nc.close()
```
### 排放差異
- 將公版模式1月份排放量加總結果與[add_tzpp.py](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis/#直接選取teds11點源資料庫add_tzpppy)結果排放量比較如下表
  - 時間範圍都以1/1/00~1/31/23
  - 空間範圍：公版條件如上述2個網格之內容。[add_tzpp.py]()則為符合管編及高度2個條件之內容。
- 排放單位：gmole/s(gas)、g/s(P*)  

|Spec|somke|add_tzpp.py|
|:-:|-:|-:|
|CO|324.92383|272.7862|
|NO|5726.74|5965.1284|
|NO2|636.30457|662.79205|
|PAL|772.9443||
|PCA|446.67633||
|PCL|8.143751||
|PEC|554.1376||
|PFE|378.05652||
|PK|60.13299||
|PMC|3100.6912||
|PMN|3.6705146||
|PMOTHR|7558.5415 (+P*=16048.072)|17837.893|
|PNCOM|164.42868||
|PNH4|45.004257||
|PNO3|7.3863435||
|POC|409.12964||
|PSI|1166.5374||
|PSO4|1316.7242||
|PTI|55.866913||
|SO2|3240.5608|3389.6604|

- 除CO外，其餘項目公版排放量略低於[add_tzpp.py]()。二者總量差異有限
- 公版有較完整的PM分率，
  - 因各PM物質的水溶性、化學特性都有差異，可能會因詳細計算結果而有較低的濃度。
  - 相對而言PMOTHR較為惰性，應為偏僻原生性污染物之保守設定。

### 結果分析
- 公版排放量模擬臺中電廠燃煤機組關閉後之空品敏感性(TZPP = BASE - dTZPP)
- [add_tzpp.py]()排放量之增量(TZPP' = aTZPP- dTZPP)

| ![TZPP_pmfM.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/TZPP_pmfM.PNG) |![TZPP_pmfT.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/TZPP_pmfT.PNG) |
|:--:|:--:|
| <b>PM<sub>25</sub>濃度差異之月最大值</b>|<b>PM<sub>25</sub>濃度差異之月均值</b>|