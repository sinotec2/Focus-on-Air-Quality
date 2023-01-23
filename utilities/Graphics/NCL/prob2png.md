---
layout: default
title:  反軌跡線通過網格機率分布圖
parent: NCL Programs
grand_parent: Graphics
has_children: true
last_modified_date: 2023-01-23 19:41:22
tags: NCL graphics
---

# 反軌跡線通過網格機率分布圖
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

- 結果詳見[WRF三維軌跡分析#NCL繪圖](../../../TrajModels/btraj_WRFnests/acc_prob.md#ncl繪圖)
- 前處理程式([acc_prob.py](../../../TrajModels/btraj_WRFnests/acc_prob.md))將軌跡通過網格的機率存成m3nc檔案，如此就可以套用[pm10.ncl](https://github.com/sinotec2/cmaq_relatives/blob/master/post/pm10.ncl)、詳見[cmaq2gif](cmaq2gif.md)。
- 以下就差異部分進行說明。詳細程式碼請參考[terr.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/terr.ncl)。

## terr.ncl與pm10.ncl差異說明

### 對照表

項目|pm10.ncl|terr.ncl|說明
:-:|:-:|:-:|-
輸入檔|cmaq標準輸出檔|含有經緯度的m3nc檔|前者需另由GRIDCRO2D檔案讀取經緯度；後者模板為tmplateD1_27km.nc
時間序列|有|無|
外加軌跡線|無|有|後者有軌跡方向之迴圈
取log10|有|無|等值界線也隨之差異
中國省界底圖|bou2_4p.shp|bou2_4p.shp|
台灣縣市底圖|無|有|小範圍需要
國界|有|無|後者範圍未涉及國界

### 輸入檔案差異

- prob.nc檔案內含經緯度，不需另外給定。

```bash
kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
$ diff ./kmean_FG123/terr.ncl ~/NCL_scripts/contour_with_basemap/pm10.ncl
155,167c155,166
<   
< ; a = addfile("/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_27km.nc","r")
<   str=(/"prob",path,".nc"/)
<   a = addfile(str_concat(str),"r")
<   lt = a->LAT(:,:)
<   ln = a->LON(:,:)
<   u = a->O(0,0,:,:)  
<   u@lat2d = lt
<   u@lon2d = ln
< 
<   wks   = gsn_open_wks ("png", path )  ; send graphics to PNG file
---
>   cmaqfile = addfile("PM10.nc","r")
>   a = addfile("GRIDCRO2D_1804_run5.nc","r")
>   lt = a->LAT(0,0,:,:)
>   ln = a->LON(0,0,:,:)
> 
>   do t = 0,2 ;15 
>   pm10 = log10(cmaqfile->PM10(t,0,:,:))  
>   pm10@lat2d = lt
>   pm10@lon2d = ln
>   st=tostring_with_format(t,"%3.3d")
>   fname=str_concat((/"pm10",st/))
>   wks   = gsn_open_wks ("png", fname )  ; send graphics to PNG file
```

### 標題、界限

```bash
181c180
<   res@tiMainString   = str_concat((/"Trajectory Cluster from ",path/))
---
>   res@tiMainString   = "2018/3/31-4/8 PM10 Episode, Log10 ug/m3"
185,198c184,188
<   pth=(/"SH", "BJ", "BH", "SC", "SW", "LOCAL", "MC"/)
<   idx=get1Dindex(pth,path)
<   bds=(/(/20,40,100,130/),(/15,max(u@lat2d),105,135/),(/20,max(u@lat2d),110,135/),(/10,35,100,130/),\
< 	(/10,30,110,135/),(/24.8,25.5,120.8,122/),(/20,40,100,130/)/)
< ;  res@mpMinLatF            = min(u@lat2d)        ; zoom in on map
< ;  res@mpMaxLatF            = max(u@lat2d)
< ;  res@mpMinLonF            = min(u@lon2d)
< ;  res@mpMaxLonF            = max(u@lon2d)
<   res@mpMinLatF            = bds(idx,0);min(u@lat2d)        ; zoom in on map
<   res@mpMaxLatF            = bds(idx,1);max(u@lat2d)
<   res@mpMinLonF            = bds(idx,2);min(u@lon2d)
<   res@mpMaxLonF            = bds(idx,3);max(u@lon2d)
< 
<   res@cnLinesOn          = False        ; turn off contour lines
---
>   res@mpMinLatF            = min(pm10@lat2d)        ; zoom in on map
>   res@mpMaxLatF            = max(pm10@lat2d)
>   res@mpMinLonF            = 60;min(pm10@lon2d)
>   res@mpMaxLonF            = max(pm10@lon2d)
```

### 等值界線的劃分方式與底圖

```bash
>   res@cnLevels           = (/-1,-0.5,0,0.5,1,1.5,2,2.5,3/)
200,218c190,195
<   if (path .eq. "LOCAL") then
<     res@mpOutlineOn           = False
<     filename="/nas1/backup/data/cwb/e-service/btraj_WRFnests/ncl_scripts/shp/TWN_COUNTY.shp"
<     res@cnLevels    = (/0.001, .002,.003,.004, .005, 0.01,.1/);(/0.001, .005, 0.01,.02,.03,.04, .05, .06,.07,.08,.09,0.1/)   ; set levels
<     res@pmTickMarkDisplayMode = "Always"            ; turn on built-in tickmarks
<   else
<     res@mpDataBaseVersion       = "MediumRes"
<     res@mpDataSetName           = "Earth..4"
<     res@mpAreaMaskingOn         = True
<     res@mpOutlineBoundarySets = "National"
<     res@mpMaskAreaSpecifiers    = (/"China","Taiwan","Disputed area between India and China","India:Arunachal Pradesh"/)
<     filename="/nas1/backup/data/cwb/e-service/btraj_WRFnests/ncl_scripts/shp/bou2_4p.shp"
<     res@cnLevels    = (/0.001, 0.01, 0.1,.12,.14,.16, .18, 0.2, 0.5,1,1.5,2/)   ; set levels
<   end if
< ;read the polylines segments
<   lonlat=asciiread(str_concat((/path,".csv"/)),(/10,3/),"float")
<   gres                  = True                ; polyline mods desired
<   gres@gsLineThicknessF = 4.0                 ; line thickness
<   gres@gsLineColor      = "Red"               ; line color 
---
>   res@cnLinesOn          = False        ; turn off contour lines
>   res@mpDataBaseVersion       = "MediumRes"
>   res@mpDataSetName           = "Earth..4"
>   res@mpAreaMaskingOn         = True
>   res@mpOutlineBoundarySets = "National"
>   res@mpMaskAreaSpecifiers    = (/"China","Taiwan","Disputed area between India and China","India:Arunachal Pradesh"/)
```

### 輸出圖形

```bash
220,221c197,198
<   plot = gsn_csm_contour_map(wks, u, res)   
<   gsn_polyline (wks, plot, lonlat(:,0), lonlat(:,1), gres)
---
>   filename="bou2_4p.shp"
>   plot = gsn_csm_contour_map(wks, pm10, res)   
233c210
```

## 富貴角與金門反軌跡NCL程式差異

- 經調整後2者有相同的邊界與等值界線劃分

### 邊界調整

```bash
kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
$ diff ./kmean_FG123/terr.ncl ./kmean_JM123/terr.ncl
188,192c188,192
< 	(/10,30,110,135/),(/24.8,25.5,120.8,122/),(/20,40,100,130/)/)
< ;  res@mpMinLatF            = min(u@lat2d)        ; zoom in on map
< ;  res@mpMaxLatF            = max(u@lat2d)
< ;  res@mpMinLonF            = min(u@lon2d)
< ;  res@mpMaxLonF            = max(u@lon2d)
---
> 	(/10,30,110,135/),(/24.3,25,117.8,118.7/),(/20,40,100,130/)/)
>   res@mpMinLatF            = min(u@lat2d)        ; zoom in on map
>   res@mpMaxLatF            = max(u@lat2d)
>   res@mpMinLonF            = min(u@lon2d)
>   res@mpMaxLonF            = max(u@lon2d)
```

### 機率值界線調整

```bash
202,204c204
<     filename="/nas1/backup/data/cwb/e-service/btraj_WRFnests/ncl_scripts/shp/TWN_COUNTY.shp"
<     res@cnLevels    = (/0.001, .002,.003,.004, .005, 0.01,.1/);(/0.001, .005, 0.01,.02,.03,.04, .05, .06,.07,.08,.09,0.1/)   ; set levels
---
>     res@cnLevels    = (/0.001, .002,.003,.004, .005, 0.01,.1/)   ; set levels
```