---
layout: default
title:  NC的線性篩選
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-05-01 18:54:06
---
# NC的線性篩選
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
- 指定nc檔案特點時間點、空間位置點的數值，是一件常見的工作。如果這些點是零散、不連續、不相關的，那在nc容器中執行此項任務、過程是非常緩慢的。
  - 如`nc[v][:,0,idx[0],idx[1]]=0`

### Xarray where 篩選
- xarray雖然有類似array的作法，也可以直接指定不連續時空的數值（如下）
- 但是速度還是很慢

```python
...
import xarray as xr
nc = xr.open_dataset(fname, engine="netcdf4")
nc[v][:,0,idx[0],idx[1]]=0. 
...
```

## np.where線型篩選一個nc檔案
- 在陣列中指定部分範圍成為另外的數值，基本上是個篩選的動作。
- nv[v][:]是個檔案，不是一般的陣列記憶體，並不適合作為篩選、置換的容器
-，篩選一個nc檔案速度會非常慢
- 另外開啟陣列var作為容器，令`var[:,idx[0],idx[1]]=0`,再一次倒回nc[v][:]檔案中，會快很多。
- 類似的情況
  - [高空點源：排放對照](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/pt2em_d04/#程式分段說明)
  - [船舶：改變解析度(reso.py)](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/FMI-STEAM/old/#改變解析度resopy)
  - [面源：網格化與存檔](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/#網格化與存檔) 
  - [生物源：線性之dataframe填入3維矩陣](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/biog/bioginc/#線性之dataframe填入3維矩陣)

```python
...
for v in V[3]:
  var=np.zeros(shape=(nt,nrow,ncol))
  var=nc[v][:,0,:,:]
  var[:,idx[0],idx[1]]=0
  nc[v][:,0,:,:]=var[:,:,:]
...
```
