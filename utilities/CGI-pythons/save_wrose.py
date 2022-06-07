#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb; cgitb.enable()


form = cgi.FieldStorage()

pth='/tmp/wrose/'
fileitem = form['filename']
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
#fn='46692v01.txt'
os.system('echo "OK!">/tmp/wrose/wrose.out') 
wrose='/opt/local/bin/wrose.py'  
cmd='cd '+pth+';export PATH=/opt/anaconda3/bin/:$PATH;'+wrose+' '+pth+fn+' >>/tmp/wrose/wrose.out'
os.system('echo "'+cmd+'">>/tmp/wrose/wrose.out') 
os.system(cmd)
os.system('echo "OK 2!">>/tmp/wrose/wrose.out') 
cmd='cp '+pth+fn+'.png /Library/WebServer/Documents/wrose_png;'
cmd+='cp '+pth+fn+'.png /Library/WebServer/Documents/wrose_png/example.png'
os.system('echo "'+cmd+'">>/tmp/wrose/wrose.out') 
os.system(cmd)
os.system('echo "OK 3!">>/tmp/wrose/wrose.out') 
#if rst !=0:
#  os.system('echo "something wrong in wrose.py process!"+str(rst)+'>>/tmp/wrose/wrose.out') 
#  sys.exit()

fn2='../../wrose_png/'+fn+'.png'
os.system('echo '+fn2+'>>/tmp/wrose/wrose.out')
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
