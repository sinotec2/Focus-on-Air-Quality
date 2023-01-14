---
layout: default
title:  earth套件展示wrfout與CCTM_ACONC結果
parent: earth
grand_parent: Graphics
last_modified_date: 2022-09-02 14:33:16
tags: CMAQ earth combine crontab graphics
---

# earth套件展示wrfout與CCTM_ACONC結果
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
- [earth][eth]應用來展示gfs預報、CWBWRF預報、[CAMS][CAMS_desc]預報等等結果數據，有其便捷性、高品質、跨平台等等強項。
- 此處之[cmaq_json.py][cmaq_json.py]乃應用來讀取並展示自行模擬WRF與CMAQ的結果。

## 執行方式

### crontab
- 每天8時執行

```bash
10 8 * * * for r in 45 09 03;do cd /nas1/Data/javascripts/D3js/earthFcst$r/public/data/weather/current;./cmaq_json.py;done
```
### [預報流程](https://sinotec2.github.io/FAQ/2022/08/30/fcst.cs.html)之最末作業

```bash
$ tail fcst.cs
...
# prepare earth json files and backup to imackuang
for r in 45 09 03;do cd /nas1/Data/javascripts/D3js/earthFcst$r/public/data/weather/current;./cmaq_json2.py;done
if ! [ -e /home/kuang/mac/do_not_delete ];then /usr/bin/fusermount -u /home/kuang/mac;/usr/bin/sshfs kuang@IMacKuang:/Users ~/mac -o nonempty -o password_stdin < ...;fi
/usr/bin/rsync -r /nas1/Data/javascripts/D3js/earthFcst45/public/data/weather/20?? ~/mac/Data/javascripts/D3js/earthFcst45/public/data/weather/20??
(py37)
```

## IO說明
### 引數
- [cmaq_json.py][cmaq_json.py]會讀取pwd環境變數從中讀取解析度(res in 03 09 45)，因此必須在正確的current目錄下執行。

### 輸入檔及目錄
- wrfout
  - 目錄：$ROOT/$GRID_NAME
  - 日期：當日起算5天
- CCTM_ACONC
  - 目錄：$FCST/grid$res/cctm.fcst/daily
  - 日期：當日起算5天    

### 輸出檔案及目錄
- 臭氧模擬結果：$weather/YYYY/MM/DD/HH00-ozone-surface-level-fcst-$res.json
  - 單位為ppb
- 風場模擬結果：$weather/YYYY/MM/DD/HH00-wind-surface-level-fcst-$res.json
  - U10, V10單位為m/s

