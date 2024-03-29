---
layout: default
title: calpost.inp
nav_order: 1
parent: CALPOST
grand_parent: Trajectory Models
last_modified_date: 2022-06-07 12:06:02
tags: cpost
---

# calpost.inp
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

      CALPUFF Demonstration


      ---------------- Run title (3 lines) ------------------------------------------

                    CALPOST MODEL CONTROL FILE
                    --------------------------

-------------------------------------------------------------------------------

## INPUT GROUP: 0 輸入及輸出檔案名稱
--------------
### 指定輸入檔案名稱
---

|File|Default File Name| settings |說明|
|-|-|-|-|
|Conc/Dep Flux File|MODEL.DAT|! MODDAT =CALPUFF.CON   !|calpuff濃度結果檔|
|Relative Humidity File|VISB.DAT||分析能見度使用|
|Background Data File|BACK.DAT||加上模擬結果進行分析|
|Transmissometer or Nephelometer Data File or DATSAV Weather Data File or Prognostic Weather  File|||補充數據|

---

### 指定輸出入檔案名稱

|File|                      Default File Name|設定值|說明|
|-|:-:|:-:|-|
|List File|                 CALPOST.LST|        ! PSTLST =CALPOST.LST   !|程式執行情況之printout|
|Pathname for Timeseries Files (activate with exclamation points only if   providing NON-BLANK character string)|   (blank)|      * TSPATH =   *||
|Pathname for Plot Files(activate with exclamation points only if    providing NON-BLANK character string)<sup>1</sup>|   (blank)|* PLPATH =   *||
|Timeseries Peak Value|TSERIES_ASPEC_ttHR_CONC_TSUNAM.DAT PEAKVAL_ASPEC_ttHR_CONC_TSUNAM.DAT|* TSUNAM =   *||
|Top Nth Rank Plot|RANK(ALL)_ASPEC_ttHR_CONC_TUNAM.DAT or  RANK(ii)_ASPEC_ttHR_CONC_TUNAM.GRD| * TUNAM =   *||
|Exceedance Plot|EXCEED_ASPEC_ttHR_CONC_XUNAM.DAT or  EXCEED_ASPEC_ttHR_CONC_XUNAM.GRD|* XUNAM =   *||
|Echo Plot (Specific Days)|yyyy_Mmm_Ddd_hhmm(UTCszzzz)_L00_ASPEC_ttHR_CONC.DAT or yyyy_Mmm_Ddd_hhmm(UTCszzzz)_L00_ASPEC_ttHR_CONC.GRD|||
|Visibility Plot(Daily Peak Summary)|DAILY_VISIB_VUNAM.DAT|! VUNAM =VTEST   !||

1. User Character String (U) to augment default filenames (activate with exclamation points only if providing NON-BLANK character string)

### 輔助輸出入檔案名稱

|File|Default File Name|設定值|說明|
|-|:-:|:-:|-|
|Visibility Change|DELVIS.DAT|* DVISDAT =   *||

### 大小寫控制
      All file names will be converted to lower case if LCFILES = T
      Otherwise, if LCFILES = F, file names will be converted to UPPER CASE
         T = lower case               ! LCFILES = T !
         F = UPPER CASE
      NOTE: (1) file/path names can be up to 132 characters in length
      NOTE: (2) Filenames for ALL PLOT and TIMESERIES FILES are constructed
          using a template that includes a pathname, user-supplied
          character(s), and context-specific strings, where
             ASPEC = Species Name
              CONC = CONC Or WFLX Or DFLX Or TFLX
                tt = Averaging Period (e.g. 03)
                ii = Rank (e.g. 02)
                hh = Hour(ending) in LST
             szzzz = LST time zone shift (EST is -0500)
              yyyy = Year(LST)
                mm = Month(LST)
                dd = day of month (LST)
          are determined internally based on selections made below.
          If a path or user-supplied character(s) are supplied, each
          must contain at least 1 non-blank character.

      !END!

