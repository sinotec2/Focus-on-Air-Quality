import numpy as np
import twd97
import os, sys
from pyproj import Proj
from terrainXYINC import terrainXYINC
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)


def rd_SO(STR):
  loc='LOCATION'
  lloc=len(loc)
  nsrc=STR.count(loc)
  ibeg,iend=[lloc],[len(STR)]
  snamo,pav,orig=([] for i in range(3))
  if nsrc>1:
    ibeg=[i+lloc for i in range(len(STR)-lloc) if STR[i:i+lloc]==loc]
    iend=[ibeg[i]-lloc for i in range(1,nsrc)]
    iend=iend+[ibeg[nsrc-1]+iend[nsrc-2]-ibeg[nsrc-2]]

  for isrc in range(nsrc):
    try:
      inp=STR[ibeg[isrc]:iend[isrc]].split()
    except:
     print"""parameter errors!</body></html>"""
     sys.exit()
    pav_i=inp[1]
    if pav_i in ['AREA','POINT','VOLUME']:
      snamo.append(inp[0])
      pav.append(inp[1]) #POINT/AREA/VOLUME tag
      orig.append([float(inp[i].replace('SO','')) for i in range(2,4)])
    else:
      print"""<p>path not right:%s, must be any one of AREA/POINT/VOLUME.</body></html>"""%pav_i
      sys.exit("path not right")
  #read the area sources
  par='SRCPARAM'
  ipar=STR.index(par)
  lpar=len(par)
  ibeg,iend=[ipar+lpar],[ipar+len(STR)]
  if nsrc>1:
    ibeg=[i+lpar for i in range(len(STR)-lpar) if STR[i:i+lpar]==par]
    iend=[ibeg[i]-lpar for i in range(1,nsrc)]
    iend=iend+[ibeg[nsrc-1]+iend[nsrc-2]-ibeg[nsrc-2]]
  snamp,H=([] for i in range(2))
  for isrc in range(nsrc):
    inp=STR[ibeg[isrc]:iend[isrc]].split()
    if inp[0] not in snamo:
      print"""<p>src names of LOC/PAR not right: %s</body></html>""" %inp[0]
      os.system('echo "src names of LOC/PAR not right: '+inp[0]+'"'+OUT)
      sys.exit('') #premature error
    snamp.append(inp[0])
    H.append(float(inp[2]))
  print"""<p>%s %s %s %s</body></html>""" % (snamo[0],orig[0][0],orig[0][1],max(H))
  return snamo[0],orig[0][0],orig[0][1],max(H)

def twdIJ1(xv,yv):
  return (int((xv-Xcent)/1000)+int(83*3/2))*1000+int((yv-Ycent)/1000)+int(137*3/2)

def terrainLOCAT(pth,snamo,P0,P1,Hs):
  from pandas import read_csv, DataFrame
  import os
  import netCDF4

  WEB='/Library/WebServer/Documents/'
  CGI='/Library/WebServer/CGI-Executables/isc/'
  OUT='>> '+pth+'isc.out'
  geninp='/opt/local/bin/gen_inp.py'
  WAITM='/opt/local/bin/wait_map.cs'
  CSV=WEB+'terr_results/TWN_1X1REC.csv'
  reg='GRIDCART'
  P=[P0,P1]
  GEO='/Users/WRF4.1/WPS/geo_em.d04_333m.nc'  
  nc = netCDF4.Dataset(GEO, 'r')
  v='HGT_M'
  c=np.array(nc.variables[v][0,:,:])
  for v in ['CLAT','CLONG']:
    exec(v+'=nc.variables[v][0,:,:]',locals())
  xg,yg=pnyc(CLONG,CLAT, inverse=False)
  xg+=Xcent
  yg+=Ycent
  d=(xg-P[0])**2+(yg-P[1])**2
  idx=np.where(d==np.min(d))
  base=max([0,c[idx[0][0],idx[1][0]]])
  dx=round(min([250,Hs]),-1)*2
  nx,ny=40,40
  x0n,y0n=(round(P[i]-dx*nx/2, -2) for i in range(2))
  x0x,y0x=(round(P[i]+dx*ny/2, -2) for i in range(2))
  
  #FLAT or COMPLEX TERRAIN
  boo=(x0n<=xg) & (xg<=x0x) & (y0n<=yg) & (yg<=y0x)
  idx=np.where(boo)
  maxBase=np.max(c[idx[0],idx[1]])
  run_aermap=False
  if maxBase > Hs:
    HEI3=min(Hs*2+base,maxBase)
    if HEI3>=maxBase:
      dx=(x0x-x0n)/nx
    else:
      boo=(HEI3<=c) & (c<=maxBase)
      idx=np.where(boo)
      dist=[np.sqrt((xg[i,j]-P[0])**2+(yg[i,j]-P[1])**2) for i,j in zip(idx[0],idx[1])]
      dx=40.
      nx=int(min(dist)*3/dx)
    x0n,y0n=(round(P[i]-dx*nx/2, -2) for i in range(2))
    x0x,y0x=(round(P[i]+dx*nx/2, -2) for i in range(2))
    x0,nx,dx,y0,ny,dy=(int(x0n),nx,int(dx),int(y0n),nx,int(dx))
    rec_txt='RE GRIDCART %s XYINC %s %s %s %s %s %s' %(snamo,x0,nx,dx,y0,ny,dy)
    RECroot=terrainXYINC(pth,rec_txt)
  return snamo
