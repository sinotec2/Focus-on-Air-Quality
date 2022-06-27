import numpy as np
from pandas import *


def CORRECT(df):
  dia,he,tmp,q,vs=df.DIA,df.HEI,df.TEMP,df.ORI_QU1,df.VEL
  from bisect import bisect
  idx=np.where(dia<=0.1)
  if len(idx[0])>0:dia[idx[0]]=he[idx[0]]*0.05
  h_intv=[0,12.5,50,100,150,200,249]
  t_intv=[171,171, 176, 202, 136, 130,  90, 85]
  idx=np.where(tmp<=100) 
  he_i=[bisect(h_intv,i) for i in he[idx[0]]]
  tmp[idx[0]]=[t_intv[i] for i in he_i]
  vs=q*4.*(tmp+273)/273./3.14159/dia/dia/60.
  v_intL=[3.0,4.5,5.3,7.1 ,14.1,15.4,18.0,19.0] 
  v_intU=[7.0,8.5,9.3,11.1,18.1,19.4,22.0,26.0] 
  v_intm=[6.5,6.5,7.3,9.1 ,16.1,17.4,20.0,23.0] 
  he_i=np.array([bisect(h_intv,i) for i in he])
  for i in set(he_i):
    idx=np.where(he_i==i)
    if len(idx[0])==0:continue
    vidx0=np.array(vs[idx[0]])
    idx2=np.where((vidx0-v_intU[i])*(vidx0-v_intL[i])>0)
    if len(idx2[0])==0:continue
    vidx0[idx2[0]]=v_intm[i] 
    vs[idx[0]]=vidx0
  df.DIA,df.HEI,df.TEMP,df.ORI_QU1,df.VEL=dia,he,tmp,q,vs
  return df

#A simple scheme is in place for PM splitting, and the SPECCIATE is not adopted.
def add_PMS(dm):
  #add the PM columns and reset to zero
  colc=['CCRS','FCRS','CPRM','FPRM']
  for c in colc:
    dm[c]=np.zeros(len(dm))
  #in case of non_PM sources, skip the routines
  if 'PM_EMI' not in dm.columns or sum(dm.PM_EMI)==0:return dm  
  # fugitive sources
  not_burn=dm.loc[dm.NOX_EMI+dm.CO_EMI+dm.SOX_EMI==0]
  crst=not_burn.loc[not_burn.PM_EMI>0]
  idx=crst.index
  dm.loc[idx,'FCRS']=np.array(crst.PM25_EMI)
  dm.loc[idx,'CCRS']=np.array(crst.PM_EMI)-np.array(crst.PM25_EMI)
  # combustion sources allocated into ?PRM, not PEC or POA 
  burn=dm.loc[(dm.NOX_EMI+dm.CO_EMI+dm.SOX_EMI)>0]
  prim=burn.loc[burn.PM_EMI>0]
  idx=prim.index
  dm.loc[idx,'FPRM']=np.array(prim.PM25_EMI)
  dm.loc[idx,'CPRM']=np.array(prim.PM_EMI)-np.array(prim.PM25_EMI)
  # check for left_over sources(NMHC fugitives), in fact no PM emits at all 
  boo=(dm.PM_EMI!=0) & ((dm.CCRS+dm.FCRS+dm.CPRM+dm.FPRM)==0)
  idx=dm.loc[boo].index
  if len(idx)!=0:
    res=dm.loc[idx]
    dm.loc[idx,'FPRM']=np.array(res.PM25_EMI)/2
    dm.loc[idx,'FCRS']=np.array(res.PM25_EMI)/2
    dm.loc[idx,'CPRM']=(np.array(res.PM_EMI)-np.array(res.PM25_EMI))/2.
    dm.loc[idx,'CCRS']=(np.array(res.PM_EMI)-np.array(res.PM25_EMI))/2.
  return dm

def check_nan(df):
  import numpy as np
  cols = list(df.columns)[1:]
  col_em = list(filter((lambda x: 'EMI' in x), cols))
  tp = [np.float64, np.int64]
  for i in cols:
    a = list(df[i])
    if type(a[0]) in tp:
      boo = (np.isnan(list(a)))
      lnan = len(df.loc[boo])
      if lnan > 1: print(i, lnan)
  # these plants with a little emission amounts, how small?
  a = set(df[np.isnan(df['UTM_E'])]['C_NO'])
  print(a)
  for sp in col_em:
    boo = (df['C_NO'].map(lambda x: x in a))
    print(sp, sum(df.loc[boo][sp]))

  # UTM is not number, maybe blank
  boo = (~(np.isnan(df['UTM_E'])) | ~(np.isnan(df['UTM_N'])))
  df = df.loc[boo]
  df = FillNan(df,'SCC', 0.)
  df['SCC']=[int(i) for i in df.SCC]
  df = FillNan(df, 'NO_P', 'E000')
  df = FillNan(df, 'NO_S', 'Y000')
  for c in ['EQ_1','EQ_2','A_NAME1']:
    df = FillNan(df, c, 'None')
  return df