## INPUT GROUP: 1 一般控制參數
### 是否執行所有氣象檔案內之時間

     Option to run all periods found
     in the met. file(s)  (METRUN)        Default: 0   ! METRUN =   1  !

         METRUN = 0 - Run period explicitly defined below
         METRUN = 1 - Run all periods in CALPUFF data file(s)

     Starting date:    Year   (ISYR)  --    No default   ! ISYR  =  2022  !
                       Month  (ISMO)  --    No default   ! ISMO  =   3 !
                       Day    (ISDY)  --    No default   ! ISDY  =  22 !
     Starting time:    Hour   (ISHR)  --    No default   ! ISHR  =  1  !
                       Minute (ISMIN) --    No default   ! ISMIN =  0  !
                       Second (ISSEC) --    No default   ! ISSEC =  0  !

     Ending date:      Year   (IEYR)  --    No default   ! IEYR  =2022 !
                       Month  (IEMO)  --    No default   ! IEMO  =   3 !
                       Day    (IEDY)  --    No default   ! IEDY  =  22 !
     Ending time:      Hour   (IEHR)  --    No default   ! IEHR  = 24  !
                       Minute (IEMIN) --    No default   ! IEMIN =  0  !
                       Second (IESEC) --    No default   ! IESEC =  0  !

     (These are only used if METRUN = 0)

     All times are in the base time zone of the CALPUFF simulation.
     CALPUFF Dataset Version 2.1 contains the zone, but earlier versions
     do not, and the zone must be specified here.  The zone is the
     number of hours that must be ADDED to the time to obtain UTC (or GMT).
     Identify the Base Time Zone for the CALPUFF simulation
                              (BTZONE) -- No default   ! BTZONE = 0. !

     Process every period of data?
                                (NREP) -- Default: 1   ! NREP  =  1  !
      (1 = every period processed,
       2 = every 2nd period processed,
       5 = every 5th period processed, etc.)

### 物質種類、濃度及沉降訊息
----------------------------------------------

      Species to process (ASPEC)       -- No default   ! ASPEC = TSP  !
      (ASPEC = VISIB for visibility processing)

      Layer/deposition code (ILAYER)   -- Default: 1   ! ILAYER =  1  !
        '1'  for CALPUFF concentrations,
        '-1' for dry deposition fluxes,
        '-2' for wet deposition fluxes,
        '-3' for wet+dry deposition fluxes.
      by Kuang: the scaling factor change units from ug/m3 into ppb
      Scaling factors of the form:     -- Defaults:    ! A =  1.0    !
            X(new) = X(old) * A + B         A = 0.0    ! B =  0.0    !
        (NOT applied if A = B = 0.0)        B = 0.0

      Add Hourly Background Concentrations/Fluxes?
                              (LBACK)  -- Default: F   ! LBACK =  F !


      Source of NO2 when ASPEC=NO2 (above) or LVNO2=T (Group 2) may be
      from CALPUFF NO2 concentrations OR from a fraction of CALPUFF NOx
      concentrations.  Specify the fraction of NOx that is treated as NO2
      either as a constant or as a table of fractions that depend on the
      magnitude of the NOx concentration:
                             (NO2CALC) -- Default: 1   ! NO2CALC =   0  !
         0 =  Use NO2 directly (NO2 must be in file)
         1 =  Specify a single NO2/NOx ratio (RNO2NOX)
         2 =  Specify a table NO2/NOx ratios (TNO2NOX)
              (NOTE: Scaling Factors must NOT be used with NO2CALC=2)

      Single NO2/NOx ratio (0.0 to 1.0) for treating some
      or all NOx as NO2, where [NO2] = [NOX] * RNO2NOX
      (used only if NO2CALC = 1)
                             (RNO2NOX) -- Default: 1.0 ! RNO2NOX = 1.0 !

      Table of NO2/NOx ratios that vary with NOx concentration.
      Provide 14 NOx concentrations (ug/m**3) and the corresponding
      NO2/NOx ratio, with NOx increasing in magnitude.  The ratio used
      for a particular NOx concentration is interpolated from the values
      provided in the table.  The ratio for the smallest tabulated NOx
      concentration (the first) is used for all NOx concentrations less
      than the smallest tabulated value, and the ratio for the largest
      tabulated NOx concentration (the last) is used for all NOx
      concentrations greater than the largest tabulated value.
      (used only if NO2CALC = 2)

       NOx concentration(ug / m3)
                             (CNOX)    -- No default
         ! CNOX = 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0 !

       NO2/NOx ratio for each NOx concentration:
                             (TNO2NOX) -- No default
         ! TNO2NOX = 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 !


