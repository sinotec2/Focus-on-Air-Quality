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

from terrainXYINC import terrainXYINC
from rd_kmlLL import rd_kmlLL

#rotate the matrix with respect to certain point
def rotate_about_a_point(target_point,center_point,angle_rs):
  cp=np.subtract(target_point,center_point)
  px=cp[0]*math.cos(math.radians(angle_rs))+cp[1]*-math.sin(math.radians(angle_rs))
  py=cp[0]*math.sin(math.radians(angle_rs))+cp[1]*math.cos(math.radians(angle_rs))
  return(np.add([px,py],center_point))

#paths
AERMOD='/Users/1.PlumeModels/AERMOD/aermod_source/aermod.exe'
BPIP='/Users/1.PlumeModels/ISC/BPIPPRM/bpipprm'
CGI='/Library/WebServer/CGI-Executables/isc/'
CHK='/opt/local/bin/chk_aermod.cs'
GEO='/Users/WRF4.1/WPS/geo_em.d04_333m.nc'
GREP='/usr/bin/grep --color=never '
MAIL='/usr/bin/mail'
MMIF='/opt/local/bin/mmif'
NULL=' >&/dev/null'
SED='/usr/bin/sed -ie'
WAIT='/opt/local/bin/wait_mmif4aermod.cs'
WAITM='/opt/local/bin/wait_map4aermod.cs'
WC='|/usr/bin/wc -l'
WEB='/Library/WebServer/Documents/'
ZIP='/usr/bin/zip'
CPU="ps -A -o %cpu | awk '{s+=$1} END {print s}'"

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth=WEB+'isc_results/aerm_'+ran+'/'
tedsp_name=WEB+'isc_results/point_QC.csv'
os.system('mkdir -p '+pth)
OUT=' >> '+pth+'isc.out'

print ('Content-Type: text/html\n\n')
with open(CGI+'header.txt','r') as f:
  lines=[i.strip('\n').strip('\r') for i in f]
  for l in lines:
    print (l)
cpu=subprocess.check_output(CPU,shell=True).decode('utf8').strip('\n')
print ('<br>cpu='+cpu+'</br>')
if float(cpu)>500:
  sys.exit()
  print ('</body></html>')
  sys.stdout.close()
  sys.exit('fine!')

form = cgi.FieldStorage()
try:
  fileitem = form['filename']
except:
  print ('<p>filename not given or not right!</p>')
  print ('</body></html>')
  sys.exit()
year = form['year'].value
yy=year[2:]
year=int(year)
emailadd = '' #form.getvalue('emailadd')

fn = os.path.basename(fileitem.filename)
open(pth+fn, 'wb').write(fileitem.file.read())

kml_file = os.path.join(pth+fn)

nplgs,npnts,names,hgts,lon,lat,lonp,latp=rd_kmlLL(kml_file)
nplms=nplgs+npnts
print ('<p>filename given (and save as):'+pth+fn+'</br></p>')

#Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
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
  print ('<p>wrong direction or skewed!</br></p>')
  for i in range(nplgs):
    print (('<p>dir for building# {:d} is: {:f} {:f} {:f} {:f}</br></p>').format(i,*dir[i,:]))
  print ('</body></html>')
  sys.exit('wrong direction or skewed!')

P=[(i,j) for i,j in zip(x[:,:4].flatten(),y[:,:4].flatten())]
angl= min([np.mean(dir[:,j]) for j in range(4)])
if angl<0:angl+=360.
orig=P[0]
Pn=[rotate_about_a_point(pnt,orig,angl) for pnt in P]
Pn=np.array(Pn).flatten().reshape(nplgs,4,2)
mnx, mny=(np.min(Pn[:,:,i]) for i in range(2))
Pn[:,:,0]+=-orig[0] #-mnx
Pn[:,:,1]+=-orig[1] #-mny

