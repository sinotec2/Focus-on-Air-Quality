#!coding=utf8
import numpy as np
from pandas import *
import subprocess
import json
from datetime import datetime, timedelta
import sys, os

# read the time variation factors
csvs={'m':'mon.csv','w':'week.csv','d':'day.csv'}
for t in 'mwd':
  df='df_A'+t
  try:
    exec(df+'=read_csv("'+df+'")')
  except:  
    sys.exit('df_A? not found, please re-run prep_dfAdmw.py ') 

#union of nsc2 in time variation files
s_nsc2=set(df_Ad.nsc2) | set(df_Am.nsc2) | set(df_Aw.nsc2)

#open the TEDS area csv file
pwd=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n')
teds=pwd.split('/')[3][4:6]
fname='areagrid'+teds+'LL.csv'
df = read_csv(fname)
df.drop_duplicates(inplace=True)
df=df.reset_index(drop=True)
if 'nsc2' not in df.columns:
  df.loc[df['NSC_SUB'].map(lambda x: (type(x)==float and np.isnan(x)==True) or ( x==' ')),'NSC_SUB']='b'
  df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
if 'CNTY' not in df.columns:
  df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]

#definition the coordinates of database
minx,miny=min(df.UTME),min(df.UTMN)
df.UTME=round(df.UTME-minx,-3)
df.UTMN=round(df.UTMN-miny,-3)
df['YX']=np.array(df.UTMN+df.UTME/1000,dtype=int)

#sum-up the grids which length maybe smaller than 1KM
cole=['EM_SOX','EM_NOX','EM_CO','EM_PM25','EM_PM','EM_NMHC']
coli=['CNTY', 'nsc2','YX']
df=pivot_table(df,index=coli,values=cole,aggfunc=np.sum).reset_index()
#nXXX:len of list XXX; dXXX:index dictionary of listXXX, iXXX:index of XXX
for c in ['CNTY','nsc2','YX']:
  exec(c+'=list(set(df.'+c+'))')
  exec(c+'.sort()')
  exec('n'+c+'=len('+c+')')
  exec('d'+c+'={'+c+'[i]:i for i in range(n'+c+')}')
  exec('df["i'+c+'"]=[d'+c+'[i] for i in df.'+c+']')

#
nsc2b=set([i for i in s_nsc2 if i[-1]=='b'])
for ii in nsc2b-set(df.nsc2):
  i=int(ii[:-1])
  s_nsc2=s_nsc2|set(df.loc[df.nsc2.map(lambda x:x[:-1]==i),'nsc2'])
#Tuple_of_Length ={0, 101, 10000, 10101, 131313, 171717, 202020, 212121, 250101}
n_rgn,s_rgn,d_rgn={},[],{}
for n in s_nsc2:
  tl_rgn=(len(df_Am[df_Am.nsc2==n])*100+len(df_Aw[df_Aw.nsc2==n]))*100+len(df_Ad[df_Ad.nsc2==n])
  s_rgn.append(tl_rgn)
  n_rgn[n]=tl_rgn
  d_rgn[tl_rgn]=n #recording last nsc2 for calling
s_rgn=set(s_rgn) #tuple of region numbers

yr=2016+(int(teds)-10)*3
bdate=datetime(yr,1,1)-timedelta(days=1)
nd365=365+2
if yr%4==0:nd365=366+2
nty=nd365*24
dts=[bdate+timedelta(days=i/24.) for i in range(nty)]

#n_cnty: the dictionary of nsc2 vs cnties applied
if os.path.exists('n_cnty.json'):
  with open('n_cnty.json', 'r', newline='') as jsonfile:
    n_cnty=json.load(jsonfile)
else:
  for kc in ['cnty','kpq']:
    jsname='d_'+kc+'.json'
    if os.path.exists(jsname):
      with open(jsname, 'r', newline='') as jsonfile:
        exec('d_'+kc+'=json.load(jsonfile)')
    else:
      sys.exit('d_'+kc+'.json not found, please re-run prep_dfAdmw.py ') 
  n_cntys={}
  for tl in s_rgn: #tuple of lengs
    n=d_rgn[tl]
    cntys=[]
    for t in 'mwd':
      exec('regs=list(df_A'+t+'.loc[df_A'+t+'.nsc2==n,"REGION"])')
      if len(regs)==0:continue
      for r in regs:
        if r in d_kpq:
          cntys+=[d_cnty[i] for i in d_kpq[r]]
        else:
          cntys+=[d_cnty[r]]
    cntys=list(set(cntys))
    for n in [i for i in n_rgn if n_rgn[i]==tl]:
      n_cntys[n]=cntys
  with open('n_cnty.json', 'w', newline='') as jsonfile:
    json.dump(n_cntys, jsonfile)


if not os.path.exists('nc_fac.json'):
  mns=np.array([dts[i].month-1 for i in range(nty)])
  wks=np.array([dts[i].weekday() for i in range(nty)])
  hrs=np.array([dts[i].hour for i in range(nty)])

  nts={'m':12,'w':7,'d':24}
  for t in 'mwd':
    exec('df_A=df_A'+t)
    df=DataFrame({})
    df_A['CNTY']=0
    for i in range(len(df_A)):
      cntys=[]
      a=df_A.loc[i]
      r=df_A.loc[i,'REGION']
      if r in d_kpq:
        cntys+=[d_cnty[i] for i in d_kpq[r]]
      else:
        cntys+=[d_cnty[r]]
      for c in cntys:
        a.CNTY=c
        df=df.append(a,ignore_index=True)
    f_A={}
    for j in range(len(df)):
      n=df.loc[j,'nsc2']
      c=df.loc[j,'CNTY']
      f_A[(n,c)]=[df.loc[j,str(i)] for i in range(1,nts[t]+1)]
    exec('f_A'+t+'=f_A')
  for i in set(f_Am)-set(f_Aw):
    f_Aw[i]=np.ones(shape=7)  
  for i in set(f_Am)-set(f_Ad):
    f_Ad[i]=np.ones(shape=24)

  nc_fac={}
  for n in s_nsc2:
    for c in n_cntys[n]:
      tup=(n,c)
      tp=n+'_'+c
      if tup not in f_Am:continue
      lfac=np.array([f_Am[tup][m]*f_Aw[tup][w]*f_Ad[tup][d] for m,w,d in zip(mns,wks,hrs)])
      sfac=sum(lfac)
      nc_fac[tp]=list(lfac/sfac)

  with open('nc_fac.json', 'w', newline='') as jsonfile:
    json.dump(nc_fac, jsonfile)

