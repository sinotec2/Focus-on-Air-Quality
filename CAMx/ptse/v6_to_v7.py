import numpy as np
import netCDF4
import os, sys, subprocess

ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')

mo='01'
fnameI='/nas1/camxruns/2016_v7/ptse/XindaG3/fortBE.14_hsinda3Gh80.3.'+mo+'.nc'
fnameO='/nas1/camxruns/2016_v7/ptse/XindaG3_v7/template_v7.nc'
ncI= netCDF4.Dataset(fnameI, 'r')
ncO= netCDF4.Dataset(fnameO, 'r')
Vi=[list(filter(lambda x:ncI.variables[x].ndim==j, [i for i in ncI.variables])) for j in [1,2,3,4]]
Vo=[list(filter(lambda x:ncO.variables[x].ndim==j, [i for i in ncO.variables])) for j in [1,2,3,4]]
lspe=[v for v in set(Vi[1])&set(Vo[1]) if np.sum(ncI.variables[v][:])!=0.]
nv=len(lspe)
ns=str(nv) #:ehd counts
s=' '
for c in set(Vo[1])-set(lspe+['plumerise','CP_NO']):
  s+=c+','
nvs=ncO.NVARS
ncI.close()
ncO.close()


PRM='XYHDTV'
names={7:['xcoord','ycoord','stkheight','stkdiam','stktemp','stkspeed'],
       6:[v+'STK' for v in PRM]}
v2c6={PRM[i]:names[6][i] for i in range(6)}
v2c7={PRM[i]:names[7][i] for i in range(6)}
for m in range(1,13):
  mo='{:02d}'.format(m)
  fnameI='/nas1/camxruns/2016_v7/ptse/XindaG3/fortBE.14_hsinda3Gh80.3.'+mo+'.nc'
  nc= netCDF4.Dataset(fnameI, 'r')
  nt,nopts=nc.variables[Vi[1][0]].shape
  var=np.zeros(shape=(nv,nt,nopts))
  for v in lspe:
    iv=lspe.index(v)
    var[iv,:,:]=nc.variables[v][:,:]
  tflag =nc.variables['TFLAG'][:,:nvs,:]
  etflag=nc.variables['ETFLAG'][:,:nvs,:]
  sdate,stime=nc.SDATE,nc.STIME
  edate,etime=nc.EDATE,nc.ETIME
  for v in PRM:
    exec(v+'=nc.variables["'+v2c6[v]+'"][:]')
  nc.close()

  fnameO='/nas1/camxruns/2016_v7/ptse/XindaG3_v7/fortBE.14_hsinda3Gh80.3.'+mo+'.nc'

  res=os.system('cp  template_v7.nc '+fnameO)
  nc = netCDF4.Dataset(fnameO, 'r+')
  nc.SDATE,nc.STIME=sdate,stime
  nc.EDATE,nc.ETIME=edate,etime
  for t in range(nt):
    nc.variables['TFLAG'][t,:,:]=tflag[t,:,:]
    nc.variables['ETFLAG'][t,:,:]=etflag[t,:,:]
  nc.variables['pigflag'][:]=1
  for v in Vo[1]:
    if v in lspe:
      iv=lspe.index(v)
      nc.variables[v][:nt,:nopts]=var[iv,:,:]
    else:
      nc.variables[v][:nt,:nopts]=0
  for v in PRM:
    exec('nc.variables["'+v2c7[v]+'"][:]='+v)
  nc.TSTEP = 10000
  nc.NSTEPS=nt
  nc.close()
