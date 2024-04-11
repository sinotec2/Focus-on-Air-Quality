#kuang@node03 /var/www/cgi-bin/traj
#$ cat surf_trajLL2.py
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb
import tempfile as tf
import json

#paths
root='/nas1/backup/data'
JSON=root+'/cwb/e-service/surf_trj/sta_list.json'
TRJs={'forc':root+'/cwb/e-service/btraj_WRFnests/ftuv10_10d.py',
      'obsv':root+'/cwb/e-service/surf_trj/traj2kml.py',
      'fine':root+'/cwb/e-service/surf_trj/traj2kmlF.py'}
WEB='/var/www/html/'
CGI='/var/www/cgi-bin/'
INI='/var/www/html/trj_results/conda_ini3'
NCL='/opt/miniconda3/envs/ncl_stable/bin/ncl '
MBLs={'obsv':WEB+'taiwan/taiMarbleScale.ncl',\
      'fine':WEB+'taiwan/taiMarbleScale.ncl',\
      'forc':WEB+'taiwan/taiMarbleScale.ncl'}
#      'forc':WEB+'taiwan/taiMarble.ncl'}
SED='/usr/bin/sed -ie'
trj=WEB+'trj_results/'
ran=tf.NamedTemporaryFile().name.replace('/tmp','')
pth=trj+'trj_'+ran+'/'
result=os.system('mkdir -p '+pth+';touch '+pth+'a')
OUT='>>'+pth+'trj.out'

print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
form = cgi.FieldStorage()
dirTJ={'b':'T','f':'F'} #back->true; foreward->false
nam = form.getvalue('AQSname')
if nam is None:nam='jilong'
ll = form.getvalue('latlon')
if len(ll)==0:
  try:
    ist=int(nam)
  except:
    AQ=nam
  else:
    fn = open(JSON)
    d_nstnam = json.load(fn)
    AQ=d_nstnam[nam]
  AQll=AQ
else:
  lls=ll.split()
  if len(lls)<2:
    for delt in ',;':
      if delt in ll:
        if ll.count(delt)>1:sys.exit('number of delimiters must be one')
        ll=ll.replace(' ','')
        lls=ll.split(delt)
  lls=[i.replace(',','').replace(';','') for i in lls]
  llo=[str(round(float(i),2)) for i in lls]
#  AQ='user-defined'+'_'+llo[0]+'_'+llo[1]+'_'
  AQ=llo[0]+'_'+llo[1]+'_'
  AQll=lls[0]+','+lls[1]
os.system('echo '+AQ+OUT)
OBF = form.getvalue("dirOF") #dirOF=obsv/forc
TRJ = TRJs[OBF]
MBL = MBLs[OBF]
DIR = form.getvalue("dirFB")
TF = dirTJ[DIR[0]]
num = form.getvalue("number")
dat = form.getvalue("date")
message=pth+DIR+AQ+dat+num+'.csv'
if os.path.isfile(message):
  msg=message.replace(WEB,'/')
  print """\
  <p>The assigned KML file has been created. You may download the old files or wait for new ones.</p>
  <p>The ncl_PNG download should start shortly(CWB WRF may takes 5 min). If it doesn't, click
  <a data-auto-download href="%s">here</a>.</p>
  <p>Or you may downnload the KML and draw the plot by yourself, please click
  <a data-auto-download href="%s">here</a>.</p>
  <p>The KML may be posted on google map or OpenStreet interface:
  <a href=http://200.200.31.47/Leaflet.FileLayer/dev/index.html>Leaflet</a>.</p>
  </body>
  </html>
  """  % (msg+'.png' ,msg+'.kml')
fn=message.split('/')[-1]
title=fn.replace('.csv','')
mbl=MBL.split('/')[-1]

cmd ='cd '+pth+';'
cmd+='cp '+trj+'wait.png '+fn+'.png;'
#cmd+='cd '+WEB+';'
cmd+= TRJ+' -t '+AQll+' -d '+dat+num+' -b '+TF+OUT+';'
cmd+='source '+INI+' ncl_stable '+OUT+';'
cmd+='cd '+pth+';'
cmd+='cp '+MBL+' .;'+SED+(' "s/TITLE/{:s}/g" '+mbl).format(title)+';'
cmd+= NCL+mbl+OUT+';'
#cmd+='mv -f topo.png '+fn+'.png;'
os.system('echo "'+cmd+'">'+pth+'cmd.cs')
if 'uv10' in cmd:
  os.system('sh '+pth+'cmd.cs & disown')
else:
  os.system('sh '+pth+'cmd.cs ')
os.system('echo "OK 3!"'+OUT)

msg=message.replace(WEB,'/')
print """\
  <p>Trajectory job has been submitted to the system. DO NOT RELOAD this page, please !!</p>
  <p>The ncl_PNG download should start shortly(CWB WRF may takes 5 min). If it doesn't, click
  <a data-auto-download href="%s">here</a>.</p>
  <p>Or you may downnload the KML and draw the plot by yourself, please click
  <a data-auto-download href="%s">here</a>.</p>
  <p>The KML may be posted on google map or OpenStreet interface:
  <a href=http://200.200.31.47/Leaflet.FileLayer/dev/index.html>Leaflet</a>.</p>
  </body>
  </html>
  """  % (msg+'.png' ,msg+'.kml')
sys.stdout.close()
sys.exit('fine!')
