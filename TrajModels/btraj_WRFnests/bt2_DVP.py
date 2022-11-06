#kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
#$ cat bt2_DVP.py
#!/cluster/miniconda/envs/py37/bin/python
import numpy as np
from pandas import *
import os, sys, subprocess, time, json
from scipy.io import FortranFile
from datetime import datetime, timedelta
import twd97
import netCDF4
from pyproj import Proj
import subprocess
from pandas import *
from scipy import interpolate
from scipy.interpolate import griddata
import bisect

#get the UVW data from NC files
#z not interpolated yet
def get_uvw(ncft,t0,z,y,x):
  (ncf,t1)=ncft[:]
  t=abs(t1-t0)
  n0=locate_nest(x,y)
  #make sure the point is in d1(at least)
  if n0==-1:
    return -1
  iii=int(x//dx[4]+ncol[4]//2)
  jjj=int(y//dx[4]+nrow[4]//2)
  kkk=int(z//dz)
  idx=(t,kkk,jjj,iii)
  if idx in f: return idx,f

  #loop for every possible nest
  for n in range(n0,n0-1,-1):
    ix=int(x//dx[n]+ncol[n]//2)
    iy=int(y//dx[n]+nrow[n]//2)
#   print(ix,iy)
    iz=bisect.bisect_left(zh[n][t1,:,iy,ix],z)

    #the data are stored in the vast, sparce matrix
    for k in range(max(0,iz-1),min(iz+3,nlay[n])):
      kk=int(z//dz)
      for j in range(max(0,iy-1),min(iy+3,nrow[n])):
        jj=int((j-nrow[n]//2)*fac[n] +nrow[4]//2)
        for i in range(max(0,ix-1),min(ix+3,ncol[n])):
          ii=int((i-ncol[n]//2)*fac[n] +ncol[4]//2)
          if (t,kk,jj,ii) in withdata:continue
          #average the stagger wind to the grid_points
          uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U'][t1,k,j,i]+ncf[n].variables['U'][t1,k,j,i+1])/2.
          uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V'][t1,k,j,i]+ncf[n].variables['V'][t1,k,j+1,i])/2.
          uvwg[2,t,kk,jj,ii]=(ncf[n].variables['W'][t1,k,j,i]+ncf[n].variables['W'][t1,k+1,j,i])/2.
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
      points=[(i,j) for i,j in zip(xx,yy)]
      grid_z2 = griddata(points, uvwg[Lv,t,kk,wd2,wd3], (xxg, yyg),  method='cubic')      
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
    for n in range(3,-1,-1):
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


def beyond(xpp, ypp, zpp):
  boo = not ((xpp - x_mesh[0]) * (xpp - x_mesh[-1]) < 0 and \
             (ypp - y_mesh[0]) * (ypp - y_mesh[-1]) < 0 and \
             (zpp - z_mesh[0]) * (zpp - z_mesh[-1]) < 0)
  return boo


#open the NC's for some day (this present day, first time, or next/yesterday)
def openNC(sdate):
  ymd = sdate.strftime('%Y-%m-%d')
  fnames=['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]
  ncf,nt,nlay,nrow,ncol=[],[],[],[],[]
  for fname in fnames:
    if not os.path.isfile(fname): sys.exit('no file for '+fname)
    nc1=netCDF4.Dataset(fname,'r')
    ncf.append(nc1)
    v4=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))
    t,lay,row,col=nc1.variables['T'].shape
    for v in 't,lay,row,col'.split(','):
      exec('n'+v+'.append('+v+')')
  return ncf, nt, nlay, nrow, ncol, ymd.replace('-','')

path='/nas1/backup/data/cwb/e-service/surf_trj/'
# restore the matrix

(d_nstnam, d_namnst) = nstnam()
stnam, DATE, BACK = getarg()
os.system('mkdir -p trj_results'+DATE[2:6])
BACK=str2bool(BACK)
BF=-1
if not BACK:BF=1
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
bdate = datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:]))
nam = [i for i in stnam.split(',')]
if len(nam) > 1:
  try:
    lat = float(nam[0])
    lon = float(nam[1])
  except:
    sys.exit('more than two station, suggest executing iteratively')
  else:
    # in case of lat,lon
    if lat < 90.:
      xy0 = twd97.fromwgs84(lat,lon)
      x0, y0 =([xy0[i]] for i in [0,1])
      x0,y0=x0-Xcent,y0-Ycent
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
  x0, y0 = [], []
  for s in nst:
    sta1 = sta_list.loc[sta_list.ID == s].reset_index(drop=True)
    x0.append(list(sta1['twd_x'])[0]-Xcent)
    y0.append(list(sta1['twd_y'])[0]-Ycent)

#initialization of traj. source, output and label lists
xp, yp, zp = x0, y0, [50.]
pdate = bdate
nc, nt, nlay, nrow, ncol, ymd0 = openNC(pdate)
nc0=nc
nc1=nc
nlay.append(251)
nrow.append(nrow[0]*27)
ncol.append(ncol[0]*27)
dx=[81000,27000,9000,3000,3000]
dz=20
fac=[dx[n]//dx[4] for n in range(5)]
#_mesh and _g in lamber conifer projection system
x_mesh = [(i-ncol[4]//2)*dx[4] for i in range(ncol[4])]
y_mesh = [(j-nrow[4]//2)*dx[4] for j in range(nrow[4])]
z_mesh = [k*dz for k in range(nlay[4])]
x_g, y_g = np.meshgrid(x_mesh, y_mesh)
xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(4)]
xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(4)]
ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(4)]
ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(4)]
zh=[]
for n in range(4):
  ph_n=nc[n].variables['PH'][:,:,:,:]
  phb_n=nc[n].variables['PHB'][:,:,:,:]
  ph=(ph_n+phb_n)/9.81
  zh_n=np.zeros(shape=(nt[n],nlay[n]+1,nrow[n],ncol[n],))
  for k in range(nlay[n]):
    zh_n[:,k+1,:,:]=ph[:,k+1,:,:]-ph[:,0,:,:]
  zh_n=np.clip(zh_n,0.,np.max(zh_n))
  zh.append(zh_n)

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
    exec(i+'_'+j+'p.append('+j+'p[s]+'+j.upper()+'cent)') #
o_zp.append(zp[s])
l_zp.append(zp[s])
IW=0
#loop for traj as long as in the domain and 24 hours
while not beyond(xp[s], yp[s], zp[s]):
  print ('run beyond days' + str(ymdh))
#    break
  t0=pdate.hour
  t1=t0+BF
  if t1==24 or t1<0:
    sdate = pdate + timedelta(hours=BF)
    nc1,dnt,dnlay,dnrow,dncol,dymd0 = openNC(sdate)

  f={}
  withdata=[]
  uvwg=np.zeros(shape=(3,2,nlay[4],nrow[4],ncol[4],))
  for sec in range(0, 3601, delt):
    boo = beyond(xp[s], yp[s], zp[s])
    if boo: break
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

  if pdate.strftime('%Y%m%d') != ymd0:
    nc0,dnt,dnlay,dnrow,dncol, ymd0 = openNC(pdate)
    nc1=nc0
  df=DataFrame({'ymdh':o_ymdh,'xp':o_xp,'yp':o_yp,'zp':o_zp,'Hour':o_time})
  col=['xp','yp','Hour','ymdh','zp']
  name='trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
  # output the line segments for each delta_t
  dfL=DataFrame({'TWD97_x':l_xp,'TWD97_y':l_yp,'zp':l_zp})
  if IW==0:
    df[col].set_index('xp').to_csv(name)
    dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'))
    IW=1
  else:
    df[col].set_index('xp').to_csv(name,mode='a',header=False)
    dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'),mode='a',header=False)
  o_ymdh,o_time,o_xp,o_yp,o_zp,l_xp,l_yp,l_zp=[],[],[],[],[],[],[],[]

#make kml file
dir='NL'
if not BACK:dir='RL'
os.system('csv2kml.py -f '+name+' -n '+dir+' -g TWD97')
os.system('csv2bln.cs '+name)
