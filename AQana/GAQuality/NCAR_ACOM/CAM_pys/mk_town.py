import numpy as np
from PseudoNetCDF.camxfiles.Memmaps import uamiv
import netCDF4

dc=uamiv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/dictd4.uamiv','r')
Vt=[list(filter(lambda x:dc.variables[x].ndim==j, [i for i in dc.variables])) for j in [1,2,3,4]]
s=set()
for v in Vt[3]:
    s=s|set(dc.variables[v][:].flatten())
towns=[int(i) for i in s]
towns.sort()
T=['T'+str(i) for i in towns]

nc = netCDF4.Dataset('20160101.ncT','r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape

for s in T:
    zz=nc.createVariable(s,"f4",('TSTEP','LAY','ROW','COL'))
    v=s
    nc.variables[v].units="fraction        "
    nc.variables[v].long_name='fraction of TOWN in code: '+s[1:]
    nc.variables[v].var_desc = "AR fractional area per grid cell                                                "
dca=np.zeros(shape=(9,nrow,ncol),dtype=int)
iv=0
for v in Vt[3]:
  dca[iv,:,:]=np.array(dc.variables[v][0,0,:,:],dtype=int)
  iv+=1
zz=np.zeros(shape=(nrow,ncol))
for s in towns:
    v='T'+str(s)
    nc.variables[v][0,0,:,:]=zz
for s in towns:
  v='T'+str(s)
  for iv in range(9):
    idx=np.where(dca[iv,:,:]==s)
    zz=np.zeros(shape=(nrow,ncol))
    zz[idx]=1./9.
    nc.variables[v][0,0,:,:]+=zz
nc.NVARS=len(T)+1
nc.close()
