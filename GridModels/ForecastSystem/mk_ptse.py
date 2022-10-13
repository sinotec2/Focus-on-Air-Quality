#!/opt/anaconda3/bin/python
import numpy as np
import netCDF4
import os, sys, subprocess, datetime
from dtconvertor import dt2jul, jul2dt

ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
tdy=sys.argv[1]
bdate=datetime.datetime.strptime(tdy,"%Y-%m-%d")
mm=tdy.split('-')[1]
nts={'const':1,'timvr':121}
for fn in nts:
  fname=fn+mm+'.nc'
  fnameO=fname.replace(mm,'')
  if 'timvr' in fname:
    nc = netCDF4.Dataset(fname, 'r')
    ebdate=datetime.datetime.strptime(str(nc.SDATE),"%Y%j")
    ebdat2=datetime.datetime.strptime(str(nc.SDATE).replace('19','22'),"%Y%j")
    dd=(bdate-ebdat2).days+1-3
    if dd<0:dd+=7
    begh=dd*24-1
    endh=begh+nts[fn]
    os.system(ncks+' -O -d TSTEP,'+str(begh)+','+str(endh)+' '+fname+' '+fnameO)
  else:
    os.system('cp '+fname+' '+fnameO)
  nc1 = netCDF4.Dataset(fnameO,'r+')
  nc1.SDATE,nc1.STIME=dt2jul(bdate)
  SDATE=[bdate+datetime.timedelta(hours=int(i)) for i in range(nts[fn])]
  for t in range(nts[fn]):
    nc1.variables['TFLAG'][t,0,:]=dt2jul(SDATE[t])
  var=np.array(nc1.variables['TFLAG'][:,0,:])
  var3=np.zeros(shape=nc1.variables['TFLAG'].shape)
  var3[:,:,:]=var[:,None,:]
  nc1.variables['TFLAG'][:]=var3[:]
  nc1.TSTEP=10000
