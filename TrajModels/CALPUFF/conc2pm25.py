import numpy as np
import os,sys,subprocess
from pandas import *
CSPEC='SO2 SO4 NOX HNO3 NO3 PMS1 PMS2 PMS3'.split()
# 由目錄中讀取所有concrec*.dat檔名。檔名是成分與時間的矩陣
fnames=list(subprocess.check_output('ls concrec*dat',shell=True).split(b'\n'))
fnames=[i.decode('utf8') for i in fnames if len(i)>0 ]
if len(fnames)==0:sys.exit('concrec not found')
#行數
wc=int(subprocess.check_output('cat '+fnames[0]+'|wc -l',shell=True).split(b'\n')[0])
#時間
jt=[int(fname.split('/')[-1].replace('.dat','')[-4:]) for fname in fnames if len(fname)>0]
#成分
js=[int(fname.split('/')[-1].replace('.dat','')[-6:-4]) for fname in fnames if len(fname)>0]
df=DataFrame({'hr':jt,'spec':js,'fname':fnames})
df=df.loc[df.spec>0].reset_index(drop=True)

#將所有檔案內容讀進來，存到矩陣C
C=np.zeros(shape=(max(js)+1,max(jt)+1,wc))
for i in range(len(df)):
  with open(df.loc[i,'fname'],'r') as f:
    tmp=[float(l.strip('\n')) for l in f]
  C[df.loc[i,'spec'],df.loc[i,'hr'],:]=tmp[:]

#分列各項污染物  
so4 =C[1,:,:]
hno3=C[3,:,:]
no3 =C[4,:,:]
p25 =C[5,:,:]
#計算結合銨鹽的重量，並重新計算所有PMF顆粒重量
nh4=so4*(36./96.)+no3*(18./62.)+hno3*(18./63.)
total=so4+no3+hno3+nh4+p25

#輸出結果
fnRoot=fnames[0].replace('.dat','')[:-6]+'00'
for it in range(1,max(jt)+1):  
  fname=fnRoot+'{:04d}'.format(it)+'.dat'
  with open(fname,'w') as f:
    for ic in range(wc):
      f.write(str(total[it,ic])+'\n')
