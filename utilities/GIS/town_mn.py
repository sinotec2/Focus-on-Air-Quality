#!/cluster/miniconda/envs/ncl_stable/bin/python
from pandas import *
import numpy as np
import netCDF4
import os,sys,datetime
import warnings

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

fname='/nas1/cmaqruns/2016base/data/land/epic_festc1.4_20180516/gridmask/TWN_TOWN_3X3.nc'
nc= netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
towns=[i for i in V[3] if 'T' == i[0] and '53' not in i]
s_idx,s_wgt={},{}
for v in towns:
  s_idx.update({v:np.where(nc.variables[v][0,0,:,:]>0.)})
  srs=np.array(list(nc[v][0,0,s_idx[v][0][:],s_idx[v][1][:]]))
  sum_srs=np.sum(srs)
  s_wgt.update({v:srs.flatten()/sum_srs})

fname=sys.argv[1]
nc=netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
p=V[3][0]
srs=[np.dot(nc[p][0,0,s_idx[v][0][:],s_idx[v][1][:]].flatten(),s_wgt[v]) for v in towns]
df=DataFrame({fname:srs})
df['town']=[int(i[1:])%1000 for i in towns]
df['cnty']=[int(i[1:])//1000 for i in towns]
df=df.sort_values(fname,ascending=False).reset_index(drop=True)
col=['cnty','town',fname]
df[col].set_index('cnty').to_csv(fname+'.csv',header=None)
