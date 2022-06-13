import numpy as np
from pandas import *
from PseudoNetCDF.camxfiles.Memmaps import uamiv
import netCDF4
import matplotlib.pyplot as plt
from scipy.io import FortranFile
import sys,os,datetime


#model pm results
fnameO = 'PMf13_12_124_137_83.bin'
year=[i for i in range(2007,2020)]
try:
  with FortranFile(fnameO, 'r') as f:
    pmm = f.read_record(dtype=np.float64)  
except:
  pmm=np.zeros(shape=(max(year)-min(year)+1,12,124,137, 83))-1
  for y in year:
    yr=str(y)
    for m in range(12):
      mm='{:02d}'.format(m+1)
      try:
        grd04=uamiv('/nas1/CAM-chem/'+yr+'/'+yr+mm+'/output/'+yr[2:4]+mm+'IC.S.grd04L','r')
        nt,nlay,nrow,ncol=grd04.variables['PM25'].shape
        pmm[y-min(year),m,:nt,:,:]=grd04.variables['PM25'][:,0,:,:]
      except:
        continue
  with FortranFile(fnameO, 'w') as f:
    f.write_record(pmm)
# observation PM2.5 (21 year,13 month, 24 hours, 608 stations
fnameO = 'PMf21_13_32_24_608.bin'
with FortranFile(fnameO, 'r') as f:
  pmf = f.read_record(dtype=np.float64)


fname='/nas1/cmaqruns/2016base/data/land/epic_festc1.4_20180516/gridmask/TWN_CNTY_3X3.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape

df_cnty=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/cnty2.csv')
df_twnaq=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/town_aqstE.csv')
df_cnty.no=[int(i) for i in df_cnty.no]
df_ll=read_csv('sta_ll.csv')
intv=1
delH=6
AQD={'Northern':[1,11,12,31,32,33,35],'Central':[17,22,36,37,38,39,40],'Southern':[2,21,41,42,43]}
NCS=[i for i in AQD]
pmm=pmm.reshape(max(year)-min(year)+1,12, 124, 137, 83)
pmf=pmf.reshape(2020-2000+1,13,32,24,608)
obs=np.ones(shape=(2020-2000+1,12,124,53))
sim=np.ones(shape=(2020-2000+1,12,124,53))
si={}
for ii in range(len(df_cnty)):
  i=df_cnty.loc[ii,'no']
  a=df_twnaq.loc[df_twnaq.code1==i,'aq_st']
#  if len(a)==0:continue
  s=set()
  for j in a:
    s=s|set(j.split(';'))
#  if len(s)==0 or s==set(['0']):continue
  s=[int(j) for j in s if len(j)>0 and j!='0']
  si.update({i:s})

sx,sy={},{}
for ii in range(len(df_cnty)):
  i=df_cnty.loc[ii,'no']
  ixx,iyy=[],[]
  for jj in si[i]:
    if jj not in list(df_ll.ID):continue
    lx=list(df_ll.loc[df_ll.ID==jj,'lcp_x'])[0]
    ly=list(df_ll.loc[df_ll.ID==jj,'lcp_y'])[0]
    ix=int((lx-nc.XORIG)//nc.XCELL)
    iy=int((ly-nc.YORIG)//nc.YCELL)
    if ix*(ix-ncol+1)>=0 or iy*(iy-nrow+1)>=0:continue
    ixx.append(ix)
    iyy.append(iy)
  sx.update({i:ixx})
  sy.update({i:iyy})
for y in year:
  for m in range(12):
    bdate=datetime.datetime(y,m+1,1)  
    for t in range(124): 
      tdate=bdate+datetime.timedelta(days=(t*delH+8)/24)
      if tdate>datetime.datetime(2019,6,30):continue
      tdate=tdate.strftime("%Y%m%d%H")
      yr,mn,da,hr=int(tdate[:4]),int(tdate[4:6]),int(tdate[6:8]),int(tdate[8:])    
      yo=yr-2000
      yy=yr-min(year)
      for ii in range(len(df_cnty)):
        i=df_cnty.loc[ii,'no']
        if si[i]==['0'] or len(si[i])==0:continue
        try:
          obs[yy,m,t,i]=np.average(pmf[yo,mn,da,hr,si[i]],weights=(pmf[yo,mn,da,hr,si[i]]>0))
        except:
          obs[yy,m,t,i]=-1
        try:
          sim[yy,m,t,i]=np.average(pmm[yy,m,t,sy[i],sx[i]],weights=(pmm[yy,m,t,sy[i],sx[i]]>0))
        except:
          sim[yy,m,t,i]=-1
  avg=np.average(obs[yy,:,:,:],weights=(obs[yy,:,:,:]>0))
  idx=np.where(obs[yy,:,:,:]<=0)
  obs[yy,idx[0],idx[1],idx[2]]=avg
  avg=np.average(sim[yy,:,:,:],weights=(sim[yy,:,:,:]>0))
  idx=np.where(sim[yy,:,:,:]<=0)
  sim[yy,idx[0],idx[1],idx[2]]=avg
xlabels=[' ']
for y in year:
  if y%2==0:continue
  for d in AQD:
    if d[0]=='N':
      xlabels.append('{:02d}'.format(y%100)+'_'+d[0])
    else:
      xlabels.append(d[0])
fig, ax = plt.subplots()
plt.title(" PM2.5 of CAM-chem Simulations(w/t correction)", loc='center' )
plt.xlabel('Year(2digits)')
plt.ylabel('PM2.5 (microgram/cubic meter)')
#   if df_cnty.loc[i,'no']<44:continue
data=[]
for y in year[:-1]:
  if y%2==0:continue
  for d in AQD:
    pm=[]
    for i in AQD[d]:
      dct='CNTY_'+'{:02d}'.format(i)
      if dct not in V[3]:continue
      pp=(pmm[y-2007,:,:,:,:]*nc.variables[dct][0,0,:,:]).flatten()
      if np.sum(sim[y-2007,:,:,i])<=0:continue #sys.exit('sim<=0 '+dct)
      rat=obs[y-2007,:,:,i]/sim[y-2007,:,:,i]
      rat=np.tile(rat,(nrow,ncol)).flatten()
      idx=np.where(pp>0)
      pr=pp[idx]*rat[idx]
      idx=np.where(pr>0)
      pm=pm+list(pr[idx])
    data.append(pm)
ax.boxplot(data, showfliers=False)
xticks=list(range(0,len(data)+1,intv))
ax.set_xticks(xticks)
ax.set_xticklabels(xlabels, fontsize=8)
plt.savefig('box_AQD.png')

