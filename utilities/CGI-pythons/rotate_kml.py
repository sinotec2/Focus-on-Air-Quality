# cat ./isc/rotate_kml.py
#!/opt/anaconda3/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb; cgitb.enable()
import tempfile as tf

import numpy as np
import math
from pykml import parser
from pandas import *
from pyproj import Proj
import sys, os
import twd97
import netCDF4
import subprocess

from rd_kmlLL import rd_kmlLL

#rotate the matrix with respect to certain point
def rotate_about_a_point(target_point,center_point,angle_rs):
  cp=np.subtract(target_point,center_point)
  px=cp[0]*math.cos(math.radians(angle_rs))+cp[1]*-math.sin(math.radians(angle_rs))
  py=cp[0]*math.sin(math.radians(angle_rs))+cp[1]*math.cos(math.radians(angle_rs))
  return(np.add([px,py],center_point))

#paths

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth=WEB+'isc_results/rott_'+ran+'/'
os.system('mkdir -p '+pth)
OUT='>> '+pth+'isc.out'
NULL=' >&/dev/null'
geo_name='/Users/WRF4.1/WPS/geo_em.d04_333m.nc'
tedsp_name=WEB+'isc_results/point_QC.csv'

print ('Content-Type: text/html\n\n')
with open(CGI+'header.txt','r') as f:
  lines=[l for l in f]
  for l in lines:
    print(l)
form = cgi.FieldStorage()
try:
  fileitem = form['filename']
except:
  print ('filename not given or not right')
  print ('</body></html>')
  sys.exit()

fn = os.path.basename(fileitem.filename)
open(pth+fn, 'wb').write(fileitem.file.read())

kml_file = os.path.join(pth+fn)
nplgs,npnts,names,hgts,lon,lat,lonp,latp=rd_kmlLL(kml_file)
nplms=nplgs+npnts
print ('filename given and opened as: '+pth+fn+'</br>')
print ('</body></html>')

Latitude_Pole, Longitude_Pole = np.mean(lat),np.mean(lon)
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

x,y=pnyc(lon,lat, inverse=False)
x+=Xcent
y+=Ycent
dir=np.zeros(shape=(nplgs,4))
for i in range(nplgs):
  diri=[90-math.atan2((y[i,j+1]-y[i,j]),(x[i,j+1]-x[i,j]))*180/math.pi for j in range(4)]
  diri.sort()
#   from North and clockwise
  dir[i,:]=np.array(diri)
if max( [np.std(dir[:,j]) for j in range(4)])>10:
  print ('wrong direction or skewed!</br>')
  for i in range(nplgs):
    print (('dir for building# {:d} is: {:f} {:f} {:f} {:f}</br>').format(i,*dir[i,:]))
  print ('</body></html>')
  sys.exit('wrong direction or skewed!')

P=[(i,j) for i,j in zip(x[:,:4].flatten(),y[:,:4].flatten())]
angl= min([np.mean(dir[:,j]) for j in range(4)])
if angl<0:angl+=360.
orig=P[0]
Pn=[rotate_about_a_point(pnt,orig,angl) for pnt in P]
Pn=np.array(Pn).flatten().reshape(nplgs,4,2)
#mnx, mny=(np.min(Pn[:,:,i]) for i in range(2))
Pn[:,:,0]+=-orig[0] #-mnx
Pn[:,:,1]+=-orig[1] #-mny

for i in range(nplgs):
  xm,ym=np.mean(Pn[i,:,0]),np.mean(Pn[i,:,1])
  x1=sum([Pn[i,j,0] for j in range(4) if Pn[i,j,0] < xm])/2
  x2=sum([Pn[i,j,0] for j in range(4) if Pn[i,j,0] > xm])/2
  y1=sum([Pn[i,j,1] for j in range(4) if Pn[i,j,1] < ym])/2
  y2=sum([Pn[i,j,1] for j in range(4) if Pn[i,j,1] > ym])/2
  Pn[i,0,0],Pn[i,3,0]=x1,x1
  Pn[i,1,0],Pn[i,2,0]=x2,x2
  Pn[i,0,1],Pn[i,1,1]=y1,y1
  Pn[i,2,1],Pn[i,3,1]=y2,y2
  if i==0:
    dist=(Pn[i,:,0])**2+(Pn[i,:,1])**2
    idx=np.where(dist==np.min(dist))
    dx,dy=-Pn[i,idx[0],0],-Pn[i,idx[0],1]
Pn[:,:,0]=Pn[:,:,0]+dx
Pn[:,:,1]=Pn[:,:,1]+dy

#for whole Taiwan, Xcent,Ycent must be center of island
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
nc = netCDF4.Dataset(geo_name, 'r')
v='HGT_M'
c=np.array(nc.variables[v][0,:,:])
for v in ['CLAT','CLONG']:
    exec(v+'=nc.variables[v][0,:,:]')
