---
layout: default
title:  NC檔案多維度批次篩選
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-05-01 18:54:06
---
# NC檔案多維度批次篩選
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
- 提取或指定nc檔案多維度之時間、空間位置點的數值，是一件常見的工作，如。
  - 這題最原始的作法就是運用迴圈一一指定(eg.早先寫的[分配港區點源及面源排放量](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/harb_ptse/#程式設計))

```python
idx=np.where(mask==0) #tuple length maybe in thousands
for i in range(len(idx[0])):
  nc[v][:,0,idx[0][i],idx[1][i]]=0  
```
- 任何批次作法都遭遇困難(包括使用xarray，因此xr也是使用netcdf引擎來開啟nc檔案)

```python
arr=nc[v][:,0,idx[0],idx[1]]  #stucked
nc[v][:,0,idx[0],idx[1]].shape  #stucked
nc[v][:,0,idx[0],idx[1]]=0  #stucked
```
### fancy indexing applied in numpy but not in netCDF
- 前述篩選如果是規則性的索引，適用fancy indexing
- 而netCDF4.Dataset與numpy array指定索引的意義有很大的出入，需要注意避免錯誤：
  - numpy.array `a=temp[0, 0, [0,1,2,3], [0,1,2,3]]`，將會得到長度4的一維序列
  - ncf `a=nc['TEMP'][0, 0, [0,1,2,3], [0,1,2,3]]`，a.shape=(4,4)
  - 尤有進者，ncf可以接受`temp[0, [0,1], [1,2,3], :]`，這在numpy是不可能的。
  - 二者的fancy indexing比較可以詳見[netcdf-python文件](https://unidata.github.io/netcdf4-python/)。
- 所以前述stucked指令，不單是個錯誤、更會是個災難。
### arbitary indexing
- 如果idx不是連續、或不具規則性的時空範圍
  - 且`(idx[0],idx[1])`可視為線型的軌跡陣列
  - 不適用fancy indexing
  - (目前網路上還找不到批次作業的建議方案)

### nc檔案的結構與存取速度
- 在ncf數組中執行此項任務、過程是非常緩慢的（除了indexing的意義差異）
  - netCDF4一直有個問題，就是[寫出速度](https://stackoverflow.com/questions/27164414/writing-a-netcdf4-file-is-6-times-slower-than-writing-a-netcdf3-classic-file-and)較netCDF3_classic為慢
  - 因為netCDF4是使用HDF5，因此是透過層級架構進行更新、壓縮、所以[存取也會比較慢](https://stackoverflow.com/questions/31865410/python-replacing-values-in-netcdf-file-using-netcdf4)一些。

## np.where線型篩選一個多維度nc檔案
- 在陣列中指定部分範圍(不連續時空點)成為另外的數值，基本上是個篩選的動作。
- nv[v][:]是個HDF5檔案，不是一般的陣列記憶體，並不適合作為篩選、置換的容器

### 解決方案
- 另外開啟陣列var作為容器，令`var[:,idx[0],idx[1]]=0`,再一次性回存 nc[v][:]檔案中，會快很多。

```python
...
for v in V[3]:
  var=np.zeros(shape=(nt,nrow,ncol))
  var[:,:,:]=nc[v][:,0,:,:]
  var[:,idx[0],idx[1]]=0
  nc[v][:,0,:,:]=var[:,:,:]
...
```

### 實例
- 類似情況發生在：
  - [高空點源：排放對照](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/pt2em_d04/#程式分段說明)
  - [船舶：改變解析度(reso.py)](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/FMI-STEAM/old/#改變解析度resopy)
  - [面源：網格化與存檔](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/#網格化與存檔) 
  - [生物源：線性之dataframe填入3維矩陣](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/biog/bioginc/#線性之dataframe填入3維矩陣)
  - [公版船舶排放之敏感性分析](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis/#dshippy)