for i in range(nplgs):
  x1=sum([Pn[i,j,0] for j in range(4) if Pn[i,j,0] < np.mean(Pn[i,:,0])])/2
  x2=sum([Pn[i,j,0] for j in range(4) if Pn[i,j,0] > np.mean(Pn[i,:,0])])/2
  y1=sum([Pn[i,j,1] for j in range(4) if Pn[i,j,1] < np.mean(Pn[i,:,1])])/2
  y2=sum([Pn[i,j,1] for j in range(4) if Pn[i,j,1] > np.mean(Pn[i,:,1])])/2
  if i==0:
    dx,dy=Pn[i,0,0]-x1,Pn[i,0,1]-y1
  Pn[i,0,0],Pn[i,1,0]=x1,x1
  Pn[i,2,0],Pn[i,3,0]=x2,x2
  Pn[i,0,1],Pn[i,3,1]=y1,y1
  Pn[i,1,1],Pn[i,2,1]=y2,y2
Pn[:,:,0]=Pn[:,:,0]+dx
Pn[:,:,1]=Pn[:,:,1]+dy

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
nc = netCDF4.Dataset(GEO, 'r')
v='HGT_M'
elv=np.array(nc.variables[v][0,:,:])
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
  base.append(elv[idx[0][0],idx[1][0]])

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
a=[]
for ll in range(1,6):
  L=ll*0.01 # 1deg~100Km
  a=df.loc[df.LON.map(lambda s:abs(s-lonp[0])<L) & df.LAT.map(lambda s:abs(s-latp[0])<L)]
  if len(a)>0:
    df=a
    break	
if len(a)==0:
  print ('<p>the point source seems not existing in database.</p> </body></html>')
  sys.exit('fail')
cole=['CO_EMI', 'NMHC_EMI', 'NOX_EMI', 'PM25_EMI', 'PM_EMI', 'SOX_EMI']
c2m={'SOX':64,'NOX':46,'CO':28,'PM25':24.5,'PM':24.5,'NMHC':12*4+10}
unit={i:'ppb' for i in c2m if 'PM' not in i}
unit.update({i:'ug/m3' for i in c2m if 'PM' in i})
hdtv=[ 'HEI', 'DIA', 'TEMP', 'VEL']
tims=[ 'DY1', 'HD1', 'HY1']
for v in cole+hdtv+tims:
  exec(v+'=[]')
for k in range(npnts):
  if len(hgts)==nplgs+npnts:
    hstk=hgts[nplgs+k]
    df['dist']=[np.sqrt((i-lonp[k])**2+(j-latp[k])**2+(h-hstk)**2) for i,j,h in zip(list(df.LON),list(df.LAT),list(df.HEI))] 
  else: 
    df['dist']=[np.sqrt((i-lonp[k])**2+(j-latp[k])**2) for i,j in zip(list(df.LON),list(df.LAT))] 
  idx=df.loc[df.dist==min(df.dist)].index
  #find the tallest stack
  print (df.dist,min(df.dist),idx)
  if len(idx)>1:
    idx=df.loc[idx].sort_values('HEI',ascending=False).head(1).index
  for v in hdtv+tims:
    exec(v+'.append(list(df.'+v+'[idx])[0])')
  if len(hgts)<nplgs+npnts:
    hgts.append(list(df.HEI[idx])[0])
  if npnts>1:
    for v in cole:
      exec(v+'.append(list(df.'+v+'[idx])[0])')
  else:
    df['C_NO']=[i[:8] for i in df.CP_NO]
    C_NO=df.C_NO[idx[0]]
    a=df.loc[df.C_NO==C_NO]
    for v in cole:
      exec(v+'.append(sum(list(a.'+v+')))')
  df=df.drop(idx)
for v in cole:
  exec(v+'=['+v+'[i]/HY1[i]/3.6*1000. for i in range(npnts)]') #TPY to GPS
TEMP=[i+273 for i in TEMP]


for i in range(npnts):
  d=(xg-P[i][0])*(xg-P[i][0])+(yg-P[i][1])*(yg-P[i][1])
  idx=np.where(d==np.min(d))
  base.append(elv[idx[0][0],idx[1][0]])

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
#collecting the case name
s=''
for ii in range(nplgs,nplms):
  s+=names[ii]
