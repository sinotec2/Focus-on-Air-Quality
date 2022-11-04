#$ cat /Users/kuang/bin/addVI.py
#!/opt/anaconda3/bin/python
import numpy as np
import netCDF4
from pandas import *
import os, sys, datetime, subprocess
from pyproj import Proj
import twd97
from scipy.interpolate import griddata

#declarations of local parameters
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
path='/Users/Data/cwb/e-service/btraj_WRFnests/CWB_forecast/'
head='U10V10_d03_'
tail='_06:00:00'
bh_wrf=int(tail[1:3])

fname=sys.argv[1]
idx=fname.index('.csv')-10
ymdh=fname[idx:idx+10]
BF=-1
try:
  bdate=datetime.datetime.strptime(ymdh,'%Y%m%d%H')
  if 'ftrj' in fname:BF=1
except:
  pwd=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[-1]
  if pwd in ['00','p1','p2','m1','m2']:
    pm=1
    if pwd[0]=='m':pm=-1
    del_pm=int(pwd[1])
    ymdh=(datetime.datetime.now()+datetime.timedelta(days=pm*del_pm)).strftime('%Y%m%d')+'12'
    bdate=datetime.datetime.strptime(ymdh,'%Y%m%d%H')
  else:
    sys.exit('wrong excution location')
#open and read csv file
df=read_csv(fname)
#if 'VI' in df.columns:sys.exit('VI already in file: '+fname)
col0=list(df.columns)
col=[i[:3].lower() for i in df.columns if len(i)>=3]
#in case of TWD97
if 'lat' not in col or min(df[df.columns[0]])>360.:
  x,y=np.array(df[df.columns[0]])-Xcent,np.array(df[df.columns[1]])-Ycent
  lon,lat= pnyc(  x,  y, inverse=True)
else:
  lon,lat=np.array(df[df.columns[0]]),np.array(df[df.columns[1]])
  x, y = pnyc(lon,lat, inverse=False)
#UTC time
if 'Title' in col0:
  ttl=np.array(df.Title)
  idx=np.where(ttl==0)[0]
  ntrj=len(idx)
  ends=[idx[i+1] for i in range(ntrj-1)]+[len(df)]
  lngs=[ends[i]-idx[i] for i in range(ntrj)]
  dd=[]
  dates=[bdate+datetime.timedelta(hours=t*BF-8) for t in range(max(lngs))]
  for n in range(ntrj):
    dd+=[dates[i] for i in range(lngs[n])]
  df['date']=dd
  nTail=ends[0]-1
else:
  dates=[bdate+datetime.timedelta(hours=t*BF-8) for t in range(len(df))]
  df['date']=dates
  nTail=len(df)

fdate=dates[0].strftime('%Y-%m-%d')
if bh_wrf>0 and dates[0].hour<bh_wrf:
  fdate=(dates[0]+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
fn=path+head+fdate+tail
nc = netCDF4.Dataset(fn,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
if 'PBLH' not in V[2]:sys.exit('PBLH not found in nc file: '+fn)
for s in V[2]:
  exec(s+'=nc.variables["'+s+'"][:]')
WS=np.sqrt(U10*U10+V10*V10)
PBLH[np.where(np.isnan(PBLH))[:]]=35.
PBLH[np.where(PBLH<35.)[:]]=35.
VI=WS*PBLH
nt,nrow,ncol=VI.shape
strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
long,latg=XLONG[0,:,:].flatten(),XLAT[0,:,:].flatten()
Xg, Yg = pnyc(long,latg, inverse=False)
Xg, Yg = Xg.reshape(nrow,ncol), Yg.reshape(nrow,ncol)
mnx,mxx=np.min(x)-nc.DX,np.max(x)+nc.DX
mny,mxy=np.min(y)-nc.DY,np.max(y)+nc.DY
idxx=np.where((mnx<Xg)&(Xg<mxx))
idxy=np.where((mny<Yg[idxx[:]])&(Yg[idxx]<mxy))
ny=len(idxy[0])
xyc= [(Xg[idxx[0][idxy[0][i]],idxx[1][idxy[0][i]]],Yg[idxx[0][idxy[0][i]],idxx[1][idxy[0][i]]]) for i in range(ny)]
ventI=[]
for dd in range(len(df)):
  now=df.date[dd]
  t=Times.index(now)
  var=VI[:]
  c = np.array([var[t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
  x1,y1=x[dd],y[dd]
  v=griddata(xyc, c, (x1, y1), method='linear')
  if np.isnan(v):
    var=WS[:]
    c = np.array([var[t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
    w=griddata(xyc, c, (x1, y1), method='linear')
    var=PBLH[:]
    c = np.array([var[t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
    p=griddata(xyc, c, (x1, y1), method='linear')
    print(now,w,p)
  ventI.append(griddata(xyc, c, (x1, y1), method='linear'))
  fdate=(now+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
  if dd==len(df)-1:continue #no need to openfile any more
  if bh_wrf==now.hour or now==dates[nTail]:
    if now==dates[nTail]:
      fdate=dates[0].strftime('%Y-%m-%d')
      if bh_wrf>0 and dates[0].hour<bh_wrf:
        fdate=(dates[0]+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    fn=path+head+fdate+tail
    nc = netCDF4.Dataset(fn,'r')
    for s in V[2]:
      if s in nc.variables:
        exec(s+'=nc.variables["'+s+'"][:]')
    WS=np.sqrt(U10*U10+V10*V10)
    PBLH[np.where(np.isnan(PBLH))[:]]=35.
    PBLH[np.where(PBLH<35.)[:]]=35.
    VI=WS*PBLH
    strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
    Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
df['VI']=ventI
df['lng']=lon
df['lat']=lat
df.VI=[round(i.item(),1) for i in df.VI]
df.date=[d+datetime.timedelta(hours=+8) for d in df.date]
col2=['lng','lat']+col0[2:]+['VI','date']
fnameO=fname.replace('.csv','V.csv')
df[col2].set_index('lng').to_csv(fnameO)
os.system('/opt/anaconda3/bin/csv_to_geojson '+fnameO)
