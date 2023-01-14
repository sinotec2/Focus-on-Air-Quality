---
layout: default
title: 地面排放檔案轉換
parent: Ground Level Emissions
grand_parent: CMAQ Model System
nav_order: 1
date: 
last_modified_date: 2022-01-11 19:52:24  
tags: CMAQ emis CAMx REAS
---

# 地面排放檔案之轉換
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
- CMAQ模式的地面排放量為一逐日拆解的檔案（每檔案需25個小時）。其開始時間為UTC 0時（LST -8）。
- 可以按照排放類別拆分或合併。
- 空間網格系統之定義乃按照[mcip](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/run_mcipMM_RR_DM/#網格系統詳細定義)之定義方式。
- 由CAMx模式排放量檔案而來，其產生過程詳如下表：

|範圍|格式|類別|
|----|----|----|
|東亞範圍|nc|[面排放源](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/REAS/reas2cmaq/)含生物源、
|||[航空排放](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)|
|||[工業排放](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)|
|||[陸上交通排放源](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)|
|||[船舶排放](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/FMI-STEAM)|
|臺灣範圍|nc|[面排放源](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/)|
|||[植物源](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/biog/bioginc/)|
|||[陸上交通排放源](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/line/)|
|||[船舶排放](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)|
|||[地面點源排放](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptseG/)|

## 污染物項目之對照[camx2cmaq.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/camx2cmaq.py)
### 執行方式
- 引數：0～4之序號，依序為`area biog line ptse ship`
- I/O檔案
  - 輸入：`home+'/'+p+'/'+'fortBE.413_teds10.'+ext[p]+mm+'.nc'`
  - 模版：`template.nc`
  - 結果：`p+'_TWN_3X3.16'+mm+'.nc'`

### 重要轉換
- 時間
  - CAMx模式為LST、CMAQ為UTC：需要減8
  - Datetime to/from Julian day：[dtconvertor](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/DateTime/dtconvertor/)
- 排放量
  - CAMx為g/hour、CMAQ為g/s：需要除3600
- 污染項目
  - 在`$EMISSCTRL_NML`檔案中定義。此處不作轉換

### [camx2cmaq.py](https://github.com/sinotec2/cmaq_relatives/blob/master/emis/camx2cmaq.py)程式碼
```python
kuang@master /nas1/cmaqruns/2019base/data/emis/TEDS
$ cat camx2cmaq.py
import os,sys
import numpy as np
import netCDF4
import datetime
from dtconvertor import dt2jul, jul2dt

ipth=int(sys.argv[1])
pth='area biog line ptse ship'.split()
ext={i:i for i in pth}
ext.update({'ship':'51Ab','ptse':'ptsG'})
home='/nas1/TEDS/teds11'
for p in pth[ipth:ipth+1]:
  for m in range(1,13):
    mm='{:02d}'.format(m)
    fname=home+'/'+p+'/'+'fortBE.413_teds10.'+ext[p]+mm+'.nc'
    fnameO=p+'_TWN_3X3.16'+mm+'.nc'
    os.system('cp template.nc '+fnameO)
    nc0= netCDF4.Dataset(fname, 'r')
    nc = netCDF4.Dataset(fnameO, 'r+')
    V0=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
    V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    nv=len(V[3])
    nt,nlay,nrow,ncol=nc0.variables[V0[3][0]].shape
    sdatetime=[jul2dt(nc0.variables['TFLAG'][t,0,:]) for t in range(nt)]
    jul2=[dt2jul(i+datetime.timedelta(hours=-8)) for i in sdatetime]
    for t in range(nt):
      nc.variables['TFLAG'][t,:,0]=[jul2[t][0] for i in range(nv)]
      nc.variables['TFLAG'][t,:,1]=[jul2[t][1] for i in range(nv)]
      for iv in range(nv):
        v=V[3][iv]
        if v in V0[3]:
          nc.variables[v][t,:,:,:]=nc0.variables[v][t,:,:,:]/3600.
        else:
          nc.variables[v][t,:,:,:]=0
    nc.SDATE, nc.STIME=(jul2[0][0],jul2[0][1])
    nc.close()
    print(fnameO)
```

## 按日拆分m3.nc檔案 
- [brk_day2.cs](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/brk_day/)

```bash
for yy in 18;do 
  for mm in 0{1..9} {10..12};do
    for path in area biog line ptse ship;do 
      brk_day2.cs ${path}_TWN_3X3.$yy$mm.nc
    done
  done
done
```

## Reference
- 
