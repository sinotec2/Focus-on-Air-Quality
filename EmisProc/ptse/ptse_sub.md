---
layout: default
title: "Prepare for PointS"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 1
date: 2021-12-03 09:54:07               
last_modified_date:   2021-12-08 13:33:38
---

# 點源排放檔案準備相關副程式
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景
- 主要是確認(解決)環保署點源資料庫的數據品質(問題)，避免後續造成錯誤。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，為此處之前處理。  

## 確認資料庫的正確性

### 修正不合理的煙道參數`CORRECT`
```python
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n ptse_sub.py
     1  import numpy as np
     2  from pandas import *
     3
     4
     5  def CORRECT(df):
     6    dia,he,tmp,q,vs=df.DIA,df.HEI,df.TEMP,df.ORI_QU1,df.VEL
     7    from bisect import bisect
```
- 修正超小煙道直徑

```python
     8    idx=np.where(dia<=0.1)
     9    if len(idx[0])>0:dia[idx[0]]=he[idx[0]]*0.05
```
- 按照煙囪高度等級先計算得到區間範圍內之代表性溫度、流速上下區間，藉以校正流速。

```python
    10    h_intv=[0,12.5,50,100,150,200,249]
    11    t_intv=[171,171, 176, 202, 136, 130,  90, 85]
    12    idx=np.where(tmp<=100)
    13    he_i=[bisect(h_intv,i) for i in he[idx[0]]]
    14    tmp[idx[0]]=[t_intv[i] for i in he_i]
    15    vs=q*4.*(tmp+273)/273./3.14159/dia/dia/60.
    16    v_intL=[3.0,4.5,5.3,7.1 ,14.1,15.4,18.0,19.0]
    17    v_intU=[7.0,8.5,9.3,11.1,18.1,19.4,22.0,26.0]
    18    v_intm=[6.5,6.5,7.3,9.1 ,16.1,17.4,20.0,23.0]
    19    he_i=np.array([bisect(h_intv,i) for i in he])
    20    for i in set(he_i):
    21      idx=np.where(he_i==i)
    22      if len(idx[0])==0:continue
    23      vidx0=np.array(vs[idx[0]])
    24      idx2=np.where((vidx0-v_intU[i])*(vidx0-v_intL[i])>0)
    25      if len(idx2[0])==0:continue
    26      vidx0[idx2[0]]=v_intm[i]
    27      vs[idx[0]]=vidx0
    28    df.DIA,df.HEI,df.TEMP,df.ORI_QU1,df.VEL=dia,he,tmp,q,vs
    29    return df
    30
```
### 簡單的PM劃分副程式

```python
    31  #A simple scheme is in place for PM splitting, and the SPECCIATE is not adopted.
    32  def add_PMS(dm):
    33    #add the PM columns and reset to zero
    34    colc=['CCRS','FCRS','CPRM','FPRM']
    35    for c in colc:
    36      dm[c]=np.zeros(len(dm))
    37    #in case of non_PM sources, skip the routines
    38    if 'PM_EMI' not in dm.columns or sum(dm.PM_EMI)==0:return dm
```
- 非燃燒PM排放源，特性是不會有SNC之排放，定義為`crst`
  - 按資料庫內容區分粗、細粒

```python
    39    # fugitive sources
    40    not_burn=dm.loc[dm.NOX_EMI+dm.CO_EMI+dm.SOX_EMI==0]
    41    crst=not_burn.loc[not_burn.PM_EMI>0]
    42    idx=crst.index
    43    dm.loc[idx,'FCRS']=np.array(crst.PM25_EMI)
    44    dm.loc[idx,'CCRS']=np.array(crst.PM_EMI)-np.array(crst.PM25_EMI)
```
- 有任何SNC排放，則為``prim`

```python
    45    # combustion sources allocated into ?PRM, not PEC or POA
    46    burn=dm.loc[(dm.NOX_EMI+dm.CO_EMI+dm.SOX_EMI)>0]
    47    prim=burn.loc[burn.PM_EMI>0]
    48    idx=prim.index
    49    dm.loc[idx,'FPRM']=np.array(prim.PM25_EMI)
    50    dm.loc[idx,'CPRM']=np.array(prim.PM_EMI)-np.array(prim.PM25_EMI)
```
- 確認是否有遺漏

```python
    51    # check for left_over sources(NMHC fugitives), in fact no PM emits at all
    52    boo=(dm.PM_EMI!=0) & ((dm.CCRS+dm.FCRS+dm.CPRM+dm.FPRM)==0)
    53    idx=dm.loc[boo].index
    54    if len(idx)!=0:
    55      res=dm.loc[idx]
    56      dm.loc[idx,'FPRM']=np.array(res.PM25_EMI)/2
    57      dm.loc[idx,'FCRS']=np.array(res.PM25_EMI)/2
    58      dm.loc[idx,'CPRM']=(np.array(res.PM_EMI)-np.array(res.PM25_EMI))/2.
    59      dm.loc[idx,'CCRS']=(np.array(res.PM_EMI)-np.array(res.PM25_EMI))/2.
    60    return dm
    61
