#!/opt/ohpc/pkg/rcec/pkg/python/wrfpost/bin/python
import numpy as np
import netCDF4
import datetime
import sys,os

def j2c(j):
  y=int(j)//1000
  d=int(j)%1000
  return (datetime.datetime(y,1,1)+datetime.timedelta(days=(d-1))).strftime("%Y%m%d")

fname=sys.argv[1]

last=fname.split('/')[-1]
outdir=fname.split('.')[-1]
if '/' in fname:
  i1=fname.index(last)
  outdir=fname[:i1]+fname.split('.')[-1]
fnroot=last.split('.')[0]
nc = netCDF4.Dataset(fname,'r')
nt=nc.dimensions['TSTEP'].size
v='TFLAG'
dates=np.array(nc.variables[v][:,0,0])
sdates=list(set(dates))
sdates.sort()

fnames=[outdir+'/'+fnroot+'.'+j2c(i) for i in sdates]
os.system('mkdir -p '+outdir)
df={i:j for i,j in zip(sdates,fnames)}
opt='/work/sinotec2/opt/cmaq_recommend'
for d in df:
  idx=np.where(dates==d)[0]
  i1,i2=str(idx[0]),str(idx[-1])
  if i1==i2:continue
  os.system(opt+'/bin/ncks -O -d TSTEP,'+i1+','+i2+' '+fname+' '+df[d])
  os.system(opt+'/bin/ncatted -a SDATE,global,o,i,'+str(d)+' '+df[d])
  os.system(opt+'/bin/add_lastHr.py '+df[d])