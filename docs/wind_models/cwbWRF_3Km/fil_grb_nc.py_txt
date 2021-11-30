#!/opt/anaconda3/envs/gribby/bin/python
import pygrib
import numpy as np
import netCDF4
from scipy.io import FortranFile
from scipy.interpolate import CubicSpline
from scipy.interpolate import interp1d
import datetime
import os, sys
import subprocess


def buck(K):
    C=K-273.
    return 611.21*np.exp((18.678-C/234.5)*C/(257.14+C))

#parameter settings
M14={661:'1',1158:'4'}
tmax=84+1
path='/Users/Data/cwb/WRF_3Km/'
#OPEN THE TEMPLATE
fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r+')
Vs=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt1,nrow1,ncol1=(nc.variables['U10'].shape[i] for i in range(3))
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
#'U10','V10','T2','SWNORM','SWDOWN','PSFC','SST']
#atbs2.append('TSLB') #3d in grb but 4d in wrfout
#FILL THE lon/lat FROM NC FILE(s)
root='M-A006'+M14[ncol1]
fname=path+root+'-0'+'{:02d}'.format(84)+'.nc'
nc1= netCDF4.Dataset(fname,'r')
lon,lat=nc1.variables['gridlon_0'][:,:],nc1.variables['gridlat_0'][:,:]
nc1.close()
dll={'XLAT':lat,'XLONG':lon}
for ll in ['XLAT','XLONG']:
  for t in range(max(nt1,tmax)):
    nc.variables[ll][t,:,:]=dll[ll][:,:]
#store the constants before time stretching
sV=Vs[0]+Vs[1]+Vs[2]+Vs[3]
sV=[i for i in sV if i not in set(atbs)|set(atbs2) and 'Time' in nc.variables[i].dimensions and i != 'Times']
for v in sV:
  exec(v+'=nc.variables["'+v+'"][:]')

#time stamps
fname=root+'-0'+'{:02d}'.format(0)+'.grb2'
grbs = pygrib.open(fname)
V=grbs[1]
beg_time=V.analDate
if beg_time.hour != 6:
  beg_time=beg_time-datetime.timedelta(days=beg_time.hour/24)+datetime.timedelta(days=6/24)
b=[t for t in range(0,tmax)]
for t in range(0,tmax):
  time=beg_time+datetime.timedelta(days=t/24.)
  b[t]=np.array([bytes(i,encoding='utf-8') for i in time.strftime("%Y-%m-%d_%H:%M:%S")])
wname=''
for i in b[0]:
  wname+=i.decode('utf-8')
v='Times'
nc.variables[v][:,:]=[b[t][:] for t in range(tmax)]
for v in sV:
  if nc.variables[v].ndim==1:
    exec('nc.variables["'+v+'"][:]='+v+'[0]')
  elif nc.variables[v].ndim==2:
    exec(v+'='+v+'[0,:]')
    exec('nc.variables["'+v+'"][:,:]='+v+'[None,:]')
  elif nc.variables[v].ndim==3:
    exec(v+'='+v+'[0,:,:]')
    exec('nc.variables["'+v+'"][:,:,:]='+v+'[None,:,:]')
  elif nc.variables[v].ndim==4:
    exec(v+'='+v+'[0,:,:,:]')
    exec('nc.variables["'+v+'"][:,:,:,:]='+v+'[None,:,:,:]')

one=np.ones(shape=(nrow1,ncol1),dtype=np.int64)
b=[t for t in range(0,tmax)]
for a in atbs:
  if a in atbs2:
    exec('s'+a+'=np.zeros(shape=(tmax,nrow1,ncol1),dtype=np.float64)')
  else:
    exec('s'+a+'=np.zeros(shape=(tmax,11,nrow1,ncol1),dtype=np.float64)')

lv=[i for i in range(10,-1,-1)]
PB,level=[],[]


