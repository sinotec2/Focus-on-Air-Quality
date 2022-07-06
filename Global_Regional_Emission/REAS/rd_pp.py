#kuang@114-32-164-198 /Users/TEDS/REAS3.1
#$ cat ./origins/rd_pp.py
import sys
from pandas import *

fname=sys.argv[1]
spec=fname.replace('REASv3.1_','').replace('_POWER_PLANTS_POINT_2015','').replace('.','').replace('_','')
with open(fname,'r') as f:
  l=[i.strip('\n') for i in f]
lu=int(l[0])
if 'NMV' in spec:
  spec=l[1].split()[0]
  spec=spec.upper()
l=l[lu:]
if len(l)==0:
  sys.exit('no data for '+spec)
l=[i.split() for i in l]
col=['lon','lat']+['mon'+str(i) for i in range(1,13)]+['state']
d={}
for i in range(len(col)-1):
  d.update({col[i]:[float(l[j][i]) for j in range(len(l))]})
i=len(col)-1
d.update({col[i]:[l[j][i]for j in range(len(l))]})
df=DataFrame(d)
df['T/Y']=[sum([df.iloc[i,j] for j in range(2,len(col)-1)]) for i in range(len(df)) ]
df.set_index('lon').to_csv('point_all.csv')
idx=df[df['state']=='TWNWC'].index
print (idx,len(df))
df=df.drop(idx)
df=df.sort_values(['lon','lat'],ascending=True).reset_index(drop=True)
df.set_index('lon').to_csv('point_'+spec+'.csv')