### 來源貢獻分析
------------------

  Option to process source contributions:
         0 =  Process only total reported contributions
         1 =  Sum all individual source contributions and process
         2 =  Run in TRACEBACK mode to identify source
              contributions at a SINGLE receptor
                             (MSOURCE) -- Default: 0   ! MSOURCE =  0  !


### 靜風處理選項
-------------------------------------

  Output from models other than CALPUFF and CALGRID can be written in
  the CONC.DAT format and processed by CALPOST.  Plume models such as
  AERMOD typically do not treat CALM hours, and do not include such hours
  in multiple-hour averages, with specific rules about how many calm hours
  can be removed from an average.  This treatment is known as CALM
  PROCESSING.  Calm periods are identified from wind speeds in the
  meteorological data file for the application, which must be identified
  in Input Group 0 as the single-point meteorological data file MET1DAT.
         0 =  Option is not used for CALPUFF/CALGRID output files
         1 =  Apply CALM processing procedures to multiple-hour averages
                          (MCALMPRO) -- Default: 0   ! MCALMPRO =  0  !

  Format of Single-point Met File
         1 =  AERMOD/AERMET SURFACE file
                           (MET1FMT) -- Default: 1   ! MET1FMT =  1  !


### 接受點訊息
--------------------

      Gridded receptors processed?    (LG) -- Default: F   ! LG  = T  !
      Discrete receptors processed?   (LD) -- Default: F   ! LD  = F  !
      CTSG Complex terrain receptors processed?
                                       (LCT) -- Default: F   ! LCT = F  !

      --Report results by DISCRETE receptor RING?
      (only used when LD = T)     (LDRING) -- Default: F   ! LDRING = F  !

      --Select range of DISCRETE receptors (only used when LD = T):

      Select ALL DISCRETE receptors by setting NDRECP flag to -1;
                                    OR
      Select SPECIFIC DISCRETE receptors by entering a flag (0,1) for each
         0 = discrete receptor not processed
         1 = discrete receptor processed
      using repeated value notation to select blocks of receptors:
         23*1, 15*0, 12*1
      Flag for all receptors after the last one assigned is set to 0
      (NDRECP) -- Default: -1
                                                   ! NDRECP =  -1  !


      --Select range of GRIDDED receptors (only used when LG = T):

            X index of LL corner (IBGRID) -- Default: -1     ! IBGRID = -1  !
               (-1 OR 1 <= IBGRID <= NX)

            Y index of LL corner (JBGRID) -- Default: -1     ! JBGRID = -1  !
               (-1 OR 1 <= JBGRID <= NY)

            X index of UR corner (IEGRID) -- Default: -1     ! IEGRID = -1  !
               (-1 OR 1 <= IEGRID <= NX)

            Y index of UR corner (JEGRID) -- Default: -1     ! JEGRID = -1  !
               (-1 OR 1 <= JEGRID <= NY)

      Note: Entire grid is processed if IBGRID=JBGRID=IEGRID=JEGRID=-1


      --Specific gridded receptors can also be excluded from CALPOST
      processing by filling a processing grid array with 0s and 1s.  If the
      processing flag for receptor index (i,j) is 1 (ON), that receptor
      will be processed if it lies within the range delineated by IBGRID,
      JBGRID,IEGRID,JEGRID and if LG=T. If it is 0 (OFF), it will not be
      processed in the run.  By default, all array values are set to 1 (ON).

      Number of gridded receptor rows provided in Subgroup (1a) to
      identify specific gridded receptors to process
                                 (NGONOFF) -- Default: 0      ! NGONOFF =  0  !

      !END!


