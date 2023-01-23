kuang@125-229-149-182 /Users/Data/cwb/e-service/btraj_WRFnests
$ cat ./kmean_FG123/terr.ncl
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
; Function that retrieves contour levels from a plot and changes the
; the requested contour levels to the requested patterns.
;
; This code is somewhat complicated because we are checking to make
; sure we don't override any line patterns that might have 
; originally been set by the user.
;
; This code is very similar to the set_contour_line_thicknesses code.
;----------------------------------------------------------------------
undef("set_contour_line_patterns")
procedure set_contour_line_patterns(plot,levels_to_change[*]:numeric,\
                                    patterns[*]:integer)
local ii, levels, nlevels, line_patterns, nchange, ncolor, n, \
      mono_pattern, line_pattern, changed_a_level
begin
;---Retrieve the original line patterns (or pattern) used for the plot.
  getvalues plot@contour
    "cnLevels"              : levels
    "cnLineDashPatterns"    : line_patterns
    "cnMonoLineDashPattern" : mono_pattern
    "cnLineDashPattern"     : line_pattern
  end getvalues

;----------------------------------------------------------------------
; If the original contour plot used a single dash pattern for
; all contour lines, then make sure we use that again for 
; any contour lines that are not being changed. Otherwise,
; we assume the user set an array of dash patterns, and
; we'll use those.
;----------------------------------------------------------------------

  if(mono_pattern) then
    line_patterns = line_pattern
  end if

  nlevels  = dimsizes(levels)
  nchange  = dimsizes(levels_to_change)
  npattern = dimsizes(patterns)

  if(npattern.ne.nchange) then
      print("set_contour_line_patterns: error: the contour line patterns must be an")
      print("array of the same length as the number of contour levels to change.")
  end if

;---Array to hold index values of contour levels that need to have a color applied
  changed_a_level = False
  do n=0,nchange-1
    ii := ind(levels.eq.levels_to_change(n))
    if(ismissing(ii(0))) then
      print("set_contour_line_patterns: warning, no contour level equal to " + levels_to_change(n))
    else
      line_patterns(ii(0)) = patterns(n)
      changed_a_level      = True
    end if   
  end do

  if(changed_a_level) then
    setvalues plot@contour
      "cnMonoLineDashPattern" : False             ; allows an array of line patterns to be set
      "cnLineDashPatterns"    : line_patterns
    end setvalues
  end if
end

;----------------------------------------------------------------------
; Function that retrieves contour levels from a plot and changes the
; the requested contour levels to the requested thicknesses.
;
; This code is somewhat complicated because we are checking to make
; sure we don't override any line thicknesses that might have 
; originally been set by the user.
;
; This code is very similar to the set_contour_line_patterns code.
;----------------------------------------------------------------------
undef("set_contour_line_thicknesses")
procedure set_contour_line_thicknesses(plot,levels_to_change[*]:numeric,\
                                       thicknesses[*]:numeric)
local ii, levels, nlevels, line_thicknesses, nchange, nthick, \
      mono_thickness, line_thickness,changed_a_level
begin
;---Retrieve the original line thicknesses (or thickness) used for the plot.
  getvalues plot@contour
    "cnLevels"            : levels
    "cnLineThicknesses"   : line_thicknesses
    "cnMonoLineThickness" : mono_thickness
    "cnLineThicknessF"    : line_thickness
  end getvalues
;----------------------------------------------------------------------
; If the original contour plot used a single dash line thickness
; all contour lines, then make sure we use that again for 
; any contour lines that are not being changed. Otherwise,
; we assume the user set an array of line thicknesses, and
; we'll use those.
;----------------------------------------------------------------------

;---Check user set line thicknesses, and apply new thicknesses if needed
  if(mono_thickness) then
    line_thicknesses = line_thickness
  end if

  nlevels = dimsizes(levels)
  nchange = dimsizes(levels_to_change)
  nthick  = dimsizes(thicknesses)

  if(nthick.ne.nchange) then
      print("set_contour_line_thicknesses: error: the contour line thicknesses must be an")
      print("array of the same length as the number of contour levels to change.")
  end if

;---Array to hold index values of contour levels that need to have a thickness applied
  changed_a_level = False
  do n=0,nchange-1
    ii := ind(levels.eq.levels_to_change(n))
    if(ismissing(ii(0))) then
      print("set_contour_line_thicknesses: warning, no contour level equal to " + levels_to_change(n))
    else
      line_thicknesses(ii(0)) = thicknesses(n)
      changed_a_level     = True
    end if   
  end do

  if(changed_a_level) then
    setvalues plot@contour
      "cnMonoLineThickness" : False             ; allows an array of line thicknesses to be set
      "cnLineThicknesses"   : line_thicknesses
    end setvalues
  end if
