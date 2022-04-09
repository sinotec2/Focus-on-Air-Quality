import numpy as np
with open('central_campus.dat','r') as f:
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
run=lines[iend]
VPH=[float(i) for i in lines[iend+1].split()]
EMF=[float(i) for i in lines[iend+2].split()]
for var in 'U,BRG,CLAS,MIXH,SIGM,AMB,T'.split(','):
    exec(var+'=np.zeros(shape=NM)')
istr=iend+3
iend=istr+NM
for i in range(NM):
    U[i],BRG[i],CLAS[i],MIXH[i],SIGM[i],AMB[i],T[i]=[float(j) for j in lines[istr+i].split()]