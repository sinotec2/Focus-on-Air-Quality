#kuang@node03 /nas1/ecmwf/CAMS/CAMS_global_atmospheric_composition_forecasts/2022
#$ cat ./grb2bcon.py
#!/opt/miniconda3/envs/py37/bin/python
import numpy as np
import json
import netCDF4
from pandas import *
from scipy.io import FortranFile
import sys, os, subprocess
import datetime
from dtconvertor import dt2jul, jul2dt

#outsourcing
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')

#import json files and dictionaries
for v in ['mws','dic','nms_gas','nms_part']:
  with open(v+'.json', 'r') as jsonfile:
    exec(v+'=json.load(jsonfile)')
dici={i:j for i,j in zip(dic.values(),dic.keys())}

gas=list(set([i for i in list(dic.values()) if 'mix' not in i and i not in ['ammonium','nitrate']]))
gas.sort()
ngas=len(gas)
gas_nm=['CO','ETH','FORM','ISOP','HNO3','NO2','NO','OLE','XPAR','O3','PAR','PAN','PRPA','SO2']
nms_gas={dici[i]:j for i,j in zip(gas,gas_nm)}

par=list(set([i for i in list(dic.values()) if i not in gas]))
par.sort()
vlist=['APOCI','APNCOMI','APOCJ','AOTHRJ','AISO3J', 'ASQTJ', 'AORGCJ', 'AOLGBJ', 'AOLGAJ']
par_nms=[]
for i in nms_part:
  par_nms+=nms_part[i]
npar=len(set(par_nms))
uts=['PPM',"ug m-3          "]
nv=len(set(dic.values()))

for fn in '123':
  fname='allEA_'+fn+'.nc' #directly read grib file will cost much of time, ncl_convert2nc the gribs
  nc = netCDF4.Dataset(fname, 'r')
  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
  if fn=='1':
    var=np.zeros(shape=(nv,nt,nlay,nrow,ncol))
    bdate=datetime.datetime.strptime(nc.variables[V[3][0]].initial_time,'%m/%d/%Y (%H:%M)')+datetime.timedelta(hours=60)
  for v in V[3]:
    iv=(gas+par).index(dic[v])
    var[iv,:,:,:,:]=nc.variables[v][:,:,:,:]
df=read_csv('BconInGrb.csv')
df['I']=df['JIseqInGrb']%1000
df['J']=df['JIseqInGrb']//1000
nbnd=len(df)
varbc=np.zeros(shape=(nv, nt, nlay,nbnd))
varbc[:]=var[:,:,:,df['J'],df['I']]
varbc=np.flip(varbc,axis=2)
fnameO='var_{:d}_{:d}_{:d}_{:d}'.format(nv, nt, nlay,nbnd)

#with FortranFile(fnameO,'w') as f:
#    f.write_record(varbc)

#read a BC file as rate base
fname='/nas1/cmaqruns/2019base/data/bcon/BCON_v53_1912_run5_regrid_20191201_TWN_3X3'
nc = netCDF4.Dataset(fname,'r')
Vb=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
rate={}
for v in nms_part:
  nms=nms_part[v]
  for nm in nms:
    if nm not in Vb[2]:sys.exit(v+' not in BCON file')
  avg=[np.mean(nc.variables[nm][:]) for nm in nms]
  sum_avg=sum(avg)
  if sum_avg==0:sys.exit('sum_avg==0')
  ratev=[avg[i]/sum_avg for i in range(len(avg))]
  rate.update({v:ratev})
for v in nms_gas:
  rate.update({v:[1.]})
nc.close()

