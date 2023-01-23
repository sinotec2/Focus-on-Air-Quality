---
layout: default
title: "高空觀測數據之自動下載"
parent: "NCEP"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-26 19:47:53
tags: Crawlers OBSGRID
---

# 高空觀測數據之自動下載 

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
- [NCEP](https://www.weather.gov/ncep/) (National Centers for Environmental Prediction)彙整了全球高空觀測數據([ds351.0](https://rda.ucar.edu/datasets/ds351.0/#!description))，是MM5/WRF進行四階同化需要的數據，資料格式是[little_r](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式，可以被`obsgrid`、`WRFDA`等程式接受。
- 同樣的，NCEP並無提供指定範圍自動下載的工具，只能下載全球範圍所有觀測值。高空數據層數較多，檔案較地面數據更大。
- 幸好檔案是ASCII格式，可以達到很高的壓縮率。

## 批次執行與自動執行
詳見[樓上](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/NCEP/)。

## 程式差異說明
因程式與ff.py很相像，此處介紹其差異之處
- 儲存路徑

```python
kuang@114-32-164-198 ~/python_eg/NCEP_fetch
$ diff ff.py uu.py
53c53
< path='/Users/WRF4.1/NCEP/FNL/'
---
> path='/Users/WRF4.1/NCEP/UPA_ds351.0/'
```

- 檔名中的日期出現在不同位置
  - FNL: fnl_**20211124**_18_00.grib2
  - SRF: SURFACE_OBS:**20211118**18
  - UPA: OBS:**20211118**18

```python
55c55
< blk=os.popen('ls '+path+yrold+'|tail -n1').read().strip('\n').split('_')
---
> blk=os.popen('ls '+path+yrold+'|tail -n1').read().strip('\n').split('_')[-1].split(':')
```

- 高空數據有可能被壓縮(`gzip`)，取用檔名時要多加此一選項。（如沒有`gz`則不會有任何改變）

```python
57c57
<   begd=int(blk[1])
---
>   begd=int(int(blk[1].replace('.gz',''))/100)
```

- 高空數據更新較慢，比實際日期晚**8天**

```python
64c64
< edate = tdate+datetime.timedelta(days=-2)
---
> edate = tdate+datetime.timedelta(days=-8)
```

- url字串的內容也有所差異

```python
76,82c76,77
< mos=[ymd[4:6] for ymd in ymds]
< head=['grib2/'+yr+'/'+yr+'.' for yr in yrs]
< med='/fnl_'
< udl='_'
< tail='_00.grib2'
< listoffiles=[head[i]+mos[i]+med+ymds[i]+udl+str(h)+tail for i in xrange(len(ymds)) for h in ['00','06','12','18']]
< #sys.exit('OK')
---
> head=['little_r/'+yr+'/OBS:' for yr in yrs]
> listoffiles=[head[i]+ymds[i]+str(h)  for i in xrange(len(ymds)) for h in ['00','06','12','18']]
```

- `macOS`能夠處理冒號，不需更換。

```python
86c81
<     ofile=file[idx+1:].replace(':','_')
---
>     ofile=file[idx+1:]#.replace(':','_')
88c83
<     ofile=file.replace(':','_')
---
>     ofile=file#.replace(':','_')
```

- 高空數據有可能被壓縮(`gzip`)，測試邏輯要多加此一選項。

```python
91c86
<   if os.path.isfile(path1+ofile):continue
---
>   if os.path.isfile(path1+ofile) or os.path.isfile(path1+ofile+'.gz') :continue
```

- NCEP 資料庫編碼，高空數據是`ds351.0`

```python
96c91
<     infile=opener.open("http://rda.ucar.edu/data/ds083.2/"+file)
---
>     infile=opener.open("http://rda.ucar.edu/data/ds351.0/"+file)
```

## 完整程式碼
- [uu.py](https://raw.githubusercontent.com/sinotec2/python_eg/master/NCEP_fetch/uu.py)
