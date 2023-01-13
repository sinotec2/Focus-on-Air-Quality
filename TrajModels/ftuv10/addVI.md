---
layout: default
title: addVI.py
nav_order: 2
parent: 地面二維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-04 14:43:02
tags: trajectory
---

# addVI.py程式說明
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

- 2021/6 在做完反軌跡的CGI程式之後，思考應該可以再增加軌跡線上的屬性，找到了[可以控制標籤大小的js程式]()，如此便可以在軌跡線滯留的情況，可以有另外的資訊判斷會不會出現嚴重空氣污染。
- 判斷是否會發生空氣污染的氣象要素，教科書上曾經提到「[通風指數][VI]」，嘗試了由CWBWRF數據計算混合層高度，但因其垂直解析度太低而作罷，最後選擇以行星邊界層作為高度的指標，至少可以清楚呈現內陸與海上的差異。
- 這支程式很單純，就是對每一個軌跡線上的時間、空間點，從wrfout檔案中找到行星邊界層與地面風速值，計算該處的[通風指數][VI]，精確說是先以矩陣統一計算，再內插指定時間位置之數值。
- 最後結果轉換成geojson格式，以利leaflet套件之讀取。

## 程式設計

### 確定反軌跡時間及檔案目錄

- 程式引數：反軌跡線csv檔案名稱
  - 如果檔案名稱中有日期，則
    1. 將其讀成`bdate`
    1. 如果檔名中有`ftrj`，則將BF值設成1(否則內設為-1)
  - 檔名中沒有日期，如在[daily_trj.cs](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/ftuv10/daily_traj_cs/)中為`today_marks.csv`
    - 設計成每日預報的情況，由`pwd`及`datetime`指令中得到時間的資訊

```python
fname=sys.argv[1]
idx=fname.index('.csv')-10
ymdh=fname[idx:idx+10]
BF=-1
try:
  bdate=datetime.datetime.strptime(ymdh,'%Y%m%d%H')
  if 'ftrj' in fname:BF=1
except:
  pwd=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[-1]
  if pwd in ['00','p1','p2','m1','m2']:
    pm=1
    if pwd[0]=='m':pm=-1
    del_pm=int(pwd[1])
    ymdh=(datetime.datetime.now()+datetime.timedelta(days=pm*del_pm)).strftime('%Y%m%d')+'12'
    bdate=datetime.datetime.strptime(ymdh,'%Y%m%d%H')
  else:
    sys.exit('wrong excution location')
```

### 確定csv檔案各欄位的內容

```python
df=read_csv(fname)
#if 'VI' in df.columns:sys.exit('VI already in file: '+fname)
col0=list(df.columns)
col=[i[:3].lower() for i in df.columns if len(i)>=3]
#in case of TWD97
if 'lat' not in col or min(df[df.columns[0]])>360.:
  x,y=np.array(df[df.columns[0]])-Xcent,np.array(df[df.columns[1]])-Ycent
  lon,lat= pnyc(  x,  y, inverse=True)
else:
  lon,lat=np.array(df[df.columns[0]]),np.array(df[df.columns[1]])
  x, y = pnyc(lon,lat, inverse=False)
#UTC time
if 'Title' in col0:
  ttl=np.array(df.Title)
  idx=np.where(ttl==0)[0]
  ntrj=len(idx)
  ends=[idx[i+1] for i in range(ntrj-1)]+[len(df)]
  lngs=[ends[i]-idx[i] for i in range(ntrj)]
  dd=[]
  dates=[bdate+datetime.timedelta(hours=t*BF-8) for t in range(max(lngs))]
  for n in range(ntrj):
    dd+=[dates[i] for i in range(lngs[n])]
  df['date']=dd
  nTail=ends[0]-1
else:
  dates=[bdate+datetime.timedelta(hours=t*BF-8) for t in range(len(df))]
  df['date']=dates
  nTail=len(df)
```

### 讀取wrfout檔案中的內容

