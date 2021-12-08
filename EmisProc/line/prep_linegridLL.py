import numpy as np
from pandas import *
import twd97
from pyproj import Proj
from scipy.io import FortranFile

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

df=read_csv('TEDS11_LINE_WGS84.csv')
APOL=[i for i in df.columns if 'EM_' in i]
APOL.sort()
NPOL=len(APOL)
LTYP=len(set(df.NSC_SUB))
VTYPE=list(set(df.NSC))
VTYPE.sort()
NVTYP=len(VTYPE)
iVTYP=np.array([VTYPE.index(i) for i in df.NSC],dtype=int)


lon,lat=np.array(df.WGS84_E),np.array(df.WGS84_N)
x,y=pnyc(lon,lat, inverse=False)
df['UTME']=x+Xcent
df['UTMN']=y+Ycent
X=np.array([int(i/1000) for i in df.UTME],dtype=int)
Y=np.array([int(i/1000) for i in df.UTMN],dtype=int)
R=np.array(df.NSC_SUB,dtype=int)
C=np.array([i//100 for i in df.DICT],dtype=int)
XYRC=X*10000*10*100+Y*10*100+R*100+C
df['XYRC']=XYRC
DD={}
for s in 'XYRC':
  exec('DD.update({"'+s+'":'+s+'})')
kin=DataFrame(DD)
kin.drop_duplicates(inplace=True)
kin=kin.reset_index(drop=True)
XYRCk=list(kin.X*10000*10*100+kin.Y*10*100+kin.R*100+kin.C)
kin.set_index('X').to_csv('df_kin.csv')
NREC=len(kin)
df['REC']=-1
for i in range(NREC):
  boo=df.XYRC==XYRCk[i]
  idx=df.loc[boo].index
  df.loc[idx,'REC']=i
if len(df.loc[df.REC==-1]) !=0:sys.exit('wrong REC!')
df['RECV']=np.array(df.REC,dtype=int)*100+iVTYP
pv=pivot_table(df,index='RECV',values=APOL,aggfunc=sum).reset_index()
pv.set_index('RECV').to_csv('TEDS11_LINE_WGS84_1Km.csv')
pv['REC']=np.array(pv.RECV//100,dtype=int)
pv['iVT']=np.array(pv.RECV%100,dtype=int)
EM=np.zeros(shape=(NREC,NPOL,NVTYP))
for i in range(NREC):
  boo=(pv.REC==i)
  EM[i,:,:]=np.array(pv.loc[boo,APOL]).T
fname = 'cl08_'+'{:d}_{:d}_{:d}'.format(NREC,NPOL,NVTYP)+'.bin'
with FortranFile(fname, 'w') as f:
  f.write_record(EM)

