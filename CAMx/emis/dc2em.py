#$ cat /nas1/camxruns/2016_v7/emis/dc2em.py
import netCDF4
from PseudoNetCDF.camxfiles.Memmaps import uamiv
from pandas import *
import os, sys
import datetime
import bisect
import subprocess

def locat(n):
# fortran indexing
# 86             Mbeg(igrd,isp)=i+ncol(igrd)*(j - 1) + ncol(igrd)*nrow(igrd)*(k - 1)
# 87      &       +ncol(igrd)*nrow(igrd)*nlay(igrd)*(isp-1) +(iptr4d(igrd)-1)

  D='0'
  for dd in ['1','2','4']:
    if n>=iptr4d[dd]:
      D=dd
  n4d=n+1-iptr4d[D]
  nx,ny,nz=ncol[D],nrow[D],nlay[D]
  nxyz=nx*ny*nz
  nxy=nx*ny
  l=n4d//nxyz+1
  n3d=n4d-nxyz*(l-1)
  k=n3d//nxy+1
  n2d=n3d-nxy*(k-1)
  j=n2d//nx+1
  i=n2d-nx*(j-1)
  return int(D),i,j,k,l
#tools
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
ncdump=subprocess.check_output('which ncdump',shell=True).decode('utf8').strip('\n')
pncgen=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')

#parameters
nn={'1': ['59', '59', '15'],'2': ['65', '65', '15'], '4': ['83', '137', '15']}
nxyz=[{} for i in range(3)]
for D in ['1','2','4']:
  for i in range(3):
    nxyz[i].update({D:int(nn[D][i])})
ncol,nrow,nlay=(nxyz[i] for i in range(3))
fname= '/nas1/camxruns/2016_v7/inputs/chem/CAMx7.0.chemparam.CB6r4_CF2'
with open(fname,'r') as f:
  part=[line.strip('\n').split() for line in f]
v4=[]
for i in part:
  if len(i) <=2:continue
  v4.append(i[1])
idx=v4.index('Spec');v4=v4[idx+1:]
idx=v4.index('Spec');v4[idx:]=v4[idx+1:]
idx=v4.index('Typ');v4=v4[:idx]
divD={'1':1000,'2':100,'4':1000} #divider for IJ
SPNAMs=['CO', 'NO2',  'O3', 'SO2','NMHC','PM10', 'PM2.5']
SPMAPs=['CO', 'NO2',  'O3', 'SO2','SOA1','SOA2', 'SOA3'] #use radical to store
#iptr4d={'2':1,'4':ncol['2']*nrow['2']*nlay['2']*len(v4)+1}
iptr4d={'1':1,'2':ncol['1']*nrow['1']*nlay['1']*len(v4)+1,'4':ncol['1']*nrow['1']*nlay['1']*len(v4)+ncol['2']*nrow['2']*nlay['2']*len(v4)+1}


#read camx700KF results
fname=sys.argv[1]
if 'dc_dt.csv' not in fname:sys.exit('only dc_dt.csv"s are considered')
root=fname.split('/')[-1].replace('dc_dt.csv','')
df=read_csv(fname)
#conc/c_obs are in micromole/cubic meter
iv=0
for v in 'date time nupd conc c_obs'.split():
  df[v]=[float(i.split()[iv]) for i in df.iloc[:,0]]
  if iv<=2:
    df[v]=[int(i) for i in df[v]]
  iv+=1
c=' date time nupd conc c_obs'
del df[c]

nupd=list(set(df.nupd))
for v in 'H,D,i,j,k,l'.split(','):
  df[v]=0
for n in nupd:
  idx=df.loc[df.nupd==n].index
  ll={v:s for v,s in zip('D,i,j,k,l'.split(','),locat(n))}
  for v in 'D,i,j,k,l'.split(','):
    df.loc[idx,v]=[ll[v] for s in idx]
df=df.loc[df.D==2].reset_index(drop=True)
df.H=df.time//100
df['dt']=[datetime.datetime.strptime(str(i)+'{:04d}'.format(j),'%y%j%H%M') for i,j in zip(list(df.date),list(df.time))]
dt=list(set(df.dt))
dt.sort()
dt=[datetime.datetime.strptime('162902000','%y%j%H%M')]+dt
deltaT=[(dt[i+1]-dt[i]).total_seconds() for i in range(len(dt)-1)]
df['delT']=0.
for t in dt[1:]:
  delT=deltaT[dt.index(t)-1]
  idx=df.loc[df.dt==t].index
  df.loc[idx,'delT']=[delT for i in idx]

