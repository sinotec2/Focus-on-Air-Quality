#!/opt/miniconda3/envs/py37/bin/python
import numpy as np
import json
import netCDF4
import sys, os, subprocess
import datetime

tpl={0:'SN',1:'WE',2:'SN',3:'WE'}
out={0:'S',1:'E',2:'N',3:'E'}
drn={0:1,1:1,2:-1,3:-1}

#read a BC file as rate base
fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r')
Vb=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nbnd=nc.variables[Vb[2][1]].shape
ibnd={	0:(1,nc.NCOLS+1),
	1:(nc.NCOLS+2,nc.NCOLS+nc.NROWS+2),
	2:(nc.NCOLS*2+nc.NROWS+2,nc.NCOLS+nc.NROWS+2),
	3:(nc.NCOLS*2+nc.NROWS*2+3,nc.NCOLS*2+nc.NROWS+3)}
i1s={0:0,1:0,2:0,3:0}
i2s={0:nc.NCOLS,1:nc.NROWS,2:nc.NCOLS,3:nc.NROWS}

nv=len(Vb[2])
tflag=np.array(nc['TFLAG'][:,0,:])

path='/nas1/cmaqruns/2022fcst/data/bcon'
for i in range(4):
  tname=path+'/template'+tpl[i]+'_CWBWRF_45k.nc'
  fnameO=tname.replace('template','today').replace(tpl[i],out[i])
  os.system('cp '+tname+' '+fnameO)
  nc1 = netCDF4.Dataset(fnameO,'r+')
  V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
  nc1.SDATE,nc1.STIME=tflag[0,:]
  for t in range(nt):
    nc1['TFLAG'][t,0,:]=tflag[t,:]
  var3=np.zeros(shape=nc1.variables['TFLAG'].shape)
  var3[:,:,:]=tflag[:,None,:]
  nc1.variables['TFLAG'][:]=var3[:]
  for v in V1[3]:
    nc1[v][:]=0.
    if v not in Vb[2]:sys.exit(v+' not in BCON file')
    nc1[v][:,0,1::3,i1s[i]:i2s[i]]=nc[v][:,:,ibnd[i][0]:ibnd[i][1]:drn[i]]
    nc1[v][:,0,0,:] =nc1[v][:,0,1,:]
    nc1[v][:,0,-1,:]=nc1[v][:,0,-2,:]
    nc1[v][:,0,2:-1:3,:]=(nc1[v][:,0,1:-2:3,:]*2+nc1[v][:,0,4::3,:]  )/3
    nc1[v][:,0,3:-1:3,:]=(nc1[v][:,0,1:-2:3,:]  +nc1[v][:,0,4::3,:]*2)/3
  nc1.close()
