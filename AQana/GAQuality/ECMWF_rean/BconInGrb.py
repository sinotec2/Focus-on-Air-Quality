#kuang@master /nas1/ecmwf/CAMS/CAMS_global_atmospheric_composition_forecasts/2022
#$ cat BconInGrb.py
import netCDF4
from pandas  import *
from pyproj import Proj
import numpy as np
import pygrib

#bcon template dimensions
fname='bcon.template'
nc1 = netCDF4.Dataset(fname, 'r')
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc1.P_ALP, lat_2=nc1.P_BET, lat_0=nc1.YCENT, lon_0=nc1.XCENT, x_0=0, y_0=0.0)
V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nc1 = netCDF4.Dataset(fname, 'r')
nt1,nlay1,nbnd1=nc1.variables[V1[2][0]].shape
nrow1,ncol1=nc1.NROWS,nc1.NCOLS
nrow0,ncol0=nc1.NROWS+5,nc1.NCOLS+5
x1d=[nc1.XORIG+nc1.XCELL*(i-2) for i in range(ncol0)]
y1d=[nc1.YORIG+nc1.YCELL*(i-2) for i in range(nrow0)]
x1,y1=np.meshgrid(x1d, y1d)
i0,j0=1,1
i1,j1=i0+ncol1+1,j0+nrow1+1
idx=[(j0,i) for i in range(i0+1,i1+1)]  +   [(j,i1) for j in range(j0+1,j1+1)] + \
    [(j1,i) for i in range(i1-1,i0-1,-1)] + [(j,i0) for j in range(j1-1,j0-1,-1)]
idxo=np.array(idx,dtype=int).flatten().reshape(nbnd1,2).T
x1,y1=x1[idxo[0],idxo[1]],y1[idxo[0],idxo[1]]
nc1.close()

#grib file
fname='allEA_1.grib'
grbs = pygrib.open(fname)
grb=grbs[1]
lats, lons = grb.latlons()
x,y=pnyc(lons,lats, inverse=False) #no flip
ny,nx=x.shape
seq=np.zeros(shape=(ny,nx),dtype=int)
for j in range(ny):
    for i in range(nx):
        seq[j,i]=j*1000+i
for i in ['x','y','seq']:
    exec(i+'='+i+'.flatten()')

n=[-1 for i in range(nbnd1)]
for i in range(nbnd1):
    dist=(x-x1[i])**2+(y-y1[i])**2      #nearest grib data for bcon
    idx=np.where(dist==np.min(dist))[0]
    if type(idx)==list and len(idx)>1: idx=idx[0]
    n[i]=idx

df=DataFrame({'NumOfBnd':[i for i in range(nbnd1)],'x1':x1,'y1':y1,'JinBCON':idxo[0],'IinBcon':idxo[1],'JIseqInGrb':[seq[n[i]][0] for i in range(nbnd1)]})
df.set_index('NumOfBnd').to_csv('BconInGrb.csv')
