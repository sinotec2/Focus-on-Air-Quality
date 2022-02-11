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

# levels size,>10 too thick, <5 too thin
N = 10
mxgrd=max([10.,np.max(grid_z2)])
levels = np.linspace(0, mxgrd, N)
col = '#00FF0A #3FFF0A #7FFF0A #BFFF0A #FFFF0A #FECC0A #FD990A #FC660A #FB330A #FA000A'.replace('#', '').split()
if len(col) != N: print ('color scale not right, please redo from http://www.zonums.com/online/color_ramp/')
aa = '28'  # ''28'~ 40%, '4d' about 75%
rr, gg, bb = ([i[j:j + 2] for i in col] for j in [0, 2, 4])
col = [aa + b + g + r for b, g, r in zip(bb, gg, rr)]

# round the values of levels to 1 significant number at least, -2 at least 2 digits
i = int(np.log10(levels[1])) - 1
levels = [round(lev, -i) for lev in levels]

#the Cntr method is valid only in previous version of matplotlib
c = cntr.Cntr(lon, lat, grid_z2)
# the tolerance to determine points are connected to the boundaries
tol = 1E-3
col0 = '4d6ecdcf'
col_line0 = 'cc2d3939'


#writing the KML, see the KML official website
head1 = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.2"><Document><name><![CDATA[' + last + ']]></name>'
st_head = ''
st_med = '</color><width>1</width></LineStyle><PolyStyle><color>'
st_tail = '</color></PolyStyle></Style>'
for i in range(N):
  st_head += '<Style id="level' + str(i) + '"><LineStyle><color>' + col[i] + st_med + col[i] + st_tail
head2 = '</styleUrl><Polygon><outerBoundaryIs><LinearRing><tessellate>1</tessellate><coordinates>'
tail2 = '</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>'
line = [head1 + st_head]
# repeat for the level lines
e, w, s, n = np.max(lon), np.min(lon), np.min(lat), np.max(lat)
for level in levels[:]:
  nlist = c.trace(level, level, 0)
  segs = nlist[:len(nlist) // 2]
  i = levels.index(level)
  for seg in segs:
    line.append('<Placemark><name>level:' + str(level) + '</name><styleUrl>#level' + str(i) + head2)
    leng = -9999
    for j in range(len(seg[:, 0])):
      line.append(str(seg[j, 0]) + ',' + str(seg[j, 1]) + ',0 ')
      if j > 0:
        leng = max(leng, np.sqrt((seg[j, 0] - seg[j - 1, 0]) ** 2 + (seg[j, 1] - seg[j - 1, 1]) ** 2))
    leng0 = np.sqrt((seg[j, 0] - seg[0, 0]) ** 2 + (seg[j, 1] - seg[0, 1]) ** 2)
    ewsn = np.zeros(shape=(4, 2))
    j = -1
    # end points not closed, add coner point(s) to close the polygons.
    if leng0 > leng and leng0 / leng > 5:
      if abs(seg[j, 0] - e) < tol: ewsn[0, 1] = 1
      if abs(seg[0, 0] - e) < tol: ewsn[0, 0] = 1
      if abs(seg[j, 0] - w) < tol: ewsn[1, 1] = 1
      if abs(seg[0, 0] - w) < tol: ewsn[1, 0] = 1
      if abs(seg[j, 1] - s) < tol: ewsn[2, 1] = 1
      if abs(seg[0, 1] - s) < tol: ewsn[2, 0] = 1
      if abs(seg[j, 1] - n) < tol: ewsn[3, 1] = 1
      if abs(seg[0, 1] - n) < tol: ewsn[3, 0] = 1
      if sum(ewsn[1, :] + ewsn[2, :]) == 2: line.append(str(np.min(lon)) + ',' + str(np.min(lat)) + ',0 ')
      if sum(ewsn[1, :] + ewsn[3, :]) == 2: line.append(str(np.min(lon)) + ',' + str(np.max(lat)) + ',0 ')
      if sum(ewsn[0, :] + ewsn[3, :]) == 2: line.append(str(np.max(lon)) + ',' + str(np.max(lat)) + ',0 ')
      if sum(ewsn[0, :] + ewsn[2, :]) == 2: line.append(str(np.max(lon)) + ',' + str(np.min(lat)) + ',0 ')
    # TODO: when contour pass half of the domain,must add two edge points.
    line.append(tail2)
line.append('</Document></kml>')
with open(fname + '.kml', 'w') as f:
  [f.write(i) for i in line]

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
