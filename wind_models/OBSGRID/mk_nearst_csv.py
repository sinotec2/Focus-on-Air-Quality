#kuang@DEVP /nas1/WRF4.0/WRFv4.2/202208
#$ cat mk_nearst_csv.py
import datetime
from wrf import getvar, interplevel
from netCDF4 import Dataset
import numpy as np
import os, sys
from scipy.interpolate import griddata
from pyproj import Proj
from pandas import *

for d in '12':
  fname='CWB_wrfout_d0'+d
  wrfin = Dataset(fname,'r')
  latm,lonm=getvar(wrfin,'lat'),getvar(wrfin,'lon')
  ny0,nx0=latm.shape
  fname='geo_em.d0'+d+'.nc'
  metin = Dataset(fname,'r')
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=metin.TRUELAT1, lat_2=metin.TRUELAT2, lat_0=metin.CEN_LAT, lon_0=metin.CEN_LON, x_0=0, y_0=0)
  x0,y0=pnyc(lonm,latm, inverse=False) #CWB net
  nz,ny,nx=metin['HGT_M'].shape
  x1d=[metin.DX*(i+0.5) for i in range(-nx//2,nx//2)]
  y1d=[metin.DY*(i+0.5) for i in range(-ny//2,ny//2)]
  x1,y1=np.meshgrid(x1d, y1d)
  for i in 'xy':
    for j in '01':
      exec(i+j+'='+i+j+'.flatten()')
  n=[]
  for i in range(ny*nx):
    dist=(x0-x1[i])**2+(y0-y1[i])**2      #nearest grib data for bcon
    idx=np.where(dist==np.min(dist))[0][0]
    n.append(idx)
  df=DataFrame({'num':[i for i in range(ny*nx)],'J0':[n[i]//nx0 for i in range(ny*nx)], 'I0':[n[i]%nx0 for i in range(ny*nx)]})
  df['J1']=df.num//nx
  df['I1']=df.num%nx
  df.set_index('num').to_csv('nearstD'+d+'.csv')
