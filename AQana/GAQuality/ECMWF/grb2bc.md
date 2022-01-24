---
layout: default
title: EAC4檔案直接寫成邊界濃度
parent: Global AQ Data Analysis
grand_parent: AQ Data Analysis
nav_order: 6
date: 2021-12-23 14:04:02
last_modified_date:   2021-12-23 14:03:54
---

# EAC4檔案轉成4階邊界檔案
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
- 使用[EAC4](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview)逐3小時檔案做為空品模式的邊界條件，除了先將其轉成5階空品檔案、使用[bcon](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/run_bconMM_RR_DM/)進行轉檔之外，考量到大多數範圍內部的空品數值是沒有作用的，此舉會儲存大量無用之檔案，不甚合理(如檔案太大也不可行、單一檔案可能上TB)，採直接轉寫較為合理。
- 程式大略類似[EAC4檔案轉成5階m3.nc]()，維須建立邊界線上的座標，並將5階之空氣密度也轉成最靠近邊界的4階檔案。
- 此處以CWBWRF_15Km範圍為例。
  - 其邊界位置為D0範圍之一圈:

```python
nrow1,ncol1=nc1.NROWS,nc1.NCOLS
nrow0,ncol0=nc1.NROWS+5,nc1.NCOLS+5
x1d=[nc1.XORIG+nc1.XCELL*(i-2) for i in range(ncol0)]
y1d=[nc1.YORIG+nc1.YCELL*(i-2) for i in range(nrow0)]
x1,y1=np.meshgrid(x1d, y1d)
i0,j0=1,1
i1,j1=i0+ncol1+1,j0+nrow1+1
idx=[(j0,i) for i in range(i0+1,i1+1)]  +   [(j,i1) for j in range(j0+1,j1+1)] + \
    [(j1,i) for i in range(i1-1,i0-1,-1)] + [(j,i0) for j in range(j1-1,j0-1,-1)]
idxo=np.array(idx,dtype=int).flatten().reshape(nbnd1,2).T
x1,y1=x1[idxo[0],idxo[1]],y1[idxo[0],idxo[1]]
```
- 原程式x1、y1為2維網格，此處改為1維陣列，其長度`nbnd=(nrow1+ncol1)*2+4`

## BCON模版之準備
- 由於EAC4只有部分空氣品質項目(NVARS=50)，因此由其他範圍之現有邊界檔案予以[擴充或裁剪](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)即可。
- 所有的座標系統設定必須維持與GRIDDESC完全一致。

```python
atts=['CDATE',  'CTIME', 'EXEC_ID', 'FILEDESC', 'FTYPE', 'GDNAM', 'GDTYP', 'HISTORY', 'IOAPI_VERSION', 'NCO', 'NCOLS',  'NROWS',
     'NTHIK', 'P_ALP', 'P_BET', 'P_GAM', 'UPNAM', 'WDATE',
     'WTIME', 'XCELL', 'XCENT', 'XORIG', 'YCELL', 'YCENT', 'YORIG']
for i in atts:
  if i not in dir(nc0):continue
  exec('nc.'+i+'=nc0.'+i)
nc.NVARS=50  
```

## 空氣密度的引用
- 空氣密度是mcip的結果，因此其網格系統定義是與ACON檔案一致的。鑒於BCON範圍是在ACON的外圍一圈，所以理論上是沒有空氣密度值的。
- 此處以網格最外圍值做為邊界上的密度，其位置與前述D0座標向內縮1格，頂點則重複以符合BCON檔案的定義：

```python
i0,j0=0,0
i1,j1=ncol1-1,nrow1-1
idxb=[(j0,i) for i in range(ncol1)] +[(j0,i1)] +   [(j,i1) for j in range(nrow1)] +[(j1,i1)] + \
    [(j1,i) for i in range(i1,i0-1,-1)] +[(j1,i0)] + [(j,i0) for j in range(j1,j0-1,-1)]+[(j0,i0)]
idxb=np.array(idxb,dtype=int).flatten().reshape(nbnd1,2).T
```
- 在引用時是將5階的矩陣予以降成4階

## 程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2D1m3.py)

## Reference
- ECMWF, **EAC4 (ECMWF Atmospheric Composition Reanalysis 4)**, [copernicus](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview),record updated 2021-12-07 16:10:05 UTC
- 純淨天空, **python numpy flip用法及代碼示例**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.flip.html)
-Python学习园, **Scipy Tutorial-多维插值griddata**, [cpython](http://liao.cpython.org/scipytutorial11.html)