#kuang@114-32-164-198 /Users/TEDS/REAS3.1
#$ cat ./origins/txt2sum.py
"""
This version txt2nc is writing the nc file with Mozart format.
"""
from netCDF4 import Dataset
from pathlib import Path
from pyproj import Proj
import numpy as np
from datetime import *
from pandas import read_csv
import os, sys, subprocess
from calendar import monthrange


path={'114-32-164-198.HINET-IP.hinet.net':'/opt/anaconda3/bin/', 'node03':'/usr/bin/','master':'/cluster/netcdf/bin/', \
      'DEVP':'/usr/bin/','centos8':'/opt/anaconda3/envs/py37/bin/'}
hname=subprocess.check_output('echo $HOSTNAME',shell=True).decode('utf8').strip('\n')
if hname not in path:
  sys.exit('wrong HOSTNAME')



date0='0000-01-01'

fname='all_file.nam'
with open(fname) as ftext:
  fnames=[line.strip('\n') for line in ftext]
fname='REAS2MOZ.csv'
df=read_csv(fname)
df.columns=['REAS','MOZ','wt']
specREAS_MOZ={}
wt_MOZ={}
for i in range(len(df)):
  specREAS_MOZ.update({df.loc[i,'REAS']:df.loc[i,'MOZ']})
  wt_MOZ.update({df.loc[i,'MOZ']:df.loc[i,'wt']})
facG=10**6 /1E6
unit_REAS={i:facG*mw for i,mw in zip(df.REAS,df.wt)}
with open('aero_fac.txt','r') as f:
  facP={i.split()[0]:float(i.split()[1])/1E6 for i in f}
REAS_part=['BC_','OC_','PM2.5','PM10_']
MOZT_part=['CB1','OC1','SA1','DUST1']
R2M={i:j for i,j in zip(REAS_part,MOZT_part)}
for i in REAS_part:
  unit_REAS.update({i:facP[R2M[i]]})


fname='cate.csv'
dfc=read_csv(fname)
#d1 domain 91.23~150.75
xmin=int( 91.23/0.25)*0.25
ymin=int(  0.05/0.25)*0.25
xmax=int(150.75/0.25+1)*0.25
ymax=int( 45.77/0.25+1)*0.25
coord_file = Path("./coord.txt")
try:
  my_abs_path = coord_file.resolve()
except:
  print ('generating nx,ny,x0,y0...')
  # doesn't exist
  x0,y0=set([xmin,xmax]),set([ymin,ymax])
  for fname in fnames:
#  if stop==1:break
    with open(fname) as text_file:
      d=[line.strip('\n').split() for line in text_file]
    f1=int(d[0][0])
    x0=set([min(max(float(d[l][0]),xmin),xmax) for l in range(f1,len(d))])|x0
    y0=set([min(max(float(d[l][1]),ymin),ymax) for l in range(f1,len(d))])|y0
  x0=list(x0);x0.sort()
  y0=list(y0);y0.sort()
  nx,ny=int((x0[-1]-x0[0])/0.25)+1,int((y0[-1]-y0[0])/0.25)+1
  x0=[x0[0]+0.25*float(i) for i in range(nx)]
  y0=[y0[0]+0.25*float(i) for i in range(ny)]
  with open('coord.txt','w') as ftext:
    ftext.write( "%s" % str(nx)+' '+str(ny)+'\n')
    for i in range(nx):
      ftext.write( "%s" % str(x0[i])+' ')
    ftext.write( "%s" % '\n')
    for i in range(ny):
      ftext.write( "%s" % str(y0[i])+' ')
else:
  print ('reading nx,ny,x0,y0...')
   # exists
  with open('coord.txt','r') as ftext:
    d=[line.strip('\n').split() for line in ftext]
  nx,ny=int(d[0][0]),int(d[0][1])
  x0=[float(d[1][i]) for i in range(nx)]
  y0=[float(d[2][i]) for i in range(ny)]

#generate the area(km^2) of each grid cells, 0.25 squre = 500~800Km^2
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
lonG, latG = np.meshgrid(x0, y0)
x,y=pnyc(lonG, latG, inverse=False)
x,y=x/1000.,y/1000.
area=np.zeros(shape=(ny,nx))
for j in range(ny-1):
  for i in range(nx-1):
    dx=(x[j+1,i+1]+x[j,i+1]-x[j+1,i]-x[j,i])/2.
    dy=(y[j+1,i+1]+y[j+1,i]-y[j,i+1]-y[j,i])/2.
    area[j,i]=dx*dy
  area[j,nx-1]=area[j,nx-2]
