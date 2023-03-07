---
layout: default
title:  繪製wrfout地面氣流線
parent: NCL Programs
grand_parent: Graphics
date:  2022-08-11
last_modified_date: 2023-03-07 16:37:55
tags: NCL graphics
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

- input file name: `wrfout`，只會讀取U10及V10與時間標籤。
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

### 結果範例

| ![wrf_gsn.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/wrf_gsn.png) |
|:--:|
| <b>CWBWRF_3k範圍地面氣流線 </b>|  

## d4範圍版本

### 修改項目

- 台灣範圍因為面積較小，流線必須密一點，div取2。
- 海岸線的解析度也必須高一些，取HighRes
  - 須至[Leibniz Institute for Baltic Sea Research Warnemünde](https://www.io-warnemuende.de/rangs-en.html)下載rags及gshhs壓縮檔，並放在正確的目錄下。

```bash
mkdir -p $NCARG_ROOT/lib/ncarg/database/rangs
cd $NCARG_ROOT/lib/ncarg/database/rangs
for i in {0..4};do wget https://www.io-warnemuende.de/tl_files/staff/rfeistel/download/rangs\(${i}\).zip;done
for i in {0..4};do wget https://www.io-warnemuende.de/tl_files/staff/rfeistel/download/gshhs\(${i}\).zip;done
for i in $(ls *zip);do unzip $i;done
```

- 光靠海岸線，台灣地區內部參考還蠻少的，需加入縣市界shape檔
  - 先暫緩plot的匯出，等待疊圖
  - 台灣內部高風速的機會較少，為使底圖具有較高的辨識效果，將shape檔的線條設成紅色
  - 呼叫gsn_add_shapefile_polylines貼上shape檔
  - 參考[shapefiles_3.ncl](https://www.ncl.ucar.edu/Applications/Scripts/shapefiles_3.ncl)與[等值圖加上色點](./cntr_w_dots.md)。

### 程式碼差異

```bash
$ diff wrf_gsn_8.ncl streamlineTW.ncl
52c52
<   div= 8 ; more is sparse, less is condense
---
>   div= 2 ; more is sparse, less is condense
99c99
<   res@mpDataBaseVersion  = "MediumRes"    ; better map outlines
---
>   res@mpDataBaseVersion  = "HighRes"    ; better map outlines
141a142,143
>   res@gsnDraw             = False          ; don't draw plot yet
>   res@gsnFrame            = False          ; don't advance frame yet
142a145,158
>
>    shapefile_dir  = "/home/kuang/NCL_scripts/shapes/"       ;-- directory containing the shapefiles
>    shp_name2      = "COUNTY_MOI_1090820.shp"                         ;-- shapefile to be used
>    shp_fname2      = shapefile_dir+shp_name2
> ;---Section to add polylines to map.
>   plres             = True           ; resource list for polylines
>   plres@gsLineColor = "red"
>
>    id = gsn_add_shapefile_polylines(wks,plot,shp_fname2,plres)
>    draw(plot)   ; This will draw attached polylines and map
>    frame(wks)   ; Advanced frame.
```

### 執行批次2

- 因每日的作業結果中已經有U10V10檔案(逐日檔、for [daily_traj](../../../TrajModels/ftuv10/daily_traj_cs.md))，因此只要將其連結起來，再按所需要的時間間隔一一繪圖。

```bash
source ~/conda_ini ncl_stable
ncrcat U10V10_d03_2023-03-* U10.nc
for i in {0..265..6};do 
  ncks -O -d Time,$i UV10.nc wrfout; 
  ncl ~/NCL_scripts/streamlineTW.ncl;
  iii=$(printf "%03d" $i);
  mv wrf_gsn.png stln_$iii.png;
done
```

### 臺灣範圍結果

| ![stln_060.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/stln_060.png) |
|:--:|
| <b>台灣地區範圍地面氣流線。夜間山區有明顯的山風。</b>|  

## 程式下載

### [wrf_gsn_8.ncl][wrf_gsn_8.ncl]

{% include download.html content="繪製wrfout地面氣流線(東亞範圍)：[wrf_gsn_8.ncl][wrf_gsn_8.ncl]" %}

### [streamlineTW.ncl][streamlineTW.ncl]

{% include download.html content="繪製wrfout地面氣流線(臺灣範圍)：[streamlineTW.ncl][streamlineTW.ncl]" %}

[eth]: <https://github.com/cambecc/earth> "cambecc(2016), earth building, launching and etc on GitHub. "
[wrf_gsn_8.ncl]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/wrf_gsn_8.ncl> "Drawing streamlines colored by another field over a map"
[streamlineTW.ncl]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/streamlineTW.ncl "streamlineTW"
