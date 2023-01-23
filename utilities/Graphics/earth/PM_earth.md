---
layout: default
title:  CMAQ粒狀物等模擬結果之earth呈現
parent: earth
grand_parent: Graphics
date:  2022-09-14
last_modified_date: 22022-09-14 14:04:00
tags: CMAQ earth graphics
---

# CMAQ粒狀物等模擬結果之earth呈現
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
- CMAQ之粒狀物是由個別粒徑比例、個別粒狀物成份濃度、搭配各網格的氣象條件所組合而成的，VOCs則是由各個成份與碳數之乘積和，詳見[combine.sh][combine]說明。
- 為簡化數據端的作業、減少暫存檔案，預報作業系統中是否重寫後處理程式的考量：
  - 複雜度：[combine.sh][combine]確實較為複雜，但若要重寫python檔，也不是很容易的一件事。
  - 平行化：[combine.sh][combine]可以使用mpirun來平行化，會有較高的執行效率，python並不會強制平行化。
  - 結果檔案：[combine.sh][combine]會需要再執行[shks.cs][shks](其核心為ncks)來讀取粒狀物項目，如果使用python則不再需要。
  - [earth][eth]套件json檔之轉接：如果是以python處理會較為直接、有效。
- 就展示端而言，[earth][eth]套件是等經緯度系統，與CMAQ直角正交系統有別，因此需要進行空間的內插，內插機制詳見[搜尋半徑距離平方反比加權之內插機制](https://sinotec2.github.io/FAQ/2022/08/20/NearstWeight.html)。各版本的內插與作業項目：
  1. [cmaq_json.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/earth/cmaq_json.py)使用griddata模組
  1. [cmaq_json2.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/earth/cmaq_json2.py)使用距離平方反比加權，同時新增臭氧8小時值的計算
  1. [cmaq_json3.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/earth/cmaq_json3.py)新增PM及SNV的轉檔(說明如下)
- 轉換歷史結果檔會需要過去的METCRO2D、METCRO3D，預報系統並沒有留存這些檔案。
  1. 由於氣象檔主要提供空氣密度、及溫度，主要差異發生在不同高度及緯度，
  1. 此處暫以最近5天模擬值來替代之(局部天氣現象地區的濃度可能會有些差異，估計差異會小於洗滌現象造成的差異)。
  1. 即便如此，也會需要進行檔案修改(說明如下)。

## 數據端
### [fcst.cs](https://sinotec2.github.io/FAQ/2022/08/30/fcst.cs.html)中之安插
- 執行CMAQ後，在處理下一層邊界/初始條件之前，安插進行[combine.sh][combine]
- 原本第3層是不處理下層的IC/BC的，因此需調整優先進行[combine.sh][combine]

```bash
...
#CMAQ stream
cd $fcst
...
for i in 0 1 2;do
...
  for id in {0..4};do
    nc=$fcst/grid$ii/cctm.fcst/daily/CCTM_ACONC_v532_intel_${DOM[$i]}_${dates[$id]}.nc
    # combine PM's
    $fcst/combine.sh $nc
    # generate bcon for next nest
    test $i -eq 2 && continue
    csh $fcst/run_bcon_NC.csh $nc >&/dev/null
  done
...
```

### 逐日處理[combine.sh][combine]
- 由於CMAQ是逐日儲存結果的，過去在[combine.sh][combine]的內容會進行日期的迴圈。
- 此處預報的架構也是逐日的，無需另外進行迴圈與整併。

### [combine.sh][combine]腳本的內容

```bash
kuang@dev2 /nas2/cmaqruns/2022fcst
$ cat combine.sh
#!/bin/bash
#gcc
nc=$1
ii=$(echo $nc|cut -c29-30)
ymd=$(echo $nc|cut -d'_' -f7|cut -d'.' -f1)
export LD_LIBRARY_PATH=/home/cmaqruns/2016base/lib/x86_64/gcc/netcdf/lib:/opt/netcdf/netcdf4_gcc/lib:/opt/openmpi/openmpi4_gcc/lib
export PATH=/opt/openmpi/openmpi4_gcc/bin:/usr/bin:$PATH
export BASE=/nas2/cmaqruns/2022fcst
export EXEC=/nas1/cmaqruns/CMAQ_Project/POST/combine/scripts/BLD_combine_v53_gcc/combine_v53.exe
export m3input=${BASE}/grid$ii
export cctmout=${BASE}/grid$ii/cctm.fcst/daily

# user define
#> File [1]: CMAQ conc/aconc file
#> File [2]: MCIP METCRO3D file
#> File [3]: CMAQ APMDIAG file
#> File [4]: MCIP METCRO2D file
export INFILE2="${m3input}/mcip/METCRO3D.nc"
export INFILE4="${m3input}/mcip/METCRO2D.nc"

# programs
export LC_ALL=C
export LANG=C
export GENSPEC=N
export SPECIES_DEF=${BASE}/SpecDef_cb6r3_ae7_aq.txt
export INFILE1=$nc
export INFILE3=${nc/ACONC/APMDIAG}
export OUTFILE=${cctmout}/out.conc.nc
if [ -e ${OUTFILE} ]; then rm ${OUTFILE};fi

time mpirun -np 10 ${EXEC} >& ${BASE}/cmb.out
if [ -e ${cctmout}/PMs$ymd.nc ];then rm ${cctmout}/PMs$ymd.nc;fi
${BASE}/shk.cs $OUTFILE ${cctmout}/PMs$ymd.nc
```
- 引數：CCTM_ACONC檔案名稱(含目錄)，將提供解析度(`$ii`)、年月日(`$ymd`)等資訊。粒徑資訊檔名(CCTM_APMDIAG)也是由引數修改而來。
- METCRO2D、METCRO3D，如非即期mcip處理結果，需先執行[metcro.py](https://sinotec2.github.io/FAQ/2022/09/14/PM_earth.html#metcro檔案之準備)。
- 使用10個核心進行平行運算

### [shk.cs][shks]之修改
- 因為其他SNO等項目可以由CCTM_ACONC檔案直接讀取，不必重複儲存，因此只由combine結果中抽出PM及VOC另存。
- 在IOAPI_nc檔案中，變數個數(NVARS)也是一個維度(VAR，僅發生在時間標籤TFLAG一項)，因此也需要做`ncks -d`，以避免檔案儲存奇異值。

```bash
#kuang@DEVP /nas2/cmaqruns/2022fcst
#$ diff ~/bin/shk.cs shk.cs
17c17
<     VAR='TFLAG,CO,NO2,SO2,O3,PM25_NO3,PM25_SO4,PM25_TOT,PM10,VOC,PM25_NH4'
---
>     VAR='TFLAG,PM1_TOT,PM25_TOT,PM10,VOC'
28c28
<   $NCKS -O -v $VAR -d LAY,0 $1 $2
---
>   $NCKS -O -v $VAR -d VAR,0,3 -d LAY,0 $1 $2
```
### METCRO檔案之準備
- 由於在預報系統中mcip結果並不會特別儲存，在需要過去日期mcip結果時，即使內容相同，還會需要進行時間標籤的變更。
- 輸入引數為YYYY-MM-DD格式之初始日期，時間為0時(UTC)
- 解析度及維度2個迴圈
- 使用[dtconvertor](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/DateTime/dtconvertor/)進行日期格式的轉換。

```python
#kuang@dev2 /nas2/cmaqruns/2022fcst
#$ cat metcro.py
import numpy as np
import netCDF4
import sys, datetime
from dtconvertor import dt2jul, jul2dt

bdate=datetime.datetime.strptime(sys.argv[1],"%Y-%m-%d")

for ii in ['03','09','45']:
  for fn in ['2D','3D']:
    fname='grid'+ii+'/mcip/METCRO'+fn+'.nc'
    nc1 = netCDF4.Dataset(fname, 'r+')
    nc1.SDATE,nc1.STIME=dt2jul(bdate)
    nt1=nc1.dimensions['TSTEP'].size
    SDATE=[bdate+datetime.timedelta(hours=int(i)) for i in range(nt1)]
    for t in range(nt1):
      nc1.variables['TFLAG'][t,0,:]=dt2jul(SDATE[t])
    var=np.array(nc1.variables['TFLAG'][:,0,:])
    var3=np.zeros(shape=nc1.variables['TFLAG'].shape)
    var3[:,:,:]=var[:,None,:]
    nc1.variables['TFLAG'][:]=var3[:]
    nc1.close()
```

## json檔之準備([cmaq_json3.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/earth/cmaq_json3.py))
- 類似(臭氧小時、8小時等)其他版本的作法，PM也是要經過內插、轉置的過程，寫入指定的年、月、日目錄。

### SNO相關段落

```python
o38=np.zeros(shape=(24*5,ny,nx))
names={'SO2':'so2','NO2':'no2','O3':'ozone'}
for i in range(nozn):
  ozn[i]['header']["parameterUnit"]= "ppbv"
  ozn[i]['header']["winds"]= "false"
for day in range(5):
  fname=fcst.replace('YYYYMMDD',YMDs[day].replace('-',''))
  if not os.path.isfile(fname):continue
  nc = netCDF4.Dataset(fname, 'r')
  for v in names:
    o3=nc[v][:,0,:,:]
    nt=nc.dimensions['TSTEP'].size
    var1=np.zeros(shape=(nt,ny*nx))
    for i in range(ny*nx):
      c = o3[:,n[i]//ncol, n[i]%ncol]
      var1[:,i]=np.sum(c*w[i],axis=1)
    o3=var1.flatten().reshape(nt,ny,nx)

    if v=='O3':o38[day*24:day*24+nt,:,:]=o3[:,:,:]
    for t in range(0,nt,3):
      bdate=jul2dt(nc['TFLAG'][t,0,:])
      dt=bdate.strftime("%Y-%m-%dT%H:%M:%SZ")
      dir=bdate.strftime("../%Y/%m/%d/")
      pwd='/nas1/Data/javascripts/D3js/earthFcst'+grds+'/public/data/weather/current/'
      os.system('mkdir -p '+pwd+dir)
      hh=bdate.strftime("%H00")

      for i in range(nozn):
        ozn[i]['header']['refTime']=dt
        ozn[i]['header']["parameterNumberName"]=v+"_Mixing_Ratio"
        var=o3[t,:,:]*1000
        ozn[i]['data']=list(np.flip(np.where(var!=var,0,var),axis=0).flatten())

      fnameO=pwd+dir+hh+'-'+names[v]+'-surface-level-fcst-'+grds+'.json'
      rst=wrtjson(day,t,fnameO,ozn)
```

### PM及VOC相關段落
- 使用ozn及o3等相同的容器。以節省記憶體
- 逐點進行濃度及加權的sumproduct，以進行內插。
- 除了日期的迴圈，還有變數名稱的迴圈。
- 使用np.flip指令進行y軸的翻轉。

```python
#PMs reading and output
PMst='/nas2/cmaqruns/2022fcst/grid'+grds+'/cctm.fcst/daily/PMsYYYYMMDD.nc'
names={'VOC':'vocs','PM1_TOT':'pm1','PM25_TOT':'pm25','PM10':'pm10'}
units={i:'microgram/m3' for i in names if 'PM' in i}
units.update({'VOC':'ppbc'})
for day in range(5):
  fname=PMst.replace('YYYYMMDD',YMDs[day].replace('-',''))
  if not os.path.isfile(fname):continue
  nc = netCDF4.Dataset(fname, 'r')
  for v in names:
    for i in range(nozn):
      ozn[i]['header']["parameterUnit"]=units[v]
    o3=nc[v][:,0,:,:]
...
        ozn[i]['header']["parameterNumberName"]=v
        var=o3[t,:,:]        
...
      rst=wrtjson(day,t,fnameO,ozn)
```
### 引數及IO
- 引數：起始日期YYYY-MM-DD
- 輸入檔：combine.sh結果。PMsYYYYMMDD.nc
- 輸出檔
  1. /nas1/Data/javascripts/D3js/earthFcst'+grds+'/public/data/weather/$YYYY/$MM/$DD/$HH00-$v-surface-level-fcst-$ii.json
  1. $v=pm1, pm25, pm10
  1. $ii=45, 09, 03

## [earth][eth]套件之修改
### html
- 新增SO<sub>2</sub>、NO<sub>2</sub>及VOC的文字按鈕(./public/index.html內之"text-button")在Overlay的第1行
- 新增PM<sub>1</sub> ~ PM<sub>10</sub>的文字按鈕(./public/index.html內之"text-button")在Overlay的第2行

```html
            <p class="wind-mode"><span style="visibility:hidden">Overlay</span> | <span
                class="text-button" id="overlay-pm1" title="CMAQ PM1">PM1</span> – <span
                class="text-button" id="overlay-pm25" title="CMAQ PM2.5">PM25</span> – <span
                class="text-button" id="overlay-pm10" title="CMAQ PM10">PM10</span> – <span
                class="text-button" id="overlay-ozone" title="CMAQ Ozone">O3</span> - <scan
                class="text-button" id="overlay-ozone8" title="8Hr Ozone">O38</span>
            </p>
```
- **必須**取代原有之TPW、TCW、MSLP等項目。超過6項會自動形成階層，無法獨立作動，可能是css的限制。

### js
- 開啟並定義各別SNV及PM的濃度等級(./public/libs/earth/1.0.0/[products.js](https://github.com/cambecc/earth/blob/master/public/libs/earth/1.0.0/products.js))
- 濃度等級
  - PM<sub>10</sub>、VOC：與臭氧小時值相同
  - PM<sub>2.5</sub>：為PM<sub>10</sub>的一半
  - PM<sub>1</sub>、SO<sub>2</sub>及NO<sub>2</sub>：為PM<sub>10</sub>的1/10(詳下述)

```java
        "pm1": {
            matches: _.matches({param: "wind", overlayType: "pm1"}),
            create: function(attr) {
                return buildProduct({
                    field: "scalar",
                    type: "pm1",
                    description: localize({
                        name: {en: "CMAQ PM1", ja: "小於1微米之粒狀物"},
                        qualifier: {en: " @ " + describeSurface(attr), ja: " @ " + describeSurfaceJa(attr)}
                    }),
                  paths: [FilePath(attr, "pm1", attr.surface, attr.level, "fcst", "45")],
                    date: gfsDate(attr),
                    builder: function(file) {
                        var record = file[0], data = record.data;
                        return {
                            header: record.header,
                            interpolate: bilinearInterpolateScalar,
                            data: function(i) {
                                return data[i];
                            }
                        }
                    },
                    units: [
                        {label: "ug/m3", conversion: function(x) { return x; }, precision: 3}
                    ],
                    scale: {
                        bounds: [0, 40],
                        gradient:
                            µ.segmentedColorScale([
                            [ 0,  [37, 4, 42]],
                            [ 2,     [41, 10, 130]],//purple blue(0~40)
                            [ 5,  [24, 132, 14]],   //green(41-60)
                            [ 9,  [247, 251, 59]], //yellow(61-124)
                            [12,  [235, 167, 21]],//
                            [18,  [230, 71, 39]], //red (165-204)
                            [30,  [128,0,128]], //purple red(205-404)
                            [40,  [81, 40, 40]],//brown
                            ])
                    }
                });
            }
        },
```

## 結果

| ![earth_pm.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/earth_pm.PNG)|
|:-:|
| <b>解析度9公里大陸東南沿海臺灣海峽範圍CMAQ PM<sub>10</sub>之模擬結果</b>|

| ![earth_SNV.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/earth_SNV.PNG)|
|:-:|
| <b>解析度3公里臺灣地區CMAQ SO<sub>2</sub>之模擬結果</b>|

[eth]: <https://github.com/cambecc/earth> "cambecc(2016), earth building, launching and etc on GitHub. "
[combine]: <https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#combine-腳本> "CMAQ Model System->Recommend System->執行檔與程式庫->COMBINE 腳本"
[shks]: <https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs> "CMAQ Model System->Post Processing->跨日結果之篩選整併->COMBINE_ACONC檔案之篩選整併->shk.cs"