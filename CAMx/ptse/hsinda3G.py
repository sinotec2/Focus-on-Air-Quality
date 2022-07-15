#kuang@master /nas1/camxruns/2016_v7/ptse/XindaG3
#$ cat hsinda3G.py

import PseudoNetCDF as pnc
import numpy as np
import sys,os, subprocess, netCDF4
from calendar import monthrange
import datetime


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


pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
v1_xinda=[168616.09,2527230.05,80.,-11.0,363.0,19.8*3600.,1]
Xcent,Ycent= 248417-333.33*5,   2613022-3000. #tuning the coordinates
v1_xinda[0:2]=[v1_xinda[0]-Xcent,v1_xinda[1]-Ycent]

fname1='fortBE.14.hsinda.1.h80.n5.09Mp'
pt=pnc.pncopen(fname1,format='point_source')
for j in range(1,4):
  exec('v'+str(j)+'=list(filter(lambda x:pt.variables[x].ndim=='+str(j)+', [i for i in pt.variables]))')
nhr,nvar,dt=pt.variables[v3[0]].shape
nt,nopts=pt.variables[v2[0]].shape
d={}
for v in 'XYHDTV':
  var=v+'STK'
  d.update({v:np.array(list(pt.variables[var][:]))})
d.update({'I':np.array([i for i in range(nopts)])})
idx=np.where(abs(d['X']-v1_xinda[0])<3000)
idy=np.where(abs(d['Y'][idx[0]]-v1_xinda[1])<3000)
idh=np.where(abs(d['H'][idx[0]][idy[0]]-80)<5)
I=d['I'][idx[0]][idy[0]][idh[0]]
parms={v:d[v][I] for v in 'XYHDTV'}
emiss={v:pt.variables[v][0,I] for v in v2 if pt.variables[v][0,I]>0}
yr=2016
for mo in range(1,13):
  mm='{:02d}'.format(mo)
  fname='fortBE.14_hsinda3Gh80.3.'+mm+'.nc'
  ntm=(monthrange(yr,mo)[1]+2)*24+1
  bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
  edate=bdate+datetime.timedelta(days=monthrange(yr,mo)[1]+3)
  #prepare the uamiv template
  try:
    nc = netCDF4.Dataset(fname, 'r+')
  except:
    os.system('cp template.nc '+fname)
    nc = netCDF4.Dataset(fname, 'r+')
  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  nt,nopts=nc.variables[v2[0]].shape
  nv=nc.variables['TFLAG'].shape[1]
  nc.SDATE,nc.STIME=dt2jul(bdate)
  nc.EDATE,nc.ETIME=dt2jul(edate)
  nc.NOTE='Point Emission for HsinDa New 3 Gas Project'
  nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
  if 'ETFLAG' not in V[2]:
    zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
  for t in range(ntm):
    sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
    nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
    nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
  for v in V[1]:
    nc.variables[v][:]=0.
  sdatetime=[jul2dt(nc.variables['TFLAG'][t,0,:]) for t in range(ntm)]
  d['D'][I]=d['D'][I]*np.sqrt(3.)
  for v in 'XYHDTV':
    var=v+'STK'
    nc.variables[var][0]=d[v][I]
  for v in emiss:
    nc.variables[v][:,0]=emiss[v][0]*3
  nc.close()
  result=os.system(pncg+' -O  --out-format=point_source '+fname+' '+fname.replace('.nc','')+'>&/dev/null')
  if result==0:
    os.system('rm '+fname)
