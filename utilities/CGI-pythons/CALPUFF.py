#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import subprocess
import tempfile as tf

WEB='/Library/WebServer/Documents'
CGI='/Library/WebServer/CGI-Executables/calpuff/'
CPUFF='/Users/cpuff/src/CALPUFF_v7.2.1_L150618/cpuff721 &> /dev/null 2>&1'
WAITC=WEB+'/cpuff_results/waitc.cs'
CPOST='/Users/cpuff/src/CALPOST_v7.1.0_L141010/con2nc'
C_MET='/Users/cpuff/src/CALMET_v6.5.0_L150223/cmet650g'
DAT2KML='/opt/local/bin/dat2kml.py'
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
ROT='cpuf'

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
rrn='/cpuff_results/'+ROT+'_'+ran+'/'
pth=WEB+rrn
OUT='>> '+pth+'cpuff.out'
os.system('mkdir -p '+pth)

RUNMDL=CPUFF
inames=[]
nf='1'
fileitem = form['filename'+nf]
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
  inames.append(pth+fn)	

cmd ='cd '+pth+';'
met_pth=subprocess.check_output('cd '+pth+';grep " METDAT " calpuff.inp|grep \!|cut -d"=" -f2',shell=True).decode('utf8').strip('\n')
if '/' not in met_pth:
  met_pth='/Users/cpuff/UNRESPForecastingSystem/CALPUFF_OUT/CALMET/20200415/calmet.dat'
  cmd+='ln -s '+met_pth+' .;'
cmd+='cp '+ WEB + '/cpuff_results/demo/autorefresh.html prog.html;'
cmd+='sed -ie "s/RAND/'+ran+'/g" prog.html;'
cmd+=RUNMDL+'&disown;echo $!'
kname=[]
#for p in pname[:]:
#  cmd+=DAT2KML+' -f '+p+';'
#  kname.append(p+'.kml')
pid=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n')
if len(pid)==0:
  fn='CALPUFF.LST'
  print """Something wrong in Model excutions, see <a href="%s">%s</a>
  </body></html>
  """  % (rrn+fn,fn)
  sys.exit()
# The cpuff721 is running, initiate the waitc.cs to generate cpuff.out for showing progress
cmd ='cd '+pth+';'
cmd+='time '+WAITC+' '+pth+' '+pid+' &disown'
os.system(cmd)

#Store the PID, RAND, and DATE
HIS='/Library/WebServer/Documents/cpuff_results/his.txt'
DATE=subprocess.check_output('date -j +"%Y-%m-%d_%H:%M"',shell=True).decode('utf8').strip('\n')
cmd ='if ! [ -e '+HIS+' ];then echo PID, RAND, DATE >'+HIS+';fi;'
cmd+='echo '+pid+', '+ran+', '+DATE+'>>'+HIS
os.system(cmd)

#The Resultant File Links
fnames=subprocess.check_output('sleep 1;ls '+pth,shell=True).decode('utf8').split('\n')
fnames+=['calpuff.con.S.grd02.nc']
fnames=[fn for fn in fnames if len(fn)>0 and 'html' not in fn]
fnames.sort()

print 'pid= '+pid+'<a href="'+rrn+'prog.html" target="_blank">(check progress)</a></br>'
print """\
  <p>Model_results:</br>
  """
for fn in fnames:
  fname=rrn+fn
  print """\
  <p><a href="%s">%s</a></br>
  """  % (fname,fn)
print '</body></html>'