--------------
### Subgroup (1a) 包括或排除特定接受點
--------------

    Specific gridded receptors are excluded from CALPOST processing
    by filling a processing grid array with 0s and 1s.  A total of
    NGONOFF lines are read here.  Each line corresponds to one 'row'
    in the sampling grid, starting with the NORTHERNMOST row that
    contains receptors that you wish to exclude, and finishing with
    row 1 to the SOUTH (no intervening rows may be skipped).  Within
    a row, each receptor position is assigned either a 0 or 1,
    starting with the westernmost receptor.
       0 = gridded receptor not processed
       1 = gridded receptor processed

    Repeated value notation may be used to select blocks of receptors:
       23*1, 15*0, 12*1

    Because all values are initially set to 1, any receptors north of
    the first row entered, or east of the last value provided in a row,
    remain ON.

    (NGXRECP) -- Default: 1


-------------------------------------------------------------------------------

## INPUT GROUP: 2 能見度參數 (ASPEC = VISIB)
--------------

    Test visibility options specified to see
    if they conform to FLAG 2008 configuration?
                           (MVISCHECK) -- Default: 1   ! MVISCHECK =  0   !
         0 =  NO checks are made
         1 =  Technical options must conform to FLAG 2008 visibility guidance
                ASPEC   = VISIB
                LVNO2   = T
                NO2CALC = 1
                RNO2NOX = 1.0
                MVISBK  = 8
                M8_MODE = 5

    Some of the data entered for use with the FLAG 2008 configuration
    are specific to the Class I area being evaluated. These values can
    be checked within the CALPOST user interface when the name of the
    Class I area is provided.

    Name of Class I Area (used for QA purposes only)
                            (AREANAME) -- Default: User  ! AREANAME =  User !


    Particle growth curve f(RH) for hygroscopic species
                                (MFRH) -- Default: 4   ! MFRH   =  4  !

         1 =  IWAQM (1998) f(RH) curve (originally used with MVISBK=1)
         2 =  FLAG (2000) f(RH) tabulation
         3 =  EPA (2003) f(RH) tabulation
         4 =  IMPROVE (2006) f(RH) tabulations for sea salt, and for small and
              large SULFATE and NITRATE particles;
              Used in Visibility Method 8 (MVISBK = 8 with M8_MODE = 1, 2, or 3)

    Maximum relative humidity (%) used in particle growth curve
                               (RHMAX) -- Default: 98  ! RHMAX  = 98 !

    Modeled species to be included in computing the light extinction
     Include SULFATE?          (LVSO4) -- Default: T   ! LVSO4  = T  !
     Include NITRATE?          (LVNO3) -- Default: T   ! LVNO3  = T  !
     Include ORGANIC CARBON?   (LVOC)  -- Default: T   ! LVOC   = F  !
     Include COARSE PARTICLES? (LVPMC) -- Default: T   ! LVPMC  = F  !
     Include FINE PARTICLES?   (LVPMF) -- Default: T   ! LVPMF  = F  !
     Include ELEMENTAL CARBON? (LVEC)  -- Default: T   ! LVEC   = T  !
     Include NO2 absorption?   (LVNO2) -- Default: F   ! LVNO2  = T  !
              With Visibility Method 8 -- Default: T
                                          FLAG (2008)

    And, when ranking for TOP-N, TOP-50, and Exceedance tables,
     Include BACKGROUND?       (LVBK)  -- Default: T   ! LVBK   = T  !

    Species name used for particulates in MODEL.DAT file
                   COARSE    (SPECPMC) -- Default: PMC ! SPECPMC = PMC !
                   FINE      (SPECPMF) -- Default: PMF ! SPECPMF = PMF !

