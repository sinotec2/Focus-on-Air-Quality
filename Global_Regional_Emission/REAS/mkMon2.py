#$ cat /Users/TEDS/REAS3.1/ems_tmp/mkMon2.py
import numpy as np
import netCDF4
import os,sys
import datetime
import subprocess
from PseudoNetCDF.camxfiles.Memmaps import uamiv
from sklearn.linear_model import LinearRegression


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


#hourly T2
wrf = netCDF4.Dataset('T2.nc','r')
ntw,nroww,ncolw=(wrf.variables['T2'].shape[i] for i in range(3))
#check the start time of wrf file
s=''.join([i.decode('utf8') for i in wrf['Times'][0][:]])
if s!='2015-12-31_00:00:00' :sys.exit('wrf start time not right')
beg=datetime.datetime(2015,12,31)
wrf_time=[beg+datetime.timedelta(days=t/24.) for t in range(ntw)]
T2=np.array(wrf.variables['T2'][:,:,:])
one=np.ones(shape=T2.shape)
T2Hi=one/T2
wrf.close()

#monthly T2
T2Mi=np.zeros(shape=(12,nroww,ncolw))
for m in range(12):
  mdate=np.array([t for t in range(ntw) if wrf_time[t].month==m+1])
  T2Mi[m,:,:]=np.mean(T2[mdate,:,:],axis=0)

#total REAS monthly emission are store in the first 12 records in fortBE.?13.teds10.base00.nc
#base00 is the result of $bs/data/emis/camx2cmaqd?.job
fname='fortBE.213.teds10.base00.nc'
nc = netCDF4.Dataset(fname,'r')
Vm=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[Vm[3][0]].shape[i] for i in range(4))
if nrow<nroww:
  ib=int((nroww-nrow)/2)
  T2Hi=T2Hi[:,ib:-ib,:]
  T2Mi=T2Mi[:,ib:-ib,:]
if ncol<ncolw:
  ib=int((ncolw-ncol)/2)
  T2Hi=T2Hi[:,:,ib:-ib]
  T2Mi=T2Mi[:,:,ib:-ib]
slope=np.zeros(shape=(nc.NVARS,nrow,ncol))
intrc=np.zeros(shape=(nc.NVARS,nrow,ncol))
r_sqr=np.zeros(shape=(nc.NVARS,nrow,ncol))
VMn=np.zeros(shape=(nc.NVARS,12,nrow,ncol))
#store the monthly mean emissions
for v in range(nc.NVARS):
  if np.max(nc.variables[Vm[3][v]][:12,0,:,:])==0.: continue
  VMn[v,:,:,:]=nc.variables[Vm[3][v]][:12,0,:,:]
  for j in range(nrow):
    for i in range(ncol):
      Y=nc.variables[Vm[3][v]][:12,0,j,i]
      X=T2Mi[:,j,i].reshape(-1,1)
      model = LinearRegression().fit(X, Y)
      r_sqr[v,j,i] = model.score(X, Y)
      intrc[v,j,i] = model.intercept_
      slope[v,j,i] = model.coef_
nc.close()

#prepare the template
mon=int(sys.argv[1])
MM='{:02d}'.format(mon)
fname='fortBE.213.teds10.base'+MM+'.nc'
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))

begdt=jul2dt([nc.SDATE,nc.STIME])

for v in V[3]:
  nc.variables[v][:,0,:,:]=np.zeros(shape=(nt,nrow,ncol))
now=[begdt+datetime.timedelta(days=t/24.) for t in range(nt)]
inow=[wrf_time.index(now[t])  for t in range(nt)]

for v in range(nc.NVARS):
  if V[3][v] not in Vm[3]:continue
  iv=Vm[3].index(V[3][v])
  if np.max(VMn[iv,:,:,:])==0.: continue
  for j in range(nrow):
    for i in range(ncol):
      if r_sqr[iv,j,i]<0.2:
        nc.variables[V[3][v]][:,0,j,i]=[VMn[iv,mon-1,j,i] for t in range(nt)]
      else:
        # calc. the emission with regression slopes and interc.
        for t in range(nt):
          nc.variables[V[3][v]][t,0,j,i]=max(0.,slope[iv,j,i]*T2Hi[inow[t],j,i]+intrc[iv,j,i])
  print(mon,v,V[3][v],Vm[3][iv])
nc.close()
