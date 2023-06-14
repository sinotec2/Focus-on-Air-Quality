#!/opt/anaconda3/bin/python
import numpy as np
import netCDF4
import os, sys, subprocess, datetime
from dtconvertor import dt2jul, jul2dt
from calendar import monthrange
from dateutil.relativedelta import relativedelta

def rel_mon(dt,im):
  a=dt+relativedelta(months=im)
  return a.year,a.month

ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
pwd=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[4]
D={'grid45':'7','grid09':'8','grid03':'3'}
nf={'grid45':1,'grid09':1,'grid03':3}
if pwd not in D:sys.exit('pwd not right!')
D=D[pwd]
nf=nf[pwd]

tdy=sys.argv[1]
bdate=datetime.datetime.strptime(tdy,"%Y-%m-%d")

nd=5
if len(sys.argv)==3:nd=int(sys.argv[2])
nhr=nd*24+1

if D !='3':
  fname='2015_D'+D+'.nc'
  fnameO=['reas_D'+D+'.nc']
  mm=str(int(tdy.split('-')[1])-1)
  os.system(ncks+' -O -d TSTEP,'+mm+' '+fname+' '+fnameO[0])
else:
  mm=tdy.split('-')[1]
  smk='/nas2/cmaq2019/download-20220503/input/2019'+mm+'/grid03/smoke/'
  ymn,ymp=rel_mon(bdate,+1)[:],rel_mon(bdate,-1)[:] #next and previous month and year[y,m sequence]
  bdate7=datetime.datetime.strptime(tdy[:-2]+'01',"%Y-%m-%d")+datetime.timedelta(days=-7)
  days=str((datetime.datetime(ymn[0],ymn[1],1)-bdate7).days)
  data_date='2019'+'{:04d}'.format(ymp[1]*100+bdate7.day)+'.'+days
  doms=['d4.ea2019_d4','TW3-d4.BaseEms','d4.ea2019_d4']
  kind=['b3gts_l.','cmaq_cb06r3_ae7_aq.'+mm+'-','egts_l.']
  fnameO=['begts.ncf','TEDS.ncf','egts.ncf']
  fnames=[smk+kind[i]+data_date+'.'+doms[i]+'.ncf' for i in range(nf)]
  ebdate=datetime.datetime.strptime(data_date.split('.')[0],"%Y%m%d")
  ebdat2=datetime.datetime.strptime(data_date.split('.')[0].replace('19','22'),"%Y%m%d")
  begh=((bdate-ebdat2).days+1-3)*24-1
  endh=begh+nhr
  for i in range(nf):
    os.system(ncks+' -O -d TSTEP,'+str(begh)+','+str(endh)+' '+fnames[i]+' '+fnameO[i])
for jf in range(nf):
  nc1 = netCDF4.Dataset(fnameO[jf],'r+')
  V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
#bdate=datetime.datetime.combine(datetime.date.today(),datetime.time(0,0,0,0))
  nc1.SDATE,nc1.STIME=dt2jul(bdate)
  nt1=nhr
  SDATE=[bdate+datetime.timedelta(hours=int(i)) for i in range(nt1)]
  for t in range(nt1):
    nc1.variables['TFLAG'][t,0,:]=dt2jul(SDATE[t])
  var=np.array(nc1.variables['TFLAG'][:,0,:])
  var3=np.zeros(shape=nc1.variables['TFLAG'].shape)
  var3[:,:,:]=var[:,None,:]
  nc1.variables['TFLAG'][:]=var3[:]
  nc1.TSTEP=10000

  if D=='3':continue
  nt,nlay,nrow,ncol=nc1.variables[V1[3][0]].shape
  var4=np.zeros(shape=(nt,nlay,nrow,ncol))
  for v in V1[3]:
    var=np.array(nc1[v][0,0,:,:])
    var4[:,:,:,:]=var[None,None,:,:]
    nc1[v][:]=var4[:]
  nc = netCDF4.Dataset('/nas2/cmaqruns/2022fcst/grid03/smoke/TEDS0.ncf','r')
  sum0=np.mean(nc['SO2'][:])
  x0,x1=nc.XORIG,nc.XORIG+nc.XCELL*nc.NCOLS
  y0,y1=nc.YORIG,nc.YORIG+nc.YCELL*nc.NROWS
  x1d=[nc1.XORIG+nc1.XCELL*i for i in range(nc1.NCOLS)]
  y1d=[nc1.YORIG+nc1.YCELL*i for i in range(nc1.NROWS)]
  x,y=np.meshgrid(x1d,y1d)
  boo=(x>=x0) & (x<=x1) & (y>=y0) & (y<=y1)  
  idx=np.where(boo)  
  sum1=np.mean(nc1['SO2'][:,:,:,:],axis=(0,1))
  sum1=np.mean(sum1[idx[0],idx[1]])
  rat=1. #sum0/sum1
  for v in V1[3]:
    nc1[v][:]*=rat
  print('rat=',rat)
  nc1.close()


