import esda
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import libpysal as lps
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

import netCDF4
root='l:/nas2/cmaqruns/2019TZPP/output/Annual/aTZPP/'
gdf = gpd.read_file(root+'twTown1982.geojson')
fname=root+'GRIDCRO2D.nc'
nc = netCDF4.Dataset(fname,'r+')
lat=np.array(nc.variables['LAT'][0,0,:,:]).flatten()
lon=np.array(nc.variables['LON'][0,0,:,:]).flatten()
df=pd.DataFrame({'LAT':lat,'LON':lon})
df['Point']=[Point(i,j) for i,j in zip(lon,lat)]
ngdf=len(gdf);ndf=len(df)
townid=[]
for i in range(ndf):
  found=0
  for j in range(ngdf):
    if df.Point[i].within(gdf.geometry[j]):
      townid.append(gdf.TOWNSN[j])
      found=1
      break
  if found==0:townid.append(-1)    
tid=np.array(townid).reshape(nc.NROWS,nc.NCOLS)
nc['MSFX2'][0,0,:,:]=tid[:,:]
nc.close()
