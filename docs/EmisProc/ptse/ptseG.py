
#! crding = utf8
from pandas import *
import numpy as np
import os, sys, subprocess
import netCDF4
import twd97
import datetime
from calendar import monthrange
from scipy.io import FortranFile

from ptse_sub import CORRECT, add_PMS, check_nan, check_landsea, FillNan, WGS_TWD, Elev_YPM

def pv_nc(dfi,spec):
  sdt,ix,iy=(np.zeros(shape=(ntm*NREC),dtype=int) for i in range(3))
  for t in range(ntm):
    t1,t2=t*NREC,(t+1)*NREC
    ix[t1:t2]=list(dfi.IX)
    iy[t1:t2]=list(dfi.IY)
  for t in range(ntm):
    t1,t2=t*NREC,(t+1)*NREC
    sdt[t1:t2]=idatetime[t]
  col=[i for i in dfi.columns if i not in ['YJH','IX','IY']]
  dfT=DataFrame({'YJH':sdt,'IX':ix,'IY':iy}) 
  if len(spec.shape)==2:
    for c in col: 
      ic=col.index(c)
      dfT[c]=spec[:,ic] 
  else:
    for c in col: 
      dfT[c]=spec[:] 
  pv=pivot_table(dfT,index=['YJH','IX','IY'],values=col,aggfunc=sum).reset_index()
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
  for c in col:
    if c not in V[3]:continue
    if sum(pv[c])==0:continue
    z=np.zeros(shape=(ntm,jmx,imx))
    ss=np.array(pv.loc[idx,c])
    #Note that negative indices are not bothersome and are only at the end of the axis.
    z[idt,iy,ix]=ss
#also mapping whole matrix, NOT by parts
    nc.variables[c][:,0,:,:]=z[:,:nrow,:ncol]
  return

