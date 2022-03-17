---
layout: default
title: "grb2wrfout_d04轉檔"
parent: "cwb WRF_3Km"
grand_parent: "wind models"
nav_order: 3
date:               
last_modified_date:   2021-11-30 10:43:16
---

# grb2wrfout_d04轉檔

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
- 續[樓上](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/)、以及[下載](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/get_M-A0064/)程序之說明，此處詳述轉檔歷程。
- 由`grb2`轉到`wrfout_d04`的空間內插問題，詳見[WRF_3Km空間內插](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/gen_D4bin/)說明。
- 雖然`grb2`格式也有其解讀、應用的軟體，然而在空氣污染領域還並不多。因此還是需要轉成`wrfout`的`nc`格式。
- 此處應用[pygrib](https://medium.com/%E6%9F%BF%E7%94%9C%E8%8C%B6%E9%A6%99/pygrib-%E7%AC%AC%E4%B8%80%E7%AB%A0-6b47e54f9085)模組進行`grb2`檔案的解析

## [rd_grbCubicA.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/cwbWRF_3Km/rd_grbCubicA.py_txt)分段說明

### 宣告與基本設定
- 引用模組
  - pygrib的建置比較特別，可以參考[pygrib的安裝、重要語法](http://www.evernote.com/l/AH12nyLrGkBL2qg3WTonSwDC-0Rtq_S9npA/)
  - 空間內插之標籤與權重檔案是以`FortranFile`儲存的，時間內插使用到`CubicSpline`，垂直空間內插使用到`interp1d`。
```python
kuang@MiniWei /Users/Data/cwb/WRF_3Km
$ cat -n rd_grbCubicA.py
     1  #!/opt/anaconda3/envs/gribby/bin/python
     2  import pygrib
     3  import numpy as np
     4  import netCDF4
     5  from scipy.io import FortranFile
     6  from scipy.interpolate import CubicSpline
     7  from scipy.interpolate import interp1d
     8  import datetime
     9  import os
    10  import subprocess
    11
```
- 溫度轉飽和蒸汽壓[Arden Buck equation](https://www.omnicalculator.com/chemistry/vapour-pressure-of-water)
  - `grb2`及`wrfout`的溫度單位都是K，但[Arden Buck equation](https://www.omnicalculator.com/chemistry/vapour-pressure-of-water)溫度單位為C。
```python
    12  def buck(K):
    13      C=K-273.
    14      return 611.21*np.exp((18.678-C/234.5)*C/(257.14+C))
    15
    16
```
- 開啟模版、讀取`d04`的網格數
  - 由於`wrfout`的變數較`grb2`檔案還多，需事先處理好(`ncks -O -x -v VAR1,VAR2... $oldNC $newNC`)。
  - 當然做為模版，也要有正確的時間、空間結構，可以使用`ncks -d`指令裁切既有檔案。
```python
    17  fname='wrfout_d04'
    18  tmax=36+1
    19  nc = netCDF4.Dataset(fname,'r+')
    20  Vs=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    21  nt1,nrow1,ncol1=(nc.variables['U10'].shape[i] for i in range(3))
    22
```
- 讀取空間內插之**標籤**檔案`idxD4.bin`、**權重矩陣**檔案`wtsD4.bin`
  - 因2個網格系統的位置不會隨時間改變，可以事先處理好備用。
```python
    23  #path='/Users/kuang/MyPrograms/UNRESPForecastingSystem/CWB_data/raw/'
    24  #path='/home/cpuff/UNRESPForecastingSystem/CWB_data/raw/'
    25  #path='/nas1/backup/data/CWB_data/raw/'
    26  path='/Users/Data/cwb/WRF_3Km/'
    27  f=FortranFile(path+'idxD4.bin', 'r')
    28  idx=f.read_record(dtype=np.int64)
    29  idx=idx.reshape(nrow1,ncol1,2)
    30
    31  f=FortranFile(path+'wtsD4.bin', 'r')
    32  wts=f.read_record(dtype=np.float64)
    33  wts=wts.reshape(nrow1,ncol1,4)
    34
```
- 時間迴圈前之準備
  - `atbs`:變數名稱對照表，**短**名稱為`wrfout`內的名稱，**長**名稱為`grb2`內的變數屬性
```python
    35  one=np.ones(shape=(nrow1,ncol1),dtype=np.int64)
    36  atbs={'U10': '10 metre U wind component',
    37   'V10': '10 metre V wind component',
    38   'T': 'Temperature',
    39   'V': 'V component of wind',
    40   'U': 'U component of wind',
    41   'W': 'Geometric vertical velocity',
    42   'QVAPOR': 'Relative humidity',
    43   'T2': '2 metre temperature',
    44   'SST': 'Temperature',
    45   'TSK': 'Skin temperature',
    46   'SWNORM': 'Net short-wave radiation flux (surface)',
    47   'SWDOWN': 'Net short-wave radiation flux (surface)',
    48   'PHB': 'Geopotential Height',
    49   'PSFC': 'Surface pressure',
    50   'RAINC':'Total precipitation'}
```
  - `atbs2`:`atbs`中之3維變數
```python
    51  atbs2=[]
    52  for v in atbs:
    53    if v in Vs[2]:atbs2.append(v)
    54  #'U10','V10','T2','SWNORM','SWDOWN','PSFC','SST','TSK']
    55  #atbs2.append('TSLB') #3d in grb but 4d in wrfout
```
- 開啟變數陣列
  - `b`為時間標籤
  - 每個atbs項目都有自己的陣列(`s`開頭的全時間變數、有別於沒有`s`為某時間的變數)
  - `grb2`的高度順序是相反的，`lv`為其標籤。
```python
    56  b=[t for t in range(0,tmax)]
    57  for a in atbs:
    58    if a in atbs2:
    59      exec('s'+a+'=np.zeros(shape=(tmax,nrow1,ncol1),dtype=np.float64)')
    60    else:
    61      exec('s'+a+'=np.zeros(shape=(tmax,11,nrow1,ncol1),dtype=np.float64)')
    62   #'GPH': 'Geopotential Height',
    63
    64  lv=[i for i in range(10,-1,-1)]
    65  PB,level=[],[]
    66
```

### 開啟檔案、讀取變量
- 開始時間迴圈、開啟`grb2`檔案  
```python
    67  for t in range(0,tmax,6):
    68    fname='M-A0064-0'+'{:02d}'.format(t)+'.grb2'
    69    grbs = pygrib.open(fname)
    70
```
- 除累積雨量外、讀取每一`grb2`變數
  - `len(grb)==1`：只有一層數據
  - 有11層數據者：要記得高度須**反向**儲存
  - 海溫`SST`設定為**地面**溫度
```python
    71    for a in set(atbs)-set(['RAINC']):
    72      grb = grbs.select(name=atbs[a])
    73      if len(grb)==1:
    74        cmd=a+'=grb[0].values'
    75        exec(cmd)
    76      else:
    77        arr=[]
    78        for k in range(11):
    79          arr.append(grb[lv[k]].values)
    80        arr=np.array(arr)
    81        exec(a+'=arr')
    82      if len(grb)==11 and len(level)==0:
    83        level=[grb[lv[i]].level for i in range(11)]
    84      if len(grb)==12 and a=='SST':SST=grb[11].values
```
- 由`gr2`的相對濕度計算`wrfout`中的水汽量
```python
    85    nlay,nrow,ncol=QVAPOR.shape
    86    if len(PB)==0:
    87      PB=np.ones(shape=(nlay,nrow,ncol),dtype=np.int64)
    88      for k in range(nlay):
    89        PB[k,:,:]=level[k]*100
    90    ps=buck(T)
    91    QVAPOR=QVAPOR/100.*(ps*18.)/(PB*28.)
    92
```
- 累積雨量之計算
  - `grb2`是逐6小時累積，`wrfout`是逐時累積
```python
    93    a='RAINC'
    94    if t==0:rain_old=np.zeros(shape=(nrow,ncol))
    95    t6=min([t+6,84])
    96    fname='M-A0064-0'+'{:02d}'.format(t6)+'.grb2'
    97    try:
    98      rain_acc=pygrib.open(fname)[62].values
    99    except:
   100      rain_acc=rain_old
   101    arr=(rain_acc-rain_old)/6. #average along 6 hrs
   102    exec(a+'=arr')
   103    rain_old[:]=rain_acc[:]
   104
```

### 空間內插
- 空間內插，並儲存在全時間變數陣列中
  - 因2個檔案的解析度一樣，簡單的線性內插即可，然因原點與投影略有差異，還是有內插模式，詳見[WRF_3Km空間內插](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/gen_D4bin/)說明。
  - 2度空間變數與3度空間變數分開處理，後者逐層處理
```python
   105    for a in atbs:
   106      exec('var='+a)
   107      n=var.ndim
   108      if n==2:
   109        kk=0
   110        for jj in [0,1]:
   111          for ii in [0,1]:
   112            vr=var[idx[:,:,0]+one*jj,idx[:,:,1]+one*ii]
   113            exec('s'+a+'[t,:,:]+=vr[:,:]*wts[:,:,kk]')
   114            kk+=1
   115      elif n==3:
   116        for k in range(11):
   117          kk=0
   118          for jj in [0,1]:
   119            for ii in [0,1]:
   120              vr=var[k,idx[:,:,0]+one*jj,idx[:,:,1]+one*ii]
   121              exec('s'+a+'[t,k,:,:]+=vr[:,:]*wts[:,:,kk]')
   122              kk+=1
```

### 時間內插 
- 取得分析時間的時間標籤
  - 校正到UTC 0600
```python
   123  #time stamps
   124    if t==0:
   125      V=grbs[1]
   126      beg_time=V.analDate
   127      if beg_time.hour != 6:
   128        beg_time=beg_time-datetime.timedelta(days=beg_time.hour/24)+datetime.timedelta(days=6/24)
   129
 ```
- 結束時間迴圈、進行時間內插
  - 產生`wrfout`逐時的時間標籤
```python
   130  X=[i for i in range(0,tmax,6)]
   131  Hstart=14 #begin local time(20 for CAMx, 14 for fitting WRF GMT 0600)
   132  for t in range(0,tmax):
   133    time=beg_time+datetime.timedelta(days=t/24.)
   134    b[t]=np.array([bytes(i,encoding='utf-8') for i in time.strftime("%Y-%m-%d_%H:%M:%S")])
   135  wname=''
   136  for i in b[0]:
   137    wname+=i.decode('utf-8')
   138
```
- 3維變數的時間內插
  - `TSLB`在`grb2`是3度，在`wrfout`是4度  
```python
   139  for a in atbs2:
   140    exec('ss=np.array([s'+a+'[t,:,:]   for t in range(0,tmax,6)])')
   141    cs = CubicSpline(X,ss)
   142    for t in range(0,tmax):
   143      if t%6==0:continue
   144      exec('s'+a+'[t,:,:]=cs(t)')
   145    if a == 'TSLB':
   146      exec('nc.variables["'+a+'"][:,0,:nrow1,:ncol1]=s'+a+'[Hstart-14:Hstart+10,:,:]')
   147    else:
   148      exec('nc.variables["'+a+'"][:,:,:]=s'+a+'[Hstart-14:Hstart+10,:,:]')
```
- 4維變數的時間內插
  - 同前`TSLB`之計算
```python
   150  for a in set(atbs)-set(atbs2):
   151    exec('ss=np.array([s'+a+'[t,:,:,:] for t in range(0,tmax,6)])')
   152    cs = CubicSpline(X,ss)
   153    for t in range(0,tmax):
   154      if t%6==0:continue
   155      exec('s'+a+'[t,:,:,:]=cs(t)')
   156    exec('nc.variables["'+a+'"][:,:nlay,:nrow1,:ncol1]=s'+a+'[Hstart-14:Hstart+10,:,:,:]')
   157
```

### 個別變數再加工
- 壓力的計算
  - `wrfout`的壓力有基準量、擾動量之分，`grb2`只有固定層壓力
```python
   158  #pressure
   159  v='PB'
   160  nt,nlay,nrow,ncol=nc.variables[v].shape
   161  for k in range(nlay):
   162    nc.variables[v][:,k,:,:]=level[k]*100.
   163  nc.variables['P'][:]=0.
   164
```
- 重力位高
  - 同樣`wrfout`的的高度也有基準量、擾動量之分。前者令為所有時間的平均值，後者即為差值。
  - 地面設為地形高度
```python
   165  #geopotential heights
   166  v='PHB'
   167  nc.variables['PH'][:]=0.
   168  PHB=nc.variables[v][:]*9.8
   169  PHBm=np.mean(PHB,axis=0) #const in time
   170  PH=PHB[:,:,:,:]-PHBm[None,:,:,:]
   171  PHBm=PHB-PH
   172  #surface geopotential height=HGT*9.8
   173  HGT=nc.variables['HGT'][:,:,:]*9.8
   174  for k in range(nlay):
   175    nc.variables['PH'][:,k+1,:,:]=PH[:,k,:,:]
   176  nc.variables[v][:,0,:,:]=HGT
   177  for k in range(nlay):
   178    nc.variables[v][:,k+1,:,:]=PHBm[:,k,:,:]+HGT[0,:,:]
   179
```
- 位溫
  - 溫度基準為定值
```python
   180  #potential temperature
   181  v='T' #WRF is temp "pertubation"
   182  PB,TK=nc.variables['PB'][:],nc.variables[v][:]
   183  nc.variables[v][:]=TK*(100000./PB)**0.286
   184  nc.variables[v][:]-=nc.variables['T00'][0]
   185
```
- 表面溫度
  - 令為`T2`
```python
   186  #T2->TSK
   187  nc.variables['TSK'][:]=nc.variables['T2'][:]
   188
```
- 逐時雨量累加成為累積雨量
```python
   189  v='RAINC'
   190  for t in range(1,24):
   191    nc.variables[v][t,:,:]+=nc.variables[v][t-1,:,:]
   192
```

### 行星邊界層高度
- 求解行星邊界層高度。由於`grb2`沒有相關任何訊息，此處以混合層高度代之。
  - 先求出`dt/dz`值(使用`np.diff`[指令](https://vimsky.com/zh-tw/examples/usage/numpy-diff-in-python.html))
```python
   193  v='PBLH'
   194  #PBLH=nc.variables[v][:]
   195  #for t in range(24):
   196  #  t_wrf=(t+6)%24
   197  #  nc.variables[v][t,:,:]=PBLH[t_wrf,:,:]
   198  T0=nc.variables['T2'][:]*(100000./nc.variables['PSFC'][:])**0.286
   199  T=nc.variables['T'][:]+290
   200  H=(nc.variables['PH'][:]+nc.variables['PHB'][:])/9.8
   201  nt,nlay,nrow,ncol=(H.shape[i] for i in range(4))
   202  nk=nlay-1
   203  HT=np.zeros(shape=T.shape)
   204  for k in range(nk):
   205    HT[:,k,:,:]=(H[:,k,:,:]+H[:,k+1,:,:])/2.-H[:,0,:,:]
   206
```
- 地面溫度少於其他高度者：混合層限制在最低高度
```python
   207  mixH=np.zeros(shape=T0.shape)
   208  minT=np.min(T,axis=1)
   209  idx=np.where(T0<=minT)
   210  HT0=np.array([max(35,i) for i in HT[:,0,:,:].flatten()]).reshape(HT[:,0,:,:].shape)
   211  mixH[idx[:]]=HT0[idx[:]]
   212
```
- 無逆溫者使用`interp1d`[指令](https://vimsky.com/zh-tw/examples/usage/python-scipy.interpolate.interp1d.html)內插到符合地面溫度的高度  
```python
   213  #potential temperature vertical profile is increasingly sorted
   214  dT=np.diff(T,axis=1)
   215  dTmin=np.min(dT,axis=1)
   216  idx=np.where((dTmin>=0)&(T0>minT))
   217  for n in range(len(idx[0])):
   218    t,j,i=(idx[k][n] for k in range(3))
   219    f=interp1d(T[t,:,j,i],HT[t,:,j,i])
   220    mixH[t,j,i]=f(T0[t,j,i])
   221
```
- 有逆溫者找到逆溫層高度
```python
   222  #with inversions
   223  idx=np.where((dTmin<0)&(T0>minT))
   224  for n in range(len(idx[0])):
   225    t,j,i=(idx[k][n] for k in range(3))
   226    k=list(dT[t,:,j,i]).index(dTmin[t,j,i])+1
   227    mixH[t,j,i]=HT[t,k,j,i]
   228  nc.variables[v][:]=mixH[:]
   229
```

### 時間標籤與屬性資料之寫入
- 寫入時間標籤
- 修改`wrfout`檔案屬性訊息  
  - 修改開始時間
  - 修改垂直層數：因變數`BOTTOM-TOP_GRID_DIMENSION`含減號`-`，不能在`python`中處理，必須用`ncatted`[指令](https://atmosai.github.io/2019/04/2019-04-12-ncattednetcdf%E5%B1%9E%E6%80%A7%E7%BC%96%E8%BE%91/)在OS處理。
  - 將`wrfout_d04`更名
```python
   230  v='Times'
   231  nc.variables[v][:,:]=b[Hstart-14:Hstart+10][:]
   232  btime= beg_time.strftime("%Y-%m-%d_%H:%M:%S")
   233  nc.SIMULATION_START_DATE=btime
   234  nc.START_DATE           =btime
   235  yr=beg_time.year
   236  nc.JULYR                =yr
   237  nc.JULDAY               =int((beg_time-datetime.datetime(yr,1,1)).total_seconds()/24/3600.)+1
   238  nc.close()
   239  ncatted='/usr/local/bin/ncatted'#subprocess.check_output('which ncatted',shell=True).decode('utf8').strip('\n')
   240  os.system(ncatted+' -a BOTTOM-TOP_GRID_DIMENSION,global,o,i,12 wrfout_d04')
   241  os.system('mv wrfout_d04 wrfout_d04_'+wname)
```

## 下載程式碼
- 可以由[github](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/cwbWRF_3Km/rd_grbCubicA.py_txt)找到原始碼。

## 檢核
- 可以使用[MeteoInfo](http://meteothink.org/)或[CWB網站](https://npd.cwb.gov.tw/NPD/products_display/product?menu_index=1)

## Reference
- sinotec2, **pygrib的安裝、重要語法**, [evernote](http://www.evernote.com/l/AH12nyLrGkBL2qg3WTonSwDC-0Rtq_S9npA/), 2021年4月1日
- Yaqiang Wang, **MeteoInfo Introduction**, [meteothink](http://meteothink.org/), 2021,10,16