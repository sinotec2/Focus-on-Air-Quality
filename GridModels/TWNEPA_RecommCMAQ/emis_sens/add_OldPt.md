---
layout: default
title: 既有點源檔案
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 3
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 既有點源檔案
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
- 基於點源在公版模式排放檔案中已被網格均化，除非是大型污染源獨佔網格空間，否則難以由背景其他污染源當中切割出來。
- 此處範例以臺中電廠燃煤機組為例，該廠坐落臺中市西南角，燃煤機組排放高度達250m，周圍沒有其他污染源。

## 直接選取TEDS11點源資料庫
- 這個(台中電廠燃煤機組為例)方案較前述[新增點源增量方案]()單純一些，程式碼控制在100行之內
### add_tzpp.py
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
