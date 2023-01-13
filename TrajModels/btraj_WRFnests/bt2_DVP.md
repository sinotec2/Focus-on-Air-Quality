---
layout: default
title: 三維反軌跡線之計算
nav_order: 2
parent: WRF三維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-25 12:03:57
tags: trajectory
---

# 三維反軌跡線之計算
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

- 這支反軌跡線計算程式([bt2_DVP.py][bt2_DVP.py])的特殊性在於：
  1. 以wrfout 3維風場為3個方向風速之數據來源。因垂直向的網格非等間距，需要特別處理。
  1. 因為是3維軌跡線，在近地面及高空最頂層，有可能離開模擬範圍，需要讓計算迴圈可以停止。
  1. 由於多數後處理與繪圖軟體是2維架構，需要將高度結果妥善安排。
  1. 做為後續wrfout 2維地面反軌跡計算程式([ftuv10.py][ftuv10.py])的原型，程式所定義的函數需更通用化。

## 程式之使用

### 引數

- 3組引數、次序不拘、每一組含tag及值，tag及值必須成組出現，如以下範例：
- \-t daliao (測站名稱)
  - 名稱必須出現在`sta_list.json`檔案內，小寫漢語拼音。
  - 也接受(lat,lon)、(twd97_x,y)(公里或公尺)之組合
  - 不接受2或多個測站的輸入
- \-d 2017123112 (軌跡起始的年月日時)
  - 必須有10碼
  - UTC(配合wrfout)
- \-b T (是否為反軌跡 T/F)
- do_bt1.cs腳本中之應用

```bash
        sub python bt2.py -t $st -d ${y}${m}${d}${h} -b True >& dum
```

### 輸入檔

- `sta_list.json`：測站編號名稱
- `path+'sta_ll.csv`：測站經緯度
- `['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]`：各層wrfout檔案(也可以是連結)

### 輸出檔

- 檔名規則：`'trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'`
- 軌跡點時間間距：15S

### 程式內掛後處理(不執行不影響主要結果)

