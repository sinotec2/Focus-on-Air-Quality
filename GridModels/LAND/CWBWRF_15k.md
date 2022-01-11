---
layout: default
title: 亞洲土地使用檔案
parent: Geography and Land Data
grand_parent: CMAQ Models
nav_order: 1
date: 2022-01-11 16:06:49
last_modified_date: 2022-01-11 16:06:52
---

# 亞洲土地使用檔案
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


## 模版處理過程
### NCO及ipython交互處理
- 原始模版：beld4.EAsia_81K.ncf
- 目標：南北擴增到389、東西伸長到665，以與mcip網格定義一致

```bash
kuang@DEVP /nas1/cmaqruns/2018base/data/land
$ cat ../mcip/1804_run5/CWBWRF_15k/GRIDDESC
' '
'TWN_PULI'
  2        10.000        40.000       121.736       121.736        23.610
' '
'CWBWRF_15k'
'TWN_PULI'  -4980000.000  -2966000.000     15000.000     15000.000 665 389   1
' '
```
#### 擴增南北向
- ncpdq改順序、ncks開放UNLIMITED

```bash
nc=beld4.CWBWRF_15k.ncf
cp beld4.EAsia_81K.ncf $nc
ncpdq -O -a ROW,TSTEP,LAY,COL $nc a;ncks -O --mk_rec_dmn ROW a $nc
```
- 進入ipython

```python
fname='beld4.CWBWRF_15k.ncf'
nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nrow,nt,nlay,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4)
for j in range(nrow,389):
  for v in V[3]:
    nc[v][j,0,0,:]=0.
nc.NROWS=389
nc.close()
```
#### 擴增東西向
- 回到OS、用ncpdq改順序、ncks開放UNLIMITED

```bash
ncpdq -O -a COL,TSTEP,LAY,ROW $nc a;ncks -O --mk_rec_dmn COL a $nc
```
- 進入ipython

```python
nc = netCDF4.Dataset(fname, 'r+')
for j in range(ncol,389):
  for v in V[3]:
    nc[v][j,0,0,:]=0.
nc.NCOLS=665
# 其他全域屬性，抄自mcip結果
# 注意：VG*、NLAYS等垂直設定不能抄襲、NVARS也不能覆蓋、刪除舊的HISTORY會使檔案看起來較為清爽
fname='../mcip/1804_run5/CWBWRF_15k/LUFRAC_CRO_1804_run5.nc'
nc0 = netCDF4.Dataset(fname, 'r')
atts=['CDATE',  'CTIME', 'EXEC_ID', 'FILEDESC', 'FTYPE', 'GDNAM', 'GDTYP', 'HISTORY', 'IOAPI_VERSION', 'NCO', 'NCOLS',  'NROWS',
     'NTHIK', 'P_ALP', 'P_BET', 'P_GAM', 'UPNAM', 'WDATE',
     'WTIME', 'XCELL', 'XCENT', 'XORIG', 'YCELL', 'YCENT', 'YORIG']
for i in atts:
  if i not in dir(nc0):continue
  exec('nc.'+i+'=nc0.'+i)
nc.close()
```

#### 恢復順序
```bash
ncpdq -O -a TSTEP,LAY,ROW,COL $nc a;ncks -O --mk_rec_dmn TSTEP a $nc
```

## 填入MODIS值
### 由LUFRAC填入MODIS
```python
fname='beld4.CWBWRF_15k.ncf'
nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
modis=["MODIS_"+str((i+1)%17) for i in range(17)]
for v in V[3]:
  nc[v][:]=0.
  if v[:6]=="MODIS_":
    try:
      ii=int(v[6:8])-1
    except:
      ii=17+int(v[9:10])
    else:
      if ii<0:ii=ii+17
    nc[v][0,0,:,:]=nc0["LUFRAC"][0,ii,:,:]
```

### 確認
- 所有網格MODIS加總必須<=1

```python
modis=[i for i in V[3] if 'MODIS' in i and 'Res' not in i]
var=np.zeros(shape=(len(modis),nrow,ncol))
for v in modis:
  iv=modis.index(v)
  var[iv,:,:]=nc[v][0,0,:,:]
sumv=np.sum(var[:,:,:],axis=0)
np.max(sumv) 
#1.0000000596046448  
```
- [VERDI]()繪圖

| ![MODIS_16.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/MODIS_16.PNG) |
|:--:|
| <b>圖 CWBWRF_15k範圍土地使用(MODIS_16)之分布</b>|

## Reference