for t in range(0,tmax,6):
  fname=root+'-0'+'{:02d}'.format(t)+'.grb2'
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
      level=np.array([grb[lv[i]].level for i in range(11)])
    if len(grb)==12 and a=='SST':SST=grb[11].values
  nlay,nrow,ncol=QVAPOR.shape
  if len(PB)==0:
    PB=np.ones(shape=(nlay,nrow,ncol),dtype=np.int64)
    PB[:,:,:]=level[:,None,None]*100.
  ps=buck(T)
  QVAPOR=QVAPOR/100.*(ps*18.)/(PB*28.)

  a='RAINC'
  if t==0:rain_old=np.zeros(shape=(nrow,ncol))
  t6=min([t+6,84])
  if 'd01' in sys.argv[1]:
    fname='M-A0061-0'+'{:02d}'.format(t6)+'.grb2'
  elif 'd03' in sys.argv[1]:
    fname='M-A0064-0'+'{:02d}'.format(t6)+'.grb2'
  else:
    sys.exit('wrong in sys.argv')  
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
      vr=var[:,:]
      exec('s'+a+'[t,:,:]=vr[:,:]')
    elif n==3:
      vr=var[:,:,:]
      for k in range(11):
        exec('s'+a+'[t,k,:,:]+=vr[k,:,:]')

X=[i for i in range(0,tmax,6)]
Hstart=20

for a in atbs2:
  exec('ss=np.array([s'+a+'[t,:,:]   for t in range(0,tmax,6)])')
  cs = CubicSpline(X,ss)
  for t in range(0,tmax):
    if t%6==0:continue
    exec('s'+a+'[t,:,:]=cs(t)')
  if a == 'TSLB':
    exec('nc.variables["'+a+'"][:,0,:nrow1,:ncol1]=s'+a+'[:,:,:]')#[Hstart-14:Hstart+10,:,:]')
  else:
    exec('nc.variables["'+a+'"][:,:,:]=s'+a+'[:,:,:]')#[Hstart-14:Hstart+10,:,:]')

for a in set(atbs)-set(atbs2):
  exec('ss=np.array([s'+a+'[t,:,:,:] for t in range(0,tmax,6)])')
  cs = CubicSpline(X,ss)
  for t in range(0,tmax):
    if t%6==0:continue
    exec('s'+a+'[t,:,:,:]=cs(t)')
  exec('nc.variables["'+a+'"][:,:nlay,:nrow1,:ncol1]=s'+a+'[:,:,:]')#[Hstart-14:Hstart+10,:,:,:]')

#pressure
v='PB'
nt,nlay,nrow,ncol=nc.variables[v].shape
nc.variables[v][:,:,:,:]=level[None,:,None,None]*100.
nc.variables['P'][:]=0.

#geopotential heights
v='PHB' #wrfout PHB means base, grb means total
nc.variables['PH'][:]=0.
PHT=nc.variables[v][:]*9.8 #grb total height, top will be overlayed
PHBm=np.mean(PHT,axis=0) #const in time
PH=PHT[:,:,:,:]-PHBm[None,:,:,:]
PHBm=PHT-PH
#nlay=11,overlay the top
PHK1=PH[:]
for k in range(11):
  PHK1[:,k+1,:,:]=PH[:,k,:,:]
nc.variables['PH'][:]=PHK1[:]
#surface geopotential height=HGT*9.8
HGT=nc.variables['HGT'][:,:,:]*9.8
nc.variables[v][:,0,:,:]=HGT[:,:,:]
for k in range(nlay):
  nc.variables[v][:,k+1,:,:]=PHBm[:,k,:,:]+HGT[:,:,:]

#potential temperature
v='T' #WRF is temp "pertubation"
PB,TK=nc.variables['PB'][:],nc.variables[v][:]
nc.variables[v][:]=TK*(100000./PB)**0.286
nc.variables[v][:]-=nc.variables['T00'][0]

#T2->TSK
nc.variables['TSK'][:]=nc.variables['T2'][:]

v='RAINC'
for t in range(1,tmax):
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

btime= beg_time.strftime("%Y-%m-%d_%H:%M:%S")
nc.SIMULATION_START_DATE=btime
nc.START_DATE           =btime
yr=beg_time.year
nc.JULYR                =yr
nc.JULDAY               =int((beg_time-datetime.datetime(yr,1,1)).total_seconds()/24/3600.)+1
nc.close()
ncatted='/usr/local/bin/ncatted' #subprocess.check_output('which ncatted',shell=True).decode('utf8').strip('\n')
os.system(ncatted+' -a BOTTOM-TOP_GRID_DIMENSION,global,o,i,12 '+sys.argv[1])
#os.system('mv wrfout_d03 wrfout_d03_'+wname)

