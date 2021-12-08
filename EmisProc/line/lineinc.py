#!/cluster/miniconda/envs/py37/bin/python
import numpy as np
import netCDF4
import os,sys
from pathlib import Path
from include2 import rd_hwcsv,rd_ASnPRnCBM
from include3 import jul2dt, dt2jul 
from scipy.io import FortranFile
from pandas import *
from calendar import monthrange
import datetime
import twd97
import subprocess


#Input the record csv and EM matrix, then reshaping them.
P=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n')+'/'
teds=int(P.split('/')[3][-2:])
yr=2016+(teds-10)*3

#read the index
df=read_csv(P+'df_kin.csv')
NREC,X,Y,R,C=len(df),list(df.X),list(df.Y),list(df.R),list(df.C)
APOL=['CO', 'EHC', 'EXHC', 'NH3', 'NMHC', 'NOX', 'PB', 'PM', 'PM25', 'PM6', 'RHC', 'RST', 'SOX', 'THC', 'TSP']
VT_TM=['bhddt', 'bhdgv', 'blddt', 'blddv', 'bldgt', 'bldgv', 'bldhev', 'bldlpg', 'bus', 'hdsv', 'ldsv', 'mc2', 'mc4', 'phddt', 'phdgv', 'plddt', 'plddv', 'pldgt', 'pldgv', 'pldhev', 'pldlpg']
NPOLn=len(APOL);LTYP=4;NVTYP=len(VT_TM)

#read the emission matrix
fname = 'cl08_'+'{:d}_{:d}_{:d}'.format(NREC,NPOLn,NVTYP)+'.bin'
with FortranFile(P+fname, 'r') as f:
  TM3=f.read_record(dtype=np.float64)
#The line type are dependent to NREC series also redundent, degrading it.
#convert the unit from T/Y to g/hr
ndays=365
if yr%4==0:ndays=366
UNIT=1000.*1000./(24.*ndays)
TM3=np.reshape(TM3,[NREC,NPOLn,NVTYP])*UNIT
#from TSP and PM2.5 calculate CPRM and store replacing original TSP
Aold='TSP PM25 SOX NOX CO EXHC EHC RHC NMHC PB'.split()
NPOL=len(Aold)
EM3=np.zeros(shape=(NREC,NPOL,NVTYP))
d_ON={i:APOL.index(Aold[i]) for i in range(NPOL)}
for i in range(NPOL):
  EM3[:,i,:]=TM3[:,d_ON[i],:]
TM3=0
TSP,FPRM=EM3[:,0,:],EM3[:,1,:]
CPRM=TSP-FPRM
EM3[:,0,:]=CPRM
APOL='CPRM FPRM SO2 NO CO EXHC EHC RHC NMHC PB'.split()

#Time varied factors
(df_t,sdf2csv)=rd_hwcsv()

#SPECIATE, PROFILE database for vehicles
(df_asgn,df_prof,df_cbm)= rd_ASnPRnCBM()
MW={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['MW']))}
colc=['CCRS','FCRS','CPRM','FPRM']
c2v={i:i for i in colc}
c2m={i:1 for i in colc}
colv='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
c2v.update({i:i for i in colv if i not in ['NR','ETHY']})
c2m.update({i:1 for i in colv if i not in ['NR','ETHY']})
c2v.update({'EM_SOX':'SO2','EM_NOX':'NO','EM_CO':'CO'})
c2m.update({'SO2':64,'NO':46,'CO':28})

BASE={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['BASE']))}
NC=[5,20] #number pf compounds for non-VOCs and VOCs
SPNAM='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
if len(SPNAM) != NC[1]: sys.exit('wrong NC_vocs or SPNAM')
colv=SPNAM
cole=APOL[:NC[0]]
#define the crustals/primary sources
try:
  prof_cbm=read_csv(P+'prof_cbm.csv')
  prof_cbm.PRO_NO=['{:04d}'.format(m) for m in prof_cbm.PRO_NO]
except:
  HC=1
  prof_cbm=DataFrame({})
  prof_cbm['PRO_NO']=list(set(df_asgn.PRO_NO))
  for c in colv:
    prof_cbm[c]=0.
  for i in range(len(prof_cbm)):
    prof=prof_cbm.PRO_NO[i]
    spec=df_prof.loc[df_prof.PRO_NO==prof].reset_index(drop=True)
    for K in range(len(spec)):
      W_K_II,IS=spec.WT[K],spec.SPE_NO[K]
      if W_K_II==0.0 or sum(BASE[IS])==0.0:continue
      VOCwt=HC*W_K_II/100. 
      VOCmole=VOCwt/MW[IS] 
      for LS in range(NC[1]): #CBM molar ratio
        if BASE[IS][LS]==0.:continue
        prof_cbm.loc[i,colv[LS]]+=VOCmole*BASE[IS][LS]
  prof_cbm.set_index('PRO_NO').to_csv('prof_cbm.csv')

