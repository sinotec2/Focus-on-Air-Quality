#kuang@node03 /nas1/Data/javascripts/D3js/earth/public/data/weather/current
#$ cat earth_dens.py
#!/usr/bin/python
import numpy as np
import os, sys, json
path=sys.argv[1]
root=path+'00-pres-isobaric-1000hPa-gfs-1.0.json'
fnames=[root,root.replace('pres','temp'),root.replace('pres','air_density')]
fnames.append(root.replace('pres','ozone'))
with open(fnames[0],'r') as f:
  pres=json.load(f)
with open(fnames[1],'r') as f:
  temp=json.load(f)
R=8.3144598
T=np.array(temp[0]['data'][:])
P=np.ones(shape=T.shape)*100000.
unit="m3.Pa.K-1.mol-1"
air_mw=28.97
D=P/(R*T)*air_mw/1000.
temp[0]['data']=list(D)
dens=temp
with open(fnames[2],'w') as f:
  json.dump(dens,f)


with open(fnames[3],'r') as f:
  ozone=json.load(f) #kg/kg
O=np.array(ozone[0]['data'][:])*air_mw/48.*1.E9
ozone[0]['data']=list(O)
with open(fnames[3],'w') as f:
  json.dump(ozone,f)
