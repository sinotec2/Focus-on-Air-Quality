#!/opt/anaconda3/envs/py27/bin/python
# /cluster/miniconda/envs/py37/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb 
import tempfile as tf

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
CUT=' |cut -c 1-44 >& tmp.PLT'	
FIT='/Users/Data/GIS/OSM_20210318/merged_GeoTIFF/tiles_to_tiffFit.py '
OVL='/Users/Data/GIS/OSM_20210318/merged_GeoTIFF/NCLonOTM.py'
NCL='mkdir -p /tmp/wrose;source /opt/local/bin/conda_ini ncl_stable >/tmp/wrose/wrose.out;'+\
	'/opt/anaconda3/envs/ncl_stable/bin/ncl /Users/Data/GIS/OSM_20210318/merged_GeoTIFF/PLT_cn.ncl'
NULL=' >&/dev/null'
pth=WEB+'isc_results/cntr_'+ran+'/'
OUT=' >> '+pth+'isc.out'
SED='/usr/bin/sed "1,8d" '

os.system('mkdir -p '+pth)

def PLT_parser(fname):
  with open(fname,'r') as f:
    l=[line.strip('\n') for line in f]
  X,Y=([float(l[i].split()[j]) for i in range(len(l))] for j in range(2))
  sX ,sY=list(set(X)),list(set(Y))
  sX.sort()
  sY.sort()
  nx,ny=len(sX),len(sY)
  dx,dy=[sX[i+1]-sX[i] for i in range(nx-1)],[sY[i+1]-sY[i] for i in range(ny-1)]
  if len(set(dx))!=1 or len(set(dy))!=1:
    sys.exit('not a regular RE GRIDCART system')
  return ' {:f} {:d} {:f} {:f} {:d} {:f} '.format(min(X),nx,set(dx),min(Y),ny,set(dy))


print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')

form = cgi.FieldStorage()
STR = str(form.getvalue("iscinp"))
os.system('echo "'+STR+'"'+OUT)
if len(STR)>=4: #in case of input a string
  cmd ='cd '+pth+';'	  
  cmd+= FIT+STR+OUT+';'	
  os.system('echo "'+cmd+'"'+OUT)
  r=os.system(cmd+OUT)
  if r!=0:sys.exit('error in ncl')
  fnames=['fitted.png']
else:	
  fileitem = form['filename']
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
    cmd ='cd '+pth+';'	  
    if pth+fn!=pth+'userinp.PLT': cmd+='cp '+pth+fn+' '+pth+'userinp.PLT;'
    cmd+= FIT+fn+OUT+';'	
    cmd+= SED+'userinp.PLT'+CUT+';'
    os.system('echo "'+cmd+'"'+OUT)
    r=os.system(cmd+OUT)
#    STR=PLT_parser(pth+'tmp.PLT')	
#    cmd ='echo "'+STR+'">param.txt;'
    cmd ='cd '+pth+';'	  
    cmd+='echo "'+fn+'">title.txt;'
    cmd+= NCL+OUT+';'
    cmd+= OVL
    os.system('echo "'+cmd+'"'+OUT)
    r=os.system(cmd+OUT)
    if r!=0:sys.exit('error in ncl')
    fnames=['fitted.png','tmp_cn.png',"NCLonOTM.png"]
 
for fn in fnames:
  fname=pth+fn
  print """\
  <a data-auto-download href="%s">%s</a>
  """  % (fname.replace(WEB,'../../../'),fname.split('/')[-1])
print """\
  </body>
  </html>
  """


