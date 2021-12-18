---
layout: default
title:  unMask a NCF
parent:   "NetCDF Relatives"
grand_parent: "Utilities"
last_modified_date:   2021-12-10 14:18:27
---
# NC矩陣遮罩之檢查與修改
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
- 一般`nc`檔案的矩陣會自動以`masked array`[numpy.ma.array](https://numpy.org/doc/stable/reference/generated/numpy.ma.array.html)型式儲存，以處理錯誤值、空缺值。
  - 發生在創造新變數、延長或放大矩陣的維度等操作，卻在儲存前沒有給定數據，`python`程式會自動遮蔽該區域的內容。    
  - 雖然嚴格來說填充的策略有所[不同](https://www.cnblogs.com/gujianmu/p/12865859.html)。
- 一個被遮蔽的`nc`檔案，在讀、寫時會遭遇困難，因為一般填入的數字是個極大值`9.969209968386869e+36`
  - 如果被遮蔽的是個模版，延長放大之後，對程式執行而言會是個災難。
- `mask`與否是`ma`矩陣的性質，不是`nc`檔案或變數的屬性，因此不能直接修改其狀態。

## 檢查
- [網友](https://github.com/Unidata/netcdf4-python/issues/849)詳細報告了`nc`矩陣遮蔽造成的困擾。實際發生時，會延長程式的執行時間。
- 進入`ipython`對話命令列，打開`nc`檔案，印出變數矩陣`nc.variables[c][:]`(是個`ma`)的`mask`屬性

```python
In [1]: import numpy as np
In [2]: import netCDF4
In [3]: fname='template_v7.nc'
In [4]: nc = netCDF4.Dataset(fname, 'r+')
In [5]: c='CO'
In [6]: nc.variables[c][:].mask
Out[6]:
array([[ True],
[ True]])
```
- 結果是一個布林的矩陣，因某些因素，`CO`的值沒有給定、被遮蔽了，如果執行`nc.variables[c][:].data`，可以發現其值為前述的極大值

## 修正
- 如果直接修正`ma`的`mask`值
  - 程式不會報錯，但不會有作用。

```python
In [7]: nc.variables[c][:].mask=False
In [8]: nc.variables[c][:].mask
Out[8]:
array([[ True],
[ True]])
```
- 改不動，改了之後，似乎有某些設定讓程式自動執行，將`mask`又再改回`True`
- 更改`nc`變數的2個屬性設定：[set_auto_mask](https://unidata.github.io/netcdf4-python/#Dataset.set_auto_mask)[、set_always_mask](https://unidata.github.io/netcdf4-python/#Dataset.set_always_mask)

```python
In [9]: nc.variables[c].set_auto_mask(False)
In [10]: nc.variables[c].set_always_mask(False)
In [11]: nc.variables[c][:].mask
---------------------------------------------------------------------------
AttributeError Traceback (most recent call last)
<ipython-input-11-ccd20a5de01b> in <module>
----> 1 nc.variables[c][:].mask

AttributeError: 'numpy.ndarray' object has no attribute 'mask'
In [12]: nc.variables[c][:]
Out[12]:
array([[9.96921e+36],
[9.96921e+36]], dtype=float32)
```

  - `set_auto_mask`、`set_always_mask`這2個設定似乎是將`masked array`整個換掉，所以連`mask`的屬性都沒有了，成了一般的`np.array`。
  - 其值為前述的極大值
- 給定數值後存檔、再開

```python
In [13]: nc.variables[c][:]=0.5
In [14]: nc.close()
In [15]: nc = netCDF4.Dataset(fname, 'r+')
In [16]: nc.variables[c][:]
Out[16]:
masked_array(
data=[[0.5],
[0.5]],
mask=False,
fill_value=1e+20,
dtype=float32)
```
- 其值已被改變，但仍然被程式改成`masked_array`，只是因為已有確定的數據，`mask`屬性都改成了`False`。

## Reference
- discussion, **Variables became numpy masked arrays**, [github.issues](https://github.com/Unidata/netcdf4-python/issues/849), 17 Oct 2018
- unidata, **netCDF4 Version 1.5.8**, [github.io](https://unidata.github.io/netcdf4-python), 
- gujianmu, **netcdf4和masked array** [博客園](https://www.cnblogs.com/gujianmu/p/12865859.html)