def check_landsea(df):
  from load_surfer import load_surfer
  xc, yc, ndct, (nxc, nyc) = load_surfer('dict.grd')
  land = set()
  for i in range(nxc - 1):
    for j in range(nyc - 1):
      if ndct[i][j] > 0:
        land.add((xc[i][j], yc[i][j]))
  df['XY'] = [(int(x) % 1000 * 1000, int(y) % 1000 * 1000) for x, y in zip(list(df.UTM_E), list(df.UTM_E))]
  df_sea = df.loc[(df['XY'].map(lambda x: x not in land))]
  sea_shore = ['P', 'D', 'S', 'N', 'T', 'V', 'F']
  boo = (df_sea['C_NO'].map(lambda x: x[0] not in sea_shore))
  df_sea = df_sea.loc[boo]
  a = {'X': Series(df_sea['UTM_E'])}
  a.update({'Y': Series(df_sea['UTM_N'])})
  a.update({'C_NO': Series(df_sea['C_NO'])})
  fname = 'outsideland3.dat'
  cola = ['X', 'Y', 'C_NO']
  #   DataFrame(a)[np.array(cola)].set_index('X').to_csv(fname)

  # modify the x coord of plants located in isolated islands
  ldf = len(df)
  df['subX'] = [0 for i in df.index]
  WXZ = ['W', 'X', 'Z']  # W for Kinmen, X for Penhu, Z for Mazu
  df.loc[df['C_NO'].map(lambda x: x[0] in WXZ), 'subX'] = 201500
  df['UTM_E'] = Series([i - j for i, j in zip(df['UTM_E'], df['subX'])], index=df.index)
  del df['XY'], df['subX']
  return df

def FillNan(df,c, s):
  idx = df.loc[df[c].map(lambda x: x != x)].index
  df.loc[idx, c] = [s for i in idx]
  return df

def WGS_TWD(df):
  import twd97
  from pandas import read_csv
  from pyproj import Proj
  ll=read_csv('TEDS_POINT_WGS84.LL')
  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
	lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
  x,y=pnyc(np.array(ll['lon']),np.array(ll.lat), inverse=False)
  df.UTM_E=x+Xcent
  df.UTM_N=y+Ycent   
  return df

def Elev_YPM(df):
  from pandas import DataFrame, pivot_table
  import netCDF4
  import twd97
  if 'IX' not in df.columns:
    Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
    Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    fn='template_d4.nc'
    nc0 = netCDF4.Dataset(fn, 'r')
    df['IX']=np.array((df.UTM_E-Xcent-nc0.XORIG)/nc0.XCELL,dtype=int)
    df['IY']=np.array((df.UTM_N-Ycent-nc0.YORIG)/nc0.YCELL,dtype=int)
    nc0.close()
  boo=(df.NO_S.map(lambda x:type(x)==str and x[0] !='P')) & (df.PM25_EMI>0)
# elevate the first 100 max ground-level PM sources
# the hourly emission is considered, not the annual emission
  dfG=df.loc[boo].reset_index(drop=True)
  dfG['PM25_EM']=[i/j/k/l for i,j,k,l in zip(dfG.PM25_EMI,dfG.HD1,dfG.DW1,dfG.WY1)]
  pvG=pivot_table(dfG,index=['IX','IY'],values='PM25_EM',aggfunc='sum').reset_index()
  a=pvG.sort_values('PM25_EM',ascending=False).reset_index(drop=True)
  a['IYX']=[(j,i) for i,j in zip(a.IX,a.IY)]
  if 'IYX' not in df.columns:
    df['IYX']=[(j,i) for i,j in zip(df.IX,df.IY)]
#assumed parameters
#the HEI may merge to the largest one in that plant
  as_p={'NO_S':'PY00','TEMP':100.,'HEI':40.,'VEL':10.,'DIA':30.}
  q=as_p['VEL']*(as_p['TEMP']+273)/273*as_p['DIA']**2*3.14/4/60.
  as_p.update({'ORI_QU1':q})
  for iyx in a.loc[:100,'IYX']:
    boo2=(df.IYX==iyx)& (boo)
    nb2=len(df.loc[boo2])
    for v in as_p:
      df.loc[boo2,v]=[as_p[v] for i in range(nb2)]
  return df 

