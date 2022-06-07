#!/opt/anaconda3/envs/py27/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb; cgitb.enable()
from pandas import *
import numpy as np
import twd97
from pyproj import Proj
import tempfile as tf

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)


form = cgi.FieldStorage()

SED='/usr/bin/sed -ie'
pth='/tmp/wrose/'
rst='/Library/WebServer/Documents/taiwan/'
CGI='/Library/WebServer/CGI-Executables/'
NCL='/opt/anaconda3/envs/ncl_stable/bin/ncl '
MBLs={'obsv':'/Library/WebServer/Documents/taiwan/taiMarbleScale.ncl',\
      'forc':'/Library/WebServer/Documents/taiwan/chnMarble.ncl'}
ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
os.system('mkdir -p '+pth)
print "Content-Type: text/html\n\n "
print open(CGI+'header.txt','r')
fileitem = [form['filename'+str(i)] for i in range(2)]
fns,dfs=[],[]
col=['x','y']
for i in range(2):
  if fileitem[i].filename:
    fns.append( os.path.basename(fileitem[i].filename))
    open(pth+fns[i], 'wb').write(fileitem[i].file.read())
  df=read_csv(pth+fns[i],header=None)
  if len(df.columns)>2:
    col_tmp=df.columns  
    for j in range(2,len(df.columns)):
      del df[col_tmp[j]]
  df.columns=col
  if type(df.loc[0,'x'])!=float:
    df=df.drop(0).reset_index(drop=True)
    df.x=np.array(df.x,dtype=float)	
    df.y=np.array(df.y,dtype=float)	
  if max(df.x)>360.:
    x_lcp,y_lcp=np.array(df.x)-Xcent,np.array(df.y)-Ycent
    lon, lat = pnyc(x_lcp, y_lcp, inverse=True)
    df.x,dfy=lon,lat
  dfs.append(df)
if len(dfs[0])>len(dfs[1]):
  line,marks=(dfs[i] for i in range(2))
else:
  marks,line=(dfs[i] for i in range(2))
line[col].set_index('x').to_csv(rst+'line.csv',header=None)
marks[col].set_index('x').to_csv(rst+'marks.csv',header=None)

MBL=MBLs['obsv']
mbl=MBL.split('/')[-1]
rmb='trj_'+ran+'.ncl'
title='trj. for '+fns[0].replace('.csv','')
cmd ='source /opt/local/bin/conda_ini ncl_stable >/tmp/wrose/wrose.out;'
cmd+='cd '+rst+';'
cmd+='cp '+mbl+' '+rmb+';'+SED+(' "s/TITLE/{:s}/g" '+rmb).format(title)+';'
cmd+= NCL+rmb+'>>/tmp/wrose/wrose.out;'
cmd+='cp topo.png ./trj_'+ran+'.png'
os.system('echo "'+cmd+'">>/tmp/wrose/wrose.out') 
os.system(cmd)
os.system('echo "OK 3!">>/tmp/wrose/wrose.out') 

fn2='../../taiwan/trj_'+ran+'.png'
print """
<p>The resultant PNG will be automatically downloaded shortly. If it doesn't, click <a data-auto-download href="%s">%s</a></p>
</body>
</html>
""" % (fn2,fn2.split('/')[-1])
