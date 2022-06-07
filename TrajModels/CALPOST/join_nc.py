#kuang@master /home/cpuff/UNRESPForecastingSystem/vis/20220605
#$ cat ../../Python/join_nc.py
#!/cluster/miniconda/envs/unresp/bin/python
import subprocess, os
import netCDF4
import numpy as np

old_date=subprocess.check_output('date -d "-2 day" +%Y%m%d',shell=True).decode('utf8').strip('\n')

fname='../'+old_date+'/calpuff.con.S.grd02.nc'
nc0 = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
fname='./calpuff.con.S.grd02.nc'
nc = netCDF4.Dataset(fname, 'r+')
nt=24
for v in V[3]:
  for t in range(nt):
    var0=nc0[v][t+nt,:,:,:]*(nt-t)/nt
    var1=nc[v][t,:,:,:]*t/nt
    nc[v][t,:,:,:]=var0+var1
nc.close()