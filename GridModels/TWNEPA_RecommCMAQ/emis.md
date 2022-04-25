---
layout: default
title: 背景及增量排放量
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 2
date: 2022-04-18 09:28:55
last_modified_date: 2022-04-18 09:28:58
---

# 排放檔案管理
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

### 轉接程式

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