```
### 確認資料庫缺值`check_nan`

```python
    62  def check_nan(df):
    63    import numpy as np
    64    cols = list(df.columns)[1:]
    65    col_em = list(filter((lambda x: 'EMI' in x), cols))
    66    tp = [np.float64, np.int64]
    67    for i in cols:
    68      a = list(df[i])
    69      if type(a[0]) in tp:
    70        boo = (np.isnan(list(a)))
    71        lnan = len(df.loc[boo])
    72        if lnan > 1: print(i, lnan)
    73    # these plants with a little emission amounts, how small?
    74    a = set(df[np.isnan(df['UTM_E'])]['C_NO'])
    75    print(a)
    76    for sp in col_em:
    77      boo = (df['C_NO'].map(lambda x: x in a))
    78      print(sp, sum(df.loc[boo][sp]))
    79
    80    # UTM is not number, maybe blank
    81    boo = (~(np.isnan(df['UTM_E'])) | ~(np.isnan(df['UTM_N'])))
    82    df = df.loc[boo]
    83    df = FillNan(df,'SCC', 0.)
    84    df['SCC']=[int(i) for i in df.SCC]
    85    df = FillNan(df, 'NO_P', 'E000')
    86    df = FillNan(df, 'NO_S', 'Y000')
    87    for c in ['EQ_1','EQ_2','A_NAME1']:
    88      df = FillNan(df, c, 'None')
    89    return df
    90
```
### 確認工廠座標都落在陸地上

```python
    91  def check_landsea(df):
    92    from load_surfer import load_surfer
    93    xc, yc, ndct, (nxc, nyc) = load_surfer('dict.grd')
    94    land = set()
    95    for i in range(nxc - 1):
    96      for j in range(nyc - 1):
    97        if ndct[i][j] > 0:
    98          land.add((xc[i][j], yc[i][j]))
    99    df['XY'] = [(int(x) % 1000 * 1000, int(y) % 1000 * 1000) for x, y in zip(list(df.UTM_E), list(df.UTM_E))]
   100    df_sea = df.loc[(df['XY'].map(lambda x: x not in land))]
   101    sea_shore = ['P', 'D', 'S', 'N', 'T', 'V', 'F']
   102    boo = (df_sea['C_NO'].map(lambda x: x[0] not in sea_shore))
   103    df_sea = df_sea.loc[boo]
   104    a = {'X': Series(df_sea['UTM_E'])}
   105    a.update({'Y': Series(df_sea['UTM_N'])})
   106    a.update({'C_NO': Series(df_sea['C_NO'])})
   107    fname = 'outsideland3.dat'
   108    cola = ['X', 'Y', 'C_NO']
   109    #   DataFrame(a)[np.array(cola)].set_index('X').to_csv(fname)
   110
   111    # modify the x coord of plants located in isolated islands
   112    ldf = len(df)
   113    df['subX'] = [0 for i in df.index]
   114    WXZ = ['W', 'X', 'Z']  # W for Kinmen, X for Penhu, Z for Mazu
   115    df.loc[df['C_NO'].map(lambda x: x[0] in WXZ), 'subX'] = 201500
   116    df['UTM_E'] = Series([i - j for i, j in zip(df['UTM_E'], df['subX'])], index=df.index)
   117    del df['XY'], df['subX']
   118    return df
   119
```
### 資料庫缺值之補遺`FillNan`

```python
   120  def FillNan(df,c, s):
   121    idx = df.loc[df[c].map(lambda x: x != x)].index
   122    df.loc[idx, c] = [s for i in idx]
   123    return df
   124
```
## 重新計算座標、處理地面PM過大問題

### 重新計算點源座標`WGS_TWD`

```python
   125  def WGS_TWD(df):
   126    import twd97
   127    from pandas import read_csv
   128    from pyproj import Proj
   129    ll=read_csv('TEDS_POINT_WGS84.LL')
   130    Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
   131    Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
   132    pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
   133          lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
   134    x,y=pnyc(np.array(ll['lon']),np.array(ll.lat), inverse=False)
   135    df.UTM_E=x+Xcent
   136    df.UTM_N=y+Ycent
   137    return df
   138
