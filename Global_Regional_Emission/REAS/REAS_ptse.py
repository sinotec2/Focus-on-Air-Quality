#$ cat /nas1/camxruns/2016_v7/ptse/pt_REAS.py
import numpy as np
import netCDF4
import PseudoNetCDF as pnc
import os,sys,twd97,json
from pyproj import Proj
import subprocess
from pandas import *
from calendar import monthrange

mon=int(sys.argv[1]) #argv[1] in 2 digits

pth='/nas1/cmaqruns/2016base/data/ptse'
fnames=subprocess.check_output('ls '+pth+'/point_*csv|grep -v reas|grep -v all',shell=True).decode('utf8').strip('\n').split()
#prepare interceptions
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
XCELL=81000.000
XORIG=-2389500.

dfa=DataFrame({})
for fn in fnames:
  spec=fn.split('/')[-1].replace('point_','').replace('.csv','').replace('./','')
  df=read_csv(fn)
  #interceptions
  lat,lon=(list(df.lat),list(df.lon))
  x,y=pnyc(lon, lat, inverse=False)
  df['x_m'],df['y_m']=(x,y)
  boo=(df['x_m']>=XORIG) & (df['x_m']<=-XORIG) & (df['y_m']>=XORIG) & (df['y_m']<=-XORIG)
  df=df.loc[boo].reset_index(drop=True)
  #reduction
  df.lat=[round(i,1) for i in df.lat]
  df.lon=[round(i,1) for i in df.lon]
  c=df.iloc[:,[0,1,mon+1]]
  c.columns=['lon','lat',spec]
  c=pivot_table(c,index=['lon','lat'],values=spec,aggfunc=sum).reset_index()
  if fn==fnames[0]:
    dfa=c
  else:
    dfa=merge(dfa,c,on=['lon','lat'],how='outer')
df=dfa.fillna(0)
fac=1000.*1000./monthrange(2015,mon)[1]/24. #T/month to gmole/hr
mws={'BC':1,'BENZENE':78.11,'BUTANES':58.12,'CO':28, 'CO2':44, 'ETHANE':30.07,
       'FORMALDEHYDE':30.031, 'INTERNAL_ALKENES':28.05, 'KETONES':86.13, 'NH3':17, 'NOX':46, 'OC':1,
       'OTHER_ALKANES':58.12, 'OTHER_AROMATICS':106.16, 'PENTANES':72.15, 'PM10':1, 'PM25':1,
       'PROPANE':44.1 , 'SO2':64, 'TERMINAL_ALKENES':28.05, 'TOLUENE':92.14, 'TOTAL_NMV':58.12,
       'XYLENES':106.16}

#units of gmole/hr or gram/hr
for c in [ i for i in df.columns if i not in ['lon','lat']]:
  if c not in mws:continue
  df[c]=np.array(df[c])*fac/mws[c]
lat,lon=(list(df.lat),list(df.lon))
x,y=pnyc(lon, lat, inverse=False)
df['x_m'],df['y_m']=(x,y)
df['IX']=(df.x_m-XORIG)//XCELL
df['IY']=(df.y_m-XORIG)//XCELL
idx=df.loc[((df.IX-27)*(df.IX-28)*(df.IX-29)==0)&(df.IY==40)].index
df=df.drop(idx)
nopts=len(df)
specs=[ i for i in df.columns if i not in ['lon','lat','x_m','y_m']]
with open('reas2cmaq.json','r') as f:
  r2c=json.load(f)


fname1='fortBE.14.teds10.base'+sys.argv[1]
fname2='fortBE.14.REAS3.base'+sys.argv[1]+'.nc'
if not os.path.isfile(fname1):sys.exit('file not found')
pt0=pnc.pncopen(fname1,format='point_source')
pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
opts=' -O -f point_source -s NSTK,0,'+str(nopts)+' --out-format=NETCDF4 '
os.system(pncg+opts+fname1+' '+fname2+'>&/dev/null')
#diff=os.system('diff '+fname1+' '+fname2+'>&/dev/null')
#if diff !=0:
#  os.system('cp '+fname1+' '+fname2)
pt=netCDF4.Dataset(fname2,'r+')
V=[list(filter(lambda x:pt.variables[x].ndim==j, [i for i in pt.variables])) for j in [1,2,3,4]]
#store the end_date and end_time, because save() procedure will drop them.
sdate=np.array(pt0.SDATE)[0]
stime=np.array(pt0.STIME)[0]
edate=np.array(pt0.EDATE)[0]
etime=np.array(pt0.ETIME)[0]
#v1:XYHDTVN
#v2 are the emission variables
#v3 are the time flag's
v1,v2,v3=(V[i] for i in range(3))
nhr,nvar,dt=pt.variables[v3[0]].shape
nt,nopts=pt.variables[v2[0]].shape
hdtv='h d t v'.split()
parm=[250.,11.,363.,19.8*3600.]
p_h={i:j for i,j in zip(hdtv,parm)}
for i in hdtv:
  df[i]=[p_h[i] for j in range(nopts)]
v1_REAS=[df.x_m, df.y_m, df.h, df.d, df.t, df.v, df.index]
for i in range(6):
  pt.variables[v1[i]][:]=list(v1_REAS[i])
#v2 filling
for s in set(v2):
  pt.variables[s][:]=0.
flow=(3.14*parm[1]**2/4.)*parm[3]
pt.variables['FLOW'][:,0]=[flow for i in range(nt)]
pt.variables['PLMHT'][:,0]=[parm[0]*2 for i in range(nt)]

for v in specs:
  if v == 'NOX':
    for t in range(nt):
      pt.variables['NO'][t,:]=np.array(df[v])*0.9
      pt.variables['NO2'][t,:]=np.array(df[v])*0.1
    continue
  if sum(np.array(df[v]))==0.:continue
  if v not in r2c :continue
  if type(r2c[v])==str: #simple mapping of specs
    if r2c[v] not in v2:continue
    for t in range(nt):
      pt.variables[r2c[v]][t,:]=np.array(df[v])
  else:         #in case CBM's, type(r2c[v]) is a list
    for i in r2c[v]:
      for t in range(nt):
        pt.variables[i][t,:]+=np.array(df[v])
#pt.NOTE='PTSRCE'+' '*54
pt.SDATE=sdate
pt.STIME=stime
pt.EDATE=edate
pt.ETIME=etime
pt.NOTE=' '*60
pt.NAME='PTSOURCE  '
pt.close()
fname3=fname2.replace('.nc','YP3')
os.system(pncg+' -O --out-format=point_source '+fname2+' '+fname3+'>&/dev/null')
