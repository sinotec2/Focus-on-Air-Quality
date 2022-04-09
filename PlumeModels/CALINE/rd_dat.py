import numpy as np
import fortranformat as ff
import sys

fnameI=sys.argv[1]
fnameO=fnameI.replace('.dat','3.INP')
with open(fnameI,'r') as f:
  lines=[i.strip('\n') for i in f]
job=lines[0].strip(' ')
z0,mw,vs,vd,NR,NL,ATIM,SCAL,NM,ASL=[float(i) for i in lines[2].split()]
NR,NL,NM=[int(i) for i in [NR,NL,NM]]
recp=[lines[i] for i in range(3,NR+3)]
xr,yr,zr=np.zeros(shape=NR),np.zeros(shape=NR),np.zeros(shape=NR)
for i in range(NR):
  xr[i],yr[i],zr[i]=[float(j) for j in lines[3+NR+i].split()]
lnks=[lines[i] for i in range(NR*2+3,NR*2+3+NL)]
for var in 'X1,Y1,X2,Y2,H,W,CBMl,CBMr,D'.split(','):
  exec(var+'=np.zeros(shape=NL)')
istr=NR*2+3+NL
iend=istr+NL
for var in 'TYP,X1,Y1,X2,Y2,H,W,CBMl,CBMr,D'.split(','):
  exec(var+'=np.zeros(shape=NL)')
for i in range(NL):
  TYP[i],X1[i],Y1[i],X2[i],Y2[i],H[i],W[i],CBMl[i],CBMr[i],D[i]=[float(j) for j in lines[istr+i].split()]
dtyp={1:'AG',2:'DP',3:'FL',4:'BR'}
TYP=[dtyp[int(i)] for i in TYP] #change int to A2
ATIM*=60. #change hour to min
run=lines[iend]
VPH=[float(i) for i in lines[iend+1].split()]
EMF=[float(i) for i in lines[iend+2].split()]
for var in 'U,BRG,CLAS,MIXH,SIGM,AMB,T'.split(','):
  exec(var+'=np.zeros(shape=NM)')
istr=iend+3
iend=istr+NM
for i in range(NM):
  BRG[i],U[i],CLAS[i],MIXH[i],SIGM[i],AMB[i],T[i]=[float(j) for j in lines[istr+i].split()]
CLAS=[min([6,i]) for i in CLAS]

#1:SITE VARIABLES, 2:RECEPTOR LOCATIONS, 3:RUN CASE, 4:LINK VARIABLES, 5:MET CONDITIONS
fmt=['A40,2F4.0,2F5.0,I2,F10.0','A12,8X,3F10.0',  'A40,2I3',  'A8,12X,A2,4F7.0,F8.0,3F4.0',      'F3.0,F4.0,I1,F6.0,F4.0']
var=[(job,ATIM,z0,vs,vd,NR,SCAL),(recp,xr,yr,zr),(run,NL,NM),(lnks,TYP,X1,Y1,X2,Y2,VPH,EMF,H,W),(U,BRG,CLAS,MIXH,AMB)]
nln=[1,NR,1,NL,NM]
lns=[]
for ig in range(5):
  w_line = ff.FortranRecordWriter(fmt[ig])
  if ig in [0,2]:
    lns.append(w_line.write([v for v in var[ig]])+'\n')
  else:
    for l in range(nln[ig]):
      lns.append(w_line.write([v[l] for v in var[ig]])+'\n')
with open(fnameO,'w') as f:
  for l in lns:
    f.write(l)
