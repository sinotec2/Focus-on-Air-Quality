#kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
#$ cat km.py
import os, sys
import netCDF4
import twd97
from pandas import *
import bisect
import numpy as np
from sklearn.cluster import KMeans

txt=sys.argv[1]
nclt=int(sys.argv[2])
with open(txt, 'r') as f:
    fnames=[l.strip('\n') for l in f]
idx=fnames[0].index('20')
#ymdh=np.array([int(i[idx:idx+10]) for i in fnames],dtype=int)
#if len(ymdh)!=len(fnames):sys.exit('wrong length in ymdh')

trjs=np.zeros(shape=(len(fnames),20))
tex=10000
n,m=0,0
ymdh=[]
for fname in fnames:
  try:
    df=read_csv(fname+'10.csv')
  except:
    m=m+1
    continue
  trjs[n,:10]=[i//tex for i in df.JI3]
  trjs[n,10:]=[i%tex for i in df.JI3]
  ymdh.append(int(fname[idx:idx+10]))
  n+=1
trjs=trjs[:-m,:]
clt = KMeans(n_clusters = nclt)

clt.fit(trjs)
a=clt.labels_
dfa=DataFrame({'lab':a,'ymdh':ymdh})
dfa.set_index('lab').to_csv('lab.csv')

ji=np.array(clt.cluster_centers_,dtype=int)
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
nc = netCDF4.Dataset('/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_3km.nc','r')
x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
for l in range(nclt):
  des=['Line'+str(l)+'_'+str(i) for i in range(10)]
  df=DataFrame({'TWD97_x':[Xcent+x_mesh[i] for i in ji[l,10:]],'TWD97_y':[Ycent+y_mesh[i] for i in ji[l,:10]],'lab':des,'des':des})
  df.set_index('TWD97_x').to_csv('res'+str(l)+'.csv')
os.system('for i in {0..'+str(nclt-1)+'};do cp res$i.csv res${i}L.csv;done')
os.system('for i in {4..'+str(nclt-1)+'};do csv2kml.py -f res$i.csv -g TWD97 -n RL;done')
os.system('for i in {2..3};do csv2kml.py -f res$i.csv -g TWD97 -n HL;done')
os.system('for i in {0..1};do csv2kml.py -f res$i.csv -g TWD97 -n NL;done')
