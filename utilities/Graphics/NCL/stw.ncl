;kuang@node03 /nas2/cmaqruns/2019TZPP/output/Annual/aTZPP
;$ cat /var/www/html/taiwan/stw.ncl
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/esmf/ESMF_regridding.ncl"
load "add_shapefile_polygons.ncl"
load "add_shapefile_polylines.ncl"
load "avg_by_town.ncl"
begin
;-- which counties shoild be plotted, if assinged, subregion limits must be changed accordingly
;pingdong,tainan,gaoxiuong
  county_name = asciiread("counties.txt",-1,"string")


;-- 1d csv values are optional
  csv   =       True
  csv_cont=asciiread("input.csv",-1,"float")
  nre=dimsizes(csv_cont)
  ntowns=toint(nre/3)
  var1d=new(ntowns,float)
  countycode1d=new(ntowns,string)
  towncode1d=new(ntowns,string)
  do i = 0, nre-1, 3
    ii=toint(i/3)
    countycode1d(ii)=tostring_with_format(toint(csv_cont(i)), "%5.5d")
    b=tostring_with_format(toint(csv_cont(i+1)), "%3.3d")
    towncode1d(ii)=countycode1d(ii)+b
    var1d(ii)=csv_cont(i+2)
  end do
; print(countycode1d)
; print(towncode1d)
; print(var1d)
    var1_mn=min(var1d)
    var1_mx=max(var1d)
    var1_int = (var1_mx-var1_mn)/20
  countycode1d=new(ntowns,string)


;-- nc file may be used  for shaping only, if csv exists
  f     =  addfile("TWN_adm/tas1.nc","r")

  lat2d       =  f->lat
  lon2d       =  f->lon
  cnty2d      =  f->CNTY
  lat1d       =  tofloat(ndtooned(lat2d))
  lon1d       =  tofloat(ndtooned(lon2d))
  cnty1d      =  tostring_with_format(toint(ndtooned(cnty2d)), "%5.5d")
  nlat        =  dimsizes(lat2d(:,0))
  nlon        =  dimsizes(lon2d(0,:))
;  print(cnty1d)
;  print(lat1d)
  minlat=lat1d(dimsizes(cnty1d) - 1)
  minlon=lon1d(dimsizes(cnty1d) - 1)
  maxlat=lat1d(0)
  maxlon=lon1d(0)
  do i = 0, dimsizes(cnty1d) - 1
    do j = 0, dimsizes(county_name) - 1
          if (county_name(j) .eq. cnty1d(i)) then
;-- subregion for the coastal states
            if (minlat.gt.lat1d(i)) then
;         print(minlat)
;         print(lat1d(i))
              minlat=lat1d(i)
            end if
            if (maxlat.lt.lat1d(i)) then
              maxlat=lat1d(i)
            end if
            if (minlon.gt.lon1d(i)) then
              minlon=lon1d(i)
            end if
            if (maxlon.lt.lon1d(i)) then
              maxlon=lon1d(i)
            end if
          end if
        end do
  end do

  var         =  f->tas(0,:,:)
  var@lat2d   =  lat2d
  var@lon2d   =  lon2d

;-- set variable minimum and maximum values and its increment
  vmin = min(var)
  vmax = max(var)
  vint = (vmax-vmin)/20.

;-- normalized by var1d if csv exists
  var =  (var-vmin)/(vmax-vmin) * (var1_mx-var1_mn) + var1_mn
        vmin = min(var)
        vmax = max(var)
        vint = (vmax-vmin)/20.

;-- convert first time step to utc calandar time string
  year     = 2020
  mon      = 2
  day      = 6
  hr       = 0
  minute   = 0
  second   = 0
  ptime    = sprinti("%0.4i", year) + "-" + sprinti("%0.2i", mon) + "-" + sprinti("%0.2i", day) + \
             "-" + sprinti("%0.2i", hr) + ":" + sprinti("%0.2i", minute) + ":" + sprinti("%0.2i", second)


;-- initial settings
  states_border  =  True      ;-- True: draw state borderlines
  subregion      =  True      ;-- True: use a subregion
  country_border =  True      ;-- True: draw country borderlines
  use_black_bg   =  False     ;-- True: use grey18/black background and white foreground color

;-- shapefile containing counties and towns
  shapefile_dir  = "./TWN_adm/"       ;-- directory containing the shapefiles
  shp_name2      = "COUNTY_MOI_1090820.shp"                         ;-- shapefile to be used
  shp_name3      = "TOWN_MOI_1090727.shp"                         ;-- shapefile to be used
  shp_fname2      = shapefile_dir+shp_name2                ;-- path of shapefile
  shp_fname3      = shapefile_dir+shp_name3                ;-- path of shapefile
  shpf2          = addfile(shp_fname2,"r")                 ;-- open shapefile
  shpf3          = addfile(shp_fname3,"r")                 ;-- open shapefile
  shp_content    = "towns"                             ;-- what's in the shapefile
  town_names     = tostring_with_format(toint(shpf3->TOWNCODE),"%8.8d")                        ;-- town names
  counties       = shpf3->COUNTYCODE                      ;-- state names
  shplon         = shpf3->x                               ;-- longitudes
  shplat         = shpf3->y                               ;-- latitudes

