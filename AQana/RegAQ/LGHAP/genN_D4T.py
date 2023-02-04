#kuang@master /nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001
#$ cat genN_D4T.py
import netCDF4
import numpy as np
from scipy.io import FortranFile
from pyproj import Proj

# open a blank template nc file for D4 domain
fname='/nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/MCD19A2.006/tempTW.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))

pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
X=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
Y=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x,y=np.meshgrid(X, Y)
x=x.flatten();y=y.flatten()
nbnd1=len(x)
minx=x[0]-5000;maxx=x[-1]+5000;miny=y[0]-5000;maxy=y[-1]+5000

# source file coordinates
fname='LGHAP.PM25.D001.template.nc'
nc = netCDF4.Dataset(fname,'r')
lat=nc['lat'][:]
lon=nc['lon'][:]
lon2d,lat2d=np.meshgrid(lon, lat)
x1,y1=pnyc(lon2d,lat2d, inverse=False)
x1=np.array(x1);y1=np.array(y1)
x1=x1.flatten();y1=y1.flatten()
boo=(x1>=minx)&(y1>=miny)&(x1<=maxx)&(y1<=maxy)
idx0=np.where(boo)
x10=x1[idx0[0]]
y10=y1[idx0[0]]

n=[-1 for i in range(nbnd1)]
for i in range(nbnd1):
  minx=x[i]-5000;maxx=x[i]+5000
  miny=y[i]-5000;maxy=y[i]+5000
  boo=(x10>=minx)&(y10>=miny)&(x10<=maxx)&(y10<=maxy)
  idx1=np.where(boo)
  if len(idx1[0])==0:continue
  x11=x10[idx1[0]]
  y11=y10[idx1[0]]
  dist=(x[i]-x11)**2+(y[i]-y11)**2      #nearest grib data for bcon
  idx=np.where(dist==np.min(dist))[0][0]
  if type(idx)==list and len(idx)>1: idx=idx[0]
  n[i]=idx0[0][idx1[0][idx]]
nar=np.array(n,dtype=int)
fnameO='N393_276.bin'
with FortranFile(fnameO, 'w') as f:
    f.write_record(nar)
