#!/bin/csh -f

# ======================= BCONv5.3 Run Script ======================== 
# Usage: run.bcon.csh >&! bcon_v53.log &                                
#
# To report problems or request help with this script/program:        
#             http://www.cmascenter.org
# ==================================================================== 

# ==================================================================
#> Runtime Environment Options
# ==================================================================

#> Choose compiler and set up CMAQ environment with correct 
#> libraries using config.cmaq. Options: intel | gcc | pgi
 setenv compiler gcc 

#> Source the config_cmaq file to set the run environment
 setenv CMAQ_HOME /nas2/cmaqruns/2022fcst
 source /opt/CMAQ_Project/config_cmaq.csh $compiler
 
# popd

#> Set General Parameters for Configuring the Simulation
set nc         = $argv[1]
set DM         = `echo $nc|cut -d'/' -f5`

set VRSN      = v53                     #> Code Version
#> Horizontal grid definition
set BCTYPE   = regrid             #> Initial conditions type [profile|regrid]
if ( $DM == 'grid45' ) then
  setenv GRID_NAMEC CWBWRF_45k    # 16-character maximum
  setenv GRID_NAME  SECN_9k       # 16-character maximum
  set DMF = grid09
else if ( $DM == 'grid09' ) then
  setenv GRID_NAMEC  SECN_9k       # 16-character maximum
  setenv GRID_NAME  TWEPA_3k      # 16-character maximum
  set DMF = grid03
else
  echo "Error input nc, must with grid??"
  exit 1
endif
set CMAQ_DATA = ${CMAQ_HOME}/${DMF}


#> Set the build directory:
 set BLD      = /opt/CMAQ_Project/PREP/bcon/scripts/BLD_BCON_${VRSN}_${compilerString}
 set EXEC     = BCON_${VRSN}.exe  
 set EXEC_ID  = bcon
 cat $BLD/BCON_${VRSN}.cfg; echo " "; set echo

#> Horizontal grid definition 
 setenv GRIDDESC $CMAQ_DATA/mcip/GRIDDESC #> grid description file 
 setenv IOAPI_ISPH 20                     #> GCTP spheroid, use 20 for WRF-based modeling

#> I/O Controls
 setenv IOAPI_LOG_WRITE F     #> turn on excess WRITE3 logging [ options: T | F ]
 setenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]
 setenv EXECUTION_ID $EXEC    #> define the model execution id

# =====================================================================
#> BCON Configuration Options
#
# BCON can be run in one of two modes:                                     
#     1) regrids CMAQ CTM concentration files (BC type = regrid)     
#     2) use default profile inputs (BC type = profile)
# =====================================================================

 setenv BCON_TYPE ` echo $BCTYPE | tr "[A-Z]" "[a-z]" `

# =====================================================================
#> Input/Output Directories
# =====================================================================

 setenv OUTDIR  $CMAQ_HOME/$DMF/bcon       #> output file directory

set DATE  = `/usr/bin/ncdump -h $nc|grep SDATE|awk '{print $3}'`
set y = `echo $DATE|cut -c1-4`
set j = `echo $DATE|cut -c5-`
set NDAYS = 1
 
    set YYYYJJJ  = ${DATE}   #> Convert YYYY-MM-DD to YYYYJJJ
    set YYYYMMDD = `date -d "${y}-01-01 +${j}days -1days" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
    set YYMMDD   = `echo $YYYYMMDD|cut -c3-` #> Convert YYYY-MM-DD to YYMMDD

 setenv CTM_CONC_1 $nc
 setenv MET_CRO_3D_CRS $CMAQ_HOME/$DM/mcip/METCRO3D.nc
 setenv MET_BDY_3D_FIN $CMAQ_DATA/mcip/nc/METBDY3D.${YYYYMMDD}
 setenv BNDY_CONC_1    "$OUTDIR/BCON_${YYYYMMDD}_${GRID_NAME} -v"

# =====================================================================
#> Output File
# =====================================================================
 
#>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR
 if ( -e "$BNDY_CONC_1" ) rm $BNDY_CONC_1

 ls -l $BLD/$EXEC; size $BLD/$EXEC
 #unlimit
 #limit

#> Executable call:
 time $BLD/$EXEC >& /dev/null

 exit() 
