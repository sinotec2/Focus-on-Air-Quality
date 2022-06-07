#root@114-32-164-198 /Library/WebServer/CGI-Executables
# cat ./isc/OLM.py
#!/opt/anaconda3/envs/py27/bin/python
# -*- coding: UTF-8 -*-

import cgi, os, sys
import cgitb; cgitb.enable()
from pandas import *
import numpy as np
import json
import datetime
import tempfile as tf

form = cgi.FieldStorage()
nTimeISC,nTimeAER=(6,8)
nTIME={'ISCST3':nTimeISC,'AERMOD':nTimeAER}

ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')
pth='/tmp/isc/'
os.system('mkdir -p '+pth)
WEB='/Library/WebServer/Documents/'
pth=WEB+'isc_results/OLMs_'+ran+'/'
os.system('mkdir -p '+pth)
rst=pth #'/Library/WebServer/Documents/isc_results/'
sph='/opt/local/bin/specHrSliderRect.py'
kml='/opt/local/bin/dat2kml.py'
zpp='/usr/bin/zip'
un={'gz':'/usr/bin/gunzip','zip':'/usr/bin/unzip'}
NS=3 #nearest stations
NUL=' >&/dev/null'
os.system('mkdir -p /tmp/wrose')
fileitem = form['filename']
if fileitem.filename:
  fn = os.path.basename(fileitem.filename)
  open(pth+fn, 'wb').write(fileitem.file.read())
  os.system('echo "start! ">/tmp/wrose/wrose.out')
  ext=fn.split('.')[-1]
  if ext in ['gz','zip']:
    cmd=un[ext]+' '+pth+fn+NUL
    os.system(cmd)
    os.system('echo "OK! '+cmd+'">>/tmp/wrose/wrose.out')
    fn=fn.replace(ext,'')[:-1]
    ext=fn.split('.')[-1]
  root=fn.replace(ext,'')[:-1]