### 消光效率 (1/Mm per ug/m**3)
----------------------------------------
    MODELED particulate species:
               PM  COARSE      (EEPMC) -- Default: 0.6   ! EEPMC  = 0.6 !
               PM  FINE        (EEPMF) -- Default: 1.0   ! EEPMF  = 1 !
    BACKGROUND particulate species:
               PM  COARSE    (EEPMCBK) -- Default: 0.6   ! EEPMCBK = 0.6 !
    Other species:
              AMMONIUM SULFATE (EESO4) -- Default: 3.0   ! EESO4  = 3 !
              AMMONIUM NITRATE (EENO3) -- Default: 3.0   ! EENO3  = 3 !
              ORGANIC CARBON   (EEOC)  -- Default: 4.0   ! EEOC   = 4 !
              SOIL             (EESOIL)-- Default: 1.0   ! EESOIL = 1 !
              ELEMENTAL CARBON (EEEC)  -- Default: 10.   ! EEEC   = 10 !
              NO2 GAS          (EENO2) -- Default: .1755 ! EENO2  = 0.1755 !
    Visibility Method 8:
              AMMONIUM SULFATE (EESO4S)   Set Internally (small)
              AMMONIUM SULFATE (EESO4L)   Set Internally (large)
              AMMONIUM NITRATE (EENO3S)   Set Internally (small)
              AMMONIUM NITRATE (EENO3L)   Set Internally (large)
              ORGANIC CARBON   (EEOCS)    Set Internally (small)
              ORGANIC CARBON   (EEOCL)    Set Internally (large)
              SEA SALT         (EESALT)   Set Internally