case=s[:8]  
if npnts==1 and len(names[-1])>len(case):
  names[-1]=case

#excution of BPIP and read the result lines
cmd ='cd '+pth+';'
cmd+= BPIP+NULL+';' 
cmd+= GREP+" ' SO ' fort.12 >build.txt"
os.system(cmd)
with open(pth+'build.txt','r') as f:
  ln=[l.strip('\n') for l in f]
idx=ln[0].index('SO')
ln=[i[idx:] for i in ln]

with open(pth+'example2.csv','w') as f:
  for i in range(nplgs):
    for j in range(4):
      f.write('{:10f},{:10f}\n'.format(Pn[i,j,0],Pn[i,j,1]))
  for i in range(npnts):
    f.write('{:10f},{:10f}\n'.format(Pp[i,0],Pp[i,1]))

fnames={'BPIP_i':[fn,'fort.10']}
fnames.update({'BPIP_o':['build.txt','example2.csv','fort.12','fort.14']})


dx=max(10,round(min([250,max(HEI)]),-1)*2)
x0n,y0n=(round(P[0][i]-dx*40/2, -2) for i in range(2))
x0x,y0x=(round(P[0][i]+dx*40/2, -2) for i in range(2))

#FLAT or COMPLEX TERRAIN
boo=(x0n<=xg) & (xg<=x0x) & (y0n<=yg) & (yg<=y0x)
idx=np.where(boo)
maxBase=np.max(elv[idx[0],idx[1]]) 
run_aermap=False
RECroot=''
nx=40
if maxBase <= np.max(HEI):
  FLAT,terropt=True,'FLAT'
  dx1=2000
  x1n,y1n=(int(round(P[0][i]-dx1*40/4, -2)) for i in range(2))
  x1x,y1x=(int(round(P[0][i]+dx1*40/4, -2)) for i in range(2))
  inp_txt=str(x1n)+'_40_'+str(dx1)+'_'+str(y1n)+'_40_'+str(dx1)
else:
  FLAT,terropt=False, 'ELEV'
  WEBterr=WEB+'terr_results/'
  dft=read_csv(WEBterr+'TWN_1X1REC.csv')
  dfi=read_csv(WEBterr+'point_ij.csv')
  IJ1=(int((P[0][0]-Xcent)/1000)+int((83*3/2)))*1000+(int((P[0][1]-Ycent)/1000)+int(137*3/2))
  if IJ1 in list(dft.centIJ):
    RECroot=list(dft.loc[dft.centIJ==IJ1,'path'])[0]
  elif IJ1 in list(dfi.IJ):
    RECroot=list(dfi.loc[dfi.IJ==IJ1,'CP_NO'])[0]
  if len(RECroot)>0:
    inp_txt=list(dft.loc[dft.path==RECroot,'inp'])[0]
    rec_txt= 'RE GRIDCART '+RECroot+' XYINC '+inp_txt.replace('_',' ')
    x0n,nx,dx,y0n,ny,dy=(int(i) for i in inp_txt.split('_'))
    for ext in ['.REC','.inp','.out|grep -v isc.out','.kml','.dem']:
      os.system('cp '+WEBterr+inp_txt+'/*'+ext+' '+pth)
  else:
    HEI3=min(np.max(HEI)*3,maxBase)
    if HEI3>=maxBase:
      dx=(x0x-x0n)/40.
    else:
      boo=(HEI3<=elv) & (elv<=maxBase)
      idx=np.where(boo)
      dist=[np.sqrt((xg[i,j]-P[0][0])**2+(yg[i,j]-P[0][1])**2) for i,j in zip(idx[0],idx[1])]
      dx=min(dist)*4/40. 	
      x0n,y0n=(round(P[0][i]-dx*25, -2) for i in range(2))
      x0x,y0x=(round(P[0][i]+dx*25, -2) for i in range(2))
      inp_txt=('{:8.0f} 40 {:4.0f} {:10.0f} 40 {:4.0f}').format(x0n,dx,y0n,dx)
      rec_txt= 'RE GRIDCART '+case+' XYINC '+inp_txt
      RECroot=terrainXYINC(pth,rec_txt)
  REC=pth+RECroot+'.REC'
  if len(REC)>0:
    with open(REC,'r') as f:
      ll=[l.strip('\n') for l in f]
  if (len(REC)>0 and rec_txt not in ll[:]) or len(REC)==0 or not os.path.exists(REC): 
    print ('<p>AERMAP must be excuted !</br></p>')
    message='<p>terr was submitted! '+cmd
    print (message+'</br></p>')
    run_aermap=True
  fnames.update({'AERMAP_i':['aermap.inp',RECroot+'.dem'],'AERMAP_o':['aermap.out',RECroot+'.REC']})
