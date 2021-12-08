import numpy as np
from pandas import *
import sys, os, subprocess
import netCDF4
from datetime import datetime, timedelta
import twd97
from include2 import rd_ASnPRnCBM_A

def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)

def jul2dt(jultm):
  jul,tm=jultm[:]
  yr=int(jul/1000)
  ih=int(tm/10000.)
  return datetime(yr,1,1)+timedelta(days=int(jul-yr*1000-1))+timedelta(hours=ih)

def disc(dm,nc):
#discretizations
  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
  dm['IX']=np.array((dm.UTME-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
  dm['IY']=np.array((dm.UTMN-Ycent-nc.YORIG)/nc.YCELL,dtype=int)
  #time_const or time_variant df files
  if 'JJJHH' not in dm.columns:
    dmg=pivot_table(dm,index=['nsc2','IX','IY'],values=cole,aggfunc=sum).reset_index()
  else:
    dmg=pivot_table(dm,index=['IX','IY','JJJHH'],values=cole,aggfunc=sum).reset_index()
  return dmg

#A simple scheme is in place for PM splitting, and the SPECCIATE is not adopted.
def add_PMS(dm):
  #add the PM columns and reset to zero
  colc=['CCRS','FCRS','CPRM','FPRM']
  for c in colc:
    dm[c]=np.zeros(len(dm))
  #in case of non_PM sources, skip the routines
  if 'EM_PM' not in dm.columns or sum(dm.EM_PM)==0:return dm
  # fugitive sources
  not_burn=dm.loc[dm.EM_NOX+dm.EM_CO+dm.EM_SOX==0]
  crst=not_burn.loc[not_burn.EM_PM>0]
  idx=crst.index
  dm.loc[idx,'FCRS']=np.array(crst.EM_PM25)
  dm.loc[idx,'CCRS']=np.array(crst.EM_PM)-np.array(crst.EM_PM25)
  # combustion sources allocated into ?PRM, not PEC or POA
  burn=dm.loc[(dm.EM_NOX+dm.EM_CO+dm.EM_SOX)>0]
  prim=burn.loc[burn.EM_PM>0]
  idx=prim.index
  dm.loc[idx,'FPRM']=np.array(prim.EM_PM25)
  dm.loc[idx,'CPRM']=np.array(prim.EM_PM)-np.array(prim.EM_PM25)
  # check for left_over sources(NMHC fugitives), in fact no PM emits at all
  boo=(dm.EM_PM!=0) & ((dm.CCRS+dm.FCRS+dm.CPRM+dm.FPRM)==0)
  idx=dm.loc[boo].index
  if len(idx)!=0:
    res=dm.loc[idx]
    dm.loc[idx,'FPRM']=np.array(res.EM_PM25)/2
    dm.loc[idx,'FCRS']=np.array(res.EM_PM25)/2
    dm.loc[idx,'CPRM']=(np.array(res.EM_PM)-np.array(res.EM_PM25))/2.
    dm.loc[idx,'CCRS']=(np.array(res.EM_PM)-np.array(res.EM_PM25))/2.
  return dm

def add_VOC(dm,n):
  df_asgn,df_prof,df_cbm=rd_ASnPRnCBM_A()
  df_asgn.NSC=[i.strip() for i in df_asgn.NSC]
  MW={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['MW']))}
  BASE={i:j for i,j in zip(list(df_cbm['SPE_NO']),list(df_cbm['BASE']))}
  colv='OLE PAR TOL XYL FORM ALD2 ETH ISOP NR ETHA MEOH ETOH IOLE TERP ALDX PRPA BENZ ETHY ACET KET'.split()
  NC=len(colv)
  try:
    prof_cbm=read_csv('prof_cbm.csv')
    prof_cbm.PRO_NO=['{:04d}'.format(m) for m in prof_cbm.PRO_NO]
  except:
    HC=1
    prof_cbm=DataFrame({})
    prof_cbm['PRO_NO']=list(set(df_prof.PRO_NO))
    for c in colv:
      prof_cbm[c]=0.
    for i in range(len(prof_cbm)):
      prof=prof_cbm.PRO_NO[i]
      spec=df_prof.loc[df_prof.PRO_NO==prof].reset_index(drop=True)
      for K in range(len(spec)):
        W_K_II,IS=spec.WT[K],spec.SPE_NO[K]
        if W_K_II==0.0 or sum(BASE[IS])==0.0:continue
        VOCwt=HC*W_K_II/100. #in T/Y
        VOCmole=VOCwt/MW[IS] #in Tmole/Y
        for LS in range(NC): #CBM molar ratio
          if BASE[IS][LS]==0.:continue
          prof_cbm.loc[i,colv[LS]]+=VOCmole*BASE[IS][LS]
    prof_cbm.set_index('PRO_NO').to_csv('prof_cbm.csv')

  #matching the category profile number
  if n not in set(df_asgn.NSC):sys.exit('nsc not assigned: '+n)
  prof=df_asgn.loc[df_asgn.NSC==n,'PRO_NO'].values[0]
  if prof not in set(prof_cbm.PRO_NO):sys.exit('prof not found: '+prof)
  prod=prof_cbm.loc[prof_cbm.PRO_NO==prof].iloc[0,1:]
  HC=dm.loc[dm.nsc2==n,'EM_NMHC']
  idx=HC.index
  for LS in range(NC): #CBM molar ratio
    dm.loc[idx,colv[LS]]=HC*prod[LS]
  return dm

