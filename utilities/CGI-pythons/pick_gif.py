#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import subprocess
import tempfile as tf

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
AERMOD='/Users/1.PlumeModels/AERMOD/aermod_source/aermod.exe'
ISCST3='/Users/1.PlumeModels/ISC/short_term/src/iscst3.exe'
DAT2KML='/opt/local/bin/dat2kml.py'
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
try:
  cpu=float(subprocess.check_output('/opt/local/bin/cpu',shell=True).decode('utf8').strip('\n').strip('%'))
except:
  sys.exit('cpu fail')
if cpu>=550:
  print 'total kerels used: '+str(cpu)+'%,  too many iscst or aermod processes are running, please wait. </br>'
  print '</body></html>'
  sys.exit()
  
form = cgi.FieldStorage()
model = form.getvalue('model')
ROT='isc3'
if model=='AERMOD': ROT='arem'

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth=WEB+'isc_results/'+ROT+'_'+ran+'/'
OUT='>> '+pth+'isc.out'
os.system('mkdir -p '+pth)

RUNMDL=ISCST3
if model=='AERMOD': RUNMDL=AERMOD
inames=[]
for nf in '1234':
  fileitem = form['filename'+nf]
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
    inames.append(pth+fn)	
  else:
    if nf=='4':continue  
    if model=='ISCST' and nf=='3':continue  
    print 'Absent of file number: '+nf+'</body></html>'
    sys.exit('err input file')	

ename=subprocess.check_output('grep ERRORFIL '+inames[0],shell=True).decode('utf8').strip('\n').split()[1]
pname=subprocess.check_output('grep PLOTFILE '+inames[0]+'|awk "{print \$NF}"',shell=True).decode('utf8').strip('\n').split()
sname=subprocess.check_output('grep SUMMFILE '+inames[0]+'|awk "{print \$NF}"',shell=True).decode('utf8').strip('\n').split()
ext=inames[0].split('.')[-1]
iname=inames[0].split('/')[-1]
oname=iname.replace(ext,'out')
cmd ='cd '+pth+';'	  
cmd+=RUNMDL+' '+iname+' '+oname+OUT+';'
kname=[]
#for p in pname[:]:
#  cmd+=DAT2KML+' -f '+p+';'
#  kname.append(p+'.kml')
cmd=cmd.strip(';')  
os.system('echo "'+cmd+'"'+OUT)
r=os.system(cmd+OUT+'&disown')
if r!=0:
  print """Something wrong in Model excutions, see <a data-auto-download href="%s">%s</a>
  </body></html>
  """  % (ename.replace(WEB,'../../'),ename.split('/')[-1])
  sys.exit()

model=model.lower()
pid=subprocess.check_output('ps -ef|grep '+model+'|grep -v grep|tail -n1|/opt/local/bin/awkk 2',shell=True).decode('utf8').strip('\n')
print 'pid= '+pid+'</br>'
ndays='365'
ifirst=1
while True:
  now=subprocess.check_output('grep "Data For Day No." '+pth+'isc.out|tail -n2|head -n1',shell=True).decode('utf8').strip('\n')
  print now+'</br>'
  break
  if '20' in now and ifirst==1:
    yr=int(now.split()[-1])
    if yr%4==0:ndays='366'
    ifirst=0
  if ndays in now:break
  os.system('sleep 30s')
fnames=[ename,oname,pth+'isc.out']+pname+sname+kname
print """\
  <p>Model_results: The Model process should be ended in 3 min. After that You may click:</br>
  """
for fn in fnames:
  fname=pth+fn
  print """\
  <a data-auto-download href="%s">%s</a></br>
  """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print '</body></html>'


