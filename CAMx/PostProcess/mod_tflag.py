#kuang@master /nas1/camxruns/2019/outputs
#$ cat mod_tflag.py
import datetime
import netCDF4
import numpy as np
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

v='TFLAG'
for m in range(7,13):
  mo='{:02d}'.format(m)
  fname='con'+mo+'/19'+mo+'base.S.nc'
  nc = netCDF4.Dataset(fname,'r+')
  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  totalH, nlay, nrow, ncol = (nc.variables[V[3][0]].shape[i] for i in range(4))
  start=datetime.datetime(2019,int(mo),1,nc.STIME//10000)+datetime.timedelta(days=-1)
  nc.SDATE=dt2jul(start)[0]
  d_hrs={'TFLAG':0,'ETFLAG':1}
  for v in d_hrs:
    for t in range(totalH):
      nc.variables[v][t,:,:]=0
    sdt=np.array([dt2jul(start+datetime.timedelta(days=(t+d_hrs[v])/24.)) for t in range(totalH)]).flatten().reshape(totalH,2)
    ARR=np.zeros(shape=(totalH,nc.NVARS,2))
    ARR[:,:,:]=sdt[:,None,:]
    nc.variables[v][:,:,:]=ARR[:,:,:]
  nc.close()
# pncgen --format=uamiv -O 1905base.S.grd01 1905base.S.nc
#  for i in {07..12};do cp con05/1905base.S.nc con$i/19${i}base.S.nc;done
# for i in {07..12};do pncgen -O --out-format=uamiv con$i/19${i}base.S.nc con$i/19${i}base.S.grd01;done
