#kuang@master /nas1/TEDS/REAS3.1/ems_tmp
#$ cat  mkMon3.py
import numpy as np
import netCDF4
import os,sys
import datetime
import subprocess
from PseudoNetCDF.camxfiles.Memmaps import uamiv
from sklearn.linear_model import LinearRegression
from calendar import monthrange
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

def rd_wrf(wrfname):
  wrf = netCDF4.Dataset(','r')
  ntw,nroww,ncolw=(wrf.variables['T2'].shape[i] for i in range(3))
  #check the start time of wrf file
  s=''.join([i.decode('utf8') for i in wrf['Times'][0][:]])
  if s!='2014-12-31_00:00:00' :sys.exit('wrf start time not right')
  beg=datetime.datetime(2015,12,31)
  T2=wrf.variables['T2'][:,:,:]
  one=np.ones(shape=T2.shape)
  T2Hi=one/T2
  wrf_time=[beg+datetime.timedelta(days=t/24.) for t in range(ntw)]
  dtm=np.array([(beg+datetime.timedelta(days=i/24.)).month for i in range(ntw)],dtype=int)
#monthly T2
  T2=np.zeros(shape=(12,nroww,ncolw))
  for m in range(1,13):
    idx=np.where(dtm==m)
    T2[m-1,:,:]=np.mean(wrf.variables['T2'][idx[0],:,:])
  one=np.ones(shape=T2.shape)
  T2Mi=one/T2
  wrf.close()
  return ntw,nroww,ncolw,T2Hi,T2Mi
def ck_Ti(nrow,nroww,ncol,ncolw,T2Hi,T2Mi):
  if nrow<nroww:
    ib=int((nroww-nrow)/2)
    T2Hi=T2Hi[:,ib:-ib,:]
    T2Mi=T2Mi[:,ib:-ib,:]
  if ncol<ncolw:
    ib=int((ncolw-ncol)/2)
    T2Hi=T2Hi[:,:,ib:-ib]
    T2Mi=T2Mi[:,:,ib:-ib]
  return T2Hi,T2Mi
#hourly T2
DOM=sys.argv[2] #DOM=d1 or d2
wrfname='/nas1/backup/data/cwb/e-service/btraj_WRFnests/2015T2_'+DOM+'/T2.nc'
ntw,nroww,ncolw,T2Hi,T2Mi=rd_wrf(wrfname)

#total REAS monthly emission are store in the first 12 records in fortBE.?13.teds10.base00.nc
#base00 is the result of $bs/data/emis/camx2cmaqd?.job
fname='../join_spec/'+DOM+'L.area'
nc = uamiv(fname,'r')
Vm=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[Vm[3][0]].shape[i] for i in range(4))
T2Hi,T2Mi=ck_Ti(nrow,nroww,ncol,ncolw,T2Hi,T2Mi)
slope=np.zeros(shape=(nc.NVARS,nrow,ncol))
intrc=np.zeros(shape=(nc.NVARS,nrow,ncol))
r_sqr=np.zeros(shape=(nc.NVARS,nrow,ncol))
VMn=np.zeros(shape=(nc.NVARS,12,nrow,ncol))
yr=2016
mon=int(sys.argv[1])
ntm=(monthrange(yr,mon)[1])*24
#store the monthly mean emissions(gmole/month)
for v in range(nc.NVARS):
  if np.max(nc.variables[Vm[3][v]][:12,0,:,:])==0.: continue
  VMn[v,:,:,:]=nc.variables[Vm[3][v]][:12,0,:,:] #gmole/hr(monthly avrg)
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
MM='{:02d}'.format(mon)
pth='/nas1/camxruns/2016_v7/emis/area/'
fname=pth+'fortBE.'+DOM[1]+'13_REAS3.base'+MM
fnameO=fname+'_T2'
res=os.system('cp '+fname+' '+fnameO)
nc = uamiv(fnameO,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))

begdt=jul2dt([nc.SDATE,nc.STIME])+datetime.timedelta(days=-8/24.)

for v in V[3]:
  nc.variables[v][:,0,:,:]=0.
now=[begdt+datetime.timedelta(days=t/24.) for t in range(nt)]
inow=[wrf_time.index(now[t])  for t in range(nt)]

wrfname='/nas1/backup/data/cwb/e-service/btraj_WRFnests/'+str(yr)+'T2_'+DOM+'/T2.nc'
ntw,nroww,ncolw,T2Hi,T2Mi=rd_wrf(wrfname)
T2Hi,T2Mi=ck_Ti(nrow,nroww,ncol,ncolw,T2Hi,T2Mi)

for v in range(nc.NVARS):
  if V[3][v] not in Vm[3]:continue
  iv=Vm[3].index(V[3][v])
  if np.max(VMn[iv,:,:,:])==0.: continue
  z=np.zeros(shape=(nt,nrow,ncol))
  idx=np.where(r_sqr[iv,:,:]<0.2)
  if len(idx[0])>0:
    z[:,idx[0][:],idx[1][:]]=[VMn[iv,mon-1,idx[0][:],idx[1][:]] for t in range(nt)]
  idx=np.where(r_sqr[iv,:,:]>=0.2)
  if len(idx[0])>0:
  # calc. the emission with regression slopes and interc.
    for t in range(nt):
      a=slope[iv,idx[0][:],idx[1][:]]*T2Hi[inow[t],idx[0][:],idx[1][:]]+intrc[iv,idx[0][:],idx[1][:]]
      z[t,idx[0][:],idx[1][:]]=np.clip(a,0,np.max(a))
#promicing the mass conservations,due to non-linear interpolations
  sumv=np.sum(z[:,:,:])/ntm
  sumo=np.sum(VMn[iv,mon-1,:,:])
  nc.variables[V[3][v]][:,0,:,:]=z[:,:,:]*sumo/sumv
  print(mon,v,V[3][v],Vm[3][iv],sumo,sumv)
nc.close()
