#$ cat /Users/TEDS/REAS3.1/ems_tmp/mkMon1.py
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


#hourly T2
wrf = netCDF4.Dataset('T2.nc','r')
ntw,nroww,ncolw=(wrf.variables['T2'].shape[i] for i in range(3))
#check the start time of wrf file
s=''
for i in wrf['Times'][0][:]:
  s+=i.decode('utf8')
if s!='2015-12-31_00:00:00' :sys.exit('wrf start time not right')
beg=datetime.datetime(2015,12,31)
wrf_time=[beg+datetime.timedelta(days=t/24.) for t in range(ntw)]
T2=np.array(wrf.variables['T2'][:,:,:])
one=np.ones(shape=T2.shape)
T2Hi=one/T2
wrf.close()

#monthly T2
nc=uamiv('d1.area','r')
T2Mi=np.array(nc.variables['PCL'][:,0,:,:])
#print(np.max(T2Mi))
#sys.exit()
nc.close()

#total REAS monthly emission are store in the first 12 records in fortBE.113.teds10.base00.nc

fname='fortBE.013.teds10.base00.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
slope=np.zeros(shape=(nc.NVARS,nrow,ncol))
intrc=np.zeros(shape=(nc.NVARS,nrow,ncol))
r_sqr=np.zeros(shape=(nc.NVARS,nrow,ncol))
VMn=np.zeros(shape=(nc.NVARS,12,nrow,ncol))
#store the monthly mean emissions
for v in range(nc.NVARS):
  if np.max(nc.variables[V[3][v]][:12,0,:,:])==0.: continue
  VMn[v,:,:,:]=nc.variables[V[3][v]][:12,0,:,:]
  for j in range(nrow):
    for i in range(ncol):
      Y=nc.variables[V[3][v]][:12,0,j,i]
      X=T2Mi[:,j,i].reshape(-1,1)
      model = LinearRegression().fit(X, Y)
      r_sqr[v,j,i] = model.score(X, Y)
      intrc[v,j,i] = model.intercept_
      slope[v,j,i] = model.coef_
nc.close()

#prepare the template
mon=int(sys.argv[1])
MM='{:02d}'.format(mon)
fname='fortBE.013.teds10.base'+MM+'.nc'
#os.system('cp fortBE.013.teds10.base01.nc '+fname)
nc = netCDF4.Dataset(fname,'r+')
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))

begdt=datetime.datetime(2016,mon,1,0,0)-datetime.timedelta(days=1)
SDATE=dt2jul(begdt)
nc.SDATE, nc.STIME=(SDATE[:])
#write the time flags
for t in range(nt):
  now=begdt+datetime.timedelta(days=t/24.)
  SDATE=dt2jul(now)
  for i in range(2):
    nc.variables['TFLAG'][t,:,i]=[SDATE[i] for j in range(nc.NVARS)]
for v in V[3]:
  nc.variables[v][:,0,:,:]=np.zeros(shape=(nt,nrow,ncol))
for v in range(nc.NVARS):
  if np.max(VMn[v,:,:,:])==0.: continue
  for j in range(nrow):
    for i in range(ncol):
      if r_sqr[v,j,i]<0.2:
        nc.variables[V[3][v]][:,0,j,i]=[VMn[v,mon-1,j,i] for t in range(nt)]
      else:
        # calc. the emission with regression slopes and interc.
        for t in range(nt):
          now=begdt+datetime.timedelta(days=t/24.)
          try:
            inow=wrf_time.index(now)
          except:
            inow=0
          nc.variables[V[3][v]][t,0,j,i]=max(0.,slope[v,j,i]*T2Hi[inow,j,i]+intrc[v,j,i])
  print(v,V[3][v])
nc.close()
