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
- 這個(台中電廠燃煤機組為例)方案較前述[新增點源增量方案](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis_sens/add_NewPt/#程式碼)單純一些，程式碼控制在100行之內

### [add_tzpp.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/emis_sens/add_tzpp.py)
- TEDS11資料庫(有管制編號CP_NO)：/nas1/cmaqruns/2019base/data/ptse/twn/目錄下之fortBE.413_teds11.ptse01.nc([CAMx nc file](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/))
  - 按照管制編號及煙囪高度2個變數來搜尋資料庫
- 常數與時變量檔案模版：目錄下之teds11.1901.timvar.nc、及teds11.1901.const.nc
- 變量檔
  - 公版的啟動時間(0:ibeg、前月25日至月底)較長，需要填入暫用值。
  - 回存時又遇到[多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)議題

```python
kuang@DEVP /nas2/cmaq2019/download/input/201901/grid03/smoke
$ cat add_tzpp.py
...
var=np.zeros(shape=(nv,nt,nlay,l_tzpp,ncol))
for v in V[3]:
  var4=nc0[v][:]
  iv=V[3].index(v)
  var[iv,:,:,:,:]=var4[:,:,tzpp.index,:]
...
for v in V[3]:
  iv=V[3].index(v)
  nc[v][:ibeg,:,:,:]=var[iv,:ibeg,:,:,:]
  nc[v][ibeg:nt0,:,:,:]=var[iv,:(nt0-ibeg),:,:,:]
...  
```

- 常數檔
  - 因各項煙囪參數並沒有時間、層數的維度，只有ROW的維度較為單純，此時ncf的indexing與np.array行為一樣，可以直接指定數值
  - (YLOCA, XLOCA)、(ROW, COL)需要以新的座標系統校正

```python
...
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

## add TZPP on BASE2 and BASE3 background
- 將同樣高空點源排放量([add_tzpp.py](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis_sens/add_OldPt/#add_tzpppy))、加在2組不同背景條件下敏感性的比較
### 背景條件說明
- 氣象：2019年1月
- BASE2:2組面源，分別是生物源及背景基準排放量(剔除特定高空點源)
  - bio3taiwan：${cmaqproject}/smoke/b3gts_l.20181225.38.d4.ea2019_d4.ncf
  - basetaiwan：${cmaqproject}/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_0-8[NoTZPP](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis_sens/dTZPP/#剔除特定位置之排放量)
- BASE3：除了前述2者，再加上egts第3層網格排放內插之排放量
  - bio3taiwan：${cmaqproject}/smoke/b3gts_l.20181225.38.d4.ea2019_d4.ncf
  - basetaiwan：${cmaqproject}/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf
  - d3_to_d4：${cmaqproject}/smoke/egts_l.20181225.38.d4.ea2019_d4.ncf

### O3 Max Hr Comparisons
| ![BASE2_O3M.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/BASE2_O3M.PNG) |![BASE3_O3M.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/BASE3_O3M.PNG) |
|:--:|:--:|
| <b>BASE2之O<sub>3</sub>全月最大小時值</b>|<b>BASE3之O<sub>3</sub>全月最大小時值</b>|

### TZPP PM2.5 Increments
- 2019年1月最大日均值
- BASE2環境背景TZPP之最大增量：3.41 &mu;g/m<sup>3</sup>
- BASE3環境背景TZPP之最大增量：3.59 &mu;g/m<sup>3</sup>

| ![TZPP_PM25DM.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/TZPP_PM25DM.PNG) |![TZPP3_PM25DM.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/TZPP3_PM25DM.PNG) |
|:--:|:--:|
| <b>BASE2之PM<sub>2.5</sub>增量</b>|<b>BASE3之PM<sub>2.5</sub>增量</b>|