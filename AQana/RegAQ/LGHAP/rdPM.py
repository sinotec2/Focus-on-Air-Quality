#kuang@master /nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001
#$ cat tmPM25.py
import netCDF4
import numpy as np
from scipy.io import FortranFile
import datetime
import sys,os

yr=sys.argv[1]
fnameO='/nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001/N393_276.bin'
with FortranFile(fnameO, 'r') as f:
  nar = f.read_record(dtype=np.int)
fnameO='A'+yr+'.nc'
os.system('cp tempTW.nc '+fnameO)
bdate=datetime.datetime(int(yr),1,1)
nd365=365
if int(yr)%4==0:nd365=366
dates=[datetime.datetime.strftime(bdate+datetime.timedelta(days=i),'%Y%m%d') for i in range(nd365)]
fnames=['LGHAP.PM25.D001.A'+i+'.nc' for i in dates]
nc = netCDF4.Dataset(fnameO,'r+')
v4=list(filter(lambda x:nc.variables[x].ndim==4, [i for i in nc.variables]))
nt,nlay,nrow,ncol=(nc.variables[v4[0]].shape[i] for i in range(4))
var=np.zeros(shape=(nd365,nrow,ncol))

t=0
for fname in fnames:
  nc0 = netCDF4.Dataset(fname,'r')
  var0=nc0['PM25'][:]
  var0=var0.T.flatten()
  var0=var0[nar]
  var[t,:,:]=var0.reshape(nrow,ncol)
  t+=1

var=np.where(var!=np.nan,var, -1)
mx=np.max(var)
if mx > 10000:var=np.where(var!=mx,var, -1)
nc.SDATE=int(yr)*1000+1
for t in range(nd365):
  nc['TFLAG'][t,:,0]=int(yr)*1000+1+t
nc['TFLAG'][:,:,1]=0
nc[v4[0]][:,0,:,:]=var[:,:,:]
nc.close()