#delE in moles/hour
fname=sys.argv[2]
fnameO=fname+'_'+root
os.system('cp '+fname+' '+fnameO)
#make sure the number of var is extendable
try:
  unlimit_dim=subprocess.check_output(ncdump+' -h '+fnameO+'|head -n10|grep UNLIMITED',shell=True).decode('utf8').strip('\t').split()[0]
except:
  rst=os.system(pncgen+' -O -f uamiv '+fnameO+' tmp')
  if rst!=0:sys.exit('pncgen fail for '+fnameO)
  rst=os.system('mv tmp '+fnameO)
  unlimit_dim=subprocess.check_output(ncdump+' -h '+fnameO+'|head -n10|grep UNLIMITED',shell=True).decode('utf8').strip('\t').split()[0]
if unlimit_dim !='VAR':
  rst=os.system(ncks+' -O  --mk_rec_dmn VAR  '+fnameO+' tmp')
  if rst!=0:sys.exit('ncks fail for '+fnameO)
  rst=os.system('mv tmp '+fnameO)

nc = netCDF4.Dataset(fnameO,'r+')
sdate,stime=(np.array(nc.variables['TFLAG'][:,0,i]) for i in range(2))
tflag=[datetime.datetime.strptime(str(i)+'{:02d}'.format(int(j/10000)),'%Y%j%H') for i,j in zip(sdate,stime)]
#only stamp can be properly located
tstamp=[datetime.datetime.timestamp(t) for t in tflag] #tflag in stamp form
dtstamp=[datetime.datetime.timestamp(t) for t in dt[1:]]# csv_dt's in stamp form
t_idx=[bisect.bisect_left(tstamp,t)-1 for t in dtstamp] #use bisect to locate appropriate hour, unless 00 sharp
df['IT']=-1
for t in dt[1:]:
  it=dt[1:].index(t)  #dt[0] is dummy start
  ti=t_idx[it]        #index of csv_dt in the tflag list (before sharp 00)
  if dtstamp[it] in tstamp:ti=tstamp.index(dtstamp[it]) #if csv_dt is 00 sharp, take index directly
  idx=df.loc[df.dt==t].index  #apply to all same dt
  df.loc[idx,'IT']=[ti for i in idx]

V0=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt, nlay, nrow, ncol = (nc.variables[V0[3][0]].shape[i] for i in range(4))
V1=set([v4[l-1] for l in set(df.l)])
newV=V1-set(V0[3])
if len(newV)>0:
  for v in newV:
    nc.createVariable(v,"f4",('TSTEP LAY ROW COL'.split()))
    nc.variables[v].units = "mol/time"
    nc.variables[v].long_name = v
    nc.variables[v].var_desc = v
    nc.variables[v][:]=0.
#extending the VAR dimension
for iv in range(nc.NVARS,nc.NVARS+len(newV)):
  for v in ['TFLAG','ETFLAG']:
    for i in range(2):
      nc.variables[v][:,iv,i]=nc.variables[v][:,0,i]
V0=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nc.NVARS=len(V0[3])
nc.close()
#the sequence of V's is control in VAR-LIST, it must be ncatted before further processing
rst=os.system('/nas1/camxruns/2016_v7/emis/add_ncatt.cs '+fnameO+' emis')
if rst !=0:sys.exit('fail to add_ncatt.cs')

nc = netCDF4.Dataset(fnameO,'r+')
#micro mole/M3 *Km*Km*m /(sec/3600)
vol=81*81*40
for l in set(df.l): #loop for specs
  v=v4[l-1]
  dfv=df.loc[df.l==l]
  var=np.array(nc.variables[v][:,:,:,:])
  for n in set(dfv.nupd): #loop for locations
    dfvn=dfv.loc[dfv.nupd==n].reset_index(drop=True)
#fortran index is one greater than python index
    i,j=dfvn.loc[0,'i']-1,dfvn.loc[0,'j']-1
    for t in range(len(dfvn)): #loop for times (delT en_effect)
      delT,it,conc,c_obs=(dfvn.loc[t,c] for c in 'delT IT conc c_obs'.split())
      var[it,0,j,i]+=(c_obs-conc)*vol

# keep emis >0 (CAMx will fail if emis<0)
  var[var<0]=0.
  nc.variables[v][:]=var[:]
nc.close()