for i in range(nx):
  area[ny-1,i]=area[ny-2,i]


nm=12
HRS=[24*monthrange(2015,m+1)[1] for m in range(nm)]
fname='./frame.nc'
a=Dataset(fname,'r')
v=[i for i in a.variables]
dm={u'ilev':2, u'lat':ny, u'lev':1,u'lon':nx,'time':nm}
dtmap={'float32':'f4','float64':'f8','int32':'i4'}

stop=0
dayb=736695-364
iy0=2015
day0=date(iy0,1,1)
for cate in list(dfc['cate']):
  if len([i for i in fnames if cate in i])==0:continue
  if os.path.isfile(cate+".nc"):continue
  if stop==1:break
  try:
    f=Dataset(cate+".nc","w")
  except:
    f.close() #in case of loop-skipping and the file is not-colsed intime yet
    try:
      f=Dataset(cate+".nc","w")
    except: #in case file is hang by other program
      continue #try next category

  for i in dm:
    f.createDimension(i,dm[i])
  for i in v:
    io=i
    if str(i)=='NOX':io='T'#the only V[3]
    f.createVariable(io,dtmap[str(a.variables[i].dtype)],a.variables[i].dimensions)
    ln=a.variables[i].ncattrs()
    if len(ln)>0:
      for j in ln:
        val=a.variables[i].getncattr(j) #save the original attributes
        f.variables[io].setncattr(j,val)
    if a.variables[i].ndim ==0:
      f.variables[i][:]=a.variables[i][:]
    if i=='lev':f.variables[i][:]=a.variables[i][-1]
    if i=='ilev':f.variables[i][:]=a.variables[i][-2:]
    if i=='mdt':f.variables[i][:]=[30*3600]
    if io=='T':
      f.variables[io][:,:,:,:]=np.ones(shape=(nm,1,ny,nx))*298.
      f.variables[io].long_name='temperature'
      f.variables[io].units='K'
    if f.variables[io].size==nm:
      if i=='time':
#       f.variables[i][:]=[(date(iy0,m+1,1)-day0).days+dayb for m in range(12)]
        f.variables[i][:]=[30*m+dayb for m in range(nm)]
      elif i=='date':
        f.variables[i][:]=[int((date(iy0,1,1)+timedelta(days=30*m)).strftime('%Y%m%d')) for m in range(nm)]
      elif i=='datesec':
        f.variables[i][:]=[int(0) for m in range(nm)]
      elif i=='timestep_index':
        f.variables[i][:]=[int(m) for m in range(nm)]
      else:
        f.variables[i][:]=a.variables[i][:nm]
  f.variables['lon'][:]=x0
  f.variables['lat'][:]=y0
  for fname in fnames:
    if 'POWER_PLANTS_POINT' in fname:continue
    if cate not in fname:continue
#read the txt file
    with open(fname) as text_file:
      d=[line.strip('\n').split() for line in text_file]
    print (fname+' '+cate)
    f1=int(d[0][0])
    spec=d[1][0]
    if spec=='Total':spec='NMHC'
    if spec=='Total_NMV':spec='NMHC'
    if spec=='Others':spec=d[1][0]+'_'+d[1][1]
    specM=specREAS_MOZ[spec]
    if specM=='None':continue

    z=np.zeros(shape=(nm,1,ny,nx))
    for l in range(f1,len(d)):
      xx=min(max(float(d[l][0]),xmin),xmax)
      yy=min(max(float(d[l][1]),ymin),ymax)
      i=x0.index(xx)
      j=y0.index(yy)
      for m in range(12):
        z[m,0,j,i]=float(d[l][m+2])

    io=specM
    i='NOX'
    try:
      f.createVariable(io,dtmap[str(a.variables[i].dtype)],a.variables[i].dimensions)
    except: #already create,
      zs=np.array(f.variables[specM][:,:,:,:])
      for m in range(nm):
        f.variables[specM][m]=zs[m]+z[m,0,:,:]/area[:,:]/unit_REAS[spec]/HRS[m]

    else:       #new to f
      f.variables[specM].units='gmoleAir/hr/km^2 or AirDens*mg/hr/km^2'#like MOZART in Volume Mix-ratio(to PPM)
      f.variables[specM].long_name=specM+' monthly emission from REAS'
      for m in range(nm):
        z2d=z[m,0,:,:]/area[:,:]/unit_REAS[spec]/HRS[m]  #in unit of mole for splitting and summing
        f.variables[specM][m]=z2d
  f.close()
  os.system(path[hname]+'/ncks -O --mk_rec_dmn time '+cate+".nc tmp;mv tmp "+cate+".nc")
