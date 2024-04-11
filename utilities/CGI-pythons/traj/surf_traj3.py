#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb
import tempfile as tf
import json

form = cgi.FieldStorage()
dirTJ={'b':'T','f':'F'} #back->true; foreward->false
nam = form.getvalue('AQSname')
try:
  ist=int(nam)
except:
  AQ=nam
else:
  fn = open('/Users/Data/cwb/e-service/surf_trj/sta_list.json')
  d_nstnam = json.load(fn)
  AQ=d_nstnam[nam]
os.system('echo '+AQ+'>&/tmp/trj.out')
DIR = form.getvalue("dirFB")
TF=dirTJ[DIR[0]]
num = form.getvalue("number")
dat = form.getvalue("date")
message='../../trj_results/'+DIR+AQ+dat+num+'.csv'
print """\
Content-Type: text/html\n\n
<html>
<head>
  <title>TRAJ KML result</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
      <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
      <script>
      $(function() {
              $('a[data-auto-download]').each(function(){
                      var $this = $(this);
                      setTimeout(function() {
                      window.location = $this.attr('href');
                      }, 2000);
              });
      });
      </script>
</head>
"""
if os.path.isfile('/Library/WebServer/Documents/'+message[6:]):
  print """\
  <body>
  <p>The assigned KML file has been created and maybe downloaded in your Downloads directory.</p>
  <p>You may re-download by clicking this <a href="%s">link</a>, or...</p>
  <p> submit the KML file at Google Maps or OpenStreet interface at the
  <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
  <p> return to the previous page and redefine the trajectory.</p>
  </body>
  </html>
  """  % (message+'.kml')
else:
  os.system('cd /Library/WebServer/Documents; \
  /Users/Data/cwb/e-service/surf_trj/traj2kml.py -t '+AQ+' -d '+dat+num+' -b '+TF+ '>>/tmp/trj.out')
  print """\
  <body>
  <p>The KML download should start shortly. If it doesn't, click
  <a data-auto-download href="%s">here</a>.</p>
  <p>The KML may be posted on google map or OpenStreet interface:
  <a href=http://114.32.164.198/Leaflet/docs/index.html>Leaflet</a>.</p>
  </body>
  </html>
  """  % (message+'.kml')
