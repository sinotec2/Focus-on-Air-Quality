---
layout: default
title: "高空觀測數據之自動下載"
parent: "NCEP"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-26 19:47:53
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

## 自動執行
- 設計夜間21:00進行下載，`crontab`如下：
```bash
crontab -l|grep fus
0 21  *  *  * /Users/WRF4.1/NCEP/fus.cs &> /Users/WRF4.1/NCEP/crontab_log.txt 2>&1
```

## 程式分段說明
-
```python

```
-
```python

```
-
```python

```
-
```python

```
-
```python

```
-
```python

```
-
```python

```
-
```python

```


## 完整程式碼
- [ff.py](https://raw.githubusercontent.com/sinotec2/python_eg/master/NCEP_fetch/ff.py)

## Reference
- University of Waterloo, [WRF Tutorial](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial),  27 June 2019, at 14:53.
- Andre R. Erler, WRF-Tools/Python/wrfrun/[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py), Commits on Nov 23, 2021.
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md)

