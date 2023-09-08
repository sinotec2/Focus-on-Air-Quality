import numpy as np
from pandas import *
import netCDF4
from libtiff import TIFF
import twd97
from shapely.geometry import Point, Polygon
import sys

tiff=TIFF.open('d4_twn1x1.tiff',mode='r')
image = tiff.read_image()
nrow3,ncol3=image.shape
nc = netCDF4.Dataset('20160101.ncT','r')

Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
xmin=Xcent+nc.XORIG+500
xmax=Xcent-nc.XORIG+500
ymin=Ycent+nc.YORIG+500
ymax=Ycent-nc.YORIG+500
x = np.arange(xmin, xmax, 1000)
y = np.arange(ymin, ymax, 1000)
if len(x)!=ncol3 or len(y)!=nrow3:sys.exit('wrong dimension')
X, Y = np.meshgrid(x, y)
ll=np.array([[twd97.towgs84(i,j) for i,j in zip(X[i,:], Y[i,:])] for i in range(nrow3)])
p1=[Point(i,j) for i,j in zip(ll[:,:,0].flatten(),ll[:,:,1].flatten())]

df=read_csv('polygons.csv')
df.drop(df.loc[df.lonlats.map(lambda x:len(x)<=2)].index, inplace=True)
df['lonlats']=[j.replace(',','').replace(')','').replace('(','').replace('[','').replace(']','').split() for j in df.lonlats]
df['lonlats']=[[float(i) for i in j] for j in df.lonlats]
df['lonlats']=[[(j[i],j[i+1]) for i in range(0,len(j),2)] for j in df.lonlats]
df['lonn']=[min([i[0] for i in j]) for j in df.lonlats]
df['latn']=[min([i[1] for i in j]) for j in df.lonlats]
df['lonx']=[max([i[0] for i in j]) for j in df.lonlats]
df['latx']=[max([i[1] for i in j]) for j in df.lonlats]

twnji=np.zeros(shape=image.shape).flatten()
isq=0
for pi in p1:
  n=int(5300)
  boo=(df.latn<=pi.x)&(df.lonn<=pi.y)&(df.latx>=pi.x)&(df.lonx>=pi.y)
  a=df.loc[boo].reset_index(drop=True)
  if len(a)!=0:
    for j in range(len(a)):
      plg=Polygon([(i[1],i[0]) for i in a.loc[j,'lonlats']])
      if pi.within(plg):
        n=int(a.loc[j,'twnid'])
        break
  twnji[isq]=n
  isq+=1
twnji=twnji.reshape(image.shape)
for j in range(nrow3):
    image[nrow3-j-1,:]=twnji[j,:]
tiff=TIFF.open('d4_twn1x1.tiff',mode='w')
tiff.write_image(image)
tiff.close()
