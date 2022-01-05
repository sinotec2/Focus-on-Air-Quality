---
layout: default
title: REAS文字直接轉CMAQ地面排放檔
parent: REAS Python
grand_parent: CMAQ Models
nav_order: 1
date: 2022-01-05 09:30:02
last_modified_date: 2022-01-05 09:30:08
---

# REAS文字直接轉CMAQ地面排放檔
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>＿
---

## 背景
- REAS (Regional Emission inventory in ASia)是日本國立環境研究所公開的亞洲地區空氣污染及溫室氣體排放量資料庫，詳見[官網](https://www.nies.go.jp/REAS/)之說明。REAS雖然不是最新、但也是持續發展、更新的資料庫系統。除電廠等主要污染源外，其地面污染源解析度為0.25度，在台灣地區約為25~27公里正好為d02的網格解析度。
- 座標系統轉換程式的困難點在於如何在過程中保持質量守恆。策略上：
  - 如果新網格網格間距大於0.25度(如d1 81Km)，則採加總方式，將新網格內的REAS排放量予以加總成該網格排放量，能夠維持總量守恆。
  - 如新網格網格間為相當或小於0.25度(如CWB WRF_15Km 或d2 27Km)，則採REAS網格之內插，可能總量會略有差異。
- 過去曾經作法
  - MM5時代使用網格經緯度為格線，切割REAS排放量，累積各網格排放量。  
  - CAMx系統有bandex程式，可以切割Mozart等間距經緯度之濃度檔，成為直角座標系統。因此先將REAS 文字檔轉成mozart檔案，再循[程序](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/MOZART/)進行解讀，將m3.nc檔案轉成CAMx之uamiv檔案。

## [reas2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD2.py)程式說明

### 程式執行
- 需要引數：domain_name(`D0`、`D2`)、category_name
```bash
for cat in DOMESTIC EXTRACTION FERTILIZER INDUSTRY MISC SOLVENTS WASTE \
ROAD_TRANSPORT OTHER_TRANSPORT POWER_PLANTS_NON-POINT MANURE_MANAGEMENT;do
sub python reas2cmaqD2.py D0 $cat
done
```
- [sub]()=`$1 $2 $3 $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13} ${14} ${15} ${16} ${17} ${18} ${19} ${20} &`

### 分段說明
- 調用模組
  - 使用scipy的griddata進行內插

```python
import numpy as np
import netCDF4
import sys, os
from pandas import *
from pyproj import Proj
from scipy.interpolate import griddata

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
```
-

```python
os.system('~/bin/findc "REASv*" >fnames.txt')
os.system('for i in $(cat fnames.txt);do echo $i $(grep "/mon" $i|cut -d[ -f1);done >spec.txt')
with open('spec.txt','r') as f:
  l=[i.strip('\n').strip('_') for i in f]
fname_spec={i.split()[0]:i.split()[1] for i in l}
spec=list(set(fname_spec.values()))
spec.sort()
nspec=len(spec)
specn={spec[i]:i for i in range(nspec)}
fnames=list(fname_spec)
nmv=set([fname_spec[f] for f in fnames if 'NMV' in f]) 
specNonV=set([fname_spec[f] for f in fnames if 'NMV' not in f]) #共9種CNPS，part(BC,OC,PM2.5,PM10),CO2,ACNS
```
-

```python
#read the coordinates
lon,lat=[],[]
for fname in fnames:
  if '0.25x0.25' not in fname:continue
  with open(fname,'r') as f:
    l=[i.strip('\n').strip('_') for i in f]
  if len(l)<=9:continue
  lon=list(set(lon+[float(i.split()[0]) for i in l[9:]]))
  lat=list(set(lat+[float(i.split()[1]) for i in l[9:]]))
# generate the x and y arrays for REAS datafile
for ll in ['lon','lat']:
  exec(ll+'.sort()')
  exec('n'+ll+'=nn=int(('+ll+'[-1]-'+ll+'[0])/0.25)+1')
  exec(ll+'M=['+ll+'[0]+0.25*i for i in range(nn)]')
  exec(ll+'n={l:'+ll+'M.index(l) for l in '+ll+'M}')
lonm, latm = np.meshgrid(lonM, latM)
x,y=pnyc(lonm,latm, inverse=False)
```
-

```python
#interpolation indexing from template  # get the argument
tail=sys.argv[1]+'.nc'
fname='template'+tail
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x1,y1=np.meshgrid(x1d,y1d)
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]
boo=(abs(x) <= (maxx - minx) /2+nc.XCELL*10) & (abs(y) <= (maxy - miny) /2+nc.YCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

```
-

```python
# category of REAS emission files
cate=['DOMESTIC', 'EXTRACTION', 'FERTILIZER', 'INDUSTRY', 'MISC', 'SOLVENTS', 'WASTE',
'ROAD_TRANSPORT', 'OTHER_TRANSPORT', 'POWER_PLANTS_NON-POINT',  'MANURE_MANAGEMENT']
cate.sort()
ncat=len(cate)
catn={cate[i]:i for i in range(ncat)}

```
-

```python
# read the monthly REAS emissions and store in var matrix
var=np.zeros(shape=(ncat,nspec,12,nlat,nlon))
for fname in fnames:
  if '0.25x0.25' not in fname:continue
  icat=-1
  for c in cate:
    if c in fname:icat=catn[c]
  if icat==-1:continue
  ispec=specn[fname_spec[fname]]
  with open(fname,'r') as f:
    l=[i.strip('\n').strip('_') for i in f]
  if len(l)<=9:continue
  lenl=len(l[9:])
  arr=np.array([float(i.split()[j]) for i in l[9:] for j in range(14)]).reshape(lenl,14)
  for i in range(lenl):
    var[icat,ispec,:,latn[arr[i,1]],lonn[arr[i,0]]]=arr[i,2:]
  print(fname)

```
-

```python
# spec name dict
df=read_csv('REAS2CMAQ.csv')
c_dup=[i for i in set(df.CMAQ) if list(df.CMAQ).count(i)>1]
REAS2CMAQ={i:j for i,j in zip(df.REAS,df.CMAQ) if i in spec}
r_dup=[i for i in REAS2CMAQ if REAS2CMAQ[i] in c_dup and i in spec]

```
-

```python
icat=int(sys.argv[2])
#for icat in range(ncat):
fname=cate[icat]+'_'+tail
os.system('cp template'+tail+' '+fname)
nc = netCDF4.Dataset(fname, 'r+')

```
-

```python
# elongate the new ncf
for t in range(12):
  nc['TFLAG'][t,:,1]=t*100*100
nc['TFLAG'][:,:,0]=nc.SDATE
# fill the new nc file
for v in V[3]:
  nc[v][:]=0.

```
-

```python
#interpolation scheme, for D0/D2 resolution(15Km/27Km)
for v in spec:
  ispec=specn[v]
  if np.sum(var[icat,ispec,:,:,:])==0.:continue
  if v not in REAS2CMAQ:continue
  vc=REAS2CMAQ[v]
  if vc not in V[3]:continue
```
-

```python
  zz=np.zeros(shape=(12,nrow,ncol))
  for t in range(12):
    c = np.array([var[icat,ispec,t,idx[0][i], idx[1][i]] for i in range(mp)])
    zz[t,:,: ] = griddata(xyc, c[:], (x1, y1), method='linear')
  zz=np.where(np.isnan(zz),0,zz)
```
-

```python
  if v in r_dup:
    nc[vc][:,0,:,:]+=zz[:,:,:]
```
-

```python
  else:
    nc[vc][:,0,:,:] =zz[:,:,:]
nc.close()
```
### 程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD2.py)

## 結果檢視
- m3.nc檔案可以用[VERDI]()檢視，如以下：
| ![erod.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/REAS_roadTransBenz.PNG) |
|:--:|
| <b>圖 d01範圍REAS 2015年1月道路交通BENZ排放量之分布</b>|

## Reference