xg,yg=pnyc(CLONG,CLAT, inverse=False)
xg+=Xcent
yg+=Ycent
base=[]
for ii in range(nplgs):
  i=ii*4
  d=(xg-P[i][0])*(xg-P[i][0])+(yg-P[i][1])*(yg-P[i][1])
  idx=np.where(d==np.min(d))
  base.append(c[idx[0][0],idx[1][0]])
x,y=pnyc(lonp,latp, inverse=False)
x+=Xcent
y+=Ycent
P=[(i,j) for i,j in zip(x,y)]
Pp=[rotate_about_a_point(pnt,orig,angl) for pnt in P]
Pp=np.array(Pp).flatten().reshape(npnts,2)
Pp[:,0]+=-orig[0] #-mnx
Pp[:,1]+=-orig[1] #-mny

#the stack heights are read from TEDS database IF that hgts are not contained in the name strings
df=read_csv(tedsp_name)
df.UTM_E+=Xcent
df.UTM_N+=Ycent
a=[]
for ll in range(1,6):
  L=ll*1000
  a=df.loc[df.UTM_E.map(lambda s:abs(s-P[0][0])<L) & df.UTM_N.map(lambda s:abs(s-P[0][1])<L)]
  if len(a)>0:
    df=a
    break
if len(a)==0:
  print ('the point source seems not existing in database. </body></html>')
#  sys.exit('fail')
cole=['CO_EMI', 'NMHC_EMI', 'NOX_EMI', 'PM25_EMI', 'PM_EMI', 'SOX_EMI']
c2m={'SOX':64,'NOX':46,'CO':28,'PM25':24.5,'PM':24.5,'NMHC':12*4+10}
unit={i:'ppb' for i in c2m if 'PM' not in i}
unit.update({i:'ug/m3' for i in c2m if 'PM' in i})
hdtv=[ 'HEI', 'DIA', 'TEMP', 'VEL']
tims=[ 'DY1', 'HD1', 'HY1']
for v in cole+hdtv+tims:
  exec(v+'=[]')
for k in range(npnts):
  df['dist']=[np.sqrt((i-P[k][0])**2+(j-P[k][1])**2) for i,j in zip(list(df.UTM_E),list(df.UTM_N))]
  idx=df.loc[df.dist==min(df.dist)].index
  if len(idx)>1:
    idx=df.loc[idx].sort_values('HEI',ascending=False).head(1).index
  for v in cole+hdtv+tims:
    exec(v+'.append(list(df.'+v+'[idx])[0])')
  if len(hgts)<nplgs+npnts:
    hgts.append(list(df.HEI[idx])[0])
for v in cole:
  exec(v+'=['+v+'[i]/HY1[i]/3.6*1000. for i in range(npnts)]')
TEMP=[i+273 for i in TEMP]


for i in range(npnts):
  d=(xg-P[i][0])*(xg-P[i][0])+(yg-P[i][1])*(yg-P[i][1])
  idx=np.where(d==np.min(d))
  base.append(c[idx[0][0],idx[1][0]])

with open(pth+'fort.10','w') as f:
  f.write(("'BPIP input file with "+'{:2d}'+' bldg and '+'{:2d}'+" stacks,originated at [{:.1f},{:.1f}](TWD97m).'\n")
  .format(nplgs,npnts,orig[0],orig[1]))
  f.write(("'P'\n"+"'METERS' 1.00\n'UTMN',"+'{:5.0f}\n').format(angl))
  f.write(('{:2d}\n').format(nplgs))
  for i in range(nplgs):
    f.write(("'"+names[i]+"' 1"+'{:6.1f}\n').format(base[i]))
    f.write(('4 '+'{:5.0f}\n').format(hgts[i]))
    for j in range(4):
      f.write(('{:5.1f}  {:5.1f}\n').format(Pn[i,j,0],Pn[i,j,1]))
  f.write(('{:2d}\n').format(npnts))
  for i in range(npnts):
    ii=i+nplgs
    f.write(("'"+names[ii]+"' "+'{:6.1f} {:6.1f} {:6.1f} {:6.1f} \n').format(base[ii],hgts[ii],Pp[i,0],Pp[i,1]))
s=''
for ii in range(nplgs,nplms):
  s+=names[ii]
case=s[:8]
cmd='cd '+pth+';cp fort.10 '+case+'_bpip.inp'
os.system(cmd)
fnames=['fort.10',case+'_bpip.inp']
# <a data-auto-download href="%s" target="_blank">%s</a></br>
for fn in fnames:
  fname=pth+fn
  print ("""\
  <a href="%s" target="_blank">%s</a></br>
  """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1]))
message='OK!'
print (message+'</body></html>')
sys.exit()
