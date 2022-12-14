#!/opt/anaconda3/envs/pyn_env/bin/python
import numpy as np
from netCDF4 import Dataset
import sys

fname=sys.argv[1]
nc=Dataset(fname)
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape

for v in V[3][:]:
  a=nc[v][:,0,:,:]
  a=np.where(a==a,a,-1)
  a=np.where(a>0,a,0)
  mxv=np.percentile(a,99.99)
  mnv=np.max([np.percentile(a,0.01),mxv/100])
print(mnv,mxv)