inps,specs=[],[]
temis=0
for c in cole:
  exec('temis+=sum('+c+')')
if temis<=0.01:
  if len(RECroot)>0:case=RECroot
  print ('total emis too small, temis='+str(temis)+' for point='+case)
  print ('</body></html>')
#  sys.exit('temis='+str(temis))
for c in cole:
  sp=c.replace('_EMI','')
  sp0=sp.replace('X','2')
  if sp0=='PM25':sp0='OTHER'
  cnvt=24.5/c2m[sp]*1E6
  exec('e='+c)
  if sum(e)<=0.01:continue
  inp=case+'_'+sp+'.inp'
  fnames.update({'AERMOD_'+sp+'_i':[inp]})
  inps.append(inp)
  specs.append(sp)
  with open(pth+inp,'w') as f:
    f.write(   'CO STARTING\n')
    f.write(   '   TITLEONE  A Simple Example Problem for the AERMOD Model with PRIME\n')
    f.write(  ('   MODELOPT  DFAULT CONC  {:s}\n').format(terropt))
    f.write(   '   AVERTIME  1  3  8  24  PERIOD\n')
    f.write(   '   POLLUTID  '+sp0+'\n')
    f.write(   '   RUNORNOT  RUN\n')
    f.write(   '   EVENTFIL  aertest_evt.inp\n')
    f.write(   '   ERRORFIL  ERRORS_'+sp+'.OUT\n')
    f.write(   'CO FINISHED\n')
    f.write(   'SO STARTING\n')
    f.write(   '   ELEVUNIT METERS\n')
    for i in range(npnts):
      ii=i+nplgs
      f.write(('   LOCATION '+names[ii]+' POINT {:10.2f} {:10.2f} {:6.1f}\n').format(P[i][0],P[i][1],base[ii]))
    for i in range(npnts):
      ii=i+nplgs
      f.write(('   SRCPARAM '+names[ii]+' {:10.2f} {:6.1f} {:6.1f} {:6.1f} {:6.1f}\n').format(e[i],HEI[i],TEMP[i],VEL[i],DIA[i]))
    for l in ln:
      f.write(l+'\n')
    f.write(  ('SO EMISUNIT {:10.3f} (GRAMS/SEC) '+unit[sp]+'\n').format(cnvt)) 
    f.write(   'SO SRCGROUP  ALL\n')
    f.write(   'SO FINISHED\n') 
    f.write(   'RE STARTING\n')
    if FLAT:	
      f.write( '   GRIDCART gd2 STA\n')
      f.write(('   GRIDCART gd2 XYINC {:8.0f} 25 {:4.0f} {:10.0f} 25 {:4.0f}\n').format(x1n,dx1,y1n,dx1))
      f.write( '   GRIDCART gd2 END\n')
    else:
      f.write(('RE INCLUDED {:s}.REC\n').format(RECroot))
    f.write(   'RE FINISHED\n')
    f.write(   'ME STARTING\n')
    f.write(   'ME SURFFILE '+case+'.sfc\n')
    f.write(   'ME SURFDATA   99999 20'+yy+'\n')
    f.write(   'ME PROFFILE '+case+'.pfl\n')
    f.write(   'ME PROFBASE   34 METERS\n')
    f.write(   'ME UAIRDATA   99999 20'+yy+'\n')
    f.write(   'ME FINISHED\n')
    f.write(   'OU STARTING\n')
    f.write(   '   RECTABLE  ALLAVE  FIRST-THIRD\n')
    f.write(   '   MAXTABLE  ALLAVE  50\n')
    f.write(   '   SUMMFILE  AER_'+sp+'.SUM\n')
    f.write(   '   PLOTFILE  1  ALL  FIRST  AER_'+sp+'_01H.PLT\n')
    f.write(   '   PLOTFILE  PERIOD    ALL  AER_'+sp+'_Y.PLT\n')
    if sp0=='NO2':	
      f.write( '   POSTFILE  1  ALL  PLOT   AER_'+sp+'_01H.PST\n')
    f.write(   'OU FINISHED\n')
  aero=['AER_'+sp+'.SUM',inp.replace('inp','out')]
  for i in ['_01H.PLT','_Y.PLT']:
    aero.append('AER_'+sp+i)
    for j in ['.kml','.grd']:
      aero.append('AER_'+sp+i+j)
  if sp0=='NO2':	
    aero.append('AER_'+sp+'_01H.PST') 
  fnames.update({'AERMOD_'+sp+'_o':aero})

