;----------------------------------------------------------------------
; wrf_gsn_8.ncl
;----------------------------------------------------------------------
; Concepts illustrated:
;   - Using gsn_csm scripts to plot WRF-ARW data
;   - Drawing streamlines colored by another field over a map
;   - Setting the correct WRF map projection using wrf_map_resources
;   - Subsetting a color map
;   - Using stLevelPalette resource to assign a color palette
;   - Using opacity to emphasize or subdue overlain features
;   - Increasing the thickness of map outlines
;----------------------------------------------------------------------
; This script is meant to show the difference between plotting WRF
; data using wrf_xxx scripts, and using gsn_csm_xxx scripts.
;
; The first plot draws the streamlines in a basic lat/lon map
; projection.
;
; The second plot draws the streamlines in the native projection
; provided on the WRF file.
;----------------------------------------------------------------------
; In NCL Versions 6.3.1 and earlier, you will get these warnings which
; you can safely ignore:
;
;   warning:start_lat is not a valid resource in wrf_gsn_streamline at this time
;   warning:start_lon is not a valid resource in wrf_gsn_streamline at this time
;   warning:end_lat is not a valid resource in wrf_gsn_streamline at this time
;   warning:end_lon is not a valid resource in wrf_gsn_streamline at this time
;   warning:mpNestTime is not a valid resource in map at this time
;----------------------------------------------------------------------
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin
;---Open WRF output file
  filename = "wrfout"
  a        = addfile(filename,"r")

;---Read several WRF variables at first time step
  it  = 0
  uu10 = wrf_user_getvar(a,"U10",it)
  vv10 = wrf_user_getvar(a,"V10",it)
  lat1 = wrf_user_getvar(a,"lat",it)
  lon1 = wrf_user_getvar(a,"lon",it)

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

  Times = wrf_user_getvar(a,"Times",it)
  print(tostring(Times))
;---Get the lowest (bottommost) level
  nl  = 0
  u10 = u10*1.94386                    ; Convert wind into knots
  v10 = v10*1.94386                    ; Convert wind into knots
  spd = sqrt(u10^2+v10^2)

;---Change the metadata
  u10@units       = "kts"
  v10@units       = "kts"

;---Required for plotting over map (not using WRF's map projection here)
  u10@lat2d = lat
  u10@lon2d = lon
  v10@lat2d = lat
  v10@lon2d = lon

  wks = gsn_open_wks("png","wrf_gsn")
  res                    = True
  res@gsnMaximize        = True
  res@mpMinLatF          = min(lat)-1
  res@mpMaxLatF          = max(lat)+1
  res@mpMinLonF          = min(lon)-1
  res@mpMaxLonF          = max(lon)+1
  res@stLineThicknessF   = 2.0
  res@tiMainString       = tostring(Times)
  res@tiMainFontHeightF  = 0.015
  res@mpFillOn           = False
  res@mpDataBaseVersion  = "MediumRes"    ; better map outlines
  res@gsnAddCyclic       = False          ; don't add longitude cyclic point
  res@stLineOpacityF     = 1.0       ; make streamlines more transparent
;
; We like the "NCV_rainbow2" colormap, but don't want to use the
; whole thing. Use read_colormap_file to read the colormap as
; an N x 4 array, and then subscript as desired.  Here we are
; starting at color 19 and ending at color 240. Uncomment the
; draw_color_palette call if you want to see what this colormap
; looks like.
;
;  draw_color_palette(wks,"NCV_rainbow2",0)

  colormap = read_colormap_file("NCV_rainbow2")
  res@stLevelPalette = colormap(19:240,:)

;---Plot streamlines in a basic lat/lon projection (cylindrical equidistant)
  ;plot = gsn_csm_streamline_scalar_map(wks,u10,v10,spd,res)

;---Plot strealines in the native WRF map projection
  delete([/u10@lat2d,u10@lon2d,v10@lat2d,v10@lon2d/])   ; This is important! Don't use lat/lon arrays for
                                                        ; native projections

;---Set the map resources needed for native projection
  res = wrf_map_resources(a,res)
  res@tfDoNDCOverlay   = True          ; Tell NCL you are doing a native plot
; res@tfDoNDCOverlay   = "NDCViewport" ; can use this in NCL V6.5.0 or later

  res@tiMainString     = tostring(Times) ;"U10/V10 streamlines colored by wind speed (native WRF projection)"
  res@stLineOpacityF     = 0.5       ; make streamlines more transparent
  ;plot = gsn_csm_streamline_scalar_map(wks,u10,v10,spd,res)

;---Customize the some resources so we can see map outlines better
  res@stLineOpacityF              = 0.8       ; make streamlines more transparent
  res@mpUSStateLineColor          = "black"
  res@mpNationalLineColor         = "black"
  res@mpGeophysicalLineColor      = "black"
  res@mpUSStateLineThicknessF     = 2.        ; default is 1.0
  res@mpNationalLineThicknessF    = 2.
  res@mpGeophysicalLineThicknessF = 2.
  res@lbTitleString    = "unit: knots"
  res@lbTitleFontHeightF= .01
  res@pmLabelBarOrthogonalPosF = .10
  plot = gsn_csm_streamline_scalar_map(wks,u10,v10,spd,res)
end
