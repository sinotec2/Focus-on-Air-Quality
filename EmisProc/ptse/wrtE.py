'''
Purpose: Generate CAMx Elev. PtSe. NC file from dfMM.fth (MM=01~12)
Usage: python wrtE.py YYMM
see descriptions at https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/wrtE/
'''
#! crding = utf8
from pandas import *
import numpy as np
import os, sys, subprocess
import netCDF4
import datetime
from calendar import monthrange

from ioapi_dates import dt2jul
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def str2lst(A):
    return [bytes(i,encoding='utf-8') for i in A[1:-1].replace("b'","").replace("'","").replace(" ","").split(',')][:8]


#Main
#locate the programs and root directory
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
P='./'

#time and space initiates
ym=sys.argv[1]
mm=ym[2:4]
mo=int(mm)
yr=2000+int(ym[:2])
ntm=(monthrange(yr,mo)[1]+2)*24+1
bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
edate=bdate+datetime.timedelta(days=ntm/24)#monthrange(yr,mo)[1]+3)
#prepare the uamiv template
print('template applied')
NCfname='fortBE.413_teds10.ptsE'+mm+'.nc'
try:
  nc = netCDF4.Dataset(NCfname, 'r+')
except:
  os.system('cp '+P+'template_v7.nc '+NCfname)
  nc = netCDF4.Dataset(NCfname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nv,dt=nc.variables[V[2][0]].shape
nv=len([i for i in V[1] if i !='CP_NO'])
nc.SDATE,nc.STIME=dt2jul(bdate)
nc.EDATE,nc.ETIME=dt2jul(edate)
nc.NOTE='Point Emission'
nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
nc.NVARS=nv
#Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
nc.name='PTSOURCE  '
nc.NSTEPS=ntm
if 'ETFLAG' not in V[2]:
  zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
if nt!=ntm or (nc.variables['TFLAG'][0,0,0]!=nc.SDATE and nc.variables['TFLAG'][0,0,1]!=nc.STIME):
  for t in range(ntm):
    sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
    nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
    nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
for c in V[1]:
  nc.variables[c].set_auto_mask(False)
  if c=='CP_NO': continue
  nc.variables[c][:]=0.
nc.close()
#template OK

df=read_feather('df'+mm+'.fth')
pv=read_csv('pv'+mm+'.csv')
pv.CP_NOb=[str2lst(i) for i in pv.CP_NOb]
nopts=len(pv)
#item sets definitions
XYHDTV=['UTM_E','UTM_N','HEI','DIA','TEMP','VEL','ORI_QU1']

#determination of camx version
ver=7
if 'XSTK' in V[0]:ver=6
col_mn=['ORI_QU1','TEMP','VEL','UTM_E', 'UTM_N','HY1','HD1','DY1']
lspec=[i for i in df.columns if i not in col_mn+['index','C_NO']]

dimn={6:'NSTK',7:'COL'}
print(dimn[ver]+' expanding and reopening')
res=os.system(ncks+' -O --mk_rec_dmn '+dimn[ver]+' '+NCfname+' tmp'+mm)
if res!=0: sys.exit(ncks+' fail')
res=os.system('mv tmp'+mm+' '+NCfname)
if res!=0: sys.exit('mv fail')
#CP_NO in S1(byte) format
print('ncfile Enlargement')
#prepare the parameter dicts
PRM='XYHDTV'
v2n={PRM[i]:XYHDTV[i] for i in range(6)}
names={7:['xcoord','ycoord','stkheight','stkdiam','stktemp','stkspeed'],
       6:[v+'STK' for v in PRM]}
v2c={PRM[i]:names[ver][i] for i in range(6)}
a=DataFrame({'SN':df.SO2+df.NO2})
a=a.sort_values('SN',ascending=False)
pig=[]#a.index[:100]
#filling the stack parameters for camx700nc

nc = netCDF4.Dataset(NCfname, 'r+')
#enlarge the record dimension (COL)
z=np.zeros(shape=ntm)
for c in V[1]:
  nc.variables[c].set_auto_mask(False)    
  if c in ['CP_NO']:continue   
  for i in range(nopts):
    nc.variables[c][:ntm,i]=z
if ver==7:nc.variables['pigflag'][:nopts]=0
nc.close()
#res=os.system(ncks+' -O --mk_rec_dmn TSTEP '+NCfname+' tmp'+mm)
#if res!=0: sys.exit(ncks+' fail')
#res=os.system('mv tmp'+mm+' '+NCfname)
#if res!=0: sys.exit('mv fail')

nc = netCDF4.Dataset(NCfname, 'r+')
for v in PRM:
  var=v2c[v]
  nc.variables[var].set_auto_mask(False)    
  nc.variables[var][:nopts]=np.array(pv[v2n[v]])
nc.variables[v2c['V']][:nopts]=nc.variables[v2c['V']][:]*3600.
nc.variables[v2c['T']][:nopts]=nc.variables[v2c['T']][:]+273.
#first 100 for PiG
if len(pig)>0:
  if ver==7:
    nc.variables['pigflag'][pig]=1
  else:
    nc.variables[v2c['D']][pig]=nc.variables[v2c['D']][pig]*-1.
for c in V[1]:
  if c not in lspec:continue
  if c not in df.columns:continue
  if c in ['CP_NO']: continue
  ic=lspec.index(c)
  nc.variables[c][:,:nopts]=np.array(df[c]).reshape(ntm,nopts)
  print(c)
nc.variables['CP_NO'][:nopts,:8]=np.array(list(pv.CP_NOb)).flatten().reshape(nopts,8)
nox=nc.variables['NO2'][:,:nopts]
nc.variables['NO'][:,:nopts]=nox[:,:nopts]*0.9
nc.variables['NO2'][:,:nopts]=nox-nc.variables['NO'][:,:nopts]
nc.NOPTS=nopts
nc.close()

