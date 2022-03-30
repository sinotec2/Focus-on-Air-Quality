---
layout: default
title: calmet.inp
nav_order: 2
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
---

# calmet.inp
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## Title

CALMET.INP      2.1             

    Hour Start and End Times with Seconds

    1 km resolution CALMET simulation for 4 hours from 5AM January 9, 1990  with MM4 data, 5 surface met stations, 1 overwater station,

    3 upper air met stations, and 16 precip stations
---------------- 
Run title (3 lines) 

------------------------------------------

                    CALMET MODEL CONTROL FILE
                    --------------------------

-------------------------------------------------------------------------------

## INPUT GROUP: 0 -- Input and Output File Names


### Subgroup (a)
------------

|Default Name|  Type|          File_Name|
|-|-|-|
|GEO.DAT|       input|    ! GEODAT=DATA/TAI3GEO_LCC.DAT    !|
|SURF.DAT|      input|    * SRFDAT=../SURF.DAT      *|
|CLOUD.DAT|     input|    * CLDDAT=            *|
|PRECIP.DAT|    input|    * PRCDAT=../PRECIP.DAT    *|
|WT.DAT|        input|    * WTDAT=../WT.DAT         *|
|CALMET.LST|    output|   ! METLST=CALMET.LST     !|
|CALMET.DAT|    output|   ! METDAT=CALMET.DAT    !|
|PACOUT.DAT|    output|   * PACDAT=            *|

All file names will be converted to lower case if LCFILES = T

Otherwise, if LCFILES = F, file names will be converted to UPPER CASE

         T = lower case      ! LCFILES = T !
         F = UPPER CASE

NUMBER OF UPPER AIR & OVERWATER STATIONS:

    Number of upper air stations (NUSTA)  No default     ! NUSTA =  0  !
    Number of overwater met stations
                                 (NOWSTA) No default     ! NOWSTA = 0  !
    Number of MM4/MM5/M3D.DAT files
                                 (NM3D) No default       ! NM3D =  1  !

    Number of IGF-CALMET.DAT files
                                 (NIGF)   No default     ! NIGF =  0  !

                       !END!
--------------------------------------------------------------------------------

### Subgroup (b) Upper air files (one per station)

|Default Name|  Type|          File_Name|
|-|-|-|
|UP1.DAT   |    input     |1  * UPDAT=../CWB692.DAT*    *END\*|
|UP2.DAT   |    input     |2  * UPDAT=../CWB699.DAT*    *END\*|
--------------------------------------------------------------------------------

### Subgroup (c) Overwater station files (one per station)

|Default Name|  Type|          File_Name|
|-|-|-|
|SEA1.DAT|       input|     1  * SEADAT=../SEA1.DAT*  *END\*|
|SEA1.DAT|       input|     2  * SEADAT=../SEA2.DAT*  *END\*|  
--------------------------------------------------------------------------------

### Subgroup (d) MM4/MM5/M3D.DAT files (consecutive or overlapping)

|Default Name|  Type|          File_Name|
|-|-|-|
|MM51.DAT    |   input  |   1  ! M3DDAT=data/processed/met_20200415.dat !    !END! |
--------------------------------------------------------------------------------

### Subgroup (e) Other file names

|Default Name|  Type|          File_Name|
|-|-|-|
|DIAG.DAT  |    input    |  * DIADAT=                  *|
|PROG.DAT  |   input     | * PRGDAT=                  *|
|TEST.PRT  |    output   |  * TSTPRT=                  *|
|TEST.OUT  |    output   |  * TSTOUT=                  *|
|TEST.KIN  |    output   |  * TSTKIN=                  *|
|TEST.FRD  |    output   |  * TSTFRD=                  *|
|TEST.SLP  |    output   |  * TSTSLP=                  *|

--------------------------------------------------------------------------------
NOTES: 
1. File/path names can be up to 70 characters in length
2. Subgroups (a) and (d) must have ONE 'END' (surround by
           delimiters) at the end of the group
3. Subgroups (b) and (c) must have an 'END' (surround by
           delimiters) at the end of EACH LINE

                         !END!

-------------------------------------------------------------------------------

