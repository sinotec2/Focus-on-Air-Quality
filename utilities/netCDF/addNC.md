---
layout: default
title:  sum of NCFs
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date:   2021-12-17 14:44:41
tags: REAS netCDF
---

# 相同規格NC檔案序列之加總
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
## addNC程式內容
- 引數：欲加總的`nc`檔案名稱，以空格隔開，最後為結果檔名
- 所有的`nc`檔案的規格(維度、變數、全域屬性等)，都必須完全一致。(程式不檢查)
- 欲加總的變數必須是**4個**維度

```python
# /opt/miniconda3/envs/py37/bin/python
import numpy as np
import netCDF4
import os,sys,subprocess
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

nf=len(sys.argv)-1              #number of files
fname=[sys.argv[i] for i in range(1,nf+1)]
os.system('cp '+fname[0]+' '+fname[nf-1])
rw=['r']*(nf-1)+['r+']
nc=[]
for i in range(nf):
  nc.append(netCDF4.Dataset(fname[i],rw[i]))
v4=list(filter(lambda x:nc[0].variables[x].ndim==4, [i for i in nc[0].variables]))
for v in v4:
  for f in range(1,nf-1):
    nc[nf-1][v][:,:,:,:]+=nc[f][v][:,:,:,:]
nc[nf-1].close()
```

## 應用
- 不同排放類別nc檔案之加總。如[REAS結果][reas_addNC]之加總
- [ISAM分析結果][isam_addNC]不同來源別(GR1、GR2、PTA等貢獻較低的類別)加總

## Reference


[reas_addNC]: <https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/REAS/reas2cmaq/#程式執行> "addNC FERTILIZER_D0.nc MISC_D0.nc ... 2015_D0.nc"

[isam_addNC]: <https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ISAM/SA_PM25_IONS/#執行腳本proccs> "ncs='';for nc in $(ls PM25_IONS${z}_2018040${d}_[GP]*.nc);do ncs=${ncs} $nc;done;python ~/bin/addNC $ncs PM25_IONS${z}_2018040${d}.nc"
