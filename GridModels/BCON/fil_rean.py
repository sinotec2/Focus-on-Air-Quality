#$ py=/nas1/cmaqruns/2019base/data/bcon/fil_rean.py
#$ cat $py
import netCDF4
import numpy as np
import datetime
import subprocess
import sys
import xarray as xr

def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)
def jul2dt(jultm):
  jul,tm=jultm[:]
  yr,ih=int(jul/1000), int(tm/10000.)
  return datetime.datetime(yr,1,1)+datetime.timedelta(days=int(jul-yr*1000-1))+datetime.timedelta(hours=ih)
l34=['21', '22', '23', '24', '25', '26', '27',
         '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
         '39', '40', '42', '43', '44', '46', '47', '48', '49', '50', '51',
         '53', '54', '56', '57', '59']
l40=['21','21', '22','22', '23','24', '24', '25','25', '26', '27',
      '28','28', '29', '30', '31','32', '32', '33', '34', '35', '36', '37', '38',
      '39', '40', '42', '43', '44', '46', '47', '48', '49', '50', '51',
      '53', '54', '56', '57', '59']
d40_23={39-k:l34.index(l40[k]) for k in range(40)}

#read the grib file(monthly)
ym,sp=(sys.argv[i] for i in [1,2])
fname='/nas1/ecmwf/reanalysis/gribs19/'+sp+ym+'D2.m3.nc'
print ('reading the grib')
nc0 = netCDF4.Dataset(fname,'r')
V0=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
nt0,nlay0,nrow0,ncol0=(nc0.variables[V0[3][0]].shape[i] for i in range(4))
dt=[jul2dt(nc0.variables['TFLAG'][i,0,:]) for i in range(nt0)]
dt0=np.array([int(str(d.strftime("%Y%m%d%H"))) for d in dt])
lastHr=dt0[-1]%100
if lastHr != 0 and lastHr==21:
  nc0 = netCDF4.Dataset(fname,'r+')
  dt_last=jul2dt(nc0.variables['TFLAG'][nt0-1,0,:])
  nc0.variables['TFLAG'][nt0,0,:]=dt2jul(dt_last+datetime.timedelta(hours=3))
  nc0.close()
  nc0 = netCDF4.Dataset(fname,'r')
  nt0,nlay0,nrow0,ncol0=(nc0.variables[V0[3][0]].shape[i] for i in range(4))
  dt=[jul2dt(nc0.variables['TFLAG'][i,0,:]) for i in range(nt0)]
  dt0=np.array([int(str(d.strftime("%Y%m%d%H"))) for d in dt])

X0=[i*3 for i in range(nt0)]
ncNROWS,ncNCOLS=(137, 83)
i0,j0=int(ncol0/2)-int(ncNCOLS/2)-1,int(nrow0/2)-int(ncNROWS/2)-1
i1,j1=int(ncol0/2)+int(ncNCOLS/2)+1,int(nrow0/2)+int(ncNROWS/2)+1
idx=[(i,j0) for i in range(i0+1,i1+1)]+   [(i1,j) for j in range(j0+1,j1+1)]+\
    [(i,j1) for i in range(i1-1,i0-1,-1)]+[(i0,j) for j in range(j1-1,j0-1,-1)]
nbnd=(ncNCOLS+ncNROWS)*2+4
idx=np.array(idx).flatten().reshape(nbnd,2)
idx=idx.T
v=V0[3][0]
print ('storing the matrix')
#nc0 = xr.open_dataset(fname)
var=nc0[v][:]
print ('cutting the boundaries')
bndR=np.zeros(shape=(nt0,nlay0,nbnd))
bnd=np.zeros(shape=(nt0,40,nbnd))
tmp=var[:,:,idx[0][:],idx[1][:]]
#ppb -> ppm
#bndR=np.diagonal(tmp,axis1=2, axis2=3)/1000.
bndR=tmp/1000.
#reverse the vertical sequence
for k in range(40):
  bnd[:,k,:]=bndR[:,d40_23[k],:]

tail='*TWN_3X3'
fnames=subprocess.check_output('ls BCON_v53_'+ym+tail,shell=True).decode('utf8').strip('\n').split()
for fname in fnames[:]:
#  if 'run12' not in fname:continue
  print (fname)
  nc = netCDF4.Dataset(fname,'r+')
  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  if v not in V[2]:sys.exit(v+' not in BCON file')
  nt,nlay,nbnd=nc.variables[v].shape#=(nc.NCOLS+nc.NROWS)*2+4
  julies,times=(np.array([nc.variables['TFLAG'][i,0,j] for i in range(nt)]) for j in range(2))
  times=[int((i/10000+1.5)/3)*30000 for i in times]
  dt=[jul2dt([i,j]) for i,j in zip(julies,times)]
  dti=np.array([int(str(d.strftime("%Y%m%d%H"))) for d in dt])
  tb,te=(np.where(dt0==dti[i])[0][0] for i in [0,-1])
  var=np.zeros(shape=(nt,nlay,nbnd))
  for t0 in range(tb,te+1):
    ymdh=dt0[t0]
    if ymdh not in dti:continue
    ti=np.where(dti==ymdh)[0]
    for t in ti:
      var[t,:,:]=bnd[t0,:,:]
  var2=np.zeros(shape=var.shape)
  # interpolate the
  for t in range(0,nt-3,3):
    var2[t+0,:,:]=var[t,:,:]
    var2[t+1,:,:]=var[t,:,:]*2/3+var[t+3,:,:]*1/3
    var2[t+2,:,:]=var[t,:,:]*1/3+var[t+3,:,:]*2/3
  nc.variables[v][:]=var2[:]
  nc.close()
