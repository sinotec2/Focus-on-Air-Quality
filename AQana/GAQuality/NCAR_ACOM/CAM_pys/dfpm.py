import numpy as np
from pandas import *
import matplotlib.pyplot as plt
from scipy.io import FortranFile

def str2lst(A):
    A=A.replace("'      '","-999.0")
    A=A.replace("'","")
    return [float(i) for i in A[1:-1].split(',')][:24]

fnameO = 'PMf21_13_32_24_608.bin'
try:
  with FortranFile(fnameO, 'r') as f:
    pmf = f.read_record(dtype=np.float64)  
  year=[i for i in range(2000,2021)]
except:
  fname='/home/backup/data/epa/pys/PM2.5_mxhr.csv'
  df=read_csv(fname)
  dft=[]
  for j in range(len(df)//10000):
    dfh=DataFrame({})
    j0=j*10000
    j1=j0+10000
    for i in range(j0,min(len(df),j1)):
      PMf=str2lst(df['PM2.5'][i])
      nst=[df.NS[i] for j in range(24)]
      hrs=[df.YYYYMMDD[i]*100+j for j in range(24)]
      dfh=dfh.append(DataFrame({'NS':nst,'PM2.5':PMf,'YMDH':hrs}),ignore_index=True)
    dft.append(dfh)
  dfh=DataFrame({})
  for i in dft:
     dfh=dfh.append(i,ignore_index=True)

  dfh=dfh.loc[dfh['PM2.5'].map(lambda x:x>0)].reset_index(drop=True)
  dfh['YEAR']=[i//1000000 for i in dfh.YMDH]
  ymdh=set(dfh.YMDH)

  dfh['MDH']=[i%1000000 for i in dfh.YMDH]
  ns=list(set(dfh.NS))
  ns.sort()
  year=list(set(dfh.YEAR))
  year.sort()
  dfh['MN']=[i//10000 for i in dfh.MDH]
  dfh['DD']=[i//100%100 for i in dfh.MDH]
  dfh['HR']=[i%100 for i in dfh.MDH]
  pmf=np.zeros(shape=(max(year)-min(year)+1,13,32,24,max(ns)+1))-1
  for s in range(len(dfh)):
    i,j,k,l,m=dfh.loc[s,'YEAR']-min(year),dfh.loc[s,'MN'],dfh.loc[s,'DD'],dfh.loc[s,'HR'],dfh.loc[s,'NS']
    pmf[i,j,k,l,m]=dfh.loc[s,'PM2.5']
  with FortranFile(fnameO, 'w') as f:
    f.write_record(pmf)

df_cnty=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/cnty2.csv')
df_twnaq=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/town_aqstE.csv')
df_cnty.no=[int(i) for i in df_cnty.no]
intv=1
xlabels=[' ']
#for y in year[:-1]:
for y in range(2007,2020):
    xlabels.append('{:02d}'.format(y%100))
pmf=pmf.reshape(max(year)-min(year)+1,13,32,24,608)
for i in range(len(df_cnty)):
    fig, ax = plt.subplots()
    n=df_cnty.loc[i,'cnty']
    plt.title(" PM2.5 of AQ Stations in "+n, loc='center' )
    plt.xlabel('Year(2digits)')
    plt.ylabel('PM2.5 (microgram/cubic meter)')
    a=df_twnaq.loc[df_twnaq.code1==df_cnty.loc[i,'no'],'aq_st']
    if len(a)==0:continue
    s=set()
    for j in a:
        s=s|set(j.split(';'))
    if len(s)==0 or s==set(['0']):continue
    s=[int(j) for j in s if len(j)>0]
    data=[]
    for y in range(2007,2020):
        yy=y-min(year)
        pp=pmf[yy,:,:,:,s].flatten()
        idx=np.where(pp>0)
        data.append(pp[idx].flatten())
    ax.boxplot(data, showfliers=False)
    xticks=list(range(0,len(data)+1,intv))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, fontsize=8)
    plt.savefig('pngs/box_'+n+'.png')

