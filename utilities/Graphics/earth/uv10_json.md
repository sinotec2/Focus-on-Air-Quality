---
layout: default
title:  地面風wrfout檔轉json
parent: earth
grand_parent: Graphics
last_modified_date: 2022-07-28 23:09:00
tags: CWBWRF earth graphics
---

# 地面風wrfout檔轉json
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
- 雖然[nc2json][nc2json]已經有網友貢獻了，此處除了檔案轉換之外，還需要轉換座標系統，將CWB wrf預報檔中原本的藍伯特投影等間距網格、轉換成等經緯度網格。
- 目的是應用cambecc的[earth][ens]套件。
  - 該套件內設讀取的是gfs預報結果檔，解析度為1度。
  - gfs與CWB檔案的差異比較詳見[earth套件讀取CWB_WRF數據][diff_tab]。
  - 由於差異太多，不易在js內修改，在系統外直接以gfs的json模版來填入CWB內容，會較為容易。
- CWB wrf預報檔之下載、解析、轉換詳見[FAQ：中央氣象局WRF_3Km數值預報產品][wrf_3km]。
- 雖然可以應用leaflet等js模組進行座標轉換，但因為CWB_WRF已經有WPS-geogrid結果，內中有XLAT與XLONG等2項經緯度變數（詳見[cwb WRF_3Km->相同網格系統之grb2轉檔][fil_grb_nc]），不需要另外進行座標轉換的計算，直接內插即可。
- 此處只是為了展示用，座標轉換前後並不必然保持各項物理量質量或動量的守恒。

## 程式IO
### input
- 引數：欲處理的wrfout檔名
  - 結果會按照檔名中的d01或d03設定解析度標籤(15K or 3K)
- json 模版
  - current-wind-surface-level-gfs-1.0.json
  - 自cambecc的github取得:`wget https://raw.githubusercontent.com/cambecc/earth/master/public/data/weather/current/current-wind-surface-level-gfs-1.0.json`

### output
- 解析度標籤不同
  - d01:`'current-wind-surface-level-cwb-15K.json'`
  - d03:`'current-wind-surface-level-cwb-3K.json'`
- 位置：結果檔必須放在`/Users/Data/javascripts/D3js/` `./earth/public/data/weather/current`目錄下

## 程式分段說明
### 經緯度範圍
- 因為藍伯特投影直角座標系統（LCC）的4角點數不足以內插，將會出現很多NaN的結果，因此必須將其去除。
- 考量到解析度的不均勻，LCC的中心解析度較高，周圍較差。
- 經度的範圍
  - 東西邊界上的最南點
  - 規避負值的經度（換日線東方）
- 緯度的範圍
  - 東西邊界上的最北點，取較低值。其確切值以bisect在中心線中決定(`lat_max` and `jm`)
  - 中心線的最南點(`lat_min`)

```python
x=nc.variables['XLONG'][0,:,:]
y=nc.variables['XLAT'][0,:,:]
lat_min=y[0,ncol//2]
lat_max=np.min([y[-1,-1],y[-1,0]])
jmx=bisect(y[:,ncol//2],lat_max)
lat_max=y[jmx,ncol//2]
dy=(lat_max-lat_min)/jmx
dx=dy

lon_min=np.max(x[:,0])
idx=np.where(x[:,-1]>0)
lon_max=np.min(x[idx[0],-1])
nx=int((lon_max-lon_min)//dx)
ny=int((lat_max-lat_min)//dy)
```

### 產生新的經緯度網格系統
- `idx`是新網格範圍內的點。經過篩選大致上可以留下7.5～8成。

```python
#new grid system(x1,y1) in equal dlat and dlon
lon1d=[lon_min+dx*i for i in range(nx)]
lat1d=[lat_min+dy*i for i in range(ny)]
x1, y1 = np.meshgrid(lon1d, lat1d)
idx=np.where((x>0)&(x>=lon_min)&(x<=lon_max)&(y>=lat_min)&(y<=lat_max))
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]
```

### 填入json模版
- 先將網格座標系統相關設定填入gfs
- json的實數必須是64位元

```python
for i in range(nr):
  gfs[i]['header']['nx']=nx
  gfs[i]['header']['ny']=ny
  gfs[i]['header']['numberPoints']=nx*ny
  for v in ['dx','dy']:
    gfs[i]['header'][v]=np.float64(dx)
  gfs[i]['header']['lo1']=np.float64(lon_min)
  gfs[i]['header']['lo2']=np.float64(lon_max)
  gfs[i]['header']['la2']=np.float64(lat_min)
  gfs[i]['header']['la1']=np.float64(lat_max)
  gfs[i]['data']=[0 for v in range(nx*ny)]
```

