"""
這段程式碼是使用Python和一些常用的數據處理庫來處理地理空間數據，主要包括以下步驟：
- 匯入必要的庫：程式碼開始時使用import語句導入了需要的庫，包括shapely.geometry、pandas、numpy、sys、os 和 json。
- 讀取CSV文件：程式碼使用pandas的read_csv函數從CSV文件中讀取數據，文件路徑為/home/QGIS/Data/TWN_town/polygons.csv，並將數據存儲在DataFrame中。
- 數據預處理：程式碼對讀取的數據執行了多個預處理步驟，包括將包含地理坐標的列進行處理，以使其更容易處理。具體來說，它將每個坐標中的逗號、括號等字符進行替換和拆分，然後將坐標轉換為浮點數。最後，它將坐標對存儲在lonlats列中。
- 創建多邊形：使用shapely.geometry中的Polygon和buffer方法，程式碼將每組坐標對轉換為多邊形，然後對每個多邊形進行緩衝操作，創建區域的緩衝多邊形。
- 查找相鄰區域：使用intersects方法，程式碼查找每個區域與其他區域的交集，以確定相鄰區域。然後，它將這些相鄰區域的ID存儲在adj_dict字典中。
- 將結果保存為JSON文件：最後，程式碼將adj_dict字典保存為JSON格式的文件，文件路徑為/home/QGIS/Data/TWN_town/adj_dict.json。

這段程式碼的主要目的是處理地理空間數據，查找相鄰的區域並將結果保存為JSON文件，以便進一步分析或應用。
"""
#kuang@master /home/QGIS/Data/TWN_town
#$ cat adj_dict.py

from shapely.geometry import Polygon
from pandas import *
import numpy as np
import sys
import os
import json

path='/home/QGIS/Data/TWN_town/'
fname=path+'polygons.csv'
df=read_csv(fname,encoding='big5')
df['lonlats']=[j.replace(',','').replace(')','').replace('(','').replace('[','').replace(']','').split() for j in df.lonlats]
df['lonlats']=[[float(i) for i in j] for j in df.lonlats]
df['lonlats']=[[(j[i],j[i+1]) for i in range(0,len(j),2)] for j in df.lonlats]
df['polygon']=[Polygon(i).buffer(0.15) for i in df.lonlats] #0.1deg~10Km
adj_dict={}
for i in range(len(df)):
  touched=[]
  for j in range(len(df)):
    if df.polygon[i].intersects(df.polygon[j]):touched.append(df.twnid[j])
  if len(touched)==0:touched=[0]
  s=''
  for t in touched:
   s+=str(t)+';'
  adj_dict.update({str(df.twnid[i]):s})
fname=path+'adj_dict.json'
fn=open(fname,'w')
json.dump(adj_dict,fn)