#if True==True:
#  fn='result.dat'
  with open(pth+fn,'r') as f:
    ll=[l for l in f]
  model=ll[0].split()[1]
  m=nTIME[model]
  head=ll[:8]
  ll=ll[8:]
  HR=[int(l.split()[m]) for l in ll]
  HRs=list(set(HR))
  HRs.sort()
  NHR=len(HRs)
  bdate=datetime.datetime.strptime(str(HRs[0]),'%y%m%d%H')
  edate=bdate+datetime.timedelta(days=1)
  begdate, enddate=(i.strftime('%Y%m%d') for i in [bdate,edate])

  twdX,twdY=([float(l.split()[m]) for l in ll] for m in range(2))
  twdX,twdY=([int(l) for l in twdX],[int(l) for l in twdY])
  centXY=((max(twdX)+min(twdX))/2,(max(twdY)+min(twdY))/2)
  NRE=len(twdX)
  if NHR>1:
    NRE=HR.index(HRs[1])
    enddate=str(2000*100*100+HRs[-1]//100)
  twdX=np.array(twdX).reshape(NHR,NRE)
  twdY=np.array(twdY).reshape(NHR,NRE)
  HR=np.array(HR).reshape(NHR,NRE)
  netID=[l.split()[m+1]  for l in ll]
  GRD=set(netID)
  NRcart,NRdisc,discID=NRE,0,[]
  if 'NA' in GRD:
    NRdisc=netID.count('NA')/NHR
    discID=np.where(np.array(netID[:NRE])=='NA')[0]
    NRdisc=len(discID)
    NRcart=NRE-NRdisc
  fnameR=root+'_rep.txt'
  with open(rst+fnameR,'w') as f:
    for i in range(5):
      f.write(head[i])
    if NRcart>0:
      f.write('*         NUM OF GRIDCART: '+str(NRcart)+'\n')
    if NRdisc>0:
      f.write('*         NUM OF DISCCART: '+str(NRdisc)+'\n')
    f.write('* NUMBER OF SIMULATION HOURS IS: {:d},'.format(NHR))
    f.write('*   FROM {:s} TO {:s} \n'.format(begdate, enddate))

# prepare the observations of NO2 and O3 from the nearest NS EPA stations

# The locations of stations
  fname='/Users/Data/cwb/e-service/surf_trj/sta_list.txt_utm'
  with open(fname,'r') as f: #, encoding='big5') as f:
#(py37)  with open(fname,'r', encoding='big5') as f:
    sta=[l.split() for l in f]
#(py37)    sta=[l.encode('big5').split() for l in f]
  ID=[str(int(l[0])) for l in sta[1:]]
  staX,staY=([float(l[i]) for l in sta[1:]] for i in [2,3])
  dfs=DataFrame({'ID':ID,'twdX':staX,'twdY':staY})

# distance of EPA stations to center of netID's
  dfs['dist']=[(x-centXY[0])**2+(y-centXY[1])**2 for x,y in zip(dfs.twdX,dfs.twdY)]
  dfs=dfs.sort_values('dist',ascending=True).reset_index(drop=True)
# station names
  fname='/Users/Data/cwb/e-service/surf_trj/sta_list.json'
  fn=open(fname)
  d_nstnam=json.load(fn)
  stnames=[d_nstnam[dfs.loc[i,'ID']] for i in range(NS)]
# perform the extraction of EPA data
  for stn in stnames:
    fname= rst+'NO2O3'+stn+begdate+enddate+'.csv'
    if os.path.isfile(fname):continue
    cmd ='cd '+rst+';'
    cmd+= sph+' -t '+stn+' -s NO2,O3 -b '+begdate+' -e '+enddate+' -a s>>/tmp/wrose/wrose.out'
    os.system(cmd)
    os.system('echo "OK! '+cmd+'">>/tmp/wrose/wrose.out')
  with open(rst+fnameR,'a') as f:
    f.write('* NEAREST {:d} STATIONS ARE: {:s} {:s} {:s}\n'.format(NS,stnames[0],stnames[1],stnames[2]))

  C=np.array([float(l.split()[2]) for l in ll]).reshape(NHR,NRE)
  csvs=''
  for js in range(NS):
    fname= 'NO2O3'+stnames[js]+begdate+enddate+'.csv'
    csvs+=' '+fname
    os.system('echo "OK!'+fname+'">>/tmp/wrose/wrose.out')
    df=read_csv(rst+fname)
    df['yMDH2']=[(i+1)-2000*100*100*100 for i in df.YMDH]
    df=df.loc[df.yMDH2.map(lambda x:x in HRs)].reset_index(drop=True)
    os.system('echo "OK!df'+fname+'">>/tmp/wrose/wrose.out')
    for v in 'O3b NO2b mnO3C'.split():
      exec(v+'=np.zeros(shape=(NHR,NRE))')
    for i in range(NRE):
      NO2b[:,i]=df.NO2[:]
      O3b[:,i]=df.O3[:]
      for j in range(NHR):
        mnO3C[j,i]=min([0.9*C[j,i],O3b[j,i]])
    OLM=0.1*C+NO2b+mnO3C
    maxC=np.max(OLM,axis=0)
    maxH=np.array([np.where(OLM[:,i]==maxC[i])[0][0] for i in range(NRE)]).flatten()
    HMNO2,HMO3=list(df.loc[df.NO2==max(df.NO2),'YMDH'])[0],list(df.loc[df.O3==max(df.O3),'YMDH'])[0]
    fnameO=root+'_'+stnames[js]+'.dat'
    with open(rst+fnameO,'w') as f:
      for  i in range(8):
        f.write(head[i])
      for  i in range(NRE):
        f.write('{:d} {:d} {:f} {:d}\n'.format(twdX[0,i],twdY[0,i],maxC[i],HR[maxH[i],0]))
    with open(rst+fnameR,'a') as f:
      f.write('*   MAX (NO2B,O3B) FOR {:s} STATIONS ARE: {:f} {:f}\n'.format(stnames[js],max(df.NO2),max(df.O3)))
      f.write('*                             MAX HR ARE: {:d} {:d}\n'.format(HMNO2,HMO3))
      maxi=list(maxC).index(max(maxC))
      maxi_h=np.where(OLM[:,maxi]==maxC[maxi])[0][0]
      f.write('*   MAX OLM_NO2 IN ALL RECPTs FOR {:s} STATIONS IS: {:f}'.format(stnames[js],max(maxC)))
      XM,YM,HM=twdX[maxi_h,maxi],twdY[maxi_h,maxi],HR[maxi_h,maxi]
      NO2M,O3M=list(df.loc[df.yMDH2==HM,'NO2'])[0],list(df.loc[df.yMDH2==HM,'O3'])[0]
      f.write(' MAX HR IS : {:d}'.format(HM))
      f.write(' MAX XY ARE: ({:d}, {:d})\n'.format(XM,YM))
      f.write('*   (NO2B,O3B) FOR {:s} AT THAT TIME: {:f} {:f}\n'.format(stnames[js],NO2M,O3M))
      if NRcart>0:
        maxi=list(maxC[:NRcart]).index(max(maxC[:NRcart]))
        maxi_h=np.where(OLM[:,maxi]==maxC[maxi])[0][0]
        XM,YM,HM=twdX[maxi_h,maxi],twdY[maxi_h,maxi],HR[maxi_h,maxi]
        NO2M,O3M=list(df.loc[df.yMDH2==HM,'NO2'])[0],list(df.loc[df.yMDH2==HM,'O3'])[0]
        f.write('*   MAX OLM_NO2 IN GRIDCART   FOR {:s} STATIONS IS: {:f}'.format(stnames[js],maxC[maxi]))
        f.write(' MAX HR IS : {:d}'.format(HM))
        f.write(' MAX XY ARE: ({:d}, {:d})\n'.format(XM,YM))
        f.write('*   (NO2B,O3B) FOR {:s} AT THAT TIME: ({:f}, {:f})\n'.format(stnames[js],NO2M,O3M))
      if NRdisc>0:
        f.write('*   MAX OLM_NO2 IN DISCCART   FOR {:s} STATIONS ARE:'.format(stnames[js]))
        for i in range(NRdisc):
          maxi=i+NRcart
          f.write('{:f}@{:d}, '.format(maxC[maxi],HR[maxH[maxi],maxi]))
        f.write('\n')
        f.write('*   (NO2B,O3B) FOR {:s} AT THAT TIME:'.format(stnames[js]))
        for i in range(NRdisc):
          maxi=i+NRcart
          HM=HR[maxH[maxi],maxi]
          NO2M,O3M=list(df.loc[df.yMDH2==HM,'NO2'])[0],list(df.loc[df.yMDH2==HM,'O3'])[0]
          f.write('({:f}, {:f}), '.format(NO2M,O3M))
        f.write('\n')

  for stn in stnames:
    cmd ='cd '+rst+';'
    cmd+= kml+' -d ALL -f '+root+'_'+stn+'.dat >>/tmp/wrose/wrose.out'
    os.system(cmd)
    os.system('echo "OK! '+cmd+'">>/tmp/wrose/wrose.out')
#zip

cmd ='cd '+rst+';'
cmd+= zpp+' '+root+'_ALL.zip '+root+'_* '+csvs+NUL
os.system(cmd)
os.system('echo "OK! '+cmd+'">>/tmp/wrose/wrose.out')

os.system('echo "OK!">>/tmp/wrose/wrose.out')
fn=rst+root+'_ALL.zip'
fn2=fn.replace('/Library/WebServer/Documents','../..')
print """\
Content-Type: text/html\n\n
<html><head><title>OLM results</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
<script>$(function(){$('a[data-auto-download]').each(function(){var $this=$(this);setTimeout(function(){window.location=$this.attr('href');},100000);});});</script>
</head>
<body>
<p>The resultant ZIP will be automatically downloaded shortly. If it doesn't, click
 <a data-auto-download href="%s">%s</a></p>
</body>
</html>
""" % (fn2,fn2.split('/')[-1])
