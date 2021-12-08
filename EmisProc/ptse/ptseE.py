
#! crding = utf8
from pandas import *
import numpy as np
import os, sys, subprocess
import netCDF4
import twd97
import datetime
from calendar import monthrange
from scipy.io import FortranFile

from mostfreqword import mostfreqword
from ptse_sub import CORRECT, add_PMS, check_nan, check_landsea, FillNan, WGS_TWD, Elev_YPM
from ioapi_dates import jul2dt, dt2jul
from cluster_xy import cluster_xy, XY_pivot

#Main
#locate the programs and root directory
pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
ncks=subprocess.check_output('which ncks',shell=True).decode('utf8').strip('\n')
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
nc.close()
#template OK

#item sets definitions
c2s={'NMHC':'NMHC','SOX':'SO2','NOX':'NO2','CO':'CO','PM':'PM'}
c2m={'SOX':64,'NOX':46,'CO':28,'PM':1}
cole=[i+'_EMI' for i in c2s]+['PM25_EMI']
XYHDTV=['UTM_E','UTM_N','HEI','DIA','TEMP','VEL']
colT=['HD1','DY1','HY1']
colc=['CCRS','FCRS','CPRM','FPRM']

#Input the TEDS csv file
try:
  df = read_csv('point.csv', encoding='utf8')
except:
  df = read_csv('point.csv')
df = check_nan(df)
df = check_landsea(df)
df = WGS_TWD(df)
df = Elev_YPM(df)
#only P??? an re tak einto account
boo=(df.HEI>=Hs) & (df.NO_S.map(lambda x:x[0]=='P'))
df=df.loc[boo].reset_index(drop=True)
#delete the zero emission sources
df['SUM']=[i+j+k+l+m for i,j,k,l,m in zip(df.SOX_EMI,df.NOX_EMI,df.CO_EMI,df.PM_EMI,df.NMHC_EMI)]
df=df.loc[df.SUM>0].reset_index(drop=True)
df['DY1']=[i*j for i,j in zip(df.DW1,df.WY1)]
df['HY1']=[i*j for i,j in zip(df.HD1,df.DY1)]
df=CORRECT(df)
df['CP_NO'] = [i + j for i, j in zip(list(df['C_NO']), list(df['NO_S']))]

#
#Coordinate translation
df.UTM_E=df.UTM_E-Xcent
df.UTM_N=df.UTM_N-Ycent
df.SCC=[str(int(i)) for i in df.SCC]
df.loc[df.SCC=='0','SCC']='0'*10
#pivot table along the dimension of NO_S (P???)
df_cp=pivot_table(df,index='CP_NO',values=cole+['ORI_QU1'],aggfunc=sum).reset_index()
df_xy=pivot_table(df,index='CP_NO',values=XYHDTV+colT,aggfunc=np.mean).reset_index()
df_sc=pivot_table(df,index='CP_NO',values='SCC', aggfunc=mostfreqword).reset_index()
df1=merge(df_cp,df_xy,on='CP_NO')
df=merge(df1,df_sc,on='CP_NO')
#T/year to g/hour
for c in cole:
  df[c]=[i*1E6 for i in df[c]]
#  df[c]=[i*1E6/j/k for i,j,k in zip(df[c],df.DY1,df.HD1)]
#determination of camx version
ver=7
if 'XSTK' in V[0]:ver=6
print('NMHC/PM splitting and expanding')
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
'30400213':'30400237',
'30120543':'30120502',
'40300215':'40300212'} #not known
for s in sccMap:
  df.loc[df.SCC==s,'SCC']=sccMap[s]
#reduce gsref and gspro
dfV=df.loc[df.NMHC_EMI>0].reset_index(drop=True)
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

cbm=list(set([i for i in set(gsproV.Species_ID) if i in V[1]]))
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
df.loc[df.SCC.map(lambda x:x in noTOG_scc),'SCC']='0'*10
for c in cbm:
  df[c]=0.
for s in set(dfV.SCC):
  i=sccV.index(s)
  idx=df.loc[df.SCC==s].index
  for c in cbm:
    j=cbm.index(c)
    df.loc[idx,c]=[prod[i,j]*k for k in df.loc[idx,'NMHC_EMI']]
#PM splitting
df=add_PMS(df)

