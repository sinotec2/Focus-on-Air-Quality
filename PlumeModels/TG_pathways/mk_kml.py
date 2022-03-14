from pyproj import Proj
from pandas import *
import twd97
import os
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
twn=read_csv('TWN_1X1REC.csv')
twn['nx_dx']=[i*j for i,j in zip(list(twn.nx),list(twn.dx))]
twn=twn.sort_values('nx_dx',ascending=False).reset_index(drop=True)
pts=read_csv('point_ij.csv')
url='http://114.32.164.198/terr_results/'
ext=['.tiff','.dem','.kml','_aermap.inp','_aermap.out','.REC','_re.dat','_TG.txt']
col=['lon','lat','name','desc']

lat,lon,name,desc=([] for i in range(4))
for i in range(len(twn)):
    for s in 'dx,dy,inp,nx,ny,path,x0,y0'.split(','):
        exec(s+'=twn.'+s+'['+str(i)+']')
    if path not in set(pts.CP_NO):continue
    for s in ['lon','lat']:
        exec(s+'.append(list(pts.loc[pts.CP_NO=="'+path+'","'+s+'"])[0])')
    urls=''
    for e in ext:
        urls+=url+inp+'/'+path+e+' '
    name.append(path)
    desc.append(urls)
DD={}
for s in ['lon','lat','name','desc']:
    exec('DD.update({"'+s+'":'+s+'})')
df=DataFrame(DD)
df[col].set_index('lon').to_csv('terrTWN_1X1.csv')
os.system('/opt/local/bin/csv2kml.py -f terrTWN_1X1.csv -n N -g LL')

lat,lon,name,desc=([] for i in range(4))
for i in range(len(twn)):
    for s in 'dx,dy,inp,nx,ny,path,x0,y0'.split(','):
        exec(s+'=twn.'+s+'['+str(i)+']')
    if path not in set(pts.CP_NO):continue
    ij=0
    for jj in range(2):
        y=y0+ny*dy*jj-Ycent
        for ii in range(2):
            x=x0+nx*dx*ii-Xcent
            if jj==1:x=x0+nx*dx*(1-ii)-Xcent
            loni, lati = pnyc(x, y, inverse=True)
            for s in ['lon','lat']:
                exec(s+'.append('+s+'i)')
            urls=''
            for e in ext:
                urls+=url+inp+'/'+path+e+' '
            p='p'+str(ij)
            name.append(path+p)
            desc.append(urls+p)
            ij+=1
DD={}
for s in ['lon','lat','name','desc']:
    exec('DD.update({"'+s+'":'+s+'})')
dfp=DataFrame(DD)
dfp[col].set_index('lon').to_csv('terrTWN_1X1P.csv')
os.system('/opt/local/bin/csv2kml.py -f terrTWN_1X1P.csv -n P -g LL')

