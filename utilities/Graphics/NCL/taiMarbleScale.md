---
layout: default
title:  軌跡線貼在Marble底圖上
parent: NCL
grand_parent: Graphics
last_modified_date: 2023-07-21 11:31:15
tags: NCL graphics traj_model Marble
---

# 軌跡線貼在Marble底圖上

{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## 背景

- 除了研究與報告試誤過程中的貼版之外，對於印刷品質要求較高的完稿，會需要使用更高解析度的地形圖做為背景底圖，這是NCL的強項之一。
- 這個系列是參考[NCL Graphics: Topographic maps](https://www.ncl.ucar.edu/Applications/topo.shtml)延續自[反軌跡線通過網格機率分布圖](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL/prob2png/)之底圖，以WPS 333公尺解析度地形高程為基底、替換原程式之地形檔(`ETOPO5.dat`)，貼上縣市界、並視軌跡線的範圍需要，減小圖面範圍以加大局部內容細節。
- 下載ncl[程式碼](./taiMarbleScale.ncl)

## 程式說明

- 程式可以獨立執行，也可搭配cgi-python呼叫`os.system`

### 輸入檔案

- WPS 333公尺解析度地形高程：`/nas1/WRF4.0/WPS/geo_em/geo_em.d04_333m.nc`
- 縣市界shp檔：`/var/www/html/taiwan/TWN_COUNTY.shp`(dbf, prj, shx also needed)
- 存著csv檔名之容器：`./filename.txt`
- 軌跡線csv檔(處理過程詳[daily_traj.cs](../../../TrajModels/ftuv10/daily_traj_cs.md))
  - (如)`./btrj23.74_120.4_2023032912.csv`，檔頭為`xp,yp,Hour,ymdh`、單位為公尺，TWD97系統座標值
  - 線段端點座標，前述主檔名+`_line.csv`，無檔頭，單位為度，經度及緯度。
  - 標記點座標，前述主檔名+`_mark.csv`，無檔頭，單位為度，經度及緯度。

### Marble顏色與色階

- GMT_ocean與OceanLakeLandSnow色階之讀取
- 此2處副程式不必修改

```bash
undef("read_ocean_land_colormap")
function read_ocean_land_colormap(num_ocean)
local cmap_ocn, cmap_lnd
begin
  cmap_ocn = read_colormap_file("GMT_ocean")
  cmap_lnd = read_colormap_file("OceanLakeLandSnow")
  newcmap = array_append_record(cmap_ocn(0:num_ocean-1,:),cmap_lnd(2::2,:),0)
  return(newcmap)
end
```

- 色階

```bash
undef("calc_levels_and_colors")
function calc_levels_and_colors(wks,emin,emax,split_elev,num_ocean_values)
local start_ocean, ocean_range, land_range, olevels, llevels, nol, nll, clen
begin
  cmap = read_ocean_land_colormap(num_ocean_values)
  clen = dimsizes(cmap(:,0))

  start_ocean = 0
  end_ocean   = num_ocean_values-1
  start_land  = end_ocean+1
  ocean_range = end_ocean-start_ocean+1
  land_range  = clen-start_land+1
  olevels     = fspan(emin,split_elev,ocean_range)
  llevels     = fspan(split_elev,emax,land_range)
  nol         = dimsizes(olevels)
  nll         = dimsizes(llevels)
  levels      = new((nol-1)+(nll-2),float)
  levels(0:nol-2) = olevels(1:)
  levels(nol-1:)  = llevels(1:nll-2)
  return([/levels,cmap/])
end
```

### 高程之讀取與修正

- 檔案來自於WPS/geogrid.exe處理結果
- Marble的特性是會畫海床的等深線，因此海邊高程如果為負值，將會被塗上顏色。需要以海陸遮蔽之標誌(`land`)來修正。

```bash
undef("read_elev_data")
function read_elev_data(topo_file)
local nlat, nlon, topo_file, lat, lon
begin
  a = addfile("/nas1/WRF4.0/WPS/geo_em/geo_em.d04_333m.nc","r")
  elev = a->HGT_M(0,:,:)
  land = a->LANDMASK(0,:,:)
  lt = a->XLAT_M(0,:,:)
  ln = a->XLONG_M(0,:,:)
  elev@lat2d = lt
  elev@lon2d = ln
  elev = elev + 5 + (land-1)*10

  return(elev)
end
```

### 繪製等高線圖及軌跡線

- 等高線圖-Marble底圖

```bash
undef("draw_topo_map")
procedure draw_topo_map(wks,elev,title)
local res, labels, nlevels
begin
...
  res                    = True
...
  split_elev               = -30; -40   ; meters
  num_ocean_colors         = 40
  emax=3000.
  levels_and_colors        = calc_levels_and_colors(wks,0.       ,emax     ,split_elev,num_ocean_colors)

  plot = gsn_csm_contour_map(wks,elev,res)
```

- 軌跡線與標記點

```bash
  gres                  = True                ; polyline mods desired
  gres@gsLineThicknessF = 3.0                 ; line thickness

  gres@gsLineOpacityF     = 1.0
  gres@gsMarkerSizeF      = 0.008
  gres@gsMarkerThicknessF =  3
  do ip=4,4
    csv   =       True
    csv_cont=asciiread(str_concat((/trj_name,pthL(ip),".csv"/)),-1,"float")
    nLL=dimsizes(csv_cont)
    npt=toint(nLL/2)
    lon=new(npt,float)
    lat=new(npt,float)
    do i=0,npt-1
      lon(i)=csv_cont(i*2)
      lat(i)=csv_cont(i*2+1)
    end do
    gres@gsLineColor        = cls(ip)               ; line color
    gsn_polyline (wks, plot, lon(:), lat(:), gres)

    gres@gsMarkerIndex      = mks(ip)
    gres@gsMarkerColor      = cls(ip)
    gres@gsMarkerOpacityF   = 1.0
    csv   =       True
    csv_cont2=asciiread(str_concat((/trj_name,pthM(ip),".csv"/)),-1,"float")
    nLL=dimsizes(csv_cont2)
    npt=toint(nLL/2)
    lon2=new(npt,float)
    lat2=new(npt,float)
    do i=0,npt-1
      lon2(i)=csv_cont2(i*2)
      lat2(i)=csv_cont2(i*2+1)
    end do
    gsn_polymarker(wks,plot,lon2(:),lat2(:), gres)
  end do
```


### 自行決定最適範圍

- 0.5度約50Km 

```bash
  res@mpMinLatF            = max((/min(lat)-0.5,min(elev@lat2d)/))       ; zoom in on map
  res@mpMaxLatF            = min((/max(lat)+0.5,max(elev@lat2d)/))
  res@mpMinLonF            = max((/min(lon)-0.5,min(elev@lon2d)/))
  res@mpMaxLonF            = min((/max(lon)+0.5,max(elev@lon2d)/))
```

### 繪製縣市邊界線

```bash
  filename="/var/www/html/taiwan/TWN_COUNTY.shp"
  dum  = gsn_add_shapefile_polylines(wks,plot,filename,True)
```

## 檢視程式碼

{% include download.html content="[軌跡線貼在Marble底圖上之ncl程式](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/taiMarbleScale.ncl)" %}
## 結果

![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-07-21-09-25-35.png)
