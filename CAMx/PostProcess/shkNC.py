#kuang@master /nas1/camxruns/2019/outputs/con10
#$ cat shkNC.py
#/cluster/miniconda/envs/py27/bin/python
#!/opt/anaconda3/bin/python
#encoding=utf-8
import netCDF4
import numpy as np
import sys,os

if len(sys.argv) == 1:
  print ("usage: shk nc_file")
  sys.exit(1)
else:
  if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print ("usage: shk nc_file")
    sys.exit(1)

path=sys.argv[1]+'S'
os.system('mk_tmp.cs '+sys.argv[1])
os.system('cp template.nc '+path)
nc0 = netCDF4.Dataset(sys.argv[1],'r')
nc1 = netCDF4.Dataset(path,'r+')
v4=list(filter(lambda x:nc0.variables[x].ndim==4, [i for i in nc0.variables]))
lis=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))

#enlarge the timeframes
nt,nlay,nrow,ncol=nc0.variables[v4[0]].shape
var=np.array(nc0.variables['TFLAG'][:,0,:])
for t in range(nt):
  nc1.variables['TFLAG'][t,0,:]=var[t,:]
var3=np.zeros(shape=nc1.variables['TFLAG'].shape)
var3[:,:,:]=var[:,None,:]
nc1.variables['TFLAG'][:]=var3[:]
for sp in lis:
  if sp in ['NMHC','PM10','PM25']:continue
  nc1.variables[sp][:]=nc0.variables[sp][:]

#definition of NMHC species in shk
sVOCs=' AACD ACET ALD2 ALDX BENZ CRES ETH  ETHA ETHY ETOH \
        FACD FORM GLYD INTR IOLE ISOP ISP  ISPD KET  MEOH \
        MEPX MGLY NTR  OLE  OPEN PACD PAN  PAR  PANX PRPA \
        TOL  TOLA TERP TRP  XYL  XYLA'.split()
num_C=[ 0.,  0.,  2.,  0.,  6.,  0.,  4.,  0.,  0.,  0., \
                  0.,  1.,  0.,  0.,  2.,  5.,  5.,  0.,  3.,  0., \
                  0.,  0.,  0.,  2.,  0.,  0.,  3., 0.5,  0.,  0., \
                  7.,  0., 10.,  0.,  8.,  0.]
v2c={i:j for i,j in zip(sVOCs,num_C) if i in v4}
vocs=np.zeros(shape=(nt,nlay,nrow,ncol))
for sp in v2c:
  vocs+=nc0.variables[sp][:]*v2c[sp]
nc1.variables['NMHC'][:]=vocs[:]


part='PNO3 PSO4 PNH4 POA SOA1 SOA2 SOA3 SOA4 SOPA SOPB PEC FPRM FCRS CPRM CCRS NA PCL PH2O'.split()
fpm2_5=[0.58,0.85,0.774]+[1.]*10+[0.,0]+[0.312]*2+[0]
sp_f={i:j for i,j in zip(part,fpm2_5) if i in v4}
for s in 'pm2_5,pm10'.split(','):
  exec(s+'=np.zeros(shape=(nt,nlay,nrow,ncol))')
for sp in sp_f:
  pm2_5+=nc0.variables[sp][:]*sp_f[sp]
  pm10 +=nc0.variables[sp][:]
nc1.variables['PM10'][:]=pm10[:]
nc1.variables['PM25'][:]=pm2_5[:]
nc1.close()
