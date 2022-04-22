---
layout: default
title:  2個nc檔案間的差值
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-04-20 14:50:26
---
# 2個nc檔案間的差值
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
- 執行2個netCDF檔案的相減，在空品模式分析過程中算是經常會遇到。
- 套件方案
  - 雖然NCO程式包中有個小工具[ncap2](https://linux.die.net/man/1/ncap2)可以執行4則運算，但需要每個變數一一指定(`ncap2 -s "T2=T*T" in.nc out.nc`)，那可不是一件小事了(也許[shk.cs](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs)後的9\~12個變數可以使用一下)。
  - [CDO](https://code.mpimet.mpg.de/projects/cdo/embedded/cdo.pdf#subsection.2.7.4)對[CF格式](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9/cf-conventions.html)檔案也有其方便性，可以將所有變數一次計算。但畢竟[ioapi格式](https://www.cmascenter.org/ioapi/)與CF格式還是差異蠻大的，尤其是TFLAG相減為0後，檔案將失去其時間標籤了。
  - [ncdiff -x -v TFLAG](https://linux.die.net/man/1/ncdiff)不會執行TFLAG的相減，也似乎一樣效果，因為結果檔案根本不存在TFLAG。
  - 應用GUI程式：如[廣告](https://www.originlab.com/index.aspx?pid=4373&gclid=Cj0KCQjwmPSSBhCNARIsAH3cYgZf0EGPvjoWChpxjOl8IjgZAbtw82MO4GK0-19YPFQjB5U_Iv9x4awaAk21EALw_wcB)，需要上、下載檔案到微軟平台上作業。  
- 最單純的方式，似乎是自己寫一支小程式來計算

## Coding

```python
#!/opt/ohpc/Taiwania3/pkg/local/python/3.9.7/bin/python3
import numpy as np
import netCDF4
import os,sys,datetime
fname=[sys.argv[i+1] for i in range(3)]
rw=['r','r','r+']
nc0=netCDF4.Dataset(fname[0],rw[0])
V=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
nt0,nlay,nrow,ncol=nc0.variables[V[3][0]].shape
nc1=netCDF4.Dataset(fname[1],rw[1])
#V=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nt1,nlay,nrow,ncol=nc1.variables[V[3][0]].shape
if nt1<nt0: fname[0]=fname[1]
os.system('cp '+fname[0]+' '+fname[2])
nc2=netCDF4.Dataset(fname[2],rw[2])
v4=V[3]
nt=min(nt1,nt0)
for v in v4:
  nc2[v][:,:,:,:]=nc0[v][:nt,:,:,:]-nc1[v][:nt,:,:,:]
nc2.close()
```
## Reference
- Community Modeling and Analysis System (CMAS), [I/O API](https://www.cmascenter.org/ioapi/), 
- Carlie J. Coats, Jr.,  [The EDSS/Models-3 I/O API ](https://www.cmascenter.org/ioapi/documentation/all_versions/html/index.html), 2020-03-25 18:03:32Z 