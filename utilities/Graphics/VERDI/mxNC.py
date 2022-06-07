#kuang@master /home/cpuff/UNRESPForecastingSystem/vis/20220605
#$ cat ../../Python/mxNC
#!/usr/bin/python

import numpy as np
import netCDF4
import os,sys,subprocess
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
fname=['calpuff.con.S.grd02.nc']
rw=['r','r+']
nc0=netCDF4.Dataset(fname[0],rw[0])
V=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
if len(V[3])>0:
  tt=nc0.variables[V[3][0]].dimensions[0]
else:
  tt=nc0.variables[V[2][0]].dimensions[0]

mxv={}
if len(V[3])>0:
  for v in V[3]:
    mxv.update({v:np.max((np.mean(nc0[v][:,:,:,:],axis=0)+np.max(nc0[v][:,:,:,:],axis=0))/2)})
fname='../../CALPUFF_INP/PM25.cfg'
with open(fname,'r') as f:
  lines=[i for i in f]
line7=lines[7]
line50=lines[50]
line38=lines[38] #footer_line_1 value
date=subprocess.check_output('date -d "-1 day" +"%Y-%m-%d"',shell=True).decode('utf8').strip('\n')
if 'footer1' not in line38:
  sys.exit(line38)
line38=line38.replace('footer1','Based on '+date+' Operation Rate%')
for spec in ['PMF','SO2','SO4','NOX']:
  ss=spec
  if spec=='PMF':ss='PM10'
  fname=ss+'.cfg'
  lines[7]=line7.replace('max=\"0.1\"','max=\"'+str(mxv[ss])+'\"')
  #min=0.01
  dc=(np.log10(mxv[ss])+2)/10
  lines[10]='<Step>0</Step>\n'
  for i in range(1,11):
    lines[10+i]='<Step>'+str(10**(dc*i-2))+'</Step>\n'
  lines[50]=line50
  lines[38]=line38
  if spec=='PMF':
    lines[50]=line50.replace('PPBv','ug/M3')
  with open(fname,'+w') as f:
    for line in lines:
      f.write(line)
