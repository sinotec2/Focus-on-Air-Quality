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

def rd_A1A2(A1,A2):
  i1,i2=STR.index(A1)+len(A1),STR.index(A2)
  try:
    return float(STR[i1:i2])
  except:
    print ('<p> fail convert: {:s} </p>').format(STR[i1:i2])
    print"""</body></html>"""
    sys.exit()

def rd_A1Ln(A1,Ln):
  i1=STR.index(A1)+len(A1)
  try:
    return float(STR[i1:i1+Ln])
  except:
    print ('<p> fail convert: {:s} </p>').format(STR[i1:i1+Ln])
    print"""</body></html>"""
    sys.exit()

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
pth=WEB+'isc_results/'
OUT='>> '+pth+'isc.out'
CSV2KML='/opt/local/bin/csv2kml.py -g TWD97 -f '
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')

STR=sys.argv[1]
#read building and stack numbers
nbld=int(rd_A1A2("with","bldg"))
nstk=int(rd_A1A2("and","stacks"))

#read the origins and angle
orig_str=STR[STR.index('[')+1:STR.index(']')].split(',')
orig=[float(i) for i in orig_str]
angl=-rd_A1Ln("'UTMN',",6)
#print ('<p> {:f} {:f} {:f} </p>').format(orig[0],orig[1],angl)

STR2=STR[STR.index("'UTMN',")+6:]
i0,i1=[STR2.index(" '")+2],[]
for i in range(nbld+nstk-1):
  i0.append(i0[-1]+1+STR2[i0[-1]+1:].index(" '")+2)
for i in range(nbld+nstk-1):
  i1.append(i0[i]+1+STR2[i0[i]+1:].index("' "))
i1.append(i1[-1]+1+STR2[i1[-1]+1:].index("' "))
names=[STR2[i0[i]:i1[i]] for  i in range(nbld+nstk)]
#for i in range(nbld+nstk):
#  print ('<p>i0,i1 : {:d} {:d} </p>').format(i0[i],i1[i])
#  print ('<p> name: {:s} </p>').format(STR2[i0[i]:i1[i]])
case=''
for i in range(nbld,nbld+nstk):
  case+=names[i]
case=case[:8]

tttX,tttY,labs=([] for i in range(3))
orig0=[0.,0.]
for ib in range(nbld):
  p=[float(i) for i in STR2[i1[ib]+1:i0[ib+1]-1].split()]
  P=[[p[4],p[5]],[p[6],p[7]],[p[8],p[9]],[p[10],p[11]],[p[4],p[5]]]
  Pn=[rotate_about_a_point(pnt,orig0,angl) for pnt in P]
  ttt=np.array(Pn)+np.array(orig*5).reshape(5,2)
#  for i in range(4):
#    print ('<p> {:f} {:f} </p>').format(ttt[i,0],ttt[i,1])
  labs+=[names[ib]+'_p'+str(i) for i in range(len(ttt[:,0]))]
  tttX+=list(ttt[:,0])
  tttY+=list(ttt[:,1])
fname=pth+case+'B.csv'
df=DataFrame({'X':tttX,'Y':tttY,'nam':labs,'lab':labs})
df.set_index('X').to_csv(fname)
os.system(CSV2KML+fname+' -n P '+OUT)
fnames=[fname]

tttX,tttY,labs=([] for i in range(3))
for ib in range(nbld,nbld+nstk):
  iend=len(STR2)
  if ib<nbld+nstk-1:iend=i0[ib+1]-1
  print ('<p> {:s} </p>').format(STR2[i1[ib]+1:iend])
for ib in range(nbld,nbld+nstk):
  iend=len(STR2)
  if ib<nbld+nstk-1:iend=i0[ib+1]-1
  p=[float(i) for i in STR2[i1[ib]+1:iend].split()]
  P=[p[2],p[3]]
  Pn=rotate_about_a_point(P,orig0,angl)
  ttt=np.array(Pn)+np.array(orig)
  print ('<p> {:f} {:f} </p>').format(Pn[0],Pn[1])
# print ('<p> {:f} {:f} </p>').format(ttt[0],ttt[1])
  labs+=[names[ib]+'_p0']
  tttX+=[ttt[0]]
  tttY+=[ttt[1]]
fname=pth+case+'S.csv'
df=DataFrame({'X':tttX,'Y':tttY,'nam':labs,'lab':labs})
df.set_index('X').to_csv(fname)
os.system(CSV2KML+fname+' -n N '+OUT)
fnames+=[fname]
    
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
