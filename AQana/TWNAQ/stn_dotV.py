#/nas2/cmaqruns/2022fcst/fusion/Voronoi
#$ cat stn_dotV.py
import pandas as pd
import geopandas as gpd
import numpy as np
import sys

yr=sys.argv[1]

llv=pd.read_csv('/nas2/cmaqruns/2022fcst/fusion/Voronoi/gridLLvor.csv')
nxy=393*276
if len(llv)!=nxy:sys.exit('wrong grid matching')
all_stn=set(list(llv.AQID))
ns=len(all_stn)
seq=list(all_stn)
seq.sort()
seqn={seq[i]:i for i in range(ns)}
fac1=np.zeros(shape=(ns,nxy))
for t in range(nxy):
  i=llv.AQID[t]
  fac1[seqn[i],t]=1.

root='/home/backup/data/epa/pys/'
df=pd.read_csv(root+yr+'.csv')
df.stn=[int(i) for i in df.stn]
col=df.columns[2:]
s=set(df.stn)

out=s-all_stn
new=all_stn-s
if len(new)>0:
    print(new)

if len(out)>0:
  df=df.loc[df.stn.map(lambda x:x not in out)].reset_index(drop=True)
  s=all_stn
nt,ni=len(set(df.ymd)),len(col)
var=np.zeros(shape=(ni,nt,ns))
if len(df)!=nt*ns:
#sys.exit('time or station data missing!')
  pv=pd.pivot_table(df,index='ymd',values='stn',aggfunc='count').reset_index()
  ymd_ng=list(pv.loc[pv.stn!=ns,'ymd'])
  for i in ymd_ng:
    ss=set(list(df.loc[df.ymd==i,'stn']))
    for j in s-ss:
      df1=pd.DataFrame({'ymd':[i],'stn':[j]})
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
res1=np.ma.dot(var,fac1)

sw=set(llv.TOWNCODE)
nw=len(sw)
seq=list(sw)
seq.sort()
seqn={seq[i]:i for i in range(nw)}
fac2=np.zeros(shape=(nxy,nw))
for t in range(nw):
  a=llv.loc[llv.TOWNCODE==seq[t]]
  n=len(a)
  for i in a.index:
    fac2[i,t]=1./n

res=np.ma.dot(res1,fac2)

ymd=list(set(df.ymd));ymd.sort()
ymd=np.array(ymd,dtype=int)
one=np.ones(shape=(nw),dtype=int)
ymds=np.outer(ymd,one)
cod=np.array(seq,dtype=int)
one=np.ones(shape=(nt),dtype=int)
cods=np.outer(one,cod)
dd=pd.DataFrame({'ymd':ymds.flatten(),'TOWNCODE':cods.flatten()})
i=0
for c in col:
  dd[c]=res[i,:,:].flatten()
  dd.loc[dd[c]<0,c]=np.nan
  i+=1
dd=dd.loc[dd.TOWNCODE>0].reset_index(drop=True)
dd.set_index('ymd').to_csv(yr+'Vor.csv')
