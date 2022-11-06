#kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
#$ cat acc_prob.py
import numpy as np
import netCDF4
import os,sys, json
import twd97
from pandas import *
import bisect
import datetime


def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)

Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
v='O' #v is depend to templates var. names
SEA=sys.argv[1]
Li=int(sys.argv[2]) #line number from 0~5
path='/nas1/backup/data/cwb/e-service/btraj_WRFnests'
with open(path+'/kmean_'+SEA+'/fnames_'+SEA+'.txt', 'r') as f:
  fnames=[l.strip('\n') for l in f]
idx=fnames[0].index('20')
ymdh=np.array([int(i[idx:idx+10]) for i in fnames if 'zhongshan' in i ],dtype=int)

lab=read_csv('lab.csv')
lab=lab.drop([3872,5793])
lab=np.array(lab.lab,dtype=int)
#print(len(lab),len(ymdh))
#sys.exit()
for L in [Li]:
  lineL=np.where(lab==L)
  ymdhL=ymdh[lineL[0]]

  fname='prob'+str(L)+'.nc'
  os.system('cp '+path+'/tmplateD1_27km.nc '+fname)
  nc = netCDF4.Dataset(fname,'r+')
  nc.variables[v][0,0,:,:]=np.zeros(shape=(nc.NROWS,nc.NCOLS))
  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
  ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
  tex=10**ex
  DATE=str(ymdhL[0])
  sdate = datetime.datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:10]))
  nt,nvars,ndt=nc.variables['TFLAG'].shape
  for idt in range(2):
    nc.variables['TFLAG'][0,:,idt]=[dt2jul(sdate)[idt] for i in range(nvars)]
  for d in ymdhL:
    ym=str(d)[2:6]
    fname=path+'/trj_results'+ym+'/trjzhongshan'+str(d)+'L.csv'
    df=read_csv(fname)
    if len(df)==0:continue
    x=np.array(df.TWD97_x)-Xcent
    y=np.array(df.TWD97_y)-Ycent
    ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
    iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
    df['JI']=[j*tex+i for i,j in zip(ix,iy)]
    pv=pivot_table(df,index='JI',values='TWD97_x',aggfunc='count').reset_index()
    pv['hr']=np.array(pv.TWD97_x)*15./3600. #in unit of hr/total hr
    pv['I']=[ji%tex for ji in pv.JI]
    pv['J']=[ji//tex for ji in pv.JI]
    for i in range(len(pv)):
      nc.variables[v][0,0,pv.J[i],pv.I[i]]+=pv.hr[i]
  nc.close()