### 背景消光計算
---------------------------------

    Method used for the 24h-average of percent change of light extinction:
    Hourly ratio of source light extinction / background light extinction
    is averaged?               (LAVER) -- Default: F   ! LAVER = F  !


    Method used for background light extinction
                              (MVISBK) -- Default: 8   ! MVISBK =  8  !
                                          FLAG (2008)

         1 =  Supply single light extinction and hygroscopic fraction
              - Hourly F(RH) adjustment applied to hygroscopic background
                and modeled sulfate and nitrate
         2 =  Background extinction from speciated PM concentrations (A)
              - Hourly F(RH) adjustment applied to observed and modeled sulfate
                and nitrate
              - F(RH) factor is capped at F(RHMAX)
         3 =  Background extinction from speciated PM concentrations (B)
              - Hourly F(RH) adjustment applied to observed and modeled sulfate
                and nitrate
              - Receptor-hour excluded if RH>RHMAX
              - Receptor-day excluded if fewer than 6 valid receptor-hours
         4 =  Read hourly transmissometer background extinction measurements
              - Hourly F(RH) adjustment applied to modeled sulfate and nitrate
              - Hour excluded if measurement invalid (missing, interference,
                or large RH)
              - Receptor-hour excluded if RH>RHMAX
              - Receptor-day excluded if fewer than 6 valid receptor-hours
         5 =  Read hourly nephelometer background extinction measurements
              - Rayleigh extinction value (BEXTRAY) added to measurement
              - Hourly F(RH) adjustment applied to modeled sulfate and nitrate
              - Hour excluded if measurement invalid (missing, interference,
                or large RH)
              - Receptor-hour excluded if RH>RHMAX
              - Receptor-day excluded if fewer than 6 valid receptor-hours
         6 =  Background extinction from speciated PM concentrations
              - FLAG (2000) monthly RH adjustment factor applied to observed and
                and modeled sulfate and nitrate
         7 =  Use observed weather or prognostic weather information for
              background extinction during weather events; otherwise, use Method 2
              - Hourly F(RH) adjustment applied to modeled sulfate and nitrate
              - F(RH) factor is capped at F(RHMAX)
              - During observed weather events, compute Bext from visual range
                if using an observed weather data file, or
              - During prognostic weather events, use Bext from the prognostic
                weather file
              - Use Method 2 for hours without a weather event
         8 =  Background extinction from speciated PM concentrations using
              the IMPROVE (2006) variable extinction efficiency formulation
              (MFRH must be set to 4)
              - Split between small and large particle concentrations of
                SULFATES, NITRATES, and ORGANICS is a function of concentration
                and different extinction efficiencies are used for each
              - Source-induced change in visibility includes the increase in
                extinction of the background aerosol due to the change in the
                extinction efficiency that now depends on total concentration.
              - Fsmall(RH) and Flarge(RH) adjustments for small and large
                particles are applied to observed and modeled sulfate and
                nitrate concentrations
              - Fsalt(RH) adjustment for sea salt is applied to background
                sea salt concentrations
              - F(RH) factors are capped at F(RHMAX)
              - RH for Fsmall(RH), Flarge(RH), and Fsalt(RH) may be obtained
                from hourly data as in Method 2 or from the FLAG monthly RH
                adjustment factor used for Method 6 where EPA F(RH) tabulation
                is used to infer RH, or monthly Fsmall, Flarge, and Fsalt RH
                adjustment factors can be directly entered.
                Furthermore, a monthly RH factor may be applied to either hourly
                concentrations or daily concentrations to obtain the 24-hour
                extinction.
                These choices are made using the M8_MODE selection.

    Additional inputs used for MVISBK = 1:
    --------------------------------------
     Background light extinction (1/Mm)
                              (BEXTBK) -- No default   ! BEXTBK = 12 !
     Percentage of particles affected by relative humidity
                              (RHFRAC) -- No default   ! RHFRAC = 10 !

    Additional inputs used for MVISBK = 6,8:
    ----------------------------------------
     Extinction coefficients for hygroscopic species (modeled and
     background) are computed using a monthly RH adjustment factor
     in place of an hourly RH factor (VISB.DAT file is NOT needed).
     Enter the 12 monthly factors here (RHFAC).  Month 1 is January.

     (RHFAC)  -- No default     ! RHFAC = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 !

    Additional inputs used for MVISBK = 7:
    --------------------------------------
     The weather data file (DATSAV abbreviated space-delimited) that
     is identified as VSRN.DAT may contain data for more than one
     station.  Identify the stations that are needed in the order in
     which they will be used to obtain valid weather and visual range.
     The first station that contains valid data for an hour will be
     used.  Enter up to MXWSTA (set in PARAMS file) integer station IDs
     of up to 6 digits each as variable IDWSTA, and enter the corresponding
     time zone for each, as variable TZONE (= UTC-LST).

     A prognostic weather data file with Bext for weather events may be used
     in place of the observed weather file.  Identify this as the VSRN.DAT
     file and use a station ID of IDWSTA = 999999, and TZONE = 0.

     NOTE:  TZONE identifies the time zone used in the dataset.  The
            DATSAV abbreviated space-delimited data usually are prepared
            with UTC time rather than local time, so TZONE is typically
            set to zero.

     (IDWSTA)   -- No default   * IDWSTA = 000000 *
     (TZONE)    -- No default   * TZONE =      0. *

    Additional inputs used for MVISBK = 2,3,6,7,8:
    ----------------------------------------------
     Background extinction coefficients are computed from monthly
     CONCENTRATIONS of ammonium sulfate (BKSO4), ammonium nitrate (BKNO3),
     coarse particulates (BKPMC), organic carbon (BKOC), soil (BKSOIL), and
     elemental carbon (BKEC).  Month 1 is January.
     (ug/m**3)

     (BKSO4)  -- No default     ! BKSO4 = 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !
     (BKNO3)  -- No default     ! BKNO3 = 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !
     (BKPMC)  -- No default     ! BKPMC = 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !
     (BKOC)   -- No default     ! BKOC  = 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !
     (BKSOIL) -- No default     ! BKSOIL= 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !
     (BKEC)   -- No default     ! BKEC  = 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !

    Additional inputs used for MVISBK = 8:
    --------------------------------------
     Extinction coefficients for hygroscopic species (modeled and
     background) may be computed using hourly RH values and hourly
     modeled concentrations, or using monthly RH values inferred from
     the RHFAC adjustment factors and either hourly or daily modeled
     concentrations, or using monthly RHFSML, RHFLRG, and RHFSEA adjustment
     factors and either hourly or daily modeled concentrations.

     (M8_MODE) -- Default: 5     ! M8_MODE=  5   !
                  FLAG (2008)

          1 = Use hourly RH values from VISB.DAT file with hourly
              modeled and monthly background concentrations.
          2 = Use monthly RH from monthly RHFAC and EPA (2003) f(RH) tabulation
              with hourly modeled and monthly background concentrations.
              (VISB.DAT file is NOT needed).
          3 = Use monthly RH from monthly RHFAC and EPA (2003) f(RH) tabulation
              with daily modeled and monthly background concentrations.
              (VISB.DAT file is NOT needed).
          4 = Use monthly RHFSML, RHFLRG, and RHFSEA with hourly modeled
              and monthly background concentrations.
              (VISB.DAT file is NOT needed).
          5 = Use monthly RHFSML, RHFLRG, and RHFSEA with daily modeled
              and monthly background concentrations.
              (VISB.DAT file is NOT needed).

     Background extinction coefficients are computed from monthly
     CONCENTRATIONS of sea salt (BKSALT).  Month 1 is January.
     (ug/m**3)

     (BKSALT) -- No default     ! BKSALT= 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !

     Extinction coefficients for hygroscopic species (modeled and
     background) can be computed using monthly RH adjustment factors
     in place of an hourly RH factor (VISB.DAT file is NOT needed).
     Enter the 12 monthly factors here (RHFSML,RHFLRG,RHFSEA).
     Month 1 is January.  (Used if M8_MODE = 4 or 5)

     Small ammonium sulfate and ammonium nitrate particle sizes
     (RHFSML) -- No default     ! RHFSML= 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !

     Large ammonium sulfate and ammonium nitrate particle sizes
     (RHFLRG) -- No default     ! RHFLRG= 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !

     Sea salt particles
     (RHFSEA) -- No default     ! RHFSEA= 0, 0, 0, 0,
                                          0, 0, 0, 0,
                                          0, 0, 0, 0 !

    Additional inputs used for MVISBK = 2,3,5,6,7,8:
    ------------------------------------------------
     Extinction due to Rayleigh scattering is added (1/Mm)
                             (BEXTRAY) -- Default: 10.0 ! BEXTRAY = 10 !

      !END!
