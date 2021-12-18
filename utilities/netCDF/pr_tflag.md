---
layout: default
title:  列印m3.nc的時間標籤
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date:   2021-12-18 19:21:11
---
# 列印m3.nc的時間標籤
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
- `nc`檔案的時間標籤是程式能否執行的關鍵。如果時間不正確，**CMAQ**系列程式很快就會跳出錯誤訊息。
- `m3.nc`檔案的時間標籤變數為`TFLAG`，其維度為：`TSTEP, VAR, DATE-TIME`
- 雖然可以使用`ncdump`印出檔案內容逐一確認，但是每一個濃度項目都有`TFLAG`，`ncdump`似乎就不好用了。
- 此處使用簡單的`python`程式，將`TFLAG`打印至螢幕以供檢查

## 程式使用 
- `python pr_tflag.py m3.nc_file_name`

## pr_tflag.py 內容

```python
#!/opt/anaconda3/envs/py37/bin/python
import numpy as np
import netCDF4
import os,sys
fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r')
v='TFLAG'
print(np.array(nc.variables[v][:,0,:]))
```