def disc(dm):
#discretizations
  dm['IX']=np.array((dm.UTM_E-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
  dm['IY']=np.array((dm.UTM_N-Ycent-nc.YORIG)/nc.YCELL,dtype=int)
  return dm 

def jul2dt(jultm):
  jul,tm=jultm[:]
  yr=int(jul/1000)
  ih=int(tm/10000.)
  return datetime.datetime(yr,1,1)+datetime.timedelta(days=int(jul-yr*1000-1))+datetime.timedelta(hours=ih)

def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)


#Main
hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
P='./'
#time and space initiates
ym=sys.argv[1]
mm=sys.argv[1][2:4]
mo=int(mm)
yr=2000+int(sys.argv[1][:2])
Hs=10 #cutting height of stacks
ntm=(monthrange(yr,mo)[1]+2)*24+1
bdate=datetime.datetime(yr,mo,1)+datetime.timedelta(days=-1+8./24)
edate=bdate+datetime.timedelta(days=ntm/24)#monthrange(yr,mo)[1]+3)
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
#prepare the uamiv template
fname='fortBE.413_teds10.ptsG'+mm+'.nc'
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
    sdate,stime=dt2jul(bdate+datetime.timedelta(days=t/24.))
    nc.variables['TFLAG'][t,:,0]=[sdate for i in range(nv)]
    nc.variables['TFLAG'][t,:,1]=[stime for i in range(nv)]
    ndate,ntime=dt2jul(bdate+datetime.timedelta(days=(t+1)/24.))
    nc.variables['ETFLAG'][t,:,0]=[ndate for i in range(nv)]
    nc.variables['ETFLAG'][t,:,1]=[ntime for i in range(nv)]
for v in V[3]:
  nc.variables[v][:]=0.
#template OK



#Input the TEDS csv file
try:
  df = read_csv('point.csv', encoding='big5')
except:
  df = read_csv('point.csv')
# check_NOPandSCC(0)
df = check_nan(df)
# check and correct the X coordinates for isolated islands
df = check_landsea(df)
df = WGS_TWD(df)
df = Elev_YPM(df)
boo=(df.HEI<Hs) | (df.NO_S.map(lambda x:x[0]!='P')) 
df=df.loc[boo].reset_index(drop=True)
df['SUM']=[i+j+k+l+m for i,j,k,l,m in zip(df.SOX_EMI,df.NOX_EMI,df.CO_EMI,df.PM_EMI,df.NMHC_EMI)]
df=df.loc[df.SUM>0].reset_index(drop=True)
df['CP_NO'] = [i + j for i, j in zip(list(df['C_NO']), list(df['NO_S']))]
df['DY1']=[i*j for i,j in zip(df.DW1,df.WY1)]
df['HY1']=[i*j for i,j in zip(df.HD1,df.DY1)]
df.SCC=[str(i) for i in df.SCC]
df.loc[df.SCC=='0','SCC']='0'*10
print('NMHC expanding')
dfV=df.loc[df.NMHC_EMI>0].reset_index(drop=True)
#prepare the profile and CBMs
fname='/'+hmp+'/SMOKE4.5/data/ge_dat/gsref.cmaq_cb05_soa.txt'
gsref=read_csv(fname,delimiter=';',header=None)
col='SCC Speciation_profile_number Pollutant_ID'.split()+['C'+str(i) for i in range(3,10)]
gsref.columns=col
for c in col[3:]:
  del gsref[c]
fname='/'+hmp+'/SMOKE4.5/data/ge_dat/gspro.cmaq_cb05_soa.txt'
gspro=read_csv(fname,delimiter=';',header=None)
col=['Speciation_profile_number','Pollutant_ID','Species_ID','Split_factor','Divisor','Mass_Fraction']
gspro.columns=col
#new SCC since TEDS9,erase and substude
sccMap={
'30111103':'30111199', #not in df_scc2
'30112401':'30112403', #Industrial Processes  Chemical Manufacturing  Chloroprene Chlorination Reactor
'30115606':'30115607',#Industrial Processes  Chemical Manufacturing  Cumene  Aluminum Chloride Catalyst Process: DIPB Strip
'30118110':'30118109',#Industrial Processes  Chemical Manufacturing  Toluene Diisocyanate  Residue Vacuum Distillation
'30120554':'30120553', #not known, 548~  Propylene Oxide Mixed Hydrocarbon Wash-Decant System Vent
'30117410':'30117421', 
'30117411':'30117421', 
'30117614':'30117612', 
'30121125':'30121104', 
'30201111':'30201121', 
'30300508':'30300615', 
'30301024':'30301014', 
'40300215':'40300212'} #not known
for s in sccMap:
  dfV.loc[dfV.SCC==s,'SCC']=sccMap[s]
#reduce gsref and gspro
gsrefV=gsref.loc[gsref.SCC.map(lambda x:x in set(dfV.SCC))].reset_index(drop=True)
prof_alph=set([i for i in set(gsrefV.Speciation_profile_number) if i.isalpha()])
gsrefV=gsrefV.loc[gsrefV.Speciation_profile_number.map(lambda x:x not in prof_alph)].reset_index(drop=True)
gsproV=gspro.loc[gspro.Speciation_profile_number.map(lambda x:x in set(gsrefV.Speciation_profile_number))].reset_index(drop=True)
pp=[]
for p in set(gspro.Speciation_profile_number):
  a=gsproV.loc[gsproV.Speciation_profile_number==p]
  if 'TOG' not in set(a.Pollutant_ID):pp.append(p)
boo=(gspro.Speciation_profile_number.map(lambda x:x not in pp)) & (gspro.Pollutant_ID=='TOG')
gsproV=gspro.loc[boo].reset_index(drop=True)

cbm=list(set([i for i in set(gsproV.Species_ID) if i in V[3]]))
d_cbm={c:V[3].index(c) for c in cbm}
idx=gsproV.loc[gsproV.Species_ID.map(lambda x:x in cbm)].index
sccV=list(set(dfV.SCC))
sccV.sort()
nscc=len(sccV)
prod=np.zeros(shape=(nscc,len(cbm)))
#dfV but with PM scc(no TOG/VOC in gspro), modify those SCC to '0'*10 in dfV, drop the pro_no in gsproV
noTOG_scc=[]
for i in range(nscc):
  s=sccV[i]
  p=list(gsrefV.loc[gsrefV.SCC==s,'Speciation_profile_number'])[0]
  a=gsproV.loc[gsproV.Speciation_profile_number==p]
  if 'TOG' not in set(a.Pollutant_ID) and 'VOC' not in set(a.Pollutant_ID):
    noTOG_scc.append(s)
    continue
  boo=(gsproV.Speciation_profile_number==p) & (gsproV.Pollutant_ID=='TOG')
  a=gsproV.loc[boo]
  for c in a.Species_ID:
    if c not in cbm:continue
    j=cbm.index(c)
    f=a.loc[a.Species_ID==c,'Mass_Fraction']
    d=a.loc[a.Species_ID==c,'Divisor']
    prod[i,j]+=f/d
dfV.loc[dfV.SCC.map(lambda x:x in noTOG_scc),'SCC']='0'*10
for c in cbm:
  dfV[c]=0.
dfV.NMHC_EMI=[i*1E6/j/k for i,j,k in zip(dfV.NMHC_EMI,dfV.DY1,dfV.HD1)]
for s in set(dfV.SCC):
  i=sccV.index(s)
  idx=dfV.loc[dfV.SCC==s].index
  for c in cbm:
    j=cbm.index(c)
    dfV.loc[idx,c]=[prod[i,j]*k for k in dfV.loc[idx,'NMHC_EMI']]
if 'IY' not in dfV.columns:
  dfV=disc(dfV)

#matching of the bin filenames
fns0={
'NMHC':'NMHC_CP9348_MDH8760_ONS.bin',
'SNCP':'SNCP_CP4072_MDH8760_ONS.bin'}
fns10={
'NMHC':'NMHC_CP10066_MDH8784_ONS.bin',
'SNCP':'SNCP_CP10845_MDH8784_ONS.bin'}
fns30={
'NMHC':'NMHC_CP12581_MDH8784_ONS.bin',
'SNCP':'SNCP_CP22614_MDH8784_ONS.bin'}
F={0:fns0,10:fns10,30:fns30}
fns=F[Hs]
fnameO=fns['NMHC']
with FortranFile(fnameO, 'r') as f:
  cp = f.read_record(dtype=np.dtype('U12'))
  mdh = f.read_record(dtype=np.int)
  ons = f.read_record(dtype=np.int)
ons=ons.reshape(len(cp),len(mdh))
dfV_cp=pivot_table(dfV,index='CP_NO',values=cbm,aggfunc=sum).reset_index()
dfV_xy=pivot_table(dfV,index='CP_NO',values=['IX','IY'],aggfunc=np.mean).reset_index()
dfV2=merge(dfV_cp,dfV_xy,on='CP_NO')
dfV2=dfV2.sort_values('CP_NO').reset_index(drop=True)
idatetime=np.array([i for i in range(ntm)],dtype=int)
ibdate=list(mdh).index(int(bdate.strftime('%m%d%H')))
iedate=list(mdh).index(int(edate.strftime('%m%d%H')))
id365=365
if yr%4==0:id365=366
if ibdate>iedate:
  ons2=np.zeros(shape=(len(dfV2),ntm))
  endp=id365*24-ibdate
  ons2[:,:endp]=ons[:,ibdate:]
  ons2[:,endp:ntm]=ons[:,:iedate]
else:
  ons2=ons[:,ibdate:iedate]

NREC,NC=len(dfV2),len(cbm)
VOC=np.zeros(shape=(ntm*NREC,NC))
for t in range(ntm):
  t1,t2=t*NREC,(t+1)*NREC
  for c in cbm:
    ic=cbm.index(c)
    VOC[t1:t2,ic]=dfV2[c]*ons2[:,t]
col=['IX','IY']+cbm
pv_nc(dfV2[col],VOC)
print('SNCP expanding')
c2s={'SOX':'SO2','NOX':'NO2','CO':'CO','PM':'PM'}
boo2=(df.SOX_EMI+df.NOX_EMI+df.CO_EMI+df.PM_EMI)>0
cole=[i+'_EMI' for i in c2s]+['PM25_EMI']
col=['C_NO','CP_NO','HD1','DY1','HY1','UTM_E','UTM_N']+cole
colT=['HD1','DY1','HY1']
dfS=df[col].loc[boo2].reset_index(drop=True)
if 'IY' not in dfS.columns:
  dfS=disc(dfS)
for c in cole:
    dfS[c]=[i*1E6/j/k for i,j,k in zip(dfS[c],dfS.DY1,dfS.HD1)]
dfS_cp=pivot_table(dfS,index='CP_NO',values=cole,aggfunc=sum).reset_index()
dfS_xy=pivot_table(dfS,index='CP_NO',values=['IX','IY']+colT,aggfunc=np.mean).reset_index()
dfS2=merge(dfS_cp,dfS_xy,on='CP_NO')
dfS2=dfS2.sort_values('CP_NO').reset_index(drop=True)
NREC=len(dfS2)

fnameO=fns['SNCP']
with FortranFile(fnameO, 'r') as f:
  cp = f.read_record(dtype=np.dtype('U12'))
  mdh = f.read_record(dtype=np.int)
  ons = f.read_record(dtype=np.int)
ons=ons.reshape(len(cp),len(mdh))
if ibdate>iedate:
  ons2=np.zeros(shape=(len(dfS2),ntm))
  endp=id365*24-ibdate
  ons2[:,:endp]=ons[:,ibdate:]
  ons2[:,endp:ntm]=ons[:,:iedate]
else:
  ons2=ons[:,ibdate:iedate]


c2m={'SOX':64,'NOX':46,'CO':28,'PM':1}
colc=['CCRS','FCRS','CPRM','FPRM']
for sp in ['SOX','NOX','CO','PM']:
  if sp=='PM':
    dfS2=add_PMS(dfS2)
  dfS2[c2s[sp]]=np.array(dfS2[sp+'_EMI'])/c2m[sp]
  col=['IX','IY',c2s[sp]]
  if sp=='PM':
    col=['IX','IY']+colc
    val=np.zeros(shape=(ntm*NREC,len(colc)))
    for t in range(ntm):
      t1,t2=t*NREC,(t+1)*NREC
      for c in colc:
        ic=colc.index(c)
        val[t1:t2,ic]=dfS2[c]*ons2[:,t]
  else:
    val=np.zeros(shape=(ntm*NREC))
    for t in range(ntm):
      t1,t2=t*NREC,(t+1)*NREC
      val[t1:t2]=dfS2[c2s[sp]]*ons2[:,t]
  pv_nc(dfS2[col],val)
nox=nc.variables['NO'][:]+nc.variables['NO2'][:]
nc.variables['NO'][:,0,:,:]=nox*0.9
nc.variables['NO2'][:,0,:,:]=nox-nc.variables['NO'][:]

a=df.loc[df['PM_EMI']>0].reset_index(drop=True)

nc.close()
  
