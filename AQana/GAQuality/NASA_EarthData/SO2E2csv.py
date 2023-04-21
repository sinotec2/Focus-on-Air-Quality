#/nas2/cmaqruns/2019TZPP/output/Annual/OMI/OMSO2E_L3/SO2E2csv.py
from pyproj import Proj
import netCDF4
import os, sys, subprocess
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
fname='temp_OMI-Aura_L3-OMSO2e.he5'
he = netCDF4.Dataset(fname,'r')
nc = he.groups['HDFEOS']['GRIDS']['OMI Total Column Amount SO2']['Data Fields']
V0=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
for v in V0[1]:
  exec(v+'=nc["'+v+'"][:]')
V0=[i for i in V0[1]]
he.close()
ln,lt=(Longitude, Latitude)
x,y = pnyc(ln, lt, inverse=False)

#neglect the old points outside new boundaries
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]

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
ndate=bdate+timedelta(days=-1)
df0=DataFrame({})

#daily loop
head='OMI-Aura_L3-OMSO2e_'
v='ColumnAmountSO2'
while ndate < edate:
  ndate=ndate+timedelta(days=1)
  nowd=ndate.strftime("%Ym%m%d")
  try:
    fname=subprocess.check_output('ls '+head+nowd+'*',shell=True).decode('utf8').strip('\n')
  except:
    continue
  he = netCDF4.Dataset(fname,'r')
  nc = he.groups['HDFEOS']['GRIDS']['OMI Total Column Amount SO2']['Data Fields']
  var=nc[v][:,:].data
  var=np.where(var>0,var,0)
  boo=(x<=maxx+ncXCELL*50) & (x>=minx-ncXCELL*50) & (y<=maxy+ncYCELL*50) & (y>=miny-ncYCELL*50) & (var>0)
  idx = np.where(boo)
  mp=len(idx[0])
  if mp<=10: continue
  xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]
  c=np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
  zz=griddata(xyc, c[:], (x1, y1), method='cubic')

  df[v]=zz.flatten()
  df1=df.loc[df[v]>0].reset_index(drop=True)
  df_tm=pivot_table(df1,index='TOWNCODE',values=v,aggfunc=np.mean).reset_index()
  df_tm['COUNTYCODE']=[i[:5] for i in df_tm.TOWNCODE]
  df_tm['COUNTYNAME']=[cn[i] for i in df_tm.COUNTYCODE]
  df_tm['TOWNNAME']=[tn[i] for i in df_tm.TOWNCODE]
  df_tm['YMD']=nowd.replace('m','')
  df0=df0.append(df_tm,ignore_index=True,sort=False)
  print(nowd)
df0.set_index('YMD').to_csv('OMI'+yr+'.csv')