cart=['CAR_LT','CAR_LV','CAR_HT','CAR_HV']
ncar=len(cart)
VT21_13={ 'bhddt': 'hddt', 'bhdgv': 'hdgv', 'blddt': 'lddt', 'blddv': 'pldd',
 'bldgt': 'ldgt', 'bldgv': 'bldg', 'bldhev':'pldg', 'bldlpg':'bldl', 'bus':   'bus',
 'hdsv':'hdsv', 'ldsv':'ldsv', 'mc2': 'mc2', 'mc4': 'mc4', 'phddt': 'hddt', 'phdgv': 'hdgv',
 'plddt': 'lddt', 'plddv': 'pldd', 'pldgt': 'ldgt', 'pldgv': 'pldg', 'pldhev':'pldg',
 'pldlpg':'bldl'}
for i in VT21_13:
  VT21_13.update({i:VT21_13[i].upper()+' '*(4-len(VT21_13[i]))})
lVT=list(set(VT21_13))
lVT.sort()
VT21_CAR={ 'bhddt':3, 'bhdgv':4, 'blddt':1, 'blddv':2,
 'bldgt':1, 'bldgv':2, 'bldhev':2, 'bldlpg':2, 'bus':3,
 'hdsv':4, 'ldsv':2, 'mc2':0, 'mc4':0, 'phddt':3, 'phdgv': 3,
 'plddt': 1, 'plddv': 2, 'pldgt': 1, 'pldgv': 2, 'pldhev':2,
 'pldlpg':2}
#old Viehle type
VTYP=['PLDG','BLDG', 'LDGT','LDDT','HDGV','HDDT', \
     'BUS ','MC2 ','MC4 ','PLDD','BLDL', 'LDSV','HDSV']
ETYP=['EX ','E  ','R  ']

#Applied the PROFILE to the vehicles and emis. sources
NETYP=3
prod=np.zeros(shape=(NETYP,NVTYP,NC[1]))
for I in range(NETYP):
  for J in range(NVTYP):
    boo1=(df_asgn['ET']==ETYP[I]) & (df_asgn['VT']==VT21_13[lVT[J]])
    prof=list(df_asgn.loc[boo1,'PRO_NO'])[0]
    cbms=prof_cbm.loc[prof_cbm.PRO_NO==prof].iloc[0,1:]
    prod[I,J,:]=cbms

#Temporal and Spatial bases
mm=sys.argv[1]
mo=int(mm)
ntm=(monthrange(yr,mo)[1]+2)*24+1
bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
edate=bdate+datetime.timedelta(days=monthrange(yr,mo)[1]+3)
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)


#prepare the uamiv template
fname='fortBE.413_teds10.line'+mm+'.nc'
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
#Time stamps
if 'ETFLAG' not in V[2]:
  zz=nc.createVariable('ETFLAG',"i4",("TSTEP","VAR","DATE-TIME"))
if 'nt' not in locals() or nt!=ntm:
  for t in range(ntm):
    sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
    nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
    nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
sdatetime=[jul2dt(nc.variables['TFLAG'][t,0,:]) for t in range(ntm)]
for c in V[3]:
  nc.variables[c][:]=0.

