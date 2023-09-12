#kuang@master /nas2/cmaqruns/2019TZPP/output/Annual/cwb_byTown
#$ cat stn_dotCWB.py
# coding="utf8"
from pandas import *
import numpy as np
import sys
import os
from datetime import datetime,timedelta

yr=sys.argv[1]

path='/home/backup/data/cwb/e-service/'
fname=path+'read_web/town_cwb.csv'
twn=read_csv(fname)
twn=twn.loc[twn.aq_st.map(lambda x:x!='0;')].reset_index(drop=True)
twn['stns']=[Series(list(set([i for i in j[:-1].split(';')]))) for j in twn.aq_st]
all_stn=set()
for i in twn.stns:
  all_stn|=set(i)


directory = path+yr+'/'
file_extension = '.csv'
fnames=[fname for fname in os.listdir(directory) if fname.endswith(file_extension)]
fnames.sort()
df=DataFrame({})
cols=['stn','ObsTime','RH']#,'Precp']
col2=['stn','ymd','RH']#,'Precp']
dt_old=datetime.strptime(yr+'0101','%Y%m%d')
for fname in fnames:
  try:
    dfi=read_csv(directory+fname)
  except:
    dfi=read_csv(directory+fname,encoding='big5')
  dfi['stn']=[i[:6] for i in dfi.stno_name]
  dfi.ObsTime=np.array(dfi.ObsTime,dtype=int)
  dfi=dfi[cols]
  dfi=dfi.dropna(axis=0).reset_index(drop=True)
  if len(dfi)==0:
    ymd=dt_old.strftime("%Y%m%d")
    dfi=df.loc[df.ymd==int(ymd)]
    ymd1=(dt_old+timedelta(days=1)).strftime("%Y%m%d")
    dfi['ymd']=int(ymd1)
  else:
    dfi['ymd']=dfi.ObsTime//100
  dfi=pivot_table(dfi,index=col2[:2],values=col2[2:],aggfunc=np.mean).reset_index()
  df=df.append(dfi[col2],ignore_index=True)
  dt_old=datetime.strptime(str(list(df.ymd)[-1]),'%Y%m%d')
#df=df.loc[df.RH>0].reset_index(drop=True)
s=set(df.stn)
new=s-all_stn
old=all_stn-s
col=df.columns[2:]

nt,ns,ni=len(set(df.ymd)),len(set(df.stn)),len(col)
var=np.zeros(shape=(ni,nt,ns))
if len(df)!=nt*ns:
#sys.exit('time or station data missing!')
  pv=pivot_table(df,index='ymd',values='stn',aggfunc='count').reset_index()
  ymd_ng=list(pv.loc[pv.stn!=ns,'ymd'])
  for i in ymd_ng:
    ss=set(list(df.loc[df.ymd==i,'stn']))
    for j in s-ss:
      df1=DataFrame({'ymd':[i],'stn':[j]})
      for c in col:
        df1[c]=np.nan
      df=df.append(df1,ignore_index=True)

df=df.sort_values(['ymd','stn']).reset_index(drop=True)
df=df.fillna(-999)
dta=df.values
m=0
for t in range(nt):
  var[:,t,:]=dta[m:m+ns,2:].T
  m+=ns
var = np.ma.masked_where(var<=0, var)

nw=len(twn)
twn=twn.sort_values(['TOWNCODE']).reset_index(drop=True)
seq=list(all_stn-old)
seq.sort()
seqn={seq[i]:i for i in range(len(seq))}
fac=np.zeros(shape=(ns,nw))
for t in range(nw):
  it=[i for i in twn.stns[t] if i in seqn]
  n=len(it)
  if n==0:
#    print twn.TOWNENG[t]
    continue #sys.exit('no stations in this town')
  for i in it:
    fac[seqn[i],t]=1./n
res=np.ma.dot(var,fac)

ymd=list(set(df.ymd));ymd.sort()
ymd=np.array(ymd,dtype=int)
one=np.ones(shape=(nw),dtype=int)
ymds=np.outer(ymd,one)
cod=list(set(twn.TOWNCODE));cod.sort()
cod=np.array(cod,dtype=int)
one=np.ones(shape=(nt),dtype=int)
cods=np.outer(one,cod)
dd=DataFrame({'ymd':ymds.flatten(),'TOWNCODE':cods.flatten()})
i=0
for c in col:
  dd[c]=res[i,:,:].flatten()
  dd.loc[dd[c]<=0,c]=np.nan
  i+=1
dd=dd.loc[dd.TOWNCODE>=0].reset_index(drop=True)
dd=dd.loc[dd.RH>0].reset_index(drop=True)
dd.set_index('ymd').to_csv(yr+'res.csv')
