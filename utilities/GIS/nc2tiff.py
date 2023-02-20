#$ cat ~/bin/nc2gtiff.py
import numpy as np
import netCDF4
import sys,os
from scipy.interpolate import griddata
import xarray as xr
import rioxarray as rio
debug=False

fname='/nas2/cmaqruns/2022fcst/grid03/mcip/GRIDCRO2D.nc'
nc = netCDF4.Dataset(fname,'r')
Y=list(nc['LAT'][0,0,:,:].flatten());X=list(nc['LON'][0,0,:,:].flatten())
mnX,mnY,mxX,mxY=(min(X),min(Y),max(X),max(Y))
fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
var=nc[V[3][0]][0,0,:,:].flatten()
dx=(mxX-mnX)/ncol;dy=(mxY-mnY)/nrow
x1_1d=[mnX+dx*i for i in range(ncol)];y1_1d=[mnY+dy*i for i in range(nrow)]
x1,y1=np.meshgrid(x1_1d, y1_1d)
x1=x1.flatten();y1=y1.flatten()
xyc=[(i,j) for i,j in zip(X,Y)]
var1=griddata(xyc, var[:], (x1, y1), method='linear')
var1=np.array(var1).reshape(nrow,ncol)
if debug:
  fnamO=fname+'_eqLL'
  os.system('cp '+fname+' '+fnamO)
  nc = netCDF4.Dataset(fnamO,'r+')
  nc[V[3][0]][0,0,:,:]=var1[:]
  nc.close()
  with open('eqLL.txt','w') as f:
    for i in x1_1d:
      f.write(str(i)+'\n')
    for i in y1_1d:
      f.write(str(i)+'\n')

da=xr.Dataset(data_vars=dict(pm=(["lat","lon"],var1)),coords=dict(lon=(["lon"],x1_1d),lat=(["lat"],y1_1d)))
pr=da.rio.set_spatial_dims("lon", "lat")
pr.rio.set_crs("epsg:4326")
if fname[-3:]=='.nc':
  fname=fname.replace('.nc','.tiff')
else:
  fname=fname+'.tiff'
pr.rio.to_raster(fname,driver="COG")
