import netCDF4
import os, sys

path='/nas1/TEDS/teds11/'
mo=int(sys.argv[1])
for m in range(mo,mo+1):
  mm='{:02d}'.format(m)
  P=path+'ptse/fortBE.413_teds10.ptsE'+mm+'.nc'
  S=path+'ship/fortBE.413_teds10.HRBE'+mm+'.nc'
  O='fortBE.413_teds11.ptse'+mm+'.nc'
  os.system('cp '+P+' '+O)
  pt = netCDF4.Dataset(P, 'r')
  ncs = netCDF4.Dataset(S, 'r')
  nco = netCDF4.Dataset(O, 'r+')
  v3=list(filter(lambda x:pt.variables[x].ndim==3, [i for i in pt.variables]))
  v2p=list(filter(lambda x:pt.variables[x].ndim==2, [i for i in pt.variables]))
  v2s=list(filter(lambda x:ncs.variables[x].ndim==2, [i for i in ncs.variables]))
  v1=list(filter(lambda x:pt.variables[x].ndim==1, [i for i in pt.variables]))
  nhr,nvar,dt=pt.variables[v3[0]].shape
  nt,noptsp=pt.variables[v2p[0]].shape
  nt,noptss=ncs.variables[v2s[0]].shape
  nopts=noptsp+noptss
  v2p1=[i for i in v2p if i!='CP_NO']
  v='CP_NO'
  for c in range(noptsp,nopts):
    nco.variables[v][c,:]=ncs.variables[v][c-noptsp,:]
  for v in v1:
    for c in range(noptsp,nopts):
      nco.variables[v][c]=ncs.variables[v][c-noptsp]
  for v in v2p1:
    for c in range(noptsp,nopts):
      nco.variables[v][:,c]=0.
      if v in v2s:
        nco.variables[v][:,c]=ncs.variables[v][:,c-noptsp]
  nco.NCOLS=nopts
  nco.close()
