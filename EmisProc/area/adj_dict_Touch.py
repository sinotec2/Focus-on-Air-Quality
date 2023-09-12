#kuang@master /home/QGIS/Data/TWN_town
#$ cat adj_dict.py

from shapely.geometry import Polygon
from pandas import *
import numpy as np
import sys
import os
import json

fname='/home/QGIS/Data/TWN_town/polygons.csv'
df=read_csv(fname,encoding='big5')
df['lonlats']=[j.replace(',','').replace(')','').replace('(','').replace('[','').replace(']','').split() for j in df.lonlats]
df['lonlats']=[[float(i) for i in j] for j in df.lonlats]
df['lonlats']=[[(j[i],j[i+1]) for i in range(0,len(j),2)] for j in df.lonlats]
df['polygon']=[Polygon(i) for i in df.lonlats]
adj_dict={}
for i in range(len(df)):
  touched=[]
  for j in range(len(df)):
    if df.polygon[i].touches(df.polygon[j]):touched.append(df.twnid[j])
  if len(touched)==0:touched=[0]
  s=''
  for t in touched:
   s+=str(t)+';'
  adj_dict.update({str(df.twnid[i]):s})
fname='adj_dict.json'
fn=open(fname,'w')
json.dump(adj_dict,fn)