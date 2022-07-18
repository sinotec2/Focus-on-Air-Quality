#kuang@master /nas1/camxruns/2016_v7/emis
#$ cat REAS2hr.py
import os,sys,datetime
import numpy as np
from PseudoNetCDF.camxfiles.Memmaps import uamiv

mm=sys.argv[1]
for d in ['1', '2']:
  for cate in ['area', 'avi', 'ind','line', 'ship']:
    fname=cate+'/fortBE.'+d+'13_REAS3.base'+mm
    if cate=='ship':
      fname=cate+'/fortBE.'+d+'13_STEAM.base'+mm
    nc= uamiv(fname, 'r+')
    V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape

    fnameI='/nas1/TEDS/REAS3.1/join_spec/d'+d+'L.'+cate+'_'+mm
    if cate=='ship':fnameI='/nas1/TEDS/en.ilmatieteenlaitos.fi/surveying-maritime-emissions/output/2015'+mm+'.emis.grd0'+d
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
        for t in range(nt):
          nc.variables[v][t,:,:,:]=nc1.variables[v1][0,:,:,:]
      elif cate=='line':
        avrg=np.mean(nc.variables[v][:,:,:,:],axis=(0,1,2,3))
        if avrg==0.:
          for t in range(nt):
            nc.variables[v][t,:,:,:]=nc1.variables[v1][0,:,:,:]
        else:
          for t in range(nt):
            a=np.mean(nc.variables[v][t,:,:,:],axis=(0,1,2))
            fac=a/avrg
            nc.variables[v][t,:,:,:]=nc1.variables[v1][0,:,:,:]*fac
      elif cate=='ship':
        sdate1=[nc1.variables['TFLAG'][t,0,0] for t in range(nt1)]
        for t in range(nt):
          sdate=nc.variables['TFLAG'][t,0,0]
          if sdate not in sdate1:sys.exit('sdate not found: '+str(sdate))
          t1=sdate1.index(sdate)
          nc.variables[v][t,:,:,:]=nc1.variables[v1][t1,:,:,:]
    nc.close()
