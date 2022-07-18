#kuang@master /nas1/camxruns/2016_v7/emis
#$ cat REAS2hr_TimVar.py
import os, sys
import numpy as np
from PseudoNetCDF.camxfiles.Memmaps import uamiv
import netCDF4
from pandas import *
import subprocess
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

part=['CCRS','CPRM', 'FCRS', 'FPRM', 'NA', 'PCL', 'PEC', 'PNO3', 'POA', 'PSO4', 'SULF']

mm=sys.argv[1]
mo=int(mm)
ntm=(monthrange(2016,mo)[1]+2)*24+1
df=read_csv('d4LTimVar.csv')
sdt=list(df.sdt) #juldate time
bdate=datetime.datetime(2016,mo,1)+datetime.timedelta(days=-1+8./24)
edate=bdate+datetime.timedelta(days=monthrange(2016,mo)[1]+3)
for d in ['1', '2']:
  fnameT='template_d'+d+'.nc'
  for cate in ['area', 'avi', 'ind','line']:
    os.system('cp '+fnameT+' tmp.nc')
    nc = netCDF4.Dataset('tmp.nc', 'r+')
    V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
    nv=len(V[3])

    nc.SDATE,nc.STIME=dt2jul(bdate)
    nc.EDATE,nc.ETIME=dt2jul(edate)
    if 'ETFLAG' not in V[2]:
      zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
    for t in range(ntm):
      sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
      nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
      nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
      ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
      nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
      nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]

    fnameI='/nas1/TEDS/REAS3.1/join_spec/d'+d+'L.'+cate+'_'+mm
    nc1= uamiv(fnameI, 'r')
    V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
    nt1,nlay1,nrow1,ncol1=nc1.variables[V1[3][0]].shape
    ss=set(V1[3])-set(V[3])
    if len(ss) !=0:
      for v in ss:
        a=np.sum(nc1.variables[v][0,:,:,:],axis=(0,1,2))
        if a!=0:
          print('spec not found: '+v )
          if v in ['CH4','TOLA', 'XYLA','BNZA','ETHY']:continue
          sys.exit('unknown spec')

    for v in V[3]:
      nc.variables[v].units='gmole/hr'
      if v in part:nc.variables[v].units='g/hr'
      v1=v
      if v in ['TOL','XYL']:v1=v1+'A'
      if v == 'BENZ':v1='BNZA'
      if v == 'ETH':v1='ETHY'
      if v1 not in V1[3]:
        nc.variables[v][:]=0
        continue
      avrg1=np.mean(nc1.variables[v1][0,:,:,:],axis=(0,1,2))
      if avrg1==0.:
        nc.variables[v][:]=0.
        continue

      if cate!='line':
        for t in range(ntm):
          nc.variables[v][t,:,:,:]=nc1.variables[v1][0,:,:,:]
      elif cate=='line':
        if v1 not in df.columns:
          nc.variables[v][:,]=0.
        else:
          for t in range(ntm):
            jdt=int(nc.variables['TFLAG'][t,0,0]*100+nc.variables['TFLAG'][t,0,1]/10000)
            if jdt <sdt[0]:jdt=int(nc.variables['TFLAG'][t+24,0,0]*100+nc.variables['TFLAG'][t+24,0,1]/10000)
            if jdt >sdt[-1]:jdt=int(nc.variables['TFLAG'][t-48,0,0]*100+nc.variables['TFLAG'][t-48,0,1]/10000)
            idx=sdt.index(jdt)
            if type(df.loc[idx,v1])==np.float64: fac=df.loc[idx,v1]
            if type(df.loc[idx,v1])==list:fac=list(df.loc[idx,v1])[0]
            nc.variables[v][t,:,:,:]=nc1.variables[v1][0,:,:,:]*fac
    nc.NAME='EMISSIONS '
    nc.NOTE='REASV3 FILE'+(60-11)*' '
    nc.close()
    nc1.close()
    fname=cate+'/fortBE.'+d+'13_REAS3.base'+mm
    os.system(pncg+' -O --out-format=uamiv tmp.nc '+fname)
