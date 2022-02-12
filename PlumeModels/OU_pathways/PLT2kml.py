#!/opt/anaconda3/envs/py37/bin/python
import numpy as np
from pandas import *
import twd97
from pyproj import Proj
from scipy.interpolate import griddata
from save_surfer import *
import sys
from cntr_kml import cntr_kml

fname = sys.argv[1]

# read the iscst result plot file, must be in TWD97-m system, with 8 lines as header
with open(fname, 'r') as f:
  g = [line for line in f]
#description txt is read from the third line
desc = ' '
if g[0][0:3] in ['* A','* I']:
  desc = g[:3]
  g = g[8:]
lg = len(g)
x, y, c = (np.array([float(i.split()[j]) for i in g]) for j in range(3))

# 1-d X/Y coordinates
fac=1.
nx, ny = int(max(int(np.sqrt(lg)), len(set(x)))*fac),int(max(int(np.sqrt(lg)), len(set(y)))*fac)

#the domain of meshes must smaller than data domain to avoid extra_polation
dx, dy=(np.max(x)-np.min(x))/nx,(np.max(y)-np.min(y))/ny
x_mesh = np.linspace(np.min(x)+dx, np.max(x)-dx, nx)
y_mesh = np.linspace(np.min(y)+dy, np.max(y)-dy, ny)
Xcent, Ycent = (x[0]+x[-1])/2.,(y[0]+y[-1])/2.
Lat, Lon=twd97.towgs84(Xcent, Ycent)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=Lat, lon_0=Lon, x_0=0, y_0=0.0)
# 2-d mesh coordinates, both in TWD97 and WGS84
x_g, y_g = np.meshgrid(x_mesh, y_mesh)

#lat,lon pairs are used in KML locations
xgl,ygl=x_g-Xcent,y_g-Ycent
lon,lat=pnyc(xgl, ygl, inverse=True)
points=[(i,j) for i,j in zip(x,y)]
grid_z2 = griddata(points, c, (x_g, y_g), method='linear')

# generate the KML file
result=cntr_kml(grid_z2, lon, lat, fname)

# save as surfer ASCII .grd file
fnameG=fname+'.grd'
x0,y0=np.min(x),np.min(y)
dx,dy=(np.max(x)-x0)/(nx-1),(np.max(y)-y0)/(ny-1)
save_surfer(fnameG,nx,ny,x0,y0,dx,dy,grid_z2.reshape(nx*ny))