;-- store shapefile names to array
  print("")
  print("Counties:   "+county_name)
  print("")
  print("Shapefile:  "+shp_name3+"  ("+ shp_content+ ")")
  print("")

;-- Germany borderline coordinates
  TWN_minlat     =  min(shplat)-0.1
  TWN_maxlat     =  max(shplat)+0.1
  TWN_minlon     =  min(shplon)-0.1
  TWN_maxlon     =  max(shplon)+0.1
  print("TWN_minlat = "+sprintf("%7.4f",TWN_minlat)+"  TWN_maxlat = "+sprintf("%7.4f",TWN_maxlat))
  print("TWN_minlon = "+sprintf("%7.4f",TWN_minlon)+"  TWN_maxlon = "+sprintf("%7.4f",TWN_maxlon))
  if(subregion) then
     print("")
     print("Use sub-region: ")
     print("minlat     = "+sprintf("%7.4f",minlat)+    "  maxlat     = "+sprintf("%7.4f",maxlat))
     print("minlon     = "+sprintf("%7.4f",minlon)+    "  maxlon     = "+sprintf("%7.4f",maxlon))
  end if

;-- set ESMF regrid resources
  Opt                     =  True
  Opt@InterpMethod        = "bilinear"
  Opt@SrcFileName         = "TWN_adm/TWNd4_SCRIP_bilinear.nc"              ;-- source file name
  Opt@DstFileName         = "TWNd4_SCRIP_bilinear3.nc"       ;-- destination file name
  Opt@WgtFileName         = "TWNd4_SCRIP_bilinear4.nc"  ;-- name of weights file, which will be generated
  Opt@ForceOverwrite      =  True
  Opt@DstGridType         = "0.11deg"                              ;-- Destination grid
  Opt@DstTitle            = "CORDEX EUR-11 unrotated"
  Opt@DstLLCorner         =  (/minlat,minlon/)
  Opt@DstURCorner         =  (/maxlat,maxlon/)
  Opt@SrcRegional         =  True
  Opt@DstRegional         =  True

;-- if we don't need to generate the source and destination grids again
;  Opt@SkipDstGrid         =  True
;  Opt@SkipSrcGrid         =  True

;-- interpolate data from CMIP5 to Worl 1x1 degree grid
  var_regrid = ESMF_regrid(var,Opt)


;-- open workstation
  wks_type                     = "png"
;  wks_type@wkOrientation       = "landscape"
  if(use_black_bg) then
     wks_type@wkBackgroundColor   = "grey18"
     wks_type@wkForegroundColor   = "white"
  end if
  wks  = gsn_open_wks(wks_type, "shapefile_3")

;-- global resources
  res                        =  True
  res@gsnDraw                =  False
  res@gsnFrame               =  False
  res@gsnAddCyclic           =  False
  res@gsnRightString         =  "(unit)" ;"["+var@units+"]"
  res@gsnRightStringFontHeightF    =  0.013
  res@gsnRightStringParallelPosF   =  1.12
  res@gsnRightStringOrthogonalPosF = -0.007
  res@gsnLeftString          = ""

  res@vpXF                   =  0.05                    ;left origins
  res@vpYF                   =  0.95                    ;top location
  res@vpWidthF               =  0.8
  res@vpHeightF              =  0.8
; res@mpDataBaseVersion      = "HighRes"              ;-- use HighRes map
; res@mpDataResolution       = "Fine"                 ;-- we need a finer resolution
; res@mpProjection           = "Mercator"             ;-- use Mercator projection
  res@mpLimitMode            = "Corners"              ;-- map limit mode
  if(isvar("subregion")) then                         ;-- is 'subregion' on command line?
     res@mpLeftCornerLatF    =  minlat-0.2            ;-- min lat
     res@mpRightCornerLatF   =  maxlat+0.2            ;-- max lat
     res@mpLeftCornerLonF    =  minlon-0.2            ;-- min lon
     res@mpRightCornerLonF   =  maxlon+0.2            ;-- max lon
  else
     res@mpLeftCornerLatF    =  TWN_minlat            ;-- min lat
     res@mpRightCornerLatF   =  TWN_maxlat            ;-- max lat
     res@mpLeftCornerLonF    =  TWN_minlon            ;-- min lon
     res@mpRightCornerLonF   =  TWN_maxlon            ;-- max lon
  end if
  res@mpCenterLatF           =  ((minlat + maxlat)*0.5)
  res@mpCenterLonF           =  ((minlon + maxlon)*0.5)
  res@mpPerimOn              =  True                    ;turns on a line that is drawn around the perimeter of the map
  res@mpGridLineColor        = "grey40"
  res@mpGridAndLimbOn        =  True
  res@mpGridLatSpacingF      =  0.2
  res@mpGridLonSpacingF      =  0.2
  res@mpFillOn               =  False
  res@mpOutlineOn            =  False
  res@mpGeophysicalLineColor =  "black"
  res@mpOceanFillColor       = (/ 0.824, 0.961, 1.0 /)
  res@mpInlandWaterFillColor = (/ 0.824, 0.961, 1.0 /)
