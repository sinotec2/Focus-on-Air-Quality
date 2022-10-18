;----------------------------------------------------------------------
; WRF_cn_1.ncl
;
; Concepts illustrated:
;   - Plotting WRF data
;----------------------------------------------------------------------
; This script creates two simple contour views of pressure at a 
; specific time and level. No map background is generated.
;----------------------------------------------------------------------
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"   
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"   
; load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin
;---Open file; substitute your own WRF output file here
  nxy=asciiread("param.txt",(/6/),"integer")
  nx=nxy(1)
  ny=nxy(4)
  t=asciiread("title.txt",1,"string")
  tit=t(0)
  f=asciiread("tmp.PLT",(/ny*nx,3/),"float")
;  f=asciiread("tmp.PLT",-1,"float")
  nnn=dimsizes(f)
  npt=toint(nnn/3)
;  nx=toint(sqrt(npt))
;  ny=nx
  p=new((/ny,nx/),float)
  do j=0,ny-1
  do i=0,nx-1
    ji=j*nx+i
    p(j,i)=f(ji,2)
  end do
  end do

;--Read variables

  printVarSummary(p)   ; Look at your data
  printMinMax(p,0)

;---Create simple contour plots  
   wks_type = "png"
   wks_type@wkWidth = 2000
   wks_type@wkHeight = 2000
   wks = gsn_open_wks(wks_type,"tmp_cn")

  res                       = True            ; plot mods desired
  res@gsnMaximize           = True            ; maximize plot size
  res@tiMainString          = tit             ; main title
  res@cnLineThicknessF      =7
  plot                      = gsn_csm_contour(wks,p(:,:),res)
end

