#kuang@DEVP /nas1/WRF4.0/WRFv4.2/202208
#$ cat mk_metoa.py
import datetime
from wrf import getvar, interplevel
from netCDF4 import Dataset
import numpy as np
import os

#get the start and end time of simulation
with open('namelist.input','r') as f:
  lines=[i for i in f]
inputs={}
for i in lines[1:]:
  itm=i.split()
  if len(itm)<3:continue
  try:
    inputs.update({itm[0]:float(itm[2].replace(',',''))})
  except:
    continue
staend={}
for var in ['sta','end']:
  tm=[i for i in inputs if var == i[:3]]
  for t in tm:
    inputs.update({t:int(inputs[t])})
  staend.update({var:datetime.datetime(inputs[tm[0]],inputs[tm[1]],inputs[tm[2]],inputs[tm[3]],)})
nt=int((staend['end']-staend['sta']).total_seconds()/3600./3)+1
fn_dt=[(staend['sta']+datetime.timedelta(hours=3*t)).strftime('%Y-%m-%d_%H:00:00') for t in range(nt)]

fname='CWB_wrfout_d01'
wrfin = Dataset(fname,'r')
nt_cwb=wrfin.dimensions['Time'].size
strT=[''.join([i.decode('utf-8') for i in wrfin.variables['Times'][t,:]]) for t in range(nt_cwb)]
p = getvar(wrfin, "pressure") #p is constant and homogeneous in x and y
uvi={'ua':0,'va':1}

fname='met_em.d01.'+fn_dt[0]+'.nc'
metin = Dataset(fname,'r')
p_met=getvar(metin, "pressure")
k_met=[list(p_met[:,0,0].values).index(k) for k in p[:,0,0].values]
kdic={k_met[k]:k for k in range(11)}
vdic={'ua':'UU','va':'VV','rh':'RH','tc':'TT'}
nz,ny,nx=p_met.shape

for t in range(nt):
  fname='met_em.d01.'+fn_dt[t]+'.nc'
  fnameO=fname.replace('met','metoa')
  os.system('cp '+fname+' '+fnameO)
  # only if fn_dt in strT(time overlaped)
  if fn_dt[t] in strT:
    tcwb=strT.index(fn_dt[0])
  else:
    continue
  metin = Dataset(fnameO,'r+')
  p_met=getvar(metin, "pressure")
  uv10=getvar(wrfin,"uvmet10",timeidx=tcwb)
  t2=getvar(wrfin,"T2",timeidx=tcwb)
  for itm in ['ua','va','rh','tc']:
    cmd='cwb=getvar(wrfin, "'+itm+'",timeidx=tcwb)'
    exec(cmd)
    var=np.zeros(shape=p_met.shape)
    if itm[1]=='a':
      var[0,:,:]=uv10[uvi[itm],:,:]
    elif itm=='tc':
      cwb+=273.
      var[0,:,:]=t2[:,:]
    else:
      var[0,:,:]=cwb[0,:,:]
    for k in range(1,22): #34-12):
      if k in kdic:
        var[k,:,:]=cwb[kdic[k],:,:]
      else:
        var[k,:,:]=interplevel(cwb,p,p_met[k,:,:])
    metin.variables[vdic[itm]][0,:22,:ny,:nx]=var[:22,:,:]
  metin.close()
  print(fnameO)
