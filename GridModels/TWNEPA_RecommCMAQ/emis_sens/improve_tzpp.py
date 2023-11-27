import numpy as np
import sys,os, subprocess, netCDF4
from pandas import *
from pyproj import Proj
from dtconvertor import dt2jul, jul2dt

mm=sys.argv[1]
targ='/u01/cmaqruns/2019TZPP/output/2019-'+mm+'/grid03/smoke/'
root='/nas1/cmaqruns/2019base/data/ptse/twn/'
teds_cems='/nas1/TEDS/teds11/ptse/point_cems.csv'
fname=root+'fortBE.413_teds11.ptse'+mm+'.nc'
nc = netCDF4.Dataset(fname,'r')
v='CP_NO'
nopt,ii=nc[v].shape
L='L0200473'
cp_no=[''.join([str(i, encoding='utf-8') for i in nc[v][t,:]]) for t in range(nopt)]
LL=[i for i in cp_no if L in i]
L=LL[0]
v='stkheight';hei=nc[v][:]
v='ycoord';ycoord=nc[v][:]
df=DataFrame({'cp':cp_no,'hei':hei,'ycoord':ycoord})
tzpp=df.loc[(df.cp==L)&(df.hei==250)]
#matching the cems CP_NO and main database(with comfirmation of ycoords)
CP_NO=['L0200473P{:1d}01'.format(i) for i in range(1,9)]+['L0200473P01{:1d}'.format(i) for i in [1,2]]
tzpp['P_NO']=CP_NO
idx={cp:tzpp.loc[tzpp.P_NO==cp].index for cp in CP_NO} #no use! because two orders are just the same
l_tzpp=len(tzpp)


fname='teds11.19'+mm+'.timvar.nc'
fnamO='teds11.19'+mm+'.timvar.nci'
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
os.system(ncks+' -O -d ROW,1,'+str(l_tzpp)+' '+root+fname+' '+targ+fnamO)
nc0 = netCDF4.Dataset(root+fname,'r')
nc = netCDF4.Dataset(targ+fnamO,'r+')
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
nv=len(V[3])

#zeroing the tzpp emission to fill with old values
var=np.zeros(shape=(nv,nt,nlay,l_tzpp,ncol))
for v in V[3]:
  var4=nc0[v][:]
  iv=V[3].index(v)
  fac=1
  if v[0]=='P':fac=0.05 # 1-95%
  var[iv,:,:,:,:]=var4[:,:,tzpp.index,:]*fac

fname=targ+'cmaq.ncf'
nc00 = netCDF4.Dataset(fname,'r')
tflag0=nc00['TFLAG'][:,0,:]
sdatim=[i*100+j/100/100 for i,j in zip(tflag0[:,0],(tflag0[:,1]))]
nt0=len(tflag0[:,0])

# link the teds_cems flow rate (NM3/hr) to NM3/s
cems=read_csv(teds_cems)
dt0=[jul2dt(list(i)) for i in tflag0]
mdh=[int('{:02d}{:02d}{:02d}'.format(i.month,i.day,i.hour)) for i in dt0]
boo=(cems.MDH.map(lambda x:x in set(mdh))) & (cems.CP_NO.map(lambda x:x in CP_NO))
cems=cems.loc[boo].reset_index(drop=True)
flows=np.zeros(shape=(nt0,l_tzpp))
for cp in CP_NO:
  icp=CP_NO.index(cp)
  a=cems.loc[cems.CP_NO==cp].reset_index(drop=True)
  if len(a)==0:continue #P012 data missing
  flows[:,icp]=np.array(a.FLOW)/3600.
sn_conc=np.array([6.16/22.4, 17.62/22.4])/1000. #g-mole/NM3

#transfer to new timeframe
begd=nc.SDATE
begt=nc.STIME
ibeg=sdatim.index(begd*100+begt/100/100)
if nt0-ibeg>nt:sys.exit('fail cover the end of month '+str(nt0)+' '+str(ibeg))

#time flags
for t in range(nt0):
  for dt in range(2):
    nc['TFLAG'][t,:,dt]=tflag0[t,dt]

for v in V[3]:
  iv=V[3].index(v)
  nc[v][:ibeg,:,:,:]=var[iv,:ibeg,:,:,:]
  nc[v][ibeg:nt0,:,:,:]=var[iv,:(nt0-ibeg),:,:,:]
nc['SO2'][:,0,:,0]=flows[:,:]*sn_conc[0]
nc['NO' ][:,0,:,0]=flows[:,:]*sn_conc[0]*0.9
nc['NO2'][:,0,:,0]=flows[:,:]*sn_conc[0]*0.1

#attributes
atts=['SDATE','STIME', 'P_ALP', 'P_BET', 'P_GAM', 'XCELL', 'XCENT', 'XORIG', 'YCELL', 'YCENT', 'YORIG']
for i in atts:
  if i not in dir(nc00):continue
  exec('nc.'+i+'=nc00.'+i)
nc.NROWS=l_tzpp
nc.close()

fname='teds11.19'+mm+'.const.nc'
os.system(ncks+' -O -d ROW,1,'+str(l_tzpp)+' '+root+fname+' '+targ+fname)
nc0 = netCDF4.Dataset(root+fname,'r')
nc = netCDF4.Dataset(targ+fname,'r+')
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
for v in V[3]:
  nc[v][0,0,:,0]=nc0[v][0,0,tzpp.index,0]

for i in atts:
  if i not in dir(nc00):continue
  exec('nc.'+i+'=nc00.'+i)
nc.NROWS=l_tzpp
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
lat,lon=nc['LATITUDE'][0,0,:,0],nc['LONGITUDE'][0,0,:,0]
x0,y0=pnyc(lon,lat, inverse=False)
nc['XLOCA'][0,0,:,0]=x0[:]
nc['YLOCA'][0,0,:,0]=y0[:]
nc['COL'][0,0,:,0]=np.array((x0[:]-nc.XORIG)/nc.XCELL,dtype=int)
nc['ROW'][0,0,:,0]=np.array((y0[:]-nc.YORIG)/nc.YCELL,dtype=int)
nc['TFLAG'][0,:,0]=nc.SDATE
nc['TFLAG'][0,:,1]=nc.STIME
nc.close()