-------------------------------------------------------------------------------

## INPUT GROUP: 3 輸出選項
--------------

### 文件
    Documentation records contained in the header of the
    CALPUFF output file may be written to the list file.
    Print documentation image?
                                (LDOC) -- Default: F   !  LDOC = F !

### 輸出單位
------------
    Units for All Output       (IPRTU) -- Default: 1   ! IPRTU =  3   !
                     for            for
                Concentration    Deposition
       1 =         g/m**3         g/m**2/s
       2 =        mg/m**3        mg/m**2/s
       3 =        ug/m**3        ug/m**2/s
       4 =        ng/m**3        ng/m**2/s
       5 =      Odour Units

    Visibility: extinction expressed in 1/Mega-meters (IPRTU is ignored)


### 平均時間
--------------------------

    1-pd averages           (L1PD) -- Default: T   !   L1PD = F  !
    (pd = averaging period of model output)

    1-hr averages           (L1HR) -- Default: T   !   L1HR = T  !

    3-hr averages           (L3HR) -- Default: T   !   L3HR = F  !

    24-hr averages         (L24HR) -- Default: T   !  L24HR = T  !

    Run-length averages    (LRUNL) -- Default: T   !  LRUNL = T  !

    User-specified averaging time in hours, minutes, seconds
    - results for this averaging time are reported if it is not zero

                           (NAVGH) -- Default: 0   !   NAVGH =  0  !
                           (NAVGM) -- Default: 0   !   NAVGM =  0  !
                           (NAVGS) -- Default: 0   !   NAVGS =  0  !


