#$ cat /nas1/WRF4.0/WRFv4.2/202208/mk_metoaTD3.py
#argument with time t=0~nt-1
import datetime
from wrf import getvar, interplevel
from netCDF4 import Dataset
import numpy as np
import os, sys
from scipy.interpolate import griddata
from pyproj import Proj

def interpXY(arr):
  c = [arr[idx[0][i], idx[1][i]] for i in range(mp)]
  return griddata(xyc, c, (x1, y1), method='linear')

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

fname='CWB_wrfout_d03'
wrfin = Dataset(fname,'r')
p = getvar(wrfin, "pressure") #p is constant and homogeneous in x and y
latm,lonm=getvar(wrfin,'lat'),getvar(wrfin,'lon') #CWB net
nz0,ny0,nx0=p.shape
uvi={'ua':0,'va':1}

fname='met_em.d03.'+fn_dt[0]+'.nc'
metin = Dataset(fname,'r')
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=metin.TRUELAT1, lat_2=metin.TRUELAT2, lat_0=metin.CEN_LAT, lon_0=metin.CEN_LON, x_0=0, y_0=0)
x,y=pnyc(lonm,latm, inverse=False) #CWB net
p_met=getvar(metin, "pressure")
k_met=[list(p_met[:,0,0].values).index(k) for k in p[:,0,0].values]
kdic={k_met[k]:k for k in range(11)}
vdic={'ua':'UU','va':'VV','rh':'RH','tc':'TT'}
nz,ny,nx=p_met.shape

x1d=[metin.DX*i for i in range(-nx//2,nx//2)]
y1d=[metin.DY*i for i in range(-ny//2,ny//2)]
x1,y1=np.meshgrid(x1d, y1d)
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]
boo=(abs(x) <= (maxx - minx) /2+metin.DX*10) & (abs(y) <= (maxy - miny) /2+metin.DY*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

base={i:0 for i in vdic} #used for temp, degC to degK
base.update({'tc':273})

surf_var={i+'a':'uv10[uvi[itm],' for i in 'uv'} #surface wind
surf_var.update({'tc':'t2[','rh':'cwb[0,'}) #temp and rh

tin=int(sys.argv[1])
if tin>=nt:sys.exit('wrong T')
for t in range(tin,tin+1):
  fname='met_em.d03.'+fn_dt[t]+'.nc'
  fnameO=fname.replace('met','metoa')
  os.system('cp '+fname+' '+fnameO)
  # only if fn_dt in strT(time overlaped)
  fname='/nas1/Data/cwb/WRF_3Km/'+dates[fn_dt[t]]+'/wrfout_d03_:00:00'
  wrfin = Dataset(fname,'r')
  nt_cwb=wrfin.dimensions['Time'].size
  strT=[''.join([i.decode('utf-8') for i in wrfin.variables['Times'][t,:]]) for t in range(nt_cwb)]
  if fn_dt[t] in strT:
    tcwb=strT.index(fn_dt[t])
  else:
    continue
  metin = Dataset(fnameO,'r+')
  p_met=getvar(metin, "pressure")
  uv10=getvar(wrfin,"uvmet10",timeidx=tcwb)
  t2=getvar(wrfin,"T2",timeidx=tcwb)
  for itm in vdic:
    cmd='cwb=getvar(wrfin, "'+itm+'",timeidx=tcwb)+base[itm]'
    exec(cmd)
    var=np.zeros(shape=(nz,ny,nx))
    exec('var[0,:,:]=interpXY('+surf_var[itm]+':,:])') #surface mapping
    for k in range(1,22): #34-12):
      if k in kdic:
        var[k,:,:]=interpXY(cwb[kdic[k],:,:])
      else:
        var[k,:,:]=interpXY(interplevel(cwb[:,:,:],p[:,:,:],p_met[k,0,0]))
    metin.variables[vdic[itm]][0,:22,:ny,:nx]=var[:22,:,:]
  metin.close()
  print(fnameO)
