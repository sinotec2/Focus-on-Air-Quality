import numpy as np
import cv2
import os, sys
from PIL import Image

image=cv2.imread('output_AVPM25_20231001140000.png')
#change the black sea to white
idx2=np.where(np.sum(image,axis=2)==0)
image[idx2[0],idx2[1],:]=255
ny2,nx2,nz2=image.shape

#original resolution (WxH 611X740)
#convert PM25_TOT_000.png -resize 432X524 PM25_TOT_0001.png
imageFrame=cv2.imread('PM25_TOT_0001.png')
idx=np.where(np.sum(imageFrame[57:,143:,:],axis=2)>=200*3) #white content
ix2=[];iy2=[];ix=[];iy=[]
for i in range(len(idx[0])):
    if idx[0][i]<ny2 and idx[1][i]<nx2:
        if np.sum(image[idx[0][i],idx[1][i],:])==255*3:continue
        ix2.append(idx[1][i]+143)
        iy2.append(idx[0][i]+57)
        iy.append(idx[0][i])
        ix.append(idx[1][i])
imageFrame[iy2,ix2,:]=image[iy,ix,:]
cv2.imwrite("NCLonOTM.png",imageFrame)

