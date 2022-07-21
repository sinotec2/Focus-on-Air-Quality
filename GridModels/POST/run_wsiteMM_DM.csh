#kuang@master /nas1/cmaqruns/2019base
#$ cat run_wsiteMM_DM.csh
#! /bin/csh -f

# ==================== WRITESITE_v5.3 Run Script ====================
# Usage: run.writesite.csh >&! writesite_v53.log &
#
# To report problems or request help with this script/program:
#             http://www.epa.gov/cmaq    (EPA CMAQ Website)
#             http://www.cmascenter.org
# ===================================================================

# ==================================================================
#> Runtime Environment Options
# ==================================================================

#> Choose compiler and set up CMAQ environment with correct
#> libraries using config.cmaq. Options: intel | gcc | pgi
 setenv compiler gcc
 setenv CMAQ_HOME $PWD
 source   ../CMAQ_Project/config_cmaq.csh gcc

#> Set General Parameters for Configuring the Simulation
 set VRSN      = v53               #> Code Version
 set PROC      = mpi               #> serial or mpi
 set MECH      = cb6r3_ae7_aq      #> Mechanism ID
set APYR       = `echo $CMAQ_HOME|cut -d'/' -f4|cut -c3-4`
set MO         = $argv[1]
set DM         = $argv[2]
set APYM       = $APYR$MO

 set APPL      = $APYM             #> Application Name (e.g. Gridname)
 set STKCASEE  = 10
if ( $DM == 'd01' ) then
  setenv GRID_NAME  EAsia_81K         # 16-character maximum
else if ( $DM == 'd02' ) then
  setenv GRID_NAME  sChina_27k        # 16-character maximum
else if( $DM == 'd04' ) then
  setenv GRID_NAME  TWN_3X3           # 16-character maximum
else
  echo "Error input d02/d04"
exit 1
endif
#
#> Define RUNID as any combination of parameters above or others. By default,
#> this information will be collected into this one string, $RUNID, for easy
#> referencing in output binaries and log files as well as in other scripts.
 setenv RUNID  ${VRSN}_${compilerString}_${APPL}

#> Set the build directory if this was not set above
#> (this is where the executable is located by default).
setenv BINDIR   ../CMAQ_Project/POST/writesite/scripts/BLD_writesite_${VRSN}_${compilerString}

#> Set the name of the executable.
 setenv EXEC writesite_${VRSN}.exe

#> Set location of CMAQ repo.  This will be used to point to the time zone file
#> needed to run bldoverlay.  The v5.2.1 repo also contains a sample SITE_FILE text file.
 setenv REPO_HOME  ${CMAQ_REPO}

#> Set output directory
 setenv CMAQ_DATA  /nas1/cmaqruns/2016base/data
 setenv CCTMOUTDIR ${CMAQ_DATA}/output_CCTM_${RUNID}
 setenv POSTDIR    ${CCTMOUTDIR}/POST     #> Location where writesite file will be written

  if ( ! -e $POSTDIR ) then
          mkdir $POSTDIR
  endif

# =====================================================================
#> WRITESITE Configuration Options
# =====================================================================

#> Projection sphere type used by I/OAPI (use type #20 to match WRF/CMAQ)
 setenv IOAPI_ISPH 20

#> name of input file containing sites to process (default is all cells)
# setenv SITE_FILE ALL
#> Sample SITE_FILE text file is available in the v5.2.1 repo.
 setenv SITE_FILE ${CMAQ_DATA}/sites/sites.txt

#> delimiter used in site file (default is <tab>)
 setenv DELIMITER ','

#> site file contains column/row values (default is N, meaning lon/lat values will be used)
 setenv USECOLROW N

#> location of time zone data file, tz.csv (this is a required input file)
#> The tz.csv file is saved within the bldoverlay folder of the v5.2.1 repo which also uses this input.
 setenv TZFILE ${CMAQ_DATA}/sites/tz.csv

#> grid layer to output (default is 1)
 setenv LAYER 1

#> adjust to local standard time (default is N)
 setenv USELOCAL Y

#> shifts time of data (default is 0)
#setenv TIME_SHIFT 1

#> output header records (default is Yes)
 setenv PRTHEAD  N
#siteid,column,row,longitude,latitude,date,Time,NO2,O3,PM10,PM25_NO3,PM25_SO4,PM25_TOT,SO2,VOC
#,,,degrees,degrees,YYYY-MM-DD,hh:mm:ss,ppbV,ppbV,ug m-3,ug m-3,ug m-3,ug m-3,ppbV,ppbC


#> output map projection coordinates x and y (default is Yes)
 setenv PRT_XY   N

#> define time window
 set BEG_DATE = `date -ud "20${APYR}-${MO}-15 +-1months" +%Y-%m-%d`
 set MRUN = 4
 @ NDYS = $MRUN * 4
 set START_DATE = `date -ud "${BEG_DATE} +${NDYS}days" +%Y-%m-%d `
 set END_DATE = `date -ud "${START_DATE} +32days" +%Y-%m-%d`



#> Convert START_DATE and END_DATE to Julian day.
#> (required format for writesite STARTDATE and ENDDATE environment variables)
 setenv STARTDATE `date -ud "${START_DATE}" +%Y%j`
 setenv STOP_DAY  `date -ud "${END_DATE}" +%Y%j`
 set I = 0
 set TODAYJ = $STARTDATE
 set TODAYG = $START_DATE
 echo $TODAYJ
#> list of species to output
 setenv SPECIES_1 NO2
 setenv SPECIES_2 O3
 setenv SPECIES_3 PM10
 setenv SPECIES_4 PM25_NO3
 setenv SPECIES_5 PM25_SO4
 setenv SPECIES_6 PM25_TOT
 setenv SPECIES_7 SO2
 setenv SPECIES_8 VOC


 while ($TODAYJ <= $STOP_DAY )  #>Compare dates in terms of YYYYJJJ
   @ R = $I / 4 + 5
   echo 'kuang' $I run$R
  #> Retrieve Calendar day Information
   set YYYY = `date -ud "${TODAYG}" +%Y`
   set YY   = `date -ud "${TODAYG}" +%y`
   set MM   = `date -ud "${TODAYG}" +%m`
   set DD   = `date -ud "${TODAYG}" +%d`
   setenv CTM_APPL ${RUNID}_run${R}_$YYYY$MM${DD}_${GRID_NAME}_${STKCASEE}

#> set input and output files
   setenv INFILE  ${POSTDIR}/COMBINE_ACONC_${CTM_APPL}.nc
        #[Add location of input file, e.g. COMBINE_ACONC file.]
   setenv OUTFILE ${POSTDIR}/MDL_${CTM_APPL}.csv

#> Executable call:
   ${BINDIR}/${EXEC}
   set TODAYG = `date -ud "${TODAYG}+1days" +%Y-%m-%d` #> Add a day for tomorrow
   set TODAYJ = `date -ud "${TODAYG}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   @ I = $I + 1
 end
 date
 exit()
