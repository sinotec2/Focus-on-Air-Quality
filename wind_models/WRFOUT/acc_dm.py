#kuang@DEVP /nas2/cmaqruns/2022fcst/grid45/wrfout
#$ cat acc_dm.py
#!/opt/anaconda3/envs/pyn_env/bin/python
import netCDF4
import datetime
import numpy as np
import sys,os
x='XTIME'
y='ITIMESTEP'
#accumulation variables
acc=['ACGRDFLX', 'ACSNOM', 'RAINC', 'RAINSH', 'RAINNC', 'SNOWNC', 'GRAUPELNC', 'HAILNC', 'ACHFX', 'ACLHF']
#note acc should be saved and restored(if needed) before following actions:
# for dm in 1 2 4;do
#   for i in $(ls wrfout_d0${dm}*);do d=$(echo $i|cut -d'_' -f3)
#     ncks -O -v Times,ACGRDFLX,ACSNOM,RAINC,RAINSH,RAINNC,SNOWNC,GRAUPELNC,HAILNC,ACHFX,ACLHF $i $d.nc;done
#   ncrcat -O 2016*.nc acc_d0${dm}.nc
# done
#each run must begin with same day(last day of previous month)
DM=sys.argv[1] #DM=1~3
nd=5
if len(sys.argv)>2:nd=int(sys.argv[2])
fnames=['wrfout_d0'+DM+'_'+str(i) for i in range(nd+1)]


#'wrfout_d0'+DM+'_'+begd.strftime("%Y-%m-%d")+'_00:00:00'
nc = netCDF4.Dataset(fnames[0],'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
v='Times'
if v not in V[1]:sys.exit('not a wrf system file')
nt=len(nc[v][:,0])
strT=[''.join([i.decode('utf-8') for i in nc[v][t,:]]) for t in range(nt)]
#
checkOK=True
for DM in range(1,nd+1):
  fname=fnames[DM]
  try:
    nc1 = netCDF4.Dataset(fname,'r')
  except:
    sys.exit('file '+fname+' is NOT OK!')
  if nc1.SIMULATION_START_DATE!=strT[0]: checkOK=False
if checkOK :sys.exit('check OK!')

#  print(datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00'))
min0=nc.variables[x][-1]+60
nc.SIMULATION_START_DATE=strT[0]
START_DATE=nc.SIMULATION_START_DATE
JULYR=nc.JULYR
JULDAY=nc.JULDAY
if JULYR%4==0:
  JULDAY=min(366,JULDAY)
else:
  JULDAY=min(365,JULDAY)
TITLE =nc.TITLE
# begin with zero accumulation
acmx={ac:np.zeros(shape=nc.variables[ac].shape[1:]) for ac in acc}
for ac in acc:
  var=np.zeros(shape=nc.variables[ac].shape)
  var[:,:,:]=np.array(nc.variables[ac][0,:,:])[None,:,:]
  nc.variables[ac][:,:,:]-=var[:,:,:]
  acmx[ac]=nc.variables[ac][-1,:,:]
nc.close()
for DM in range(1,nd+1):
  fname=fnames[DM]
  nc = netCDF4.Dataset(fname,'r+')
  nt=len(nc[v][:,0])
  for ac in acc:
    var=np.zeros(shape=nc.variables[ac].shape)
    var[:,:,:]=acmx[ac][None,:,:]-np.array(nc.variables[ac][0,:,:])[None,:,:]
    nc.variables[ac][:]+=var[:]
    acmx[ac]=nc.variables[ac][-1,:,:]
  nc.SIMULATION_START_DATE=START_DATE
  nc.START_DATE           =START_DATE
  nc.JULYR                =JULYR
  nc.JULDAY               =JULDAY
  nc.TITLE                =TITLE
  for t in range(nt):
    mins=min0+((DM-2)*24+t)*60
    nc.variables[x][t]=float(mins)
    nc.variables[x].units='minutes since '+START_DATE
    nc.variables[x].description='minutes since '+START_DATE
    nc.variables[y][t]=int(mins)
  nc.close()
