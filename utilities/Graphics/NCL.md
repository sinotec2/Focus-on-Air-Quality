---
layout: default
title:  NCL Programs
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-02-05 09:43:40
---

# NCL Programs
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
- NCL([NCAR Command Language](https://www.ncl.ucar.edu/))是美國大氣研究中心出台的繪圖軟體，目前已經出到6.6.2版。
- 雖然NCL也會持續維護，然而自2019年開始，NCAR開始將系統陸續[轉到python平台](https://www.ncl.ucar.edu/Document/Pivot_to_Python/faq.shtml)上，6.6.2版之上將不會發展新的功能。
- 由於NCL的圖面已為各大期刊所熟識，其解析度、正確性及品質也受到肯定，因此許多程式仍然繼續沿用。
- 此處介紹CMAQ結果GIF之製作方式，以做為範例。

## 程式說明
### 引用模版及副程式
- 模版程式：coneff_18.ncl
- 副程式
  - 
### 程式碼

```bash
kuang@114-32-164-198 ~/NCL_scripts/contour_with_basemap
$ cat pm10.ncl
;----------------------------------------------------------------------
; coneff_18.ncl
;
; Concepts illustrated:
;   - Using functions for cleaner code
;   - Setting contour line thicknesses and patterns
;   - Using "setvalues" to set resource values
;   - Using "getvalues" to retrieve resource values
;   - Drawing partially transparent filled contours
;----------------------------------------------------------------------
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;----------------------------------------------------------------------

;----------------------------------------------------------------------
; Main code
;----------------------------------------------------------------------
begin
cmap = read_colormap_file("OceanLakeLandSnow")


;---Read data file and open workstation
  cmaqfile = addfile("PM10.nc","r")
  a = addfile("GRIDCRO2D_1804_run5.nc","r")
  lt = a->LAT(0,0,:,:)
  ln = a->LON(0,0,:,:)

  do t = 0,215 
  pm10 = log10(cmaqfile->PM10(t,0,:,:))  
  pm10@lat2d = lt
  pm10@lon2d = ln
  st=tostring_with_format(t,"%3.3d")
  fname=str_concat((/"pm10",st/))
  wks   = gsn_open_wks ("png", fname )  ; send graphics to PNG file

;---Set plot resources
  res                = True 
  res@gsnMaximize    = True
  res@cnFillOn       = True
  res@mpFillOn       = False
  res@cnFillPalette      = cmap(2:,:)
  res@tiMainString = "Default plot"

;---Recreate plot but with contours more opaque
  res@gsnDraw        = False    ; Don\'t draw plot or
  res@gsnFrame       = False    ;   advance frame
  res@cnFillOpacityF = 0.5
  res@tiMainString   = "2018/3/31-4/8 PM10 Episode, Log10 ug/m3"
; res@gsnCenterStringFontHeightF = 0.2
  res@gsnLeftStringFontHeightF=0.01
  res@gsnRightStringFontHeightF=0.01
  res@mpMinLatF            = min(pm10@lat2d)        ; zoom in on map
  res@mpMaxLatF            = max(pm10@lat2d)
  res@mpMinLonF            = 60;min(pm10@lon2d)
  res@mpMaxLonF            = max(pm10@lon2d)
  res@cnLevels           = (/-1,-0.5,0,0.5,1,1.5,2,2.5,3/)
  res@cnLevelSelectionMode = "ExplicitLevels"   ; set explicit contour levels
  res@cnLinesOn          = False        ; turn off contour lines
  res@mpDataBaseVersion       = "MediumRes"
  res@mpDataSetName           = "Earth..4"
  res@mpAreaMaskingOn         = True
  res@mpOutlineBoundarySets = "National"
  res@mpMaskAreaSpecifiers    = (/"China","Taiwan","Disputed area between India and China","India:Arunachal Pradesh"/)

  filename="bou2_4p.shp"
  plot = gsn_csm_contour_map(wks, pm10, res)   

  res@gsLineColor      = "blue"
  res@gsLineThicknessF = 1
  dum  = gsn_add_shapefile_polylines(wks,plot,filename,True)

  draw(plot)
  frame(wks)
end do
end
```

## Reference
- Mohit Kaushik, **Reading and Visualizing GeoTiff | Satellite Images with Python**, [towardsdatascience](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510),Aug 2, 2020
- Mapbox Revision, **Rasterio: access to geospatial raster data**, [readthedocs](https://rasterio.readthedocs.io/en/latest/), 2018
- Chimin, **Day26 網格資料的處理-Rasterio初探**, [ithome](https://ithelp.ithome.com.tw/articles/10209222)2018-11-10 21:56:37