def pv_nc(dfi,nc,spec):
  NREC=len(dfi)
  col=[i for i in dfi.columns if i not in ['IX','IY']]
  if len(col)!=spec.shape[-1]:sys.exit('last dimension must be ic')
  ntm,nrow,ncol=(nc.dimensions[c].size for c in ['TSTEP','ROW', 'COL'])
  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
  z=np.zeros(shape=spec.shape[:-1],dtype=int)
  z[:,:]=np.array([i for i in range(NREC)])[:,None]
  z=z.flatten()
  #Using dict, not DataFrame filtering, not list_indexing relatives methods
  dIX, dIY={i:dfi.IX[i] for i in range(NREC)}, {i:dfi.IY[i] for i in range(NREC)}
  ix,iy=[dIX[i] for i in z],[dIY[i] for i in z] 
  for ic in range(len(col)):
    c=col[ic]
    if c not in V[3]:continue
    if np.sum(spec[:,:,ic])==0.: continue
    dfT=Mat2DF(spec[:,:,ic])
    dfT['IX'],dfT['IY']=ix,iy
    dfT=dfT.loc[dfT.val>0].reset_index(drop=True) 
    boo=(dfT.IX>=0) & (dfT.IY>=0) & (dfT.IX<ncol) & (dfT.IY<nrow)
    dfT=dfT.loc[boo].reset_index(drop=True) 
    pv=pivot_table(dfT,index=['col_2','IY','IX'],values='val',aggfunc=sum).reset_index()
    var,lst=DF2Mat(pv,['col_2','IY','IX'],'val')
    i0,i1,i2=(np.zeros(shape=var.shape,dtype=int) for i in range(3)) 
    i0[:]=lst[0][:,None,None]
    i1[:]=lst[1][None,:,None]
    i2[:]=lst[2][None,None,:]
    #Note that negative indices are not bothersome and are only at the end of the axis.
    z=np.zeros(shape=(ntm,nrow,ncol))
    z[i0.flatten(),i1.flatten(),i2.flatten()]=var.flatten()
#also mapping whole matrix, NOT by parts
    nc.variables[c][:,0,:,:]=z[:,:,:]
    print(c)
  return

def disc(dm,nc):
#discretizations
  if min(dm.UTM_N)<0:
    dm['IX']=np.array((dm.UTM_E-nc.XORIG)/nc.XCELL,dtype=int)
    dm['IY']=np.array((dm.UTM_N-nc.YORIG)/nc.YCELL,dtype=int)
  else:
    dm['IX']=np.array((dm.UTM_E-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
    dm['IY']=np.array((dm.UTM_N-Ycent-nc.YORIG)/nc.YCELL,dtype=int)
  return dm


# input df, index cols(list), value cols name(str)
# return matrix, index lists (in cols order)
def DF2Mat(dd,idx_lst,vname):
  import sys
  import numpy as np
  from pandas import DataFrame
  ret_lst, num_lst=[],[]
  for c in idx_lst:
#mac    lst=eval('list(set(dd.'+c+'))');lst.sort()
    lst=list(set(dd[c]));lst.sort()
    n=len(lst)
    ret_lst.append(np.array(lst));num_lst.append(n)
    dct={lst[i]:i for i in range(n)}
    dd['i'+c]=[dct[i] for i in dd[c]]
  mat=np.zeros(shape=num_lst)
  s='mat['+''.join(['dd.i'+c+'[:],' for c in idx_lst]).strip(',')+']=dd.'+vname+'[:]' 
  exec(s,locals())
  return mat, ret_lst


# input any ranks of matrix a
# return df which columns is [col_1,col_2 ... col_ndim, val]
def Mat2DF(a):
  import sys
  import numpy as np
  from pandas import DataFrame
  ndim=a.ndim
  if ndim<2:sys.exit('ndim too small, no need to convert')
  H,T,C,N='[', ']', ':,', 'None,'
  ranks=[]
  for n in range(ndim):
    s=H
    for i in range(ndim):
      m=N
      if i==n:m=C
      s+=m    
    ranks.append(s.strip(',')+T)
  DD={}
  for i in range(ndim):
    var=np.zeros(shape=a.shape,dtype=int)
#mac    var[:]=eval('np.array([j for j in range(a.shape[i])],dtype=int)'+ranks[i],locals())
    exec('var[:]=np.array([j for j in range(a.shape[i])],dtype=int)'+ranks[i],locals())
    DD['col_'+str(i+1)]=var[:].flatten()
  DD['val']=a.flatten()
  return DataFrame(DD)



