import numpy as np
from pandas import *
import twd97, utm
from scipy.interpolate import griddata
#python3 -m pip install --index-url https://github.com/matplotlib/legacycontour.git legacycontour
import legacycontour._cntr as cntr
import bisect
import sys,os
from pyproj import Proj
import rasterio
from rasterio.transform import Affine
from cntr_kml import cntr_kml

#read the 20M DTM data TIFF from https://dtm.moi.gov.tw/2020dtm20m/台灣本島及4離島\(龜山島_綠島_蘭嶼_小琉球\).7z
fname='taiwan2020.tif'
img = rasterio.open(fname)
data=np.flip(img.read()[0,:,:],[0])
x0,y0=img.xy(0,0)
mn=img.shape
dxm,dym=(img.bounds.right-img.bounds.left)/img.width,-(img.bounds.top-img.bounds.bottom)/img.height
x1d = np.array([x0+dxm*i for i in range(mn[1])])
y1d = np.array([y0+dym*i for i in range(mn[0])])
y1d.sort()


#gdname, xmin,nx,dx,ymin,ny,dy
args = [sys.argv[i] for i in range(1,8)]
fname, dir, last = (args[0],'.',args[0])
if '/' in fname:
  last=fname.split('/')[-1]
  dir=fname.replace(last,'')
else:
  fname='./'+fname
distr = 'ALL'
xmin,nx,dx,ymin,ny,dy=(float(args[i]) for i in range(1,7))
nx,ny=int(nx),int(ny)
xmax=xmin+(nx-1)*dx
ymax=ymin+(ny-1)*dy
Xcent=(xmin+xmax)/2
Ycent=(ymin+ymax)/2
Latitude_Pole, Longitude_Pole=twd97.towgs84(Xcent, Ycent)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

M=5
x_mesh = np.linspace(xmin-dx*M, xmax+dx*M, nx+2*M)
y_mesh = np.linspace(ymin-dy*M, ymax+dy*M, ny+2*M)
# 2-d mesh coordinates, both in TWD97 and WGS84
x_g, y_g = np.meshgrid(x_mesh, y_mesh)
xgl=x_g-Xcent
ygl=y_g-Ycent
lon,lat=pnyc(xgl, ygl, inverse=True)


# cut taiwan2020.tif
#the domain of ele. data must be greater than receptor domain to avoid extra_polation

I1=bisect.bisect_left(x1d,x_mesh[0])-2;I2=bisect.bisect_left(x1d,x_mesh[-1])+2
J1=bisect.bisect_left(y1d,y_mesh[0])-2;J2=bisect.bisect_left(y1d,y_mesh[-1])+2
c=data[J1:J2,I1:I2].flatten()
c=np.where(c<0,0,c)
x=np.array([x1d[I1:I2] for j in range(J2-J1)]).flatten()
y=np.array([[j for i in range(I2-I1)] for j in y1d[J1:J2]]).flatten()

#interpolation from points to the receptor grid (x_g, y_g)
points=[(i,j) for i,j in zip(x,y)]
grid_z2 = griddata(points, c, (x_g, y_g), method='linear')

#save tiff file
TIF,DEM,NUL=fname+'.tiff',last+'.dem',' >>'+dir+'geninp.out'
os.system('cp template.tiff '+TIF)
resx,resy=(np.max(lon)-np.min(lon))/(nx+2*M-1),(np.max(lat)-np.min(lat))/(ny+2*M-1),
transform = Affine.translation(np.min(lon), np.max(lat)) * Affine.scale(resx, -resy)
new_dataset = rasterio.open(TIF,'w',driver='GTiff',height=grid_z2.shape[0],width=grid_z2.shape[1],count=1,
  dtype=grid_z2.dtype,crs='+proj=latlong',transform=transform,)
data=np.flip(grid_z2,[0])
new_dataset.write(data, 1)
new_dataset.close()