#Horizontal Grid system, which is dependent to template
df['UTME']=df.X*1000.
df['UTMN']=df.Y*1000.
df['IX']=np.array((df.UTME-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
df['IY']=np.array((df.UTMN-Ycent-nc.YORIG)/nc.YCELL,dtype=int)


#Expand and store the hourly factors into facs and fact matrix
DICT=list(set(df_t.DICT))
NCNT=len(DICT)+1
idict={i:len(DICT) for i in set(df.C)-set(df_t.DICT)} #df.CNTY not in df_t.DICT, mappint to 17(last one)
idict.update({i:DICT.index(i) for i in DICT})
NSLT=ncar+1 #0 for motorcycles, 1/2/3/4 are small, light and heavy T and V
facs=np.ones(shape=(ntm,NCNT,NSLT))
#loop for time
for it in range(ntm):
  year,mo,da,hr=sdatetime[it].year,sdatetime[it].month,sdatetime[it].day,sdatetime[it].hour
  boo=(df_t['MONTH']==mo)&(df_t['DATE']==da)&(df_t['HOUR']==hr*100)
  df1=df_t.loc[boo]
  if len(df1)==0:
    sys.exit('DateHr not found:'+str(mo)+str(da)+str(hr))
  for cnt in DICT:
    idc=idict[cnt]
    df2=df1.loc[df1['DICT']==cnt]
    if len(df2)==0:continue
    facs[it,idc,:]=[0]+[list(df2[cart[icar]])[0]*ndays*24. for icar in range(ncar)]
facs[:,:,0]=np.mean(facs[:,:,1:2],axis=2) #motocycle is same as light
facs[:,len(DICT),:]=np.mean(facs[:,:len(DICT)+1,:],axis=1) #last one store the mean values

df['idc']=[idict[i] for i in df.C]
fact=np.zeros(shape=(ntm,NREC,NVTYP))
for J in range(NVTYP):
  fact[:,:,J]=facs[:,df.idc[:],VT21_CAR[lVT[J]]]

facs=0
#expand the POLs matrixs
EM4=np.zeros(shape=(ntm,NREC,NC[0],NVTYP))
c2mv=np.array([c2m[cole[I]] for I in range(NC[0])])
EM4[:,:,:,:]=EM3[None,:,:NC[0],:]*fact[:,:,None,:]/c2mv[None,None,:,None]

#sum-up the vehicle dimension
POL=np.sum(EM4[:,:,:,:],axis=3)
#expand the VOCs matrixs
EM4=np.zeros(shape=(ntm,NREC,NETYP,NVTYP))
EM4[:,:,:,:]=EM3[None,:,NC[0]:NC[0]+NETYP,:]*fact[:,:,None,:]
VOC=np.dot(EM4.reshape(ntm, NREC, NETYP*NVTYP), prod.reshape(NETYP*NVTYP,NC[1]))
sdt,ix,iy=(np.zeros(shape=(ntm*NREC),dtype=int) for i in range(3))
idatetime=np.array([i for i in range(ntm)],dtype=int)
for t in range(ntm):
    t1,t2=t*NREC,(t+1)*NREC
    ix[t1:t2]=list(df.IX)
    iy[t1:t2]=list(df.IY)
for t in range(ntm):
    t1,t2=t*NREC,(t+1)*NREC
    sdt[t1:t2]=idatetime[t]
dfT=DataFrame({'YJH':sdt,'IX':ix,'IY':iy}) 
for ic in range(NC[0]): 
    dfT[cole[ic]]=POL[:,:,ic].flatten() 
for ic in range(NC[1]): 
    dfT[colv[ic]]=VOC[:,:,ic].flatten() 
pv=pivot_table(dfT,index=['YJH','IX','IY'],values=colv+cole,aggfunc=sum).reset_index()
pv.IX=[int(i) for i in pv.IX]
pv.IY=[int(i) for i in pv.IY]
pv.YJH=[int(i) for i in pv.YJH]
imn,jmn=min(pv.IX),min(pv.IY)
imx,jmx=max(max(pv.IX)+abs(imn)*2+1,ncol), max(max(pv.IY)+abs(jmn)*2+1,nrow)
if imn<0 and imx+imn<ncol:sys.exit('negative indexing error in i')
if jmn<0 and jmx+jmn<nrow:sys.exit('negative indexing error in j')
idx=pv.index
idt=np.array(pv.loc[idx,'YJH'])
iy=np.array(pv.loc[idx,'IY'])
ix=np.array(pv.loc[idx,'IX'])

for c in colv+cole:
  if c not in V[3]:continue
  z=np.zeros(shape=(ntm,jmx,imx))
  ss=np.array(pv.loc[idx,c])
  #Note that negative indices are not bothersome and are only at the end of the axis.
  z[idt,iy,ix]=ss
#also mapping whole matrix, NOT by parts
  nc.variables[c][:,0,:,:]=z[:,:nrow,:ncol]
nox=nc.variables['NO'][:]+nc.variables['NO2'][:]
nc.variables['NO'][:,0,:,:]=nox*0.9
nc.variables['NO2'][:,0,:,:]=nox-nc.variables['NO'][:]

nc.close()
pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
result=os.system(pncg+' -O --out-format=uamiv '+fname+' '+fname.replace('.nc',''))
