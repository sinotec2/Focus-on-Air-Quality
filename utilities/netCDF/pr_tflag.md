---
layout: default
title:  m3.nc檔案時間標籤的列印
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date:   2021-12-18 19:21:11
---
# m3.nc檔案時間標籤的列印
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
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v='TFLAG'
print(np.array(nc.variables[v][:,0,:]))
```