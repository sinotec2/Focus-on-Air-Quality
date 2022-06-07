#!/opt/anaconda3/envs/py27/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb; cgitb.enable()
from pandas import *
import numpy as np

form = cgi.FieldStorage()

pth='/tmp/wrose/'
os.system('mkdir -p '+pth)
rst='/Library/WebServer/Documents/taiwan/'
fileitem = form['filename']
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
df=read_csv(pth+fn,header=None)
col=['c','t','v']
df.columns=col
counties=list(set(df.c))
if counties[0]<=99:
  dft=read_csv('/Users/Data/gis/TWN_town/record2.csv')
  O2N={i:j for i,j in zip(list(dft.TOWNCODE_old),list(dft.TOWNCODE))}
  if len(set(df.t)-set(dft.TOWNCODE_old))>0:
    sys.exit('wrong TOWNCODE_old')
  cnt_t=[O2N[i] for i in df.t]
  df.c=[int(t//1000) for t in cnt_t]
  df.t=[int(i%1000) for i in cnt_t]
  counties=list(set(df.c))
df.set_index('c').to_csv(rst+'input.csv',header=None)
with open(rst+"counties.txt",'w') as f:
  for c in counties:
    f.write("{:05d}\n".format(c))

cmd ='source /opt/local/bin/conda_ini ncl_stable >/tmp/wrose/wrose.out;'
cmd+='cd '+rst+';'
cmd+='/opt/anaconda3/envs/ncl_stable/bin/ncl stw.ncl>>/tmp/wrose/wrose.out;'
cmd+='cp ./shapefile_3.png ./'+fn+'.png'
os.system('echo "'+cmd+'">>/tmp/wrose/wrose.out') 
os.system(cmd)
os.system('echo "OK 3!">>/tmp/wrose/wrose.out') 

fn2='../../taiwan/'+fn+'.png'
print """\
Content-Type: text/html\n\n
<html><head><title>wrose results</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
<script>$(function(){$('a[data-auto-download]').each(function(){var $this=$(this);setTimeout(function(){window.location=$this.attr('href');},2000);});});</script>
</head>
<body>
<p>The resultant PNG will be automatically downloaded shortly. If it doesn't, click <a data-auto-download href="%s">%s</a></p>
</body>
</html>
""" % (fn2,fn2.split('/')[-1])
