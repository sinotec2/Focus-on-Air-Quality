#$ cat /nas1/camxruns/2016_v7/emis/area/mod11.py
import numpy as np
import netCDF4
import os, sys, subprocess

hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
P='/'+hmp+'/TEDS/teds10_camx/HourlyWeighted/'
fname='/'+hmp+'/cmaqruns/2016base/data/land/epic_festc1.4_20180516/gridmask/AQFZones_EAsia_81K.nc'
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
#AQFZ0~7 0:sea_other_country/1:jinjinji/2:huabei/3:dongbei/4:xibei/5:huanan_taiwan/6:xinan/7:huadong
AQFZ={'SOC':0,'JJZ':1,'HB':2,'DB':3,'XB':4,'HN':5,'XN':6,'HD':7}
ic=0
dsgn=['JJZ']
R_dsgn={'JJZ':0.5}
zone=['AQFZ'+str(AQFZ[i]) for i in dsgn]
nv=len(zone)
izone=[V[3].index(v) for v in zone]
cnty_frac=np.zeros(shape=(nv,nrow,ncol))
cnty_frac[ic,:,:]=nc.variables[zone[ic]][0,0,:,:]
for c in ['X','Y']:
  for d in ['ORIG','CELL']:
    exec(c+d+'=nc.'+c+d)
nc.close()

fname=sys.argv[1]
fnameO=fname+'_'+dsgn[ic]
os.system('cp '+fname+' '+fnameO)
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
#ptse file
if len(V[3])==0 and len(V[1])>2:
  nt,nopts=(nc.variables[V[1][0]].shape[i] for i in range(2))
#determine which stacks remain in the domain
  IX=[int((x-XORIG)/XCELL) for x in nc.variables['xcoord'][:]]
  IY=[int((y-YORIG)/YCELL) for y in nc.variables['ycoord'][:]]
  cnty_frac1=np.zeros(shape=(nopts,nv))
  for i in range(nopts):
    if IY[i]*(IY[i]-nrow)<=0 and IX[i]*(IX[i]-ncol)<=0:
      cnty_frac1[i,:]=cnty_frac[:,IY[i],IX[i]]
  nv1=len(V[1])
  var=np.zeros(shape=(nv1,nt,nopts))
  v0=['CP_NO','plumerise']
#store the variable matrix
  for v in V[1]:
    if v in v0:continue
    iv=V[1].index(v)
    var[iv,:,:]=nc.variables[v][:,:]
    if np.sum(var[iv,:,:])==0:v0.append(v)
  nc.close()
  nc = netCDF4.Dataset(fnameO, 'r+')
  for v in V[1]:
    if v in v0:continue
    iv=V[1].index(v)
    nc.variables[v][:,:]=var[iv,:,:]*(1-cnty_frac1[:,ic]*R_dsgn[dsgn[ic]])
  nc.close()
#area files
else:
  nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
  nv=len(V[3])
  var=np.zeros(shape=(nv,nt,nrow,ncol))
  v0=[]
  for v in V[3]:
    iv=V[3].index(v)
    var[iv,:,:,:]=nc.variables[v][:,0,:,:]
    if np.sum(var[iv,:,:,:])==0:v0.append(v)
  nc.close()
  nc = netCDF4.Dataset(fnameO, 'r+')
  cf=1-cnty_frac[ic,:,:]*R_dsgn[dsgn[ic]]
  for v in V[3]:
    if v in v0:continue
    iv=V[3].index(v)
    nc.variables[v][:,0,:,:]=var[iv,:,:,:]*cf
  nc.close()
