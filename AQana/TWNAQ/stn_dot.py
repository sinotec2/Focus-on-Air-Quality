#kuang@master /home/backup/data/epa/pys
#$ cat stn_dot.py
from pandas import *
import numpy as np
import sys

yr=sys.argv[1]

fname='/nas1/CAM-chem/Annuals/town_aqstEnew.csv'
twn=read_csv(fname)
twn=twn.loc[twn.aq_st.map(lambda x:'0;' not in x)].reset_index(drop=True)
twn['stns']=[Series([int(i) for i in j[:-1].split(';')]) for j in twn.aq_st]
all_stn=[]
for i in twn.stns:
  if len(i)==0:continue
  a=all_stn+list(i)
  all_stn=list(set(a))
all_stn=set(all_stn)

df=read_csv(yr+'.csv')
df.stn=[int(i) for i in df.stn]
col=df.columns[2:]
s=set(df.stn)

new=s-all_stn
old=all_stn-s
if len(old)>0:
    print(old)

if len(new)>0:
  df=df.loc[df.stn.map(lambda x:x not in new)].reset_index(drop=True)
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
var = np.ma.masked_where(var< 0, var)

nw=len(twn)
twn=twn.sort_values(['new_code']).reset_index(drop=True)
seq=list(all_stn-old)
seq.sort()
seqn={seq[i]:i for i in range(len(seq))}
fac=np.zeros(shape=(ns,nw))
for t in range(nw):

  n=len(twn.stns[t])
  if n==0:sys.exit('no stations in this town')
  for i in twn.stns[t]:
    if i in old:continue
    fac[seqn[i],t]=1/n
res=np.ma.dot(var,fac)

ymd=list(set(df.ymd));ymd.sort()
ymd=np.array(ymd,dtype=int)
one=np.ones(shape=(nw),dtype=int)
ymds=np.outer(ymd,one)
cod=list(set(twn.new_code));cod.sort()
cod=np.array(cod,dtype=int)
one=np.ones(shape=(nt),dtype=int)
cods=np.outer(one,cod)
dd=DataFrame({'ymd':ymds.flatten(),'TOWNCODE':cods.flatten()})
i=0
for c in col:
  dd[c]=res[i,:,:].flatten()
  dd.loc[dd[c]<0,c]=np.nan
  i+=1
dd=dd.loc[dd.TOWNCODE>=0].reset_index(drop=True)
dd.set_index('ymd').to_csv(yr+'res.csv')