; res@mpLandFillColor        = (/ 0.7, 0.7, 0.7 /)

  res@cnFillOn               =  True                 ;-- turn on color
  res@cnMissingValFillColor  = -1                    ;-- set to transparent
  res@cnLinesOn              =  False                ;-- no contour lines
  res@cnLineLabelsOn         =  False                ;-- no contour labels
  res@cnLevelSelectionMode   = "ManualLevels"        ;-- set contour levels manually
  res@cnMinLevelValF         =  vmin                 ;-- minimum contour level
  res@cnMaxLevelValF         =  vmax                 ;-- maximum contour level
  res@cnLevelSpacingF        =  vint                 ;-- contour level spacing
  res@cnFillPalette          = "BkBlAqGrYeOrReViWh200"

  res@tiXAxisString          = ""
  res@tiYAxisString          = ""

  res@trYReverse             =  True
  res@tfDoNDCOverlay         =  True                 ;-- transform to standard lat/lon
  res@trGridType             = "TriangularMesh"

  res@lbOrientation          = "vertical"
  res@lbLabelFontHeightF     =  0.013
;  res@pmLabelBarParallelPosF = 0.1
  res@pmLabelBarOrthogonalPosF = -0.015
  res@lbBoxMinorExtentF      =  0.2


;-- create contour data plot
  plot = gsn_csm_contour_map(wks,var_regrid,res)

;-- this gives us the colors and levels to use for the filled polygons
;  getvalues plot@contour
;    "cnLevels"               : levels               ;-- retrieve levels
;     "cnFillColors"           : colors               ;-- retrieve colors
;     "cnInfoLabelFontHeightF" : font_h               ;-- retrieve font height
;  end getvalues
  colors=(/2130706432,2130706524, 2130706626, 2130714623, 2130740735, 2130764031, 2130897596, 2131086949, 2131932686, 2137772297, \
                   2144268291,2147479552, 2147470080, 2147461376, 2147445248, 2147429888, 2146107408, 2142109761, 2137718904, 2139045285, \
                   2143527892,2147483647/)
  font_h                                         =      0.01830624
  levels=new(21,float)
  diffE=abs(log10(abs(var1_mx))-log10(abs(var1_mn)))
  if (diffE.le.1) then
    do i=0,20
      levels(i)=var1_mn+var1_int*i
    end do
  else
    x=var1d
    ip = dim_pqsort(x, 2)
    if (ntowns .gt. 20) then
      nint=toint(ntowns/20)
      do i=0,20
        ii=i*nint
        levels(i)=x(ii)
      end do
    else
      do i=0,ntowns-1
        levels(i)=x(i)
      end do
    end if
    a=tostring_with_format(levels, "%12.3g")
    levels=tofloat(a)
    print(levels)
  end if

  res@lbLabelStrings       = sprintf("%12.3g",levels)   ; Format the labels
  plot = gsn_csm_contour_map(wks,var_regrid,res)

;-- clear the contour plot, but hold the map to attach the polygons, polylines, labelbar and text
  map = setColorContourClear(plot,min(var),max(var))

;-- loop over selected counties
  wc1      = new(dimsizes(town_names),typeof(town_names)) ;-- assign arra"y for the selected counties
  col_avg1 = new(dimsizes(wc1),integer)               ;-- assign new color map

  do k=0,dimsizes(county_name)-1
     wc1 := new(dimsizes(town_names),typeof(town_names))     ;-- assign array for the selected counties
     if(.not.isatt(wc1,"_FillValue")) then
        wc1@_FillValue = default_fillvalue(typeof(town_names)) ;-- make sure "wc" has a missing value
     end if
     n=0
     do m=0,dimsizes(town_names)-1
        if(counties(m).eq.county_name(k)) then
           wc1(n) = town_names(m)                             ;-- get counties of the state
        else
           wc1(n) = default_fillvalue(typeof(town_names))   ;-- set other counties to missing value
        end if
        n=n+1
     end do
     wtowns1 := ind(.not. ismissing(wc1))                     ;-- indices of towns
