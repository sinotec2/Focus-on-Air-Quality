#!/opt/ohpc/pkg/rcec/pkg/python/wrfpost/bin/python
import netCDF4
import sys, os, subprocess
import datetime

tdy=sys.argv[1]
bdate=datetime.datetime.strptime(tdy,"%Y-%m-%d")
nd=12
dates=[(bdate+datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(nd)]

pwd=subprocess.check_output("pwd" ,shell=True).decode('utf8').strip('\n')
fcst='/work/sinotec2/cmaqruns/forecast'
targ=fcst+'/grid45/wrfout'

ads={1:['3'],2:['1','2']}
gds={1:['03'],2:['45','09']}
ndms=1
if pwd[-3:]=='45k':
  ndms=2
with open(targ+'/att.txt', 'r') as f:
  var=[i.split(':')[1].split('=')[0].replace(' ','') for i in f if len(i)>0]
for ii in range(ndms):
  ad=ads[ndms][ii]
  ad0=ad
  if ndms==1:ad0='1'
  ftemp=targ+'/wrfout_d0'+ad+'_template'
  for jj in range(nd):
    fnam0=pwd+'/wrfout_d0'+ad0+'_'+dates[jj]+'_00:00:00'
    if not os.path.isfile(fnam0):continue
    nc0= netCDF4.Dataset(fnam0,'r')
    fname=targ+'/wrfout_d0'+ad+'_'+str(jj)
    os.system('test -e '+fname+' && rm -f '+fname+';cp '+ftemp+' '+fname)
    nc = netCDF4.Dataset(fname,'r+')
    V =[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    V0=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
    v='V10'
    nt,nrow,ncol=nc0[v].shape
#    print(fnam0)
    for t in range(nt):
      nc[v][t,:,:]=nc0[v][t,:,:]
    for v in V[3]:
      nc[v][:,:,:,:]=nc0[v][:,:,:,:]
    for v in V[2]:
      if v not in V0[2]:continue
      nc[v][:,:,:]=nc0[v][:,:,:]
    for v in V[1]:
      if nc[v].shape!=nc0[v].shape:continue
      nc[v][:,:]=nc0[v][:,:]
    for v in V[0]:
      nc[v][:]=nc0[v][:]
    for v in var:
      if '-' in v:continue
      try:
        exec('nc.'+v+'=nc0.'+v)
      except:
        continue
    nc.close()
  gd=gds[ndms][ii]
  os.system('/usr/bin/sbatch '+fcst+'/csh_mcip.sh '+gd)
