import numpy as np
from pandas import *
from PseudoNetCDF.camxfiles.Memmaps import uamiv
import netCDF4
import matplotlib.pyplot as plt
from scipy.io import FortranFile

fnameO = 'PMf13_12_124_137_83.bin'
year=[i for i in range(2007,2020)]
try:
  with FortranFile(fnameO, 'r') as f:
    pmf = f.read_record(dtype=np.float64)  
except:
  pmf=np.zeros(shape=(max(year)-min(year)+1,12,124,137, 83))-1
  for y in year:
    yr=str(y)
    for m in range(12):
      mm='{:02d}'.format(m+1)
      try:
        grd04=uamiv('/nas1/CAM-chem/'+yr+'/'+yr+mm+'/output/'+yr[2:4]+mm+'IC.S.grd04L','r')
        nt,nlay,nrow,ncol=grd04.variables['PM25'].shape
        pmf[y-min(year),m,:nt,:,:]=grd04.variables['PM25'][:,0,:,:]
      except:
        continue
  with FortranFile(fnameO, 'w') as f:
    f.write_record(pmf)
fname='/nas1/cmaqruns/2016base/data/land/epic_festc1.4_20180516/gridmask/TWN_CNTY_3X3.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]

df_cnty=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/cnty2.csv')
df_twnaq=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/town_aqstE.csv')
df_cnty.no=[int(i) for i in df_cnty.no]
intv=1
xlabels=[' ']
for y in year:
    xlabels.append('{:02d}'.format(y%100))
pmf=pmf.reshape(max(year)-min(year)+1,12, 124, 137, 83)
for i in range(len(df_cnty)):
    fig, ax = plt.subplots()
    n=df_cnty.loc[i,'cnty']
    plt.title(" PM2.5 of CAM-chem Simulations in "+n, loc='center' )
    plt.xlabel('Year(2digits)')
    plt.ylabel('PM2.5 (microgram/cubic meter)')
#   if df_cnty.loc[i,'no']<44:continue
    dct='CNTY_'+'{:02d}'.format(df_cnty.loc[i,'no'])
    if dct not in V[3]:continue
    data=[]
    for y in year:
        pm=[]
        for m in range(12):
            pp=(pmf[y-2007,m,:,:,:]*nc.variables[dct][0,0,:,:]).flatten()
            idx=np.where(pp>0)
            pm=pm+list(pp[idx])
        data.append(pm)
    ax.boxplot(data, showfliers=False)
    xticks=list(range(0,len(data)+1,intv))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, fontsize=8)
    plt.savefig('box_'+n+'.png')

