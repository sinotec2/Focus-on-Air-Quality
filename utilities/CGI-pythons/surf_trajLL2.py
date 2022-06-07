#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import tempfile as tf
import json

#paths
JSON='/Users/Data/cwb/e-service/surf_trj/sta_list.json'
TRJs={'forc':'/Users/Data/cwb/e-service/btraj_WRFnests/ftuv10.py','obsv':'/Users/Data/cwb/e-service/surf_trj/traj2kml.py'}
WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/'
INI='/opt/local/bin/conda_ini'
NCL='/opt/anaconda3/envs/ncl_stable/bin/ncl '
MBLs={'obsv':'/Library/WebServer/Documents/taiwan/taiMarbleScale.ncl',\
      'forc':'/Library/WebServer/Documents/taiwan/chnMarble.ncl'}
SED='/usr/bin/sed -ie'
pth=WEB+'trj_results/'
OUT='>>'+pth+'trj.out'

form = cgi.FieldStorage()
dirTJ={'b':'T','f':'F'} #back->true; foreward->false
nam = form.getvalue('AQSname')
try:
  ist=int(nam)
except:
  AQ=nam
else:
  fn = open(JSON)
  d_nstnam = json.load(fn)
  AQ=d_nstnam[nam]
os.system('echo '+AQ+OUT)
OBF = form.getvalue("dirOF") #dirOF=obsv/forc
TRJ = TRJs[OBF]
MBL = MBLs[OBF]
DIR = form.getvalue("dirFB")
TF = dirTJ[DIR[0]]
num = form.getvalue("number")
dat = form.getvalue("date")
message='../../trj_results/'+DIR+AQ+dat+num+'.csv'
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
if os.path.isfile(WEB+message[6:]):
  print """\
  <p>The assigned KML file has been created and maybe downloaded in your Downloads directory.</p>
  <p>You may re-download by clicking this <a href="%s">link</a>, or...</p>
  <p> submit the KML file at Google Maps or OpenStreet interface at the
  <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
  <p> return to the previous page and redefine the trajectory.</p>
  </body>
  </html>
  """  % (message+'.kml')
else:
  fn=message.split('/')[-1]
  title=fn.replace('.csv','').replace('trj','trj_')
  mbl=MBL.split('/')[-1]

  cmd ='cd '+pth+';'
  cmd+='cp wait.png '+fn+'.png;'
  cmd+='cd '+WEB+';'
  cmd+= TRJ+' -t '+AQ+' -d '+dat+num+' -b '+TF+OUT+';'
  cmd+='source '+INI+' ncl_stable '+OUT+';'
  cmd+='cd '+pth+';'
  cmd+='cp '+MBL+' .;'+SED+(' "s/TITLE/{:s}/g" '+mbl).format(title)+';'
  cmd+= NCL+mbl+OUT+';'
  cmd+='cp topo.png '+fn+'.png;'
  os.system('echo "'+cmd+'">'+pth+'cmd.cs')
  if 'uv10' in cmd:
    os.system('sh '+pth+'cmd.cs & disown')
  else:
    os.system('sh '+pth+'cmd.cs ')
  os.system('echo "OK 3!"'+OUT)

  print """\
  <p>Trajectory job has been submitted to the system. DO NOT RELOAD this page, please !!</p>
  <p>The ncl_PNG download should start shortly(CWB WRF may takes 5 min). If it doesn't, click
  <a data-auto-download href="%s">here</a>.</p>
  <p>Or you may downnload the KML and draw the plot by yourself, please click
  <a data-auto-download href="%s">here</a>.</p>
  <p>The KML may be posted on google map or OpenStreet interface: 
  <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
  </body>
  </html>
  """  % (message+'.png' ,message+'.kml')
sys.stdout.close()
sys.exit('fine!')

