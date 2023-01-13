---
layout: default
title:  繪製wrfout地面氣流線
parent: NCL Programs
grand_parent: Graphics
date:  2022-08-11
last_modified_date: 2022-08-11 16:37:07
tags: NCL
---

# 繪製wrfout地面氣流線
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
- 快速繪製地面氣流線，除了可以使用meteoinfo之外，似乎沒有好的方式。
  - 新版VERDI不再有vector的功能。
  - meteoinfo似乎不能直接開wrfout，還是需要ncks將數據取出
  - 如果解析度不是很高，也許可以轉成json檔，用[eth][eth]套件去開啟，也是一個不錯的方式。
  - 如果wrf-python有流線的套件就好了，可惜事與願違。
- NCL的介紹與文件檔案連結，可以到[NCL Programs](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL) 去找。

## 執行批次
- 繪製流線圖至少需要wrfout的經緯度、時間標籤、以及U10/V10等變數。
- 環境變數NCAR_ROOT設定在執行檔前面，這是for crontab的執行方式，一般命令列也是可行執行。
- 下面範例會畫出2022-08-10～17日每天00Z的流線圖

```bash
for d in {0..7};do 
nc=wrfout_d01_2022-08-1${d}_00:00:00
  for i in 0;do 
    rm wrfout
    ncks -O -v Times,XLAT,XLONG,U10,V10,PBLH -d Time,$i $nc wrfout
    NCAR_ROOT=/opt/anaconda3/envs/ncl_stable /opt/anaconda3/envs/ncl_stable/bin/ncl ~/NCL_scripts/streamline/wrf_gsn_8.ncl
    mv wrf_gsn.png wrf_gsn${d}_$i.png
  done
done
```

## [wrf_gsn_8.ncl][wrf_gsn_8.ncl]修改說明
- 原始的程式可以參考[NCL官網wrfgsn](https://www.ncl.ucar.edu/Applications/Scripts/wrf_gsn_8.ncl)

### IO
- input file name: `wrfout`
- output png filename: `wrf_gsn.png`

### 流線圖面密度調整
- NCL函數沒有提供調整密度的選項，必須自行篩選要進入繪圖程式的數據
- `dimsizes()`:輸出矩陣的維度
- `div=8`:每8格取樣。將結果存到u10/v10/lon/lat矩陣，適用原本的繪圖程式。

```python
  dom_dims = dimsizes(uu10)
  dom_rank = dimsizes(dom_dims)
  nx = dom_dims(dom_rank - 1) - 1
  ny = dom_dims(dom_rank - 2) - 1
  div= 8 ; more is sparse, less is condense
  i=nx/div
  j=ny/div
  nx2=toint(i)
  ny2=toint(j)
  u10 =new((/ny2,nx2/), "float")
  v10 =new((/ny2,nx2/), "float")
  lat =new((/ny2,nx2/), "float")
  lon =new((/ny2,nx2/), "float")
  do i=0,nx2-1
  do j=0,ny2-1
    u10(j,i)=uu10(j*div,i*div)
    v10(j,i)=vv10(j*div,i*div)
    lat(j,i)=lat1(j*div,i*div)
    lon(j,i)=lon1(j*div,i*div)
  end do
  end do
```

### 圖說
- 讀取wrfout的時間標籤作為圖說[tiMainString](https://www.ncl.ucar.edu/Document/Graphics/Resources/ti.shtml#tiMainString)

```python
  Times = wrf_user_getvar(a,"Times",it)
...
  res@tiMainString       = tostring(Times)
```

### 色標單位
- 色標距離主題（[pmLabelBarOrthogonalPosF](http://ncl.ucar.edu/Document/Graphics/Resources/pm.shtml#pmLabelBarOrthogonalPosF)）太靠近，放不進單位之文字
- 文字與字型大小（[lbTitleString](https://www.ncl.ucar.edu/Document/Graphics/Resources/lb.shtml#lbTitleString) / [lbTitleFontHeightF](https://www.ncl.ucar.edu/Document/Graphics/Resources/lb.shtml#lbTitleFontHeightF)）

```python
...
  res@lbTitleString    = "unit: knots"
  res@lbTitleFontHeightF= .01
  res@pmLabelBarOrthogonalPosF = .10
```
## 結果範例

| ![wrf_gsn.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/wrf_gsn.png) |
|:--:|
| <b>CWBWRF_3k範圍地面氣流線 </b>|  

## [wrf_gsn_8.ncl][wrf_gsn_8.ncl]程式下載

{% include download.html content="將CWB數據填入WRF客觀分析場之程式：[wrf_gsn_8.ncl][wrf_gsn_8.ncl]" %}

[eth]: <https://github.com/cambecc/earth> "cambecc(2016), earth building, launching and etc on GitHub. "
[wrf_gsn_8.ncl]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/wrf_gsn_8.ncl> "Drawing streamlines colored by another field over a map"