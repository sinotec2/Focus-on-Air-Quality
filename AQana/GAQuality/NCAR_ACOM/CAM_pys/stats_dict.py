import numpy as np
from pandas import *
import twd97
from pyproj import Proj

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

fname='stats_tab.csv'
df=read_csv(fname)
lon,lat=df.LON,df.LAT
xgl, ygl=pnyc( lon,lat,inverse=False)
UTME=(xgl+Xcent)//1000*1000
UTMN=(ygl+Ycent)//1000*1000
df['YX']=np.array(UTMN+UTME//1000,dtype=int)

dict_xy=read_csv('/nas1/TEDS/teds10_camx/HourlyWeighted/area/dict_xy.csv')
dict_xy['YX']=np.array(dict_xy.y+dict_xy.x//1000,dtype=int)
dd={yx:name for yx,name in zip(dict_xy.YX,dict_xy.name)}
df1=df.loc[df.YX.map(lambda x:x in dd)].reset_index(drop=True)
df1['name']=[dd[yx] for yx in df1.YX]
cols=['stno','stat_name','name','LON','LAT','YX']
df1[cols].set_index('stno').to_csv('stats_dict.csv')

