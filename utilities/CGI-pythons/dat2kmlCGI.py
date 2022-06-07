#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import tempfile as tf

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
NULL=' >&/dev/null'

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth=WEB+'isc_results/kmls_'+ran+'/'
os.system('mkdir -p '+pth)
OUT='>> '+pth+'isc.out'
DAT2KML='/opt/local/bin/dat2kml.py'

print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
form = cgi.FieldStorage()
fileitem = form['filename']
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
else:	
  print 'filename not right, please re-enter'
  print ' </body> </html>'
  sys.exit('wrong filename!')

cmd ='cd '+pth+';'	  
cmd+=DAT2KML+' -f '+fn
os.system('echo "'+cmd+'"'+OUT)
os.system(cmd+OUT)

fnames=[pth+i for i in [fn,fn+'.kml',fn+'.grd']]
fname=fnames[0]
print """\
<p>filename given and save as: <a href="%s">%s</a></br></p>
"""% (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print """\
  <p>BPIPPRIN_results: The download process should start shortly. If it doesn't, click:</p>
  """
for fname in fnames[1:]:
  print """\
  <a data-auto-download href="%s">%s</a></br>
  """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print """\
KML file could be view by Googlemap, <a href="http://114.32.164.198/Leaflet/docs/index.html">Leaflet,</a> or modified by a <a href="http://114.32.164.198/LeafletDigitizer/index.html">digitizer</a></br>
  </body>
  </html>
  """
