#!/opt/anaconda3/envs/env_name/bin/python
import numpy as np
import cv2
import os, sys
from PIL import Image

convert='/usr/local/bin/convert'



image=cv2.imread('tmp_cn.png')
ny,nx,nz=image.shape

#locate the frame of contour plot
nwidth=np.array([len(np.where(image[j,:,:]!=255)[0]) for j in range(ny)])
nheight=np.array([len(np.where(image[:,i,:]!=255)[0]) for i in range(nx)])
wh={'j':'nwidth','i':'nheight'}
nxy={'j':'ny','i':'nx'}
for ij in wh:
  n=nxy[ij]
  exec('id1=int(np.mean(np.where('+wh[ij]+'>=max('+wh[ij]+')-2)[0]))')
  exec('id2=int(np.mean(np.where('+wh[ij]+'==max(['+wh[ij]+'[i] for i in range('+n+') if abs(i-id1) > 2]))))')
  if id1==id2:
     exec('id1=np.min(np.where('+wh[ij]+'>=max('+wh[ij]+')-2)[0])')  
     exec('id2=np.max(np.where('+wh[ij]+'>=max('+wh[ij]+')-2)[0])')  
  exec(ij+'0=min([id1,id2])')
  exec(ij+'1=max([id1,id2])')
size = (j1-j0,i1-i0)

#darken the lines inside of the frame
image3=image[:]
boo=(image[:,:,0]==image[:,:,1]) & (image[:,:,1]==image[:,:,2])& (image[:,:,2]!=255)
idx=np.where(boo)
idx0=np.array([idx[0][i] for i in range(len(idx[0])) if idx[0][i]>j0 and idx[0][i]<j1 and idx[1][i]>i0 and idx[1][i]<i1])
idx1=np.array([idx[1][i] for i in range(len(idx[0])) if idx[0][i]>j0 and idx[0][i]<j1 and idx[1][i]>i0 and idx[1][i]<i1])
if len(idx0)>0 and len(idx1)>0:image3[idx0,idx1,:]=0

#resize (alignment the resolutions)
image2=cv2.imread('fitted.png')
ny2,nx2,nz=image2.shape
if ny2<size[0] and size[0]/ny2>1.3 :sys.exit('make a more detail basemap')
rate=(ny2/size[0],nx2/size[1])
size2=(int(rate[0]*ny),int(rate[1]*nx))
im_resized = cv2.resize(image3,size2, interpolation=cv2.INTER_CUBIC)
image3=np.array(im_resized)
j0,i0=int(j0*rate[0]),int(i0*rate[1])

#replace the nodata location with OSM plot
for j in range(j0,j0+ny2):
  for i in range(i0,i0+nx2):
    if (image3[j,i,:]==0).all():continue  
#    if sum(image3[j,i,:])>=200+255:
    image3[j,i,:]=image2[j-j0,i-i0,:]
cv2.imwrite("NCLonOTM.png",image3)

