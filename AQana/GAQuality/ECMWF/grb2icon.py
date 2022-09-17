#kuang@node03 /nas1/ecmwf/CAMS/CAMS_global_atmospheric_composition_forecasts/2022
#$ cat ./grb2icon.py
#!/opt/miniconda3/envs/py37/bin/python
import numpy as np
import json
import netCDF4
from pandas import *
from scipy.io import FortranFile
import sys, os, subprocess
import datetime
from dtconvertor import dt2jul, jul2dt
from pyproj import Proj
from scipy.interpolate import griddata

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

fname='AllEA.nc' #directly read grib file will cost much of time, ncl_convert2nc the gribs
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
var=np.zeros(shape=(nv,nt,nlay,nrow,ncol))
xlat=np.flip(nc['lat_0'])
xlon=nc['lon_0']
lonm, latm = np.meshgrid(xlon, xlat)

#date=datetime.datetime.strptime(nc.variables[V[3][0]].initial_time,'%m/%d/%Y (%H:%M)')+datetime.timedelta(hours=12)
td=datetime.datetime.today()
bdate=datetime.datetime(td.year,td.month,td.day)
for v in V[3]:
  iv=(gas+par).index(dic[v])
  var[iv,:,:,:,:]=nc.variables[v][:,:,:,:]
var=np.flip(var,axis=(2,3))

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
dens=np.zeros(shape=(nlay1,nrow1,ncol1))
dens[:]=np.mean(nc.variables['DENS'][:,:,:,:],axis=0) *1E9 #(kg to microgram)
nc.close()

fname='/nas1/cmaqruns/2022fcst/data/icon/ICON_template_CWBWRF_45k'
fnameO=fname.replace('template','yesterday')
os.system('cp '+fname+' '+fnameO)
nc1 = netCDF4.Dataset(fnameO,'r+')
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc1.P_ALP, lat_2=nc1.P_BET, lat_0=nc1.YCENT, lon_0=nc1.XCENT, x_0=0, y_0=0.0)
x0,y0=pnyc(lonm,latm, inverse=False)
V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nt1,nlay1,nrow1,ncol1=nc1.variables[V1[3][0]].shape
##interpolation indexing
x1d=[nc1.XORIG+nc1.XCELL*i for i in range(ncol1)]
y1d=[nc1.YORIG+nc1.YCELL*i for i in range(nrow1)]
x1,y1=np.meshgrid(x1d, y1d)

for i in 'xy':
  for j in '01':
    exec(i+j+'='+i+j+'.flatten()')

n,w=[],[]
for i in range(ncol1*nrow1):
  dist=(x0-x1[i])**2+(y0-y1[i])**2
  boo=(dist<=(nc1.XCELL*5)**2) & (dist>0)
  idx=np.where(boo)[0]
  if len(idx)==0:sys.exit('distance too short')
  wgt=1./dist[idx]
  swgt=np.sum(wgt)
  wgt[:]/=swgt
  n.append(idx)
  w.append(wgt)


#buildup the timeflags
nc1.SDATE,nc1.STIME=dt2jul(bdate)
nc1.variables['TFLAG'][0,:,:]=np.array(dt2jul(bdate))[None,:]

var1=np.zeros(shape=(nv,nt1,nlay1,nrow1*ncol1))
for i in range(nrow1*ncol1):
  c = var[:,:,:,n[i]//ncol, n[i]%ncol]
  var1[:,:,:,i]=np.sum(c*w[i],axis=3)
var1=var1.flatten().reshape(nv,nt1,nlay1,nrow1,ncol1)

for v in gas_nm+par_nms:
  if v in V1[3]:nc1[v][:]=0.

#iv in (gas+par) transfer to V1[3]
for v in list(nms_gas)+list(nms_part):
  print(v)
  iv=(gas+par).index(dic[v])
  if v in nms_gas:
    nm=nms_gas[v]
    if nm not in V1[3]:continue
    nc1[nm][:]=var1[iv,:,:,:,:]*28.E6/mws[dic[v]] #mixing ratio to ppm
    continue
  skip=0
  nms=nms_part[v]
  for nm in nms:
    if nm not in V1[3]:skip=1
  if skip==1:continue
#    unit=dens[:] (kg/kg) to microgram/M3
  for nm in nms:
    im=nms.index(nm)
    nc1[nm][:]+=var1[iv,:,:,:,:]*rate[v][im]*dens[None,:,:,:]
nc1.close()