;-- calculate the averages
     var_avg1 = avg_by_town(wks, map, var_regrid, shpf3, county_name(k), wtowns1, levels, colors)
     print("--------------------------------------------------")
     print("Data values: " + num(.not. ismissing(var_avg1))+ "  Missing values: " + num(ismissing(var_avg1)))
     print("--------------------------------------------------")

;-- get the correct color indices for the averaged data
    col_avg1 := new(dimsizes(wc1),integer)                      ;-- assign new color map
    col_avg1 = -1
    if (csv) then
     do ii=0,dimsizes(wtowns1)-1
        i=wtowns1(ii)
          n=-1
          do jj=0,dimsizes(towncode1d)-1
            if(towncode1d(jj).eq.wc1(i))then
              n=jj
            end if
          end do
                  if (n .gt. -1) then
            do j=0,dimsizes(levels)-1
               if(var1d(n).ge.levels(j)) then
                   col_avg1(i) = colors(j) ;-- values in between
               end if
            end do
                 else
                          print (wc1(i))
         end if
     end do
    else
     do i=0,dimsizes(wc1)-1
        if(ismissing(var_avg1(i))) then
           col_avg1(i) = -1                                      ;-- set to transparent
        else
            do j=0,dimsizes(levels)-1
               if (var_avg1(i).lt.levels(0)) then
                   col_avg1(i) = colors(0)                         ;-- values less than min(levels)
               else if(var_avg1(i).ge.levels(dimsizes(levels)-1)) then
                   col_avg1(i) = colors(dimsizes(colors)-1)        ;-- values greater than max(levels)
               else if(var_avg1(i).ge.levels(j).and.var_avg1(i).lt.levels(j+1)) then
                   col_avg1(i) = colors(j+1)                       ;-- values in between
               end if
               end if
               end if
            end do
        end if
     end do
    end if

     print("--------------------------------------------------")

;-- draw only the colored data averages in the towns polygons and the town polylines of selected counties
     dumstr       = unique_string("poly")
     map@$dumstr$ = add_shapefile_polygons(wks, map, county_name(k), col_avg1, shpf3, True)
     dumstrl       = unique_string("poly")
     map@$dumstrl$ = add_shapefile_polylines(wks, map, county_name(k), col_avg1, shpf3, True)
     dumstr2       = unique_string("poly")
     map@$dumstr2$ = gsn_add_shapefile_polylines(wks, map, shp_fname2, True)

;-- free memory
     delete(var_avg1)
     delete(col_avg1)
     delete(wc1)
     delete(wtowns1)


  end do
;-- draw title strings
  str0 = f@project_id+"  "+f@CORDEX_domain+":"
  txres                        =  True
  txres@txFont                 =  22             ;-- text font "helvetica-bold"
  txres@txFontHeightF          =  0.020
  txres@txJust                 = "BottomLeft"
;  gsn_text_ndc(wks, str0, 0.05, 0.96, txres)

  main_title = "Mean Temperature Change"
  txres@txFontHeightF          =  0.018
  txres@txJust                 = "BottomLeft"
;  gsn_text_ndc(wks, main_title, 0.05, 0.925, txres)

;  str0  = "variable:"
;  str1  = "model:"
;  str2  = "forcing:"
;  str3  = "experiment:"
;  str00 =  ""+var@standard_name
;  str10 =  ""+f@model_id
;  str20 =  ""+f@driving_model_id
;  str30 =  ""+f@experiment_id
  txres@txFontHeightF          =  0.010
  txres@txFont                 =  21             ;-- text font "helvetica"
;  gsn_text_ndc(wks, str0, 0.59, 0.96, txres)
;  gsn_text_ndc(wks, str1, 0.59, 0.94, txres)
;  gsn_text_ndc(wks, str2, 0.59, 0.92, txres)
;  gsn_text_ndc(wks, str3, 0.59, 0.90, txres)

;  gsn_text_ndc(wks, str00, 0.72, 0.96, txres)
;  gsn_text_ndc(wks, str10, 0.72, 0.94, txres)
;  gsn_text_ndc(wks, str20, 0.72, 0.92, txres)
  txres@txFont                 =  22             ;-- text font "helvetica-bold"
;  gsn_text_ndc(wks, str30, 0.72, 0.90, txres)

  txres@txFont                 =  21             ;-- text font "helvetica"
  str4 = "time: "+ptime
;  gsn_text_ndc(wks, str4, 0.05, 0.90, txres)


  txres@txJust                 = "BottomRight"
  txres@txFontHeightF          =  0.010
  str = " "
;  str = "~F35~c ~F21~~N~SEC"
;  str = "~F35~c ~F21~~N~DKRZ / "+f@institute_id
  gsn_text_ndc(wks,str, 0.95, 0.01, txres)

;-- draw the frame
  draw(map)
  frame(wks)
end