```
### 給予地面大量PM點源合理的排放條件`Elev_YPM`

```python
   139  def Elev_YPM(df):
   140    from pandas import DataFrame, pivot_table
   141    import netCDF4
   142    import twd97
   143    if 'IX' not in df.columns:
   144      Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
   145      Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
   146      fn='template_d4.nc'
   147      nc0 = netCDF4.Dataset(fn, 'r')
   148      df['IX']=np.array((df.UTM_E-Xcent-nc0.XORIG)/nc0.XCELL,dtype=int)
   149      df['IY']=np.array((df.UTM_N-Ycent-nc0.YORIG)/nc0.YCELL,dtype=int)
   150      nc0.close()
   151    boo=(df.NO_S.map(lambda x:type(x)==str and x[0] !='P')) & (df.PM25_EMI>0)
```

- 計算網格地面排放

```python
   152  # elevate the first 100 max ground-level PM sources
   153  # the hourly emission is considered, not the annual emission
   154    dfG=df.loc[boo].reset_index(drop=True)
   155    dfG['PM25_EM']=[i/j/k/l for i,j,k,l in zip(dfG.PM25_EMI,dfG.HD1,dfG.DW1,dfG.WY1)]
   156    pvG=pivot_table(dfG,index=['IX','IY'],values='PM25_EM',aggfunc='sum').reset_index()
   157    a=pvG.sort_values('PM25_EM',ascending=False).reset_index(drop=True)
   158    a['IYX']=[(j,i) for i,j in zip(a.IX,a.IY)]
   159    if 'IYX' not in df.columns:
   160      df['IYX']=[(j,i) for i,j in zip(df.IX,df.IY)]
```
- 假設排放條件

```python
   161  #assumed parameters
   162  #the HEI may merge to the largest one in that plant
   163    as_p={'NO_S':'PY00','TEMP':100.,'HEI':40.,'VEL':10.,'DIA':30.}
   164    q=as_p['VEL']*(as_p['TEMP']+273)/273*as_p['DIA']**2*3.14/4/60.
   165    as_p.update({'ORI_QU1':q})
```
- 排放量排名前100大者，給予一排放高度與其他條件

```python
   166    for iyx in a.loc[:100,'IYX']:
   167      boo2=(df.IYX==iyx)& (boo)
   168      nb2=len(df.loc[boo2])
   169      for v in as_p:
   170        df.loc[boo2,v]=[as_p[v] for i in range(nb2)]
   171    return df
   172
```

## 地面點源處理會用到的副程式

### 網格整併與轉寫到nc檔案
- 此副程式會把逐時、逐煙道的排放量矩陣展開成資料庫形態，以便進行`pivot_table`，整併(加總)網格排放量。

```python
   173  def pv_nc(dfi,nc,spec):
   174    NREC=len(dfi)
   175    ntm,nrow,ncol=(nc.dimensions[c].size for c in ['TSTEP','ROW', 'COL'])
   176    V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
   177    sdt,ix,iy=(np.zeros(shape=(ntm*NREC),dtype=int) for i in range(3))
   178    for t in range(ntm):
   179      t1,t2=t*NREC,(t+1)*NREC
   180      ix[t1:t2]=list(dfi.IX)
   181      iy[t1:t2]=list(dfi.IY)
   182    for t in range(ntm):
   183      sdt[t*NREC:(t+1)*NREC]=t
   184    col=[i for i in dfi.columns if i not in ['YJH','IX','IY']]
   185    dfT=DataFrame({'YJH':sdt,'IX':ix,'IY':iy})
   186    if len(spec.shape)==2:
   187      for c in col:
   188        ic=col.index(c)
   189        dfT[c]=spec[:,ic]
   190    else:
   191      for c in col:
   192        dfT[c]=spec[:]
   193    pv=pivot_table(dfT,index=['YJH','IX','IY'],values=col,aggfunc=sum).reset_index()
   194    pv.IX=[int(i) for i in pv.IX]
   195    pv.IY=[int(i) for i in pv.IY]
   196    pv.YJH=[int(i) for i in pv.YJH]
   197    imn,jmn=min(pv.IX),min(pv.IY)
   198    imx,jmx=max(max(pv.IX)+abs(imn)*2+1,ncol), max(max(pv.IY)+abs(jmn)*2+1,nrow)
   199    if imn<0 and imx+imn<ncol:sys.exit('negative indexing error in i')
   200    if jmn<0 and jmx+jmn<nrow:sys.exit('negative indexing error in j')
   201    idx=pv.index
   202    idt=np.array(pv.loc[idx,'YJH'])
   203    iy=np.array(pv.loc[idx,'IY'])
   204    ix=np.array(pv.loc[idx,'IX'])
   205    for c in col:
   206      if c not in V[3]:continue
   207      if sum(pv[c])==0:continue
   208      z=np.zeros(shape=(ntm,jmx,imx))
   209      ss=np.array(pv.loc[idx,c])
   210      #Note that negative indices are not bothersome and are only at the end of the axis.
   211      z[idt,iy,ix]=ss
   212  #also mapping whole matrix, NOT by parts
   213      nc.variables[c][:,0,:,:]=z[:,:nrow,:ncol]
   214    return
   215