## INPUT GROUP: 1 -- General run control parameters
--------------
     Starting date:    Year   (IBYR)  --    No default   ! IBYR  =  2020  !
                       Month  (IBMO)  --    No default   ! IBMO  =  04  !
                       Day    (IBDY)  --    No default   ! IBDY  =  15  !
     Starting time:    Hour   (IBHR)  --    No default   ! IBHR  =  0  !
                       Second (IBSEC) --    No default   ! IBSEC =  0  !

     Ending date:      Year   (IEYR)  --    No default   ! IEYR  =  2020  !
                       Month  (IEMO)  --    No default   ! IEMO  =  04  !
                       Day    (IEDY)  --    No default   ! IEDY  =  30  !
     Ending time:      Hour   (IEHR)  --    No default   ! IEHR  =  0  !
                       Second (IESEC) --    No default   ! IESEC =  0  !

      UTC time zone         (ABTZ) -- No default         ! ABTZ = UTC+0000 !
         (character*8)
         PST = UTC-0800, MST = UTC-0700 , GMT = UTC-0000
         CST = UTC-0600, EST = UTC-0500

     Length of modeling time-step (seconds)
     Must be a fraction of 1 hour
     (NSECDT)                        Default:3600     ! NSECDT =  3600 !
                                     Units: seconds

     Run type            (IRTYPE) -- Default: 1       ! IRTYPE=  1  !

        0 = Computes wind fields only
        1 = Computes wind fields and micrometeorological variables
            (u*, w*, L, zi, etc.)
        (IRTYPE must be 1 to run CALPUFF or CALGRID)

     Compute special data fields required
     by CALGRID (i.e., 3-D fields of W wind
     components and temperature)
     in additional to regular            Default: T    ! LCALGRD = T !
     fields ? (LCALGRD)
     (LCALGRD must be T to run CALGRID)

      Flag to stop run after
      SETUP phase (ITEST)             Default: 2       ! ITEST=  2   !
      (Used to allow checking
      of the model inputs, files, etc.)
      ITEST = 1 - STOPS program after SETUP phase
      ITEST = 2 - Continues with execution of
                  COMPUTATIONAL phase after SETUP
    Test options specified to see if
     they conform to regulatory
     values? (MREG)                   No Default       ! MREG =  0   !

        0 = NO checks are made
        1 = Technical options must conform to USEPA guidance
                  IMIXH    -1       Maul-Carson convective mixing height
                                    over land; OCD mixing height overwater
                  ICOARE   0        OCD deltaT method for overwater fluxes
                  THRESHL  0.0      Threshold buoyancy flux over land needed
                                    to sustain convective mixing height growth


!END!

-------------------------------------------------------------------------------

## INPUT GROUP: 2 -- Map Projection and Grid control parameters
--------------

### Projection for all (X,Y):
-------------------------

      Map projection
     (PMAP)                     Default: UTM    ! PMAP = LCC  !

         UTM :  Universal Transverse Mercator
         TTM :  Tangential Transverse Mercator
         LCC :  Lambert Conformal Conic
          PS :  Polar Stereographic
          EM :  Equatorial Mercator
        LAZA :  Lambert Azimuthal Equal Area

     False Easting and Northing (km) at the projection origin
     (Used only if PMAP= TTM, LCC, or LAZA)
     (FEAST)                    Default=0.0     ! FEAST  =  0.000  !
     (FNORTH)                   Default=0.0     ! FNORTH =  0.000  !

     UTM zone (1 to 60)
     (Used only if PMAP=UTM)
     (IUTMZN)                   No Default      ! IUTMZN =  51   !

     Hemisphere for UTM projection?
     (Used only if PMAP=UTM)
     (UTMHEM)                   Default: N      ! UTMHEM = N  !
         N   :  Northern hemisphere projection
         S   :  Southern hemisphere projection

     Latitude and Longitude (decimal degrees) of projection origin
     (Used only if PMAP= TTM, LCC, PS, EM, or LAZA)
     (RLAT0)                    No Default      ! RLAT0 =  23.61N!
     (RLON0)                    No Default      ! RLON0 = 120.99E!

         TTM :  RLON0 identifies central (true N/S) meridian of projection
                RLAT0 selected for convenience
         LCC :  RLON0 identifies central (true N/S) meridian of projection
                RLAT0 selected for convenience
         PS  :  RLON0 identifies central (grid N/S) meridian of projection
                RLAT0 selected for convenience
         EM  :  RLON0 identifies central meridian of projection
                RLAT0 is REPLACED by 0.0N (Equator)
         LAZA:  RLON0 identifies longitude of tangent-point of mapping plane
                RLAT0 identifies latitude of tangent-point of mapping plane

     Matching parallel(s) of latitude (decimal degrees) for projection
     (Used only if PMAP= LCC or PS)
     (XLAT1)                    No Default      ! XLAT1 = 10N  !
     (XLAT2)                    No Default      ! XLAT2 = 40N  !

         LCC :  Projection cone slices through Earth's surface at XLAT1 and XLAT2
         PS  :  Projection plane slices through Earth at XLAT1
                (XLAT2 is not used)

     ----------
     Note:  Latitudes and longitudes should be positive, and include a
            letter N,S,E, or W indicating north or south latitude, and
            east or west longitude.  For example,
            35.9  N Latitude  =  35.9N
            118.7 E Longitude = 118.7E


