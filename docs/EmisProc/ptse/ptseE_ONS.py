
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

#Main
hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
P='./'
Hs=0 #cutting height of stacks
#Input the TEDS csv file
try:
  df = read_csv('point.csv', encoding='utf8')
except:
  df = read_csv('point.csv')
# check_NOPandSCC(0)
df = check_nan(df)
# check and correct the X coordinates for isolated islands
df = check_landsea(df)
df = Elev_YPM(df)
df=df.loc[(df.HEI>=Hs) & (df.NO_S.map(lambda x:x[0]=='P'))].reset_index(drop=True)
df['SUM']=[i+j+k+l+m for i,j,k,l,m in zip(df.SOX_EMI,df.NOX_EMI,df.CO_EMI,df.PM_EMI,df.NMHC_EMI)]
df=df.loc[df.SUM>0].reset_index(drop=True)
df['CP_NO'] = [i + j for i, j in zip(list(df['C_NO']), list(df['NO_S']))]
df['DY1']=[i*j for i,j in zip(df.DW1,df.WY1)]
df['HY1']=[i*j for i,j in zip(df.HD1,df.DY1)]

#71 factories with CEMS will emit (at ground) when stacks are operating
fname=P+'point_cems.csv'
cems=read_csv(fname)
if 'CP_NO' not in cems.columns:
  idx=cems[cems.C_NO=='C_NO'].index
  cems=cems.drop(idx).reset_index(drop=True)
  cems['SNF']=[i+j+k for i,j,k in zip(cems.SOX,cems.NOX,cems.FLOW)]
  cems.drop(cems.loc[cems.SNF==0].index,inplace=True)
  cems=cems.reset_index(drop=True)
  cems['CP_NO'] = [i + j for i, j in zip(list(cems['C_NO']), list(cems['NO_S']))]
  cems['PM']=[(i+j)/2 for i,j in zip(cems.SOX,cems.NOX)]
  val='SOX PM NOX FLOW X_BLANK1 X_BLANK2'.split()
  if max(cems.HOUR)>100:
    cems['MDH']=[int(i*10000+j*100+k/100) for i,j,k in zip(cems.MONTH,cems.DATE,cems.HOUR)]
  else:
    cems['MDH']=[int(i*10000+j*100+k) for i,j,k in zip(cems.MONTH,cems.DATE,cems.HOUR)]
  cems=pivot_table(cems,index=['CP_NO','MDH'],values=val,aggfunc=sum).reset_index()
  cems=cems.sort_values('MDH',ascending=True).reset_index(drop=True)
  cems['MD']=[i//100 for i in cems.MDH]
  #coverage test
  id365=365
  if len(cems.loc[(cems.MD==229)])>0:id365=366
  s365=set([i*24 for i in range(id365)])
  ih8760=id365*24
  mdh=list(set(cems.MDH))
  if len(mdh)!=ih8760:sys.exit('mdh coverage not enough!')
  mdh.sort()
  md=list(set(cems.MD))
  md.sort()
  cs,cp_no=[],set(cems.CP_NO)
  for c in cp_no:
    n=len(cems.loc[cems.CP_NO==c])
    if n != ih8760: cs.append(c)
  #fill the hours
  idc=['CP_NO']
  cp_no=set(cems.CP_NO)
  add_cems=DataFrame({})
  for c in cp_no:
    cemsp=cems.loc[cems.CP_NO==c].reset_index(drop=True)
    n=len(cemsp)
    if n>ih8760:sys.exit('wrong in ih8760 for '+c)
    if n != ih8760:
      a=dict(cemsp.loc[0])
      for ci in val:
        a[ci]=0.
      sMDH=set(mdh)-set(cemsp.MDH)
      ns=len(sMDH)
      md_c,mdh_c=[s//100 for s in sMDH],[s for s in sMDH]
      b=cems.loc[:ns-1].reset_index(drop=True)
      for ci in idc+val:
        b.loc[:,ci]=a[ci]
      b.MD,b.MDH=md_c,mdh_c
      add_cems=add_cems.append(b,ignore_index=True)
  cems=cems.append(add_cems,ignore_index=True)
  cems['C_NO']=[i[:8] for i in cems.CP_NO]
  cems.set_index('CP_NO').to_csv(fname)
else:
  #coverage test
  id365=365
  if len(cems.loc[(cems.MD==229)])>0:id365=366
  s365=set([i*24 for i in range(id365)])
  ih8760=id365*24
  mdh=list(set(cems.MDH))
  mdh.sort()
  md=list(set(cems.MD))
  md.sort()

pv_cems1=pivot_table(cems,index=['C_NO','MDH'],values='SOX',aggfunc=sum).reset_index()
pv_cems1['HR']=[i%100 for i in pv_cems1.MDH]
cems_HROD=DataFrame({'C_NO':list(set(pv_cems1.C_NO))})
cems_HROD['SOX_HR_ODER']=0
for ic in range(len(cems_HROD.C_NO)):
  c=cems_HROD.C_NO[ic]
  pv1=pv_cems1.loc[pv_cems1.C_NO==c]
  pv3=pivot_table(pv1,index=['HR'],values='SOX',aggfunc=sum).reset_index()
  pv3=pv3.sort_values('SOX',ascending=False).reset_index(drop=True)
  s=''
  for i in range(24):
    s+=str(list(pv3.HR)[i])+' '  
  cems_HROD.loc[ic,'SOX_HR_ODER']=s
#orders for DY1  
pv_cems2=pivot_table(cems,index=['C_NO','MD'],values='FLOW',aggfunc=sum).reset_index()
#Indexing is an exhaustive process.
pv_cems2['MD']=[mdh.index(i*100) for i in pv_cems2.MD] #change the MMDD into sequence among MMDD00's
cems_DAOD=DataFrame({'C_NO':list(set(pv_cems2.C_NO))})
cems_DAOD['FLOW_DA_ODER']=0
for ic in range(len(cems_DAOD.C_NO)):
  c=cems_DAOD.C_NO[ic]
  pv1=pv_cems2.loc[pv_cems2.C_NO==c]
  pv3=pv1.sort_values('FLOW',ascending=False).reset_index(drop=True)
  s=''
  for i in range(len(pv3)):
    s+=str(list(pv3.MD)[i])+' '
  cems_DAOD.loc[ic,'FLOW_DA_ODER']=s

dfxy=pivot_table(df,index='C_NO',values=['UTM_E','UTM_N'],aggfunc=np.mean).reset_index() 

#booleans for pollutant selection
c2v={'NMHC':'PM','SOX':'SOX','NOX':'NOX','PM':'PM','CO':'NOX'} #point.csv vs cems.csv
BLS={c:df[c+'_EMI']>0 for c in c2v}
colT=['HD1','DY1','HY1']
col=['C_NO','CP_NO','HD1','DY1','HY1']+[i for i in df.columns if 'EMI' in i]
for spe in [s for s in [sys.argv[1]] if s in BLS]:
  dfV=df[col].loc[BLS[spe]].reset_index(drop=True)
  dfV1=pivot_table(dfV,index='CP_NO',values=spe+'_EMI',aggfunc=sum).reset_index()
  dfV2=pivot_table(dfV,index='CP_NO',values=colT,aggfunc=np.mean).reset_index()
  dfV=merge(dfV1,dfV2,on='CP_NO')
  dfV['C_NO']=[i[:8] for i in dfV.CP_NO]
  for c in colT:
    dfV[c]=np.array(dfV[c],dtype=int)
  a,b=set(dfV.C_NO),set(cems.C_NO) 
  a,b=list(a),list(b)
  a.sort()
  b.sort()
  ab=[i for i in a if i in b]
  cp=list(set(dfV.CP_NO))
  cp.sort()
  ons=np.zeros(shape=(len(cp),len(mdh)))#,dtype=int)
  #other fatories without CEMS, take the nearest one
  b1=set(b)-set(dfxy.C_NO)
  c1=[c for c in b if c not in b1 and c in a]
  cemsX=np.array([list(dfxy.loc[dfxy.C_NO==c,'UTM_E'])[0] for c in b if c not in b1 and c in a])
  cemsY=np.array([list(dfxy.loc[dfxy.C_NO==c,'UTM_N'])[0] for c in b if c not in b1 and c in a])
  #loop for every factories
  for c in [i for i in a if i not in b1]:
    c_cems=c
    if c not in ab:
      x0,y0=list(dfxy.loc[dfxy.C_NO==c,'UTM_E'])[0],list(dfxy.loc[dfxy.C_NO==c,'UTM_N'])[0]
      dist=(cemsX-x0)**2+(cemsY-y0)**2
      idx=list(dist).index(min(dist))
      c_cems=c1[idx]
    pv2MD=np.array(list(cems_DAOD.loc[cems_DAOD.C_NO==c_cems,'FLOW_DA_ODER'])[0].split(),dtype=int)
    if len(pv2MD)<id365:
      app=list(s365-set(pv2MD))
      pv2MD=np.array(list(pv2MD)+app)
    df_cp=dfV.loc[dfV.C_NO==c].reset_index(drop=True)
    #loop for every NO_S in this factory
    for p in set(df_cp.CP_NO):
      i=cp.index(p)
      if p in set(cems.CP_NO):
        ons[i,:]=cems.loc[cems.CP_NO==p,c2v[spe]]*ih8760
      else:
        dy1=dfV.DY1[i]
        hd1=dfV.HD1[i]
        md3=pv2MD[:dy1] 
        days=np.zeros(shape=(dy1,hd1),dtype=int)
        if hd1==24:
          hrs=np.array([i for i in range(24)],dtype=int)
        else:
          first=np.array(list(cems_HROD.loc[cems_HROD.C_NO==c_cems,'SOX_HR_ODER'])[0].split(),dtype=int)[0]
          hrs=np.array([(first+i)%24 for i in range(hd1)])
        for id in range(dy1):
          days[id,:]=md3[id]+hrs[:]
        idx=days.flatten()
        ons[i,idx]=1.
#other sources
  fnameO=spe+'_ECP'+str(len(cp))+'_MDH'+str(len(mdh))+'_ONS.bin'
  with FortranFile(fnameO, 'w') as f:
    f.write_record(cp)
    f.write_record(mdh)
    f.write_record(ons)
