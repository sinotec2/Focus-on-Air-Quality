---
layout: default
title: 船舶排放之敏感性分析
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 6
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 船舶排放之敏感性分析
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
- TEDS11並沒有公開更新後的船舶排放量。
- 公版基準排放量檔案中船舶的空間分布，與TEDS10很類似，缺乏海峽中線西方與公海部分排放量，這非常可能是低估SO<sub>2</sub>濃度的原因。
- 要探討這個課題，首先必須要能將基準排放量中開放水域的部分予以歸零，才能探討次部分排放量的影響程度。
- 公版模式提供了ocean.ncf，其中的MASK有3個數字律定
  - 2:開放水域
  - 1:海岸線
  - 0:其他
- 程式需要將開放水域位置予以標定，將所有該等位置的排放量歸零，即可。

### dSHIP.py
- 使用np.where將開放水域位置予以標定（`idx`）
- 事先先複製一份基準排放量檔案當成模版
- 注意nc檔案並不適用np.array的fancy indexing
  - 詳[NC檔案多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)

```python
In [24]: pwd
Out[24]: '/data/cmaqruns/2019simen/input/201901/grid03/smoke'

In [25]: !cat dSHIP.py
import numpy as np
import netCDF4
fname='/data/cmaqruns/2019simen/output/2019-01/grid03/ocean/ocean.ncf'
nc = netCDF4.Dataset(fname,'r')
v='MASK'
mask=nc[v][0,0,:,:]
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
idx=np.where(mask==2)
fname='/data/cmaqruns/2019simen/output/2019-01/grid03/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf_dSHIP'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
var=np.zeros(shape=(nt,nrow,ncol))
for v in V[3]:
  var[:,:,:]=nc[v][:,0,:,:]
  var[:,idx[0],idx[1]]=0
  nc[v][:,0,:,:]=var[:,:,:]
nc.close()
```
### 船舶排放造成的空氣品質增量