#pivot along the axis of XY coordinates
#def. of columns and dicts
fns0={
'CO'  :'CO_ECP7496_MDH8760_ONS.bin',
'NMHC':'NMHC_ECP2697_MDH8760_ONS.bin',
'NOX' :'NOX_ECP13706_MDH8760_ONS.bin',
'PM'  :'PM_ECP17835_MDH8760_ONS.bin',
'SOX' :'SOX_ECP8501_MDH8760_ONS.bin'}

fns10={
'CO'  :'CO_ECP4919_MDH8784_ONS.bin',
'NMHC':'NMHC_ECP3549_MDH8784_ONS.bin',
'NOX' :'NOX_ECP9598_MDH8784_ONS.bin',
'PM'  :'PM_ECP11052_MDH8784_ONS.bin',
'SOX' :'SOX_ECP7044_MDH8784_ONS.bin'}
fns30={
'CO'  :'CO_ECP1077_MDH8784_ONS.bin',
'NMHC':'NMHC_ECP1034_MDH8784_ONS.bin',
'NOX' :'NOX_ECP1905_MDH8784_ONS.bin',
'PM'  :'PM_ECP2155_MDH8784_ONS.bin',
'SOX' :'SOX_ECP1468_MDH8784_ONS.bin'}
F={0:fns0,10:fns10,30:fns30}
fns=F[Hs]
cols={i:[c2s[i]] for i in c2s}
cols.update({'NMHC':cbm,'PM':colc})
colp={c2s[i]:i+'_EMI' for i in fns}
colp.update({i:i for i in cbm+colc})
lspec=[i for i in list(colp) if i not in ['NMHC','PM']]
c2m={i:1 for i in colp}
c2m.update({'SO2':64,'NO2':46,'CO':28})
col_id=["C_NO","XY"]
col_em=list(colp.values())
col_mn=['TEMP','VEL','UTM_E', 'UTM_N','HY1','HD1','DY1']
col_mx=['HEI']
df['XY']=[(x,y) for x,y in zip(df.UTM_E,df.UTM_N)]
df["C_NO"]=[x[:8] for x in df.CP_NO]


print('Time fraction multiplying and expanding')
#matching of the bin filenames
nopts=len(df)
SPECa=np.zeros(shape=(ntm,nopts,len(lspec)))
id365=365
if yr%4==0:id365=366
for spe in fns: 
  fnameO=fns[spe]
  with FortranFile(fnameO, 'r') as f:
    cp = f.read_record(dtype=np.dtype('U12'))
    mdh = f.read_record(dtype=np.int)
    ons = f.read_record(dtype=float)
  ons=ons.reshape(len(cp),len(mdh))
  s_ons=np.sum(ons,axis=1)
  #only those CP with emission accounts
  idx=np.where(s_ons>0)
  cp1 = [i for i in cp[idx[0]] if i in list(df.CP_NO)]
  idx= np.array([list(cp).index(i) for i in cp1])
  cp, ons, s_ons =cp1,ons[idx,:],s_ons[idx]
  #normalize to be the fractions in a year
  ons=ons/s_ons[:,None]
  idx_cp=[list(df.CP_NO).index(i) for i in cp]
  ibdate=list(mdh).index(int(bdate.strftime('%m%d%H')))
  iedate=list(mdh).index(int(edate.strftime('%m%d%H')))
  ons2=np.zeros(shape=(nopts,ntm)) #time fractions for this month
  if ibdate>iedate:
    endp=id365*24-ibdate
    ons2[idx_cp,:endp]=ons[:,ibdate:]
    ons2[idx_cp,endp:ntm]=ons[:,:iedate]
  else:
    ons2[idx_cp,:]=ons[:,ibdate:iedate]
  NREC,NC=nopts,len(cols[spe])
  ons =np.zeros(shape=(ntm,NREC,NC))
  SPEC=np.zeros(shape=(ntm,NREC,NC))
  for c in cols[spe]:
    ic=cols[spe].index(c)
    for t in range(ntm):
      SPEC[t,:,ic]=df[colp[c]]/c2m[c]
  OT=ons2.T[:,:]
  for ic in range(NC):
    ons[:,:,ic]=OT
  #whole matrix production is faster than idx_cp selectively manupilated
  for c in cols[spe]:
    if c not in V[1]:continue
    ic=cols[spe].index(c)
    icp=lspec.index(c)
    SPECa[:,:,icp]=SPEC[:,:,ic]*ons[:,:,ic]