### 報告表格
------------------------------

   1) Visibility: daily visibility tabulations are always reported
                  for the selected receptors when ASPEC = VISIB.
                  In addition, any of the other tabulations listed
                  below may be chosen to characterize the light
                  extinction coefficients.
                  [List file or Plot/Analysis File]


   2) Top 50 table for each averaging time selected
      [List file only]
                            (LT50) -- Default: T   !   LT50 = F  !

   3) Top 'N' table for each averaging time selected
      [List file or Plot file]
                           (LTOPN) -- Default: F   !  LTOPN = T  !

        -- Number of 'Top-N' values at each receptor
           selected (NTOP must be <= 4)
                            (NTOP) -- Default: 4   ! NTOP =  1   !

        -- Specific ranks of 'Top-N' values reported
           (NTOP values must be entered)
                   (ITOP(4) array) -- Default:     ! ITOP =  1   !
                                      1,2,3,4


   4) Threshold exceedance counts for each receptor and each averaging
      time selected
      [List file or Plot file]
                           (LEXCD) -- Default: F   !  LEXCD = F  !

        -- Identify the threshold for each averaging time by assigning a
           non-negative value (output units).

                                   -- Default: -1.0
           Threshold for  1-hr averages   (THRESH1) !  THRESH1 = 10 !
           Threshold for  3-hr averages   (THRESH3) !  THRESH3 = -1.0  !
           Threshold for 24-hr averages  (THRESH24) ! THRESH24 = -1.0  !
           Threshold for NAVG-hr averages (THRESHN) !  THRESHN = -1.0  !


        -- Counts for the shortest averaging period selected can be
           tallied daily, and receptors that experience more than NCOUNT
           counts over any NDAY period will be reported.  This type of
           exceedance violation output is triggered only if NDAY > 0.

           Accumulation period(Days)
                            (NDAY) -- Default: 0   !    NDAY =  0  !
           Number of exceedances allowed
                          (NCOUNT) -- Default: 1   !  NCOUNT =  1  !


   5) Selected day table(s)

      Echo Option -- Many records are written each averaging period
      selected and output is grouped by day
      [List file or Plot file]
                           (LECHO) -- Default: F   !  LECHO = F  !

      Timeseries Option -- Averages at all selected receptors for
      each selected averaging period are written to timeseries files.
      Each file contains one averaging period, and all receptors are
      written to a single record each averaging time.
      [TSERIES_ASPEC_ttHR_CONC_TSUNAM.DAT files]
                           (LTIME) -- Default: F   !  LTIME = F  !

      Peak Value Option -- Averages at all selected receptors for
      each selected averaging period are screened and the peak value
      each period is written to timeseries files.
      Each file contains one averaging period.
      [PEAKVAL_ASPEC_ttHR_CONC_TSUNAM.DAT files]
                           (LPEAK) -- Default: F   !  LPEAK = F  !

        -- Days selected for output
                      (IECHO(366)) -- Default: 366*0
           ! IECHO  = 366*0  !
           (366 values must be entered)

### 繪圖選項
-------------------

     Plot files can be created for the Top-N, Exceedance, and Echo
     tables selected above.  Two formats for these files are available,
     DATA and GRID.  In the DATA format, results at all receptors are
     listed along with the receptor location [x,y,val1,val2,...].
     In the GRID format, results at only gridded receptors are written,
     using a compact representation.  The gridded values are written in
     rows (x varies), starting with the most southern row of the grid.
     The GRID format is given the .GRD extension, and includes headers
     compatible with the SURFER(R) plotting software.

     A plotting and analysis file can also be created for the daily
     peak visibility summary output, in DATA format only.

     Generate Plot file output in addition to writing tables
     to List file?
                                 (LPLT) -- Default: F   ! LPLT  = T !

     Use GRID format rather than DATA format,
     when available?
                                 (LGRD) -- Default: F   ! LGRD  = T !


### 後續分析輔助輸出
------------------------------------------------

      Visibility

      A separate output file may be requested that contains the change
      in visibility at each selected receptor when ASPEC = VISIB.  This
      file can be processed to construct visibility measures that are
      not available in CALPOST.

      Output file with the visibility change at each receptor?
                                (MDVIS) -- Default: 0   ! MDVIS  =  0  !

           0 =  Do Not create file
           1 =  Create file of DAILY (24 hour) Delta-Deciview
           2 =  Create file of DAILY (24 hour) Extinction Change (%)
           3 =  Create file of HOURLY Delta-Deciview
           4 =  Create file of HOURLY Extinction Change (%)


### 偵錯輸出
-----------------------

      Output selected information to List file
      for debugging?
                                 (LDEBUG) -- Default: F  ! LDEBUG  = F !

      Output hourly extinction information to REPORT.HRV?
      (Visibility Method 7)
                                 (LVEXTHR) -- Default: F  ! LVEXTHR = F !

      !END!

      !END!
