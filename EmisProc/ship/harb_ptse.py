

#! crding = utf8
from pandas import *
import numpy as np
import os, sys, subprocess
import netCDF4


ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
P='/'+hmp+'/TEDS/teds11/ship/'

IXYfromVerdi=[(26,93),(53,124),(55,124),(66,124),(71,104),(15,75),(63,82),(18,33),(20,31),(15,46)]
HarbName=['TaiZhong','TaiBeiW','TaiBeiE','JiLong','SuAuo','MaiLiao','HuaLian','KS_W','KS_E','AnPin']
IYX=[(j-1,i-1) for (i,j) in IXYfromVerdi]
nhb=len(IYX)

#time and space initiates
ym=sys.argv[1]
mm=sys.argv[1][2:4]
mo=int(mm)
yr=2000+int(sys.argv[1][:2])

fname='fortBE.413_teds10.51A_'+mm+'.nc'
fname1=fname.replace('A_','Ab')
os.system('cp '+fname+' '+fname1)
try:
  nc = netCDF4.Dataset(fname1, 'r+')
except:
  sys.exit(fname1+' not found')

V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
nv=len(V[3])
#store the matrix
var=np.zeros(shape=(nv,nt,nrow,ncol))
for v in V[3]:
  iv=V[3].index(v)
  var[iv,:,:,:]=nc.variables[v][:,0,:,:]
#store the att. and flags
for c in ['X','Y']:
  for d in ['ORIG','CELL']:
    exec(c+d+'=nc.'+c+d)
for c in ['S','E']:
  for d in ['DATE','TIME']:
    exec(c+d+'=nc.'+c+d)
for c in ['TFLAG','ETFLAG']:
  exec(c+'=nc.variables["'+c+'"][:,0,:]')


hb=np.zeros(shape=(nv,nt,nhb))
for yx in IYX:
  ihb=IYX.index(yx)
  neibi=[]
  for j in range(yx[0]-1, yx[0]+2):
    for i in range(yx[1]-1, yx[1]+2):
      if (j,i) in IYX:continue
      neibi.append((j,i))
  nnb=len(neibi)
  b=np.array(neibi).flatten().reshape(nnb,2)
  base=np.mean(var[:,:,b[:,0],b[:,1]],axis=2)
  hb[:,:,ihb]=var[:,:,yx[0],yx[1]]-base[:,:]
#modified the ground level emission
  for v in V[3]:
    iv=V[3].index(v)
    nc.variables[v][:,0,yx[0],yx[1]]=base[iv,:]
nc.close()
idx=np.where(hb<0)
if len(idx[0])>0:sys.exit(' hb<0, redo python csv2uamivNSC.py '+mm+' 51A,51B,51C,51D and check the location of HRBs')
v3=[]
for v in V[3]:
  iv=V[3].index(v)
  if np.sum(hb[iv,:,:])==0:continue
  v3.append(v)
if 'NO2' not in v3:v3.append('NO2')
nv3=len(v3)

#prepare the uamiv template
print('template applied')
NCfname='fortBE.413_teds10.HRBE'+mm+'.nc'
try:
  nc = netCDF4.Dataset(NCfname, 'r+')
except:
  os.system('cp '+P+'template_v7.nc '+NCfname)
  nc = netCDF4.Dataset(NCfname, 'r+')
Vo=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nto,nv,dt=nc.variables['TFLAG'].shape
if len(set(v3)-set(Vo[1])) != 0:sys.exit('some pollutants not in template, must be created')
#restore the attributes
nc.SDATE,nc.STIME=SDATE,STIME
nc.EDATE,nc.ETIME=EDATE,ETIME
nc.NOTE='Point Emission'
nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
#Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
nc.name='PTSOURCE  '
nc.NSTEPS=nt
if 'ETFLAG' not in Vo[2]:
  zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
