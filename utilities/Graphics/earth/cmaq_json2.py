#kuang@node03 /nas1/Data/javascripts/D3js/earthFcst03/public/data/weather/current
#$ cat cmaq_json2.py
#!/opt/anaconda3/envs/gribby/bin/python
import numpy as np
import json
import sys, os
import netCDF4
from pyproj import Proj
from bisect import bisect
import subprocess
from dtconvertor import dt2jul, jul2dt
import datetime

grds=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[5].replace('earthFcst','')
#the json template
fname='current-wind-surface-level-fcst-'+grds+'.json'
with open(fname,'r+') as f:
  gfs=json.load(f)
ngfs=len(gfs)
fname='current-ozone-surface-level-fcst-'+grds+'.json'
with open(fname,'r+') as f:
  ozn=json.load(f)
nozn=len(ozn)
nr={'o':nozn,'g':ngfs}
jsn={'o':ozn,'g':gfs}


gdnam={'45':'CWBWRF_45k','09':'SECN_9k','03':'TWEPA_3k'}
Xo={'45':0,'09':1,'03':4}

fcst='/nas2/cmaqruns/2022fcst/grid'+grds+'/cctm.fcst/daily/CCTM_ACONC_v532_intel_'+gdnam[grds]+'_YYYYMMDD.nc'
bdate=datetime.datetime.now()
YMDs=[(bdate+datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]

#read lat,lon
fname='/nas2/cmaqruns/2022fcst/grid'+grds+'/mcip/GRIDCRO2D.nc'
nc = netCDF4.Dataset(fname, 'r')
lonm=nc.variables['LON'][0,0,:,:]
latm=nc.variables['LAT'][0,0,:,:]
nrow,ncol=lonm.shape
x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x0,y0=np.meshgrid(x1d, y1d)

dx=(lonm[nrow//2,ncol//2+1]-lonm[nrow//2,ncol//2-1])/2
dy=(latm[nrow//2+1,ncol//2]-latm[nrow//2-1,ncol//2])/2
lat_min=latm[0,ncol//2]-dy
lat_max=np.min([latm[-1,-1],latm[-1,0]])+dy
lon_min=lonm[0,0]-dx
lon_max=lonm[0,-1]+dx
nx=int((lon_max-lon_min)//dx)+2
ny=int((lat_max-lat_min)//dy)+1
#new grid system(x1,y1) in equal dlat and dlon
lon1d=[lon_min+dx*i for i in range(nx)]
lat1d=[lat_min+dy*i for i in range(ny)]
lonm, latm = np.meshgrid(lon1d, lat1d)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET, lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
x1,y1=pnyc(lonm,latm, inverse=False)

for i in 'xy':
  for j in '01':
    exec(i+j+'='+i+j+'.flatten()')

n,w=[],[]
for i in range(ny*nx):
  dist=(x0-x1[i])**2+(y0-y1[i])**2
  boo=(dist<=(nc.XCELL*5)**2) & (dist>0)
  idx=np.where(boo)[0]
  if len(idx)==0:sys.exit('distance too short')
  wgt=1./dist[idx]
  swgt=np.sum(wgt)
  wgt[:]/=swgt
  n.append(idx)
  w.append(wgt)


for k in ['o','g']:
  for i in range(nr[k]):
    jsn[k][i]['header']['nx']=nx
    jsn[k][i]['header']['ny']=ny
    jsn[k][i]['header']['numberPoints']=nx*ny
    jsn[k][i]['header']['dx']=np.float64(dx)
    jsn[k][i]['header']['dy']=np.float64(dy)
    jsn[k][i]['header']['lo1']=np.float64(lon_min)
    jsn[k][i]['header']['lo2']=np.float64(lon_max)
    jsn[k][i]['header']['la2']=np.float64(lat_min)
    jsn[k][i]['header']['la1']=np.float64(lat_max)
    jsn[k][i]['header']['center']=0
    jsn[k][i]['header']["forecastTime"]=0
    jsn[k][i]['header']['centerName']="WRF and CMAQ Forecastings"
    jsn[k][i]['data']=[0 for v in range(nx*ny)]

uv=['U10', 'V10']
head='/nas1/backup/data/NOAA/NCEP/GFS/YYYY/'+gdnam[grds]+'/wrfout_d01_'
tail='_00:00:00'
pwd='/nas1/Data/javascripts/D3js/earthFcst'+grds+'/public/data/weather/current/'

nc = netCDF4.Dataset(fname, 'r')
for day in range(5):
  fname=head+YMDs[day]+tail
  if not os.path.isfile(fname):continue
  nc = netCDF4.Dataset(fname, 'r')
  nt=nc.dimensions['Time'].size
  var1=np.zeros(shape=(nt,ny*nx))
  for a in uv:
    var=np.array(nc[a][:,Xo[grds]:Xo[grds]+nrow,Xo[grds]:Xo[grds]+ncol])
    for i in range(ny*nx):
      c = var[:,n[i]//ncol, n[i]%ncol]
      var1[:,i]=np.sum(c*w[i],axis=1)
    exec(a+'=var1.flatten().reshape(nt,ny,nx)')

  strT=[''.join([i.decode('utf-8') for i in nc['Times'][t,:]]) for t in range(nt)]
  for t in range(0,nt,3):
    bdate=datetime.datetime.strptime(strT[t],'%Y-%m-%d_%H:00:00')
    dt=bdate.strftime("%Y-%m-%dT%H:%M:%SZ")
    dir=bdate.strftime("../%Y/%m/%d/")
    os.system('mkdir -p '+pwd+dir)
    hh=bdate.strftime("%H00")
    for i in range(ngfs):
      gfs[i]['header']['refTime']=dt
    for ir in range(ngfs):
      exec('var='+uv[ir]+'[t,:,:]')
      gfs[ir]['data']=list(np.flip(np.where(var!=var,0,var),axis=0).flatten())

    fnameO=pwd+dir+hh+'-wind-surface-level-fcst-'+grds+'.json'
    with open(fnameO,'w') as f:
      json.dump(gfs,f)

for day in range(5):
  fname=fcst.replace('YYYYMMDD',YMDs[day].replace('-',''))
  if not os.path.isfile(fname):continue
  nc = netCDF4.Dataset(fname, 'r')
  o3=nc['O3'][:,0,:,:]
  nt=nc.dimensions['TSTEP'].size
  var1=np.zeros(shape=(nt,ny*nx))
  for i in range(ny*nx):
    c = o3[:,n[i]//ncol, n[i]%ncol]
    var1[:,i]=np.sum(c*w[i],axis=1)
  o3=var1.flatten().reshape(nt,ny,nx)
  for t in range(0,nt,3):
    bdate=jul2dt(nc['TFLAG'][t,0,:])
    dt=bdate.strftime("%Y-%m-%dT%H:%M:%SZ")
    dir=bdate.strftime("../%Y/%m/%d/")
    pwd='/nas1/Data/javascripts/D3js/earthFcst'+grds+'/public/data/weather/current/'
    os.system('mkdir -p '+pwd+dir)
    hh=bdate.strftime("%H00")

    for i in range(nozn):
      ozn[i]['header']['refTime']=dt
    for ir in range(nozn):
      var=o3[t,:,:]*1000
      ozn[ir]['data']=list(np.flip(np.where(var!=var,0,var),axis=0).flatten())

    fnameO=pwd+dir+hh+'-ozone-surface-level-fcst-'+grds+'.json'
    with open(fnameO,'w') as f:
      json.dump(ozn,f)
