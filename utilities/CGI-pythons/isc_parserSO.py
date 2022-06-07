#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import math
import numpy as np
from pandas import *
def rotate_about_a_point(target_point,center_point,angle_rs):
  cp=np.subtract(target_point,center_point)
  px=cp[0]*math.cos(math.radians(angle_rs))+cp[1]*-math.sin(math.radians(angle_rs))
  py=cp[0]*math.sin(math.radians(angle_rs))+cp[1]*math.cos(math.radians(angle_rs))
  return(np.add([px,py],center_point))

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
pth=WEB+'isc_results/'
OUT='>> '+pth+'isc.out'
CSV2KML='/opt/local/bin/csv2kml.py -g TWD97 -f '

#cgi header
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
STR=sys.argv[1]
os.system('echo "'+STR+'"'+OUT)
#read the origins
loc='SO LOCATION'
lloc=len(loc)
nsrc=STR.count(loc)
ibeg,iend=[lloc],[len(STR)]
snamo,pav,orig=([] for i in range(3))
if nsrc>1: 
  ibeg=[i+lloc for i in range(len(STR)-lloc) if STR[i:i+lloc]==loc]
  iend=[ibeg[i]-lloc for i in range(1,nsrc)]
  iend=iend+[ibeg[nsrc-1]+iend[nsrc-2]-ibeg[nsrc-2]]

for isrc in range(nsrc):
  try:
    inp=STR[ibeg[isrc]:iend[isrc]].split()
  except:
   print"""</body></html>"""
   sys.exit()
  pav_i=inp[1]
  if pav_i in ['AREA','POINT','VOLUME']:
    snamo.append(inp[0])
    pav.append(inp[1]) #POINT/AREA/VOLUME tag
    orig.append([float(inp[i].replace('SO','')) for i in range(2,4)])
  else:
    print"""<p>path not right:%s, must be any one of AREA/POINT/VOLUME.</body></html>"""%pav_i
    os.system('echo "path not right"'+OUT)
    sys.exit()
#read the area sources
par='SO SRCPARAM'
ipar=STR.index(par)
lpar=len(par)
ibeg,iend=[ipar+lpar],[ipar+len(STR)]
if nsrc>1: 
  ibeg=[i+lpar for i in range(len(STR)-lpar) if STR[i:i+lpar]==par]
  iend=[ibeg[i]-lpar for i in range(1,nsrc)]
  iend=iend+[ibeg[nsrc-1]+iend[nsrc-2]-ibeg[nsrc-2]]
snamp,tttX,tttY,labs=([] for i in range(4))
fnames=[]
for isrc in range(nsrc):
  inp=STR[ibeg[isrc]:iend[isrc]].split()
#  for i in range(nsrc):
#    print ('<p> {:d} {:d} </p>').format(ibeg[i],iend[i])
#  print"""</body></html>"""
#  sys.exit()
  if inp[0] not in snamo:
    print"""<p>src names of LOC/PAR not right: %s</body></html>""" %inp[0]
    os.system('echo "src names of LOC/PAR not right: '+inp[0]+'"'+OUT)
    sys.exit('') #premature error
  jsrc=snamo.index(inp[0])
  snamp.append(inp[0])
  if pav[jsrc][0] in 'AV':
    X,Y=[float(inp[i]) for i in range(3,5)] #length in eastern and northern directions
    if pav[jsrc]=='AREA':
      angl=-float(inp[5])
      os.system(('echo "src XYangle {:f} {:f} {:f}'+'"'+OUT).format(X,Y,angl))
    if pav[jsrc]=='VOLUME':
      Y,angl=(X,0.)
    P=[[0,0],[X,0],[X,Y],[0,Y],[0,0]]
    Pn=[rotate_about_a_point(pnt,P[0],angl) for pnt in P]
    ttt=np.array(Pn)+np.array(orig[jsrc]*5).reshape(5,2)
  labs+=[inp[0]+'_p'+str(i) for i in range(len(ttt[:,0]))]
  tttX+=list(ttt[:,0])  
  tttY+=list(ttt[:,1])  

fname=pth+snamp[0]+'.csv'
df=DataFrame({'X':tttX,'Y':tttY,'nam':labs,'lab':labs})
df.set_index('X').to_csv(fname)
os.system(CSV2KML+fname+' -n P '+OUT)
os.system(CSV2KML+fname+' -n P '+OUT)

fnames=[fname]

if 'POINT' in pav:
  fname=pth+snamp[0]+'P.csv'
  lab=[snamp[isrc]+'p'+str(i) for isrc in range(nsrc) if pav[isrc]=='POINT']
  X=[orig[isrc][0] for isrc in range(nsrc) if pav[isrc]=='POINT']
  Y=[orig[isrc][1] for isrc in range(nsrc) if pav[isrc]=='POINT']
  df=DataFrame({'X':X,'Y':Y,'nam':lab,'lab':lab})
  df.set_index('X').to_csv(fname)
  os.system(CSV2KML+fname+' -n N '+OUT)
  fnames.append(fname)

rec='RE DISCCART'
lrec=len(rec)
if rec in STR:
  fname=pth+snamp[0]+'R.csv'
  nrec=STR.count(rec)
  lab=['p'+str(i) for i in range(nrec)]
  irec=[i+lrec for i in range(len(STR)-lrec) if STR[i:i+lrec]==rec]
  X,Y=[],[]
  for r in range(nrec):
    inp=STR[irec[r]:].split()
    Xi,Yi=[float(inp[i].replace('RE','')) for i in range(2)]
    X.append(Xi)
    Y.append(Yi)
  df=DataFrame({'X':X,'Y':Y,'nam':lab,'lab':lab})
  df.set_index('X').to_csv(fname)
  os.system(CSV2KML+fname+' -n N '+OUT)
  fnames.append(fname)
    
print """\
  <p>The KML download should start shortly. If it doesn't, click
  """
for fname in fnames:
  print """\
  <a data-auto-download href="%s">%s</a>
  """  % (fname.replace(WEB,'../../')+'.kml',fname.split('/')[-1])
print """\
  </p><p>The KML may be posted on google map or OpenStreet interface: 
  <a href=http://114.32.164.198/Leaflet.FileLayer/docs/index.html>Leaflet.FileLayer</a>.</p>
  </body>
  </html>
  """