```

### 格點化
- 將資料庫中的`UTM_E`及`UTM_N`按照網格系統的原點與解析度予以格點化。
  - 為適應座標系統有可能先行平移，測驗座標值是否有負值，若是，則不必再平移

```python
   216  def disc(dm):
   217  #discretizations
   218    if min(dm.UTM_N)<0:
   219      dm['IX']=np.array((dm.UTM_E-nc.XORIG)/nc.XCELL,dtype=int)
   220      dm['IY']=np.array((dm.UTM_N-nc.YORIG)/nc.YCELL,dtype=int)
   221    else:
   222      dm['IX']=np.array((dm.UTM_E-Xcent-nc.XORIG)/nc.XCELL,dtype=int)
   223      dm['IY']=np.array((dm.UTM_N-Ycent-nc.YORIG)/nc.YCELL,dtype=int)
   224    return dm
   225
   226
```

## 資料表與矩陣的互換

### 資料表轉成矩陣
- 目前既有的轉檔工具都假設資料表本身就是2階矩陣的內容，不適用在資料表含有字串的欄位，以其他欄位作為維度、多維度、不限維度的情況
- 維度欄位令為`idx_lst`的序列，可以是任何物件、種類。
- 資料表（名稱令為`dd`）的值在最後一欄，其欄位名稱令為`vname`，即為矩陣的值。
- 目標矩陣(`mat`)維度階級數未知、形狀未知。

```python
# input df, index cols(list), value cols name(str)
# return matrix, index lists (in cols order)
def DF2Mat(dd,idx_lst,vname):
  import sys
  import numpy as np
  from pandas import DataFrame
```
- 取出每個維度欄位的值(`lst`)，予以排序，將值反算成序位標籤(`'i'+c`)，存回資料表。
  - 序列`lst`要取長度，並且準備回傳。
  - 使用`dict`對照，而不要使用`list.index()`，後者耗費的時間會很長。

```python
  ret_lst, num_lst=[],[]
  for c in idx_lst:
    lst=eval('list(set(dd.'+c+'))');lst.sort()
    n=len(lst)
    ret_lst.append(lst);num_lst.append(n)
    dct={lst[i]:i for i in range(n)}
    dd['i'+c]=[dct[i] for i in dd[c]]
```
- 開啟新的矩陣，其形狀即為每個`lst`的長度。
  - 每個欄位的序位標籤，將用在指示`mat`的空間位置，將`vname`的值存放在正確的位置。
  - 此處使用`exec`指令，以因應不同的階級數的情況
  - 在副程式內執行`exec`，需加上`locals()`,避免動到主程式的變數名稱。

```python
  mat=np.zeros(shape=num_lst)
  s='mat['+''.join(['dd.i'+c+'[:],' for c in idx_lst]).strip(',')+']=dd.'+vname+'[:]' 
  exec(s,locals())
  return mat, ret_lst
```

### 矩陣轉資料表
- 目的是使用資料表的`pivot_table`平行計算功能
   - 回傳資料表並未去 `0`，如果需要減少資料表的長度，使用者要自己執行篩選、刪除。
   - 同樣不限矩陣階級數的上限，只有下限。

```python
# input any ranks of matrix a
# return df which columns is [col_1,col_2 ... col_ndim, val]
def Mat2DF(a):
  import sys
  import numpy as np
  from pandas import DataFrame
  ndim=a.ndim
  if ndim<2:sys.exit('ndim too small, no need to convert')
```
- `ranks`是個字串序列，如果是3階，將會是`["[:,None,None]", "[None,:,None]", "[None,None,:]"]`套用在每個維度的標籤，1維轉多維的複製過程。

```python
  H,T,C,N='[', ']', ':,', 'None,'
  ranks=[]
  for n in range(ndim):
    s=H
    for i in range(ndim):
      m=N
      if i==n:m=C
      s+=m    
    ranks.append(s.strip(',')+T)
```
- 寫出每個維度的標籤當成新的維度欄位。實際的值需要前述`ret_lst`內容來套入。

```python
  DD={}
  for i in range(ndim):
    var=np.zeros(shape=a.shape,dtype=int)
    var[:]=eval('np.array([j for j in range(a.shape[i])],dtype=int)'+ranks[i],locals())
	DD['col_'+str(i+1)]=var[:].flatten()
  DD['val']=a.flatten()
  return DataFrame(DD)

```

## 檔案下載
- `python`程式：[ptse_sub.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptse_sub.py)。

## Reference