#read density of air
fname='/nas1/cmaqruns/2022fcst/data/mcip/2208_run8/CWBWRF_45k/METCRO3D.nc'
nc = netCDF4.Dataset(fname,'r')
nt1,nlay1,nrow1,ncol1=nc.variables['DENS'].shape
i0,j0=0,0
i1,j1=i0+ncol1+1,j0+nrow1+1
dens=np.zeros(shape=(nlay,j1,i1))
dens[:,:nrow1,:ncol1]=np.mean(nc.variables['DENS'][:,:,:,:],axis=0) *1E9 #(kg to microgram)
nc.close()
dens[:,-1,:] = dens[:,-2,:]
dens[:,:,-1] = dens[:,:,-2]
dens[:,-1,-1]= dens[:,-2,-2]
nbnd1=(nrow1+ncol1)*2+4
if nbnd != nbnd1:sys.exit('wrong nbnd')
idx=[(j0,i) for i in range(i0,i1)]  +   [(j,i1-1) for j in range(j0,j1)] + \
    [(j1-1,i) for i in range(i1-1,i0-1,-1)] + [(j,i0) for j in range(j1-1,j0-1,-1)]
idxo=np.array(idx,dtype=int).flatten().reshape(nbnd1,2).T
dens1d=np.zeros(shape=(nlay,nbnd))
dens1d[:,:]=dens[:,idxo[0],idxo[1]]


fname='/nas1/cmaqruns/2022fcst/data/bcon/BCON_template_CWBWRF_45k'
fnameO=fname.replace('template','today')
os.system('cp '+fname+' '+fnameO)
nc1 = netCDF4.Dataset(fnameO,'r+')
V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nv1=len(V1[2])
nt1,nlay1,nbnd1=nc1.variables[V1[2][0]].shape
varv=np.zeros(shape=(nv1,nt,nlay1,nbnd1))
#buildup the timeflags
if nt1>(nt-1)*3:
  nc1.close()
  os.system(ncks+' -O -d TSTEP,0,'+str(nt-1)+' '+fname+' tmp.nc;mv tmp.nc '+fname)
  nc1 = netCDF4.Dataset(fname,'r+')
nc1.SDATE,nc1.STIME=dt2jul(bdate)
nt1=(nt-1)*3+1
SDATE=[bdate+datetime.timedelta(hours=int(i)) for i in range(nt1)]
for t in range(nt1):
  nc1.variables['TFLAG'][t,0,:]=dt2jul(SDATE[t])
var=np.array(nc1.variables['TFLAG'][:,0,:])
var3=np.zeros(shape=nc1.variables['TFLAG'].shape)
var3[:,:,:]=var[:,None,:]
nc1.variables['TFLAG'][:]=var3[:]
nc1.TSTEP=10000

for v in V1[2]:
  if v=='TFLAG':continue
  nc1[v][:]=0.

#iv in (gas+par) transfer to V1[2]
for v in list(nms_gas)+list(nms_part):
  print(v)
  iv=(gas+par).index(dic[v])
  if v in nms_gas:
    nm=nms_gas[v]
    if nm not in V1[2]:continue
    varv[V1[2].index(nm),:,:,:]=varbc[iv,:,:,:]*28.E6/mws[dic[v]] #mixing ratio to ppm
    continue
  skip=0
  nms=nms_part[v]
  for nm in nms:
    if nm not in V1[2]:skip=1
  if skip==1:continue
#    unit=dens[:] (kg/kg) to microgram/M3
  for nm in nms:
    im=nms.index(nm)
    varv[V1[2].index(nm),:,:,:]+=varbc[iv,:,:,:]*rate[v][im]*dens1d[None,:,:]
var2=np.zeros(shape=(nv1,nt1,nlay1,nbnd1))
for t in range(0,nt1,3):
  t3=int(t/3)
  t31=min(nt-1,t3+1)
  t11=min(nt1-1,t+1)
  t21=min(nt1-1,t+2)
  var2[:,t+0,:,:]=varv[:,t3,:,:]
  var2[:,t11,:,:]=varv[:,t3,:,:]*2/3+varv[:,t31,:,:]*1/3
  var2[:,t21,:,:]=varv[:,t3,:,:]*1/3+varv[:,t31,:,:]*2/3
for nm in V1[2]:
  if nm=='TFLAG':continue
  nc1.variables[nm][:]=var2[V1[2].index(nm),:,:,:]
nc1.close()
