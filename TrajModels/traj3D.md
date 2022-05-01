---
layout: default
title: 三維軌跡分析
nav_order: 6
parent: Trajectory Models
last_modified_date: 2022-03-31 15:20:02
---

# WRF三維軌跡分析
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

## WRFOUT三維軌跡主程式
### wrfout檔案之彙整、連結
- 由於所需歷年來之wrfout，可能分散在不同目錄、磁碟機檔案系統、需要先做好連結。['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]：各層wrfout檔案(連結)
- 時間規格：每天一個檔，檔案為逐時，自UTC 0時開始，結束於隔天0時。
- wrf版本：不限、不檢查

### bt2_DVP.py
- 3維軌跡程式參考2維程式進行增修，2維(CWB觀測值內插)軌跡程式公開於github(https://github.com/sinotec2/rd_cwbDay/blob/master/traj2kml.py)
- arguments:     -t daliao -d 20171231 -b T (測站名稱、軌跡起始的年月日時、是否為反軌跡(T/F))
- 輸入檔：sta_list.json：測站編號名稱path+'sta_ll.csv：測站經緯度['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]：各層wrfout檔案(連結)
- 輸出檔：'trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
- 軌跡點時間間距：15S
- 程式內掛後處理(不執行不影響主要結果)csv2kml.py：繪製google mapcsv2bln.cs：bln file is used for surfer plotting


```python
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat -n bt2_DVP.py
     1  #!/cluster/miniconda/envs/py37/bin/python
     2  import numpy as np
     3  from pandas import *
     4  import os, sys, subprocess, time, json
     5  from scipy.io import FortranFile
     6  from datetime import datetime, timedelta
     7  import twd97
     8  import netCDF4
     9  from pyproj import Proj
    10  import subprocess
    11  from pandas import *
    12  from scipy import interpolate
    13  from scipy.interpolate import griddata
    14  import bisect
    15
    16  #get the UVW data from NC files
    17  #z not interpolated yet
    18  def get_uvw(ncft,t0,z,y,x):
    19    (ncf,t1)=ncft[:]
    20    t=abs(t1-t0)
    21    n0=locate_nest(x,y)
    22    #make sure the point is in d1(at least)
    23    if n0==-1:
    24      return -1
    25    iii=int(x//dx[4]+ncol[4]//2)
    26    jjj=int(y//dx[4]+nrow[4]//2)
    27    kkk=int(z//dz)
    28    idx=(t,kkk,jjj,iii)
    29    if idx in f: return idx,f
    30
    31    #loop for every possible nest
    32    for n in range(n0,n0-1,-1):
    33      ix=int(x//dx[n]+ncol[n]//2)
    34      iy=int(y//dx[n]+nrow[n]//2)
    35  #   print(ix,iy)
    36      iz=bisect.bisect_left(zh[n][t1,:,iy,ix],z)
    37
    38      #the data are stored in the vast, sparce matrix
    39      for k in range(max(0,iz-1),min(iz+3,nlay[n])):
    40        kk=int(z//dz)
    41        for j in range(max(0,iy-1),min(iy+3,nrow[n])):
    42          jj=int((j-nrow[n]//2)*fac[n] +nrow[4]//2)
    43          for i in range(max(0,ix-1),min(ix+3,ncol[n])):
    44            ii=int((i-ncol[n]//2)*fac[n] +ncol[4]//2)
    45            if (t,kk,jj,ii) in withdata:continue
    46            #average the stagger wind to the grid_points
    47            uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U'][t1,k,j,i]+ncf[n].variables['U'][t1,k,j,i+1])/2.
    48            uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V'][t1,k,j,i]+ncf[n].variables['V'][t1,k,j+1,i])/2.
    49            uvwg[2,t,kk,jj,ii]=(ncf[n].variables['W'][t1,k,j,i]+ncf[n].variables['W'][t1,k+1,j,i])/2.
    50            #np.where(abs(uvwg)>0) is too slow, remember the locations directly
    51            withdata.append((t,kk,jj,ii))
    52    wd2=[i[2] for i in withdata]
    53    wd3=[i[3] for i in withdata]
    54    xx,yy=x_g[wd2,wd3], y_g[wd2,wd3]
    55    if n0<3:
    56      xx_mesh, yy_mesh=np.arange(min(xx),max(xx)+1,3000),np.arange(min(yy),max(yy)+1,3000)
    57      iis,jjs=x_mesh.index(min(xx)),  y_mesh.index(min(yy))
    58      iie,jje=x_mesh.index(max(xx))+1,y_mesh.index(max(yy))+1
    59      xxg, yyg = np.meshgrid(xx_mesh, yy_mesh)
    60      for Lv in range(3):
    61        points=[(i,j) for i,j in zip(xx,yy)]
    62        grid_z2 = griddata(points, uvwg[Lv,t,kk,wd2,wd3], (xxg, yyg),  method='cubic')
    63        uvwg[Lv,t,kk,jjs:jje,iis:iie]=grid_z2
    64    fcn=[]
    65  #  for Lv in range(3):
    66  #    try:
    67  #      fcn.append(interpolate.interp2d(yy, xx, uvwg[Lv,t,kk,wd2,wd3], kind='cubic'))
    68  #    except:
    69  #      fcn.append(interpolate.interp2d(yy, xx, uvwg[Lv,t,kk,wd2,wd3], kind='linear'))
    70  #  f.update({idx:fcn})
    71    return idx,f
    72
    73  def locate_nest(x,y):
    74      for n in range(3,-1,-1):
    75          if xmin[n]<=x<xmax[n] and ymin[n]<=y<ymax[n]:
    76              return n
    77      return -1
    78
    79
    80  def getarg():
    81    """ read time period and station name from argument(std input)
    82    traj2kml.py -t daliao -d 20171231 """
    83    import argparse
    84    ap = argparse.ArgumentParser()
    85    ap.add_argument("-t", "--STNAM", required=True, type=str, help="station name,sep by ,or Lat,Lon")
    86    ap.add_argument("-d", "--DATE", required=True, type=str, help="yyyymmddhh")
    87    ap.add_argument("-b", "--BACK", required=True, type=str, help="True or False")
    88    args = vars(ap.parse_args())
    89    return [args['STNAM'], args['DATE'],args['BACK']]
    90
    91  def str2bool(v):
    92      if isinstance(v, bool):
    93         return v
    94      if v.lower() in ('yes', 'true', 't', 'y', '1'):
    95          return True
    96      elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    97          return False
    98      else:
    99          raise argparse.ArgumentTypeError('Boolean value expected.')
   100
   101  def nstnam():
   102    import json
   103    fn = open(path+'sta_list.json')
   104    d_nstnam = json.load(fn)
   105    d_namnst = {v: k for k, v in d_nstnam.items()}
   106    return (d_nstnam, d_namnst)
   107
   108
   109  def beyond(xpp, ypp, zpp):
   110    boo = not ((xpp - x_mesh[0]) * (xpp - x_mesh[-1]) < 0 and \
   111               (ypp - y_mesh[0]) * (ypp - y_mesh[-1]) < 0 and \
   112               (zpp - z_mesh[0]) * (zpp - z_mesh[-1]) < 0)
   113    return boo
   114
   115
   116  #open the NC's for some day (this present day, first time, or next/yesterday)
   117  def openNC(sdate):
   118    ymd = sdate.strftime('%Y-%m-%d')
   119    fnames=['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]
   120    ncf,nt,nlay,nrow,ncol=[],[],[],[],[]
   121    for fname in fnames:
   122      if not os.path.isfile(fname): sys.exit('no file for '+fname)
   123      nc1=netCDF4.Dataset(fname,'r')
   124      ncf.append(nc1)
   125      v4=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))
   126      t,lay,row,col=nc1.variables['T'].shape
   127      for v in 't,lay,row,col'.split(','):
   128        exec('n'+v+'.append('+v+')')
   129    return ncf, nt, nlay, nrow, ncol, ymd.replace('-','')
   130
   131  path='/nas1/backup/data/cwb/e-service/surf_trj/'
   132  # restore the matrix
   133
   134  (d_nstnam, d_namnst) = nstnam()
   135  stnam, DATE, BACK = getarg()
   136  os.system('mkdir -p trj_results'+DATE[2:6])
   137  BACK=str2bool(BACK)
   138  BF=-1
   139  if not BACK:BF=1
   140  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
   141  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
   142  bdate = datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:]))
   143  nam = [i for i in stnam.split(',')]
   144  if len(nam) > 1:
   145    try:
   146      lat = float(nam[0])
   147      lon = float(nam[1])
   148    except:
   149      sys.exit('more than two station, suggest executing iteratively')
   150    else:
   151      # in case of lat,lon
   152      if lat < 90.:
   153        xy0 = twd97.fromwgs84(lat,lon)
   154        x0, y0 =([xy0[i]] for i in [0,1])
   155        x0,y0=x0-Xcent,y0-Ycent
   156        nam[0] = str(round(lat,2))+'_'+str(round(lon,2))+'_'
   157      #   in case of twd97_x,y
   158      else:
   159        # test the coordinate unit
   160        if lat>1000.:
   161          x0, y0 = [lat],[lon]
   162          x0,y0=x0-Xcent,y0-Ycent
   163          nam[0] = str(int(lat/1000))+'+'+str(int(lon/1000))+'_'
   164        else:
   165          x0, y0 = [lat*1000],[lon*1000]
   166          x0,y0=x0-Xcent,y0-Ycent
   167          nam[0] = str(int(lat))+'_'+str(int(lon))+'_'
   168
   169  # len(nam)==1, read the location from csv files
   170  else:
   171    for stnam in nam:
   172      if stnam not in d_namnst: sys.exit("station name not right: " + stnam)
   173    nst = [int(d_namnst[i]) for i in nam]
   174    # locations of air quality stations
   175    # read from the EPA web.sprx
   176    fname = path+'sta_ll.csv'
   177    sta_list = read_csv(fname)
   178    x0, y0 = [], []
   179    for s in nst:
   180      sta1 = sta_list.loc[sta_list.ID == s].reset_index(drop=True)
   181      x0.append(list(sta1['twd_x'])[0]-Xcent)
   182      y0.append(list(sta1['twd_y'])[0]-Ycent)
   183
   184  #initialization of traj. source, output and label lists
   185  xp, yp, zp = x0, y0, [50.]
   186  pdate = bdate
   187  nc, nt, nlay, nrow, ncol, ymd0 = openNC(pdate)
   188  nc0=nc
   189  nc1=nc
   190  nlay.append(251)
   191  nrow.append(nrow[0]*27)
   192  ncol.append(ncol[0]*27)
   193  dx=[81000,27000,9000,3000,3000]
   194  dz=20
   195  fac=[dx[n]//dx[4] for n in range(5)]
   196  #_mesh and _g in lamber conifer projection system
   197  x_mesh = [(i-ncol[4]//2)*dx[4] for i in range(ncol[4])]
   198  y_mesh = [(j-nrow[4]//2)*dx[4] for j in range(nrow[4])]
   199  z_mesh = [k*dz for k in range(nlay[4])]
   200  x_g, y_g = np.meshgrid(x_mesh, y_mesh)
   201  xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(4)]
   202  xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(4)]
   203  ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(4)]
   204  ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(4)]
   205  zh=[]
   206  for n in range(4):
   207    ph_n=nc[n].variables['PH'][:,:,:,:]
   208    phb_n=nc[n].variables['PHB'][:,:,:,:]
   209    ph=(ph_n+phb_n)/9.81
   210    zh_n=np.zeros(shape=(nt[n],nlay[n]+1,nrow[n],ncol[n],))
   211    for k in range(nlay[n]):
   212      zh_n[:,k+1,:,:]=ph[:,k+1,:,:]-ph[:,0,:,:]
   213    zh_n=np.clip(zh_n,0.,np.max(zh_n))
   214    zh.append(zh_n)
   215
   216  uvwt=np.zeros(shape=(2,3))
   217  delt = 15
   218  s = 0
   219  o_ymdh,o_time,o_xp,o_yp,o_zp,l_xp,l_yp,l_zp=[],[],[],[],[],[],[],[]
   220  itime=0
   221  ymdh=int(DATE)
   222  o_ymdh.append('ymd='+DATE+'_'+str(int(round(zp[s],0))))
   223  o_time.append('hour='+str(itime))
   224  for i in 'ol':
   225    for j in 'xy':
   226      exec(i+'_'+j+'p.append('+j+'p[s]+'+j.upper()+'cent)') #
   227  o_zp.append(zp[s])
   228  l_zp.append(zp[s])
   229  IW=0
   230  #loop for traj as long as in the domain and 24 hours
   231  while not beyond(xp[s], yp[s], zp[s]):
   232    print ('run beyond days' + str(ymdh))
   233  #    break
   234    t0=pdate.hour
   235    t1=t0+BF
   236    if t1==24 or t1<0:
   237      sdate = pdate + timedelta(hours=BF)
   238      nc1,dnt,dnlay,dnrow,dncol,dymd0 = openNC(sdate)
   239
   240    f={}
   241    withdata=[]
   242    uvwg=np.zeros(shape=(3,2,nlay[4],nrow[4],ncol[4],))
   243    for sec in range(0, 3601, delt):
   244      boo = beyond(xp[s], yp[s], zp[s])
   245      if boo: break
   246      for ncft in [(nc0,t0),(nc1,t1)]:
   247        result=get_uvw(ncft,t0,zp[s],yp[s],xp[s])
   248        if result==-1:break
   249        (tt,kk,jj,ii),f=result[0], result[1]
   250        uvwt[tt,:] = [uvwg[i,tt,kk,jj,ii] for i in range(3)]# [f[(tt,kk,jj,ii)][i](yp[s],xp[s]) for i in range(3)]
   251      if result==-1:break
   252      fcnt=interpolate.interp1d([0,3600], uvwt,axis=0)
   253      ub, vb, wb= fcnt(sec)
   254      xp[s], yp[s], zp[s] = xp[s]+BF*delt * ub, yp[s]+BF*delt * vb,  zp[s]+BF*delt * wb
   255      l_xp.append(xp[s]+Xcent)
   256      l_yp.append(yp[s]+Ycent)
   257      l_zp.append(zp[s])
   258    if result==-1:break
   259    pdate = pdate + timedelta(hours=BF)
   260    ymdh = int(pdate.strftime('%Y%m%d%H'))
   261    itime+=1
   262    o_ymdh.append('ymd='+str(ymdh)+'_'+str(int(round(zp[s],0))))
   263    o_time.append('hour='+str(itime))
   264    o_xp.append(xp[s]+Xcent)
   265    o_yp.append(yp[s]+Ycent)
   266    o_zp.append(zp[s])
   267
   268    if pdate.strftime('%Y%m%d') != ymd0:
   269      nc0,dnt,dnlay,dnrow,dncol, ymd0 = openNC(pdate)
   270      nc1=nc0
   271    df=DataFrame({'ymdh':o_ymdh,'xp':o_xp,'yp':o_yp,'zp':o_zp,'Hour':o_time})
   272    col=['xp','yp','Hour','ymdh','zp']
   273    name='trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
   274    # output the line segments for each delta_t
   275    dfL=DataFrame({'TWD97_x':l_xp,'TWD97_y':l_yp,'zp':l_zp})
   276    if IW==0:
   277      df[col].set_index('xp').to_csv(name)
   278      dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'))
   279      IW=1
   280    else:
   281      df[col].set_index('xp').to_csv(name,mode='a',header=False)
   282      dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'),mode='a',header=False)
   283    o_ymdh,o_time,o_xp,o_yp,o_zp,l_xp,l_yp,l_zp=[],[],[],[],[],[],[],[]
   284
   285  #make kml file
   286  dir='NL'
   287  if not BACK:dir='RL'
   288  os.system('csv2kml.py -f '+name+' -n '+dir+' -g TWD97')
   289  os.system('csv2bln.cs '+name)
```



### do_bt1.cs 動態執行批次檔
argument:
     $1=station name
     $2=month(2 digits)
     $3=day

```bash
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat do_bt1.cs
#do_bt1 station mm dd
st=$1
for y1 in {16..16};do
y=20$y1
#for m in {02..03};do
m=$2
ym=$y1$m
#for d in {01..31};do
d=$3
  h=00
  if ! [ -e links/wrfout_d04_${y}-${m}-${d}_${h}:00:00 ];then continue;fi
  for h in {00..23};do
    if [ -e trj_results${ym}/trj${st}${y}${m}${d}${h}.csv ];then continue;fi
    n=$(psg bt2.py|wc -l)
    while true;do
      if [ $n -lt 90 ];then
        touch trj_results${ym}/trj${st}${y}${m}${d}${h}.csv
        sub python bt2.py -t $st -d ${y}${m}${d}${h} -b True >& dum
        sleep 5s
        break
      else
        sleep 5s
        n=$(psg bt2.py|wc -l)
      fi
    done
  done
#done
#done
done
```

## 叢集分析
### choose10 .py(前處理)
從前述bt2.py所得之軌跡點L.csv檔案，選取其中10個點，將20個維度之矩陣進行k_means分析
輸入檔案：
     tmplateD1_3km.nc：讀取網格設定，以簡化軌跡點
     fnames.txt(檔案路徑名稱之listing)
輸出檔案：
     *10.csv

```python
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat -n choose10.py
     1  import os, sys
     2  import netCDF4
     3  import twd97
     4  from pandas import *
     5  import bisect
     6
     7  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
     8  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
     9
    10  nc = netCDF4.Dataset('/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_3km.nc','r')
    11
    12  ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
    13  tex=10**ex
    14  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
    15  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
    16
    17  os.system('ls trjzhongshan*L.csv>fnames.txt')
    18  with open('fnames.txt','r')as f:
    19    fnames=[i.strip('\n') for i in f]
    20
    21  for fname in fnames:
    22  #  if os.path.isfile(fname+'10.csv'):continue
    23    df=read_csv(fname)
    24    x=np.array(df.TWD97_x)-Xcent
    25    y=np.array(df.TWD97_y)-Ycent
    26    ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
    27    iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
    28    df['JI']=[j*tex+i for i,j in zip(ix,iy)]
    29    reduced_ji=[]
    30    for i in range(1,len(df)):
    31      if df.JI[i-1]!=df.JI[i]:
    32        reduced_ji.append(df.JI[i-1])
    33    df=DataFrame({'JI3':reduced_ji})
    34    if len(df)<10:continue
    35    ji10=[df.JI3[i] for i in range(0,len(df),int(len(df)/10))]
    36    df=DataFrame({'JI3':ji10[:10]})
    37    df.set_index('JI3').to_csv(fname+'10.csv')
```



### km.py
- arguments:條列*10.csv檔案路徑名稱之文字檔nclt: number of clusters
- 輸入檔*10.csv：choose10.py的結果tmplateD1_3km.nc：由JI轉換成網格化座標位置
- 輸出檔lab.csv：逐時的叢集編號'res'+str(l)+'.csv' ：各叢集的代表性軌跡
- 內掛後處理由csv產生kml→google map繪圖

```python
$ cat -n km.py
     1  import os, sys
     2  import netCDF4
     3  import twd97
     4  from pandas import *
     5  import bisect
     6  import numpy as np
     7  from sklearn.cluster import KMeans
     8
     9  txt=sys.argv[1]
    10  nclt=int(sys.argv[2])
    11  with open(txt, 'r') as f:
    12      fnames=[l.strip('\n') for l in f]
    13  idx=fnames[0].index('20')
    14  #ymdh=np.array([int(i[idx:idx+10]) for i in fnames],dtype=int)
    15  #if len(ymdh)!=len(fnames):sys.exit('wrong length in ymdh')
    16
    17  trjs=np.zeros(shape=(len(fnames),20))
    18  tex=10000
    19  n,m=0,0
    20  ymdh=[]
    21  for fname in fnames:
    22    try:
    23      df=read_csv(fname+'10.csv')
    24    except:
    25      m=m+1
    26      continue
    27    trjs[n,:10]=[i//tex for i in df.JI3]
    28    trjs[n,10:]=[i%tex for i in df.JI3]
    29    ymdh.append(int(fname[idx:idx+10]))
    30    n+=1
    31  trjs=trjs[:-m,:]
    32  clt = KMeans(n_clusters = nclt)
    33
    34  clt.fit(trjs)
    35  a=clt.labels_
    36  dfa=DataFrame({'lab':a,'ymdh':ymdh})
    37  dfa.set_index('lab').to_csv('lab.csv')
    38
    39  ji=np.array(clt.cluster_centers_,dtype=int)
    40  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
    41  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    42  nc = netCDF4.Dataset('/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_3km.nc','r')
    43  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
    44  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
    45  for l in range(nclt):
    46    des=['Line'+str(l)+'_'+str(i) for i in range(10)]
    47    df=DataFrame({'TWD97_x':[Xcent+x_mesh[i] for i in ji[l,10:]],'TWD97_y':[Ycent+y_mesh[i] for i in ji[l,:10]],'lab':des,'des':des})
    48    df.set_index('TWD97_x').to_csv('res'+str(l)+'.csv')
    49  os.system('for i in {0..'+str(nclt-1)+'};do cp res$i.csv res${i}L.csv;done')
    50  os.system('for i in {4..'+str(nclt-1)+'};do csv2kml.py -f res$i.csv -g TWD97 -n RL;done')
    51  os.system('for i in {2..3};do csv2kml.py -f res$i.csv -g TWD97 -n HL;done')
    52  os.system('for i in {0..1};do csv2kml.py -f res$i.csv -g TWD97 -n NL;done')
```
## google map繪圖、軌跡命名
由於叢集分析結果為數字，需繪圖後、從google map上軌跡點之說明內容，來定義數字與文字(區域方向)之對照(path.txt)
可以參考筆記(繪製逆軌跡圖流程、csv2kml)


```
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests/kmean_spr
$ cat n_clusters6/path.txt
1SH     5 Shang Hai and northwestern China
2BJ     3 Bei Jing
3SW     1 South Western of stations
4LOCAL  2 Local Circulations
6BH     0 Bo Hai
7SC     4 Southern China
```



## 其他後處理
### acc_prob.py
從軌跡點L.csv檔案，統計網格通過機率，以便進行繪圖
輸入檔案：
     fnames.txt(檔案路徑名稱之listing)
輸出檔案：
     probJ.nc
單位：crossing time/total time

```python
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat -n acc_prob.py
     1  import numpy as np
     2  import netCDF4
     3  import os,sys, json
     4  import twd97
     5  from pandas import *
     6  import bisect
     7  import datetime
     8
     9
    10  def dt2jul(dt):
    11    yr=dt.year
    12    deltaT=dt-datetime.datetime(yr,1,1)
    13    deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
    14    return (yr*1000+deltaT.days+1,deltaH*10000)
    15
    16  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
    17  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    18  os.system('cp ../tmplateD1_27km.nc probJ.nc')
    19  v='O' #v is depend to templates var. names
    20  nc = netCDF4.Dataset('probJ.nc','r+')
    21  nc.XORIG
    22  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
    23  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
    24  #os.system('ls trjj*L.csv > fnames.txt')
    25  with open('fnames.txt', 'r') as f:
    26    fnames=[l.strip('\n') for l in f]
    27  nc.variables[v][0,0,:,:]=np.zeros(shape=(nc.NROWS,nc.NCOLS))
    28  i=fnames[0].index('2')
    29  DATE=fnames[0][i:i+11]
    30  sdate = datetime.datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:10]))
    31  nt,nvars,ndt=nc.variables['TFLAG'].shape
    32  for idt in range(2):
    33    nc.variables['TFLAG'][0,:,idt]=[dt2jul(sdate)[idt] for i in range(nvars)]
    34  ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
    35  tex=10**ex
    36  for fname in fnames:
    37    df=read_csv(fname)
    38    if len(df)==0:continue
    39    x=np.array(df.TWD97_x)-Xcent
    40    y=np.array(df.TWD97_y)-Ycent
    41    ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
    42    iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
    43    df['JI']=[j*tex+i for i,j in zip(ix,iy)]
    44    pv=pivot_table(df,index='JI',values='TWD97_x',aggfunc='count').reset_index()
    45    pv.TWD97_x=np.array(pv.TWD97_x)*15./3600./len(fnames) #in unit of hr/total hr in that month
    46    pv['I']=[ji%tex for ji in pv.JI]
    47    pv['J']=[ji//tex for ji in pv.JI]
    48    for i in range(len(pv)):
    49      nc.variables[v][0,0,pv.J[i],pv.I[i]]+=pv.TWD97_x[i]
    50  nc.close()
```


Links
Here：WRF三維軌跡與叢集分析*
