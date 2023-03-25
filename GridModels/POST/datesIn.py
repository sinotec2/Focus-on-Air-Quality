#kuang@dev2 /nas1/cmaqruns/2019base/data/wsites
#$ cat datesIn.py
#!/cluster/miniconda/envs/ncl_stable/bin/python
from pandas import *
import datetime
import subprocess
import fortranformat as ff

def rdA15(a):
  ii=-1
  for i in range(3):
    try:
      ai=int(a[i])
      ii=i
    except:
      break
  if ii<0:return 'fail'
  cum=0
  for i in range(0,ii+1):
    ai=int(a[i])
    cum+=ai*10**(ii-i)
  return cum

with open('abi_inp.txt','r') as f:
  l=[i.strip('\n') for i in f]
bdate,edate=[datetime.datetime.strptime(i,'%y%m%d%H') for i in l[1].split()[0:2]]

md=read_csv('MDL.csv')
md['dt']=[datetime.datetime.strptime(i+j[:2],'%Y-%m-%d%H') for i,j in zip(md.date,md.Time)]
md=md.loc[md.dt.map(lambda x: x >=bdate and x<=edate)].reset_index(drop=True)

yr=int(subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[-1][:2])
df=read_csv('ovm.dat_camxBAK',encoding='big5')
hd=df.columns[0].split()[:14]
DD={}
for c in range(14):
  srs=[i.split()[c] for i in df.iloc[:,0]]
  if c==1 or c==2:srs=[int(i) for i in srs]
  if c>2:srs=[float(i) for i in srs]
  DD.update({hd[c]:srs})
ob=DataFrame(DD)
ob['dt']=[datetime.datetime.strptime(str(yr*1000000+i),'%y%m%d%H') for i in ob.CalDat]
ob=ob.loc[ob.dt.map(lambda x: x >=bdate and x<=edate)].reset_index(drop=True)
ob['siteid']=[rdA15(a) for a in ob[hd[0]]]
stll=read_csv('/nas1/cmaqruns/2016base/data/sites/sta_ll.csv')
old={i:j for i,j in zip(stll.ID,stll.Old)}
ob[hd[0]]=[old[i] for i in ob['siteid']]

ints=set(md.siteid).intersection(set(ob.siteid))
md=md.loc[md.siteid.map(lambda x:x in ints)].reset_index(drop=True)
md.set_index('siteid').to_csv('MDL.csv')

ob=ob.loc[ob.siteid.map(lambda x:x in ints)].reset_index(drop=True)
head=' '+str(len(ints))+' JuliHr CalDat    SO2    CMO    OZN    PMT    NOX    P25    NO2    THC    NMH    WSP    WDR\n'
fmt300='I3,A12,I8,I7,7F7.1,4F8.1/'
w_line = ff.FortranRecordWriter(fmt300)
with open('ovm.dat_camx','w') as f:
  f.write(head)
  for i in range(len(ob)):
    i3=ob.loc[i,'siteid']
    a12=ob.loc[i,hd[0]].replace(str(i3),'')[:12]
    f.write(w_line.write([i3]+[ob.loc[i,c] for c in hd[:]]))
