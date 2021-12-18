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