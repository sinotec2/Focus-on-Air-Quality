#!/opt/anaconda3/envs/env_name/bin/python
import math
import urllib.request
import os, sys, subprocess
import glob
import subprocess
import shutil
from osgeo import gdal
import twd97
from pyproj import Proj


Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
def TWD2LL(E,N):
  x,y=E-Xcent,N-Ycent
  lon,lat=pnyc(x, y, inverse=True)
  return lat,lon

Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)


#---------- CONFIGURATION -----------#
#tile_server = "https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=" + os.environ.get('MAPBOX_ACCESS_TOKEN')
tile_server = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
tile_server = "https://tile.opentopomap.org/{z}/{x}/{y}.png"
store_dir = os.path.join(os.path.dirname(__file__), '../pngs')
temp_dir = 'temp'
if not os.path.exists(temp_dir):os.system('mkdir -p '+temp_dir)
output_dir = '.'
mtg=os.path.join(os.path.dirname(__file__), 'mtg.cs')
zoomi = 22 #initial zoomming level
lon_min = 21.49147
lon_max = 21.5
lat_min = 65.31016
lat_max = 65.31688
gd='/opt/anaconda3/envs/env_name/bin/gdal_translate'
env='GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
convert='/usr/local/bin/convert'
gdalinfo='/opt/anaconda3/envs/env_name/bin/gdalinfo'
awkk='/opt/local/bin/awkk'
wget='/opt/local/bin/wget -q -U zzzzzzzz '
larg=len(sys.argv)
if larg<6:
    fname=sys.argv[1]
    with open(fname,'r') as f:
        ll=[l for l in f]
    if ll[0][0]=='*':
      ll=ll[8:]
    X,Y=([float(l.split()[i]) for l in ll] for i in [0,1])
    mnX,mnY,mxX,mxY=(min(X),min(Y),max(X),max(Y))	
else:
    mnX,nx,dx,mnY,ny,dy=(float(sys.argv[i]) for i in range(larg-6,larg))
    mxX,mxY=mnX+nx*dx,mnY+ny*dy
lat_min,lon_min=TWD2LL(mnX,mnY)
lat_max,lon_max=TWD2LL(mxX,mxY)
#-----------------------------------#

from math import log, tan, radians, cos, pi, floor, degrees, atan, sinh
def sec(x):
    return(1/cos(x))


def latlon_to_xyz(lat, lon, z):
    tile_count = pow(2, z)
    x = (lon + 180) / 360
    y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
    return(tile_count*x, tile_count*y)

def bbox_to_xyz(lon_min, lon_max, lat_min, lat_max, z):
    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)
    return(floor(x_min), floor(x_max), floor(y_min), floor(y_max))

def x_to_lon_edges(x, z):
    tile_count = pow(2, z)
    unit = 360 / tile_count
    lon1 = -180 + x * unit
    lon2 = lon1 + unit
    return(lon1, lon2)

def mercatorToLat(mercatorY):
    return(degrees(atan(sinh(mercatorY))))


def y_to_lat_edges(y, z):
    tile_count = pow(2, z)
    unit = 1 / tile_count
    relative_y1 = y * unit
    relative_y2 = relative_y1 + unit
    lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
    lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
    return(lat1, lat2)

def tile_edges(x, y, z):
    lat1, lat2 = y_to_lat_edges(y, z)
    lon1, lon2 = x_to_lon_edges(x, z)
    return[lon1, lat1, lon2, lat2]


def download_tile(x, y, z, tile_server):
    url = tile_server.replace(
        "{x}", str(x)).replace(
        "{y}", str(y)).replace(
        "{z}", str(z))
    store = f'{store_dir}/{x}_{y}_{z}.png'
    path = f'{temp_dir}/{x}_{y}_{z}.png'
    if os.path.exists(store):
        os.system('ln -sf '+store+' '+path)	
        return(path)
    if "street" in tile_server:
        os.system(wget+url+' -O '+path)
    else:
        urllib.request.urlretrieve(url, path)
    os.system('cp '+path+' '+store)	
    return(path)


def merge_tiles(input_pattern, output_path):

    merge_command = ['/opt/anaconda3/envs/env_name/bin/gdal_merge.py','-o', output_path]

    for name in glob.glob(input_pattern):
        merge_command.append(name)
    if os.path.exists(output_path):os.system('rm -f '+output_path)		
    subprocess.call(merge_command)


def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)

for zoom in range(zoomi,5,-1):
  x_min, x_max, y_min, y_max = bbox_to_xyz(
    lon_min, lon_max, lat_min, lat_max, zoom)
  ntiles=(x_max - x_min + 1) * (y_max - y_min + 1)
  if 150 > ntiles > 20:break
print(f"Downloading {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")
for x in range(x_min, x_max + 1):
    for y in range(y_min, y_max + 1):
        print(f"{x},{y}")
        png_path = download_tile(x, y, zoom, tile_server)
        georeference_raster_tile(x, y, zoom, png_path)

print("Download complete")

print("Merging tiles")
merge_tiles(temp_dir + '/*.tif', output_dir + '/merged.tif')
if 'satellite' not in tile_server:
  cmd ='cd '+temp_dir+';'
  cmd+= mtg+' {:d} {:d} {:d} {:d} {:d}'.format(x_min,x_max,y_min,y_max,zoom)
  os.system(cmd)
print("Merge complete")

llSE=' {:f} {:f} '.format(lon_max,lat_min)
llNW=' {:f} {:f} '.format(lon_min,lat_max)+llSE
UL={'ul':'\"Upper Left\"','lr':'\"Lower Right\"'}
aa={'lon':',','lat':')'}
cc={'lon':4,'lat':5}
for l in aa:
     for p in ['ul','lr']:
         exec("{:s}{:s}=subprocess.check_output(gdalinfo+' merged.tif |grep {:s}|'+awkk+' {:d}',shell=True).decode('utf8').split('{:s}\\n')".format(p,l,UL[p],cc[l],aa[l]))
         exec(p+l+'=[float(i) for i in '+p+l+' if len(i)>0][0]')

ULLR=' {:f} {:f} {:f} {:f} '.format(ullon, ullat, lrlon, lrlat)
os.system(env+gd+' -of GTiff -a_ullr'+ULLR+'-a_srs EPSG:4269 merged_montage.tif merged_montageC.tif')
os.system(env+gd+' -projwin '+llNW+' -of GTiff merged_montageC.tif fitted.tif')
os.system(convert+' fitted.tif fitted.png >&/dev/null')

#os.system('rm -f '+temp_dir+'/*.[t]*')
#shutil.rmtree(temp_dir)
#os.makedirs(temp_dir)

