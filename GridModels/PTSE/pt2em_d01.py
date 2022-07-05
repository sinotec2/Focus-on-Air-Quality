#kuang@master /nas1/cmaqruns/2016base/data/ptse/twn
#$ cat pt2em_d01.py
import netCDF4
import numpy as np
import datetime
import sys,os
from pyproj import Proj
import twd97

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

MM=sys.argv[1]
fname=MM+'.timvar.nc'
nct = netCDF4.Dataset(fname,'r')
Vt=[list(filter(lambda x:nct.variables[x].ndim==j, [i for i in nct.variables])) for j in [1,2,3,4]]
ntt,nlayt,nrowt,ncolt=nct.variables[Vt[3][0]].shape

fname=MM+'.const.nc'
ncc = netCDF4.Dataset(fname,'r')
Vc=[list(filter(lambda x:ncc.variables[x].ndim==j, [i for i in ncc.variables])) for j in [1,2,3,4]]
ntc,nlayc,nrowc,ncolc=ncc.variables[Vc[3][0]].shape
if nrowc != nrowt :sys.exit('nopts not equal in const and timvar files')
lat=ncc.variables['LATITUDE'][0,0,:,0]
lon=ncc.variables['LONGITUDE'][0,0,:,0]
X,Y=pnyc(lon,lat, inverse=False)

fname=MM+'_d01.nc'
os.system('cp temp_d01.nc '+fname)
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape

pwr=10**(int(np.log10(ncol))+1)
ji=[int((y-nc.YORIG)/nc.YCELL)*pwr+int((x-nc.YORIG)/nc.XCELL) for x,y in zip(X,Y)]
sji=set(ji)
ji=np.array(ji)
idx,idx0=[],[]
for a in sji:
    j,i=int(a/pwr),int(a%pwr)
    if i>=ncol or j>=nrow or i<0 or j<0:continue
    idx.append(np.where(ji==a)[0])
    idx0.append(a)

sint=[]
for v in set(Vt[3])&set(V[3]):
    if np.sum(nct.variables[v][:])==0.:continue
    sint.append(v)
sint.sort()
nv=len(sint)

#write time flags, and lengthen the span of time
for t in range(ntt):
    nc.variables['TFLAG'][t,:,:]=nct.variables['TFLAG'][t,:,:]

#blanking all variables
for v in V[3]:
    nc.variables[v][:]=0.

var0=np.zeros(shape=(nv,ntt,nrowt))
var1=np.zeros(shape=(nv,ntt,len(idx)))
for iv in range(nv):
    var0[iv,:,:]=nct.variables[sint[iv]][:,0,:,0]
for ii in range(len(idx)):
    var1[:,:,ii]=np.sum(var0[:,:,idx[ii]],axis=2)

for iv in range(nv):
    v=sint[iv]
    print(v)
    for ii in range(len(idx0)):
        a=idx0[ii]
        j,i=int(a/pwr),int(a%pwr)
        nc.variables[v][:,0,j,i]=var1[iv,:,ii]
nc.close()
