undef("read_ocean_land_colormap")
function read_ocean_land_colormap(num_ocean)
local cmap_ocn, cmap_lnd
begin
  cmap_ocn = read_colormap_file("GMT_ocean")
  cmap_lnd = read_colormap_file("OceanLakeLandSnow")
  newcmap = array_append_record(cmap_ocn(0:num_ocean-1,:),cmap_lnd(2::2,:),0)
  return(newcmap)
end

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

undef("draw_topo_map")
procedure draw_topo_map(wks,elev,title)
local res, labels, nlevels
begin
  trj_name = asciiread("filename.txt",-1,"string")
  trj_name = str_sub_str(trj_name,".csv","_")
  cls=(/"Red","Blue", "Green","Black","Red"/)
  pthL=(/"SH", "BJ", "BH", "SC", "line"/)
  pthM=(/"SH", "BJ", "BH", "SC", "mark"/)
  mks=(/16,  7, 8, 6, 16/);16dot, 7TriAng, 8invTriAng, 6Sqare, 5Cross
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
  end do



  res                    = True

  res@gsnMaximize        = True     ; maximize plot in frame

  res@cnFillOn           = True     ; turn on contour fill
  res@cnFillMode         = "MeshFill"
  res@cnLinesOn          = False    ; turn off contour lines
  res@cnLineLabelsOn     = False    ; turn off line labels
  res@cnInfoLabelOn      = False    ; turn off info label
  res@lbBoxLinesOn       = False    ; turn off labelbar box lines

  split_elev               = -30; -40   ; meters
  num_ocean_colors         = 40
  emax=3000.
  levels_and_colors        = calc_levels_and_colors(wks,0.       ,emax     ,split_elev,num_ocean_colors)

  res@cnLevelSelectionMode = "ExplicitLevels"
  res@cnLevels             = levels_and_colors[0]
  res@cnFillPalette        = levels_and_colors[1]
  res@gsnAddCyclic         = False           ; don't add longitude cyclic point

  res@mpFillOn                    = False
  res@pmTickMarkDisplayMode       = "Always"   ; Nicer map labels
  res@mpGeophysicalLineThicknessF = 2          ; Thicker map outlines
  res@mpMinLatF            = max((/min(lat)-0.5,min(elev@lat2d)/))       ; zoom in on map
  res@mpMaxLatF            = min((/max(lat)+0.5,max(elev@lat2d)/))
  res@mpMinLonF            = max((/min(lon)-0.5,min(elev@lon2d)/))
  res@mpMaxLonF            = min((/max(lon)+0.5,max(elev@lon2d)/))
  res@mpOutlineOn        = False        ; turn off map outlines

  res@tiMainString                = "TITLE"  ; Main title

  nlevels           = dimsizes(res@cnLevels)
  labels            = new(nlevels+2,string)
  labels            = ""                 ; Blank out all but
  ii                = ind(res@cnLevels.eq.split_elev)+1
  labels(0)         = "" + 0;min(elev)     ; First,
  labels(nlevels+1) = "" + emax;max(elev)     ; last, and
  labels(ii)         = "" + split_elev   ; middle labels

  res@lbLabelAutoStride = False            ; This will make sure every labelbar
  res@lbLabelAlignment = "ExternalEdges"   ; can potentially be labeled.
  res@lbLabelStrings   = labels

  res@gsnDraw        = False    ; Don't draw plot or
  res@gsnFrame       = False    ;   advance frame
  res@gsnLeftStringFontHeightF=0.01
  res@gsnRightStringFontHeightF=0.01
  res@cnFillOpacityF = 0.6 ;1.0fully opaque

  plot = gsn_csm_contour_map(wks,elev,res)

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

  filename="/var/www/html/taiwan/TWN_COUNTY.shp"
; filename="/Users/Data/GIS/OSM_20210318/gis_osm_places_free_1.shp"
  dum  = gsn_add_shapefile_polylines(wks,plot,filename,True)

  txres                        =  True
  txres@txJust                 = "BottomRight"
  txres@txFontHeightF          =  0.010
  str = "~F35~c ~F21~~N~SEC"
  gsn_text_ndc(wks,str, 0.95, 0.01, txres)

  draw(plot)
  frame(wks)


end

begin
  wks_type = "png"
  wks_type@wkHeight = 2500
  wks_type@wkWidth = 2500
  wks = gsn_open_wks(wks_type,"topo") ; send graphics to PNG file
  topo_filename = "ETOPO5.DAT"
  elev = read_elev_data(topo_filename)
  draw_topo_map(wks,elev,topo_filename)
end
