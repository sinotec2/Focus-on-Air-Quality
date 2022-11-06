#kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
#$ cat choose10.py
import os, sys
import netCDF4
import twd97
from pandas import *
import bisect

Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)

nc = netCDF4.Dataset('/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_3km.nc','r')

ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
tex=10**ex
x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]

#os.system('ls trjj*L.csv>fnames.txt')
with open('fnamesQC.txt','r')as f:
  fnames=[i.strip('\n') for i in f]

for fname in fnames:
#  if os.path.isfile(fname+'10.csv'):continue
  df=read_csv(fname)
  x=np.array(df.TWD97_x)-Xcent
  y=np.array(df.TWD97_y)-Ycent
  ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
  iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
  df['JI']=[j*tex+i for i,j in zip(ix,iy)]
  reduced_ji=[]
  for i in range(1,len(df)):
    if df.JI[i-1]!=df.JI[i]:
      reduced_ji.append(df.JI[i-1])
  df=DataFrame({'JI3':reduced_ji})
  if len(df)<10:continue
  ji10=[df.JI3[i] for i in range(0,len(df),int(len(df)/10))]
  df=DataFrame({'JI3':ji10[:10]})
  df.set_index('JI3').to_csv(fname+'10.csv')
