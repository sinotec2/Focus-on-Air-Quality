#kuang@node03 /nas1/Data/javascripts/D3js/earthFcst45/public/data/weather/current
#$ cat cmaq_json.py
#!/opt/miniconda3/envs/gribby/bin/python
import numpy as np
import json
import sys, os
import netCDF4
from scipy.interpolate import griddata
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
x0={'45':0,'09':1,'03':4}

fcst='/nas2/cmaqruns/2022fcst/grid'+grds+'/cctm.fcst/daily/CCTM_ACONC_v532_intel_'+gdnam[grds]+'_YYYYMMDD.nc'
bdate=datetime.datetime.now()
YMDs=[(bdate+datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]

#read lat,lon
fname='/nas2/cmaqruns/2022fcst/grid'+grds+'/mcip/GRIDCRO2D.nc'
nc = netCDF4.Dataset(fname, 'r')
x=nc.variables['LON'][0,0,:,:]
y=nc.variables['LAT'][0,0,:,:]
nrow,ncol=x.shape
lat_min=y[1,ncol//2]
lat_max=np.min([y[-2,-2],y[-2,1]])
jmx=bisect(y[:,ncol//2],lat_max)
dy=(y[jmx,ncol//2]-lat_min)/jmx
dx=dy
lon_min=np.max(x[:,1])
idx=np.where(x[:,-2]>0)
lon_max=np.min(x[idx[0],-2])
nx=int((lon_max-lon_min)//dx)
ny=int((lat_max-lat_min)//dy)
#new grid system(x1,y1) in equal dlat and dlon
lon1d=[lon_min+dx*i for i in range(nx)]
lat1d=[lat_min+dy*i for i in range(ny)]
x1, y1 = np.meshgrid(lon1d, lat1d)
idx=np.where((x>0)&(x>=lon_min)&(x<=lon_max)&(y>=lat_min)&(y<=lat_max))
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]

for k in ['o','g']:
  for i in range(nr[k]):
    jsn[k][i]['header']['nx']=nx
    jsn[k][i]['header']['ny']=ny
    jsn[k][i]['header']['numberPoints']=nx*ny
    for v in ['dx','dy']:
      jsn[k][i]['header'][v]=np.float64(dx)
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
  nc = netCDF4.Dataset(fname, 'r')
  for a in uv:
    cmd=a+'=np.array(nc["'+a+'"][:,x0[grds]:x0[grds]+nrow,x0[grds]:x0[grds]+ncol])'
    exec(cmd)
  nt=nc.dimensions['Time'].size
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
      c = np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
      zz = griddata(xyc, c[:], (x1, y1), method='cubic')
      gfs[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())

    fnameO=pwd+dir+hh+'-wind-surface-level-fcst-'+grds+'.json'
    with open(fnameO,'w') as f:
      json.dump(gfs,f)

for day in range(5):
  fname=fcst.replace('YYYYMMDD',YMDs[day].replace('-',''))
  nc = netCDF4.Dataset(fname, 'r')
  o3=nc['O3'][:,0,:,:]
  nt=nc.dimensions['TSTEP'].size
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
      c = np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
      zz = griddata(xyc, c[:], (x1, y1), method='cubic')
      ozn[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())

    fnameO=pwd+dir+hh+'-ozone-surface-level-fcst-'+grds+'.json'
    with open(fnameO,'w') as f:
      json.dump(ozn,f)
