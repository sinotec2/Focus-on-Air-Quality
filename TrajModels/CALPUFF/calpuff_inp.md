---
layout: default
title: calpuff.inp
nav_order: 2
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-03-22 08:56:43
tags: cpuff 
---

# calpuff.inp
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

    CALPUFF test case run - 3 point sources
    24-Hour Simulation using CALMET met. data
    Gridded receptors on 35x55  9-km met grid
---------------- Run title (3 lines) ------------------------------------------

                    CALPUFF MODEL CONTROL FILE
                    --------------------------

-------------------------------------------------------------------------------

## INPUT GROUP: 0 -- Input and Output File Names
--------------
### Main I/O Files
---

|Default Name|  Type|          File_Name|說明|
|-|-|-|-|
|CALMET.DAT|    input|    ! METDAT =data/calmet_20200415.dat !|下列5項擇一。CALMET處理結果|
|ISCMET.DAT|    input|    * ISCDAT =             *|ISC氣象檔|
|PLMMET.DAT|    input|    * PLMDAT =             *|AUSPLUME(澳洲煙陣模式)氣象檔|
|PROFILE.DAT|   input|    * PRFDAT =             *|aermet或ctdm垂直剖面|
|SURFACE.DAT|   input|    * SFCDAT =             *|同上之地面氣象檔|
|RESTARTB.DAT|  input|    ! RSTARTB= restart_20200425.dat ! |濃度起始瞬時煙陣濃度|
|CALPUFF.LST|   output|   ! PUFLST =CALPUFF.LST  !|執行訊息檔|
|CONC.DAT|      output|   ! CONDAT =CALPUFF.CON  !|3維網格濃度|
|DFLX.DAT|      output|   ! DFDAT  =CALPUFF.DFX  !|乾沉降|
|WFLX.DAT|      output|   ! WFDAT  =CALPUFF.WFX  !|溼沉降
|VISB.DAT|      output|   * VISDAT =             *|能見度|
|TK2D.DAT|      output|   * T2DDAT =             *|2m溫度|
|RHO2D.DAT|     output|   * RHODAT =             *|空氣密度|
|RESTARTE.DAT|  output|   ! RSTARTE=  restart_20200427.dat  !|模擬結束瞬時之煙陣濃度|

--------------------------------------------------------------------------------

### Hourly Emission Files
--------------

|Default Name|  Type|          File_Name|說明|
|-|-|-|-|
|PTEMARB.DAT|   input|    * PTDAT  = ../PTEMTAIC.DAT*|點源|
|VOLEMARB.DAT|  input|    * VOLDAT =             *|體源|
|BAEMARB.DAT|   input|    * ARDAT  =             *|面源|
|LNEMARB.DAT|   input|    * LNDAT  =             *|線源|

--------------------------------------------------------------------------------

### Other Files
-----------

|Default Name|  Type|          File_Name|說明|
|-|-|-|-|
|OZONE.DAT|     input|    * OZDAT  = ../OZONE.DAT *|測站逐時臭氧值|
|VD.DAT|        input|    * VDDAT  =             *|沉降速度|
|CHEM.DAT|      input|    * CHEMDAT=             *|化學反應|
|H2O2.DAT|      input|    * H2O2DAT=             *|逐時過氧化氫濃度|
|HILL.DAT|      input|    * HILDAT=             *|CTDM山高|
|HILLRCT.DAT|   input|    * RCTDAT=             *|CTDM複雜地形接受點|
|COASTLN.DAT|   input|    * CSTDAT=             *|海岸線|
|FLUXBDY.DAT|   input|    * BDYDAT=             *|邊界通量|
|BCON.DAT|      input|    * BCNDAT=             *|邊界濃度|
|DEBUG.DAT|     output|   ! DEBUG = debug.out   !|偵錯訊息|
|MASSFLX.DAT|   output|   * FLXDAT=             *|質量通量|
|MASSBAL.DAT|   output|   ! BALDAT=massbal.dat  !|質量平衡|
|FOG.DAT|       output|   * FOGDAT=             *|霧|
|RISE.DAT|      output|   * RISDAT=             *|煙流上升|

--------------------------------------------------------------------------------
      All file names will be converted to lower case if LCFILES = T
      Otherwise, if LCFILES = F, file names will be converted to UPPER CASE
               T = lower case      ! LCFILES = T !
               F = UPPER CASE
      NOTE: (1) file/path names can be up to 70 characters in length


### Provision for multiple input files
----------------------------------
     Number of CALMET.DAT Domains (NMETDOM)
                                     Default: 1       ! NMETDOM =   1   !

     Number of CALMET.DAT files for run (NMETDAT)
                                     Default: 1       ! NMETDAT =   1   !

     Number of PTEMARB.DAT files for run (NPTDAT)
                                     Default: 0       ! NPTDAT =  0  !

     Number of BAEMARB.DAT files for run (NARDAT)
                                     Default: 0       ! NARDAT =  0  !

     Number of VOLEMARB.DAT files for run (NVOLDAT)
                                     Default: 0       ! NVOLDAT =  0  !
      !END!


### Subgroup (0a) CALMET.DAT filenames
-------------

      The following CALMET.DAT filenames are processed in sequence if NMETDAT>1

|Default Name|  Type|          File_Name|
|-|-|-|
| none|         input|    * METDAT=../CMET1.DAT  *   *END\*|
| none|         input|    * METDAT=../CMET2.DAT  *   *END\*|
| none|         input|    * METDAT=../CMET3.DAT  *   *END\*|
| none|         input|    * METDAT=../CMET4.DAT  *   *END\*|

--------------------------------------------------------------------------------

## INPUT GROUP: 1 -- General Run Control Parameters
--------------
### Run all periods
    Option to run all periods found
    in the met. file     (METRUN)   Default: 0       ! METRUN =   0  !

         METRUN = 0 - Run period explicitly defined below
         METRUN = 1 - Run all periods in met. file

### Start and end
     Starting date:    Year   (IBYR)  --    No default   ! IBYR  =  2020  !
                       Month  (IBMO)  --    No default   ! IBMO  =  04  !
                       Day    (IBDY)  --    No default   ! IBDY  =  15  !
     Starting time:    Hour   (IBHR)  --    No default   ! IBHR  =  0  !
                       Minute (IBMIN) --    No default   ! IBMIN =  0  !
                       Second (IBSEC) --    No default   ! IBSEC =  0  !

     Ending date:      Year   (IEYR)  --    No default   ! IEYR  =  2020  !
                       Month  (IEMO)  --    No default   ! IEMO  =  04 !
                       Day    (IEDY)  --    No default   ! IEDY  =  27  !
     Ending time:      Hour   (IEHR)  --    No default   ! IEHR  =  0  !
                       Minute (IEMIN) --    No default   ! IEMIN =  0  !
                       Second (IESEC) --    No default   ! IESEC =  0  !

### Time zone
     (These are only used if METRUN = 0)
							! ABTZ= UTC+0000 !
     Base time zone        (XBTZ) -- No default       * XBTZ=  0.  *
     The zone is the number of hours that must be
     ADDED to the time to obtain UTC (or GMT)
     Examples: PST = 8., MST = 7.
               CST = 6., EST = 5.

### Length of modeling time-step
     Length of modeling time-step (seconds)
     Equal to update period in the primary
     meteorological data files, or an
     integer fraction of it (1/2, 1/3 ...)
     Must be no larger than 1 hour
     (NSECDT)                        Default:3600     ! NSECDT =3600   !
                                     Units: seconds

### Number of chemical species
     Number of chemical species (NSPEC)
                                     Default: 5       ! NSPEC =  8   !

     Number of chemical species
     to be emitted  (NSE)            Default: 3       ! NSE =  8   !

     Flag to stop run after
     SETUP phase (ITEST)             Default: 2       ! ITEST =  2   !
     (Used to allow checking
     of the model inputs, files, etc.)
           ITEST = 1 - STOPS program after SETUP phase
           ITEST = 2 - Continues with execution of program
                       after SETUP

### Restart Configuration:

        Control flag (MRESTART)      Default: 0       ! MRESTART = 2 !

           0 = Do not read or write a restart file
           1 = Read a restart file at the beginning of
               the run
           2 = Write a restart file during run
           3 = Read a restart file at beginning of run
               and write a restart file during run

        Number of periods in Restart
        output cycle (NRESPD)        Default: 0       ! NRESPD =  0   !

           0 = File written only at last period
          >0 = File updated every NRESPD periods

### Meteorological Data Formats
      Meteorological Data Format (METFM)

                                     Default: 1       ! METFM =  1   !

           METFM = 1 - CALMET binary file (CALMET.MET)
           METFM = 2 - ISC ASCII file (ISCMET.MET)
           METFM = 3 - AUSPLUME ASCII file (PLMMET.MET)
           METFM = 4 - CTDM plus tower file (PROFILE.DAT) and
                       surface parameters file (SURFACE.DAT)
           METFM = 5 - AERMET tower file (PROFILE.DAT) and
                       surface parameters file (SURFACE.DAT)

     Meteorological Profile Data Format (MPRFFM)
            (used only for METFM = 1, 2, 3)
                                     Default: 1       ! MPRFFM =  1   !

           MPRFFM = 1 - CTDM plus tower file (PROFILE.DAT)
           MPRFFM = 2 - AERMET tower file (PROFILE.DAT)