end


;----------------------------------------------------------------------
; Main code
;----------------------------------------------------------------------
begin
cmap = read_colormap_file("OceanLakeLandSnow")


;---Read data file and open workstation
  
; a = addfile("/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_27km.nc","r")
  str=(/"prob",path,".nc"/)
  a = addfile(str_concat(str),"r")
  lt = a->LAT(:,:)
  ln = a->LON(:,:)
  u = a->O(0,0,:,:)  
  u@lat2d = lt
  u@lon2d = ln
; u = smth9_Wrap(u, 0.3, 0.15, True) ;(.5,0.25) is heavy, (0.1,0.05) is no smooth
;  data = generate_2d_array(15, 20, 0., 80., 0, (/59,59/))

  wks   = gsn_open_wks ("png", path )  ; send graphics to PNG file

;---Set plot resources
  res                = True 
  res@gsnMaximize    = True
  res@cnFillOn       = True
  res@mpFillOn       = False
  res@cnFillPalette      = cmap(2:,:)
  res@tiMainString = "Default plot"

;---Recreate plot but with contours more opaque
  res@gsnDraw        = False    ; Don't draw plot or
  res@gsnFrame       = False    ;   advance frame
  res@cnFillOpacityF = 0.5
  res@tiMainString   = str_concat((/"Trajectory Cluster from ",path/))
; res@gsnCenterStringFontHeightF = 0.2
  res@gsnLeftStringFontHeightF=0.01
  res@gsnRightStringFontHeightF=0.01
  pth=(/"SH", "BJ", "BH", "SC", "SW", "LOCAL", "MC"/)
  idx=get1Dindex(pth,path)
  bds=(/(/20,40,100,130/),(/15,max(u@lat2d),105,135/),(/20,max(u@lat2d),110,135/),(/10,35,100,130/),\
	(/10,30,110,135/),(/24.8,25.5,120.8,122/),(/20,40,100,130/)/)
;  res@mpMinLatF            = min(u@lat2d)        ; zoom in on map
;  res@mpMaxLatF            = max(u@lat2d)
;  res@mpMinLonF            = min(u@lon2d)
;  res@mpMaxLonF            = max(u@lon2d)
  res@mpMinLatF            = bds(idx,0);min(u@lat2d)        ; zoom in on map
  res@mpMaxLatF            = bds(idx,1);max(u@lat2d)
  res@mpMinLonF            = bds(idx,2);min(u@lon2d)
  res@mpMaxLonF            = bds(idx,3);max(u@lon2d)

  res@cnLinesOn          = False        ; turn off contour lines
  res@cnLevelSelectionMode = "ExplicitLevels"   ; set explicit contour levels
  if (path .eq. "LOCAL") then
    res@mpOutlineOn           = False
    filename="/nas1/backup/data/cwb/e-service/btraj_WRFnests/ncl_scripts/shp/TWN_COUNTY.shp"
    res@cnLevels    = (/0.001, .002,.003,.004, .005, 0.01,.1/);(/0.001, .005, 0.01,.02,.03,.04, .05, .06,.07,.08,.09,0.1/)   ; set levels
    res@pmTickMarkDisplayMode = "Always"            ; turn on built-in tickmarks
  else
    res@mpDataBaseVersion       = "MediumRes"
    res@mpDataSetName           = "Earth..4"
    res@mpAreaMaskingOn         = True
    res@mpOutlineBoundarySets = "National"
    res@mpMaskAreaSpecifiers    = (/"China","Taiwan","Disputed area between India and China","India:Arunachal Pradesh"/)
    filename="/nas1/backup/data/cwb/e-service/btraj_WRFnests/ncl_scripts/shp/bou2_4p.shp"
    res@cnLevels    = (/0.001, 0.01, 0.1,.12,.14,.16, .18, 0.2, 0.5,1,1.5,2/)   ; set levels
  end if
;read the polylines segments
  lonlat=asciiread(str_concat((/path,".csv"/)),(/10,3/),"float")
  gres                  = True                ; polyline mods desired
  gres@gsLineThicknessF = 4.0                 ; line thickness
  gres@gsLineColor      = "Red"               ; line color 

  plot = gsn_csm_contour_map(wks, u, res)   
  gsn_polyline (wks, plot, lonlat(:,0), lonlat(:,1), gres)

  res@gsLineColor      = "blue"
  res@gsLineThicknessF = 1
  dum  = gsn_add_shapefile_polylines(wks,plot,filename,True)

;---Change some line thicknesses and patterns and redraw the plot
;  set_contour_line_thicknesses(plot,(/20,24,28,32/),(/2.,3.5,2.,7.5/))
;  set_contour_line_patterns(plot,(/20,28/),(/2,10/))

  draw(plot)
  frame(wks)

end
