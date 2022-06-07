# cat ./isc/bpipprim.py
#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb
import tempfile as tf

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
GREP='/usr/bin/grep --color=never'
NULL=' >&/dev/null'

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth=WEB+'isc_results/bpip_'+ran+'/'
os.system('mkdir -p '+pth)
OUT='>> '+pth+'isc.out'
BPIP='/Users/1.PlumeModels/ISC/BPIPPRM/bpipprm'
form = cgi.FieldStorage()
STR = str(form.getvalue("iscinp"))
os.system('echo "'+STR+'"'+OUT)
if len(STR)<=4: #in case of input a SO/RE file
  fileitem = form['filename']
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
else:
    with open(pth+fn,'w') as ftext:
      ftext.write(STR)
cmd ='cd '+pth+';'
if pth+fn!=pth+'fort.10': cmd+='cp '+pth+fn+' '+pth+'fort.10;'
cmd+=BPIP
os.system('echo "'+cmd+'"'+OUT)
os.system(cmd+OUT)
cmd ='cd '+pth+';'
cmd+= BPIP+NULL+';'
cmd+= GREP+" ' SO ' fort.12 >build.txt"
os.system(cmd)

fnames=[pth+i for i in [fn,'build.txt','fort.12','fort.14']]
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')
fname=fnames[0]
print """\
<p>filename given and save as: <a href="%s" target="_blank">%s</a></br></p>
"""% (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print """\
  <p>BPIPPRIN_results: The download process should start shortly. If it doesn't, click:</p>
  """
for fname in fnames[1:]:
  print """\
  <a href="%s" target="_blank">%s</a>
  """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print """\
  </body>
  </html>
  """
