#kuang@master /nas1/ecmwf/CAMS/CAMS_global_atmospheric_composition_forecasts/2022
#$ cat grb2json.py
#!/opt/miniconda3/envs/gribby/bin/python
import numpy as np
import json
import sys, os
import netCDF4
from scipy.interpolate import griddata
from bisect import bisect
import pygrib

#the json template
src='/nas1/Data/javascripts/D3js/earth/public/data/weather/current/'
fname='current-wind-surface-level-gfs-1.0.json'
fnameO=fname.replace('wind','ozone')
os.system('cp '+src+fname+' '+fnameO)
with open(fnameO,'r+') as f:
  gfs=json.load(f)
nr=len(gfs)

fname=sys.argv[1]
grbs = pygrib.open(fname)
uv=['ozone', ]
atbs={'ozone': 'GEMS Ozone',}
for a in set(atbs):
  grb = grbs.select(name=atbs[a])
  cmd=a+'=grb[0].values'
  exec(cmd)
ozone=np.flip(ozone,axis=0)
lat_min=-90.
lat_max=90.
dy=0.4
dx=dy

lon_min=0.
lon_max=360.
nx=int((lon_max-lon_min)//dx)+1
ny=int((lat_max-lat_min)//dy)+2
if ozone.shape != (ny,nx):sys.exit('wrong ny,nx')
lon1d=[lon_min+dx*i for i in range(nx)]
lat1d=[lat_min+dy*i for i in range(ny)]
x, y = np.meshgrid(lon1d, lat1d)

#target coordinates
nx1=gfs[0]['header']['nx']
ny1=gfs[0]['header']['ny']
lon_min=gfs[0]['header']['lo1']
lat_min=gfs[0]['header']['la2']
dx1=gfs[0]['header']['dx']
dy1=gfs[0]['header']['dy']
lon1d=[lon_min+dx1*i for i in range(nx1)]
lat1d=[lat_min+dy1*i for i in range(ny1)]
x1, y1 = np.meshgrid(lon1d, lat1d)

idx=np.where((x>0)&(x>=lon_min)&(x<=lon_max)&(y>=lat_min)&(y<=lat_max))
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

for i in range(nr):
  gfs[i]['header']['centerName']="AMS_global_atmospheric_composition_forecasts"
  gfs[i]['data']=[0 for v in range(nx*ny)]


dt=grbs[1].validDate.strftime("%Y-%m-%dT%H:%M:%SZ")

for i in range(nr):
  gfs[i]['header']['refTime']=dt
for ir in range(nr):
  c = np.array([ozone[idx[0][i], idx[1][i]] for i in range(mp)])*2.e9
  zz = griddata(xyc, c[:], (x1, y1), method='cubic')
  gfs[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())

with open(fnameO,'w') as f:
  json.dump(gfs,f)
