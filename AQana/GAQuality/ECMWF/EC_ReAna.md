---
layout: default
title: "ECMWF ReAnalysis"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 4
date: 2021-12-16 14:07:27
last_modified_date:   2021-12-16 14:07:31
---

# 歐洲中期天氣預報中心再分析數據之下載
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

### 作業流程
- 須先在[哥白尼網站](https://ads.atmosphere.copernicus.eu/user/login?destination=/)註冊帳密(免費)。在User Profile處取得將API Key，將其寫進電腦的${HOME}/.cdsapirc檔案內，範例如下

```bash
$ cat ~/.cdsapirc
url: https://ads.atmosphere.copernicus.eu/api/v2
key: 2556:e6b523da-4703-4dc7-bcfd-94cb2d8ed395 
```
- 下載cdsapi軟件：pip install cdsapi
- 到[eac4網址](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=form)勾選下載項目
- 在網址上選好選項後，點選「Show API request」複製retrieve{...}內容，貼在python程式內，以python程式進行下載。
- 下載完成後繼續轉變格式(ncl_convert2nc)、將nc檔案內容填入m3.nc檔案備用(進一步檢查)

## 下載、準備、編譯

### 空品數據之下載(get_d2.py)

```python
import cdsapi
import datetime
import os
c = cdsapi.Client()

def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)

SPECs=['carbon_monoxide', 'ethane', 'formaldehyde', 'isoprene', 'nitrogen_dioxide', 'nitrogen_monoxide', 'propane', 'sulphur_dioxide' ]
SPEC+=['ozone', 'isoprene'] 
iyr=2019

for sp in SPECs:
  for m in range(1,13):
    mo='{:02d}'.format(m)
    fname=sp+'_'+str(iyr)[2:]+mo+'.grib'
    if os.path.exists(fname):continue
    lastYr=(datetime.datetime(iyr,m,1)+datetime.timedelta(days=-1)).year
    lastMo=(datetime.datetime(iyr,m,1)+datetime.timedelta(days=-1)).month
    beg0=datetime.datetime(lastYr,lastMo,15)
    begd=beg0+datetime.timedelta(days=4*4)
    endd=beg0+datetime.timedelta(days=12*4)
    begd=str(begd.strftime("%Y-%m-%d"))
    endd=str(endd.strftime("%Y-%m-%d"))

    c.retrieve(
    'cams-global-reanalysis-eac4',
    {
    'model_level': ['21', '22', '23', '24', '25', '26', '27',
      '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
      '39', '40', '42', '43', '44', '46', '47', '48', '49', '50', '51',
      '53', '54', '56', '57', '59'],
    'variable': sp,
    'date': begd+'/'+endd,
    'time': [
      '00:00', '03:00', '06:00',
      '09:00', '12:00', '15:00',
      '18:00', '21:00',
        ],
    'area': [
      32, 111, 15,
      131,
      ],
    'format': 'grib',
    },
     fname)  
```

## Reference
