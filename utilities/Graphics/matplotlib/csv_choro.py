#kuang@master /nas2/cmaqruns/2022fcst/fusion/Voronoi
#$ cat csv_choro.py
#!~/.conda/envs/pyn_env/bin/python
import geopandas as gpd
import pandas as pd
import geoplot as gplt
import geoplot.crs as gcrs
import shapely

import matplotlib.pyplot as plt
import numpy as np
import sys, os

# domain of figure
x,y=[119.9,122.4,122.4,119.9,],[21.5,21.5,25.5,25.5,]
Frame=shapely.geometry.Polygon([shapely.geometry.Point(i,j) for i,j in zip(x,y)])

#town_moi shape file loading and screening
shp_path = '/nas1/Data/GIS/TWN_town/TOWN_MOI_1120317.shp'
twn=gpd.read_file(shp_path)
twn=twn.loc[twn.geometry.map(lambda p:p.within(Frame))]
sTOWNCODE=set(twn.TOWNCODE)

itm_nam=sys.argv[1]
fname=sys.argv[2]
df=pd.read_csv(fname)

col=[i for i in df.columns]
if 'TOWNCODE' not in col:sys.exit('TOWNCODE must exists')
if type(df.TOWNCODE[0]) != str:
  df.TOWNCODE=[str(i) for i in df.TOWNCODE]
  df.TOWNCODE=[(8-len(i))*'0'+str(i) for i in df.TOWNCODE]
lastTwn=sTOWNCODE & set(df.TOWNCODE)
twn=twn.loc[twn.TOWNCODE.map(lambda s:s in lastTwn)]
df=df.loc[df.TOWNCODE.map(lambda s:s in lastTwn)].reset_index(drop=True)
if len(df)>len(lastTwn):
  df=df[:len(lastTwn)]
df_itm={i:0 for i in twn.TOWNCODE}
df_itm.update({i:j for i,j in zip(list(df.TOWNCODE),list(df[itm_nam]))})
twn[itm_nam]=[df_itm[i] for i in twn.TOWNCODE]

#plotting
proj = gcrs.AlbersEqualArea(central_latitude=24.5, central_longitude=120)
f=plt.figure(figsize=(15, 13))
ax=plt.axes(projection=proj)
if '/' in fname:
  fname=fname.split('/')[-1]
plt.title(itm_nam+' in '+fname, fontsize=16)
gplt.choropleth(
        twn.loc[:, [itm_nam, 'geometry']],
        hue=itm_nam, cmap='rainbow', #cmap='Blues',
        linewidth=0.0, ax=ax,
        legend=True,
    )
gplt.polyplot(
        twn, edgecolor='black', linewidth=0.5, ax=ax,
    )
plt.show()
