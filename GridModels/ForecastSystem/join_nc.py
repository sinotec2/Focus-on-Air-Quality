#kuang@DEVP /nas2/cmaqruns/2022fcst $ cat join_nc.py
#!/opt/anaconda3/envs/py37/bin/python
import subprocess, os, sys
import netCDF4
import numpy as np

fnameO=sys.argv[1]
fname=fnameO+'_bak'
nc0 = netCDF4.Dataset(fname, 'r')
nc  = netCDF4.Dataset(fnameO, 'r+')
V=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
nt=nc0.dimensions['TSTEP'].size
for v in V[3]:
  for t in range(nt):
    var0=nc0[v][t,:,:,:]*(nt-t)/nt
    var1=nc[v][t,:,:,:]*t/nt
    nc[v][t,:,:,:]=var0+var1
nc.close()
