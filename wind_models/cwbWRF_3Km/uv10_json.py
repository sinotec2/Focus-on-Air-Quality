#kuang@master /home/cpuff/UNRESPForecastingSystem/CWB_data/raw/20220726
#$ cat uv10_json.py
import numpy as np
import json
import sys
import netCDF4
from scipy.interpolate import griddata
from bisect import bisect

#the json template
fname='current-wind-surface-level-gfs-1.0.json'
with open(fname,'r+') as f:
  gfs=json.load(f)
nr=len(gfs)
fname=sys.argv[1]
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nrow,ncol=nc.variables[V[2][0]].shape
x=nc.variables['XLONG'][0,:,:]
y=nc.variables['XLAT'][0,:,:]
lat_min=y[0,ncol//2]
lat_max=np.min([y[-1,-1],y[-1,0]])
jmx=bisect(y[:,ncol//2],lat_max)
dy=(y[jmx,ncol//2]-lat_min)/jmx
dx=dy

lon_min=np.max(x[:,0])
idx=np.where(x[:,-1]>0)
lon_max=np.min(x[idx[0],-1])
nx=int((lon_max-lon_min)//dx)
ny=int((lat_max-lat_min)//dy)

#new grid system(x1,y1) in equal dlat and dlon
lon1d=[lon_min+dx*i for i in range(nx)]
lat1d=[lat_min+dy*i for i in range(ny)]
x1, y1 = np.meshgrid(lon1d, lat1d)
idx=np.where((x>0)&(x>=lon_min)&(x<=lon_max)&(y>=lat_min)&(y<=lat_max))
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

for i in range(nr):
  gfs[i]['header']['nx']=nx
  gfs[i]['header']['ny']=ny
  gfs[i]['header']['numberPoints']=nx*ny
  for v in ['dx','dy']:
    gfs[i]['header'][v]=np.float64(dx)
  gfs[i]['header']['lo1']=np.float64(lon_min)
  gfs[i]['header']['lo2']=np.float64(lon_max)
  gfs[i]['header']['la2']=np.float64(lat_min)
  gfs[i]['header']['la1']=np.float64(lat_max)
  gfs[i]['data']=[0 for v in range(nx*ny)]


uv=['U10', 'V10']
for ir in range(nr):
  var=nc.variables[uv[ir]][0,:,:]
  c = np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
  zz = griddata(xyc, c[:], (x1, y1), method='linear')
  gfs[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())

if 'd01' in fname:fnameO='current-wind-surface-level-cwb-15K.json'
if 'd03' in fname:fnameO='current-wind-surface-level-cwb-3K.json'
with open(fnameO,'w') as f:
  json.dump(gfs,f)
