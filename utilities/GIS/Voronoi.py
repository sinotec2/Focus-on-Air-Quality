# https://towardsdatascience.com/how-to-create-voronoi-regions-with-geospatial-data-in-python-adbb6c5f2134
#/nas2/cmaqruns/2022fcst/fusion/Voronoi/voronoi.py
#!/opt/anaconda3/envs/py36/bin/python
import numpy as np
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.ops import cascaded_union, unary_union
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from geovoronoi import voronoi_regions_from_coords, points_to_coords

shp_fname="/home/kuang/bin/TWN_COUNTY.shp"
gdf = gpd.read_file(shp_fname)

CNTYNAM=set(gdf.COUNTYNAME)-{'金門縣','澎湖縣','連江縣'}
ifirst=1
for c in list(CNTYNAM)[:]:
    a=gdf.loc[gdf.COUNTYNAME==c].reset_index(drop=True)
    area=[i.area for i in a.geometry]
    imax=area.index(max(area))
    if len(a)==1:
        b=a.to_crs(epsg=4326)
    else:
        b=a.loc[a.index==imax].reset_index(drop=True).to_crs(epsg=4326)
    if ifirst==1:       
        df0=b.to_crs(epsg=4326)
        ifirst=0
    else:        
        df0=gpd.GeoDataFrame(pd.concat([df0,b],ignore_index=True))

stn=pd.read_csv('/nas1/cmaqruns/2016base/data/sites/sta_ll.csv')
stnpnt=[Point(i,j) for i,j in zip(stn.lon,stn.lat)]

for i in range(len(stn)):
    b=gpd.GeoDataFrame({'COUNTYSN':stn.loc[i,'ID'] ,'COUNTYNAME':stn.loc[i,'New'],'geometry':[stnpnt[i]]})
    df0=gpd.GeoDataFrame(pd.concat([df0,b],ignore_index=True))

df1=df0.loc[:21]
df1.to_file('mainisland.shp',mode='w')
df2=df0.loc[22:]
df1.to_file('stn.shp',mode='w')

boundary = boundary.to_crs(epsg=4326)
boundary_shape = unary_union(boundary.geometry)

df2=df2.reset_index(drop=True)
for i in range(len(df2)):
    p=df2.loc[i,'geometry']
    if not p.within(boundary_shape) or boundary_shape.exterior.distance(p) < 0.01:
        df2=df2.drop(i)
df2=df2.reset_index(drop=True)

gdf_proj = df2.to_crs(boundary.crs)
coords = points_to_coords(gdf_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, boundary_shape)

boundary = gpd.read_file("mainisland.shp")
fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color="gray")
df1.plot(ax=ax, markersize=3.5)#, color="brown")
df2.plot(ax=ax, markersize=3.5, color="brown")
ax.axis("off")
plt.axis("equal")
plt.show()

fig, ax = subplot_for_map()
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, region_polys, coords, region_pts)
ax.set_title('Voronoi regions of Schools in Uppsala')
plt.tight_layout()
plt.show()
