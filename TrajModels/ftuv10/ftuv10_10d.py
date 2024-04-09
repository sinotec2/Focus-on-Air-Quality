# cat /nas1/backup/data/cwb/e-service/btraj_WRFnests/ftuv10_10d.py
#!/opt/miniconda3/envs/py37/bin/python
import bisect
from datetime import datetime, timedelta
import netCDF4
import numpy as np
import os, sys, subprocess, time, json
from pandas import *
from pyproj import Proj
from scipy import interpolate
from scipy.io import FortranFile
from scipy.interpolate import griddata
import twd97

#get the UVW data from NC files
#z not interpolated yet
def get_uvw(ncft,t0,z,y,x):
  (ncf,tt)=ncft[:]
  t=1#abs(tt-t0)
  n0=locate_nest(x,y)
  #make sure the point is in d1(at least)
  if n0==-1:
    return -1
  iii=int(x//dx[M]+ncol[M]//2)
  jjj=int(y//dx[M]+nrow[M]//2)
  kkk=int(z//dz)
  idx=(t,kkk,jjj,iii)
  if idx in f: return idx,f

  #loop for every possible nest
  for n in range(n0,n0-1,-1):
    ix=int(x//dx[n]+ncol[n]//2)
    iy=int(y//dx[n]+nrow[n]//2)
#   print(ix,iy)
    iz=1 #bisect.bisect_left(zh[n][t1,:,iy,ix],z)

    #the data are stored in the vast, sparce matrix
    for k in range(max(0,iz-1),min(iz+3,nlay[n])):
      kk=int(z//dz)
      for j in range(max(0,iy-1),min(iy+3,nrow[n])):
        if j+1>=ncf[n].variables['U10'].shape[-2]:continue
        jj=int((j-nrow[n]//2)*fac[n] +nrow[M]//2)
        for i in range(max(0,ix-1),min(ix+3,ncol[n])):
          if i+1>=ncf[n].variables['U10'].shape[-1]:continue
          ii=int((i-ncol[n]//2)*fac[n] +ncol[M]//2)
          if (t,kk,jj,ii) in withdata:continue
          #average the stagger wind to the grid_points
          if ii>=ncol[M] or jj>=nrow[M]:continue
          uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U10'][tt,j,i]+ncf[n].variables['U10'][tt,j,i+1])/2.
          uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V10'][tt,j,i]+ncf[n].variables['V10'][tt,j+1,i])/2.
          uvwg[2,t,kk,jj,ii]=0.#(ncf[n].variables['W'][tt,k,j,i]+ncf[n].variables['W'][tt,k+1,j,i])/2.
          #np.where(abs(uvwg)>0) is too slow, remember the locations directly
          withdata.append((t,kk,jj,ii))
  wd2=[i[2] for i in withdata]
  wd3=[i[3] for i in withdata]
  xx,yy=x_g[wd2,wd3], y_g[wd2,wd3]
  if n0<3:
    xx_mesh, yy_mesh=np.arange(min(xx),max(xx)+1,3000),np.arange(min(yy),max(yy)+1,3000)
    iis,jjs=x_mesh.index(min(xx)),  y_mesh.index(min(yy))
    iie,jje=x_mesh.index(max(xx))+1,y_mesh.index(max(yy))+1
    xxg, yyg = np.meshgrid(xx_mesh, yy_mesh)
    for Lv in range(3):
      if len(set(xx))>1 and len(set(yy))>1:
        points=[(i,j) for i,j in zip(xx,yy)]
        grid_z2 = griddata(points, uvwg[Lv,t,kk,wd2,wd3], (xxg, yyg),  method='linear')
        uvwg[Lv,t,kk,jjs:jje,iis:iie]=grid_z2

  fcn=[]
#  for Lv in range(3):
#    try:
#      fcn.append(interpolate.interp2d(yy, xx, uvwg[Lv,t,kk,wd2,wd3], kind='cubic'))
#    except:
#      fcn.append(interpolate.interp2d(yy, xx, uvwg[Lv,t,kk,wd2,wd3], kind='linear'))
#  f.update({idx:fcn})
  return idx,f

def locate_nest(x,y):
    for n in range(1,-1,-1):
        if xmin[n]<=x<xmax[n] and ymin[n]<=y<ymax[n]:
            return n
    return -1


def getarg():
  """ read time period and station name from argument(std input)
  traj2kml.py -t daliao -d 20171231 """
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument("-t", "--STNAM", required=True, type=str, help="station name,sep by ,or Lat,Lon")
  ap.add_argument("-d", "--DATE", required=True, type=str, help="yyyymmddhh")
  ap.add_argument("-b", "--BACK", required=True, type=str, help="True or False")
  args = vars(ap.parse_args())
  return [args['STNAM'], args['DATE'],args['BACK']]

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def nstnam():
  import json
  fn = open(path+'sta_list.json')
  d_nstnam = json.load(fn)
  d_namnst = {v: k for k, v in d_nstnam.items()}
  return (d_nstnam, d_namnst)


def beyond(xpp, ypp, zpp, ddt):
  dday= abs(ddt.total_seconds()/3600/24)
  boo = not (((xpp - x_mesh[0]) * (xpp - x_mesh[-1]) < 0 and \
             (ypp - y_mesh[0]) * (ypp - y_mesh[-1]) < 0 and \
             (zpp - z_mesh[0]) * (zpp - z_mesh[-1]) < 0  ) and \
                         (dday <= 5))
  return boo


#open the NC's for some day (this present day, first time, or next/yesterday)
def openNC(sdate):
  uvPath='/nas2/backup/data/NOAA/NCEP/GFS/YYYY/tw_CWBWRF_45k/'
  uvHead='U10V10_d0'
  if M==2:uvTail='_06:00:00' # CWB WRF
  if M==3:uvTail='_00:00:00' # fcst WRF
  UTCstart=int(uvTail[1:3])
  gdate=sdate+timedelta(hours=-8)
  dd=0
  if UTCstart>0 and gdate.hour<UTCstart:dd=-1
  ymd = (gdate+timedelta(days=dd)).strftime('%Y-%m-%d')
  dd=-5
  if BF==1: dd=-1# forward traj
  ymdPath = (bdate+timedelta(days=dd)).strftime('%Y%m%d')
  if M==3:
    fnames=[uvPath+ymdPath+'/'+uvHead+str(i)+'_'+ymd+uvTail for i in range(1,M+1)] #d01~d03
    fnames[2]=fnames[2].replace('tw_CWBWRF_45k','TWEPA_3k') #d03 locate at different path
  elif M==2:
    fnames=[uvPath+str(i)+'_'+ymd+uvTail for i in [1,3]]
  ncf,mt,mlay,mrow,mcol,dtimes=[],[],[],[],[],[]
  for fname in fnames:
    print(fname)
    if not os.path.isfile(fname): sys.exit('no file for '+fname)
    nc1=netCDF4.Dataset(fname,'r')
    ncf.append(nc1)
    v3=list(filter(lambda x:nc1.variables[x].ndim==3, [i for i in nc1.variables]))
    t,row,col=nc1.variables['U10'].shape
    lay=1
    for v in 't,lay,row,col'.split(','):
      exec('m'+v+'.append('+v+')')
    #get Times in datetime form (local time)
    dtime=[]
    for it in range(t):
      s=''
      for j in [i.decode('utf-8') for i in nc1.variables['Times'][it,:]]:
        s+=j
      dtime.append(datetime.strptime(s,"%Y-%m-%d_%H:00:00")+timedelta(hours=8))
    if sdate not in dtime:
      print(sdate,'not in ',fname)
      return [[-1] for i in range(6)]
#sys.exit('Times not right'+ymd)
    dtimes.append(dtime)
  return ncf, mt, mlay, mrow, mcol, dtimes

path='/nas1/backup/data/cwb/e-service/surf_trj/'
# restore the matrix

(d_nstnam, d_namnst) = nstnam()
stnam, DATE, BACK = getarg()
BACK=str2bool(BACK)
BF=-1
M=3 #number of nests 2: CWB_WRF, 3:fcst_WRF
if not BACK:BF=1
bdate = datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:]))
nc, nt, nlay, nrow, ncol, dtimes0 = openNC(bdate)
Latitude_Pole, Longitude_Pole = nc[1].CEN_LAT, nc[1].CEN_LON
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

nam = [i for i in stnam.split(',')]
print(nam)
x0, y0 = [], []
if len(nam) > 1:
  try:
    lat = float(nam[0])
    lon = float(nam[1])
  except:
    sys.exit('more than two station, suggest executing iteratively')
  else:
    # in case of lat,lon
    if lat < 90.:
#      xy0 = twd97.fromwgs84(lat,lon)
#      x0, y0 =([xy0[i]] for i in [0,1])
#      x0,y0=x0-Xcent,y0-Ycent
      xx0,yy0=pnyc(lon,lat, inverse=False)
      x0.append(xx0)
      y0.append(yy0)
      nam[0] = str(round(lat,2))+'_'+str(round(lon,2))+'_'
    #   in case of twd97_x,y
    else:
      # test the coordinate unit
      if lat>1000.:
        x0, y0 = [lat],[lon]
        x0,y0=x0-Xcent,y0-Ycent
        nam[0] = str(int(lat/1000))+'+'+str(int(lon/1000))+'_'
      else:
        x0, y0 = [lat*1000],[lon*1000]
        x0,y0=x0-Xcent,y0-Ycent
        nam[0] = str(int(lat))+'_'+str(int(lon))+'_'

# len(nam)==1, read the location from csv files
else:
  for stnam in nam:
    if stnam not in d_namnst: sys.exit("station name not right: " + stnam)
  nst = [int(d_namnst[i]) for i in nam]
  # locations of air quality stations
  # read from the EPA web.sprx
  fname = path+'sta_ll.csv'
  sta_list = read_csv(fname)
  for s in nst:
    sta1 = sta_list.loc[sta_list.ID == s].reset_index(drop=True)
    xx0,yy0=pnyc(list(sta1['lon'])[0],list(sta1['lat'])[0], inverse=False)
    x0.append(xx0) #list(sta1['twd_x'])[0]-Xcent)
    y0.append(yy0) #list(sta1['twd_y'])[0]-Ycent)

#initialization of traj. source, output and label lists
xp, yp, zp = x0, y0, [50.]
print('len_nc',len(nc))
pdate = bdate
nc0=nc
nc1=nc
nlay.append(251)
nrow.append(nrow[0]*5)
ncol.append(ncol[0]*5)
if M==3:
  dx=[45000,9000,3000,3000]
elif M==2:
  dx=[15000,3000,3000]
dz=20
fac=[dx[n]//dx[M] for n in range(M+1)]
#_mesh and _g in lamber conifer projection system
x_mesh = [(i-ncol[M]//2)*dx[M] for i in range(ncol[M])]
y_mesh = [(j-nrow[M]//2)*dx[M] for j in range(nrow[M])]
z_mesh = [k*dz for k in range(nlay[M])]
x_g, y_g = np.meshgrid(x_mesh, y_mesh)
xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(M)]
xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(M)]
ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(M)]
ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(M)]
#zh=[]
#for n in range(2):
#  ph_n=nc[n].variables['PH'][:,:,:,:]
#  phb_n=nc[n].variables['PHB'][:,:,:,:]
#  ph=(ph_n+phb_n)/9.81
#  zh_n=np.zeros(shape=(nt[n],nlay[n]+1,nrow[n],ncol[n],))
#  for k in range(nlay[n]):
#    zh_n[:,k+1,:,:]=ph[:,k+1,:,:]-ph[:,0,:,:]
#  zh_n=np.clip(zh_n,0.,np.max(zh_n))
#  zh.append(zh_n)

uvwt=np.zeros(shape=(2,3))
delt = 15
s = 0
o_ymdh,o_time,o_xp,o_yp,o_zp,l_xp,l_yp,l_zp=[],[],[],[],[],[],[],[]
itime=0
ymdh=int(DATE)
o_ymdh.append('ymd='+DATE+'_'+str(int(round(zp[s],0))))
o_time.append('hour='+str(itime))
for i in 'ol':
  for j in 'xy':
    print(i+'_'+j+'p.append('+j+'p[s]+'+j.upper()+'cent)')
    exec(i+'_'+j+'p.append('+j+'p[s]+'+j.upper()+'cent)') #
o_zp.append(zp[s])
l_zp.append(zp[s])
IW=0
#loop for traj as long as in the domain and 24 hours
while not beyond(xp[s], yp[s], zp[s], pdate-bdate):
  print ('run within domain, ymdh=' + str(ymdh))
#    break
  t0=dtimes0[0].index(pdate)
  t1=t0+BF
  if nt[0]==24:
    boo=(t1==nt[0]) #in case of forward traj.
  else:
    boo=(bdate.hour+int(abs((pdate-bdate).total_seconds()/3600))==nt[0])
  if boo or t1<0:
    if nt[0]!=24:break
    sdate = pdate + timedelta(hours=BF)
    nc1,nt,dnlay,dnrow,dncol, dtimes0 = openNC(sdate)
    if type(nc1)==int:break
    if BACK:
      t1=t1+nt[0]
    else:
      t1=0
  f={}
  withdata=[]
  uvwg=np.zeros(shape=(3,2,nlay[M],nrow[M],ncol[M],))
  for sec in range(0, 3601, delt):
    boo = beyond(xp[s], yp[s], zp[s], pdate-bdate)
    if boo:
#      print('beyond TRUE')
      break
    for ncft in [(nc0,t0),(nc1,t1)]:
      result=get_uvw(ncft,t0,zp[s],yp[s],xp[s])
      if result==-1:break
      (tt,kk,jj,ii),f=result[0], result[1]
      uvwt[tt,:] = [uvwg[i,tt,kk,jj,ii] for i in range(3)]# [f[(tt,kk,jj,ii)][i](yp[s],xp[s]) for i in range(3)]
    if result==-1:break
    fcnt=interpolate.interp1d([0,3600], uvwt,axis=0)
    ub, vb, wb= fcnt(sec)
    xp[s], yp[s], zp[s] = xp[s]+BF*delt * ub, yp[s]+BF*delt * vb,  zp[s]+BF*delt * wb
    l_xp.append(xp[s]+Xcent)
    l_yp.append(yp[s]+Ycent)
    l_zp.append(zp[s])
  if result==-1:break
  pdate = pdate + timedelta(hours=BF)
  ymdh = int(pdate.strftime('%Y%m%d%H'))
  itime+=1
  o_ymdh.append('ymd='+str(ymdh)+'_'+str(int(round(zp[s],0))))
  o_time.append('hour='+str(itime))
  o_xp.append(xp[s]+Xcent)
  o_yp.append(yp[s]+Ycent)
  o_zp.append(zp[s])

  if pdate not in dtimes0[0]:
    if nt[0]==24:
      nc0,nt,dnlay,dnrow,dncol, dtimes0 = openNC(pdate)
      if type(nc0)==int:break
      nc1=nc0
    if nt[0]<24:break
  nc0=nc1 #shift the nc
  df=DataFrame({'ymdh':o_ymdh,'xp':o_xp,'yp':o_yp,'zp':o_zp,'Hour':o_time})
  #geodetic LL
  lon, lat = pnyc(np.array(o_xp)-Xcent,np.array(o_yp)-Ycent, inverse=True)
  dfg=DataFrame({'lon':lon,'lat':lat})

  col=['xp','yp','Hour','ymdh','zp']
  dr='f'
  if BACK:dr='b'
  name='trj_results/'+dr+'trj'+nam[0]+DATE+'.csv'
  # output the line segments for each delta_t
  dfL=DataFrame({'TWD97_x':l_xp,'TWD97_y':l_yp,'zp':l_zp})
  #geodetic LL
  lon, lat = pnyc(np.array(l_xp)-Xcent, np.array(l_yp)-Ycent, inverse=True)
  dfLg=DataFrame({'lon':lon,'lat':lat})

  if IW==0:
    df[col].set_index('xp').to_csv(name)
    dfg.set_index('lon').to_csv(name.replace('.csv','_mark.csv'),header=None)
    dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'))
    dfLg.set_index('lon').to_csv(name.replace('.csv','_line.csv'),header=None)
    IW=1
  else:
    df[col].set_index('xp').to_csv(name,mode='a',header=False)
    dfg.set_index('lon').to_csv(name.replace('.csv','_mark.csv'),mode='a',header=None)
    dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'),mode='a',header=False)
    dfLg.set_index('lon').to_csv(name.replace('.csv','_line.csv'),mode='a',header=None)
  o_ymdh,o_time,o_xp,o_yp,o_zp,l_xp,l_yp,l_zp=[],[],[],[],[],[],[],[]

#make kml file
dir='NL'
if not BACK:dir='NL'
os.system('/usr/kbin/csv2kml.py -f '+name+' -n '+dir+' -g TWD97')
os.system('/usr/kbin/csv2bln.cs '+name)
with open('trj_results/filename.txt','w') as f:
  f.write(name.split('/')[1])
