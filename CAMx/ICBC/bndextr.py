#kuang@master /nas1/camxruns/2018/outputs/con01/grd01_bnd
#$ cat bndextr.py
import numpy as np
from PseudoNetCDF.camxfiles.Memmaps import uamiv, lateral_boundary
import netCDF4
import sys, os, subprocess
from bisect import bisect
from scipy.interpolate import CubicSpline

#read the airqualy concentration of coarse grid
path=sys.argv[1]
pathO=path+'B.nc'
nc0 = uamiv(path,'r')
V0=[list(filter(lambda x:nc0.variables[x].ndim==j, [i for i in nc0.variables])) for j in [1,2,3,4]]
nt0,nlay0,nrow0,ncol0=nc0.variables[V0[3][0]].shape

#duplicate the template for writting
#pncgen -s TSTEP,0 -f lateral_boundary base.grd01.base.bc bnd.nc
#ncks -O --mk_rec_dmn TSTEP bnd.nc a;mv a bnd.nc
os.system('cp bnd.nc '+pathO)
nc1 = netCDF4.Dataset(pathO, 'r+')
V=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
nlay1,nrow1,ncol1=nc1.NLAYS,nc1.NROWS,nc1.NCOLS

nvar=len(V[2])-2
if nvar!=len(V0[3])*4:sys.exit('wrong in NVARS matching')
spec=set([v.split('_')[1] for v in V[2][:] if 'FLAG' not in v])
if spec !=set(V0[3]):sys.exit('wrong in spec matching')
if nc1.XCELL>nc0.XCELL or nc1.YCELL>nc0.YCELL:sys.exit('wrong in resolution matching')

for a in '01':#fine(1) and coarse(1) meshes
  exec('x1d'+a+'=[nc'+a+'.XORIG+i*nc'+a+'.XCELL for i in range(ncol'+a+')]')
  exec('y1d'+a+'=[nc'+a+'.YORIG+i*nc'+a+'.YCELL for i in range(nrow'+a+')]')

for a in 'xy': #corner points of fine grid in coarse mesh
  exec('min'+a+'=bisect('+a+'1d0,'+a+'1d1[0])-1')
  exec('max'+a+'=bisect('+a+'1d0,'+a+'1d1[-1])+1')

for t in range(nt0):#elongate the time axis
  for v in ['TFLAG','ETFLAG']:
    for dt in range(2):
      nc1[v][t,:,dt]=nc0.variables[v][t,0,dt]
nc1.SDATE,nc1.STIME=nc1['TFLAG'][0,0,:]

#mapping the faces
sides={0:'WEST',1:'EAST',2:'SOUTH',3:'NORTH'}
mni={0:minx,  1:maxx,  2:minx,  3:minx}
mxi={0:minx+1,1:maxx+1,2:maxx,  3:maxx}
mnj={0:miny,  1:miny,  2:miny,  3:maxy}
mxj={0:maxy,  1:maxy,  2:miny+1,3:maxy+1}
X={0:np.array([y1d0[i] for i in range(miny,maxy)]), 2:np.array([x1d0[i] for i in range(minx,maxx)])}
X.update({1:X[0],3:X[2]})
xy1d1={0:y1d1,1:y1d1,2:x1d1,3:x1d1}
#cubicspline interpolation of coarse grid along x and y directions(axis=2)
for face in range(4):
  for v in V0[3]:
    var=nc0.variables[v][:,:,mnj[face]:mxj[face],mni[face]:mxi[face]]
    var=var.flatten().reshape(nt0,nlay0,np.prod(var.shape)//nt0//nlay0) #reshape for dropping dimension of 1
    cs=CubicSpline(X[face],var,axis=2)
    nc1[sides[face]+'_'+v][:,:,:]=np.transpose(cs(xy1d1[face][:]),axes=(0,2,1))#shape in [NSTEPS,NCOLS/NROWS,NLAYS]
nc0.close()
nc1.close()
pncg=subprocess.check_output('which pncgen',shell=True).decode('utf8').strip('\n')
if len(pncg)>0:
  os.system(pncg+' -f netcdf --out-format=lateral_boundary '+pathO+' '+pathO.replace('.nc','.bc'))
else:
  sys.exit('pncgen not found')
