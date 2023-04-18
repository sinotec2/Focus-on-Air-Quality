#$ cat /u01/cmaqruns/2019TZPP/output/EARR/EARR2csv.py
from pyproj import Proj
import netCDF4
import os,sys
import numpy as np
from scipy.interpolate import griddata
from datetime import datetime,timedelta
from pandas import *


#1X1 TWN domain
root='/nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001'
fname=root+'/tempTW.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
#new coordinates
x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x1,y1=np.meshgrid(x1d,y1d)
ncXCELL=nc.XCELL
ncYCELL=nc.YCELL

#old coordinates
fname='slev/EARR.slev.20100606.t12z.nc'
nc = netCDF4.Dataset(fname,'r')
V0=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
for v in V0[1]:
  exec(v+'=nc["'+v+'"][:]')
V0=[i for i in V0[1] if i[0] != 'l']+['precip_acc6h']
nc.close()
x,y = pnyc(lon, lat, inverse=False)

#neglect the old points outside new boundaries
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]
boo=(x<=maxx+ncXCELL*10) & (x>=minx-ncXCELL*10) & (y<=maxy+ncYCELL*10) & (y>=miny-ncYCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

#township mapping
df=read_csv(root+'/gridLL.csv')
df.TOWNCODE=['{:08d}'.format(i) for i in df.TOWNCODE]
df.COUNTYCODE=['{:05d}'.format(i) for i in df.COUNTYCODE]
tn={i:j for i,j in zip(df.TOWNCODE, df.TOWNNAME)}
cn={i:j for i,j in zip(df.COUNTYCODE, df.COUNTYNAME)}

#temporal range
yr=sys.argv[1]
bdate=datetime(int(yr),1,1)
edate=datetime(int(yr),12,31)
ndate=bdate
df0=DataFrame({})

# file directories
dirs=['slev','precip']
tail={'slev':'.nc','precip':'.f06h.nc'}
ndiv={'slev':4,'precip':1}

#daily loop
while ndate <= edate:
  nowd=ndate.strftime("%Y%m%d")
  zz={v:np.zeros(shape=(nrow,ncol)) for v in V0}
  for d in dirs:
    for h in range(0,24,6):
      fname=d+'/EARR.'+d+'.'+nowd+'.t{:02d}z'.format(h)+tail[d]
      nc = netCDF4.Dataset(fname,'r+')
      V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
      for v in V0:
        if v not in V[1]:continue
        c=np.array([nc[v][idx[0][i], idx[1][i]] for i in range(mp)])
        zz[v][:,:]+=griddata(xyc, c[:], (x1, y1), method='cubic')/ndiv[d]

  for v in V0:
    df[v]=zz[v][:,:].flatten()
  precip=df['precip_acc6h']
  precip=np.where(precip>=0,precip,0)
  df['precip_acc6h']=precip
  df_tm=pivot_table(df,index='TOWNCODE',values=V0,aggfunc=np.mean).reset_index()
  df_tm['COUNTYCODE']=[i[:5] for i in df_tm.TOWNCODE]
  df_tm['COUNTYNAME']=[cn[i] for i in df_tm.COUNTYCODE]
  df_tm['TOWNNAME']=[tn[i] for i in df_tm.TOWNCODE]
  df_tm['YMD']=nowd
  df0=df0.append(df_tm,ignore_index=True,sort=False)
  print(nowd)
  ndate=ndate+timedelta(days=1)
df0.set_index('YMD').to_csv('EARR'+yr+'.csv')
