
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
P=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n')+'/'
teds=int(P.split('/')[3][-2:])
yr=2016+(teds-10)*3
ndays=365
if yr%4==0:ndays=366
s365=set([i*24 for i in range(ndays)])
nhrs=ndays*24

Hs=10 #cutting height of stacks
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
#sys.exit(str(len(df)))
df['SUM']=[i+j+k+l+m for i,j,k,l,m in zip(df.SOX_EMI,df.NOX_EMI,df.CO_EMI,df.PM_EMI,df.NMHC_EMI)]
df=df.loc[df.SUM>0].reset_index(drop=True)
df['CP_NO'] = [i + j for i, j in zip(list(df['C_NO']), list(df['NO_S']))]
df['DY1']=[i*j for i,j in zip(df.DW1,df.WY1)]
df['HY1']=[i*j for i,j in zip(df.HD1,df.DY1)]

#71 factories with CEMS will emit (at ground) when stacks are operating
fname=P+'point_cems.csv'
cems=read_csv(fname)
val='SOX PM NOX FLOW X_BLANK1 X_BLANK2'.split()
nval=len(val)
if 'CP_NO' not in cems.columns: #pre-process
  cems=cems.drop(cems.loc[cems.C_NO=='C_NO'].index).reset_index(drop=True)
  cems['CP_NO'] = [i + j for i, j in zip(list(cems['C_NO']), list(cems['NO_S']))]
  cems['PM']=[(i+j)/2 for i,j in zip(cems.SOX,cems.NOX)]
  if max(cems.HOUR)>100:
    cems['MDH']=[int(i*10000+j*100+k/100) for i,j,k in zip(cems.MONTH,cems.DATE,cems.HOUR)]
  else:
    cems['MDH']=[int(i*10000+j*100+k) for i,j,k in zip(cems.MONTH,cems.DATE,cems.HOUR)]
  cems=pivot_table(cems,index=['CP_NO','MDH'],values=val,aggfunc=sum).reset_index()
  #cems(df) convert to cemsM(matrix)
  for MC in ['CP_NO','MDH']:
    mc=MC.lower()
    exec(mc+'=list(set(cems.'+MC+'))');exec(mc+'.sort()')
    exec('n'+MC+'=len('+mc+')')
    exec('d'+MC+'={'+mc+'[i]:i for i in range(n'+MC+')}')
    exec('cems["i'+MC+'"]=[d'+MC+'[i] for i in cems.'+MC+']')
  if len(mdh)!=ndays*24:sys.exit('mdh coverage not enough!')
  cemsM=np.zeros(shape=(nMDH,nCP_NO,nval))
  for i in range(nval):
    cemsM[cems.iMDH[:],cems.iCP_NO[:],i]=cems[val[i]]
  DD={}
  for i in range(nval):
    DD[val[i]]=cemsM[:,:,i].flatten()
  DD['MDH']  =[i for i in mdh for j in cp_no]
  DD['CP_NO']=[j for i in mdh for j in cp_no]
  cems=DataFrame(DD)
  cems['C_NO']=[i[:8] for i in cems.CP_NO]
  cems['MD']=[i//100 for i in cems.MDH]
  cems.set_index('CP_NO').to_csv(fname)

for MC in ['CP_NO','MDH','MD','C_NO']:
  mc=MC.lower()
  exec(mc+'=list(set(cems.'+MC+'))');exec(mc+'.sort()')
  exec('n'+MC+'=len('+mc+')')

#Hour of Day pattern
cems['HR']=[i%100 for i in cems.MDH]
pv_cems1=pivot_table(cems,index=['C_NO','HR'],values='SOX',aggfunc=sum).reset_index()

cems_HROD=DataFrame({'C_NO':c_no})
cems_HROD['SOX_HR_ODER']=0
for ic in cems_HROD.index:
  pv1=pv_cems1.loc[pv_cems1.C_NO==c_no[ic]]
  pv3=pv1.sort_values('SOX',ascending=False).reset_index(drop=True)
  cems_HROD.loc[ic,'SOX_HR_ODER']=''.join(['{:d} '.format(i) for i in pv3.HR])
#orders for DY1  
pv_cems2=pivot_table(cems,index=['C_NO','MD'],values='FLOW',aggfunc=sum).reset_index()
#Indexing is an exhaustive process.
iMD=[mdh.index(i*100) for i in pv_cems2.MD] #change the MMDD into index sequence among MMDD00's
pv_cems2.MD=iMD
cems_DAOD=DataFrame({'C_NO':c_no})
cems_DAOD['FLOW_DA_ODER']=0
for ic in cems_DAOD.index:
  pv1=pv_cems2.loc[pv_cems2.C_NO==c_no[ic]]
  pv3=pv1.sort_values('FLOW',ascending=False).reset_index(drop=True)
  cems_DAOD.loc[ic,'FLOW_DA_ODER']=''.join(['{:d} '.format(i) for i in pv3.MD])

dfxy=pivot_table(df,index='C_NO',values=['UTM_E','UTM_N'],aggfunc=np.mean).reset_index() 

#booleans for pollutant selection
boo1=df.NMHC_EMI>0
boo2=(df.SOX_EMI+df.NOX_EMI+df.CO_EMI+df.PM_EMI)>0
BLS={'NMHC':boo1,'SNCP':boo2}
lsp={'NMHC':['NMHC_EMI'],'SNCP':'SOX_EMI,NOX_EMI,CO_EMI,PM_EMI'.split(',')}
colT=['HD1','DY1','HY1']
col=['C_NO','CP_NO','HD1','DY1','HY1']+[i for i in df.columns if 'EMI' in i]
for spe in [s for s in [sys.argv[1]] if s in BLS]:
  dfV=df[col].loc[BLS[spe]].reset_index(drop=True)
  dfV1=pivot_table(dfV,index='CP_NO',values=lsp[spe],aggfunc=sum).reset_index()
  dfV2=pivot_table(dfV,index='CP_NO',values=colT,aggfunc=np.mean).reset_index()
  dfV=merge(dfV1,dfV2,on='CP_NO')
  dfV['C_NO']=[i[:8] for i in dfV.CP_NO]
  for c in colT:
    dfV[c]=np.array(dfV[c],dtype=int)
  a,b=list(set(dfV.C_NO)),list(set(cems.C_NO));a.sort();b.sort()
  ab=[i for i in a if i in b]
  cp=list(set(dfV.CP_NO))
  cp.sort()
  ons=np.zeros(shape=(len(cp),len(mdh)),dtype=int)
  #other fatories without CEMS, take the nearest one
  b1=set(b)-set(dfxy.C_NO) #cems factory but without UTM location
  c1=[c for c in b if c not in b1 and c in a] #cems plant with X,Y
  cemsX=np.array([list(dfxy.loc[dfxy.C_NO==c,'UTM_E'])[0] for c in c1])
  cemsY=np.array([list(dfxy.loc[dfxy.C_NO==c,'UTM_N'])[0] for c in c1])
  #loop for every factories
  for c in [i for i in a if i not in b1]:
    c_cems=c
    if c not in ab:
      x0,y0=list(dfxy.loc[dfxy.C_NO==c,'UTM_E'])[0],list(dfxy.loc[dfxy.C_NO==c,'UTM_N'])[0]
      dist=(cemsX-x0)**2+(cemsY-y0)**2
      idx=list(dist).index(min(dist))
      c_cems=c1[idx]
    pv2MD=np.array(list(cems_DAOD.loc[cems_DAOD.C_NO==c_cems,'FLOW_DA_ODER'])[0].split(),dtype=int)
    if len(pv2MD)<ndays: pv2MD=np.array(list(pv2MD)+list(s365-set(pv2MD)))
    df_cp=dfV.loc[dfV.C_NO==c].reset_index(drop=True)
    #loop for every NO_S in this factory
    for p in set(df_cp.CP_NO):
      ip=cp.index(p)
      dy1=dfV.DY1[ip]
      hd1=dfV.HD1[ip]
      md3=pv2MD[:dy1] 
      days=np.zeros(shape=(dy1,hd1),dtype=int)
      if hd1==24:
        hrs=np.array([ih for ih in range(24)],dtype=int)
      else:
        first=np.array(list(cems_HROD.loc[cems_HROD.C_NO==c_cems,'SOX_HR_ODER'])[0].split(),dtype=int)[0]
        hrs=np.array([(first+ih)%24 for ih in range(hd1)])
      for id in range(dy1):
        days[id,:]=md3[id]+hrs[:]
      idx=days.flatten()
      ons[ip,idx]=1
#other sources
  fnameO=spe+'_CP'+str(len(cp))+'_MDH'+str(len(mdh))+'_ONS.bin'
  with FortranFile(fnameO, 'w') as f:
    f.write_record(cp)
    f.write_record(mdh)
    f.write_record(ons)
