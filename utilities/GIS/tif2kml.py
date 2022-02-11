#!/opt/anaconda3/envs/py37/bin/python
import numpy as np
import twd97
import sys
from cntr_kml import cntr_kml
from pyproj import Proj
import rasterio

fname = sys.argv[1]
img = rasterio.open(fname)
data=np.flip(img.read()[0,:,:],[0])
l,b,r,t=img.bounds[:]
LL=False
if (l+r)/2==img.lnglat()[0]:LL=True
x0,y0=img.xy(0,0)
nx,ny=img.width,  img.height
dx,dy=(r-l)/nx,-(t-b)/ny
x = np.array([x0+dx*i for i in range(nx)])
y = np.array([y0+dy*i for i in range(ny)])
y.sort()
if LL:
  lon, lat = np.meshgrid(x, y)
else:
  x_g, y_g = np.meshgrid(x, y)
  Xcent,Ycent=(x[0]+x[-1])/2, (y[0]+y[-1])/2
  Latitude_Pole, Longitude_Pole=twd97.towgs84(Xcent, Ycent)
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
  xgl,ygl=x_g-Xcent,  y_g-Ycent
  lon,lat=pnyc(xgl, ygl, inverse=True)
result=cntr_kml(data, lon, lat, fname)