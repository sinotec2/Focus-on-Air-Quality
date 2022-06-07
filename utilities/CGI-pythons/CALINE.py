#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import subprocess
import tempfile as tf

WEB='/Library/WebServer/Documents'
CGI='/Library/WebServer/CGI-Executables/caline/'
CLINE='/Users/1.PlumeModels/CALINE3/caline3 '
KML2INP=CGI+'kml2inp.py'
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
try:
  cpu=float(subprocess.check_output('/opt/local/bin/cpu',shell=True).decode('utf8').strip('\n').strip('%'))
except:
  sys.exit('cpu fail')
if cpu>=550:
  print 'total kerels used: '+str(cpu)+'%,  too many processes are running, please wait. </br>'
  print '</body></html>'
  sys.exit()
  
form = cgi.FieldStorage()
ROT='clin'

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
rrn='/caline_results/'+ROT+'_'+ran+'/'
pth=WEB+rrn
OUT='>> '+pth+'cline.out'
os.system('mkdir -p '+pth)

RUNMDL=CLINE
inames=[]
nf='1'
fileitem = form['filename'+nf]
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
  inames.append(pth+fn)	

inp=fn
cmd ='cd '+pth+';'
if '.kml' in fn.lower():
  inp=fn.replace('.kml','.inp')
  cmd+=KML2INP+' '+fn+';'
cmd+=RUNMDL+'<'+inp+'>CALINE3.OUT &disown;echo $!'
pid=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n')
if len(pid)==0:
  fn='CALINE3.OUT'
  print """Something wrong in Model excutions, see <a href="%s">%s</a>
  </body></html>
  """  % (rrn+fn,fn)
  sys.exit()

#Store the PID, RAND, and DATE
HIS='/Library/WebServer/Documents/caline_results/his.txt'
DATE=subprocess.check_output('date -j +"%Y-%m-%d_%H:%M"',shell=True).decode('utf8').strip('\n')
cmd ='if ! [ -e '+HIS+' ];then echo PID, RAND, DATE >'+HIS+';fi;'
cmd+='echo '+pid+', '+ran+', '+DATE+'>>'+HIS
os.system(cmd)

#The Resultant File Links
fnames=subprocess.check_output('sleep 1;ls '+pth,shell=True).decode('utf8').split('\n')

print 'pid= '+pid+' is already done.</br>'
print """\
  <p>Model_results:</br>
  """
for fn in fnames:
  fname=rrn+fn
  print """\
  <p><a href="%s" target="_blank">%s</a></br>
  """  % (fname,fn)
print '</body></html>'