### PG sigma-y adjustment
     PG sigma-y is adjusted by the factor (AVET/PGTIME)**0.2
     Averaging Time (minutes) (AVET)
                                     Default: 60.0    ! AVET = 60. !
     PG Averaging Time (minutes) (PGTIME)
                                     Default: 60.0    ! PGTIME = 60. !

      !END!


-------------------------------------------------------------------------------

## INPUT GROUP: 2 -- Technical options
--------------

### Plume Behaviors
     Vertical distribution used in the
     near field (MGAUSS)                   Default: 1     ! MGAUSS =  1   !
        0 = uniform
        1 = Gaussian

     Terrain adjustment method
     (MCTADJ)                              Default: 3     ! MCTADJ =  3   !
        0 = no adjustment
        1 = ISC-type of terrain adjustment
        2 = simple, CALPUFF-type of terrain
            adjustment 
        3 = partial plume path adjustment

     Subgrid-scale complex terrain
     flag (MCTSG)                          Default: 0     ! MCTSG =  0   !
        0 = not modeled
        1 = modeled

     Near-field puffs modeled as
     elongated slugs? (MSLUG)              Default: 0     ! MSLUG =  1   !
        0 = no
        1 = yes (slug model used)

     Transitional plume rise modeled?
     (MTRANS)                              Default: 1     ! MTRANS =  1   !
        0 = no  (i.e., final rise only)
        1 = yes (i.e., transitional rise computed)

     Stack tip downwash? (MTIP)            Default: 1     ! MTIP =  1  !
        0 = no  (i.e., no stack tip downwash)
        1 = yes (i.e., use stack tip downwash)

     Method used to compute plume rise for
     point sources not subject to building
     downwash? (MRISE)                     Default: 1     ! MRISE =   1  !
        1 = Briggs plume rise
        2 = Numerical plume rise

     Method used to simulate building
     downwash? (MBDW)                      Default: 1     ! MBDW =   1  !
        1 = ISC method
        2 = PRIME method

     Vertical wind shear modeled above
     stack top (modified Briggs plume rise)?
     (MSHEAR)                              Default: 0     ! MSHEAR =  0  !
        0 = no  (i.e., vertical wind shear not modeled)
        1 = yes (i.e., vertical wind shear modeled)

     Puff splitting allowed? (MSPLIT)      Default: 0     ! MSPLIT =  0  !
        0 = no (i.e., puffs not split)
        1 = yes (i.e., puffs are split)

### Chemistry and Deposition
     Chemical mechanism flag (MCHEM)       Default: 1     ! MCHEM =  1   !
        0 = chemical transformation not
            modeled
        1 = transformation rates computed
            internally (MESOPUFF II scheme)
        2 = user-specified transformation
            rates used
        3 = transformation rates computed
            internally (RIVAD/ARM3 scheme)
        4 = secondary organic aerosol formation
            computed (MESOPUFF II scheme for OH)

     Aqueous phase transformation flag (MAQCHEM)
     (Used only if MCHEM = 1, or 3)        Default: 0     ! MAQCHEM =  0   !
        0 = aqueous phase transformation
            not modeled
        1 = transformation rates adjusted
            for aqueous phase reactions

     Wet removal modeled ? (MWET)          Default: 1     ! MWET =  1   !
        0 = no
        1 = yes

     Dry deposition modeled ? (MDRY)       Default: 1     ! MDRY =  1   !
        0 = no
        1 = yes
        (dry deposition method specified
         for each species in Input Group 3)


     Gravitational settling (plume tilt)
     modeled ? (MTILT)                     Default: 0     ! MTILT =  0   !
        0 = no
        1 = yes
        (puff center falls at the gravitational
         settling velocity for 1 particle species)

     Restrictions:
         - MDRY  = 1
         - NSPEC = 1  (must be particle species as well)
         - sg    = 0  GEOMETRIC STANDARD DEVIATION in Group 8 is
                      set to zero for a single particle diameter

### Plume Dispersion
     Method used to compute dispersion
     coefficients (MDISP)                  Default: 3     ! MDISP =  3   !

        1 = dispersion coefficients computed from measured values
            of turbulence, sigma v, sigma w
        2 = dispersion coefficients from internally calculated 
            sigma v, sigma w using micrometeorological variables
            (u*, w*, L, etc.)
        3 = PG dispersion coefficients for RURAL areas (computed using
            the ISCST multi-segment approximation) and MP coefficients in
            urban areas
        4 = same as 3 except PG coefficients computed using
            the MESOPUFF II eqns.
        5 = CTDM sigmas used for stable and neutral conditions.
            For unstable conditions, sigmas are computed as in
            MDISP = 3, described above.  MDISP = 5 assumes that
            measured values are read

     Sigma-v/sigma-theta, sigma-w measurements used? (MTURBVW)
     (Used only if MDISP = 1 or 5)         Default: 3     ! MTURBVW =  3  !
        1 = use sigma-v or sigma-theta measurements
            from PROFILE.DAT to compute sigma-y
            (valid for METFM = 1, 2, 3, 4, 5)
        2 = use sigma-w measurements
            from PROFILE.DAT to compute sigma-z
            (valid for METFM = 1, 2, 3, 4, 5)
        3 = use both sigma-(v/theta) and sigma-w
            from PROFILE.DAT to compute sigma-y and sigma-z
            (valid for METFM = 1, 2, 3, 4, 5)
        4 = use sigma-theta measurements
            from PLMMET.DAT to compute sigma-y
            (valid only if METFM = 3)

     Back-up method used to compute dispersion
     when measured turbulence data are
     missing (MDISP2)                      Default: 3     ! MDISP2 =  3  !
     (used only if MDISP = 1 or 5)
        2 = dispersion coefficients from internally calculated 
            sigma v, sigma w using micrometeorological variables
            (u*, w*, L, etc.)
        3 = PG dispersion coefficients for RURAL areas (computed using
            the ISCST multi-segment approximation) and MP coefficients in
            urban areas
        4 = same as 3 except PG coefficients computed using
            the MESOPUFF II eqns.

     [DIAGNOSTIC FEATURE]
     Method used for Lagrangian timescale for Sigma-y
     (used only if MDISP=1,2 or MDISP2=1,2)
     (MTAULY)                              Default: 0     ! MTAULY =  0  !
        0 = Draxler default 617.284 (s)
        1 = Computed as Lag. Length / (.75 q) -- after SCIPUFF
       10 < Direct user input (s)             -- e.g., 306.9


     [DIAGNOSTIC FEATURE]
     Method used for Advective-Decay timescale for Turbulence
     (used only if MDISP=2 or MDISP2=2)
     (MTAUADV)                             Default: 0     ! MTAUADV =  0  !
        0 = No turbulence advection
        1 = Computed (OPTION NOT IMPLEMENTED)
       10 < Direct user input (s)   -- e.g., 800


     Method used to compute turbulence sigma-v &
     sigma-w using micrometeorological variables
     (Used only if MDISP = 2 or MDISP2 = 2)
     (MCTURB)                              Default: 1     ! MCTURB =  1  !
        1 = Standard CALPUFF subroutines
        2 = AERMOD subroutines

     PG sigma-y,z adj. for roughness?      Default: 0     ! MROUGH =  0  !
     (MROUGH)
        0 = no
        1 = yes

     Partial plume penetration of          Default: 1     ! MPARTL =  1  !
     elevated inversion modeled for
     point sources?
     (MPARTL)
        0 = no
        1 = yes

     Partial plume penetration of          Default: 1     ! MPARTLBA =  0  !
     elevated inversion modeled for
     buoyant area sources?
     (MPARTLBA)
        0 = no
        1 = yes

     Strength of temperature inversion     Default: 0     ! MTINV =  0  !
     provided in PROFILE.DAT extended records?
     (MTINV)
        0 = no (computed from measured/default gradients)
        1 = yes

     PDF used for dispersion under convective conditions?
                                           Default: 0     ! MPDF =  0  !
     (MPDF)
        0 = no
        1 = yes

     Sub-Grid TIBL module used for shore line?
                                           Default: 0     ! MSGTIBL = 0  !
     (MSGTIBL)
        0 = no
        1 = yes

### Generate the BCON
     Boundary conditions (concentration) modeled?
                                           Default: 0     ! MBCON = 0  !
     (MBCON)
        0 = no
        1 = yes, using formatted BCON.DAT file
        2 = yes, using unformatted CONC.DAT file

     Note:  MBCON > 0 requires that the last species modeled
            be 'BCON'.  Mass is placed in species BCON when
            generating boundary condition puffs so that clean
            air entering the modeling domain can be simulated
            in the same way as polluted air.  Specify zero
            emission of species BCON for all regular sources.

     Individual source contributions saved?
                                           Default: 0     ! MSOURCE = 0  !
     (MSOURCE)
        0 = no
        1 = yes

### Fog and Ice
     Analyses of fogging and icing impacts due to emissions from
     arrays of mechanically-forced cooling towers can be performed
     using CALPUFF in conjunction with a cooling tower emissions
     processor (CTEMISS) and its associated postprocessors.  Hourly
     emissions of water vapor and temperature from each cooling tower
     cell are computed for the current cell configuration and ambient
     conditions by CTEMISS. CALPUFF models the dispersion of these
     emissions and provides cloud information in a specialized format
     for further analysis. Output to FOG.DAT is provided in either
     'plume mode' or 'receptor mode' format.

     Configure for FOG Model output?
                                           Default: 0     ! MFOG =  0   !
     (MFOG)
        0 = no
        1 = yes  - report results in PLUME Mode format
        2 = yes  - report results in RECEPTOR Mode format

