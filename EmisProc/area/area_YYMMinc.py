"""usage:
python YYMM(year and month both in 2 digits)
1.Domain is determined by the template chosen.
2.One file(month) at a time. The resultant file will not be overwritten.
3.nc files may be corrupted if not properly written. must be remove before redoing.
4.nc_fac.json file is needed, df_Admw.py must be excuted earlier.
"""
import numpy as np
from pandas import *
from calendar import monthrange
import sys, os, subprocess
import netCDF4
from datetime import datetime, timedelta
from include2 import rd_ASnPRnCBM_A, WGS_TWD, tune_UTM
from include3 import dt2jul, jul2dt, disc, add_PMS, add_VOC
from mostfreqword import mostfreqword
import json
import warnings

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#Main
ym=sys.argv[1]
mm=sys.argv[1][2:4]
mo=int(mm)
yr=2000+int(sys.argv[1][:2])
if (yr-2016)%3 !=0 or 0==mo or mo>12:sys.exit('wrong ym='+ym)
teds=str((yr-2016)//3+10) #TEDS version increase every 3 years
P='./'

#time and space initiates
ntm=(monthrange(yr,mo)[1]+2)*24+1
bdate=datetime(yr,mo,1)+timedelta(days=-1+8./24)
edate=bdate+timedelta(days=monthrange(yr,mo)[1]+3)
#prepare the template
fname='fortBE.413_teds'+teds+'.area'+mm+'.nc'
try:
  nc = netCDF4.Dataset(fname, 'r+')
except:
  os.system('cp '+P+'template_d4.nc '+fname)
  nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
nv=len(V[3])
nc.SDATE,nc.STIME=dt2jul(bdate)
nc.EDATE,nc.ETIME=dt2jul(edate)
nc.NOTE='grid Emission'
nc.NOTE=nc.NOTE+(60-len(nc.NOTE))*' '
#Name-names may encounter conflicts with newer versions of NCFs and PseudoNetCDFs.
#nc.NAME='EMISSIONS '
if 'ETFLAG' not in V[2]:
  zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
if nt!=ntm or (nc.variables['TFLAG'][0,0,0]!=nc.SDATE and nc.variables['TFLAG'][0,0,1]!=nc.STIME):
  for t in range(ntm):
    sdate,stime=dt2jul(bdate+timedelta(days=t/24.))
    nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    ndate,ntime=dt2jul(bdate+timedelta(days=(t+1)/24.))
    nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
for v in V[3]:
  nc.variables[v][:]=0.
sdatetime=[jul2dt(nc.variables['TFLAG'][t,0,:]) for t in range(ntm)]
col=['PM','PM25', 'CO', 'NOX', 'NMHC', 'SOX','NH3'] #1NO   2NO2   3SO2   4NH3   5CCRS   6FCRS   7PAR
cole=['EM_'+i for i in col] #1NO   2NO2   3SO2   4NH3   5CCRS   6FCRS   7PAR
#define the crustals/primary sources
colc=['CCRS','FCRS','CPRM','FPRM']
c2v={i:i for i in colc}
c2m={i:1 for i in colc}
colv='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
NC=len(colv)
c2v.update({i:i for i in colv if i not in ['NR','ETHY']})
c2m.update({i:1 for i in colv if i not in ['NR','ETHY']})
c2v.update({'EM_SOX':'SO2','EM_NOX':'NO','EM_CO':'CO','EM_NH3':'NH3'})
c2m.update({'EM_SOX':64,'EM_NOX':46,'EM_CO':28,'EM_NH3':17})


#import the gridded area sources
fname=P+'areagrid'+teds+'LL.csv'
df = read_csv(fname)
minx,miny=min(df.UTME),min(df.UTMN)
df.UTME=round(df.UTME-minx,-3)
df.UTMN=round(df.UTMN-miny,-3)
df['YX']=np.array(df.UTMN+df.UTME/1000,dtype=int)

#add nh3 separately
YX_DICT=pivot_table(df,index=['YX'],values='DICT',aggfunc=mostfreqword).reset_index()
YX_DICT={i:j for i,j in zip(YX_DICT.YX,YX_DICT.DICT)}
df['EM_NH3']=0.
fname=P+'nh3.csv'
nh3=read_csv(fname)
nh3 = tune_UTM(nh3)
nh3['NSC']='nh3'
nh3['NSC_SUB']='b'
if 'nsc2' in df.columns: nh3['nsc2']='nh3b'
nh3.UTME=round(nh3.UTME-minx,-3)
nh3.UTMN=round(nh3.UTMN-miny,-3)
nh3['YX']=np.array(nh3.UTMN+nh3.UTME/1000,dtype=int)
nh3=nh3.loc[nh3.YX.map(lambda x:x in YX_DICT)].reset_index(drop=True)
nh3['DICT']=[YX_DICT[i] for i in nh3.YX]
for c in df.columns:
  if c not in nh3.columns:
    nh3[c]=0
df=df.append(nh3,ignore_index=True)
nh3=0#clean_up of mem

#The two levels of the NCS are grouped as one.
if 'nsc2' not in df.columns:
  df.loc[df['NSC_SUB'].map(lambda x: (type(x)==float and np.isnan(x)==True) or ( x==' ')),'NSC_SUB']='b'
  df['nsc2']=[str(x)+str(y) for x,y in zip(df['NSC'],df['NSC_SUB'])]
df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
if 'CNTY' not in df.columns:
  df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
coli=['CNTY', 'nsc2','YX']
df=pivot_table(df,index=coli,values=cole,aggfunc=np.sum).reset_index()

#note the df is discarded
df=add_PMS(df)
#add the VOC columns and reset to zero
if 'EM_NMHC' in df.columns:
  nmhc=df.loc[df.EM_NMHC>0]
  if len(nmhc)>0:
    for c in colv:
      df[c]=np.zeros(len(df))
    nsc2=set(nmhc.nsc2)
    for n in nsc2:
      df=add_VOC(df,n)
#Summed up for all the categories. The results are filled into the nc template
if set(c2v).issubset(set(df.columns)):
  df=pivot_table(df,index=['CNTY', 'YX', 'nsc2'],values=list(c2v),aggfunc=sum).reset_index()
else:
  sys.exit('not pivot')

#df store to matrix 
for c in ['CNTY','nsc2','YX']:
  exec(c+'=list(set(df.'+c+'))')
  exec(c+'.sort()')
  exec('n'+c+'=len('+c+')')
  exec('d'+c+'={'+c+'[i]:i for i in range(n'+c+')}')
  exec('df["i'+c+'"]=[d'+c+'[i] for i in df.'+c+']')
list_c2v=list(c2v)
list_c2v.sort()
NLC=len(c2v)
TPY=np.zeros(shape=(NLC,nCNTY,nnsc2,nYX))
for i in range(NLC):
  c=list_c2v[i]
  TPY[i,df.iCNTY[:],df.insc2[:],df.iYX[:]]=df[c][:]

#processing all the time-variation and constant categories
with open('nc_fac.json', 'r', newline='') as jsonfile:
  nc_fac=json.load(jsonfile)

yr=2016+(int(teds)-10)*3
bdate0=datetime(yr,1,1)-timedelta(days=1)
nd365=365
if yr%4==0:nd365=366
nty=(nd365+2)*24
dts=[bdate0+timedelta(days=i/24.) for i in range(nty)]

#time-variant part of nsc2
ll=list(nc_fac)
df=DataFrame({'nsc2':[i.split('_')[0] for i in ll],\
'CNTY':[i.split('_')[1] for i in ll],\
'fac':[nc_fac[i] for i in ll]})
nc_fac=0#clean_up of mem
#time variation files use ??b to represent all kind of NSC_SUB
for n2 in set(df.nsc2)-set(nsc2):
  a=df.loc[df.nsc2==n2].reset_index(drop=True)
  nns=[i for i in nsc2 if i[:-1]==n2[:-1]]
  for n in nns:
    a.nsc2=n
    df=df.append(a,ignore_index=True)
df=df.loc[df.nsc2.map(lambda x:x in nsc2)].reset_index(drop=True) #drop these surrogate nsc2
df=df.loc[df.CNTY.map(lambda x:x in CNTY)].reset_index(drop=True) #drop 53
nfac=len(df)
var2=np.zeros(shape=(nfac,nty),dtype=int)
fac =np.zeros(shape=(nCNTY,nnsc2,nty))
for c in ['CNTY','nsc2']:
  exec('var2[:,:]=np.array([d'+c+'[i] for i in df.'+c+'])[:,None]')
  exec('i'+c+'=var2[:,:].flatten()')
var2[:,:]=np.arange(nty)[None,:];    it=var2.flatten()
fac1=np.array([np.array(i) for i in df.fac]).flatten()
fac[iCNTY[:],insc2[:],it[:]]=fac1[:]
fac1=0#clean_up of mem

#constant part of nsc2
insc2=np.array([dnsc2[n] for n in set(nsc2)-set(df.nsc2)])
nnsc2=len(insc2)
var3=np.zeros(shape=(nCNTY,nnsc2,nty),dtype=int)
var3[:,:,:]=np.arange(nCNTY)[:,None,None];iCNTY=var3.flatten()
var3[:,:,:]=           insc2[None,:,None];insc2=var3.flatten()
var3[:,:,:]=  np.arange(nty)[None,None,:];it   =var3.flatten()
fac[iCNTY[:],insc2[:],it[:]]=1./nty

#cutting for desired month from whole year time-factors
ib=dts.index(bdate)
dts=dts[ib:ib+ntm]
fac=fac[:,:,ib:ib+ntm] #clean_up of mem

#eliminate the nsc2 and CNTY dimensions (multiply-and-sum by tensordot)
df,var2,var3,iCNTY,insc2,it=0,0,0,0,0,0 			#clean_up of mem
aTPY = np.tensordot(TPY,fac, axes=([1,2],[0,1])) 	#in shape of (isp, nYX, ntm)
TPY,fac=0,0											#clean_up of mem

idx=np.where(np.sum(aTPY[:,:,:],axis=0)>0)
dd,ic={},0
for c in list_c2v:
  dd[c]=aTPY[ic,idx[0][:],idx[1][:]]
  ic+=1
dd['YX']=[YX[i] for i in idx[0]]
dd['idt']=idx[1]
df=DataFrame(dd)
df['UTME']=(df.YX%1000)*1000+minx
df['UTMN']=(df.YX//1000)*1000+miny
df=disc(df,nc)											#disc after tensordot

fac=1000.*1000./nd365/24 #ton/yr to g/hr
  
#Filling to the template
var3=np.zeros(shape=(ntm,nrow,ncol))
for c in c2v:
  if c not in df.columns:continue
  if sum(df[c])==0.:continue
  if c2v[c] not in V[3]:continue
  #T/Y to gram/hour (gmole for SNC and VOCs)
  dfc=df.loc[df[c]>0].reset_index(drop=True)
  var3[:]=0.
  var3[dfc.idt,dfc.IY,dfc.IX]=dfc[c]*fac/c2m[c]
  nc.variables[c2v[c]][:,0,:,:]=var3[:,:,:]

nox=nc.variables['NO'][:]+nc.variables['NO2'][:]
nc.variables['NO'][:,0,:,:]=nox*0.9
nc.variables['NO2'][:,0,:,:]=nox-nc.variables['NO'][:]

nc.close()
