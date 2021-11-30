#!/opt/miniconda3/envs/gribby/bin/python
import pygrib
import numpy as np
import netCDF4
from scipy.io import FortranFile
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
import datetime
import os
import subprocess

def buck(K):
    C=K-273.
    return 611.21*np.exp((18.678-C/234.5)*C/(257.14+C))


fname='wrfout_d04'
tmax=36+1
nc = netCDF4.Dataset(fname,'r+')
Vs=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt1,nrow1,ncol1=(nc.variables['U10'].shape[i] for i in range(3))

path='/Users/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/raw/'
path='/home/cpuff/UNRESPForecastingSystem/CWB_data/raw/'
path='/nas1/backup/data/CWB_data/raw/'
path='/Users/Data/cwb/WRF_3Km/'
path='/nas1/Data/cwb/WRF_3Km/'
f=FortranFile(path+'idxD4.bin', 'r')
idx=f.read_record(dtype=np.int64)
idx=idx.reshape(nrow1,ncol1,2)

f=FortranFile(path+'wtsD4.bin', 'r')
wts=f.read_record(dtype=np.float64)
wts=wts.reshape(nrow1,ncol1,4)

one=np.ones(shape=(nrow1,ncol1),dtype=np.int64)
atbs={'U10': '10 metre U wind component',
 'V10': '10 metre V wind component',
 'T': 'Temperature',
 'V': 'V component of wind',
 'U': 'U component of wind',
 'W': 'Geometric vertical velocity',
 'QVAPOR': 'Relative humidity',
 'T2': '2 metre temperature',
 'SST': 'Temperature',
 'TSK': 'Skin temperature',
 'SWNORM': 'Net short-wave radiation flux (surface)',
 'SWDOWN': 'Net short-wave radiation flux (surface)',
 'PHB': 'Geopotential Height',
 'PSFC': 'Surface pressure',
 'RAINC':'Total precipitation'}
atbs2=[]
for v in atbs:
  if v in Vs[2]:atbs2.append(v)
#'U10','V10','T2','SWNORM','SWDOWN','PSFC','SST','TSK']
#atbs2.append('TSLB') #3d in grb but 4d in wrfout
b=[t for t in range(0,tmax)]
for a in atbs:
  if a in atbs2:
    exec('s'+a+'=np.zeros(shape=(tmax,nrow1,ncol1),dtype=np.float64)')
  else:
    exec('s'+a+'=np.zeros(shape=(tmax,11,nrow1,ncol1),dtype=np.float64)')
 #'GPH': 'Geopotential Height',

lv=[i for i in range(10,-1,-1)]
PB,level=[],[]

for t in range(0,tmax,6):
  fname='M-A0064-0'+'{:02d}'.format(t)+'.grb2'
  grbs = pygrib.open(fname)

  for a in set(atbs)-set(['RAINC']):
    grb = grbs.select(name=atbs[a])
    if len(grb)==1:
      cmd=a+'=grb[0].values'
      exec(cmd)
    else:
      arr=[]
      for k in range(11):
        arr.append(grb[lv[k]].values)
      arr=np.array(arr)
      exec(a+'=arr')
    if len(grb)==11 and len(level)==0:
      level=[grb[lv[i]].level for i in range(11)]
    if len(grb)==12 and a=='SST':SST=grb[11].values
  nlay,nrow,ncol=QVAPOR.shape
  if len(PB)==0:
    PB=np.ones(shape=(nlay,nrow,ncol),dtype=np.int64)
    for k in range(nlay):
      PB[k,:,:]=level[k]*100
  ps=buck(T)
  QVAPOR=QVAPOR/100.*(ps*18.)/(PB*28.)
  
  a='RAINC'
  if t==0:rain_old=np.zeros(shape=(nrow,ncol))
  t6=min([t+6,84])
  fname='M-A0064-0'+'{:02d}'.format(t6)+'.grb2'
  try:
    rain_acc=pygrib.open(fname)[62].values
  except:
    rain_acc=rain_old
  arr=(rain_acc-rain_old)/6. #average along 6 hrs
  exec(a+'=arr')
  rain_old[:]=rain_acc[:]

  for a in atbs:
    exec('var='+a)
    n=var.ndim
    if n==2:
      kk=0
      for jj in [0,1]:
        for ii in [0,1]:
          vr=var[idx[:,:,0]+one*jj,idx[:,:,1]+one*ii]
          exec('s'+a+'[t,:,:]+=vr[:,:]*wts[:,:,kk]')
          kk+=1
    elif n==3:
      for k in range(11):
        kk=0
        for jj in [0,1]:
          for ii in [0,1]:
            vr=var[k,idx[:,:,0]+one*jj,idx[:,:,1]+one*ii]
            exec('s'+a+'[t,k,:,:]+=vr[:,:]*wts[:,:,kk]')
            kk+=1
#time stamps
  if t==0:
    V=grbs[1]
    beg_time=V.analDate
    if beg_time.hour != 6:
      beg_time=beg_time-datetime.timedelta(days=beg_time.hour/24)+datetime.timedelta(days=6/24)

X=[i for i in range(0,tmax,6)]
Hstart=14 #begin local time(20 for CAMx, 14 for fitting WRF GMT 0600)
for t in range(0,tmax):
  time=beg_time+datetime.timedelta(days=t/24.)
  b[t]=np.array([bytes(i,encoding='utf-8') for i in time.strftime("%Y-%m-%d_%H:%M:%S")])
