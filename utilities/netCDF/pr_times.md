---
layout: default
title:  列印wrf檔案的時間標籤
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2021-12-30 12:34:29
---
# 列印wrf檔案的時間標籤
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
- 雖然wrf系統相關檔案也都是nc檔，但與m3.nc有很大的出入，無法套用，須另外撰寫讀取程式。
- wrf系統執行同樣對檔案的時間標籤非常敏感，這也是wrf系統會把檔案內容的時間寫成檔名的理由。
  - 但畢竟檔名只能記過檔案的起始時間，對間距、最終時間等等內容，還是需要另外讀取。
  - wrf檔案的時間標籤、轉換的方式，請參考[WRF的時間標籤](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/DateTime/WRF_Times/)。
- 此處仿照m3.nc的[pr_tflag.py](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pr_tflag/)使用簡單的`python`程式，將wrf相關檔案的`Times`打印至螢幕以供檢查。

## 程式使用 
- `python pr_times.py wrf_file_name`

## pr_times.py 內容

```python
#!/opt/anaconda3/envs/py37/bin/python
import numpy as np
import netCDF4
import os,sys
import datetime

fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v='Times'
if v not in V[1]:sys.exit('not a wrf system file')
nt=len(nc[v][:,0])
strT=[''.join([i.decode('utf-8') for i in nc[v][t,:]]) for t in range(nt)]
for a in strT:
  print(datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00'))

```