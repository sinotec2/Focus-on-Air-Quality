#kuang@master /nas2/cmaqruns/2019TZPP/output/Annual/iTZPP
#$ cat nc3_to_1.py
import numpy as np
import netCDF4
import sys, os
from pandas import *
from pyproj import Proj
from scipy.interpolate import griddata


#interpolation indexing from template  # get the argument
fname3=sys.argv[1]
fnameO=fname3+'_1x1'
nc3 = netCDF4.Dataset(fname3, 'r')
V3=[list(filter(lambda x:nc3.variables[x].ndim==j, [i for i in nc3.variables])) for j in [1,2,3,4]]
if len(V3[3])!=1:sys.exit('variable lengths must equal to one')
sp=V3[3][0]
fname1='tempTW_'+sp+'_1x1.nc'
os.system('cp '+fname1+' '+fnameO)

nc = netCDF4.Dataset(fnameO, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x1,y1=np.meshgrid(x1d,y1d)
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]

nt3,nlay3,nrow3,ncol3=nc3.variables[V3[3][0]].shape
x1d=[nc3.XORIG+nc3.XCELL*i for i in range(ncol3)]
y1d=[nc3.YORIG+nc3.YCELL*i for i in range(nrow3)]
x,y=np.meshgrid(x1d,y1d)

boo=(x<=maxx+nc.XCELL*10) & (x>=minx-nc.XCELL*10) & (y<=maxy+nc.YCELL*10) & (y>=miny-nc.YCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

# time variables
nc.SDATE=nc3.SDATE
nc.STIME=nc3.STIME
v='TFLAG'
# elongate the new ncf
for t in range(nt3):
  nc.variables[v][t,0,:]=nc3.variables[v][t,0,:]
v=V[3][0]
var=nc3.variables[v][:,:,:]
nc3.close()

# fill the new nc file
for v in V[3]:
  nc[v][:]=0.

#interpolation scheme, for D0/D2 resolution(3Km/1Km)
ispec=0
for v in V[3]:
  for t in range(nt3):
    zz=np.zeros(shape=(nrow,ncol))
    c = np.array([var[ispec,t,idx[0][i], idx[1][i]] for i in range(mp)])
    zz[:,:] = griddata(xyc, c[:], (x1, y1), method='linear')
    zz=np.where(np.isnan(zz),0,zz)
    nc[v][t,0,:,:] =zz[:,:]
nc.close()