if nto!=nt:
#must be enlared gradulally in do loop
  for t in range(nt):
    nc.variables['TFLAG'][t,:,0] =[TFLAG[t,0] for i in range(nv)]
    nc.variables['TFLAG'][t,:,1] =[TFLAG[t,1] for i in range(nv)]
    nc.variables['ETFLAG'][t,:,0]=[ETFLAG[t,0] for i in range(nv)]
    nc.variables['ETFLAG'][t,:,1]=[ETFLAG[t,1] for i in range(nv)]
nc.close()
#prepare the template
s=' '
for c in set(Vo[1])-set(v3):
  if c in ['CP_NO','plumerise']:continue
  s+=c+','
if len(s)>1:
  res=os.system(ncks+' -O -x -v'+s.strip(',')+' '+NCfname+' tmp'+mm)
  if res!=0: sys.exit(ncks+' -x var fail')
  ns=str(len(v3))
  res=os.system(ncks+' -O -d VAR,0,'+ns+' tmp'+mm+' '+NCfname)
  if res!=0: sys.exit(ncks+' -d VAR fail')
#determination of camx version
ver=7
if 'XSTK' in Vo[0]:ver=6
dimn={6:'NSTK',7:'COL'}
print(dimn[ver]+' expanding and reopening')
res=os.system(ncks+' -O --mk_rec_dmn '+dimn[ver]+' '+NCfname+' tmp'+mm)
if res!=0: sys.exit(ncks+' fail')
res=os.system('mv tmp'+mm+' '+NCfname)
if res!=0: sys.exit('mv fail')

#CP_NO in S1(byte) format
print('ncfile filling')
#prepare the parameter dicts
PRM='XYHDTV'
names={7:['xcoord','ycoord','stkheight','stkdiam','stktemp','stkspeed'],
       6:[v+'STK' for v in PRM]}
v2c={PRM[i]:names[ver][i] for i in range(6)}

pv=DataFrame({
'xcoord':[(i+0.5)*XCELL+XORIG for (j,i) in IYX],
'ycoord':[(j+0.5)*YCELL+YORIG for (j,i) in IYX],
'stkheight':[75. for i in range(nhb)],
'stktemp'  :[100. for i in range(nhb)],
'stkspeed'  :[10. for i in range(nhb)],
'stkdiam'  :[30. for i in range(nhb)],
})
pv['CP_NOb'] = [[bytes(i,encoding='utf-8') for i in j]+[bytes(' ',encoding='utf-8')]*(8-len(j)) for j in HarbName ]



#filling the stack parameters for camx700nc
nc = netCDF4.Dataset(NCfname, 'r+')
Vo=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nopts=nhb
#enlarge the record dimension (COL)
for c in Vo[1]:
  if c == 'CP_NO':continue
  for i in range(nopts):
    nc.variables[c][0,i]=0.
if ver==7:nc.variables['pigflag'][:nopts]=0
for v in PRM:
  var=v2c[v]
  nc.variables[var][:nopts]=np.array(pv[var])
nc.variables[v2c['V']][:nopts]=nc.variables[v2c['V']][:]*3600.
nc.variables[v2c['T']][:nopts]=nc.variables[v2c['T']][:]+273.
#first 100 for PiG
pig=[]
if len(pig)>0:
  if ver==7:
    nc.variables['pigflag'][pig]=1
  else:
    nc.variables[v2c['D']][pig]=nc.variables[v2c['D']][pig]*-1.
for c in Vo[1]:
  if c not in v3:continue
  ic=V[3].index(c)
  nc.variables[c][:,:nopts]=hb[ic,:,:]
  print(c)
nc.variables['CP_NO'][:nopts,:8]=np.array(list(pv.CP_NOb)).flatten().reshape(nopts,8)
nox=nc.variables['NO2'][:,:nopts]
nc.variables['NO'][:,:nopts]=nox[:,:nopts]*0.9
nc.variables['NO2'][:,:nopts]=nox-nc.variables['NO'][:,:nopts]
nc.NOPTS=nopts
nc.NVARS=len(v3)+1
nc.close()


