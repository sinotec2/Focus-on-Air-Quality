import netCDF4
import numpy as np
from pandas import *
import sys

fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v=V[3][0]
df=read_csv('gridLL.csv')
df.TOWNCODE=['{:08d}'.format(i) for i in df.TOWNCODE]
df.COUNTYCODE=['{:05d}'.format(i) for i in df.COUNTYCODE]
tn={i:j for i,j in zip(df.TOWNCODE, df.TOWNNAME)}
cn={i:j for i,j in zip(df.COUNTYCODE, df.COUNTYNAME)}

df['var']=np.array(nc[v][0,0,:,:]).flatten()
df0=df.loc[df['var']>0].reset_index(drop=True)
df_tm=pivot_table(df0,index='COUNTYCODE',values='var',aggfunc=np.mean).reset_index()
df_tm=df_tm.sort_values('var',ascending=False)
df_tm['COUNTYNAME']=[cn[i] for i in df_tm.COUNTYCODE]
df_tm.set_index('COUNTYCODE').to_csv(fname+'_cnty.csv')
