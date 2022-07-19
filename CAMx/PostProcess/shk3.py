#kuang@master ~/bin
#$ cat shk3.py
#!/cluster/miniconda/envs/py37/bin/python
#encoding=utf-8
from PseudoNetCDF.camxfiles.Memmaps import uamiv
import numpy as np
import sys,os
from pandas import *
from scipy.io import FortranFile
import datetime

def YMD2YJ(nowd):
  yr=nowd/100/100
  i=datetime.datetime(nowd/100/100,nowd/100%100,nowd%100)
  return yr*1000+int(str((i-datetime.datetime(yr,1,1)).days).split()[0])+1

if (len(sys.argv) == 1):
  print "usage: shk uamiv_file"
  sys.exit(1)
elif: sys.argv[1] == '-h' or sys.argv[1] == '--help':
  print "usage: shk uamiv_file"
  sys.exit(1)

YMDH='20'+sys.argv[1][:8]
yjh=YMD2YJ(int(YMDH[:-2]))*100+int(YMDH[-2:])
df=read_csv('/home/backup/data/epa/pys/2013ByMonth/'+YMDH[:4]+'IJ4.csv')
df=df.loc[df.YJH==yjh].reset_index(drop=True)
SPNAMs=['CO', 'NO2',  'O3', 'SO2','NMHC','PM10', 'PM2.5']

os.system('cp '+sys.argv[1]+'.finst '+sys.argv[1]+'R.finst')
path=sys.argv[1]+'R.finst'
con_file= uamiv(path,'r+')
v4=list(filter(lambda x:con_file.variables[x].ndim==4, [i for i in con_file.variables]))
nt,nlay,nrow,ncol=con_file.variables[v4[0]].shape
for SPNAM in SPNAMs[:4]:
  for i in range(len(df)):
    val=df.loc[i,SPNAM]
    if np.isnan(val):continue
    if val<=0.:continue
    II,JJ=df.loc[i,'IJ']/1000,df.loc[i,'IJ']%1000
    con_file.variables[SPNAM][0,0,JJ,II]=val

#definition of NMHC species in shk
sVOCs=' AACD ACET ALD2 ALDX BENZ CRES ETH  ETHA ETHY ETOH \
        FACD FORM GLYD INTR IOLE ISOP ISP  ISPD KET  MEOH \
        MEPX MGLY NTR  OLE  OPEN PACD PAN  PAR  PANX PRPA \
        TOL  TOLA TERP TRP  XYL  XYLA'.split()
num_C=[ 0.,  0.,  2.,  0.,  6.,  0.,  4.,  0.,  0.,  0., \
                  0.,  1.,  0.,  0.,  2.,  5.,  5.,  0.,  3.,  0., \
                  0.,  0.,  0.,  2.,  0.,  0.,  3., 0.5,  0.,  0., \
                  7.,  0., 10.,  0.,  8.,  0.]
v2c={i:j for i,j in zip(sVOCs,num_C)}
for SPNAM in SPNAMs[4:5]:
  for i in range(len(df)):
    val=df.loc[i,SPNAM]
    if np.isnan(val):continue
    II,JJ=df.loc[i,'IJ']/1000,df.loc[i,'IJ']%1000
    vocs=0
    for sp in sVOCs:
      if sp not in v4:continue
      vocs+=con_file.variables[sp][0,0,JJ,II]*v2c[sp]
    if vocs==0.:
      for sp in sVOCs:
        if sp not in v4:continue
        con_file.variables[sp][0,0,JJ,II]=val/len(sVOCs) #divided evenly
    else:
      for sp in sVOCs:
        if sp not in v4:continue
        if v2c[sp]==0:continue
        con_file.variables[sp][0,0,JJ,II]=con_file.variables[sp][0,0,JJ,II]/vocs*val/v2c[sp]

with open('/nas1/camxruns/2013_enKF/inputs/part.txt','r') as f:
    part=[line.strip('\n').split()[1] for line in f]
part3sp='CPRM CCRS PH2O'.split()
fpm2_5=[0.58,0.85,0.774]+[1.]*10+[0.,0]+[0.312]*2+[0]
sp_f={i:j for i,j in zip(part,fpm2_5)}
len_pm2_5=len([i for i in fpm2_5 if i>0 and i in v4])
len_pm10 =len([i for i in part if  i in v4])
for i in range(len(df)):
    val_p25=df.loc[i,SPNAMs[6]]
    val_p10=df.loc[i,SPNAMs[5]]
    if np.isnan(val_p25) or np.isnan(val_p10) :continue
    II,JJ=df.loc[i,'IJ']/1000,df.loc[i,'IJ']%1000
    pm2_5,pm10,pm3sp=0,0,0
    for sp in part:
      if sp not in v4:continue
      pm2_5+=con_file.variables[sp][0,0,JJ,II]*sp_f[sp]
      pm10 +=con_file.variables[sp][0,0,JJ,II]
      if sp in part3sp:pm3sp+=con_file.variables[sp][0,0,JJ,II]
    if pm2_5==0.:
      for sp in part:
        if sp not in v4:continue
        if sp_f[sp]==0:continue
        con_file.variables[sp][0,0,JJ,II]=val_p25/len_pm2_5 #divided evenly
    else:
      for sp in part:
        if sp not in v4:continue
        if sp_f[sp]==0:continue
        con_file.variables[sp][0,0,JJ,II]=con_file.variables[sp][0,0,JJ,II]/pm2_5*val_p25/sp_f[sp]

    pmC=0
    for sp in part:
      if sp not in v4:continue
      if sp_f[sp] in [1.,0.]:continue
      pmC+=con_file.variables[sp][0,0,JJ,II]*(1-sp_f[sp])

    if pm3sp==0:
      for sp in part3sp:
        if sp not in v4:continue
        con_file.variables[sp][0,0,JJ,II]=(val_p10-val_p25-pmC)/3. #divided evenly
    else:
      pmc=max(0.,val_p10-val_p25-pmC)
      for sp in part3sp:
        if sp not in v4:continue
        con_file.variables[sp][0,0,JJ,II]=con_file.variables[sp][0,0,JJ,II]/pm3sp*pmc
con_file.close