### USEPA LRT Guidance
     Test options specified to see if
     they conform to regulatory
     values? (MREG)                        Default: 1     ! MREG =  0   !

        0 = NO checks are made
        1 = Technical options must conform to USEPA
            Long Range Transport (LRT) guidance
                       METFM    1 or 2
                       AVET     60. (min)
                       PGTIME   60. (min)
                       MGAUSS   1
                       MCTADJ   3
                       MTRANS   1
                       MTIP     1
                       MRISE    1
                       MCHEM    1 or 3 (if modeling SOx, NOx)
                       MWET     1
                       MDRY     1
                       MDISP    2 or 3
                       MPDF     0 if MDISP=3
                                1 if MDISP=2
                       MROUGH   0
                       MPARTL   1
                       MPARTLBA 0
                       SYTDEP   550. (m)
                       MHFTSZ   0
                       SVMIN    0.5
      !END!


-------------------------------------------------------------------------------

## INPUT GROUP: 3 -- Species list
------------
### Subgroup (3a) Model Species
------------

      The following species are modeled:

      ! CSPEC =          SO2 !         !END!
      ! CSPEC =          SO4 !         !END!
      ! CSPEC =          NOX !         !END!
      ! CSPEC =          HNO3 !         !END!
      ! CSPEC =          NO3 !         !END!
      ! CSPEC =          PMS1! !END!
      ! CSPEC =          PMS2! !END!
      ! CSPEC =          PMS3! !END!

                                                       Dry                OUTPUT GROUP
    SPECIES          MODELED          EMITTED       DEPOSITED                NUMBER
     NAME         (0=NO, 1=YES)    (0=NO, 1=YES)    (0=NO,                 (0=NONE,
      (Limit: 12                                        1=COMPUTED-GAS        1=1st CGRUP,
         Characters                                       2=COMPUTED-PARTICLE   2=2nd CGRUP,
         in length)                                       3=USER-SPECIFIED)     3= etc.)

      !          SO2  =         1,               1,           1,                 0   !
      !          SO4  =         1,               1,           2,                 0   !
      !          NOX  =         1,               1,           1,                 0   !
      !          HNO3 =         1,               1,           1,                 0   !
      !          NO3  =         1,               1,           2,                 0   !
      !          PMS1 =         1,               1,           2,                 1   !
      !          PMS2 =         1,               1,           2,                 2   !
      !          PMS3 =         1,               1,           2,                 3   !
      !END!

      Note:  The last species in (3a) must be 'BCON' when using the
         boundary condition option (MBCON > 0).  Species BCON should
         typically be modeled as inert (no chem transformation or
         removal).


-------------
### Subgroup (3b) PM Group Names
-------------
      The following names are used for Species-Groups in which results
      for certain species are combined (added) prior to output.  The
      CGRUP name will be used as the species name in output files.
      Use this feature to model specific particle-size distributions
      by treating each size-range as a separate species.
      Order must be consistent with 3(a) above.

      ! CGRUP = PM25 ! !END!
      ! CGRUP = PM10 ! !END!
      ! CGRUP = TSP  ! !END!

-------------------------------------------------------------------------------


## INPUT GROUP: 4 -- Map Projection and Grid control parameters
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
     (FEAST)                    Default=0.0     ! FEAST  = 0.000  !
     (FNORTH)                   Default=0.0     ! FNORTH = 0.000  !

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
     (RLAT0)                    No Default      ! RLAT0 =  23.61N !
     (RLON0)                    No Default      ! RLON0 = 120.99E !

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


     Datum-region
     ------------

     The Datum-Region for the coordinates is identified by a character
     string.  Many mapping products currently available use the model of the
     Earth known as the World Geodetic System 1984 (WGS-84).  Other local
     models may be in use, and their selection in CALMET will make its output
     consistent with local mapping products.  The list of Datum-Regions with
     official transformation parameters is provided by the National Imagery and
     Mapping Agency (NIMA).

     NIMA Datum - Regions(Examples)
     ------------------------------------------------------------------------------
     WGS-84    WGS-84 Reference Ellipsoid and Geoid, Global coverage (WGS84)
     NAS-C     NORTH AMERICAN 1927 Clarke 1866 Spheroid, MEAN FOR CONUS (NAD27)
     NAR-C     NORTH AMERICAN 1983 GRS 80 Spheroid, MEAN FOR CONUS (NAD83)
     NWS-84    NWS 6370KM Radius, Sphere
     ESR-S     ESRI REFERENCE 6371KM Radius, Sphere

     Datum-region for output coordinates
     (DATUM)                    Default: WGS-84    ! DATUM = WGS-G  !

### METEOROLOGICAL Grid:

     Rectangular grid defined for projection PMAP,
     with X the Easting and Y the Northing coordinate

     No. X grid cells (NX)      No default     ! NX =  83 !
     No. Y grid cells (NY)      No default     ! NY =  137 !
     No. vertical layers (NZ)   No default     ! NZ =   15  !
     Grid spacing (DGRIDKM)     No default  ! DGRIDKM = 3.000 !
                                       Units: km

                Cell face heights
                    (ZFACE(nz+1))      No defaults
                                       Units: m
      !ZFACE=0.0,20.0,47.0,75.0,106.5,141.5,181.0,226.0,277.0,334.5,399.5,555.5,757.0,1177.0,1566.5,2403.5!

            Reference Coordinates
           of SOUTHWEST corner of
                 grid cell(1, 1):

      X coordinate (XORIGKM)     No default   72! XORIGKM = -124.5!
      Y coordinate (YORIGKM)     No default     ! YORIGKM = -205.5!
                                      Units: km


### COMPUTATIONAL Grid:

     The computational grid is identical to or a subset of the MET. grid.
     The lower left (LL) corner of the computational grid is at grid point
     (IBCOMP, JBCOMP) of the MET. grid.  The upper right (UR) corner of the
     computational grid is at grid point (IECOMP, JECOMP) of the MET. grid.
     The grid spacing of the computational grid is the same as the MET. grid.

        X index of LL corner (IBCOMP)      No default     ! IBCOMP =  1   !
                  (1 <= IBCOMP <= NX)

        Y index of LL corner (JBCOMP)      No default     ! JBCOMP =  1   !
                  (1 <= JBCOMP <= NY)


        X index of UR corner (IECOMP)      No default     ! IECOMP = 83   !
                  (1 <= IECOMP <= NX)

        Y index of UR corner (JECOMP)      No default     ! JECOMP = 137  !
                  (1 <= JECOMP <= NY)



### SAMPLING Grid (GRIDDED RECEPTORS):

     The lower left (LL) corner of the sampling grid is at grid point
     (IBSAMP, JBSAMP) of the MET. grid.  The upper right (UR) corner of the
     sampling grid is at grid point (IESAMP, JESAMP) of the MET. grid.
     The sampling grid must be identical to or a subset of the computational
     grid.  It may be a nested grid inside the computational grid.
     The grid spacing of the sampling grid is DGRIDKM/MESHDN.

        Logical flag indicating if gridded
        receptors are used (LSAMP)         Default: T     ! LSAMP = T !
        (T=yes, F=no)

        X index of LL corner (IBSAMP)      No default     ! IBSAMP =  1   !
         (IBCOMP <= IBSAMP <= IECOMP)

        Y index of LL corner (JBSAMP)      No default     ! JBSAMP =  1   !
         (JBCOMP <= JBSAMP <= JECOMP)


        X index of UR corner (IESAMP)      No default     ! IESAMP = 83  !
         (IBCOMP <= IESAMP <= IECOMP)

        Y index of UR corner (JESAMP)      No default     ! JESAMP = 137  !
         (JBCOMP <= JESAMP <= JECOMP)


       Nesting factor of the sampling
        grid (MESHDN)                      Default: 1     ! MESHDN =  1  !
        (MESHDN is an integer >= 1)
      !END!


-------------------------------------------------------------------------------


