import numpy as np
from PseudoNetCDF.camxfiles.Memmaps import uamiv
import netCDF4
from libtiff import TIFF

tiff=TIFF.open('d4_twn1x1.tiff',mode='r')
image = tiff.read_image()
towns=[int(i) for i in set(image.flatten())]
towns.sort()
T=['T'+str(i) for i in towns]

nrow3,ncol3=image.shape
zz=np.zeros(shape=(nrow3,ncol3),dtype=int)
for j in range(nrow3):
  zz[j,:]=np.array(image[nrow3-j-1,:],dtype=int)
image=zz

nc = netCDF4.Dataset('20160101.ncT','r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape

dca=np.zeros(shape=(9,nrow,ncol))
for j in range(0,nrow3,3):
  jj=j//3
  for i in range(0,ncol3,3):
    ii=i//3
    iv=0
    for j1 in range(3):
      for i1 in range(3):
        dca[iv,jj,ii]=image[j+j1,i+i1]
        iv+=1
    
for s in T:
    zz=nc.createVariable(s,"f4",('TSTEP','LAY','ROW','COL'))
    v=s
    nc.variables[v].units="fraction        "
    nc.variables[v].long_name='fraction of TOWN in code: '+s[1:]
    nc.variables[v].var_desc = "AR fractional area per grid cell                                                "

zz=np.zeros(shape=(nrow,ncol))
for v in T:
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