### Datum-region
------------

     The Datum-Region for the coordinates is identified by a character string.  Many mapping products currently available use the model of the WGS-84).  Other local models may be in use, and their selection in CALMET will make its output consistent with local mapping products.  The list of Datum-Regions with official transformation parameters is provided by the National Imagery and Mapping Agency (NIMA).

     NIMA Datum - Regions(Examples)
------------------------------------------------------------------------------
     WGS-84    WGS-84 Reference Ellipsoid and Geoid, Global coverage (WGS84)
     NAS-C     NORTH AMERICAN 1927 Clarke 1866 Spheroid, MEAN FOR CONUS (NAD27)
     NAR-C     NORTH AMERICAN 1983 GRS 80 Spheroid, MEAN FOR CONUS (NAD83)
     NWS-84    NWS 6370KM Radius, Sphere
     ESR-S     ESRI REFERENCE 6371KM Radius, Sphere

     Datum-region for output coordinates
     (DATUM)                    Default: WGS-84    ! DATUM = WGS-G  !


### Horizontal grid definition:
---------------------------

     Rectangular grid defined for projection PMAP,
     with X the Easting and Y the Northing coordinate

     No. X grid cells (NX)      No default     ! NX =  83 !
     No. Y grid cells (NY)      No default     ! NY =  137  !
    Grid spacing (DGRIDKM)      No default     ! DGRIDKM =3.000 !
                                       Units: km
     Reference grid coordinate of
     SOUTHWEST corner of grid cell (1,1)
    X coordinate (XORIGKM)     No default   72! XORIGKM = -124.5!
    Y coordinate (YORIGKM)     No default     ! YORIGKM = -205.5!

### Vertical grid definition:
-------------------------

    No. of vertical layers (NZ)    No default     ! NZ =  15  !

        Cell face heights in arbitrary
        vertical grid (ZFACE(NZ+1))    No defaults
                                       Units: m
    !ZFACE=0.0,20.0,47.0,75.0,106.5,141.5,181.0,226.0,277.0,334.5,399.5,555.5,757.0,1177.0,1566.5,2403.5!

    *ZFACE=0, 20., 32.03, 64.07,96.32, 128.58, 193.77, 258.96, 358.51, 458.05,730.37, 1011.02, 1374.45, 1753.08, 2562.08, 11656.23*
!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 3 -- Output Options
--------------

### DISK OUTPUT OPTION

       Save met. fields in an unformatted
       output file ?              (LSAVE)  Default: T     ! LSAVE = T !
       (F = Do not save, T = Save)

       Type of unformatted output file:
       (IFORMO)                            Default: 1    ! IFORMO =  1  !

            1 = CALPUFF/CALGRID type file (CALMET.DAT)
            2 = MESOPUFF-II type file     (PACOUT.DAT)


### LINE PRINTER OUTPUT OPTIONS:

       Print met. fields ?  (LPRINT)       Default: F     ! LPRINT = F !
       (F = Do not print, T = Print)
       (NOTE: parameters below control which
              met. variables are printed)

       Print interval
       (IPRINF) in hours                   Default: 1     ! IPRINF =  1  !
       (Meteorological fields are printed
        every  1  hours)


       Specify which layers of U, V wind component
       to print (IUVOUT(NZ)) -- NOTE: NZ values must be entered
       (0=Do not print, 1=Print)
       (used only if LPRINT=T)        Defaults: NZ*0 
       ! IUVOUT =  1 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0  !
       -----------------------


       Specify which levels of the W wind component to print
       (NOTE: W defined at TOP cell face --  10  values)
       (IWOUT(NZ)) -- NOTE: NZ values must be entered
       (0=Do not print, 1=Print)
       (used only if LPRINT=T & LCALGRD=T)
       -----------------------------------
                                            Defaults: NZ*0 
        ! IWOUT =  1 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0  !


       Specify which levels of the 3-D temperature field to print
       (ITOUT(NZ)) -- NOTE: NZ values must be entered
       (0=Do not print, 1=Print)
       (used only if LPRINT=T & LCALGRD=T)
       -----------------------------------
                                            Defaults: NZ*0 
        ! ITOUT =  1 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0  !

       Specify which meteorological fields
       to print
       (used only if LPRINT=T)             Defaults: 0 (all variables)
       -----------------------


         Variable            Print ?
                         (0 = do not print,
                          1 = print)
         --------        ------------------

      !  STABILITY  =           1           ! - PGT stability class
      !  USTAR      =           1           ! - Friction velocity
      !  MONIN      =           1           ! - Monin-Obukhov length
      !  MIXHT      =           1           ! - Mixing height
      !  WSTAR      =           1           ! - Convective velocity scale
      !  PRECIP     =           1           ! - Precipitation rate
      !  SENSHEAT   =           1           ! - Sensible heat flux
      !  CONVZI     =           1           ! - Convective mixing ht.


       Testing and debug print options for micrometeorological module

          Print input meteorological data and
          internal variables (LDB)         Default: F       ! LDB = F !
          (F = Do not print, T = print)
          (NOTE: this option produces large amounts of output)

          First time step for which debug data
          are printed (NN1)                Default: 1       ! NN1 =  1  !

          Last time step for which debug data
          are printed (NN2)                Default: 1       ! NN2 =  1  !


       Testing and debug print options for wind field module
       (all of the following print options control output to
        wind field module's output files: TEST.PRT, TEST.OUT,
        TEST.KIN, TEST.FRD, and TEST.SLP)

          Control variable for writing the test/debug
          wind fields to disk files (IOUTD)
          (0=Do not write, 1=write)        Default: 0       ! IOUTD =  0  !

          Number of levels, starting at the surface,
          to print (NZPRN2)                Default: 1       ! NZPRN2 =  1  !

          Print the INTERPOLATED wind components ?
          (IPR0) (0=no, 1=yes)             Default: 0       !  IPR0 =  1  !

          Print the TERRAIN ADJUSTED surface wind
          components ?
          (IPR1) (0=no, 1=yes)             Default: 0       !  IPR1 =  1  !

          Print the SMOOTHED wind components and
          the INITIAL DIVERGENCE fields ?
          (IPR2) (0=no, 1=yes)             Default: 0       !  IPR2 =  1  !

          Print the FINAL wind speed and direction
          fields ?
          (IPR3) (0=no, 1=yes)             Default: 0       !  IPR3 =  1  !

          Print the FINAL DIVERGENCE fields ?
          (IPR4) (0=no, 1=yes)             Default: 0       !  IPR4 =  1  !

          Print the winds after KINEMATIC effects
          are added ?
          (IPR5) (0=no, 1=yes)             Default: 0       !  IPR5 =  1  !

          Print the winds after the FROUDE NUMBER
          adjustment is made ?
          (IPR6) (0=no, 1=yes)             Default: 0       !  IPR6 =  1  !

          Print the winds after SLOPE FLOWS
          are added ?
          (IPR7) (0=no, 1=yes)             Default: 0       !  IPR7 =  1  !

          Print the FINAL wind field components ?
          (IPR8) (0=no, 1=yes)             Default: 0       !  IPR8 =  1  !