## INPUT GROUP: 5 -- Output Options
--------------
                                             *                          *
      FILE                       DEFAULT VALUE             VALUE THIS RUN
      ----                       -------------             --------------

      Concentrations (ICON)              1                   !  ICON =  1   !
      Dry Fluxes (IDRY)                  1                   !  IDRY =  1   !
      Wet Fluxes (IWET)                  1                   !  IWET =  1   !
      2D Temperature (IT2D)              0                   !  IT2D =  0   !
      2D Density (IRHO)                  0                   !  IRHO =  0   !
      Relative Humidity (IVIS)           1                   !  IVIS =  0   !
      (relative humidity file is
      required for visibility
      analysis)
      Use data compression option in output file?
      (LCOMPRS)                           Default: T         ! LCOMPRS = T !

      *
    0 = Do not create file, 1 = create file


    QA PLOT FILE OUTPUT OPTION:

       Create a standard series of output files (e.g.
       locations of sources, receptors, grids ...)
       suitable for plotting?
       (IQAPLOT)                       Default: 1         ! IQAPLOT =  1   !
         0 = no
         1 = yes

    DIAGNOSTIC MASS FLUX OUTPUT OPTIONS:

       Mass flux across specified boundaries
       for selected species reported?
       (IMFLX)                         Default: 0         ! IMFLX =  0  !
         0 = no
         1 = yes (FLUXBDY.DAT and MASSFLX.DAT filenames
                  are specified in Input Group 0)

       Mass balance for each species
       reported?
       (IMBAL)                         Default: 0         ! IMBAL =  0  !
         0 = no
         1 = yes (MASSBAL.DAT filename is
              specified in Input Group 0)


    NUMERICAL RISE OUTPUT OPTION:

       Create a file with plume properties for each rise
       increment, for each model timestep?
       This applies to sources modeled with numerical rise.
       (INRISE)                        Default: 0         ! INRISE =  0   !
         0 = no
         1 = yes (RISE.DAT filename is
                  specified in Input Group 0)


    LINE PRINTER OUTPUT OPTIONS:

       Print concentrations (ICPRT)    Default: 0         ! ICPRT =  1   !
       Print dry fluxes (IDPRT)        Default: 0         ! IDPRT =  0   !
       Print wet fluxes (IWPRT)        Default: 0         ! IWPRT =  0   !
       (0 = Do not print, 1 = Print)

       Concentration print interval
       (ICFRQ) in timesteps            Default: 1         ! ICFRQ =  24   !
       Dry flux print interval
       (IDFRQ) in timesteps            Default: 1         ! IDFRQ =  1   !
       Wet flux print interval
       (IWFRQ) in timesteps            Default: 1         ! IWFRQ =  1   !

       Units for Line Printer Output
       (IPRTU)                         Default: 1         ! IPRTU =  1   !
                       for            for
                  Concentration    Deposition
           1 =       g/m**3         g/m**2/s
           2 =      mg/m**3        mg/m**2/s
           3 =      ug/m**3        ug/m**2/s
           4 =      ng/m**3        ng/m**2/s
           5 =     Odour Units

       Messages tracking progress of run
       written to the screen ?
       (IMESG)                         Default: 2         ! IMESG =  2   !
         0 = no
         1 = yes (advection step, puff ID)
         2 = yes (YYYYJJJHH, # old puffs, # emitted puffs)


     SPECIES (or GROUP for combined species) LIST FOR OUTPUT OPTIONS

                     ---- CONCENTRATIONS ----   ------ DRY FLUXES ------   ------ WET FLUXES ------   -- MASS FLUX --
         SPECIES
         /GROUP        PRINTED?  SAVED ON DISK?   PRINTED?  SAVED ON DISK?   PRINTED?  SAVED ON DISK?   SAVED ON DISK?
         -------       ------------------------   ------------------------   ------------------------   ---------------
      !          SO2 =     0,           1,           0,           1,           0,           1,           1   !
      !          SO4 =     0,           1,           0,           1,           0,           1,           1   !
      !          NOX =     0,           1,           0,           1,           0,           1,           1   !
      !          HNO3=     0,           1,           0,           1,           0,           1,           1   !
      !          NO3 =     0,           1,           0,           1,           0,           1,           1   !
      !          PM25=     0,           1,           0,           1,           0,           1,           1   !
      !          PM10=     0,           1,           0,           1,           0,           1,           1   !
      !          TSP =     0,           1,           0,           1,           0,           1,           1   !

  Note:  Species BCON (for MBCON > 0) does not need to be saved on disk.


     OPTIONS FOR PRINTING "DEBUG" QUANTITIES (much output)   

       Logical for debug output
       (LDEBUG)                                 Default: F     ! LDEBUG = F !

       First puff to track
       (IPFDEB)                                 Default: 1     ! IPFDEB =  1  !

       Number of puffs to track
       (NPFDEB)                                 Default: 1     ! NPFDEB =  10  !

       Met. period to start output
       (NN1)                                    Default: 1     ! NN1 =  1   !

       Met. period to end output
       (NN2)                                    Default: 10    ! NN2 =  10  !

      !END!


-------------------------------------------------------------------------------


## INPUT GROUP: 6 -- Subgrid scale complex terrain inputs

---------------
### Subgroup (6a)
---------------
       Number of terrain features (NHILL)       Default: 0     ! NHILL =  0   !

       Number of special complex terrain
       receptors  (NCTREC)                      Default: 0     ! NCTREC =  0   !

       Terrain and CTSG Receptor data for 
       CTSG hills input in CTDM format ?
       (MHILL)                                  No Default     ! MHILL =  2   !
       1 = Hill and Receptor data created
           by CTDM processors & read from
           HILL.DAT and HILLRCT.DAT files
       2 = Hill data created by OPTHILL &
           input below in Subgroup (6b);
           Receptor data in Subgroup (6c)

       Factor to convert horizontal dimensions  Default: 1.0   ! XHILL2M = .0 !
       to meters (MHILL=1)

       Factor to convert vertical dimensions    Default: 1.0   ! ZHILL2M = .0 !
       to meters (MHILL=1)

       X-origin of CTDM system relative to      No Default     ! XCTDMKM = 0 !
       CALPUFF coordinate system, in Kilometers (MHILL=1)

       Y-origin of CTDM system relative to      No Default     ! YCTDMKM = 0 !
       CALPUFF coordinate system, in Kilometers (MHILL=1)

      ! END !

---------------
### Subgroup (6b)
---------------

                      1 **
     HILL information


      HILL           XC        YC       THETAH  ZGRID  RELIEF    EXPO 1    EXPO 2   SCALE 1    SCALE 2    AMAX1     AMAX2
      NO.          (km)      (km)      (deg.)   (m)     (m)      (m)       (m)       (m)        (m)       (m)       (m)
      ----          ----      ----      ------  -----  ------    ------    ------   -------    -------    -----     -----

      ---------------
### Subgroup (6c)
---------------

    COMPLEX TERRAIN RECEPTOR INFORMATION

                      XRCT         YRCT        ZRCT          XHH
                      (km)         (km)         (m)
                     ------        -----      ------         ----


-------------------
      1
      Description of Complex Terrain Variables:
          XC, YC  = Coordinates of center of hill
          THETAH  = Orientation of major axis of hill (clockwise from
                    North)
          ZGRID   = Height of the  0  of the grid above mean sea
                    level
          RELIEF  = Height of the crest of the hill above the grid elevation
          EXPO 1  = Hill-shape exponent for the major axis
          EXPO 2  = Hill-shape exponent for the major axis
          SCALE 1 = Horizontal length scale along the major axis
          SCALE 2 = Horizontal length scale along the minor axis
          AMAX    = Maximum allowed axis length for the major axis
          BMAX    = Maximum allowed axis length for the major axis

          XRCT, YRCT = Coordinates of the complex terrain receptors
          ZRCT    = Height of the ground (MSL) at the complex terrain
                    Receptor
          XHH     = Hill number associated with each complex terrain receptor
                    (NOTE: MUST BE ENTERED AS A REAL NUMBER)

      **
         NOTE: DATA for each hill and CTSG receptor are treated as a separate
               input subgroup and therefore must end with an input group terminator.

-------------------------------------------------------------------------------


## INPUT GROUP: 7 -- Chemical parameters for dry deposition of gases
--------------

      SPECIES     DIFFUSIVITY      ALPHA STAR      REACTIVITY    MESOPHYLL RESISTANCE     HENRY'S LAW COEFFICIENT
      NAME        (cm**2/s)                                            (s/cm)                (dimensionless)
      -------     -----------      ----------      ----------    --------------------     -----------------------
      ! SO2 = 0.1509 , 1.00E3 , 8.0 , 0.0 , 4.e-2 !
      ! NOX = 0.1656 , 1.00 , 8.0 , 5.0 , 3.5 !
      ! HNO3 = 0.1628 , 1.00 , 18.0 , 0.0 , 8.e-8 !

      !END!


-------------------------------------------------------------------------------


## INPUT GROUP: 8 -- Size parameters for dry deposition of particles
--------------

     For SINGLE SPECIES, the mean and standard deviation are used to
     compute a deposition velocity for NINT (see group 9) size-ranges,
     and these are then averaged to obtain a mean deposition velocity.

     For GROUPED SPECIES, the size distribution should be explicitly
     specified (by the 'species' in the group), and the standard deviation
     for each should be entered as 0.  The model will then use the
     deposition velocity for the stated mean diameter.

            SPECIES      GEOMETRIC MASS MEAN        GEOMETRIC STANDARD
            NAME             DIAMETER                   DEVIATION
                              (microns)                  (microns)
            -------      -------------------        ------------------
      !     SO4 =        0.48,                     2. !
      !     NO3 =        0.48,                     2. !
      !     PMS1 =        2.5,                     2. !
      !     PMS2 =        10.,                     2. !
      !     PMS3 =        15.,                     2. !
      !END!


-------------------------------------------------------------------------------


## INPUT GROUP: 9 -- Miscellaneous dry deposition parameters
--------------

     Reference cuticle resistance (s/cm)
     (RCUTR)                           Default: 30    !  RCUTR = 30.0 !
     Reference ground resistance  (s/cm)
     (RGR)                             Default: 10    !    RGR = 10.0 !
     Reference pollutant reactivity
     (REACTR)                          Default: 8     ! REACTR = 8.0 !

     Number of particle-size intervals used to 
     evaluate effective particle deposition velocity
     (NINT)                            Default: 9     !   NINT =  9  !

     Vegetation state in unirrigated areas
     (IVEG)                            Default: 1     !   IVEG =  1   !
        IVEG=1 for active and unstressed vegetation
        IVEG=2 for active and stressed vegetation
        IVEG=3 for inactive vegetation

      !END!


-------------------------------------------------------------------------------


## INPUT GROUP: 10 -- Wet Deposition Parameters
---------------

                                                          
                      Scavenging Coefficient -- Units: (sec)**(-1)

       Pollutant      Liquid Precip.       Frozen Precip.
       ---------      --------------       --------------
      !   SO2 =            3.0E-5,          0.0           !
      !   SO4 =            10.0E-5,         3.0E-5        !
      !   NOX =            0.0E-5,          0.0           !
      !   HNO3=            6.0E-5,          0.0           !
      !   NO3 =            10.0E-5,         3.0E-5        ! 
      !   PMS1=            1.0E-4,          3.0E-5        ! 
      !   PMS2=            1.0E-4,          3.0E-5        ! 
      !   PMS3=            1.0E-4,          3.0E-5        ! 

!END!


-------------------------------------------------------------------------------


## INPUT GROUP: 11 -- Chemistry Parameters
---------------

     Ozone data input option (MOZ)     Default: 1            ! MOZ =  0   !
     (Used only if MCHEM = 1, 3, or 4)
        0 = use a monthly background ozone value
        1 = read hourly ozone concentrations from
            the OZONE.DAT data file

     Monthly ozone concentrations
     (Used only if MCHEM = 1, 3, or 4 and 
      MOZ = 0 or MOZ = 1 and all hourly O3 data missing)
     (BCKO3) in ppb                    Default: 12*80.
     !  BCKO3 = 80.00, 80.00, 80.00, 80.00, 80.00, 80.00, 80.00, 80.00, 80.00, 80.00, 80.00, 80.00 !

     Monthly ammonia concentrations
     (Used only if MCHEM = 1, or 3)
     (BCKNH3) in ppb                   Default: 12*10.       
     !  BCKNH3 = 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0 !

     Nighttime SO2 loss rate (RNITE1)
     in percent/hour                   Default: 0.2          ! RNITE1 = .2 !

     Nighttime NOx loss rate (RNITE2)
     in percent/hour                   Default: 2.0          ! RNITE2 = 2.0 !

     Nighttime HNO3 formation rate (RNITE3)
     in percent/hour                   Default: 2.0          ! RNITE3 = 2.0 !

     H2O2 data input option (MH2O2)    Default: 1            ! MH2O2 =  1   !
     (Used only if MAQCHEM = 1)
        0 = use a monthly background H2O2 value
        1 = read hourly H2O2 concentrations from
            the H2O2.DAT data file

     Monthly H2O2 concentrations
     (Used only if MQACHEM = 1 and
      MH2O2 = 0 or MH2O2 = 1 and all hourly H2O2 data missing)
     (BCKH2O2) in ppb                  Default: 12*1.        
     !  BCKH2O2 = 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00 !


 --- Data for SECONDARY ORGANIC AEROSOL (SOA) Option
     (used only if MCHEM = 4)

     The SOA module uses monthly values of:
          Fine particulate concentration in ug/m^3 (BCKPMF)
          Organic fraction of fine particulate     (OFRAC)
          VOC / NOX ratio (after reaction)         (VCNX)
     to characterize the air mass when computing
     the formation of SOA from VOC emissions.
     Typical values for several distinct air mass types are:

        Month    1    2    3    4    5    6    7    8    9   10   11   12
                Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec

     Clean Continental
        BCKPMF   1.   1.   1.   1.   1.   1.   1.   1.   1.   1.   1.   1.
        OFRAC  .15  .15  .20  .20  .20  .20  .20  .20  .20  .20  .20  .15
        VCNX    50.  50.  50.  50.  50.  50.  50.  50.  50.  50.  50.  50.

     Clean Marine (surface)
        BCKPMF  .5   .5   .5   .5   .5   .5   .5   .5   .5   .5   .5   .5
        OFRAC  .25  .25  .30  .30  .30  .30  .30  .30  .30  .30  .30  .25
        VCNX    50.  50.  50.  50.  50.  50.  50.  50.  50.  50.  50.  50.

     Urban - low biogenic (controls present)
        BCKPMF  30.  30.  30.  30.  30.  30.  30.  30.  30.  30.  30.  30.
        OFRAC  .20  .20  .25  .25  .25  .25  .25  .25  .20  .20  .20  .20
        VCNX     4.   4.   4.   4.   4.   4.   4.   4.   4.   4.   4.   4.

     Urban - high biogenic (controls present)
        BCKPMF  60.  60.  60.  60.  60.  60.  60.  60.  60.  60.  60.  60.
        OFRAC  .25  .25  .30  .30  .30  .55  .55  .55  .35  .35  .35  .25
        VCNX    15.  15.  15.  15.  15.  15.  15.  15.  15.  15.  15.  15.

     Regional Plume
        BCKPMF  20.  20.  20.  20.  20.  20.  20.  20.  20.  20.  20.  20.
        OFRAC  .20  .20  .25  .35  .25  .40  .40  .40  .30  .30  .30  .20
        VCNX    15.  15.  15.  15.  15.  15.  15.  15.  15.  15.  15.  15.

     Urban - no controls present
        BCKPMF 100. 100. 100. 100. 100. 100. 100. 100. 100. 100. 100. 100.
        OFRAC  .30  .30  .35  .35  .35  .55  .55  .55  .35  .35  .35  .30
        VCNX     2.   2.   2.   2.   2.   2.   2.   2.   2.   2.   2.   2.

     Default: Clean Continental
     !  BCKPMF = 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00 !
     !  OFRAC  = 0.15, 0.15, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.20, 0.15 !
     !  VCNX   = 50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00, 50.00 !

      !END!


-------------------------------------------------------------------------------


## INPUT GROUP: 12 -- Misc. Dispersion and Computational Parameters
---------------

     Horizontal size of puff (m) beyond which
     time-dependent dispersion equations (Heffter)
     are used to determine sigma-y and
     sigma-z (SYTDEP)                           Default: 550.   ! SYTDEP = 5.5E02 !

     Switch for using Heffter equation for sigma z           
     as above (0 = Not use Heffter; 1 = use Heffter
     (MHFTSZ)                                   Default: 0      ! MHFTSZ =  0   !

     Stability class used to determine plume
     growth rates for puffs above the boundary
     layer (JSUP)                               Default: 5      ! JSUP =  5   !

     Vertical dispersion constant for stable
     conditions (k1 in Eqn. 2.7-3)  (CONK1)     Default: 0.01   ! CONK1 = .01 !

     Vertical dispersion constant for neutral/
     unstable conditions (k2 in Eqn. 2.7-4)
     (CONK2)                                    Default: 0.1    ! CONK2 = .1 !

     Factor for determining Transition-point from
     Schulman-Scire to Huber-Snyder Building Downwash
     scheme (SS used for Hs < Hb + TBD * HL)
     (TBD)                                      Default: 0.5    ! TBD = .5 !
        TBD < 0   ==> always use Huber-Snyder
        TBD = 1.5 ==> always use Schulman-Scire
        TBD = 0.5 ==> ISC Transition-point

     Range of land use categories for which
     urban dispersion is assumed
     (IURB1, IURB2)                             Default: 10     ! IURB1 =  10  !
                                                         19     ! IURB2 =  19  !

     Site characterization parameters for single-point Met data files ---------
     (needed for METFM = 2,3,4,5)

        Land use category for modeling domain
        (ILANDUIN)                              Default: 20     ! ILANDUIN =  20  !

        Roughness length (m) for modeling domain
        (Z0IN)                                  Default: 0.25   ! Z0IN = .25 !

        Leaf area index for modeling domain
        (XLAIIN)                                Default: 3.0    ! XLAIIN = 3.0 !

        Elevation above sea level (m)
        (ELEVIN)                                Default: 0.0    ! ELEVIN = .0 !

        Latitude (degrees) for met location
        (XLATIN)                                Default: -999.  ! XLATIN = -999.0 !

        Longitude (degrees) for met location
        (XLONIN)                                Default: -999.  ! XLONIN = -999.0 !

     Specialized information for interpreting single-point Met data files -----

        Anemometer height (m) (Used only if METFM = 2,3)
        (ANEMHT)                                Default: 10.    ! ANEMHT = 10.0 !

        Form of lateral turbulance data in PROFILE.DAT file
        (Used only if METFM = 4,5 or MTURBVW = 1 or 3)
        (ISIGMAV)                               Default: 1      ! ISIGMAV =  1  !
            0 = read sigma-theta
            1 = read sigma-v

        Choice of mixing heights (Used only if METFM = 4)
        (IMIXCTDM)                              Default: 0      ! IMIXCTDM =  0  !
            0 = read PREDICTED mixing heights
            1 = read OBSERVED mixing heights

     Maximum length of a slug (met. grid units)
     (XMXLEN)                                   Default: 1.0    ! XMXLEN = 1.0 !

     Maximum travel distance of a puff/slug (in
     grid units) during one sampling step
     (XSAMLEN)                                  Default: 1.0    ! XSAMLEN = 1.0 !

     Maximum Number of slugs/puffs release from
     one source during one time step            
     (MXNEW)                                    Default: 99     ! MXNEW =  99   !

     Maximum Number of sampling steps for    
     one puff/slug during one time step             
     (MXSAM)                                    Default: 99     ! MXSAM =  5   !

     Number of iterations used when computing
     the transport wind for a sampling step
     that includes gradual rise (for CALMET
     and PROFILE winds)
     (NCOUNT)                                   Default: 2      ! NCOUNT =  2   !

     Minimum sigma y for a new puff/slug (m)      
     (SYMIN)                                    Default: 1.0    ! SYMIN = 1.0  !

     Minimum sigma z for a new puff/slug (m)     
     (SZMIN)                                    Default: 1.0    ! SZMIN = 1.0  !

     Maximum sigma z (m) allowed to avoid
     numerical problem in calculating virtual
     time or distance.  Cap should be large
     enough to have no influence on normal events.
     Enter a negative cap to disable.
     (SZCAP_M)                                  Default: 5.0e06 ! SZCAP_M = -1.0  !


     Default minimum turbulence velocities sigma-v and sigma-w
     for each stability class over land and over water (m/s)
     (SVMIN(12) and SWMIN(12))

                     ----------  LAND  ----------       ---------  WATER  ----------
        Stab Class :  A    B    C    D    E    F         A    B    C    D    E    F
                     ---  ---  ---  ---  ---  ---       ---  ---  ---  ---  ---  ---
     Default SVMIN : .50, .50, .50, .50, .50, .50,      .37, .37, .37, .37, .37, .37
     Default SWMIN : .20, .12, .08, .06, .03, .016,     .20, .12, .08, .06, .03, .016

           ! SVMIN = 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500, 0.500!
           ! SWMIN = 0.200, 0.120, 0.080, 0.060, 0.030, 0.016, 0.200, 0.120, 0.080, 0.060, 0.030, 0.016!

     Divergence criterion for dw/dz across puff
     used to initiate adjustment for horizontal
     convergence (1/s)
     Partial adjustment starts at CDIV(1), and
     full adjustment is reached at CDIV(2)
     (CDIV(2))                                  Default: 0.0,0.0  ! CDIV = .01, .01 !

     Search radius (number of cells) for nearest
     land and water cells used in the subgrid
     TIBL module
     (NLUTIBL)                                  Default: 4      ! NLUTIBL = 4 !

     Minimum wind speed (m/s) allowed for
     non-calm conditions. Also used as minimum
     speed returned when using power-law 
     extrapolation toward surface
     (WSCALM)                                   Default: 0.5    ! WSCALM = .5 !

     Maximum mixing height (m)                      
     (XMAXZI)                                   Default: 3000.  ! XMAXZI = 3000.0 !

     Minimum mixing height (m)                     
     (XMINZI)                                   Default: 50.    ! XMINZI = 50.0 !

     Default wind speed classes --
     5 upper bounds (m/s) are entered;
     the 6th class has no upper limit
     (WSCAT(5))                      Default   : 
                                     ISC RURAL : 1.54, 3.09, 5.14, 8.23, 10.8 (10.8+)

                              Wind Speed Class :  1     2     3     4     5  
                                                 ---   ---   ---   ---   --- 
                                       ! WSCAT = 1.54, 3.09, 5.14, 8.23, 10.80 !

     Default wind speed profile power-law
     exponents for stabilities 1-6
     (PLX0(6))                       Default   : ISC RURAL values
                                     ISC RURAL : .07, .07, .10, .15, .35, .55
                                     ISC URBAN : .15, .15, .20, .25, .30, .30

                               Stability Class :  A     B     C     D     E     F
                                                 ---   ---   ---   ---   ---   ---
                                        ! PLX0 = 0.07, 0.07, 0.10, 0.15, 0.35, 0.55 !

     Default potential temperature gradient
     for stable classes E, F (degK/m)
     (PTG0(2))                       Default: 0.020, 0.035
                                        ! PTG0 = 0.020,   0.035 !

     Default plume path coefficients for
     each stability class (used when option
     for partial plume height terrain adjustment
     is selected -- MCTADJ=3)
     (PPC(6))                  Stability Class :  A     B     C     D     E     F
                                  Default  PPC : .50,  .50,  .50,  .50,  .35,  .35
                                                 ---   ---   ---   ---   ---   ---
                                        !  PPC = 0.50, 0.50, 0.50, 0.50, 0.35, 0.35 !

     Slug-to-puff transition criterion factor
     equal to sigma-y/length of slug
     (SL2PF)                               Default: 10.        ! SL2PF = 5.0 !

     Puff-splitting control variables ------------------------

       VERTICAL SPLIT
       --------------

       Number of puffs that result every time a puff
       is split - nsplit=2 means that 1 puff splits
       into 2
       (NSPLIT)                            Default:   3        ! NSPLIT =  3  !

       Time(s) of a day when split puffs are eligible to
       be split once again; this is typically set once
       per day, around sunset before nocturnal shear develops.
       24 values: 0 is midnight (00:00) and 23 is 11 PM (23:00)
       0=do not re-split    1=eligible for re-split
       (IRESPLIT(24))                      Default:  Hour 17 = 1
       !  IRESPLIT = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0 !

       Split is allowed only if last hour's mixing
       height (m) exceeds a minimum value
       (ZISPLIT)                           Default: 100.       ! ZISPLIT = 100.0 !

       Split is allowed only if ratio of last hour's
       mixing ht to the maximum mixing ht experienced
       by the puff is less than a maximum value (this
       postpones a split until a nocturnal layer develops)
       (ROLDMAX)                           Default: 0.25       ! ROLDMAX = 0.25 !


       HORIZONTAL SPLIT
       ----------------

       Number of puffs that result every time a puff
       is split - nsplith=5 means that 1 puff splits
       into 5
       (NSPLITH)                           Default:   5        ! NSPLITH =  5  !

       Minimum sigma-y (Grid Cells Units) of puff
       before it may be split
       (SYSPLITH)                          Default:  1.0       ! SYSPLITH = 1.0 !

       Minimum puff elongation rate (SYSPLITH/hr) due to
       wind shear, before it may be split
       (SHSPLITH)                          Default:  2.        ! SHSPLITH = 2.0 !

       Minimum concentration (g/m^3) of each
       species in puff before it may be split
       Enter array of NSPEC values; if a single value is
       entered, it will be used for ALL species
       (CNSPLITH)                          Default:  1.0E-07   ! CNSPLITH = 1.0E-07 !

     Integration control variables ------------------------

       Fractional convergence criterion for numerical SLUG
       sampling integration
       (EPSSLUG)                           Default:   1.0e-04  ! EPSSLUG = 1.0E-04 !

       Fractional convergence criterion for numerical AREA
       source integration
       (EPSAREA)                           Default:   1.0e-06  ! EPSAREA = 1.0E-06 !

       Trajectory step-length (m) used for numerical rise
       integration
       (DSRISE)                            Default:   1.0      ! DSRISE = 1.0 !

       Boundary Condition (BC) Puff control variables ------------------------

       Minimum height (m) to which BC puffs are mixed as they are emitted
       (MBCON=2 ONLY).  Actual height is reset to the current mixing height
       at the release point if greater than this minimum.
       (HTMINBC)                           Default:   500.     ! HTMINBC = 500.0 !

       Search radius (km) about a receptor for sampling nearest BC puff.
       BC puffs are typically emitted with a spacing of one grid cell
       length, so the search radius should be greater than DGRIDKM.
       (RSAMPBC)                           Default:   10.      ! RSAMPBC = 15.0 !

       Near-Surface depletion adjustment to concentration profile used when
       sampling BC puffs?
       (MDEPBC)                            Default:   1        ! MDEPBC =  0  !
          0 = Concentration is NOT adjusted for depletion
          1 = Adjust Concentration for depletion
      !END!


-------------------------------------------------------------------------------


## INPUT GROUPS: 13 -- Point source parameters
--------------------------------

---------------
### Subgroup (13a) Number of point sources
---------------

     Number of point sources with
     parameters provided below      (NPT1)  No default  !  NPT1 = 1!

     Units used for point source
     emissions below                (IPTU)  Default: 1  !  IPTU =   1  !
           1 =        g/s
           2 =       kg/hr
           3 =       lb/hr
           4 =     tons/yr
           5 =     Odour Unit * m**3/s  (vol. flux of odour compound)
           6 =     Odour Unit * m**3/min
           7 =     metric tons/yr

     Number of source-species
     combinations with variable
     emissions scaling factors
     provided below in (13d)        (NSPT1) Default: 0  !  NSPT1 =  0  !

     Number of point sources with
     variable emission parameters
     provided in external file      (NPT2)  No default  !  NPT2 =  0!

     (If NPT2 > 0, these point
     source emissions are read from
     the file: PTEMARB.DAT)

      !END!

---------------
### Subgroup (13b) Constant Emissions
---------------
                                          a
               POINT SOURCE: CONSTANT DATA
               -----------------------------
                                                                                 b          c
      Source       X         Y       Stack    Base     Stack    Exit  Exit    Bldg.  Emission
      No.     Coordinate Coordinate Height Elevation Diameter  Vel.  Temp.   Dwash   Rates
                  (km)      (km)       (m)      (m)       (m)  (m/s) (deg. K)         
      SO2 SO4 NOX HNO3 NO3 PMS1(fine),PMS2(10)PMS3(coarse)
      ------   ---------- ---------- ------  ------   -------- ----- -------- ----- --------
      L0200473PNG1
      1 ! SRCNAM = 1 !
      1 ! X =  -32.064, 97.505,  150,      4.7,    11.00,  19.8, 363.0,   .0,   5.440,
         1.08, 34.511,0.,0., 2.104,0.0,0.0!
      1 ! ZPLTFM  =      .0 !
      1 ! FMFAC  =      1.0 !   !END!

--------

    a
     Data for each source are treated as a separate input subgroup
     and therefore must end with an input group terminator.

     SRCNAM  is a 12-character name for a source
             (No default)
     X       is an array holding the source data listed by the column headings
             (No default)
     SIGYZI  is an array holding the initial sigma-y and sigma-z (m)
             (Default: 0.,0.)
     FMFAC   is a vertical momentum flux factor (0. or 1.0) used to represent
             the effect of rain-caps or other physical configurations that
             reduce momentum rise associated with the actual exit velocity.
             (Default: 1.0  -- full momentum used)
     ZPLTFM  is the platform height (m) for sources influenced by an isolated
             structure that has a significant open area between the surface
             and the bulk of the structure, such as an offshore oil platform.
             The Base Elevation is that of the surface (ground or ocean),
             and the Stack Height is the release height above the Base (not
             above the platform).  Building heights entered in Subgroup 13c
             must be those of the buildings on the platform, measured from
             the platform deck.  ZPLTFM is used only with MBDW=1 (ISC
             downwash method) for sources with building downwash.
             (Default: 0.0)

    b
     0. = No building downwash modeled
     1. = Downwash modeled for buildings resting on the surface
     2. = Downwash modeled for buildings raised above the surface (ZPLTFM > 0.)
     NOTE: must be entered as a REAL number (i.e., with decimal point)

    c
     An emission rate must be entered for every pollutant modeled.
     Enter emission rate of zero for secondary pollutants that are
     modeled, but not emitted.  Units are specified by IPTU
     (e.g. 1 for g/s).

---------------
### Subgroup (13c) Building Dimensions
---------------

           BUILDING DIMENSION DATA FOR SOURCES SUBJECT TO DOWNWASH
           -------------------------------------------------------
Source                                                                     a
 No.       Effective building height, width, length and X/Y offset (in meters)
           every 10 degrees.  LENGTH, XBADJ, and YBADJ are only needed for
           MBDW=2 (PRIME downwash option)
------     --------------------------------------------------------------------
      1    * SRCNAM  =   1 *
      1    * HEIGHT  =  50.0,   50.0,   50.0,   50.0,   50.0,   50.0,   
                   50.0,   50.0,   50.0,   50.0,   50.0,   50.0,   
                   50.0,   50.0,   50.0,   50.0,   50.0,   50.0,   
                   50.0,   50.0,   50.0,   50.0,   50.0,   50.0,   
                   50.0,   50.0,   50.0,   50.0,   50.0,   50.0,   
                   50.0,   50.0,   50.0,   50.0,   50.0,   50.0 *
      1    * WIDTH  =   62.26,   72.64,   80.8,   86.51,   89.59,   89.95,   
                   87.58,   82.54,   75.0,   82.54,   87.58,   89.95,   
                   89.59,   86.51,   80.8,   72.64,   62.26,   50.0,   
                   62.26,   72.64,   80.8,   86.51,   89.59,   89.95,   
                   87.58,   82.54,   75.0,   82.54,   87.58,   89.95,   
                   89.59,   86.51,   80.8,   72.64,   62.26,   50.0 *
      1  *  LENGTH =  82.54,  87.58,  89.95,  89.59,  86.51,  80.80, 
                 72.64,  62.26,  50.00,  62.26,  72.64,  80.80, 
                 86.51,  89.59,  89.95,  87.58,  82.54,  75.00, 
                 82.54,  87.58,  89.95,  89.59,  86.51,  80.80, 
                 72.64,  62.26,  50.00,  62.26,  72.64,  80.80, 
                 86.51,  89.59,  89.95,  87.58,  82.54,  75.00 *
      1  *  XBADJ =  -47.35, -55.76, -62.48, -67.29, -70.07, -70.71, 
                -69.21, -65.60, -60.00, -65.60, -69.21, -70.71, 
                -70.07, -67.29, -62.48, -55.76, -47.35, -37.50, 
                -35.19, -31.82, -27.48, -22.30, -16.44, -10.09, 
                 -3.43,   3.34,  10.00,   3.34,  -3.43, -10.09, 
                -16.44, -22.30, -27.48, -31.82, -35.19, -37.50 *
      1  *  YBADJ =   34.47,  32.89,  30.31,  26.81,  22.50,  17.50, 
                 11.97,   6.08,   0.00,  -6.08, -11.97, -17.50, 
                -22.50, -26.81, -30.31, -32.89, -34.47, -35.00, 
                -34.47, -32.89, -30.31, -26.81, -22.50, -17.50, 
                -11.97,  -6.08,   0.00,   6.08,  11.97,  17.50, 
                 22.50,  26.81,  30.31,  32.89,  34.47,  35.00 *
      *END*


--------

    a
     Building height, width, length, and X/Y offset from the source are treated
     as a separate input subgroup for each source and therefore must end with
     an input group terminator.  The X/Y offset is the position, relative to the
     stack, of the center of the upwind face of the projected building, with the
     x-axis pointing along the flow direction.

---------------
### Subgroup (13d) Variable Emissions
---------------
                                                a
          POINT SOURCE: VARIABLE EMISSIONS DATA
          ---------------------------------------

     Use this subgroup to describe temporal variations in the emission
     rates given in 13b.  Factors entered multiply the rates in 13b.
     Skip sources here that have constant emissions.  For more elaborate
     variation in source parameters, use PTEMARB.DAT and NPT2 > 0.

     IVARY determines the type of variation, and is source-specific:
     (IVARY)                                Default: 0
           0 =       Constant
           1 =       Diurnal cycle (24 scaling factors: hours 1-24)
           2 =       Monthly cycle (12 scaling factors: months 1-12)
           3 =       Hour & Season (4 groups of 24 hourly scaling factors,
                                    where first group is DEC-JAN-FEB)
           4 =       Speed & Stab. (6 groups of 6 scaling factors, where
                                    first group is Stability Class A,
                                    and the speed classes have upper
                                    bounds (m/s) defined in Group 12
           5 =       Temperature   (12 scaling factors, where temperature
                                    classes have upper bounds (C) of:
                                    0, 5, 10, 15, 20, 25, 30, 35, 40,
                                    45, 50, 50+)



--------
    a
     Data for each species are treated as a separate input subgroup
     and therefore must end with an input group terminator.


-------------------------------------------------------------------------------


## INPUT GROUPS: 14 -- Area source parameters

---------------
### Subgroup (14a) Number of Sources
---------------

     Number of polygon area sources with
     parameters specified below (NAR1)       No default  !  NAR1 =  0   !

     Units used for area source
     emissions below            (IARU)       Default: 1  !  IARU =   1  !
           1 =        g/m**2/s
           2 =       kg/m**2/hr
           3 =       lb/m**2/hr
           4 =     tons/m**2/yr
           5 =     Odour Unit * m/s  (vol. flux/m**2 of odour compound)
           6 =     Odour Unit * m/min
           7 =     metric tons/m**2/yr

     Number of source-species
     combinations with variable
     emissions scaling factors
     provided below in (14d)        (NSAR1) Default: 0  !  NSAR1 =  0  !

     Number of buoyant polygon area sources
     with variable location and emission
     parameters (NAR2)                      No default  !  NAR2 =  0   !
     (If NAR2 > 0, ALL parameter data for
     these sources are read from the file: BAEMARB.DAT)

      !END!

---------------
### Subgroup (14b) Constant Emissions
---------------
                                          a
               AREA SOURCE: CONSTANT DATA
               ----------------------------
                                                               b
      Source           Effect.    Base      Initial    Emission
      No.             Height   Elevation   Sigma z     Rates
                        (m)       (m)        (m)      
      -------          ------    ------     --------   ---------


--------
    a
     Data for each source are treated as a separate input subgroup
     and therefore must end with an input group terminator.
    b
     An emission rate must be entered for every pollutant modeled.
     Enter emission rate of zero for secondary pollutants that are
     modeled, but not emitted.  Units are specified by IARU 
     (e.g. 1 for g/m**2/s).

---------------
### Subgroup (14c) Location of Source Vertex
---------------

           COORDINATES (km) FOR EACH VERTEX(4) OF EACH POLYGON
           --------------------------------------------------------
      Source^a
      No. Ordered list of X followed by list of Y, grouped by source


--------
    a
     Data for each source are treated as a separate input subgroup
     and therefore must end with an input group terminator.


---------------
### Subgroup (14d) Temporal variation of area sources
---------------
                                               a
          AREA SOURCE: VARIABLE EMISSIONS DATA
          --------------------------------------

     Use this subgroup to describe temporal variations in the emission
     rates given in 14b.  Factors entered multiply the rates in 14b.
     Skip sources here that have constant emissions.  For more elaborate
     variation in source parameters, use BAEMARB.DAT and NAR2 > 0.

     IVARY determines the type of variation, and is source-specific:
     (IVARY)                                Default: 0
           0 =       Constant
           1 =       Diurnal cycle (24 scaling factors: hours 1-24)
           2 =       Monthly cycle (12 scaling factors: months 1-12)
           3 =       Hour & Season (4 groups of 24 hourly scaling factors,
                                    where first group is DEC-JAN-FEB)
           4 =       Speed & Stab. (6 groups of 6 scaling factors, where
                                    first group is Stability Class A,
                                    and the speed classes have upper
                                    bounds (m/s) defined in Group 12
           5 =       Temperature   (12 scaling factors, where temperature
                                    classes have upper bounds (C) of:
                                    0, 5, 10, 15, 20, 25, 30, 35, 40,
                                    45, 50, 50+)



--------
    a
     Data for each species are treated as a separate input ### Subgroup
     and therefore must end with an input group terminator.


-------------------------------------------------------------------------------

## INPUT GROUPS: 15 -- Line source parameters
---------------------------

---------------
### Subgroup (15a) Number of Sources
---------------

     Number of buoyant line sources
     with variable location and emission
     parameters (NLN2)                              No default  !  NLN2 =  0   !

     (If NLN2 > 0, ALL parameter data for
      these sources are read from the file: LNEMARB.DAT)

     Number of buoyant line sources (NLINES)        No default   ! NLINES =  0  !

     Units used for line source
     emissions below                (ILNU)          Default: 1  !  ILNU =   1  !
           1 =        g/s
           2 =       kg/hr
           3 =       lb/hr
           4 =     tons/yr
           5 =     Odour Unit * m**3/s  (vol. flux of odour compound)
           6 =     Odour Unit * m**3/min
           7 =     metric tons/yr

     Number of source-species
     combinations with variable
     emissions scaling factors
     provided below in (15c)        (NSLN1) Default: 0  !  NSLN1 =  0  !

     Maximum number of segments used to model
     each line (MXNSEG)                             Default: 7   ! MXNSEG =  7  !

     The following variables are required only if NLINES > 0.  They are
     used in the buoyant line source plume rise calculations.

        Number of distances at which                Default: 6   ! NLRISE =  6  !
        transitional rise is computed

        Average building length (XL)                No default   ! XL = .0 !
                                                    (in meters)

        Average building height (HBL)               No default   ! HBL = .0 !
                                                    (in meters)

        Average building width (WBL)                No default   ! WBL = .0 !
                                                    (in meters)

        Average line source width (WML)             No default   ! WML = .0 !
                                                    (in meters)

        Average separation between buildings (DXL)  No default   ! DXL = .0 !
                                                    (in meters)

        Average buoyancy parameter (FPRIMEL)        No default   ! FPRIMEL = .0 !
                                                    (in m**4/s**3)

      !END!

---------------
### Subgroup (15b) Constant Emissions
---------------

               BUOYANT LINE SOURCE: CONSTANT DATA
               ----------------------------------
                                                                                                a
      Source     Beg. X      Beg. Y      End. X    End. Y     Release    Base        Emission
      No.     Coordinate  Coordinate  Coordinate Coordinate  Height    Elevation      Rates
                  (km)        (km)        (km)       (km)       (m)       (m)          
      ------   ----------  ----------  ---------  ----------  -------   ---------    ---------

--------

    a
     Data for each source are treated as a separate input Subgroup and therefore must end with an input group terminator.

    b
     An emission rate must be entered for every pollutant modeled.
     Enter emission rate of zero for secondary pollutants that are
     modeled, but not emitted.  Units are specified by ILNTU 
     (e.g. 1 for g/s).

---------------
### Subgroup (15c) Variable Emissions
---------------
                                                       a
          BUOYANT LINE SOURCE: VARIABLE EMISSIONS DATA
          ----------------------------------------------

     Use this Subgroup to describe temporal variations in the emission rates given in 15b.  Factors entered multiply the rates in 15b.
     Skip sources here that have constant emissions.

     IVARY determines the type of variation, and is source-specific:
     (IVARY)                                Default: 0
           0 =       Constant
           1 =       Diurnal cycle (24 scaling factors: hours 1-24)
           2 =       Monthly cycle (12 scaling factors: months 1-12)
           3 =       Hour & Season (4 groups of 24 hourly scaling factors,
                                    where first group is DEC-JAN-FEB)
           4 =       Speed & Stab. (6 groups of 6 scaling factors, where
                                    first group is Stability Class A,
                                    and the speed classes have upper
                                    bounds (m/s) defined in Group 12
           5 =       Temperature   (12 scaling factors, where temperature
                                    classes have upper bounds (C) of:
                                    0, 5, 10, 15, 20, 25, 30, 35, 40,
                                    45, 50, 50+)
--------
    a
     Data for each species are treated as a separate input Subgroup
     and therefore must end with an input group terminator.


-------------------------------------------------------------------------------


## INPUT GROUPS: 16 -- Volume source parameters
---------------------------

### Subgroup (16a) Number of Sources
---------------

     Number of volume sources with
     parameters provided in 16b,c (NVL1)     No default  !  NVL1 =  0   !

     Units used for volume source
     emissions below in 16b       (IVLU)     Default: 1  !  IVLU =   1  !
           1 =        g/s
           2 =       kg/hr
           3 =       lb/hr
           4 =     tons/yr
           5 =     Odour Unit * m**3/s  (vol. flux of odour compound)
           6 =     Odour Unit * m**3/min
           7 =     metric tons/yr

     Number of source-species
     combinations with variable
     emissions scaling factors
     provided below in (16c)      (NSVL1)    Default: 0  !  NSVL1 =  0  !

     Number of volume sources with
     variable location and emission
     parameters                   (NVL2)     No default  !  NVL2 =   0   !

     (If NVL2 > 0, ALL parameter data for
      these sources are read from the VOLEMARB.DAT file(s) )

      !END!

---------------
### Subgroup (16b) Constant Data
---------------
                                        a
           VOLUME SOURCE: CONSTANT DATA
           ------------------------------
                                                                               b
         X           Y        Effect.    Base     Initial    Initial    Emission
     Coordinate  Coordinate   Height   Elevation  Sigma y    Sigma z     Rates
        (km)       (km)         (m)       (m)        (m)       (m)      
     ----------  ----------   ------    ------    --------   --------   --------


--------
    a
     Data for each source are treated as a separate input  Subgroup
     and therefore must end with an input group terminator.

    b
     An emission rate must be entered for every pollutant modeled.
     Enter emission rate of zero for secondary pollutants that are
     modeled, but not emitted.  Units are specified by IVLU 
     (e.g. 1 for g/s).

---------------
### Subgroup (16c) Variable Emissions
---------------
                                                 a
          VOLUME SOURCE: VARIABLE EMISSIONS DATA
          ----------------------------------------

     Use this subgroup to describe temporal variations in the emission
     rates given in 16b.  Factors entered multiply the rates in 16b.
     Skip sources here that have constant emissions.  For more elaborate
     variation in source parameters, use VOLEMARB.DAT and NVL2 > 0.

     IVARY determines the type of variation, and is source-specific:
     (IVARY)                                Default: 0
           0 =       Constant
           1 =       Diurnal cycle (24 scaling factors: hours 1-24)
           2 =       Monthly cycle (12 scaling factors: months 1-12)
           3 =       Hour & Season (4 groups of 24 hourly scaling factors,
                                    where first group is DEC-JAN-FEB)
           4 =       Speed & Stab. (6 groups of 6 scaling factors, where
                                    first group is Stability Class A,
                                    and the speed classes have upper
                                    bounds (m/s) defined in Group 12
           5 =       Temperature   (12 scaling factors, where temperature
                                    classes have upper bounds (C) of:
                                    0, 5, 10, 15, 20, 25, 30, 35, 40,
                                    45, 50, 50+)



--------
    a
     Data for each species are treated as a separate input subgroup
     and therefore must end with an input group terminator.


-------------------------------------------------------------------------------

## INPUT GROUPS: 17 -- Non-gridded (discrete) receptor information
-----------------------

---------------
### Subgroup (17a) Number of Receptors
---------------

     Number of non-gridded receptors (NREC)  No default  !  NREC =  11371 !
     Number of receptor group names (NRGRP)  Default: 0  !  NRGRP =  0   !

      !END!
      * RGRPNAM =   X          *   *END*

---------------
### Subgroup (17b) List of Receptors
---------------
                                               a
           NON-GRIDDED (DISCRETE) RECEPTOR DATA
           ------------------------------------

                        X            Y          Ground        Height   b
    Receptor       Coordinate   Coordinate    Elevation   Above Ground
      No.             (km)         (km)          (m)           (m)
    --------       ----------   ----------    ---------   ------------
    1 !  X  = -124.5,-205.5,0.0,0 !!END!
    2 !  X  = -121.5,-205.5,0.0,0 !!END!
    3 !  X  = -118.5,-205.5,0.0,0 !!END!
    ...
    11371 !  X  = 121.5,202.5,0.0076263417,0 !!END!
-------------
    a
     Data for each receptor are treated as a separate input subgroup
     and therefore must end with an input group terminator.

    b
     Receptor height above ground is optional.  If no value is entered,
     the receptor is placed on the ground.

