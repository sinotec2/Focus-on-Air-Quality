---
layout: default
title: ftuv10.py
nav_order: 1
parent: 地面二維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2024-04-09 17:18:14
tags: trajectory CWBWRF CODiS geojson
---

# ftuv10.py程式說明
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

- 因為讀取風場格式的特性，[ftuv10.py][ftuv10]比較類似[bt2_DVP.py][bt2_DVP]3維軌跡分析的2維版本，而不像讀取測站觀測數據的[traj2kml.py][traj2kml.py]。
- 程式的IO與使用方法也與[bt2_DVP.py][bt2_DVP]相同
  
### 程式運作原理

- 讀取地面10m高度之風場(wrfout格式)
- 自測站開始進行2維反軌跡計算
- 超過3公里解析度之模式模擬範圍，則繼續讀取15公里解析度檔案。
- 輸出結果(csv檔案)可以轉成geojson檔案，貼在[GitHub Pages](https://sinotec2.github.io/traj/)畫面

## Usage

- 本程式為[daily_traj.cs][daily_traj_cs]的核心程式，其運作方式如下

```bash
PY=/Users/Data/cwb/e-service/btraj_WRFnests/ftuv10_5d.py
cd /Library/WebServer/Documents
today=$(date +%Y%m%d)
for t in zhongshan zhongming jiayi qianjin;do
  $PY -t $t -d ${today}12 -b True
```

## 2/3維程式碼差異

項目|3維版本[bt2_DVP.py][bt2_DVP]|2維版本[ftuv10.py][ftuv10]|說明
:-:|:-:|:-:|:-:|
wrfout來源|自行模擬|CWB數值預報|
nc檔案個數(層數)|4|2|

```python
$ diff /Users/Data/cwb/e-service/btraj_WRFnests/bt2_DVP.py /Users/Data/cwb/e-service/btraj_WRFnests/ftuv10.py
19,20c17,18
<   (ncf,t1)=ncft[:]
<   t=abs(t1-t0)
---
>   (ncf,tt)=ncft[:]
>   t=1#abs(tt-t0)
36c34
<     iz=bisect.bisect_left(zh[n][t1,:,iy,ix],z)
---
>     iz=1 #bisect.bisect_left(zh[n][t1,:,iy,ix],z)
47,49c45,47
<           uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U'][t1,k,j,i]+ncf[n].variables['U'][t1,k,j,i+1])/2.
<           uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V'][t1,k,j,i]+ncf[n].variables['V'][t1,k,j+1,i])/2.
<           uvwg[2,t,kk,jj,ii]=(ncf[n].variables['W'][t1,k,j,i]+ncf[n].variables['W'][t1,k+1,j,i])/2.
---
>           uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U10'][tt,j,i]+ncf[n].variables['U10'][tt,j,i+1])/2.
>           uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V10'][tt,j,i]+ncf[n].variables['V10'][tt,j+1,i])/2.
>           uvwg[2,t,kk,jj,ii]=0.#(ncf[n].variables['W'][tt,k,j,i]+ncf[n].variables['W'][tt,k+1,j,i])/2.
74c72
<     for n in range(3,-1,-1):
---
>     for n in range(1,-1,-1):
109,110c107,109
< def beyond(xpp, ypp, zpp):
<   boo = not ((xpp - x_mesh[0]) * (xpp - x_mesh[-1]) < 0 and \
---
> def beyond(xpp, ypp, zpp, ddt):
>   dday= abs(ddt.total_seconds()/3600/24)
>   boo = not (((xpp - x_mesh[0]) * (xpp - x_mesh[-1]) < 0 and \
112c111,112
<              (zpp - z_mesh[0]) * (zpp - z_mesh[-1]) < 0)
---
>              (zpp - z_mesh[0]) * (zpp - z_mesh[-1]) < 0  ) and \
>                        (dday < 3))
118,120c118,123
<   ymd = sdate.strftime('%Y-%m-%d')
<   fnames=['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]
<   ncf,nt,nlay,nrow,ncol=[],[],[],[],[]
---
>   gdate=sdate+timedelta(hours=-8)
>   dd=0
>   if gdate.hour<6:dd=-1
>   ymd = (gdate+timedelta(days=dd)).strftime('%Y-%m-%d')
>   fnames=['/Users/Data/cwb/e-service/btraj_WRFnests/CWB_forecast/U10V10_d0'+str(i)+'_'+ymd+'_06:00:00' for i in [1,3]]
>   ncf,mt,mlay,mrow,mcol,dtimes=[],[],[],[],[],[]
125,126c128,130
<     v4=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))
<     t,lay,row,col=nc1.variables['T'].shape
---
>     v3=list(filter(lambda x:nc1.variables[x].ndim==3, [i for i in nc1.variables]))
>     t,row,col=nc1.variables['U10'].shape
>     lay=1
128,129c132,144
<       exec('n'+v+'.append('+v+')')
<   return ncf, nt, nlay, nrow, ncol, ymd.replace('-','')
---
>       exec('m'+v+'.append('+v+')')
>     #get Times in datetime form (local time)
>     dtime=[]
>     for it in range(t):
>       s=''
>       for j in [i.decode('utf-8') for i in nc1.variables['Times'][it,:]]:
>         s+=j
>       dtime.append(datetime.strptime(s,"%Y-%m-%d_%H:00:00")+timedelta(hours=8))
>     if sdate not in dtime:
>       return [[-1] for i in range(6)]
> #sys.exit('Times not right'+ymd)
>     dtimes.append(dtime)
>   return ncf, mt, mlay, mrow, mcol, dtimes
131c146
< path='/nas1/backup/data/cwb/e-service/surf_trj/'
---
> path='/Users/Data/cwb/e-service/surf_trj/'
136d150
< os.system('mkdir -p trj_results'+DATE[2:6])
141a156,158
> pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
>         lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
>
153,155c170,173
<       xy0 = twd97.fromwgs84(lat,lon)
<       x0, y0 =([xy0[i]] for i in [0,1])
<       x0,y0=x0-Xcent,y0-Ycent
---
> #      xy0 = twd97.fromwgs84(lat,lon)
> #      x0, y0 =([xy0[i]] for i in [0,1])
> #      x0,y0=x0-Xcent,y0-Ycent
>       x0,y0=pnyc(lon,lat, inverse=False)
181,182c199,201
<     x0.append(list(sta1['twd_x'])[0]-Xcent)
<     y0.append(list(sta1['twd_y'])[0]-Ycent)
---
>     xx0,yy0=pnyc(list(sta1['lon'])[0],list(sta1['lat'])[0], inverse=False)
>     x0.append(xx0) #list(sta1['twd_x'])[0]-Xcent)
>     y0.append(yy0) #list(sta1['twd_y'])[0]-Ycent)
185a205
> nc, nt, nlay, nrow, ncol, dtimes0 = openNC(bdate)
187d206
< nc, nt, nlay, nrow, ncol, ymd0 = openNC(pdate)
191,193c210,212
< nrow.append(nrow[0]*27)
< ncol.append(ncol[0]*27)
< dx=[81000,27000,9000,3000,3000]
---
> nrow.append(nrow[0]*5)
> ncol.append(ncol[0]*5)
> dx=[15000,3000,3000]
195c214
< fac=[dx[n]//dx[4] for n in range(5)]
---
> fac=[dx[n]//dx[2] for n in range(3)]
197,199c216,218
< x_mesh = [(i-ncol[4]//2)*dx[4] for i in range(ncol[4])]
< y_mesh = [(j-nrow[4]//2)*dx[4] for j in range(nrow[4])]
< z_mesh = [k*dz for k in range(nlay[4])]
---
> x_mesh = [(i-ncol[2]//2)*dx[2] for i in range(ncol[2])]
> y_mesh = [(j-nrow[2]//2)*dx[2] for j in range(nrow[2])]
> z_mesh = [k*dz for k in range(nlay[2])]
201,214c220,233
< xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(4)]
< xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(4)]
< ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(4)]
< ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(4)]
< zh=[]
< for n in range(4):
<   ph_n=nc[n].variables['PH'][:,:,:,:]
<   phb_n=nc[n].variables['PHB'][:,:,:,:]
<   ph=(ph_n+phb_n)/9.81
<   zh_n=np.zeros(shape=(nt[n],nlay[n]+1,nrow[n],ncol[n],))
<   for k in range(nlay[n]):
<     zh_n[:,k+1,:,:]=ph[:,k+1,:,:]-ph[:,0,:,:]
<   zh_n=np.clip(zh_n,0.,np.max(zh_n))
<   zh.append(zh_n)
---
> xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(2)]
> xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(2)]
> ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(2)]
> ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(2)]
> #zh=[]
> #for n in range(2):
> #  ph_n=nc[n].variables['PH'][:,:,:,:]
> #  phb_n=nc[n].variables['PHB'][:,:,:,:]
> #  ph=(ph_n+phb_n)/9.81
> #  zh_n=np.zeros(shape=(nt[n],nlay[n]+1,nrow[n],ncol[n],))
> #  for k in range(nlay[n]):
> #    zh_n[:,k+1,:,:]=ph[:,k+1,:,:]-ph[:,0,:,:]
> #  zh_n=np.clip(zh_n,0.,np.max(zh_n))
> #  zh.append(zh_n)
```

### 時間迴圈

```python
231,232c250,251
< while not beyond(xp[s], yp[s], zp[s]):
<   print ('run beyond days' + str(ymdh))
---
> while not beyond(xp[s], yp[s], zp[s], pdate-bdate):
> #  print ('run within domain, ymdh=' + str(ymdh))
234c253
<   t0=pdate.hour
---
>   t0=dtimes0[0].index(pdate)
236c255,260
<   if t1==24 or t1<0:
---
>   if nt[0]==24:
>     boo=(t1==nt[0])
>   else:
>     boo=(bdate.hour+int(abs((pdate-bdate).total_seconds()/3600))==nt[0])
>   if boo or t1<0:
>     if nt[0]!=24:break
238c262,267
<     nc1,dnt,dnlay,dnrow,dncol,dymd0 = openNC(sdate)
---
>     nc1,nt,dnlay,dnrow,dncol, dtimes0 = openNC(sdate)
>     if type(nc1)==int:break
>     if BACK:
>       t1=t1+nt[0]
>     else:
>       t1=0
244,245c273,276
<     boo = beyond(xp[s], yp[s], zp[s])
<     if boo: break
---
>     boo = beyond(xp[s], yp[s], zp[s], pdate-bdate)
>     if boo:
> #      print('beyond TRUE')
>       break
268,270c299,304
<   if pdate.strftime('%Y%m%d') != ymd0:
<     nc0,dnt,dnlay,dnrow,dncol, ymd0 = openNC(pdate)
<     nc1=nc0
---
>   if pdate not in dtimes0[0]:
>     if nt[0]==24:
>       nc0,nt,dnlay,dnrow,dncol, dtimes0 = openNC(pdate)
>       if type(nc0)==int:break
>       nc1=nc0
>     if nt[0]<24:break
```

### 後處理部分

- 增加了經緯度座標的軌跡點，以配合geojson程式的應用
- 因為每日預報乃由crontab來執行程式，外掛執行檔都需要寫完整的路徑

```python
271a306,309
>   #geodetic LL
>   lon, lat = pnyc(np.array(o_xp)-Xcent,np.array(o_yp)-Ycent, inverse=True)
>   dfg=DataFrame({'lon':lon,'lat':lat})
>
273c311,315
<   name='trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
---
>   dr='f'
>   if BACK:dr='b'
>   name='trj_results/'+dr+'trj'+nam[0]+DATE+'.csv'
>   with open('trj_results/filename.txt','w') as f:
>     f.write(name.split('/')[1])
275a318,321
>   #geodetic LL
>   lon, lat = pnyc(np.array(l_xp)-Xcent, np.array(l_yp)-Ycent, inverse=True)
>   dfLg=DataFrame({'lon':lon,'lat':lat})
>
277a324
>     dfg.set_index('lon').to_csv(name.replace('.csv','_mark.csv'),header=None)
278a326
>     dfLg.set_index('lon').to_csv(name.replace('.csv','_line.csv'),header=None)
281a330
>     dfg.set_index('lon').to_csv(name.replace('.csv','_mark.csv'),mode='a',header=None)
282a332
>     dfLg.set_index('lon').to_csv(name.replace('.csv','_line.csv'),mode='a',header=None)
287,289c337,339
< if not BACK:dir='RL'
< os.system('csv2kml.py -f '+name+' -n '+dir+' -g TWD97')
< os.system('csv2bln.cs '+name)
---
> if not BACK:dir='NL'
> os.system('/opt/local/bin/csv2kml.py -f '+name+' -n '+dir+' -g TWD97')
> os.system('/opt/local/bin/csv2bln.cs '+name)
```

## 3/5天上限版本差異

- 為增加擴大模擬範圍，軌跡終點的時間差自3天延長至5天。
- 5天上限版本除了放寬日數的限制之外，也改用了風場的內插方式，以減少錯誤的可能，提高計算的效率。另為與WRF模式10天預報接軌，檔名中的時間標記採用變數定義，以配合新的系統設定。
- 5天上限版本應用在軌跡的逐日預報工作中([daily_traj.cs](daily_traj_cs.md))
- 提供WRF網格層數M=2/M=3的選項，前者為CWB_WRF數值產品，後者則為10天fcst_WRF預報結果

項目|[ftuv10.py][ftuv10]|[ftuv10_5d.py][ftuv10_5d]|說明
:-:|:-:|:-:|-
上限日數|3|5|擴大範圍。d1範圍可以達到中國東半壁
模式中心點|固定在[23.61000, 120.990]|由wrfout內設定|適應不同來源之模擬結果
wrfout來源|CWB_WRF|CWB_WRF(M=2) / fcst_WRF(M=3)|M值(網格層數) 須在程式內指定
wrfout檔名時間標籤|_06:00:00|任意起始時間|前者為配合CWB WRF之起始時間。
內插法|cubic spline|linear|前者雖然較為平緩, 但有可能發生錯誤、計算速度也較慢

## 程式細節說明

### 主程式

### 程式說明

這段程式碼用於軌跡模擬，根據提供的初始位置、日期和時間，模擬特定時間段內的物體軌跡。以下是程式的輸入、輸出和主要處理邏輯的說明：

#### 輸入

- `path`: 軌跡模擬過程中所需資料的路徑。
- `stnam`: 指定的站點名稱或經緯度，可以是單個站點或多個站點，如果是多個站點，以逗號分隔。
- `DATE`: 指定的日期和時間，格式為YYYYMMDDHH，例如2023010100表示2023年1月1日0時。
- `BACK`: 一個布林值，指示是否執行回溯模擬。
  
#### 輸出

- CSV 檔案：包含軌跡模擬結果的位置和時間資訊。
- KML 檔案：用於在 Google Earth 等地理信息軟體中顯示軌跡模擬結果。
- 文字檔案（`filename.txt`）：包含生成的 CSV 檔案的名稱。

#### 主要處理邏輯

1. 初始化模擬參數，包括模擬的時間段、初始位置等。
2. 根據提供的站點名稱或經緯度，計算初始位置的經緯度坐標。
3. 開始模擬過程，根據初始位置和時間，以一定的時間間隔進行模擬計算。
4. 在模擬過程中，根據模擬結果，更新物體的位置和時間。
5. 將模擬結果寫入 CSV 檔案和 KML 檔案中。

該程式利用數值模型資料（例如 WRF 模型）計算軌跡模擬，並將結果輸出為 CSV 和 KML 格式，以便進行後續分析和可視化。

### openNC函式

這個函式用於打開 NetCDF 檔案，並讀取其中的資料。以下是函式的輸入、輸出和主要處理邏輯的說明：

#### 輸入

- `sdate`: 指定的日期和時間，表示要打開的 NetCDF 檔案的日期和時間。

#### 輸出

- 如果成功打開了 NetCDF 檔案，則返回包含以下六個元素的列表：
  1. `ncf`: 打開的 NetCDF 檔案對象列表。依序是東亞、東南沿海、台灣地區等3個domain，以下列表均相同。
  2. `mt`: 模型域數量的列表。
  3. `mlay`: 垂直層數的列表。
  4. `mrow`: 行數的列表。
  5. `mcol`: 列數的列表。
  6. `dtimes`: 時間序列的列表，每個元素都是一個包含日期和時間的 datetime 對象。

#### 主要處理邏輯

1. 根據提供的日期和時間 `sdate`，確定要打開的 NetCDF 檔案的路徑和檔名。
2. 遍歷每個模型域，打開對應的 NetCDF 檔案，並將相關資訊讀取到變數中。
3. 如果指定的日期和時間 `sdate` 不在該檔案的時間序列中，則返回特殊值 `[-1]`。
4. 返回打開的 NetCDF 檔案對象列表以及相關資訊的列表。

這個函式的主要目的是準備打開 NetCDF 檔案並讀取資料，以供後續的軌跡模擬使用。

### get_uvw函式說明

這個函式用於從已打開的 NetCDF 檔案中獲取風速和風向資訊。以下是函式的輸入、輸出和主要處理邏輯的說明：

#### 輸入

- `ncft`: 一個包含 NetCDF 檔案對象和時間索引的元組，表示要從中獲取資訊的 NetCDF 檔案以及對應的時間索引。
- `t0`: 目標時間索引。
- `z`: 指定的高度。
- `y`: 經度。
- `x`: 緯度。

#### 輸出

- 如果成功獲取了風速和風向資訊，則返回一個元組 `(idx, f)`，其中：
  - `idx`: 包含時間、垂直層、行和列索引的元組。
  - `f`: 包含風速和風向的函式列表。

#### 主要處理邏輯

1. 根據指定的時間和位置，定位到對應的模型域。
2. 獲取目標點附近的風速和風向資訊，並將其存儲在 `uvwg` 中。
3. 根據模型域的不同，進行插值操作以填補缺失的風速和風向資訊。
4. 返回包含風速和風向的函式列表 `f`。

這個函式的主要目的是根據指定的時間和位置，從 NetCDF 檔案中獲取風速和風向資訊，以供軌跡模擬使用。

### 其他函式說明

這些函式用於不同的功能，包括位置定位、命令行參數解析、參數轉換和其他邏輯處理。以下是每個函式的說明：

#### `locate_nest(x, y)`

這個函式根據給定的位置坐標 `(x, y)` 定位到對應的模型域。它首先從最高層的模型域開始搜索，然後逐步向下搜索，直到找到包含給定位置的模型域。如果找不到對應的模型域，則返回 -1。

#### `getarg()`

這個函式從命令行參數中解析出時間段和站點名稱。它使用 `argparse` 模組解析命令行參數，並返回包含站點名稱、日期和後向軌跡的布爾值的列表。

#### `str2bool(v)`

這個函式用於將字串轉換為布爾值。它接受一個字串作為輸入，並返回對應的布爾值。支持的布爾值包括 `'yes', 'true', 't', 'y', '1'` 和 `'no', 'false', 'f', 'n', '0'`。

#### `nstnam()`

這個函式從 JSON 文件中讀取站點名稱和對應的編號。它打開一個 JSON 文件，讀取其中的內容，並返回兩個字典，分別包含站點名稱到編號和編號到站點名稱的映射。

#### `beyond(xpp, ypp, zpp, ddt)`

這個函式用於判斷給定的位置和時間是否在指定的模型域範圍之外。如果位置超出範圍或時間超出範圍（超過5天），則返回 True；否則返回 False。

## 程式下載

{% include download.html content="[地面uv10二維軌跡分析程式ftuv10.py][ftuv10]" %}
{% include download.html content="[地面uv10軌跡分析(上限五天版本)ftuv10_5d.py][ftuv10_5d]" %}
{% include download.html content="[地面uv10軌跡分析(上限十天版本)ftuv10_10d.py][ftuv10_10d]" %}

[ftuv10]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/ftuv10/ftuv10.py> "地面uv10二維軌跡分析程式ftuv10.py"
[ftuv10_5d]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/ftuv10/ftuv10.py> "地面uv10二維軌跡分析程式(上限五天版本)ftuv10_5d.py"
[ftuv10_10d]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/ftuv10/ftuv10_10d.py> "地面uv10二維軌跡分析程式(上限十天版本)ftuv10_10d.py"
[bt2_DVP]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/bt2_DVP/> "三維反軌跡線之計算"
[traj2kml.py]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/5.traj/#軌跡程式說明> "traj2kml.py"
[daily_traj_cs]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/ftuv10/daily_traj_cs/> "daily_traj.cs程式說明"
