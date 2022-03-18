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
- 程式大略類似[EAC4檔案轉成5階m3.nc](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2D1m3/)，維須建立邊界線上的座標，並將5階之空氣密度也轉成最靠近邊界的4階檔案。
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
  if i in ['EXEC_ID','FILEDESC','UPNAM','GDNAM','FTYPE']:continue
  exec('nc.'+i+'=nc0.'+i)
nc.NVARS=50  
```
- 其中**FTYPE**有關鍵影響，一般檔案此值為1，BCON檔案此值為**2**。


## 空氣密度的引用
- 空氣密度是mcip的結果，因此其網格系統定義是與ACON檔案一致的。鑒於BCON範圍是在ACON的外圍一圈，所以理論上是沒有空氣密度值的。

### 空氣密度之邊界位置
- 此處以網格最外圍值做為邊界上的密度，其位置與前述D0座標向內縮1格，頂點則重複以符合BCON檔案的定義：

```python
i0,j0=0,0
i1,j1=ncol1-1,nrow1-1
idxb=[(j0,i) for i in range(ncol1)] +[(j0,i1)] +   [(j,i1) for j in range(nrow1)] +[(j1,i1)] + \
    [(j1,i) for i in range(i1,i0-1,-1)] +[(j1,i0)] + [(j,i0) for j in range(j1,j0-1,-1)]+[(j0,i0)]
idxb=np.array(idxb,dtype=int).flatten().reshape(nbnd1,2).T
```

### 矩陣之降階(selection)
- 在引用時是將4階的矩陣予以降成3階，將X, Y 2維消除成為1維的邊界線
- 使用指標系統，並利用定型矩陣的None功能，來指定重複的指標，從XY空間中挑出邊界上的位置。
- 將3階的N矩陣壓平成為1階，這樣就可以做為dens的指標。多階矩陣整數，無法成為另一矩陣的指標，而能發揮迴圈效果的。
- 最後將dens矩陣reshape將其恢復成3階形狀
- 除了選取邊界上的密度、此一手法也用在D0 2維網格系統的線性化、也用在最近距離點的選取。

```python
N=[np.zeros(shape=(ntA,nlay1, nbnd1),dtype=int) for i in range(4)]
N[0][:,:,:]=np.array([t for t in range(ntA)])[:,None,None]
N[1][:,:,:]=np.array([k for k in range(nlay1)])[None,:,None]
N[2][:,:,:]=idxb[0][None,None,:]
N[3][:,:,:]=idxb[1][None,None,:]
for n in range(4):
  N[n]=N[n].flatten()
dens2=np.zeros(shape=(ntA,nlay1, nbnd1))
if nlay1==40:
  dens2[:,:,:]=dens[N[0],N[1],N[2],N[3]].reshape(ntA,nlay1, nbnd1)
```

## EAC4網格點之取值
- 因邊界線已經非常靠近EAC4下載範圍的外圍，甚或不在範圍內。因此使用griddata進行內插會造成無值的結果(nan)。
- 同時以龐大的2維矩陣內插出少數點，似乎在效率上也不對等。
- 

## 程式下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2bc.py)

## Reference
- ECMWF, **EAC4 (ECMWF Atmospheric Composition Reanalysis 4)**, [copernicus](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview),record updated 2021-12-07 16:10:05 UTC
- 純淨天空, **python numpy flip用法及代碼示例**, [vimsky](https://vimsky.com/zh-tw/examples/usage/python-numpy.flip.html)
-Python学习园, **Scipy Tutorial-多维插值griddata**, [cpython](http://liao.cpython.org/scipytutorial11.html)
