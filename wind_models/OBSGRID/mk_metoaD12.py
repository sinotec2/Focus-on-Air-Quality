#$ cat /nas1/WRF4.0/WRFv4.2/202208/mk_metoaD12.py
#argument with time t=0~nt-1
import datetime
from wrf import getvar, interplevel
from netCDF4 import Dataset
import numpy as np
import os, sys
from scipy.interpolate import griddata
from pyproj import Proj
from pandas import *

def pick_nearst(oldarr):
  n=oldarr.ndim
  shp=oldarr.shape
  if n==2:
    return oldarr[df.J0,df.I0].reshape(ny,nx)
  if n==3:
    k,j,i=oldarr.shape
    return oldarr[:,df.J0,df.I0].reshape(k,ny,nx)

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
#timestamp for each met and metoa file
fn_dt=[(staend['sta']+datetime.timedelta(hours=3*t)).strftime('%Y-%m-%d_%H:00:00') for t in range(nt)]
#path dic of CWB_wrfouts, searched by fn_dt
dates={fn_dt[t]:(staend['sta']+datetime.timedelta(hours=t*3-6)).strftime('%Y%m%d') for t in range(nt)}
vdic={'ua':'UU','va':'VV','rh':'RH','tc':'TT'}
base={i:0 for i in vdic} #used for temp, degC to degK
base.update({'tc':273})
surf_var={i+'a':'uv10[uvi[itm],' for i in 'uv'} #surface wind
surf_var.update({'tc':'t2[','rh':'cwb[0,'}) #temp and rh
cwbwrf={'1':'/wrfout_d01_:00:00','2':'/wrfout_d03_:00:00'}
uvi={'ua':0,'va':1}

for d in '2':
  df=read_csv('nearstD'+d+'.csv')

  fname='met_em.d0'+d+'.'+fn_dt[0]+'.nc'
  metin = Dataset(fname,'r')
  p_met=getvar(metin, "pressure")
  nz,ny,nx=p_met.shape

  fname='CWB_wrfout_d0'+d
  wrfin = Dataset(fname,'r')
  p0 = getvar(wrfin, "pressure").data #p is constant and homogeneous in x and y
  nz0,ny0,nx0=p0.shape
  p=pick_nearst(p0)

  k_met=[list(p_met[:,0,0].values).index(k) for k in p[:,0,0]]
  kdic={k_met[k]:k for k in range(11)}

  for t in range(nt):
    fname='met_em.d0'+d+'.'+fn_dt[t]+'.nc'
    fnameO=fname.replace('met','metoa')
    os.system('cp '+fname+' '+fnameO)
    # only if fn_dt in strT(time overlaped)
    fname='/nas1/Data/cwb/WRF_3Km/'+dates[fn_dt[t]]+cwbwrf[d]
    wrfin = Dataset(fname,'r')
    nt_cwb=wrfin.dimensions['Time'].size
    strT=[''.join([i.decode('utf-8') for i in wrfin.variables['Times'][t,:]]) for t in range(nt_cwb)]
    if fn_dt[t] in strT:
      tcwb=strT.index(fn_dt[t])
    else:
      continue
    metin = Dataset(fnameO,'r+')
    p_met=getvar(metin, "pressure").data
    uv10=pick_nearst(getvar(wrfin,"uvmet10",timeidx=tcwb).data)
    t2=pick_nearst(getvar(wrfin,"T2",timeidx=tcwb).data)
    for itm in vdic:
      cmd='cwb=pick_nearst(getvar(wrfin, "'+itm+'",timeidx=tcwb).data+base[itm])'
      exec(cmd)
      var=np.zeros(shape=(nz,ny,nx))
      cmd='var[0,:,:]='+surf_var[itm]+':,:]'
      exec(cmd) #surface mapping
      for k in range(1,22): #34-12):
        if k in kdic:
          var[k,:,:]=cwb[kdic[k],:,:]
        else:
          var[k,:,:]=interplevel(cwb[:,:,:],p[:,:,:],p_met[k,0,0])
    metin.variables[vdic[itm]][0,:22,:ny,:nx]=var[:22,:,:]
    metin.close()
    print(fnameO)
