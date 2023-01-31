;kuang@node03 /var/www/html/taiwan
;$ cat avg_by_town.ncl
;----------------------------------------------------------------------
;-- Function:  avg_by_town(...)
;--                ->  compute the average of the data for each town
;--------------------------------------------------------------------
undef("avg_by_town")
;--------------------------------------------------------------------
function avg_by_town(wks,plot,data,f,county_name,wtowns,levels,colors)
;--------------------------------------------------------------------
local f, segments, geometry, geomDims, geom_segIndex, geom_numSegs, segs_xyzIndex, \
      segs_numPnts, numFeatures, i, lat, lon, startSegment, numSegments, seg, \
      startPT, endPT, dims, minlat, maxlat, minlon, maxlon
begin
  getvalues plot
      "mpLeftCornerLatF"      :   minlat                        ;-- retrieve map min lat
      "mpRightCornerLatF"     :   maxlat                        ;-- retrieve map max lat
      "mpLeftCornerLonF"      :   minlon                        ;-- retrieve map min lon
      "mpRightCornerLonF"     :   maxlon                        ;-- retrieve map max lon
  end getvalues

;-- read shapefile data
  geomDims      =  getfilevardimsizes(f,"geometry")
  numFeatures   =  geomDims(0)
  segments      =  f->segments
  geometry      =  f->geometry
  geom_segIndex =  f@geom_segIndex
  geom_numSegs  =  f@geom_numSegs
  segs_xyzIndex =  f@segs_xyzIndex
  segs_numPnts  =  f@segs_numPnts
  lat           =  f->y
  lon           =  f->x
  dims          =  dimsizes(data)
  nlat          =  dims(0)
  nlon          =  dims(1)
  lat1d         =  ndtooned(conform_dims((/nlat,nlon/),data&lat,0))
  lon1d         =  ndtooned(conform_dims((/nlat,nlon/),data&lon,1))
  nlatlon       =  dimsizes(lat1d)
  ii_latlon     =  ind(lat1d.ge.minlat.and.lat1d.le.maxlat.and.lon1d.ge.minlon.and.lon1d.le.maxlon)
  nii_latlon    =  dimsizes(ii_latlon)

;-- grab the indexes containing the townes
  counties      =  f->COUNTYCODE                            ;-- state names reference
  names3        =  f->TOWNID                                ;-- town names copied from DEU_adm3.shp
  TWN_towns     =  ind(names3.ne."")                           ;-- read all town names

;-- get state_name townes
  wc=new(dimsizes(names3),typeof(names3))
  if(.not.isatt(wc,"_FillValue")) then
    wc@_FillValue = default_fillvalue(typeof(names3))          ;-- make sure "wc" has a missing value
  end if
  n=0
  do m=0,dimsizes(names3)-1
    if(counties(m).eq.county_name) then
       wc(n) = names3(m)                                       ;-- get all relevant townes
    else
       wc(n) = default_fillvalue(typeof(names3))               ;-- set all other to missing value
    end if
    n=n+1
  end do
  wtowns = ind(.not. ismissing(wc))
  county_towns = new(dimsizes(wtowns),string)
  do jj=0,dimsizes(wtowns)-1
     county_towns(jj) = names3(wtowns(jj))                ;-- get the names of the relevant townes
  end do


;-- create array to hold new data mask and averaged data
  data_mask_1d  = new(nlatlon,integer)
  if(.not.isatt(data,"_FillValue")) then
    data@_FillValue = default_fillvalue(typeof(data))          ;-- make sure "data" has a missing value
  end if
  data_1d  = ndtooned(data)                                    ;-- convert data to 1D array
  data_avg = new(dimsizes(TWN_towns),typeof(data),data@_FillValue)

  gnres    = True                                              ;-- polygon resource list
  nfill    = dimsizes(colors)

  do i=0,dimsizes(TWN_towns)-1
     do ll=0,dimsizes(wtowns)-1
        if (names3(i) .eq. county_towns(ll)) then
           data_mask_1d = 0                                          ; Be sure to reset to 0 for every town
           startSegment = geometry(TWN_towns(i), geom_segIndex)
           numSegments  = geometry(TWN_towns(i), geom_numSegs)
           do seg=startSegment, startSegment+numSegments-1
              startPT = segments(seg, segs_xyzIndex)
              endPT   = startPT + segments(seg, segs_numPnts) - 1
              do n=0,nii_latlon-1
                 nn = ii_latlon(n)                                   ; Get index of point we're checking
                 if(lat1d(nn).lt.min(lat(startPT:endPT)).or.lat1d(nn).gt.max(lat(startPT:endPT)).or.\
                    lon1d(nn).lt.min(lon(startPT:endPT)).or.lon1d(nn).gt.max(lon(startPT:endPT)))
                    continue
                 end if
                 if(gc_inout(lat1d(nn),lon1d(nn),lat(startPT:endPT),lon(startPT:endPT))) then
                    data_mask_1d(nn) = 1    ; This point is inside this town
                 end if
              end do
           end do
           ndm = num(data_mask_1d.eq.1)
           ;-- calculate the averages
           if(ndm.gt.0) then
             data_avg(i)  = avg(where(data_mask_1d.eq.1,data_1d,data_1d@_FillValue))
             print("-----------------------------------------------------------------")
             print((ll+1)+": Inspecting "+county_name+" county '" + names3(TWN_towns(i)) + "'...")
             print("     "+ndm + " data values found --> average = " + data_avg(i))
           end if
        end if
     end do
  end do

  return(data_avg)                               ;-- return data averages for each town
end