#generate the mmif.inp file
cmd ='cd '+pth+';'
cmd+='cp ../mmif.inp_blank mmif.inp;'
cmd+=SED+' "s/LATI/{:f}/g" mmif.inp'.format(latp[0])+';'
cmd+=SED+' "s/LONG/{:f}/g" mmif.inp'.format(lonp[0])+';'
cmd+=SED+' "s/xiehe/{:s}/g" mmif.inp'.format(case)
os.system('echo "'+cmd+'"'+OUT)
os.system(cmd)
fnames.update({'MMIF_i':['mmif.inp']})

IJ=(int((orig[0]-Xcent-1500)/3000)+int(83/2))*1000+(int((orig[1]-Ycent-1500)/3000)+int(137/2))
dfname=WEB+'mmif_results/TWN_3X3_mmif.csv'
df=read_csv(dfname)
if IJ in list(df.IJ) and year in set(list(df.YR)):
  boo=(df.IJ==IJ) &(df.YR==year)
  idx=np.where(boo==True)
  if len(idx[0])!=1:
    print ('met data not repared for year='+yy+' and IJ='+str(IJ))
    sys.exit('boo not meet')
  caseold=df.loc[idx[0][0],'FNAME']
#  print 'caseold='+caseold+' '+str(idx[0][0])
  os.system('cp '+caseold+'.sfc '+pth+case+'.sfc')
  os.system('cp '+caseold+'.pfl '+pth+case+'.pfl') 
  run_mmif=False
else:
  cmd ='cd '+pth+';'
  cmd+=MMIF+'>mmif_'+case+'.out &disown'
  os.system(cmd)
  run_mmif=True
  print (" <p>mmif(and aermod subsequently) is running at the background, DO NOT RELOAD this web page, please! </br></p> ")
  dfa=DataFrame({'IJ':[IJ],'FNAME':[WEB+'mmif_results/'+case],'YR':[year]})
  df=df.append(dfa,ignore_index=True)
  df.set_index('IJ').to_csv(dfname)
fnames.update({'MMIF_o':[case+i for i in ['.pfl','.sfc']]+['mmif_'+case+'.out']})
for inp in inps:
  iname=pth+inp
  oname=iname.replace('inp','out')
  if run_mmif==False and run_aermap==False:
    cmd ='cd '+pth+';'
    cmd+= AERMOD+' '+inp+' '+oname+OUT+' & disown;echo $!'
    pid=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n')
    if inp==inps[-1]:
      cmd=CHK+' '+pth+' '+pid+' & disown'
      os.system(cmd)
      
if run_mmif==False:
  m=str(int(nx*nx*25/318/318))
  print (" <p>AERMOD_results: The AERMOD process should be ended in "+m+" min(NOx/OLM will take time) for XYINC "+ \
	inp_txt.replace('_',' ')+"</br></p> ")
  print (" <p>After MMIF being done, You may open the links in new pages:</br></p> ")
  if run_aermap==True:
    cmd ='cd '+pth+';'
    cmd+= WAITM+' '+pth+' '+emailadd+OUT+' &disown'
    os.system(cmd)
