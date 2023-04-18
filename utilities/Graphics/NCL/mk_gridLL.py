#/nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/LGHAP.PM25.D001
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import netCDF4
from pyproj import Proj
import numpy as np

fname='tempTW.nc'
nc = netCDF4.Dataset(fname,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc[V[3][0]].shape[i] for i in range(4))
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
X=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
Y=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
x,y=np.meshgrid(X, Y)
x=x.flatten();y=y.flatten()
lon, lat = pnyc(x, y, inverse=True)
df=pd.DataFrame({'LAT':lat,'LON':lon})
df['Point']=[Point(i,j) for i,j in zip(lon,lat)]
ndf=len(x)

root='/nas1/Data/GIS/TWN_town/'
gdf = gpd.read_file(root+'TOWN_MOI_1090727_geo.json')
ngdf=len(gdf);ndf=len(df)

townid=[]
for i in range(ndf):
  found=0
  for j in range(ngdf):
    if df.Point[i].within(gdf.geometry[j]):
      townid.append(gdf.TOWNCODE[j])
      found=1
      break
  if found==0:townid.append('00000000')

df['TOWNCODE']=townid

tn={i:j for i,j in zip(gdf.TOWNCODE, gdf.TOWNNAME)}
cn={i:j for i,j in zip(gdf.COUNTYCODE, gdf.COUNTYNAME)}
cn.update({'00000':'海'})
tn.update({'00000000':'海'})
df['COUNTYCODE']=[i[:5] for i in df.TOWNCODE]
df['COUNTYNAME']=[cn[i] for i in df.COUNTYCODE]
df['TOWNNAME']=[tn[i] for i in df.TOWNCODE]
df.set_index('LAT').to_csv('gridLL.csv')