!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 4 -- Meteorological data options
--------------

### NO OBSERVATION MODE
                                 (NOOBS)  Default: 0     ! NOOBS =  2   !
          0 = Use surface, overwater, and upper air stations
          1 = Use surface and overwater stations (no upper air observations)
              Use MM4/MM5/M3D for upper air data
          2 = No surface, overwater, or upper air observations
              Use MM4/MM5/M3D for surface, overwater, and upper air data

### NUMBER OF SURFACE & PRECIP. METEOROLOGICAL STATIONS

       Number of surface stations   (NSSTA)  No default     ! NSSTA =  0 !

       Number of precipitation stations
       (NPSTA=-1: flag for use of MM5/M3D precip data)
                                    (NPSTA)  No default    ! NPSTA=-1 !

### CLOUD DATA OPTIONS
       Gridded cloud fields:
                                   (ICLOUD)  Default: 0     ! ICLOUD =  3  !
       ICLOUD = 0 - Gridded clouds not used
       ICLOUD = 1 - Gridded CLOUD.DAT generated as OUTPUT
       ICLOUD = 2 - Gridded CLOUD.DAT read as INPUT
       ICLOUD = 3 - Gridded cloud cover from Prognostic Rel. Humidity

### FILE FORMATS

       Surface meteorological data file format
                                   (IFORMS)  Default: 2     ! IFORMS =  2  !
       (1 = unformatted (e.g., SMERGE output))
       (2 = formatted   (free-formatted user input))

       Precipitation data file format
                                   (IFORMP)  Default: 2     ! IFORMP =  2  !
       (1 = unformatted (e.g., PMERGE output))
       (2 = formatted   (free-formatted user input))

       Cloud data file format
                                   (IFORMC)  Default: 2     ! IFORMC =  2  !
       (1 = unformatted - CALMET unformatted output)
       (2 = formatted   - free-formatted CALMET output or user input)

!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 5 -- Wind Field Options and Parameters
--------------