- [csv2kml.py][csv2kml]：繪製google map
- [csv2bln.cs](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/traj/#csv2bln)：bln file is used for surfer plotting

## 自定義函數

### get_uvw

- 這個函數的用意在於讀取wrfout中特定時間、空間的風速數據，get_uvw函數出現在[bt2_DVP.py][bt2_DVP.py]、[ft2.py][ft2.py]、[ftuv10.py][ftuv10.py]
- 引數(ncft,t0,z,y,x)
  - ncft：nc檔案、時間。2者所組成的tuple。
  - t0：前一個小時
  - z,y,x：軌跡點之座標
- 回覆
  - idx：軌跡點在4度空間位置的指標
  - f：idx所形成的集合

```python
#get the UVW data from NC files
#z not interpolated yet
def get_uvw(ncft,t0,z,y,x):
  (ncf,t1)=ncft[:]
  t=abs(t1-t0)
  n0=locate_nest(x,y)
  #make sure the point is in d1(at least)
  if n0==-1:
    return -1
  iii=int(x//dx[4]+ncol[4]//2)
  jjj=int(y//dx[4]+nrow[4]//2)
  kkk=int(z//dz)
  idx=(t,kkk,jjj,iii)
  if idx in f: return idx,f
...
```

- uvwg矩陣之讀取與應用
  - 此一矩陣額有5個維度，分別是3個分量、時間、3度空間
  - 其值在本函數內由nc檔案中讀取(如下)、在主程式內進行時間軸的線性內插

```python
...
          #average the stagger wind to the grid_points
          uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U'][t1,k,j,i]+ncf[n].variables['U'][t1,k,j,i+1])/2.
          uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V'][t1,k,j,i]+ncf[n].variables['V'][t1,k,j+1,i])/2.
          uvwg[2,t,kk,jj,ii]=(ncf[n].variables['W'][t1,k,j,i]+ncf[n].variables['W'][t1,k+1,j,i])/2.
```

- uvwg 矩陣回到主程式內進行時間軸的線性內插，得到指定時間(`sec`)的三個風速分量(`ub, vb, wb`)

```python
...
uvwt[tt,:] = [uvwg[i,tt,kk,jj,ii] for i in range(3)]# [f[(tt,kk,jj,ii)][i](yp[s],xp[s]) for i in range(3)]
...
fcnt=interpolate.interp1d([0,3600], uvwt,axis=0)
ub, vb, wb= fcnt(sec)
```

### openNC

- 按照輸入的日期(`sdate`)開啟wrfout的nc檔
- 一次開啟所有範圍之wrfout(d01~d04)
- 回覆主程式項目
  - ncf：4個wrfout之nc檔案
  - nt, nlay, nrow, ncol：時間及空間之維度長度
  - ymd.replace('-','')：`sdate`年月日字串

```python
#open the NC's for some day (this present day, first time, or next/yesterday)
def openNC(sdate):
  ymd = sdate.strftime('%Y-%m-%d')
  fnames=['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]
  ncf,nt,nlay,nrow,ncol=[],[],[],[],[]
  for fname in fnames:
    if not os.path.isfile(fname): sys.exit('no file for '+fname)
    nc1=netCDF4.Dataset(fname,'r')
    ncf.append(nc1)
    v4=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))
    t,lay,row,col=nc1.variables['T'].shape
    for v in 't,lay,row,col'.split(','):
      exec('n'+v+'.append('+v+')')
  return ncf, nt, nlay, nrow, ncol, ymd.replace('-','')
```

### locate_nest

- 這個函數用在判定(x, y)所在位置的網格系統
- 因3層網格系統均以臺灣為中心，因此判別自最內圈開始，如果符合隨即跳出
- 判定原則以座標值是否都在該系統之範圍
- 最外圈(`locate_nest=0`)~最內圈(`locate_nest=0`)之
  - `dx=[81000,27000,9000,3000,3000]`

```python
def locate_nest(x,y):
    for n in range(3,-1,-1):
        if xmin[n]<=x<xmax[n] and ymin[n]<=y<ymax[n]:
            return n
    return -1
```

## 主程式

### 引數之讀取及確認

- 時間及正反軌跡的確認尚屬單純，主要的篇幅在確認測站或指定起始點座標

```python
(d_nstnam, d_namnst) = nstnam()
stnam, DATE, BACK = getarg()
os.system('mkdir -p trj_results'+DATE[2:6])
BACK=str2bool(BACK)
BF=-1
if not BACK:BF=1
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
bdate = datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:]))
nam = [i for i in stnam.split(',')]
if len(nam) > 1:
  try:
    lat = float(nam[0])
    lon = float(nam[1])
  except:
    sys.exit('more than two station, suggest executing iteratively')
  else:
    # in case of lat,lon
    if lat < 90.:
      xy0 = twd97.fromwgs84(lat,lon)
      x0, y0 =([xy0[i]] for i in [0,1])
      x0,y0=x0-Xcent,y0-Ycent
      nam[0] = str(round(lat,2))+'_'+str(round(lon,2))+'_'
    #   in case of twd97_x,y
    else:
      # test the coordinate unit
      if lat>1000.:
        x0, y0 = [lat],[lon]
        x0,y0=x0-Xcent,y0-Ycent
        nam[0] = str(int(lat/1000))+'+'+str(int(lon/1000))+'_'
      else:
        x0, y0 = [lat*1000],[lon*1000]
        x0,y0=x0-Xcent,y0-Ycent
        nam[0] = str(int(lat))+'_'+str(int(lon))+'_'

# len(nam)==1, read the location from csv files
else:
  for stnam in nam:
    if stnam not in d_namnst: sys.exit("station name not right: " + stnam)
  nst = [int(d_namnst[i]) for i in nam]
  # locations of air quality stations
  # read from the EPA web.sprx
  fname = path+'sta_ll.csv'
  sta_list = read_csv(fname)
  x0, y0 = [], []
  for s in nst:
    sta1 = sta_list.loc[sta_list.ID == s].reset_index(drop=True)
    x0.append(list(sta1['twd_x'])[0]-Xcent)
    y0.append(list(sta1['twd_y'])[0]-Ycent)
```

### 軌跡點與程式之初始化

- 主要重點在產生新的垂直網格系統
  - 等間距網格
  - 間距為20m、共251格5000M

```python
...
#_mesh and _g in lamber conifer projection system
x_mesh = [(i-ncol[4]//2)*dx[4] for i in range(ncol[4])]
y_mesh = [(j-nrow[4]//2)*dx[4] for j in range(nrow[4])]
z_mesh = [k*dz for k in range(nlay[4])]
...
```

### 時間之迴圈

- 第一層迴圈
  - 限定軌跡點仍然在範圍內：`while not beyond(xp[s], yp[s], zp[s]):`
- 第二層迴圈
  - 小時內每個步階：`  for sec in range(0, 3601, delt):`
- 迴圈之最內層：累加風速分量造成的位移

```python
...
      uvwt[tt,:] = [uvwg[i,tt,kk,jj,ii] for i in range(3)]# [f[(tt,kk,jj,ii)][i](yp[s],xp[s]) for i in range(3)] 
    if result==-1:break
    fcnt=interpolate.interp1d([0,3600], uvwt,axis=0)
    ub, vb, wb= fcnt(sec)
    xp[s], yp[s], zp[s] = xp[s]+BF*delt * ub, yp[s]+BF*delt * vb,  zp[s]+BF*delt * wb
    l_xp.append(xp[s]+Xcent)	
    l_yp.append(yp[s]+Ycent)	
    l_zp.append(zp[s])
...
```

### 輸出檔案及後處理

- 使用`to_csv(name,mode='a',header=False)`技巧逐時輸出、並將序列歸零，以降低記憶體需求。
- 不輸出表頭，以方便月份或季節之合併分析。
- 每一條軌跡線都產生kml檔案，以利結果之確認偵錯。

```python
  if pdate.strftime('%Y%m%d') != ymd0:
    nc0,dnt,dnlay,dnrow,dncol, ymd0 = openNC(pdate)
    nc1=nc0
  df=DataFrame({'ymdh':o_ymdh,'xp':o_xp,'yp':o_yp,'zp':o_zp,'Hour':o_time})
  col=['xp','yp','Hour','ymdh','zp']
  name='trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
  # output the line segments for each delta_t
  dfL=DataFrame({'TWD97_x':l_xp,'TWD97_y':l_yp,'zp':l_zp})
  if IW==0:
    df[col].set_index('xp').to_csv(name)
    dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'))
    IW=1
  else:
    df[col].set_index('xp').to_csv(name,mode='a',header=False)
    dfL.set_index('TWD97_x').to_csv(name.replace('.csv','L.csv'),mode='a',header=False)
  o_ymdh,o_time,o_xp,o_yp,o_zp,l_xp,l_yp,l_zp=[],[],[],[],[],[],[],[]

#make kml file
dir='NL'
if not BACK:dir='RL'
os.system('csv2kml.py -f '+name+' -n '+dir+' -g TWD97')
os.system('csv2bln.cs '+name)
```

## 程式下載

{% include download.html content="三維反軌跡線之計算程式[bt2_DVP.py][bt2_DVP.py]" %}

[bt2_DVP.py]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/bt2_DVP.py> "三維反軌跡線之計算程式"
[ftuv10.py]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/ftuv10> "地面二維軌跡分析程式"
[ft2.py]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/ft2/> "CWBWRF預報風場之正軌跡分析程式"
[csv2kml]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/csv2kml/> "點狀資訊KML檔之撰寫(csv2kml.py)"