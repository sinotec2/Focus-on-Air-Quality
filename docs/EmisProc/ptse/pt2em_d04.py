import netCDF4
import numpy as np
import datetime
import os, sys, subprocess
from pandas import *

ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
ncatted=subprocess.check_output('which ncatted',shell=True).decode('utf8').strip('\n')
MM=sys.argv[1]
fname=MM
#store the point source matrix
nct = netCDF4.Dataset(fname,'r')
Vt=[list(filter(lambda x:nct.variables[x].ndim==j, [i for i in nct.variables])) for j in [1,2,3,4]]
ntt,nvt,dt=nct.variables[Vt[2][0]].shape
try:
  nopts=nct.NOPTS
except:
  nopts=nct.dimensions['COL'].size

TFLAG=nct.variables['TFLAG'][:,0,:]
ETFLAG=nct.variables['ETFLAG'][:,0,:]
SDATE=nct.SDATE
STIME=nct.STIME
Vt1=[i for i in Vt[1] if i not in ['CP_NO','plumerise']]
var=np.zeros(shape=(len(Vt1),ntt,nopts))
for v in Vt1:
  iv=Vt1.index(v)
  var[iv,:,:]=nct.variables[v][:,:]

fname=MM+'_d04.nc'
os.system('cp template_d4.nc '+fname)
nc = netCDF4.Dataset(fname,'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
#determination of camx version and prepare IX/IY
ver=7
if 'XSTK' in Vt[0]:ver=6
X={6:'XSTK',7:'xcoord'}
Y={6:'YSTK',7:'ycoord'}
#store the coordinate system param. for calibration
for c in ['X','Y']:
  for d in ['ORIG','CELL']:
    exec(c+d+'=nc.'+c+d)
IX=np.array([(i-nc.XORIG)/nc.XCELL for i in nct.variables[X[ver]][:nopts]],dtype=int)
IY=np.array([(i-nc.YORIG)/nc.XCELL for i in nct.variables[Y[ver]][:nopts]],dtype=int)
nct.close()
nc.close()

#variable sets interception and with values
sint=[v for v in set(Vt1)&set(V[3]) if np.sum(var[Vt1.index(v),:,:])!=0.]
if len(sint)!=len(V[3]):
  s=''.join([c+',' for c in set(V[3])-set(sint)])
  ftmp=fname+'tmp'
  res=os.system(ncks+' -O -x -v'+s.strip(',')+' '+fname+' '+ftmp)
  if res!=0: sys.exit(ncks+' -x var fail')
  ns=str(len(sint)-1) 
  res=os.system(ncks+' -O -d VAR,0,'+ns+' '+ftmp+' '+fname)
  if res!=0: sys.exit(ncks+' -d VAR fail')
#template is OK

#pivoting
ntm,NREC=ntt,nopts
sdt,ix,iy=(np.zeros(shape=(ntm*NREC),dtype=int) for i in range(3))
idatetime=np.array([i for i in range(ntt)],dtype=int)
for t in range(ntm):
    t1,t2=t*NREC,(t+1)*NREC
    ix[t1:t2]=IX
    iy[t1:t2]=IY
for t in range(ntm):
    t1,t2=t*NREC,(t+1)*NREC
    sdt[t1:t2]=idatetime[t]
dfT=DataFrame({'YJH':sdt,'IX':ix,'IY':iy})
for v in sint:
  iv=Vt1.index(v)
  dfT[v]=var[iv,:,:].flatten()
pv=pivot_table(dfT,index=['YJH','IX','IY'],values=sint,aggfunc=sum).reset_index()
pv.IX=[int(i) for i in pv.IX]
pv.IY=[int(i) for i in pv.IY]
pv.YJH=[int(i) for i in pv.YJH]
boo=(pv.IX>=0) & (pv.IY>=0) & (pv.IX<ncol) & (pv.IY<nrow)
pv=pv.loc[boo].reset_index(drop=True)
imn,jmn=min(pv.IX),min(pv.IY)
imx,jmx=max(max(pv.IX)+abs(imn)*2+1,ncol), max(max(pv.IY)+abs(jmn)*2+1,nrow)
if imn<0 and imx+imn<ncol:sys.exit('negative indexing error in i')
if jmn<0 and jmx+jmn<nrow:sys.exit('negative indexing error in j')
idx=pv.index
idt=np.array(pv.loc[idx,'YJH'])
iy=np.array(pv.loc[idx,'IY'])
ix=np.array(pv.loc[idx,'IX'])
#reopen nc files and write time flags, and lengthen the span of time
nc = netCDF4.Dataset(fname,'r+')
for t in range(ntt):
  for i in range(2):
    nc.variables['TFLAG'][t,:,i]=TFLAG[t,i]
    nc.variables['ETFLAG'][t,:,i]=ETFLAG[t,i]
nc.SDATE=SDATE
nc.STIME=STIME
#blanking all variables
for c in sint:
  nc.variables[c][:]=0.
  z=np.zeros(shape=(ntm,jmx,imx))
  ss=np.array(pv.loc[idx,c])
  #Note that negative indices are not bothersome and are only at the end of the axis.
  z[idt,iy,ix]=ss
#also mapping whole matrix, NOT by parts
  nc.variables[c][:,0,:,:]=z[:,:nrow,:ncol]
nc.close()
#using CSC and XieHePP to calibrate the Map
xiheIXY_Verdi=(67,126) #fallen in the sea
xiheIXY_Target=(66,124)#calibrate with County border and seashore line
CSCIXY_Verdi=(20,30) #fallen in the KSHarbor
CSCIXY_Target=(21,31)
rateXY=np.array([(xiheIXY_Target[i]-CSCIXY_Target[i])/(xiheIXY_Verdi[i]-CSCIXY_Verdi[i]) for i in range(2)])
dxy_new=rateXY*np.array([XCELL,YCELL])
oxy_new=(1-rateXY)*dxy_new*np.array([ncol,nrow])/2.+np.array([XORIG,YORIG])
cmd1=' -a XCELL,global,o,f,'+str(dxy_new[0])
cmd2=' -a YCELL,global,o,f,'+str(dxy_new[1])
cmd3=' -a XORIG,global,o,f,'+str(oxy_new[0])
cmd4=' -a YORIG,global,o,f,'+str(oxy_new[1])
#ncatted -a XCELL,global,o,f,2872.340425531915 -a YCELL,global,o,f,2906.25 -a XORIG,global,o,f,-119074.46808510639 -a YORIG,global,o,f,-199078.125 fortBE.413_teds10.ptsE01.nc_d04.nc
#res=os.system(ncatted+cmd1+cmd2+cmd3+cmd4+' '+fname)
#if res!=0:sys.exit('fail ncatted')
sys.exit('fine!')