print('pivoting along the C_NO axis')
#forming the DataFrame
CPlist=list(set(df.CP_NO))
CPlist.sort()
pwrt=int(np.log10(len(CPlist))+1)
CPdict={i:CPlist.index(i) for i in CPlist}
df['CP_NOi']=[CPdict[i] for i in df.CP_NO]
idatetime=np.array([i for i in range(ntm) for j in range(nopts)],dtype=int)
dfT=DataFrame({'idatetime':idatetime})
ctmp=np.zeros(shape=(ntm*nopts))
for c in col_mn+col_mx+['CP_NOi']+['ORI_QU1']:
  clst=np.array(list(df[c]))
  for t in range(ntm):
    t1,t2=t*nopts,(t+1)*nopts
    a=clst
    if c=='CP_NOi':a=t*10**(pwrt)+clst
    ctmp[t1:t2]=a
  dfT[c]=ctmp
#dfT.C_NOi=np.array(dfT.C_NOi,dtype=int)
for c in lspec: 
  icp=lspec.index(c)
  dfT[c]=SPECa[:,:,icp].flatten()
#usage: orig df, index, sum_cols, mean_cols, max_cols
df=XY_pivot(dfT,['CP_NOi'],lspec,col_mn+['ORI_QU1'],col_mx).reset_index()
df['CP_NO']=[int(j)%10**pwrt for j in df.CP_NOi]

pv=XY_pivot(df,['CP_NO'],lspec,col_mn+['ORI_QU1'],col_mx).reset_index()
Bdict={CPdict[j]:[bytes(i,encoding='utf-8') for i in j] for j in CPlist}
pv['CP_NOb'] =[Bdict[i] for i in pv.CP_NO]
nopts=len(set(pv))

#blanck the PY sources
PY=pv.loc[pv.CP_NOb.map(lambda x:x[8:10]==[b'P', b'Y'])]
nPY=len(PY)
a=np.zeros(ntm*nPY)
for t in range(ntm):
  t1,t2=t*nPY,(t+1)*nPY
  a[t1:t2]=t*nopts+np.array(PY.index,dtype=int)
for c in colc:
  ca=df.loc[a,c]/5.  
  df.loc[a,c]=ca
df.to_feather('df'+mm+'.fth')
pv.set_index('CP_NO').to_csv('pv'+mm+'.csv')
    
sys.exit()

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
v2n={PRM[i]:XYHDTV[i] for i in range(6)}
names={7:['xcoord','ycoord','stkheight','stkdiam','stktemp','stkspeed'],
       6:[v+'STK' for v in PRM]}
v2c={PRM[i]:names[ver][i] for i in range(6)}
a=DataFrame({'SN':df.SO2+df.NO2})
a=a.sort_values('SN',ascending=False)
pig=a.index[:100]
#filling the stack parameters for camx700nc
nc = netCDF4.Dataset(NCfname, 'r+')
#enlarge the record dimension (COL)
for c in V[1]:
  if c == 'CP_NO':continue
  for i in range(nopts):
    nc.variables[c][0,i]=0.
if ver==7:nc.variables['pigflag'][:nopts]=0
for v in PRM:
  var=v2c[v]
  nc.variables[var][:nopts]=np.array(pv[v2n[v]])
nc.variables[v2c['V']][:nopts]=nc.variables[v2c['V']][:]*3600.
#first 100 for PiG
if ver==7:
  nc.variables['pigflag'][pig]=1
else:
  nc.variables[v2c['D']][pig]=nc.variables[v2c['D']][pig]*-1.
for c in V[1]:
  if c not in lspec:continue
  ic=lspec.index(c)
  nc.variables[c][:,:nopts]=np.array(df[c]).reshape(ntm,nopts)
  print(c)
nc.variables['CP_NO'][:nopts,:8]=np.array(list(pv.CP_NOb)).flatten().reshape(nopts,8)
nox=nc.variables['NO2'][:,:nopts]
nc.variables['NO'][:,:nopts]=nox[:,:nopts]*0.9
nc.variables['NO2'][:,:nopts]=nox-nc.variables['NO'][:,:nopts]
nc.close()

sys.exit()
