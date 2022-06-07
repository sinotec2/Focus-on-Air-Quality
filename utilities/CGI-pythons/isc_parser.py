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
form = cgi.FieldStorage()
STR = str(form.getvalue("iscinp"))
os.system('echo "'+STR+'"'+OUT)
if len(STR)<=4: #in case of input a SO/RE file
  fileitem = form['filename']
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
    with open(pth+fn,'r') as ftext:
      d=[line.strip('\n')+' ' for line in ftext if line[0] not in ['*', ';','\n'] and len(line)>0]
    STR=''
    for i in d:
      STR+=i
  else:
    print"""<p>SO LOCATION/SRCPARAM/BPIP text must be uploaded, please return and fill in the blanks, thank you!</p></body></html>"""
    os.system('echo "blank inputs !"'+OUT)
    sys.exit()

if '\n' in STR:STR=STR.replace('\n',' ')
if '\r' in STR:STR=STR.replace('\r',' ')
os.system('echo "'+STR+'"'+OUT)
LBPIP=False
if 'BPIP' in STR[:10]:LBPIP=True
if LBPIP: 
  os.system(CGI+'isc_parserBP.py '+'"'+STR+'"')
else:
  os.system(CGI+'isc_parserSO.py '+'"'+STR+'"')
