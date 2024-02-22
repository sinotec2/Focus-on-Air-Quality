#kuang@dev2 /nas2/cmaq2019/download-20221018/input
#$ cat sum_cmaq.py
import numpy as np
import netCDF4
import os,sys,datetime
from dtconvertor import dt2jul, jul2dt

root='/nas2/cmaq2019/download-20221018/input/'
spec='SO2 NO2 NO CO'.split()
pm=0
for v in spec:
    exec(v+'=0')
for m in range(12):
    fname=root+'2019{:02d}/grid03/smoke/cmaq.ncf'.format(m+1)
    nc=netCDF4.Dataset(fname,'r')
    V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
    vv=[i for i in V[3] if i[0]=='P' and i not in ['PH2O','PAR','PRPA']]
    dt=[jul2dt(nc.variables['TFLAG'][t,0,:]) for t in range(nt)]
    dtm=np.array([i.month for i in dt])
    idx=np.where(dtm==(m+1))[0]
    p=0
    for v in vv:
        p+=np.sum(nc.variables[v][idx[:],4,86:88,39])
    pm+=p
    for v in spec:
        exec(v+'+=np.sum(nc.variables["'+v+'"][idx[:],4,86:88,39])')
    print(m+1)
mw=[64,46,46,28]
mws={i:j for i,j in zip(spec,mw)}
fac=3600*1000*1000
print(pm*fac)
for v in spec:
    exec('print('+v+'*fac)')
