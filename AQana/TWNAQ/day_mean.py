#kuang@master /home/backup/data/epa/pys
#$ cat daymean.py
from pandas import *
import sys, os, subprocess
import numpy as np
import math


def vec_mean(ws,wd):
  idx=np.where(wd==888)
  if len(idx[0]>0):ws[idx]=0
  wd_rad = np.radians(wd)
  wx = ws * np.cos(wd_rad)
  wy = ws * np.sin(wd_rad)
  wx_avg = np.mean(wx)
  wy_avg = np.mean(wy)
  mean_wd_rad = math.atan2(wy_avg, wx_avg)
  mean_wd_deg = np.degrees(mean_wd_rad)
  if mean_wd_deg < 0: mean_wd_deg+=360
  mean_ws = np.mean(ws)
  return mean_ws, mean_wd_deg

root='/home/backup/data/epa/'
marks=['      ','******']
fname=root+'item2.txt'#items of EPA monitoring stations
with open(fname,'r') as ftext:
  itm=[line.strip('\n') for line in ftext]
ditm={i:itm[i] for i in range(len(itm))}
nitm={ditm[i]:i for i in ditm if ditm[i] !='dum'}
wswd=[nitm['WIND_SPEED'],nitm['WIND_DIREC']]

yr=sys.argv[1]
fnames=subprocess.check_output('ls '+root+yr+'/HS*.???',shell=True).decode('utf8').split('\n')[:-1]
fnames=[f for f in fnames if f[-3] in '01']

df=DataFrame({'ymd':[],'stn':[]})
for c in itm:
  if c=='dum':continue
  df[c]=0
for fname in fnames:
  with open(fname,'r') as f:
    fn=[line for line in f]
  if len(fn)==0:continue
  if ',' not in fn[0]:
    itms,ymds=(np.array([int(line.split()[j]) for line in fn],dtype=int) for j in [1,2])
    cons=np.array([np.array([i.strip('\n') for i in line.split(',')[3:]], dtype=str) for line in fn])
  else:
    n=3
    itms,ymds=(np.array([int(line.split(',')[j]) for line in fn],dtype=int) for j in [2,3])
    cons=np.array([np.array([i.strip('\n') for i in line.split(',')[4:]], dtype=str) for line in fn])
  if ymds.mean()<20000000:ymds+=20000000
  for m in marks:
    cons=np.where(cons==m,'-999',cons)
  cons=np.array(cons,dtype=float)
  masked = np.ma.masked_where(cons< 0, cons)
  cons=masked.mean(axis=1)
  dd=DataFrame({'ymds':ymds,'itms':itms,'con':cons})
  s_ymds=list(set(ymds))
  s_ymds.sort()
  for ymd in s_ymds:
    iws,iwd=(dd.loc[(dd.ymds==ymd) & (dd.itms==i)].index.values for i in wswd)
    dd.loc[iws,'con'],dd.loc[iwd,'con']=vec_mean(masked[iws,:],masked[iwd,:])
  dd=dd.sort_values('ymds').reset_index(drop=True)
  di=DataFrame({'ymd':s_ymds})
  di['stn']=int(fname[-3:])
  for c in itm:
    if c=='dum':continue
    val=list(dd.loc[dd.itms==nitm[c],'con'])
    if len(val)!=len(di):continue
    di[c]=val
  df=df.append(di,ignore_index=True)
df.set_index('ymd').to_csv(yr+'.csv')
