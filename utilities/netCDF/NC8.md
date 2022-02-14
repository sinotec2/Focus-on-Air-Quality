---
layout: default
title:  NCf之8小時移動平均
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-02-14 10:51:59
---
# NC檔案之8小時移動平均
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
## 背景與注意事項
- 此處以np.cumsum進行移動平均值之計算。
- 結果檔之模版：由輸入檔複製一份
- 命名方式：字尾+8
- 除了臭氧之外，其餘空品項目並無8小時值之規範，因此為減少計算浪費，需先以[ncks]()將臭氧抽出，單獨計算即可。

## NC8程式內容

```python
# /opt/miniconda3/envs/py37/bin/python
import numpy as np
import netCDF4
import os,sys,subprocess
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

fname=[sys.argv[1],sys.argv[1]+'8']

os.system('cp '+fname[0]+' '+fname[1])
rw=['r','r+']
nc0=netCDF4.Dataset(fname[0],rw[0])
nc1=netCDF4.Dataset(fname[1],rw[1])
v4=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))
nt,nlay,nrow,ncol=nc1.variables[v4[0]].shape
a=np.zeros(shape=(nt,len(v4),nlay,nrow,ncol))
for v in v4:
  iv=v4.index(v)
  a[:,iv,:,:,:]=nc0.variables[v][:,:,:,:]
ret = np.cumsum(a,axis=0, dtype=float)
n=8
ret[n:] = ret[n:] - ret[:-n]
b=ret[n - 1:] / n
for v in v4:
  iv=v4.index(v)
  nc1.variables[v][3:nt-4,:,:,:]=b[:,iv,:,:,:]
nc1.close()
```