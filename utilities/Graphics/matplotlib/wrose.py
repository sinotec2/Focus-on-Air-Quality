#!/opt/anaconda3/envs/py27/bin/python
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
import numpy as np	
import sys
from pandas import *
from windrose import WindroseAxes

def wdir(ii):
  a=float(ii)+180.
  if a>360:a=a-360.
  return a 

#read iscst met. file
fname=sys.argv[1]
with open(fname,'r') as f:
    l=[i for i in f]
l=l[1:] #neglect first line of header
if ',' in l[0]:
  # csv format
  df=read_csv(fname)
  col=df.columns
  for c in col:
    if type(df.loc[0,c])==str:
      del df[c]
    else:	  
      if max(list(df[c]))>360.:	
        del df[c]
  smx=mxv=[max(list(df[c])) for c in df.columns]
  smx.sort()
  iwd,iws=(mxv.index(smx[i]) for i in [-1,-2])
  wd,ws=(list(df[df.columns[i]]) for i in [iwd,iws])
else:  
  try:
#   isc met format  
    y,m,d,h=(int(l[0][i:i+2]) for i in range(0,7,2))
    wd=[wdir(i[8:18]) for i in l]
    ws=[float(i[18:27]) for i in l]
  except:  
    try: 
#     sfc format
      y,m,d,j,h=(int(l[0][i:i+3]) for i in range(0,13,3))
      wd=[float(i.split()[16]) for i in l]
      ws=[float(i.split()[15]) for i in l]
    except:
#	  pfl format
      try:
        y,m,d,h=(int(l[0][i:i+3]) for i in range(0,10,3))
      except:
        print ' format error!'
        sys.exit('format error')	  
      else:		
        top=[int(i[20]) for i in l]
        ltop=[l[i] for i in range(len(l)) if top[i]==1 ]		
        wd=[float(i.split()[6]) for i in ltop]
        ws=[float(i.split()[7]) for i in ltop]
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
ax.figure.savefig(fname+'.png')
