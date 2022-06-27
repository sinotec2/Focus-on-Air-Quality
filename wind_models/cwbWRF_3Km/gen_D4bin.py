import netCDF4
import numpy as np
import os
import twd97
from scipy.io import FortranFile
from bisect import bisect

fname='M-A0064-084.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nlay,nrow,ncol=nc.variables[V[2][0]].shape

nc1= netCDF4.Dataset('wrfout_d04_2020-06-14_06:00:00','r+')
V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nt1,nlay1,nrow1,ncol1=nc1.variables[V1[3][3]].shape

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)

xlon,xlat=nc1.variables['XLONG'][0,:,:].flatten(),nc1.variables['XLAT'][0,:,:].flatten()
xy1=np.array([twd97.fromwgs84(i, j) for i, j in zip(xlat, xlon)])
x1,y1=(xy1[:,i].reshape(nrow1,ncol1) for i in range(2))

xlon,xlat=nc.variables['gridlon_0'][:,:].flatten(),nc.variables['gridlat_0'][:,:].flatten()
xy=np.array([twd97.fromwgs84(i, j) for i, j in zip(xlat, xlon)])
x,y=(xy[:,i].reshape(nrow,ncol) for i in range(2))

idx=np.zeros(shape=(nrow1,ncol1,2),dtype=np.int)
for j in range(nrow1):
  min_j=min([bisect(list(y[:,ii]),y1[j,0]) for ii in range(ncol)])-1
  min_i=min([bisect(list(x[jj,:]),x1[j,0]) for jj in range(nrow)])-1
  max_j=max([bisect(list(y[:,ii]),y1[j,-1]) for ii in range(ncol)])+1
  max_i=max([bisect(list(x[jj,:]),x1[j,-1]) for jj in range(nrow)])+1
  for i in range(ncol1):
    for jj in range(min_j,max_j):
      for ii in range(min_i,max_i):
        if x[jj,ii]<=x1[j,i]<=x[jj+1,ii+1] and y[jj,ii]<=y1[j,i]<=y[jj+1,ii+1]:(idx[j,i,0],idx[j,i,1])=(jj,ii)

idx0=np.where(idx==0)
for j,i in zip(idx0[0],idx0[1]):
  min_j=min([bisect(list(y[:,ii]),y1[j,i]) for ii in range(ncol)])-1
  min_i=min([bisect(list(x[jj,:]),x1[j,i]) for jj in range(nrow)])-1
  max_j=max([bisect(list(y[:,ii]),y1[j,i]) for ii in range(ncol)])+1
  max_i=max([bisect(list(x[jj,:]),x1[j,i]) for jj in range(nrow)])+1
  xr=x[min_j:max_j,min_i:max_i]
  yr=y[min_j:max_j,min_i:max_i]
  di=np.sqrt((xr-x1[j,i])**2+(yr-y1[j,i])**2)
  dis=di.flatten()
  dis.sort()
  ii,jj=[],[]
  for k in range(4):
    min_k=np.where(di==dis[k])
    jj.append(min_j+min_k[0])
    ii.append(min_i+min_k[1])
  idx[j,i,0],idx[j,i,1]=(min(jj),min(ii)) 

wts=np.zeros(shape=(nrow1,ncol1,4),dtype=np.float64)
one=np.ones(shape=(nrow1,ncol1),dtype=np.int64)
kk=0
for jj in [0,1]:
  for ii in [0,1]:
    xr,yr=x[idx[:,:,0]+one*jj,idx[:,:,1]+one*ii],y[idx[:,:,0]+one*jj,idx[:,:,1]+one*ii]
    wts[:,:,kk]=one/((xr-x1)**2+(yr-y1)**2)
    kk+=1
sum_wts=np.sum(wts,axis=2)
for kk in range(4):
   wts[:,:,kk]=wts[:,:,kk]/sum_wts[:,:]
fname = 'idxD4.bin'
with FortranFile(fname, 'w') as f:
  f.write_record(idx) 
fname = 'wtsD4.bin'
with FortranFile(fname, 'w') as f:
  f.write_record(wts) 