### 2維線性內插
- 使用`np.where`將周邊少數NaN值設為0
- GFS定義y軸是自北向南，與wrf相反。在壓平（`np.flatten()`）前必須先將y軸反轉（`np.flip(...)`）。

```python
uv=['U10', 'V10']
for ir in range(nr):
  var=nc.variables[uv[ir]][0,:,:]
  c = np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
  zz = griddata(xyc, c[:], (x1, y1), method='linear')
  gfs[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())
```

### 寫出檔案

```python
if 'd01' in fname:fnameO='current-wind-surface-level-cwb-15K.json'
if 'd03' in fname:fnameO='current-wind-surface-level-cwb-3K.json'
with open(fnameO,'w') as f:
  json.dump(gfs,f)
```

## 程式下載

{% include download.html content="地面風wrfout檔轉json：[uv10_json.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/wind_models/cwbWRF_3Km/uv10_json.py)" %}

## grib2 to json directly
### 目的
- 這個版本直接由grib2檔案讀取地面風進行內插。grib2轉成wrfout是個艱辛的歷程，d01、d04還可接受，d03執行時間和檔案容量都大到無法作業化。  
  - 直接使用gribby模組來開啟、讀取地面風。
  - 檔名：採CWB模式結果M-A0064-006.grb2(~84)。每6小時下載，006的模式時間約與目前時間一致。
  - XLAT，XLONG改由uv10_temp.nc模版讀取
- 內插結果再轉成json檔繪圖

### 與前述程式的差異

```python
7a8
> import pygrib
14c15
< fname=sys.argv[1]
---
> fname='uv10_temp.nc'
19a21,22
> nc.close()
>
49a53,54
>   gfs[i]['header']['center']=0
>   gfs[i]['header']['centerName']="交通部中央氣象局區域預報模式(WRF)"
53a59,79
> atbs={'U10': '10 metre U wind component',
>       'V10': '10 metre V wind component'}
> for a in atbs:
>   exec('s'+a+'=np.zeros(shape=(nrow,ncol),dtype=np.float64)')
>
> fname=sys.argv[1]
> grbs = pygrib.open(fname)
> for a in set(atbs):
>   grb = grbs.select(name=atbs[a])
>   cmd=a+'=grb[0].values'
>   exec(cmd)
> dt=grbs[1].validDate.strftime("%Y-%m-%dT%H:%M:%SZ")
> dir=grbs[1].validDate.strftime("../%Y/%m/%d/")
> pwd='/nas1/Data/javascripts/D3js/earth/public/data/weather/current/'
> os.system('mkdir -p '+pwd+dir)
> mac=pwd.replace('nas1','home/kuang/mac')
> os.system('mkdir -p '+mac+dir)
> hh=grbs[1].validDate.strftime("%H00")
>
> for i in range(nr):
>   gfs[i]['header']['refTime']=dt
55c81
<   var=nc.variables[uv[ir]][0,:,:]
---
>   exec('var='+uv[ir]+'[:,:]')
57c83
<   zz = griddata(xyc, c[:], (x1, y1), method='linear')
---
>   zz = griddata(xyc, c[:], (x1, y1), method='cubic')
60,61c86,87
< if 'd01' in fname:fnameO='current-wind-surface-level-cwb-15K.json'
< if 'd03' in fname:fnameO='current-wind-surface-level-cwb-3K.json'
---
> if '61' in fname:fnameO=pwd+dir+hh+'-wind-surface-level-cwb-15K.json'
> if '64' in fname:fnameO=pwd+dir+hh+'-wind-surface-level-cwb-3K.json'
63a90,96
> os.system('cp '+fnameO+' '+fnameO.replace('nas1','home/kuang/mac'))
> if '006.grb2' in fname and '64' in fname:
>   fnameO=pwd+'current-wind-surface-level-cwb-3K.json'
>   with open(fnameO,'w') as f:
>     json.dump(gfs,f)
> #  os.system('cp '+fnameO+' '+fnameO.replace('nas1','home/kuang/mac'))
>
```



[nc2json]: <https://github.com/pwcazenave/netcdf2json/blob/master/netcdf2json.py> "pwcazenave(2017), Convert netCDF output to JSON for use in earth, netcdf2json"
[diff_tab]: <https://sinotec2.github.io/FAQ/2022/07/26/CWBwrf_3Km2NWC.html> "earth套件讀取CWB_WRF數據-> diff of first paramter in gfs and cwbwrf_15Km files"
[ens]: <https://earth.nullschool.net/> "earth, a visualization of global weather conditions, forecast by supercomputers, updated every three hours"
[wrf_3km]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/> "中央氣象局WRF_3Km數值預報產品"
[fil_grb_nc]: <https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/4.fil_grb_nc/> "cwb WRF_3Km->相同網格系統之grb2轉檔"
