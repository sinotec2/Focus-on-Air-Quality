---
layout: default
title: EDGAR to CMAQ
parent: Emis. Database for Global Atm. Res.
grand_parent: Global/Regional Emission
nav_order: 1
date: 2022-02-25 15:04:48
last_modified_date: 2022-02-25 15:04:52
---

# EDGARv5之下載與處理
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
- 當3公里解析度模擬範圍擴大到境外，就會需要較高解析度的境外排放數據。[REAS](https://sinotec2.github.io/Focus-on-Air-Quality/REASnFMI/REAS/reas_download/)與其他全球排放數據傳統上大多以0.25度為合理的解析度，然在臺灣附近，約為25~27Km，與3Km差異頗大的。
- [Ding et al(2017)](https://acp.copernicus.org/articles/17/10125/2017/acp-17-10125-2017.html)比較了9種排放清冊，從其中可以發現由bottom-up方式的推估成果並不多，除了[REAS](https://sinotec2.github.io/Focus-on-Air-Quality/REASnFMI/REAS/reas_download/)之外以[EDGAR (Emissions Database for Global Atmospheric Research)](https://edgar.jrc.ec.europa.eu/)較為活躍，其餘如[MEIC (Multi-resolution Emission Inventory for China)](http://meicmodel.org/)受到該國的管制並不公開提供。
- [EDGAR](https://edgar.jrc.ec.europa.eu/)污染項目雖然不多(9樣，詳批次檔)，也沒有點源詳細數據，然而其0.1度解析度確實較[REAS](https://sinotec2.github.io/Focus-on-Air-Quality/REASnFMI/REAS/reas_download/)更加符合需要。


## 下載方式及格式
### 批次檔
- 直接到[EDGAR](https://edgar.jrc.ec.europa.eu/)官網點選下載nc連結，製做批次檔如下。

```bash
for cat in TOTALS ENE REF_TRF IND \
        TNR_Aviation_CDS TNR_Aviation_CRS TNR_Aviation_LTO TNR_Aviation_SPS \
        TRO_noRES TRO_RES TNR_Other TNR_Ship RCO PRO NMM CHE IRO NFE NEU PRU_SOL FOO_PAP \
        MNM AWB AGS SWD_LDF SWD_INC WWT FFF;do
  for i in BC CO NH3 NMVOC NOx OC PM10 PM2.5 SO2;do
    https=https://cidportal.jrc.ec.europa.eu/ftp/jrc-opendata/EDGAR/datasets/v50_AP/${i}/${cat}
    if [ $cat == 'TOTALS' ];then
      filez=v50_${i}_2015.0.1x0.1.zip
    elif [ $cat == 'TNR_Aviation_SPS' ];then
      filez=${cat}_nc.zip
    else
      filez=v50_${i}_2015_monthly_${cat}_nc.zip
    fi
    zz=${https}/${filez}
    wget -q --no-check-certificate $zz
    if [ -e ${filez} ];then unzip -q -o ${filez};fi
  done
done
```
### 類別資訊
- EDGAR參照IPCC之分類方式進行排放推估，共28種類別。
- 因排放類別可對照時間變化、成分特性等訊息，具有發展成排放模式之潛能

|Abb.| Category|
|-|-|
|TOTALS|all the categories|
|ENE|Power industry|
|REF_TRF|Oil refineries and Transformation industry|
|IND|Combustion for manufacturing|
|TNR_Aviation_CDS| Aviation climbing&descent|
|TNR_Aviation_CRS| Aviation cruise|
|TNR_Aviation_LTO| Aviation landing&takeoff|
|TNR_Aviation_SPS| Aviation supersonic|
|TRO_noRES| Road transportation no resuspension|
|TRO_RES| Road transportation resuspension|
|TNR_Other| Railways pipelines and off-road transport|
|TNR_Ship| Shipping|
|RCO| Energy for buildings|
|PRO| Fuel exploitation|
|NMM| Non-metallic minerals production|
|CHE| Chemical processes|
|IRO| Iron and steel production|
|NFE| Non-ferrous metals production|
|NEU|Non energy use of fuels|
|PRU_SOL| Solvents and products use|
|FOO_PAP| Food and Paper|
|MNM| Manure management|
|AWB| Agricultural waste burning|
|AGS| Agricultural soils|
|SWD_LDF| Solid waste landfills|
|SWD_INC| Solid waste incineration|
|WWT| Waste water handling|
|FFF| Fossil Fuel Fires|

### 座標資訊
- 其經緯度的起始點及點數為：
  - 經度：0.05 (3600點)
  - 緯度：-89.5 (1800點)

## 內插程式說明
### [EDGAR2cmaqD2.py](https://raw.githubusercontent.com/sinotec2/cmaq_relatives/master/emis/EDGAR/EDGAR2cmaqD2.py)
- 採用與[reas2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/reas2cmaqD2.py)類似的方式進行內插。
- 由於EDGAR已經是網格化的nc檔案了，因此讀取較為單純。
### 調用模組
- EDGAR資料解析度為0.1度，在台灣地區約為10公里，對3公里之網格系統仍需內插。此處採griddata線性內插。

```python
kuang@master /nas1/TEDS/EDGARv5
$ cat EDGAR2cmaqD2.py
import numpy as np
import netCDF4
import sys, os
from pandas import *
from pyproj import Proj
from scipy.interpolate import griddata
```
### 讀取各物種之總量檔案
- 簡要開始
- 加上一個新物質名稱：粗粒物`PMC`，以對應到排放量CCRS或CPRM

```python
spec='BC CO NH3 NMVOC NOx OC PM10 PM2.5 SO2'.split()
nspec=len(spec)
specn={spec[i]:i for i in range(nspec)}

ny,nx=1800,3600
var=np.zeros(shape=(9+1,ny,nx))
for s in spec:
  fname='v50_'+s+'_2015.0.1x0.1.nc'
  nc = netCDF4.Dataset(fname,'r')
  v='emi_'+s.lower()
  var[specn[s],:,:]=nc[v][:,:]
var[-1,:,:]=var[specn['PM10'],:,:]-var[specn['PM2.5'],:,:]
var=np.where(var<0,0,var)
spec+=['PMC']
specn.update({'PMC':len(spec)-1})

lonM=[  0.05+i*0.1 for i in range(nx)]
latM=[-89.95+i*0.1 for i in range(ny)]
lonm, latm = np.meshgrid(lonM, latM)
```
### 讀取排放量檔案之模版
- 將EDGAR之網格經緯度座標值轉到模版檔案的網格系統
- 找到在模版範圍內的EDGAR座標點(idx)，準備進行griddata內插

```python
DD=sys.argv[1]
#interpolation indexing from template  # get the argument
tail=DD+'.nc'
fname='template'+tail
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x1,y1=np.meshgrid(x1d,y1d)
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]

pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
x,y=pnyc(lonm,latm, inverse=False)

boo=(x<=maxx+nc.XCELL*10) & (x>=minx-nc.XCELL*10) & (y<=maxy+nc.YCELL*10) & (y>=miny-nc.YCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]
```
### 污染項目之對照
- 此處將所有NOx先放在NO<sub>2</sub>，未來再予以調整
- VOCs另行處理(使用REAS的排放比例)

```python
# spec name dict
EDGAR2EMIS={'BC':'PEC','OC':'POA','PM2.5':'FPRM','PMC':'CPRM'}

spec='BC CO NH3 NMVOC NOx OC PM10 PM2.5 SO2'.split()
mw={i:1 for i in EDGAR2EMIS}
mw.update({'CO':28,'NH3':17,'NMVOC':58,'NOx':46,'SO2':64})
EDGAR2EMIS.update({'NOx':'NO2'})
EDGAR2EMIS.update({i:i for i in 'CO NH3 SO2'.split()})
VOCs=['ALD2','ALDX','BENZ','ETH','ETHA','ETHY','ETOH','FORM','HONO','IOLE','ISOP','KET','MEOH','OLE','PAR','PRPA','TERP','TOL','XYL']
nv=len(VOCs)
```
### 複製模版、內插、先處理一般污染物
- 單位轉換：kg/m<sup>2</sup>/s → gmole/cell/s

```python
fname='EDGAR'+tail
os.system('cp template'+tail+' '+fname)
nc = netCDF4.Dataset(fname, 'r+')

# elongate the new ncf
# fill the new nc file
for v in V[3]:
  nc[v][:]=0.

#interpolation scheme, for D0/D2 resolution(15Km/27Km)
for v in spec:
  if v not in EDGAR2EMIS.keys():continue #(PM10 and NMVOC)
  ispec=specn[v]
  vc=EDGAR2EMIS[v]
  if vc not in V[3]:continue
  zz=np.zeros(shape=(nrow,ncol))
  c = np.array([var[ispec,idx[0][i], idx[1][i]] for i in range(mp)])
  zz[:,: ] = griddata(xyc, c[:], (x1, y1), method='linear')
  zz=np.where(np.isnan(zz),0,zz)
  nc[vc][0,0,:,:] =zz[:,:]/mw[v]*1000.*nc.XCELL*nc.YCELL
  print (v)
```
### 處理VOCs之成分
- 此處借用REAS的成分比例做為EDGAR VOCs的計算
- 如果REAS網格沒有VOCs，則以一平均之分布代之

```python
fname='2015_'+DD+'.nc'
nc0 = netCDF4.Dataset(fname, 'r')
Vspl=np.zeros(shape=(nv,nrow,ncol))
for v in VOCs:
  iv=VOCs.index(v)
  Vspl[iv,:,:]+=np.sum(nc0[v][:,0,:,:],axis=0)
vss=np.sum(Vspl[:,:,:],axis=0)
iidx=np.where(vss>0)
Vspl_mean=np.array([np.mean(Vspl[i,iidx[0],iidx[1]]) for i in range(nv)])
Vspl_mean/=sum(Vspl_mean)

iidx=np.where(vss==0)
vss=np.where(vss==0,1,vss)
Vspl[:,:,:]/=vss[None,:,:]
for i in range(nv):
  Vspl[i,iidx[0],iidx[1]]=Vspl_mean[i]
v='NMVOC'
zz=np.zeros(shape=(nrow,ncol))
c = np.array([var[specn[v],idx[0][i], idx[1][i]] for i in range(mp)])
zz[:,: ] = griddata(xyc, c[:], (x1, y1), method='linear')
zz=np.where(np.isnan(zz),0,zz)/mw[v]*1000.*nc.XCELL*nc.YCELL
for v in VOCs:
  iv=VOCs.index(v)
  nc[v][0,0,:,:]=zz[:,:]*Vspl[iv,:,:]

nc.close()
```
### 程式下載

{% include download.html content="python程式：[EDGAR2cmaqD2.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/EDGAR/EDGAR2cmaqD2.py)" %}


## Results

| ![NOx_EastAsia.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NOx_EastAsia.PNG) |![NO2_D6.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NO2_D6.PNG) |
|:--:|:--:|
| <b>圖 Ding(2017) 衛星反衍東亞地區NOx排放之分布</b>|<b>圖 HUADON_3k範圍EDGARv5 NO<sub>2</sub>排放之分布(log gmole/s)</b>|  

## Reference
- Ding, J., Miyazaki, K., van der A, R.J., Mijling, B., Kurokawa, J., Cho, S., Janssens-Maenhout, G., Zhang, Q., Liu, F., and Levelt, P.F. (2017). **Intercomparison of NOx emission inventories over East Asia.** Atmos. Chem. Phys. 17 (16):10125–10141. [doi:10.5194/acp-17-10125-2017](https://acp.copernicus.org/articles/17/10125/2017/acp-17-10125-2017.pdf).