else:
  cmd ='cd '+pth+';'
  cmd+=WAIT+' '+pth+' '+emailadd+' &disown'
  os.system(cmd)
  print (" <p>AERMOD_results: The AERMOD process had been sumitted for grdsys:"+inp_txt+"</br></p> ")
  print (" <p>After MMIF being done, You may open the links in new pages:</br></p> ")
fnames.update({'POST_i':[]})
fnames.update({'POST_o':['result.zip','AER_NOX_01H_rep.txt','isc.out']})

#OUTPUT
formats={'grd':'SURFER ascii grd file',
	 'out':'program print_out',
	 'SUM':'AERMOD/ISC summary print_out',
	 'OUT':'AERMOD/ISC error file',
	 'PLT':'AERMOD/ISC plot file in particular average time',
	 'PST':'AERMOD/ISC hourly plot file,(for OLM)',
	'inp':'MMIF/AERMOD/ISC run stream file',
	'sfc':'MMIF surface output file(for AERMOD)',
	'pfl':'MMIF profile output file(for AERMOD)',
	'txt':'SO run stream or OLM report',
	'10':'BPIP input file',
	'12':'BPIP processing information(for AERMOD)',
	'14':'BPIP evaluation output file',
	'csv':'BPIP coordinates output file',
	'dem':'USGS Digital Elevation Models file',
	'REC':'AERMOD receptor include file',
	'kml':'Google Keyhole Markup Language file',
	'zip':'resultant zip file',
}
tools={'grd':'SURFER',
'zip':'archive openner',
'kml':'<a href=\"http://114.32.164.198/LeafletDigitizer/index.html" target="_blank">Digitizer</a>',
'PLT':'text editors, gridded by SURFER or <a href=\"http://114.32.164.198/dat2kml.html" target="_blank">dat2kml</a>',
'PST':'text editors, huge, do not open',
}
tools.update({i:'text editors' for i in [ '10', '12', '14', 'csv', 'out', 'OUT', 'inp', 'dem', 'REC', 'txt', 'pfl', 'sfc', 'SUM'] })
fnameo={}
for prs in fnames:
  fns=[]
  for fn in fnames[prs]:
    fni=(pth+fn).replace(WEB,'../../../')
    fns.append('<a href=\"'+fni+'\" target="_blank">'+fn+'</a>')
#    fns.append('<a data-auto-download href=\"'+fni+'\">'+fn+'</a>')
  fnameo.update({prs:fns})
#fname table in order of process
print ('<table BORDER=2 RULES=ROWS FRAME=BOX width="70%">')
print ('<tr><th>Process</th><th>Filename</th><th>Meanings</th><th>Format/Checker</th></tr>')
IO=['input','output']
for pr in ['BPIP','AERMAP','MMIF',]+['AERMOD_'+s for s in specs]+['POST']:
  if FLAT and pr=='AERMAP':continue
  for io in IO:
    prs=pr+'_'+io[0]
    if len(fnames[prs])==0:continue
    print ('<tr><td width=\"10%\">'+pr+' '+io+'</td><td width=\"15%\">')
    for itm in fnameo[prs]:
      print (itm+'<br>')
    print ('</td><td width="25%">')
    for itm in fnames[prs]:
      ext=itm.split('.')[-1]
      print (formats[ext]+'<br>')
    print ('</td><td width="20%">')
    for itm in fnames[prs]:
      ext=itm.split('.')[-1]
      print (tools[ext]+'<br>')
    print ('</td></tr>')

if len(emailadd)==0 or '@' not in emailadd:
  message='<p>email was not given, please download by yourself after program excutions!</p>'
  print (message+'</body></html>')
  sys.exit('fine')

os.system(CHK+' '+pth+' "'+emailadd+'" & disown')
message='<p>An automated inspection was launched and emails will be sent to '+emailadd+' to inform you of the execution results.</p>'
print (message+'</body></html>')
sys.stdout.close()
sys.exit('fine!')
