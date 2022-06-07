#!/opt/anaconda3/envs/py27/bin/python
#/usr/bin/python
import os, sys

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
pth='./'
OUT='>> '+pth+'isc.out'

STR = sys.argv[1]
if '\n' in STR:STR=STR.replace('\n','')
os.system('echo "'+STR+'"'+OUT)
#read the name of RE_net
reg='GRIDCART'
if reg not in STR:
  os.system('echo "'+reg+' not in STR!" '+OUT)
  sys.exit(reg+' not in STR!')
inam=STR.index(reg)
inp=STR[(inam+len(reg)):].split()
snamo=inp[0]

#read the others
inc='XYINC'
iinc=STR.index(inc)
inp=STR[(iinc+len(inc)):]
fname=pth+snamo+'.zip'
geninp='/opt/local/bin/gen_inp.py'
aermap='/opt/local/bin/aermap'
#cmd ='cd '+pth+';'
cmd ='sed s/test/'+snamo+'/g '+WEB+'trj_results/aermap.inp_template>aermap.inp;'
os.system(cmd)
#cmd ='cd '+pth+';'
cmd = geninp+' '+snamo+' '+inp+' >>geninp.out;'
os.system(cmd)
cmd ='cd '+pth+';'
cmd+= aermap+OUT+';'
rst=os.system(cmd)
