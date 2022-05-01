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
- 指定nc檔案特定時間點、空間位置點的數值，是一件常見的工作。

```python
idx=np.where(mask==0)
nc[v][:,0,idx[0],idx[1]]=0
```
- idx不一定是連續時空範圍
    - 但`(idx[0],idx[1])卻顯然是個線型的陣列
- 如果這些點是零散、不連續、不相關的，那在nc容器中執行此項任務、過程是非常緩慢的。
  - netCDF4一直有個問題，就是[寫出速度](https://stackoverflow.com/questions/27164414/writing-a-netcdf4-file-is-6-times-slower-than-writing-a-netcdf3-classic-file-and)較netCDF3_classic為慢
  - 因為netCDF4是使用HDF5，因此是透過層級架構進行更新、壓縮、所以[存取也會比較慢](https://stackoverflow.com/questions/31865410/python-replacing-values-in-netcdf-file-using-netcdf4)一些。
  - 具體問題討論在網路上還真不多。

### Xarray where 篩選
- xarray雖然有類似array的作法，也可以使用where指令、直接指定不連續時空的數值（如下）
- 但是速度還是很慢，應該也是因為使用了netcdf4的引擎。

```python
...
import xarray as xr
nc = xr.open_dataset(fname, engine="netcdf4")
nc[v][:,0,idx[0],idx[1]]=0. 
...
```

## np.where線型篩選一個nc檔案
- 在陣列中指定部分範圍(不連續時空點)成為另外的數值，基本上是個篩選的動作。
- nv[v][:]是個HDF5檔案，不是一般的陣列記憶體，並不適合作為篩選、置換的容器

### 解決方案
- 另外開啟陣列var作為容器，令`var[:,idx[0],idx[1]]=0`,再一次性回存nc[v][:]檔案中，會快很多。
- 類似情況發生在：
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