### WIND FIELD MODEL OPTIONS
       Model selection variable (IWFCOD)     Default: 1      ! IWFCOD =  0  !
          0 = Objective analysis only
          1 = Diagnostic wind module

       Compute Froude number adjustment
       effects ? (IFRADJ)                    Default: 1      ! IFRADJ =  1  !
       (0 = NO, 1 = YES)

       Compute kinematic effects ? (IKINE)   Default: 0      ! IKINE  =  1  !
       (0 = NO, 1 = YES)

       Use O'Brien procedure for adjustment
       of the vertical velocity ? (IOBR)     Default: 0      ! IOBR =  1  !
       (0 = NO, 1 = YES)

       Compute slope flow effects ? (ISLOPE) Default: 1      ! ISLOPE  =  1  !
       (0 = NO, 1 = YES)

       Extrapolate surface wind observations
       to upper layers ? (IEXTRP)            Default: -4     ! IEXTRP =  1  !
       (1 = no extrapolation is done,
        2 = power law extrapolation used,
        3 = user input multiplicative factors
            for layers 2 - NZ used (see FEXTRP array)
        4 = similarity theory used
        -1, -2, -3, -4 = same as above except layer 1 data
            at upper air stations are ignored

       Extrapolate surface winds even
       if calm? (ICALM)                      Default: 0      ! ICALM  =  0  !
       (0 = NO, 1 = YES)

       Layer-dependent biases modifying the weights of
       surface and upper air stations (BIAS(NZ))
         -1<=BIAS<=1
       Negative BIAS reduces the weight of upper air stations
         (e.g. BIAS=-0.1 reduces the weight of upper air stations
       by 10%; BIAS= -1, reduces their weight by 100 %)
       Positive BIAS reduces the weight of surface stations
         (e.g. BIAS= 0.2 reduces the weight of surface stations
       by 20%; BIAS=1 reduces their weight by 100%)
       Zero BIAS leaves weights unchanged (1/R**2 interpolation)
       Default: NZ*0
                               ! BIAS =  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0  !

       Minimum distance from nearest upper air station
       to surface station for which extrapolation
       of surface winds at surface station will be allowed
       (RMIN2: Set to -1 for IEXTRP = 4 or other situations
        where all surface stations should be extrapolated)
                                              Default: 4.    ! RMIN2 = -1.0 !

       Use gridded prognostic wind field model
       output fields as input to the diagnostic
       wind field model (IPROG)              Default: 0      ! IPROG = 13  !
       (0 = No, [IWFCOD = 0 or 1]
        1 = Yes, use CSUMM prog. winds as Step 1 field, [IWFCOD = 0]
        2 = Yes, use CSUMM prog. winds as initial guess field [IWFCOD = 1]
        3 = Yes, use winds from MM4.DAT file as Step 1 field [IWFCOD = 0]
        4 = Yes, use winds from MM4.DAT file as initial guess field [IWFCOD = 1]
        5 = Yes, use winds from MM4.DAT file as observations [IWFCOD = 1]
        13 = Yes, use winds from MM5/M3D.DAT file as Step 1 field [IWFCOD = 0]
        14 = Yes, use winds from MM5/M3D.DAT file as initial guess field [IWFCOD = 1]
        15 = Yes, use winds from MM5/M3D.DAT file as observations [IWFCOD = 1]

       Timestep (hours) of the prognostic
       model input data   (ISTEPPG)          Default: 1      ! ISTEPPG =  6   !

### RADIUS OF INFLUENCE PARAMETERS

       Use varying radius of influence       Default: F      ! LVARY =  F!
       (if no stations are found within RMAX1,RMAX2,
        or RMAX3, then the closest station will be used)

       Maximum radius of influence over land
       in the surface layer (RMAX1)          No default      ! RMAX1 =  2. !
                                             Units: km
       Maximum radius of influence over land
       aloft (RMAX2)                         No default      ! RMAX2 =  2. !
                                             Units: km
       Maximum radius of influence over water
       (RMAX3)                               No default      ! RMAX3 =  2. !
                                             Units: km


### OTHER WIND FIELD INPUT PARAMETERS

       Minimum radius of influence used in
       the wind field interpolation (RMIN)   Default: 0.1    ! RMIN =0.1!
                                             Units: km
       Radius of influence of terrain
       features (TERRAD)                     No default      ! TERRAD = 2. !

                                             Units: km
       Relative weighting of the first
       guess field and observations in the
       SURFACE layer (R1)                    No default      ! R1 =2. !
       (R1 is the distance from an           Units: km
       observational station at which the
       observation and first guess field are
       equally weighted)

       Relative weighting of the first
       guess field and observations in the
       layers ALOFT (R2)                     No default      ! R2 = 2. !
       (R2 is applied in the upper layers    Units: km
       in the same manner as R1 is used in
       the surface layer).

       Relative weighting parameter of the
       prognostic wind field data (RPROG)    No default      ! RPROG = 3. !
       (Used only if IPROG = 1)              Units: km
       ------------------------

       Maximum acceptable divergence in the
       divergence minimization procedure
       (DIVLIM)                              Default: 5.E-6  ! DIVLIM= 5.0E-06 !

       Maximum number of iterations in the
       divergence min. procedure (NITER)     Default: 50     ! NITER =  50  !

       Number of passes in the smoothing
       procedure (NSMTH(NZ))
       NOTE: NZ values must be entered
            Default: 2,(mxnz-1)*4 
      ! NSMTH =  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0 ,  0, 0,0,0,0,0,0  !

       Maximum number of stations used in
       each layer for the interpolation of
       data to a grid point (NINTR2(NZ))
       NOTE: NZ values must be entered       Default: 99.    
      ! NINTR2 =  5  ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5, 5, 5, 5, 5, 5, 5  !

       Critical Froude number (CRITFN)       Default: 1.0    ! CRITFN = 1. !

       Empirical factor controlling the
       influence of kinematic effects
       (ALPHA)                               Default: 0.1    ! ALPHA = 0.1 !

       Multiplicative scaling factor for
       extrapolation of surface observations
       to upper layers (FEXTR2(NZ))          Default: NZ*0.0 
      ! FEXTR2 = 0., 0., 0., 0., 0., 0., 0., 0., 0., 0. !
       (Used only if IEXTRP = 3 or -3)


### BARRIER INFORMATION

       Number of barriers to interpolation
       of the wind fields (NBAR)             Default: 0      ! NBAR =  0  !

       Level (1 to NZ) up to which barriers
       apply (KBAR)                          Default: NZ     * KBAR = NZ *

       THE FOLLOWING 4 VARIABLES ARE INCLUDED
       ONLY IF NBAR > 0
       NOTE: NBAR values must be entered     No defaults
             for each variable               Units: km

          X coordinate of BEGINNING
          of each barrier (XBBAR(NBAR))      ! XBBAR = 43.02,46.02 !
          Y coordinate of BEGINNING
          of each barrier (YBBAR(NBAR))      ! YBBAR = 108.16,83.16 !

          X coordinate of ENDING
          of each barrier (XEBAR(NBAR))      ! XEBAR = 23.02,-24.98 !
          Y coordinate of ENDING
          of each barrier (YEBAR(NBAR))      ! YEBAR = 85.16,-126.84 !


 ### DIAGNOSTIC MODULE DATA INPUT OPTIONS

       Surface temperature (IDIOPT1)         Default: 0      ! IDIOPT1 =  0  !
          0 = Compute internally from
              hourly surface observations
          1 = Read preprocessed values from
              a data file (DIAG.DAT)

          Surface met. station to use for
          the surface temperature (ISURFT)   No default     ! ISURFT =  -1 !
          (Must be a value from 1 to NSSTA)
          (Used only if IDIOPT1 = 0)
          --------------------------

       Domain-averaged temperature lapse
       rate (IDIOPT2)                        Default: 0     ! IDIOPT2 =  0  !
          0 = Compute internally from
              twice-daily upper air observations
          1 = Read hourly preprocessed values
              from a data file (DIAG.DAT)

          Upper air station to use for
          the domain-scale lapse rate (IUPT) No default     ! IUPT   =  -1 !
          (Must be a value from 1 to NUSTA)
          (Used only if IDIOPT2 = 0)
          --------------------------

          Depth through which the domain-scale
          lapse rate is computed (ZUPT)      Default: 200.  ! ZUPT = 200. !
          (Used only if IDIOPT2 = 0)         Units: meters
          --------------------------

       Domain-averaged wind components
       (IDIOPT3)                             Default: 0     ! IDIOPT3 =  0  !
          0 = Compute internally from
              twice-daily upper air observations
          1 = Read hourly preprocessed values
              a data file (DIAG.DAT)

          Upper air station to use for
          the domain-scale winds (IUPWND)    Default: -1    ! IUPWND = 2  !
          (Must be a value from -1 to NUSTA)
          (Used only if IDIOPT3 = 0)
          --------------------------

          Bottom and top of layer through
          which the domain-scale winds
          are computed
          (ZUPWND(1), ZUPWND(2))        Defaults: 1., 1000. ! ZUPWND= 1., 1000. !
          (Used only if IDIOPT3 = 0)    Units: meters
          --------------------------

       Observed surface wind components
       for wind field module (IDIOPT4)  Default: 0     ! IDIOPT4 =  0  !
          0 = Read WS, WD from a surface
              data file (SURF.DAT)
          1 = Read hourly preprocessed U, V from
              a data file (DIAG.DAT)

       Observed upper air wind components
       for wind field module (IDIOPT5)  Default: 0     ! IDIOPT5 =  0  !
          0 = Read WS, WD from an upper
              air data file (UP1.DAT, UP2.DAT, etc.)
          1 = Read hourly preprocessed U, V from
              a data file (DIAG.DAT)

       LAKE BREEZE INFORMATION

          Use Lake Breeze Module  (LLBREZE)
                                           Default: F      ! LLBREZE = F !

           Number of lake breeze regions (NBOX)            ! NBOX =  0  !

        X Grid line 1 defining the region of interest
                                                        ! XG1 = 0. !
        X Grid line 2 defining the region of interest
                                                        ! XG2 = 0. !
        Y Grid line 1 defining the region of interest
                                                        ! YG1 = 0. !
        Y Grid line 2 defining the region of interest
                                                        ! YG2 = 0. !

         X Point defining the coastline (Straight line)
                   (XBCST)  (KM)   Default: none    ! XBCST = 0. !

         Y Point defining the coastline (Straight line)
                   (YBCST)  (KM)   Default: none    ! YBCST = 0. !

         X Point defining the coastline (Straight line)
                   (XECST)  (KM)   Default: none    ! XECST = 0. !

         Y Point defining the coastline (Straight line)
                   (YECST)  (KM)   Default: none    ! YECST = 0. !


       Number of stations in the region     Default: none ! NLB =  0 ! 
       (Surface stations + upper air stations)

       Station ID's  in the region   (METBXID(NLB))
       (Surface stations first, then upper air stations)
         ! METBXID =  0 !

!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 6 -- Mixing Height, Temperature and Precipitation Parameters
--------------

### EMPIRICAL MIXING HEIGHT CONSTANTS

       Neutral, mechanical equation
       (CONSTB)                              Default: 1.41   ! CONSTB = 1.41 !
       Convective mixing ht. equation
       (CONSTE)                              Default: 0.15   ! CONSTE = 0.15 !
       Stable mixing ht. equation
       (CONSTN)                              Default: 2400.  ! CONSTN = 2400.!
       Overwater mixing ht. equation
       (CONSTW)                              Default: 0.16   ! CONSTW = 0.16 !
       Absolute value of Coriolis
       parameter (FCORIOL)                   Default: 1.E-4  ! FCORIOL = 1.0E-04!
                                             Units: (1/s)

### SPATIAL AVERAGING OF MIXING HEIGHTS

       Conduct spatial averaging
       (IAVEZI)  (0=no, 1=yes)               Default: 1      ! IAVEZI =  1  !

       Max. search radius in averaging
       process (MNMDAV)                      Default: 1      ! MNMDAV = 1000 !
                                             Units: Grid
                                                    cells
       Half-angle of upwind looking cone
       for averaging (HAFANG)                Default: 30.    ! HAFANG = 30. !
                                             Units: deg.
       Layer of winds used in upwind
       averaging (ILEVZI)                    Default: 1      ! ILEVZI =  1  !
       (must be between 1 and NZ)

### OTHER MIXING HEIGHT VARIABLES

       Minimum potential temperature lapse
       rate in the stable layer above the
       current convective mixing ht.         Default: 0.001  ! DPTMIN = 0.001 !
       (DPTMIN)                              Units: deg. K/m
       Depth of layer above current conv.
       mixing height through which lapse     Default: 200.   ! DZZI = 20. !
       rate is computed (DZZI)               Units: meters

       Minimum overland mixing height        Default:  50.   ! ZIMIN = 20. !
       (ZIMIN)                               Units: meters
       Maximum overland mixing height        Default: 3000.  ! ZIMAX = 2500. !
       (ZIMAX)                               Units: meters
       Minimum overwater mixing height       Default:   50.  ! ZIMINW = 20. !
       (ZIMINW) -- (Not used if observed     Units: meters
       overwater mixing hts. are used)
       Maximum overwater mixing height       Default: 3000.  ! ZIMAXW = 2500. !
       (ZIMAXW) -- (Not used if observed     Units: meters
       overwater mixing hts. are used)


### TEMPERATURE PARAMETERS

       3D temperature from observations or
       from prognostic data? (ITPROG)        Default:0         !ITPROG =  2   !

          0 = Use Surface and upper air stations
              (only if NOOBS = 0)
          1 = Use Surface stations (no upper air observations)
              Use MM5/M3D for upper air data
              (only if NOOBS = 0,1)
          2 = No surface or upper air observations
              Use MM5/M3D for surface and upper air data
              (only if NOOBS = 0,1,2)

       Interpolation type
       (1 = 1/R ; 2 = 1/R**2)                Default:1         ! IRAD =  1  !

       Radius of influence for temperature
       interpolation (TRADKM)                Default: 500.     ! TRADKM =10 !
                                             Units: km

       Maximum Number of stations to include
       in temperature interpolation (NUMTS)  Default: 5        ! NUMTS = 5  !

       Conduct spatial averaging of temp-
       eratures (IAVET)  (0=no, 1=yes)         Default: 1     ! IAVET =  1  !
       (will use mixing ht MNMDAV,HAFANG
        so make sure they are correct)

       Default temperature gradient        Default: -.0098 ! TGDEFB = -0.0098 !
       below the mixing height over
       water (K/m) (TGDEFB)

       Default temperature gradient        Default: -.0045 ! TGDEFA = -0.0045 !
       above the mixing height over
       water (K/m) (TGDEFA)

       Beginning (JWAT1) and ending (JWAT2)
       land use categories for temperature                    ! JWAT1 =  55  !
       interpolation over water -- Make                       ! JWAT2 =  55  !
       bigger than largest land use to disable

### PRECIP INTERPOLATION PARAMETERS

       Method of interpolation (NFLAGP)      Default = 2    ! NFLAGP =  2  !
        (1=1/R,2=1/R**2,3=EXP/R**2)
       Radius of Influence (km) (SIGMAP)     Default = 100.0  ! SIGMAP =100 !
        (0.0 => use half dist. btwn
         nearest stns w & w/out
         precip when NFLAGP = 3)
       Minimum Precip. Rate Cutoff (mm/hr)   Default = 0.01  ! CUTP = 0.01 !
        (values < CUTP = 0.0 mm/hr)
!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 7 -- Surface meteorological station parameters
--------------

     SURFACE STATION VARIABLES
     (One record per station --  5  records in all)


| Name<sup>1</sup> |  Station_Code<sup>2</sup>  |  X_coord.(km) | Y_coord.(km) |Time_zone Anem.Ht.(m)|
|-|-|-|-|-|
|! SS1  ='BnQi' |  466880  | 47.031  |153.302     |    -8  10 !|
|! SS2  ='DnSh' |  466900 |  47.860 | 171.692   |      -8  10 !|
|! SS3  ='AnBu' |  466910 |  55.949 | 173.908   |      -8  10 !|
|...|||
|! SS81 ='YoHe' |  460700 |  49.120 | 148.973    |     -8  10 !|
-------------------
      1
        Four character string for station name
        (MUST START IN COLUMN 9)

      2
        Six digit integer for station ID

!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 8 -- Upper air meteorological station parameters
--------------

     UPPER AIR STATION VARIABLES
     (One record per station --  3  records in all)

|Name<sup>1</sup>|   Station_Code<sup>2</sup>|    X_coord.(km)|  Y_coord.(km)| Time_zone|
|-|-|-|-|--------------------------------
|! US1  ='BnQi' |   46692   |    48.020 |  159.158 | -8 !|
|! US2  ='HuLn' |   46699   |   66.020  | 42.158 |  -8 !|
-------------------
      1
        Four character string for station name
        (MUST START IN COLUMN 9)

      2
        Five digit integer for station ID

!END!


-------------------------------------------------------------------------------

## INPUT GROUP: 9 -- Precipitation station parameters
--------------

PRECIPITATION STATION VARIABLES

(One record per station --  16  records in all)

(NOT INCLUDED IF NPSTA = 0)

|Name<sup>1</sup>   Station_Code<sup>2</sup>    X_coord.(km)  Y_coord.(km)
|------------------------------------
|! PS1  ='BnQi'   466880   47.031  153.302 !
|! PS2  ='DnSh'   466900   47.860  171.692 !
|! PS3  ='AnBu'   466910   55.949  173.908 !
|! PS4  ='TaiB'   466920   54.426  157.679 !
|! PS5  ='ZhZH'   466930   57.575  171.521 !
|! PS6  ='KeLn'   466940   77.283  167.968 !
|! PS7  ='PnJY'   466950   25.141 -175.140 !
|! PS8  ='HLia'   466990   63.159   39.884 !|
|! PS9  ='SuAo'   467060   90.120  108.821 !|
|! PS10 ='YiLn'   467080   78.502  127.072 !|
|! PS11 ='DngJ'   467300 -136.148  -38.257 !|
|! PS12 ='PenH'   467350 -146.464   -3.787 !|
|! PS13 ='TNan'   467410  -82.330  -66.772 !|
|! PS14 ='YnKn'   467420  -78.932  -61.911 !|
|! PS15 ='GaXg'   467440  -71.739 -114.313 !|
|! PS16 ='JiYi'   467480  -57.951  -11.506 !|
|! PS17 ='TZho'   467490  -31.087   60.024 !|
|! PS18 ='ALSh'   467530  -19.050  -10.767 !|
|! PS19 ='DaWu'   467540  -11.629 -138.571 !|
|! PS20 ='YShn'   467550   -4.103  -13.326 !|
|! PS21 ='XnZh'   467570    3.574  135.100 !|
|! PS22 ='HnCh'   467590  -28.435 -177.312 !|
|! PS23 ='ChgG'   467610   37.658  -57.052 !|
|! PS24 ='LanY'   467620   55.496 -174.671 !|
|! PS25 ='MnTn'   467650   -7.920   30.177 !|
|! PS26 ='TDon'   467660   14.781  -94.988 !|
|! PS27 ='Wchi'   467770  -47.218   72.614 !|
|! PS28 ='QiGu'   467780  -99.999  -99.999 !|
|! PS29 ='MaTz'   467990  -90.39   283.999 !|
-------------------
      1
        Four character string for station name
        (MUST START IN COLUMN 9)

      2
        Six digit station code composed of state
        code (first 2 digits) and station ID (last
        4 digits)

!END!
