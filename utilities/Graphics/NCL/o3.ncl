;kuang@master ~/NCL_scripts/rcm_2
;$ cat o3.ncl
;*******************************************
; rcm_2.ncl
;
; Concepts illustrated:
;   - Plotting RCM data
;   - Plotting Cray binary data
;   - Drawing filled contours over a Lambert Conformal map
;   - Drawing U.S. states
;   - Adding units and long_name attributes to get subtitles
;*******************************************
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
;********************************************
begin

  fmet = "/nas1/cmaqruns/2016base/data/mcip/1601_run5/TWN_3X3/GRIDCRO2D_1601_run5.nc"
  met   =  addfile(fmet ,"r")
  fname = "/nas1/cmaqruns/2016base/data/output_CCTM_v53_gcc_1610/POST/ENKF/COMBINE_ACONC_v53_gcc_1610_run9_20161020_TWN_3X3_10.nc"
  f     =  addfile(fname ,"r")

  lat2d       =  met->LAT(0,0,:,:)
  lon2d       =  met->LON(0,0,:,:)
  nlat        =  dimsizes(lat2d(:,0))
  nlon        =  dimsizes(lon2d(0,:))
  var         =  f->O3(5,0,:,:)
  var@lat2d   =  lat2d
  var@lon2d   =  lon2d
; read the station observations(1d)
  csv_cont=asciiread("EPA_ALL2016102013.csv",-1,"float")
  nrec=dimsizes(csv_cont)
  nstat=toint(nrec/3)
  O31d=new(nstat,float)
  lat1d=new(nstat,float)
  lon1d=new(nstat,float)
  do i = 0, nrec-1, 3
    ii=toint(i/3)
    lat1d(ii)=csv_cont(i)
    lon1d(ii)=csv_cont(i+1)
    O31d(ii)=csv_cont(i+2)
  end do

  nlev = 15
   num_distinct_markers = nlev+1
   levels = new((/num_distinct_markers/),float,-999)
   div = max(O31d) / nlev
   do i = 0, nlev
     levels(i) = i * div
   end do

   var=var*(max(O31d)/max(var))

;********************************
; plot
;********************************
   wks_type = "png"
   wks_type@wkWidth = 5000
   wks_type@wkHeight = 5000
   wks = gsn_open_wks(wks_type,"rcm")
   cmap = read_colormap_file("gui_default") ; read color data
   nclr=dimsizes(cmap(:,0))
   intv=toint(nclr/nlev)
   res                 = True                    ; plot mods desired
   res@cnLinesOn       = False
   res@cnFillOn        = True               ; color plot desired
   res@cnFillPalette   = cmap(:nclr-1:intv,:)        ; set color map
   res@cnLineLabelsOn  = False              ; turn off contour lines

; !!!!! any plot of data that is on a native grid, must use the "corners"
; method of zooming in on map.

   res@mpLimitMode       = "Corners"            ; choose range of map
   res@mpLeftCornerLatF  = lat2d(0,0)
   res@mpLeftCornerLonF  = lon2d(0,0)
   res@mpRightCornerLatF = lat2d(nlat-1,nlon-1)
   res@mpRightCornerLonF = lon2d(nlat-1,nlon-1)

; The following 4 pieces of information are REQUIRED to properly display
; data on a native lambert conformal grid.  This data should be specified
; somewhere in the model itself.

; WARNING: our local RCM users could not provide us with this information,
; so this is our best guess as to the correct numbers. Use at your own risk.

   res@mpProjection        = "LambertConformal"
   res@mpLambertParallel1F = 10
   res@mpLambertParallel2F = 40
   res@mpLambertMeridianF  = 120.99
;
; usually, when data is placed onto a map, it is TRANSFORMED to the specified
; projection. Since this model is already on a native lambert conformal grid,
; we want to turn OFF the transformation.
;
;  res@tfDoNDCOverlay        = True
 res@tfDoNDCOverlay        = "NDCViewport"  ; NCL V6.5.0 or later


   res@mpOutlineBoundarySets  = False                   ; draw box around map
   res@mpPerimOn              = True                    ; draw box around map
   res@mpGridLineDashPattern  = 2                       ; lat/lon lines as dashed
  res@pmTickMarkDisplayMode       = "Always"   ; Nicer map labels
  res@tmXTOn = False
  res@tmYROn = False
  res@lbOrientation        = "vertical"


; to take advantage of NCL's automatic labeling, we need to assign som attributes:

   shapefile_dir  = "/home/kuang/NCL_scripts/shapes/"       ;-- directory containing the shapefiles
   shp_name2      = "COUNTY_MOI_1090820.shp"                         ;-- shapefile to be used
   shp_fname2      = shapefile_dir+shp_name2
   dumstr2       = unique_string("poly")
   map = gsn_csm_contour_map(wks,var,res)    ; Draw contours over a map.
   map@$dumstr2$ = gsn_add_shapefile_polylines(wks, map, shp_fname2, True)

  txres                        =  True
  txres@txJust                 = "BottomRight"
  txres@txFontHeightF          =  0.010
  str = "~F35~c ~F21~~N~SEC"
  gsn_text_ndc(wks,str, 0.95, 0.01, txres)


  nlevels = dimsizes(levels)
  colors  = span_color_rgba("gui_default",nlevels+1) ;"gui_default"
  npts = nstat
  lat_new = new((/num_distinct_markers,npts/),float,-999)
  lon_new = new((/num_distinct_markers,npts/),float,-999)
  R = O31d
  do i = 0, num_distinct_markers-1
    if (i.eq.0) then
      indexes = ind(R.lt.levels(0))
    end if
    if (i.eq.num_distinct_markers-1) then
      indexes = ind(R.ge.max(levels))
    end if
    if (i.gt.0.and.i.lt.num_distinct_markers-1) then
      indexes = ind(R.ge.levels(i-1).and.R.lt.levels(i))
    end if
    if (.not.any(ismissing(indexes))) then
      npts_range = dimsizes(indexes)   ; # of points in this range.
      lat_new(i,0:npts_range-1) = lat1d(indexes)
      lon_new(i,0:npts_range-1) = lon1d(indexes)
    end if
    delete(indexes)            ; Necessary b/c "indexes" may be a different
                               ; size next time.
  end do

;--Create logical variables to hold the marker resources.
  gsres               = True
  gsres@gsMarkerIndex = 16          ; Use filled dots for markers.
;
; Loop through each grouping of markers, and draw them one set at
; a time, assigning the proper color and size with gsn_marker.
;
  base_size = 0.008
  pmid = new(num_distinct_markers,graphic)
  do i = 0, num_distinct_markers-1
    if (.not.ismissing(lat_new(i,0)))
      gsres@gsMarkerColor      = colors(i,:)
      gsres@gsMarkerSizeF      = base_size ; * (i+1)/3.
      gsres@gsMarkerThicknessF = 0.7; *(i+1)
      pmid(i) = gsn_add_polymarker(wks,map,lon_new(i,:),lat_new(i,:),gsres)
    end if
  end do

  draw(map)
  frame(wks)


end
