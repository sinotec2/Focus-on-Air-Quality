---
layout: default
title: "地面觀測數據之自動下載"
parent: "NCEP"
grand_parent: "wind models"
nav_order: 3
date:               
last_modified_date:   2021-11-26 19:47:53
---

# 地面觀測數據之自動下載 

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
- 全球地面觀測數據([ds461.0](https://rda.ucar.edu/datasets/ds461.0/#!description))是MM5/WRF進行四階同化需要的數據，資料格式是l[little_r](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式，可以被`obsgrid`、`WRFDA`等程式接受。
- 同樣的，NCEP並無提供指定範圍自動下載的工具，只能下載全球範圍所有觀測值。幸好檔案是ASCII格式，可以達到很高的壓縮率。

## 自動執行
- 設計夜間21:00進行下載，`crontab`如下：
```bash
crontab -l|grep fus
0 21  *  *  * /Users/WRF4.1/NCEP/fus.cs &> /Users/WRF4.1/NCEP/crontab_log.txt 2>&1
```

## 程式特色說明
因程式與ff.py很相像，此處介紹其差異之處
- 結果檔案儲存位置
```python
kuang@114-32-164-198 ~/python_eg/NCEP_fetch
$ diff ff.py ss.py
53c53
< path='/Users/WRF4.1/NCEP/FNL/'
---
> path='/Users/WRF4.1/NCEP/SRF_ds461.0/'
```
- 
```python
55c55,57
< blk=os.popen('ls '+path+yrold+'|tail -n1').read().strip('\n').split('_')
---
> print yrold
> blk=os.popen('ls '+path+yrold+'|tail -n1').read().strip('\n').split('_')[-1].split(':')
> print blk
```
- 
```python
57c59
<   begd=int(blk[1])
---
>   begd=int(int(blk[1].replace('.gz',''))/100)
```
- 
```python
64c66
< edate = tdate+datetime.timedelta(days=-2)
---
> edate = tdate+datetime.timedelta(days=-8)
```
- 
```python
76,82c78,79
< mos=[ymd[4:6] for ymd in ymds]
< head=['grib2/'+yr+'/'+yr+'.' for yr in yrs]
< med='/fnl_'
< udl='_'
< tail='_00.grib2'
< listoffiles=[head[i]+mos[i]+med+ymds[i]+udl+str(h)+tail for i in xrange(len(ymds)) for h in ['00','06','12','18']]
< #sys.exit('OK')
---
> head=['little_r/'+yr+'/SURFACE_OBS:' for yr in yrs]
> listoffiles=[head[i]+ymds[i]+str(h)  for i in xrange(len(ymds)) for h in ['00','06','12','18']]
```
- 
```python
86c83
<     ofile=file[idx+1:].replace(':','_')
---
>     ofile=file[idx+1:]#.replace(':','_')
88c85
<     ofile=file.replace(':','_')
---
>     ofile=file#.replace(':','_')
```
- 
```python
91c88
<   if os.path.isfile(path1+ofile):continue
---
>   if os.path.isfile(path1+ofile) or os.path.isfile(path1+ofile+'.gz') :continue
```
- 
```python
96c93
<     infile=opener.open("http://rda.ucar.edu/data/ds083.2/"+file)
---
>     infile=opener.open("http://rda.ucar.edu/data/ds461.0/"+file)

```



## 完整程式碼
- [ff.py](https://raw.githubusercontent.com/sinotec2/python_eg/master/NCEP_fetch/ff.py)

## Reference
- University of Waterloo, [WRF Tutorial](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial),  27 June 2019, at 14:53.
- Andre R. Erler, WRF-Tools/Python/wrfrun/[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py), Commits on Nov 23, 2021.
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)

