#!/opt/anaconda3/envs/py27/bin/python
#/usr/bin/python

import cgi, os, sys
import cgitb 
import tempfile as tf
from pandas import *
from terrainXYINC import terrainXYINC 
from terrainLOCAT import rd_SO, terrainLOCAT

cgitb.enable(display=1, logdir='/tmp/isc', context=5, format="html")
WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth=WEB+'isc_results/terr_'+ran+'/'
os.system('mkdir -p '+pth)
OUT='>> '+pth+'isc.out'
geninp='/opt/local/bin/gen_inp.py'
WAITM='/opt/local/bin/wait_map.cs'
CSV=WEB+'terr_results/TWN_1X1REC.csv'

form = cgi.FieldStorage()
STR = str(form.getvalue("iscinp"))
if '\n' in STR:STR=STR.replace('\n','')
os.system('echo "'+STR+'"'+OUT)
#read the name of RE_net
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
reg='GRIDCART'
loc='LOCATION'
if reg not in STR and loc not in STR:
  os.system('echo "'+reg+' or '+loc+' not in STR!" '+OUT)
  sys.exit(reg+'/'+loc+' not in STR!')

if reg in STR: snamo=terrainXYINC(pth,STR)
if loc in STR: 
  snamo,xs,ys,hs=rd_SO(STR)
  snamo=terrainLOCAT(pth,snamo,xs,ys,hs)

fname=pth+snamo+'.zip'
fn2=fname.replace('/Library/WebServer/Documents/','../../../')
ext=['_aermap.inp','.dem','.REC','.kml','.tiff','_TG.txt','_re.dat',
'_DOMDETAIL.OUT','_MAPDETAIL.OUT','_MAPPARAMS.OUT','_MAPPARAMS.OUT',
'_aermap.out','_geninp.out','_isc.out'] 
fmts=['text','USGS DEM','text','KML','GeoTiff']+['text' for i in range(9)]
mns=['aermap run stream','gdal result for aermap','aermap result for aermod include file','terrain plot','eio result','terrain file for iscst3','terrain setting in iscst.inp']+['aermap checking' for i in range(5)]+['running checks' for i in range(2)]
strs=[]
for s in ext:
  strs.append(fn2.replace('.zip',s))
  strs.append(snamo+s)
print """\
<table border-collapse=collapse width="50%">
<tr>
<th>filename</th>
<th>Meanings</th>
<th>format</th>
</tr>
"""
for i in range(len(ext)):
  print '<tr><td width=\"10%\"><a href=\"'+strs[i*2]+'\">'+strs[i*2+1]+'</a></td>'
  print '<td width="20%">'+mns[i]+'</td><td width="20%">'+fmts[i]+'</td> </tr>'
print """\
<h3><p>Your request of terrain pre-processing is done (setting as "%s") </p></h3>
<p>The resultant ZIP will be automatically downloaded shortly. If it doesn't, click <a href="%s">%s</a></p>
<p>The KML may be posted on google map or OpenStreet interface: <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
</body>
</html>
""" % (STR,fn2,fn2.split('/')[-1])
sys.stdout.close()
sys.exit('fine!')
