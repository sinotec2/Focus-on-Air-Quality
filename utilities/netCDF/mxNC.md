---
layout: default
title:  nc檔案時空最大值
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-04-22 11:04:44
---
# nc檔案時空最大值
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
- 快速檢查netCDF檔案變數的最大值，以掌握檔案內容。

## Coding
- 只有1個引數，就是IOAPI之netCDF檔案名稱
- 將會輸出**時間**最大值檔案
- 螢幕會顯示各項變數**時空**的最大值。不會存檔，請自行redirect到文件檔、或其他的pipeline指令(如*grep*)。

```python
#$ cat ~/bin/mxNC
#!/opt/anaconda3/bin/python
import numpy as np
import netCDF4
import os,sys,subprocess
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

fname=[sys.argv[1],sys.argv[1]+'M']

path={'114-32-164-198.HINET-IP.hinet.net':'/opt/anaconda3/bin/', 'node03':'/usr/bin/','master':'/cluster/netcdf/bin/', \
      'DEVP':'/usr/bin/','node02':'/cluster/netcdf/bin/'}
hname=subprocess.check_output('echo $HOSTNAME',shell=True).decode('utf8').strip('\n')
if hname not in path:
  sys.exit('wrong HOSTNAME')
rw=['r','r+']
nc0=netCDF4.Dataset(fname[0],rw[0])
V=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
if len(V[3])>0:
  tt=nc0.variables[V[3][0]].dimensions[0]
else:
  tt=nc0.variables[V[2][0]].dimensions[0]

os.system(path[hname]+'ncks -O -d '+tt+',0,0 '+fname[0]+' '+fname[1])
nc1=netCDF4.Dataset(fname[1],rw[1])
if len(V[3])>0:
  for v in V[3]:
    mxv=np.max(nc0[v][:,:,:,:],axis=0)
    nc1[v][0,:,:,:]=mxv
    print(v,np.max(mxv))
if len(V[2])>0:
  for v in V[2]:
    mxv=np.max(nc0[v][:,:,:],axis=0)
    nc1[v][0,:,:]=mxv
    print(v,np.max(mxv))
if len(V[1])>0:
  for v in V[1]:
    mxv=np.max(nc0[v][:,:],axis=0)
    nc1[v][0,:]=mxv
    print(v,np.max(mxv))
nc1.close()
```
## Reference