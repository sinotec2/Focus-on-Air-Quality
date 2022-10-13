#!/bin/csh -f
setenv compiler gcc
set CMAQ_HOME = /nas2/cmaqruns/2022fcst
source /opt/CMAQ_Project/config_cmaq.csh $compiler
set DM         = $argv[1]
set ND         = 5
if (  $#argv >= 2 ) then
  set ND = $argv[2]
endif
set CoordName  = TWN_PULI          # 16-character maximum
if ( $DM == 'grid45' ) then
  set GridName   = CWBWRF_45k        # 16-character maximum
  set d          = 'd01'
else if ( $DM == 'grid09' ) then
  set GridName   = SECN_9k       # 16-character maximum
  set d          = 'd02'
else if ( $DM == 'grid03' ) then
  set GridName   = TWEPA_3k        # 16-character maximum
  set d          = 'd03'
else
  echo "Error input grid45,09,~03"
  exit 1
endif
set CMAQ_DATA  = $CMAQ_HOME/${DM}
set DataPath   = $CMAQ_DATA
set InMetDir   = $DataPath/wrfout
set InGeoDir   = $DataPath/wrfout
set OutDir     = $DataPath/mcip
set ProgDir    = /opt/CMAQ_Project/PREP/mcip/src
#set ProgDir    = /nas2/cmaq2019/download/model/cmaq_recommend_ipncf/PREP/mcip/src #/opt/CMAQ_Project/PREP/mcip/src
set WorkDir    = $OutDir
set InMetFiles = 
foreach i (`seq 0 ${ND}`)
  set InMetFiles = ( $InMetFiles $InMetDir/wrfout_${d}_${i} )
end
set IfGeo      = "T"
set InGeoFile  = $InGeoDir/geo_em.${d}.nc
set LPV     = 0
set LWOUT   = 1
set LUVBOUT = 1

set BEGD = `~/bin/pr_times.py $InMetFiles[1]|head -n1|cut -c1-10` #date -d now +%Y-%m-%d`
set START = `date -d $BEGD +%Y-%m-%d`
set ENDDT = `date -d "$BEGD +${ND}days" +%Y-%m-%d`
set MCIP_START = ${START}:01:00.0000  # [UTC]
set MCIP_END   = ${ENDDT}:00:00.0000  # [UTC]

set INTVL      = 60 # [min]

set IOFORM = 1

set BTRIM = -1

if ( $DM == 'grid45' ) then
  set X0    =   1
  set Y0    =   1
  set NCOLS = 218
  set NROWS = 126
  set NP    =   1
else if ( $DM == 'grid09' ) then
  set X0    =   2 
  set Y0    =   2
  set NCOLS = 200
  set NROWS = 200
  set NP    =   1
else if ( $DM == 'grid03' ) then
  set X0    =   5 
  set Y0    =   5
  set NCOLS =  92
  set NROWS = 131
  set NP    =   1
endif

set LPRT_COL = 0
set LPRT_ROW = 0

set WRF_LC_REF_LAT = 25


set PROG = mcip

date

#-----------------------------------------------------------------------
# Make sure directories exist.
#-----------------------------------------------------------------------

if ( ! -d $InMetDir ) then
  echo "No such input directory $InMetDir"
  exit 1
endif

if ( ! -d $OutDir ) then
  echo "No such output directory...will try to create one"
  mkdir -p $OutDir
  if ( $status != 0 ) then
    echo "Failed to make output directory, $OutDir"
    exit 1
  endif
endif

if ( ! -d $ProgDir ) then
  echo "No such program directory $ProgDir"
  exit 1
endif

#-----------------------------------------------------------------------
# Make sure the input files exist.
#-----------------------------------------------------------------------

if ( $IfGeo == "T" ) then
  if ( ! -f $InGeoFile ) then
    echo "No such input file $InGeoFile"
    exit 1
  endif
endif

foreach fil ( $InMetFiles )
  if ( ! -f $fil ) then
    echo "No such input file $fil"
    exit 1
  endif
end

#-----------------------------------------------------------------------
# Make sure the executable exists.
#-----------------------------------------------------------------------

if ( ! -f $ProgDir/${PROG}.exe ) then
  echo "Could not find ${PROG}.exe"
  exit 1
endif

#-----------------------------------------------------------------------
# Create a work directory for this job.
#-----------------------------------------------------------------------

if ( ! -d $WorkDir ) then
  mkdir -p $WorkDir
  if ( $status != 0 ) then
    echo "Failed to make work directory, $WorkDir"
    exit 1
  endif
endif

cd $WorkDir

#-----------------------------------------------------------------------
# Set up script variables for input files.
#-----------------------------------------------------------------------

if ( $IfGeo == "T" ) then
  if ( -f $InGeoFile ) then
    set InGeo = $InGeoFile
  else
    set InGeo = "no_file"
  endif
else
  set InGeo = "no_file"
endif

set FILE_GD  = $OutDir/GRIDDESC

#-----------------------------------------------------------------------
# Create namelist with user definitions.
#-----------------------------------------------------------------------

set MACHTYPE = `uname`
if ( ( $MACHTYPE == "AIX" ) || ( $MACHTYPE == "Darwin" ) ) then
  set Marker = "/"
else
  set Marker = "&END"
endif

cat > $WorkDir/namelist.${PROG} << !

 &FILENAMES
  file_gd    = "$FILE_GD"
  file_mm    = "$InMetFiles[1]",
!

if ( $#InMetFiles > 1 ) then
  @ nn = 2
  while ( $nn <= $#InMetFiles )
    cat >> $WorkDir/namelist.${PROG} << !
               "$InMetFiles[$nn]",
!
    @ nn ++
  end
endif

if ( $IfGeo == "T" ) then
cat >> $WorkDir/namelist.${PROG} << !
  file_geo   = "$InGeo"
!
endif

cat >> $WorkDir/namelist.${PROG} << !
  ioform     =  $IOFORM
 $Marker

 &USERDEFS
  lpv        =  $LPV
  lwout      =  $LWOUT
  luvbout    =  $LUVBOUT
  mcip_start = "$MCIP_START"
  mcip_end   = "$MCIP_END"
  intvl      =  $INTVL
  coordnam   = "$CoordName"
  grdnam     = "$GridName"
  btrim      =  $BTRIM
  lprt_col   =  $LPRT_COL
  lprt_row   =  $LPRT_ROW
  wrf_lc_ref_lat = $WRF_LC_REF_LAT
 $Marker

 &WINDOWDEFS
  x0         =  $X0
  y0         =  $Y0
  ncolsin    =  $NCOLS
  nrowsin    =  $NROWS
 $Marker

!

#-----------------------------------------------------------------------
# Set links to FORTRAN units.
#-----------------------------------------------------------------------

rm fort.*
if ( -f $FILE_GD ) rm -f $FILE_GD

ln -s $FILE_GD                   fort.4
ln -s $WorkDir/namelist.${PROG}  fort.8

set NUMFIL = 0
foreach fil ( $InMetFiles )
  @ NN = $NUMFIL + 10
  ln -s $fil fort.$NN
  @ NUMFIL ++
end

#-----------------------------------------------------------------------
# Set output file names and other miscellaneous environment variables.
#-----------------------------------------------------------------------
#add by kuang
setenv IOAPI_CHECK_HEADERS  F
setenv IOAPI_OFFSET_64      T
setenv IOAPI_CFMETA YES
setenv IOAPI_CMAQMETA NONE	
setenv IOAPI_SMOKEMETA NONE	
setenv IOAPI_TEXTMETA NONE	

setenv EXECUTION_ID         $PROG

setenv GRID_BDY_2D          $OutDir/GRIDBDY2D.nc
setenv GRID_CRO_2D          $OutDir/GRIDCRO2D.nc
setenv GRID_DOT_2D          $OutDir/GRIDDOT2D.nc
setenv MET_BDY_3D           $OutDir/METBDY3D.nc
setenv MET_CRO_2D           $OutDir/METCRO2D.nc
setenv MET_CRO_3D           $OutDir/METCRO3D.nc
setenv MET_DOT_3D           $OutDir/METDOT3D.nc
setenv LUFRAC_CRO           $OutDir/LUFRAC_CRO.nc
setenv SOI_CRO              $OutDir/SOI_CRO.nc
setenv MOSAIC_CRO           $OutDir/MOSAIC_CRO.nc

if ( -f $GRID_BDY_2D ) rm -f $GRID_BDY_2D
if ( -f $GRID_CRO_2D ) rm -f $GRID_CRO_2D
if ( -f $GRID_DOT_2D ) rm -f $GRID_DOT_2D
if ( -f $MET_BDY_3D  ) rm -f $MET_BDY_3D
if ( -f $MET_CRO_2D  ) rm -f $MET_CRO_2D
if ( -f $MET_CRO_3D  ) rm -f $MET_CRO_3D
if ( -f $MET_DOT_3D  ) rm -f $MET_DOT_3D
if ( -f $LUFRAC_CRO  ) rm -f $LUFRAC_CRO
if ( -f $SOI_CRO     ) rm -f $SOI_CRO
if ( -f $MOSAIC_CRO  ) rm -f $MOSAIC_CRO

if ( -f $OutDir/mcip.nc      ) rm -f $OutDir/mcip.nc
if ( -f $OutDir/mcip_bdy.nc  ) rm -f $OutDir/mcip_bdy.nc

#-----------------------------------------------------------------------
# Execute MCIP.
#-----------------------------------------------------------------------

#Version:                                 3.3.2
#mpirun --use-hwthread-cpus $ProgDir/${PROG}.exe
#mpirun --oversubscribe -np $NP $ProgDir/${PROG}.exe

#Intel(R) MPI Library for Linux* OS, Version 2019 Update 6 Build 20191024 (id: 082ae5608)
#setenv LD_LIBRARY_PATH /opt/netcdf/netcdf4_intel/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin
mpirun -np $NP $ProgDir/${PROG}.exe #  >& /dev/null
if ( $status == 0 ) then
  rm fort.*
  exit 0
else
  echo "Error running $PROG"
  exit 1
endif
