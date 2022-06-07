# cat ./isc/AERMOD.py
#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb
import subprocess
import tempfile as tf

WEB='/Library/WebServer/Documents'
CGI='/Library/WebServer/CGI-Executables/isc/'
AERMOD='/Users/1.PlumeModels/AERMOD/aermod_source/aermod.exe'
ISCST3='/Users/1.PlumeModels/ISC/short_term/src/iscst3.exe'
WAITC=WEB+'/isc_results/waitc.cs'
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
rrn='/isc_results/'+ROT+'_'+ran+'/'
pth=WEB+rrn
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
kname=[p+'.kml'for p in pname[:]]
#execution of model

cmd ='cd '+pth+';'
#progression checking webpage
cmd+='cp '+ WEB + '/isc_results/demo/autorefresh.html prog.html;'
cmd+='sed -ie "s/RAND/'+ran+'/g" prog.html;'
cmd+=RUNMDL+' '+iname+' '+oname+OUT+';'
cmd=cmd.strip(';')
os.system('echo "'+cmd+'"'+OUT)
pid=subprocess.check_output(cmd+OUT+'&disown;echo $!',shell=True).decode('utf8').strip('\n')
if len(pid)==0:
  print """Something wrong in Model excutions, see <a href="%s" target="_blank">%s</a>
  </body></html>
  """  % (rrn+ename,ename)
  sys.exit()
# The model is running, initiate the waitc.cs to generate log.out for showing progress
cmd ='cd '+pth+';'
cmd+='time '+WAITC+' '+pth+' '+pid+' &disown'
os.system(cmd)

print 'pid= '+pid+'<a href="'+rrn+'prog.html" target="_blank">(check progress)</a></br>'

fnames=[ename,oname,pth+'isc.out']+pname+sname+kname
print """\
  <p>Model_results: The Model process should be ended in 3 min. After that You may click:</br>
  """
for fn in fnames:
  fname=pth+fn
  print """\
  <a href="%s" target="_blank">%s</a></br>
  """  % (fname.replace(WEB,'../../..'),fname.split('/')[-1])
print '</body></html>'
