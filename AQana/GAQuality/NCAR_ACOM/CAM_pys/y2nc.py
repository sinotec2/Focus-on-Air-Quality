import numpy as np
from pandas import *
import netCDF4
import sys, datetime

def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)

def jul2dt(jultm):
  jul,tm=jultm[:]
  yr=int(jul/1000)
  ih=int(tm/10000.)
  return datetime.datetime(yr,1,1)+datetime.timedelta(days=int(jul-yr*1000-1))+datetime.timedelta(hours=ih)

csv=sys.argv[1]
dfv=read_csv(csv)
ymd=list(set(dfv.ymd))
ymd.sort()
beg=ymd[0]
bdate=datetime.datetime(beg//10000,beg//100%100, beg%100)

dc = netCDF4.Dataset('20160101.ncT','r')#fraction of towns
Vd=[list(filter(lambda x:dc.variables[x].ndim==j, [i for i in dc.variables])) for j in [1,2,3,4]]

nc = netCDF4.Dataset('PM25_TOT.nc','r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
if len(ymd)>nt:sys.exit('template length not enough')
delt=8766
nc.TSTEP=delt*10000
nc.STIME=0.
iyb=int(beg//10000)
nc.SDATE=int(iyb*1000+1)
nc.NVARS=1
v='TFLAG'
for t in range(len(ymd)):
    nc.variables[v][t,0,0]=(iyb+t)*1000+1
    nc.variables[v][t,0,1]=0
zz=np.zeros(shape=(nrow,ncol))
v=V[3][0]
for t in range(len(ymd)):
    nc.variables[v][t,0,:,:]=zz
    symd=ymd[t]
    a=dfv.loc[dfv.ymd==symd].reset_index(drop=True)
    for i in range(len(a)):
        ii=a.loc[i,'s']
        dct='T'+str(ii)
        if dct not in Vd[3]:continue
        nc.variables[v][t,0,:,:]+=dc.variables[dct][0,0,:,:]*a.loc[i,'v']
nc.close()