wname=''
for i in b[0]:
  wname+=i.decode('utf-8')

for a in atbs2:
  exec('ss=np.array([s'+a+'[t,:,:]   for t in range(0,tmax,6)])')
  cs = CubicSpline(X,ss)
  for t in range(0,tmax):
    if t%6==0:continue
    exec('s'+a+'[t,:,:]=cs(t)')
  if a == 'TSLB':
    exec('nc.variables["'+a+'"][:,0,:nrow1,:ncol1]=s'+a+'[Hstart-14:Hstart+10,:,:]')
  else:
    exec('nc.variables["'+a+'"][:,:,:]=s'+a+'[Hstart-14:Hstart+10,:,:]')

for a in set(atbs)-set(atbs2):
  exec('ss=np.array([s'+a+'[t,:,:,:] for t in range(0,tmax,6)])')
  cs = CubicSpline(X,ss)
  for t in range(0,tmax):
    if t%6==0:continue
    exec('s'+a+'[t,:,:,:]=cs(t)')
  exec('nc.variables["'+a+'"][:,:nlay,:nrow1,:ncol1]=s'+a+'[Hstart-14:Hstart+10,:,:,:]')

#pressure
v='PB'
nt,nlay,nrow,ncol=nc.variables[v].shape
for k in range(nlay):
  nc.variables[v][:,k,:,:]=level[k]*100.
nc.variables['P'][:]=0.

#geopotential heights
v='PHB'
nc.variables['PH'][:]=0.
PHB=nc.variables[v][:]*9.8
PHBm=np.mean(PHB,axis=0) #const in time
PH=PHB[:,:,:,:]-PHBm[None,:,:,:]
PHBm=PHB-PH
#surface geopotential height=HGT*9.8
HGT=nc.variables['HGT'][:,:,:]*9.8
for k in range(nlay):
  nc.variables['PH'][:,k+1,:,:]=PH[:,k,:,:]
nc.variables[v][:,0,:,:]=HGT 
for k in range(nlay):
  nc.variables[v][:,k+1,:,:]=PHBm[:,k,:,:]+HGT[0,:,:]

#potential temperature
v='T' #WRF is temp "pertubation"
PB,TK=nc.variables['PB'][:],nc.variables[v][:]
nc.variables[v][:]=TK*(100000./PB)**0.286
nc.variables[v][:]-=nc.variables['T00'][0] 

#T2->TSK
nc.variables['TSK'][:]=nc.variables['T2'][:] 

v='RAINC'
for t in range(1,24):
  nc.variables[v][t,:,:]+=nc.variables[v][t-1,:,:]

v='PBLH'
#PBLH=nc.variables[v][:]
#for t in range(24):
#  t_wrf=(t+6)%24
#  nc.variables[v][t,:,:]=PBLH[t_wrf,:,:]
T0=nc.variables['T2'][:]*(100000./nc.variables['PSFC'][:])**0.286
T=nc.variables['T'][:]+290
H=(nc.variables['PH'][:]+nc.variables['PHB'][:])/9.8
nt,nlay,nrow,ncol=(H.shape[i] for i in range(4))
nk=nlay-1
HT=np.zeros(shape=T.shape)
for k in range(nk):
  HT[:,k,:,:]=(H[:,k,:,:]+H[:,k+1,:,:])/2.-H[:,0,:,:]

mixH=np.zeros(shape=T0.shape)
minT=np.min(T,axis=1)
idx=np.where(T0<=minT)
HT0=np.array([max(35,i) for i in HT[:,0,:,:].flatten()]).reshape(HT[:,0,:,:].shape)
mixH[idx[:]]=HT0[idx[:]]

#potential temperature vertical profile is increasingly sorted
dT=np.diff(T,axis=1)
dTmin=np.min(dT,axis=1)
idx=np.where((dTmin>=0)&(T0>minT))
for n in range(len(idx[0])):
  t,j,i=(idx[k][n] for k in range(3))
  f=interp1d(T[t,:,j,i],HT[t,:,j,i]) 
  mixH[t,j,i]=f(T0[t,j,i])

#with inversions
idx=np.where((dTmin<0)&(T0>minT))
for n in range(len(idx[0])):
  t,j,i=(idx[k][n] for k in range(3))
  k=list(dT[t,:,j,i]).index(dTmin[t,j,i])+1
  mixH[t,j,i]=HT[t,k,j,i]
nc.variables[v][:]=mixH[:]

v='Times'
nc.variables[v][:,:]=b[Hstart-14:Hstart+10][:]
btime= beg_time.strftime("%Y-%m-%d_%H:%M:%S")
nc.SIMULATION_START_DATE=btime
nc.START_DATE           =btime
yr=beg_time.year
nc.JULYR                =yr
nc.JULDAY               =int((beg_time-datetime.datetime(yr,1,1)).total_seconds()/24/3600.)+1
nc.close()
ncatted=subprocess.check_output('which ncatted',shell=True).decode('utf8').strip('\n')
os.system(ncatted+' -a BOTTOM-TOP_GRID_DIMENSION,global,o,i,12 wrfout_d04')
os.system('mv wrfout_d04 wrfout_d04_'+wname)