# convert the tiff to dem
llSE=str(lon[1,-2])+' '+str(lat[1,-2])
llNW=str(lon[-2,1])+' '+str(lat[-2,1])+' '+llSE
pth1='/opt/anaconda3/bin/'
pth2='/opt/anaconda3/envs/ncl_stable/bin/'
gd_data=';export PATH='+pth1+':'+pth2+':$PATH;GDAL_DATA=/opt/anaconda3/envs/py37/share/gdal '
os.system('echo "before gdal"'+NUL)
gd='gdal_translate'
cmd='cd '+dir+gd_data+gd+' -of USGSDEM -ot Float32 -projwin '+llNW+' '+TIF+' '+DEM+NUL
os.system('echo "'+cmd+'"'+NUL)
os.system(cmd)

#generate aermap.inp,
xy=utm.from_latlon(lat,lon)
uxmn,uxmx=int(np.min(xy[0][M:-M,M])),int(np.max(xy[0][M:-M,-M]))
uymn,uymx=int(np.min(xy[1][M,M:-M])),int(np.max(xy[1][-M,M:-M]))
co,an,z='   DOMAINXY  ','   ANCHORXY  ',' 51 '
UTMrange=co+str(uxmn)+' '+str(uymn)+z+str(uxmx)+' '+str(uymx)+z
xmid,ymid=(xmin+xmax)/2., (ymin+ymax)/2.
llanc=pnyc(xmid-Xcent, ymid-Ycent, inverse=True)
uxanc,uyanc=utm.from_latlon(llanc[1],llanc[0])[0:2]
UTMancha=an+str(int(xmid))+' '+str(int(ymid))+' '+str(int(uxanc))+' '+str(int(uyanc))+z+'0'

#change the contain of aermap
text_file = open("aermap.inp", "r+")
d=[line for line in text_file]
keywd=[i[3:11] for i in d]
ifile=keywd.index('DATAFILE')
idmxy=keywd.index('DOMAINXY')
ianxy=keywd.index('ANCHORXY')
ihead=keywd.index('ELEVUNIT')
iend=d.index('RE FINISHED\n')

text_file = open("aermap.inp", "w")

x0,y0=xmin,ymin
sta='RE GRIDCART '+last+' STA\n'
args[0]=last
STR='RE GRIDCART {:s} XYINC {:s} {:s} {:s} {:s} {:s} {:s}\n'.format(*args)
s=[sta,STR,sta.replace('STA','END')]
for l in range(ihead+1):
#  if l == ifile:
#    text_file.write( "%s" % '   DATAFILE  '+DEM+'\n')
  if l == idmxy:
    text_file.write( "%s" % UTMrange+'\n')
  elif l == ianxy:
    text_file.write( "%s" % UTMancha+'\n')
  else:
    text_file.write( "%s" % d[l])
for l in range(len(s)):
    text_file.write( "%s" % s[l])
for l in range(iend,len(d)):
    text_file.write( "%s" % d[l])
text_file.close()

# execute the aermap
aermap_path='./'
os.system(aermap_path+'aermap >& isc.out')

result=cntr_kml(grid_z2, lon, lat, fname)

# generate the ISC files
if M>0:
  grid_z2=grid_z2[M:-M,M:-M]
  x_g, y_g = x_g[M:-M,M:-M], y_g[M:-M,M:-M] 

xy = np.array([[(i, j) for i, j in zip(x_g[k], y_g[k])] for k in range(ny)])
with open(fname + '_re.dat','w') as f:
  f.write('RE ELEVUNIT METERS\n')
  for j in range(ny):
    for i in range(nx):
      f.write('RE DISCCART '+str(xy[j,i,0])+' '+str(xy[j,i,1])+' '+str(grid_z2[j,i])+'\n')

#terrain grid file
with open(fname + '_TG.txt','w') as f:
  f.write(str(nx)+' '+str(ny)+' '+str(xmin)+' '+str(xmax)+' '+str(ymin)+' '+str(ymax)+' '+str(dx)+' '+str(dy)+'\n')
  for j in range(ny):
    ele=[str(int(grid_z2[j,i])) for i in range(nx)]
    st=ele[0]
    for i in range(1,nx):
      st+=' '+ele[i]
    f.write(st+'\n')
