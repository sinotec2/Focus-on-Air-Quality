#kuang@master /nas1/cmaqruns/2022fcst/data/emis/REAS_CWBWRF_45k
#$ cat mk_emis.py
import netCDF4
import numpy as np
from pyproj import Proj
from scipy.interpolate import griddata
import os

#new grid system
fname='GRIDCRO2D_2208_run8.nc'
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET, lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x1,y1=np.meshgrid(x1d,y1d)
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]

fname='area_CWBWRF_45k.template.nc'
nc1 = netCDF4.Dataset(fname, 'r+')
atts=['NCOLS','NROWS','NLAYS','SDATE','STIME', 'P_ALP', 'P_BET', 'P_GAM', 'XCELL', 'XCENT', 'XORIG', 'YCELL', 'YCENT', 'YORIG']
for a in atts:
  exec('nc1.'+a+'=nc.'+a)
nc.close()
nc1.close()

# old lat,lon
fname='GRIDCRO2D_1804_run5.nc'
nc = netCDF4.Dataset(fname, 'r')
lats,lons=np.array(nc.variables['LAT'][0,0,:,:]), np.array(nc.variables['LON'][0,0,:,:])
x,y=pnyc(lons,lats, inverse=False)
boo=(x<=maxx+nc.XCELL*10) & (x>=minx-nc.XCELL*10) & (y<=maxy+nc.YCELL*10) & (y>=miny-nc.YCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]
nc.close()


fname='area_CWBWRF_15k.20180403.nc'
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
var=np.zeros(shape=(len(V[3]),nt,nlay,nrow,ncol))
for v in V[3]:
  iv=V[3].index(v)
  var[iv,:,:,:]=nc.variables[v][:,:,:,:]
nc.close()

fname='area_CWBWRF_45k.20220810.nc'
os.system('cp area_CWBWRF_45k.template.nc '+fname)
nc = netCDF4.Dataset(fname, 'r+')

for v in V[3]:
  iv=V[3].index(v)
  if np.sum(var[iv,:,:,:,:])==0:continue
  for t in range(nt):
    c = np.array([var[iv,t,0,idx[0][i], idx[1][i]] for i in range(mp)])
    zz=griddata(xyc, c[:], (x1, y1), method='linear')
    zz=np.where(np.isnan(zz),0,zz)
    nc.variables[v][t,0,:,:]=zz[:,:]
nc.close()
