#!/bin/csh -f

# ======================= ICONv5.3 Run Script ========================
# Usage: run.icon.csh >&! icon_v53.log &                                   
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

#> Set General Parameters for Configuring the Simulation
 set nc         = $argv[1]
 set DM         = `echo $nc|cut -d'/' -f5`
 set VRSN     = v53                     #> Code Version
 set ICTYPE   = regrid                  #> Initial conditions type [profile|regrid]

#> Set the working directory:
 set BLD      = /opt/CMAQ_Project/PREP/icon/scripts/BLD_ICON_${VRSN}_${compilerString}
 set EXEC     = ICON_${VRSN}.exe  
 set EXEC_ID  = icon
 cat $BLD/ICON_${VRSN}.cfg; echo " "; set echo

#> Horizontal grid definition 
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

 setenv GRIDDESC $CMAQ_HOME/$DMF/mcip/GRIDDESC #> grid description file
 setenv IOAPI_ISPH 20                     #> GCTP spheroid, use 20 for WRF-based modeling

#> I/O Controls
 setenv IOAPI_LOG_WRITE T     #> turn on excess WRITE3 logging [ options: T | F ]
 setenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]
 setenv EXECUTION_ID $EXEC    #> define the model execution id

 setenv ICON_TYPE ` echo $ICTYPE | tr "[A-Z]" "[a-z]" ` 

 set OUTDIR   = $CMAQ_HOME/$DMF/icon                        #> output file directory

set DATE  = `/usr/bin/ncdump -h $nc|grep SDATE|awk '{print $3}'`
set y = `echo $DATE|cut -c1-4`
set j = `echo $DATE|cut -c5-`

    set YYYYJJJ  = ${DATE}
    set YYYYMMDD = `date -d "${y}-01-01 +${j}days -1days" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
    set YYMMDD   = `echo $YYYYMMDD|cut -c3-`   #> Convert YYYY-MM-DD to YYMMDD

    setenv SDATE           ${YYYYJJJ}
    setenv STIME           0

    setenv CTM_CONC_1 $nc
    setenv MET_CRO_3D_CRS $CMAQ_HOME/$DM/mcip/METCRO3D.nc
    setenv MET_CRO_3D_FIN $CMAQ_HOME/$DMF/mcip/METCRO3D.nc
    setenv INIT_CONC_1    "$OUTDIR/ICON_yesterday_${GRID_NAME}"
    if ( -e $INIT_CONC_1 ) rm $INIT_CONC_1
#>- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

 if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR

 ls -l $BLD/$EXEC; size $BLD/$EXEC
# unlimit
# limit

#> Executable call:
 time $BLD/$EXEC >& /dev/null

 exit() 
