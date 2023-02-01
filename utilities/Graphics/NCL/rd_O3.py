#kuang@master ~/NCL_scripts/rcm_2
#$ cat rd_O3.py
from pandas import *
import json
import os, sys, datetime
def nstnam():
  import json
  fn = open('/home/backup/data/epa/pys/sta_list.json')
  d_nstnam = json.load(fn)
  d_namnst = {d_nstnam[k]: k for k in list(d_nstnam)}
  return (d_nstnam, d_namnst)

d_nstnam, d_namnst=nstnam()
#arg: YYYYMMDDHH
ymdh=sys.argv[1]
adate=ymdh[:-2]
bdate=datetime.datetime.strptime(adate,'%Y%m%d')
edate=bdate+datetime.timedelta(days=1)
adate2=edate.strftime("%Y%m%d")
os.system('/usr/kbin/specHrSliderRect.py -t EPA_ALL -s O3 -a s -b '+adate+' -e '+adate2)
fname='EPA_ALL'+adate+adate2+'.csv'
df=read_csv(fname)
dfs=df.loc[df.YMDH==int(ymdh)].reset_index(drop=True)

fname='/nas1/cmaqruns/2019base/data/wsites/sta_ll.csv'
dfLL=read_csv(fname)
dfLL.loc[78,'ID']=82
dfLL.loc[78,'New']='lulinshan'
dfLL.loc[78,'Old']='lulinshan'
dfLL.loc[78,'lat']=23.47194791586524
dfLL.loc[78,'lon']=120.88155513844625
Dlat, Dlon ={i:j for i,j in zip(dfLL.ID,dfLL.lat)} ,{i:j for i,j in zip(dfLL.ID,dfLL.lon)}
dfs['lat']=[Dlat[int(d_namnst[i])] for i in list(dfs.nam)]
dfs['lon']=[Dlon[int(d_namnst[i])] for i in list(dfs.nam)]
col='lat,lon,O3'.split(',')
dfs[col].set_index('lat').to_csv('EPA_ALL'+ymdh+'.csv',header=None)