```python
fdate=dates[0].strftime('%Y-%m-%d')
if bh_wrf>0 and dates[0].hour<bh_wrf:
  fdate=(dates[0]+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
fn=path+head+fdate+tail
nc = netCDF4.Dataset(fn,'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
if 'PBLH' not in V[2]:sys.exit('PBLH not found in nc file: '+fn)
for s in V[2]:
  exec(s+'=nc.variables["'+s+'"][:]')
WS=np.sqrt(U10*U10+V10*V10)
PBLH[np.where(np.isnan(PBLH))[:]]=35.
PBLH[np.where(PBLH<35.)[:]]=35.
VI=WS*PBLH
nt,nrow,ncol=VI.shape
strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
long,latg=XLONG[0,:,:].flatten(),XLAT[0,:,:].flatten()
```

### 通風指數之內插

- 使用griddata模組
- DataFrame.date格式是datetime，與wrfout的Times（經轉換）相同，可用以確認順位。

```python
Xg, Yg = pnyc(long,latg, inverse=False)
Xg, Yg = Xg.reshape(nrow,ncol), Yg.reshape(nrow,ncol)
mnx,mxx=np.min(x)-nc.DX,np.max(x)+nc.DX
mny,mxy=np.min(y)-nc.DY,np.max(y)+nc.DY
idxx=np.where((mnx<Xg)&(Xg<mxx))
idxy=np.where((mny<Yg[idxx[:]])&(Yg[idxx]<mxy))
ny=len(idxy[0])
xyc= [(Xg[idxx[0][idxy[0][i]],idxx[1][idxy[0][i]]],Yg[idxx[0][idxy[0][i]],idxx[1][idxy[0][i]]]) for i in range(ny)]
ventI=[]
for dd in range(len(df)):
  now=df.date[dd]
  t=Times.index(now)
  var=VI[:]
  c = np.array([var[t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
  x1,y1=x[dd],y[dd]
  v=griddata(xyc, c, (x1, y1), method='linear')
  if np.isnan(v):
    var=WS[:]
    c = np.array([var[t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
    w=griddata(xyc, c, (x1, y1), method='linear')
    var=PBLH[:]
    c = np.array([var[t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
    p=griddata(xyc, c, (x1, y1), method='linear')
    print(now,w,p)
  ventI.append(griddata(xyc, c, (x1, y1), method='linear'))
  fdate=(now+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
```

### 跨日wrfout檔案之讀取

```python
  if dd==len(df)-1:continue #no need to openfile any more
  if bh_wrf==now.hour or now==dates[nTail]:
    if now==dates[nTail]:
      fdate=dates[0].strftime('%Y-%m-%d')
      if bh_wrf>0 and dates[0].hour<bh_wrf:
        fdate=(dates[0]+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    fn=path+head+fdate+tail
    nc = netCDF4.Dataset(fn,'r')
    for s in V[2]:
      if s in nc.variables:
        exec(s+'=nc.variables["'+s+'"][:]')
    WS=np.sqrt(U10*U10+V10*V10)
    PBLH[np.where(np.isnan(PBLH))[:]]=35.
    PBLH[np.where(PBLH<35.)[:]]=35.
    VI=WS*PBLH
    strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
    Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
```

### 輸出及檔案轉換

- 將通風指數寫在原檔案的最後一欄位
- 直接在程式內執行`csv_to_geojson`
- 將時間轉成LST

```python
df['VI']=ventI
df['lng']=lon
df['lat']=lat
df.VI=[round(i.item(),1) for i in df.VI]
df.date=[d+datetime.timedelta(hours=+8) for d in df.date]
col2=['lng','lat']+col0[2:]+['VI','date']
fnameO=fname.replace('.csv','V.csv')
df[col2].set_index('lng').to_csv(fnameO)
os.system('/opt/anaconda3/bin/csv_to_geojson '+fnameO)
```

## 程式下載

- {% include download.html content="軌跡線上通風指數之計算[addVi.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/ftuv10/addVI.py)" %}

[VI]: <https://www2.gov.bc.ca/gov/content/environment/air-land-water/air/air-pollution/smoke-burning/ventilation-index#:~:text=The%20Ventilation%20Index%20is%20a,will%20mix%20into%20the%20air.> "通風指數(Ventilation Index, VI)：系指一個地區的平均風速、與其混合層高度之乘積。"