## 程式設計
### 網格系統的轉換(griddata版本[cmaq_json.py][cmaq_json.py])
- [earth][eth]內設是等間距經緯度系統，(但該等json檔案似乎也可以接受直角座標系統)，此處需將WRF及CMAQ的直角座標系統進行轉換。
  1. 由於數據(目前)只有地面層、項目也只有U10、V10、及ozone等3項，就使用griddata進行內插。
  2. 由於griddata在邊界上會出現NaN結果，因此內縮一圈，並將NaN結果設為0。
  3. 內插方式還可精進(詳下：[搜尋半徑版本](./cmaq_json.html#搜尋半徑版本cmaq_json2py)。
- 時間迴圈之外座標轉換相關的設定

```python
#read lat,lon
fname='/nas2/cmaqruns/2022fcst/grid'+grds+'/mcip/GRIDCRO2D.nc'
nc = netCDF4.Dataset(fname, 'r')
x=nc.variables['LON'][0,0,:,:]
y=nc.variables['LAT'][0,0,:,:]
nrow,ncol=x.shape
lat_min=y[1,ncol//2]
lat_max=np.min([y[-2,-2],y[-2,1]])
jmx=bisect(y[:,ncol//2],lat_max)
dy=(y[jmx,ncol//2]-lat_min)/jmx
dx=dy
lon_min=np.max(x[:,1])
idx=np.where(x[:,-2]>0)
lon_max=np.min(x[idx[0],-2])
nx=int((lon_max-lon_min)//dx)
ny=int((lat_max-lat_min)//dy)
#new grid system(x1,y1) in equal dlat and dlon
lon1d=[lon_min+dx*i for i in range(nx)]
lat1d=[lat_min+dy*i for i in range(ny)]
x1, y1 = np.meshgrid(lon1d, lat1d)
idx=np.where((x>0)&(x>=lon_min)&(x<=lon_max)&(y>=lat_min)&(y<=lat_max))
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]])]
```
- 時間迴圈下之內插應用
  - ozone因直接讀取自CCTM_ACONC，單位為ppm，需進行單位轉換以符合固定色階的設定。
  - 注意json檔案的矩陣方向在南北向是由北向南，需進行翻轉(np.flip)。

```python
...
      exec('var='+uv[ir]+'[t,:,:]')
      c = np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
      zz = griddata(xyc, c[:], (x1, y1), method='cubic')
      gfs[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())
...
      var=o3[t,:,:]*1000
      c = np.array([var[idx[0][i], idx[1][i]] for i in range(mp)])
      zz = griddata(xyc, c[:], (x1, y1), method='cubic')
      ozn[ir]['data']=list(np.flip(np.where(zz!=zz,0,zz),axis=0).flatten())
```

### 搜尋半徑版本[cmaq_json2.py][cmaq_json2.py]
- 雖然griddata在本次專案的執行效率尚可接受，然而仍有改善空間
  1. 在邊界上內插出現NaN，導致填充0值，出現濃度或風速的驟變，圖面非常突兀。
  1. griddata也是按照直角座標進行內插，使用經緯度數字並不正確，在數據梯度較大之處(鋒面、雲雨現象)，會出現太過平滑的結果。
- 作法參考[搜尋半徑距離平方反比加權之內插機制][near_wgt]，此處仍以5倍網格距離作為搜尋半徑。
- 程式下載[github][cmaq_json2.py]

### 時間標籤的傳遞
- wrfout及CCTM_ACONC檔案有個自的時間標籤，需轉換成json檔案header部分的`refTime`及`forecastTime`。
  - 在[earth][eth]套件中的時間是這2者之和(./public/libs/earth/1.0.0/[products.js][js1])：

```java  
 function buildGrid(builder) {
...  
    var date = new Date(header.refTime);
        date.setHours(date.getHours() + header.forecastTime);
```

- 時間標籤設計成以`refTime`為主，取消`forecastTime`，以因應不同模擬批次結果的混合狀況。
- 區分為時間變化及共同部分
- 共同部分(forecastTime)：

```python
nr={'o':nozn,'g':ngfs}
jsn={'o':ozn,'g':gfs}
for k in ['o','g']:
  for i in range(nr[k]):
...
    jsn[k][i]['header']["forecastTime"]=0
```

- wrfout的時間標籤：Times

```python
  nt=nc.dimensions['Time'].size
  strT=[''.join([i.decode('utf-8') for i in nc['Times'][t,:]]) for t in range(nt)]
  for t in range(0,nt,3):
    bdate=datetime.datetime.strptime(strT[t],'%Y-%m-%d_%H:00:00')
    dt=bdate.strftime("%Y-%m-%dT%H:%M:%SZ")
    dir=bdate.strftime("../%Y/%m/%d/")
    os.system('mkdir -p '+pwd+dir)
    hh=bdate.strftime("%H00")
    for i in range(ngfs):
      gfs[i]['header']['refTime']=dt
...
    fnameO=pwd+dir+hh+'-wind-surface-level-fcst-'+grds+'.json'
```

- CCTM_ACONC的時間標籤：TFLAG，使用[dtconvertor.py][dtconvertor]來轉換

```python
from dtconvertor import dt2jul, jul2dt
...
    bdate=jul2dt(nc['TFLAG'][t,0,:])
    dt=bdate.strftime("%Y-%m-%dT%H:%M:%SZ")
    dir=bdate.strftime("../%Y/%m/%d/")
    os.system('mkdir -p '+pwd+dir)
    hh=bdate.strftime("%H00")
    for i in range(nozn):
      ozn[i]['header']['refTime']=dt
    fnameO=pwd+dir+hh+'-ozone-surface-level-fcst-'+grds+'.json'
```

## 其他[earth][eth]套件需配合修正事項
### json檔案的開啟
- 在./public/libs/earth/1.0.0/[products.js][js1]中原本開啟檔案的副程式gfs1p0degPath，需進行修改來開啟前述fcst-??檔案
  - 抄寫成FilePath，以開啟任意來源(src)及解析度(res)的json檔案
  - 取消原來gfs1p0degPath之呼叫
  - 指定讀取fcst(來源)及45(解析度)之檔案

```java
//kuang@node03 /nas1/Data/javascripts/D3js
//$ diff earth/public/libs/earth/1.0.0/products.js earthFcst45/public/libs/earth/1.0.0/products.js
48a49,53
>     function FilePath(attr, type, surface, level, src, res) {
>         var dir = attr.date, stamp = dir === "current" ? "current" : attr.hour;
>         var file = [stamp, type, surface, level, src, res].filter(µ.isValue).join("-") + ".json";
>         return [WEATHER_PATH, dir, file].join("/");
>     }
122c127,128
<                     paths: [gfs1p0degPath(attr, "wind", attr.surface, attr.level)],
---
>                     //paths: [gfs1p0degPath(attr, "wind", attr.surface, attr.level)],
>                       paths: [FilePath(attr, "wind", attr.surface, attr.level, "fcst", "45")],
409c415
<                         name: {en: "GEMS Ozone", ja: "臭氧"},
---
>                         name: {en: "CMAQ Ozone", ja: "臭氧"},
412c418
<                     paths: [gfs1p0degPath(attr, "ozone", attr.surface, attr.level)],
---
>                   paths: [FilePath(attr, "ozone", attr.surface, attr.level, "fcst", "45")],
```

### 內設直接開啟ozone圖層與放大倍率
- DEFAULT的設定寫在./public/libs/earth/1.0.0/micro.js內

```java
kuang@node03 /nas1/Data/javascripts/D3js/earthFcst45
$ grep -n DEFA public/libs/earth/1.0.0/micro.js
14:    var DEFAULT_CONFIG = "current/wind/surface/level/overlay=ozone/orthographic=-241.67,21.03,1385";
```



[eth]: <https://github.com/cambecc/earth> "cambecc(2016), earth building, launching and etc on GitHub. "
[cmaq_json.py]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/earth/cmaq_json.py> "解讀wrfout與CCTM_ACONC檔案轉換成json檔案之程式cmaq_json.py"
[dtconvertor]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/DateTime/dtconvertor/> "Datetime轉Julian day、Julian day轉Datetime"
[near_wgt]: <https://sinotec2.github.io/FAQ/2022/08/20/NearstWeight.html> "這個內插機制主要針對2維griddata速度太慢所因應的修改方案。同時也需要規避griddata結果會有NaN內插錯誤的結果。主要因為空氣品質或排放量的內插會與距離的遠近有關，太遠的數據對內插影響也較低，還是適用距離相關的內插機制較為合理。同時摒除遙遠的數據對提升計算速度有非常重要的貢獻。"
[cmaq_json2.py]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/earth/cmaq_json2.py> "搜尋半徑版本cmaq_json2.py"
[js1]: <https://github.com/cambecc/earth/blob/master/public/libs/earth/1.0.0/products.js> "cambecc/earth/public/libs/earth/1.0.0/products.js"
[CAMS_desc]: <https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview> "CAMS每天2次進行全球大氣成分的5天預報，包括50多種氣狀物和7種顆粒物(沙漠塵埃、海鹽、有機物、黑碳、硫酸鹽、硝酸鹽和銨氣溶膠)。初始條件為衛星及地面觀測數據同化分析結果，允許在地面觀測數據覆蓋率低、或無法直接觀測到的大氣污染物進行估計，除此之外，它還使用到基於調查清單或觀測反衍的排放估計，以作為表面的邊界條件。"