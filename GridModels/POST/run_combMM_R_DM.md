---
layout: default
title: 綜合空品項目之計算
parent: Post Processing
grand_parent: CMAQ Model System
nav_order: 1
date: 2021-12-16 11:34:01
last_modified_date:   2021-12-19 14:12:15
---

# **CMAQ**綜合空品項目之計算(combine)
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

## 背景
- 由於CCTM是按照日期進行檔案的輸出，污染項目也是按照226項細項輸出，因此如需複合之空品項目如PM、VOCs等，則需進行後處理combine.exe。
  - 如只是需要特定污染項目，直接使用[ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#變數variable)進行讀取切割較為簡便。注意ACONC檔案之濃度單位為ppm(或&mu;g/M<sup>3</sup>)。
- 測站定點濃度之讀取，需待combine處理後，另以write_site程式處理。

## 腳本程式說明
### 程式名稱
- [run_combMM_RR_DM.csh](https://github.com/sinotec2/cmaq_relatives/blob/master/post/run_combMM_R_DM.csh)
- 修改自[USEAP_CMAQ](https://github.com/USEPA/CMAQ)之[run_combine.csh](https://github.com/USEPA/CMAQ/blob/main/POST/combine/scripts/run_combine.csh)

### I/O檔案
- CCTM執行結果
  - CCTM_ACONC檔案：逐日小時平均濃度、共有226項空氣品質，含4項大氣要素
  - CCTM_APMDIAG檔案：網格點上各粒徑比例之小時平均紀錄
- 氣象數據
  - METCRO3D
  - METCRO2D
- 空品/沉降量定義檔：$[SPECIES_DEF](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/#species_def檔案之設定)
- 結果檔案OUTFILE 
  - 小時平均濃度：${POSTDIR}/COMBINE_ACONC_${CTM_APPD}，共有135項(在$SPECIES_DEF中定義)。
  - 小時沉降量：${POSTDIR}/COMBINE_DEP_${CTM_APPD}

### 執行方式
- 讀取引數：2碼月份、批次序(5\~12)、[網格編號](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/run_mcipMM_RR_DM/#網格系統詳細定義)(`d01`/`d02`/`d04`、無`d03`)
  - `CAS`設定為**TEDS**編號，與年代有關，2019附近使用TEDS**11**

### SPECIES_DEF檔案之設定
- 參考[github.USEPA樣板](https://github.com/USEPA/CMAQ/blob/main/CCTM/src/MECHS/cb6r3_ae7_aq/SpecDef_cb6r3_ae7_aq.txt)
- `!`之後為註解沒作用，將回復到內設值。
- `#`之後為變數名稱。
- 層數之定義
  - 此範例將只會進行第1層(地面層)的整併。
  - 如加上`!`之後，程式將會按照CCTM_ACONC的層數進行合併

```
[kuang@DEVP 2018base]$ echo $SPEC_CONC
../CMAQ_Project/POST/combine/scripts/spec_def_files/SpecDef_cb6r3_ae7_aq.txt
[kuang@DEVP 2018base]$ head $SPEC_CONC
!#start   YYYYJJJ  000000
!#end     YYYYJJJ  230000
#layer    1
```
### VOC之定義

```fortran
VOC             ,ppbC      ,1000.0* (PAR[1] +2.0*ETHA[1] +3.0*PRPA[1] +MEOH[1]\
                            +2.0*ETH[1] +2.0*ETOH[1] +2.0*OLE[1] +3.0*ACET[1] \
                            +7.0*TOL[1] +8.0*XYLMN[1] +6.0*BENZENE[1] \
                            +FORM[1] +3.0*GLY[1] +4.0*KET[1] +2.0*ETHY[1] \
                           +2.0*ALD2[1] + 2.0*ETHA[1] + 4.0*IOLE[1] + 2.0*ALDX[1]  \
                           +5.0*ISOP[1] + 10.0*TERP[1]+ 10.0*NAPH[1] +10.*APIN[1])
```
### 粒狀物之定義
- total ions in particulate ATOT
  - ATOTI[0]、ATOTJ[0]、ATOTK[0]為i,j,k 3個mode之粒狀物濃度加總結果。

```fortran
!! Total PM Aggregates
ATOTI           ,ug m-3     ,ASO4I[1]+ANO3I[1]+ANH4I[1]+ANAI[1]+ACLI[1] \
                           +AECI[1]+AOMI[0]+AOTHRI[1]
ATOTJ           ,ug m-3     ,ASO4J[1]+ANO3J[1]+ANH4J[1]+ANAJ[1]+ACLJ[1] \
                           +AECJ[1]+AOMJ[0]+AOTHRJ[1]+AFEJ[1]+ASIJ[1]  \
                           +ATIJ[1]+ACAJ[1]+AMGJ[1]+AMNJ[1]+AALJ[1]+AKJ[1]
ATOTK           ,ug m-3     ,ASOIL[1]+ACORS[1]+ASEACAT[1]+ACLK[1]+ASO4K[1] \
                           +ANO3K[1]+ANH4K[1]
```
- i,j,k分別為
  - [Aitken][Aitken] mode、
  - [accumulation][acm] mode、及 
  - [coarse][crs] mode。

[Aitken]: <https://www.sciencedirect.com/topics/earth-and-planetary-sciences/aitken-nuclei> "The Aitken nuclei, with 0.01 < D < 0.08 μm, arise from ambient-temperature gas-to-particle conversion as well as combustion processes in which hot, supersaturated vapors are formed and subsequently undergo condensation.(From: Chemistry of the Upper and Lower Atmosphere, 2000)"
[acm]:<https://glossary.ametsoc.org/wiki/Accumulation_mode> "Aerosol particles in the size range 0.5–2 μm in diameter. The name arises from the fact that particles in this size range are aerodynamically stable and do not settle out, nor do they agglomerate to form larger particles; thus they tend to accumulate in the atmosphere."
[crs]: <https://ec.europa.eu/health/scientific_committees/opinions_layman/en/indoor-air-pollution/glossary/abc/coarse-particles.htm> "Coarse particles are the relatively large airborne particles mainly produced by the mechanical break-up of even larger solid particles. Examples of coarse particles include dust, pollen, spores, fly ash, and plant and insect parts. Coarse particles have an aerodynamic diameter ranging from 2.5 to 10µm (PM10-2.5), which distinguishes them from the smaller airborne particulate matter referred to as fine (PM2.5) and ultrafine particles (PM0.1)."

- PM<sub>2.5</sub>的定義
  - 為前述i,j,k各集成濃度、與其PM<sub>2.5</sub>粒徑所佔重量比例之sumproduct，公式如下

```fortran
!! PM 2.5
PM25_TOT        ,ug m-3     ,ATOTI[0]*PM25AT[3]+ATOTJ[0]*PM25AC[3]+ATOTK[0]*PM25CO[3]
```
- PM25AT[3]、PM25AC[3]、PM25CO[3]三個值對應到i,j,k mode濃度在PM2.5粒徑之貢獻比例
  - 為CCTM_APMDIAG檔案之內容
  - 這些比例值隨時間、空間、以及**排放個案**而異。

- PM<sub>10</sub>的定義，類似PM25_TOT的計算方式，只是改成對應到PM<sub>10</sub>的重量比例。

```fortran
!     PM10.0 and Coarse-Sized Species
PM10            ,ug m-3     ,ATOTI[0]*PM10AT[3]+ATOTJ[0]*PM10AC[3]+ATOTK[0]*PM10CO[3]
```

### 分段說明
- 原腳本說明段

```python
$ cat -n ~/GitHub/cmaq_relatives/combine/run_combMM_R_DM.csh
     1	#! /bin/csh -f
     2	
     3	# ====================== COMBINE_v5.3 Run Script ======================== 
     4	# Usage: run.combine.uncoupled.csh >&! combine_v53_uncoupled.log &                                
     5	#
     6	# To report problems or request help with this script/program:     
     7	#             http://www.epa.gov/cmaq    (EPA CMAQ Website)
     8	#             http://www.cmascenter.org  (CMAS Website)
     9	# ===================================================================  
    10	
    11	# ==================================================================
    12	#> Runtime Environment Options
    13	# ==================================================================
    14	
    15	#> Choose compiler and set up CMAQ environment with correct
    16	#> libraries using config.cmaq. Options: intel | gcc | pgi
```
- 基本環境變數設定
  - 編譯器版本`gcc`
  - 程式碼位置
  - 程式I/O檔案目錄

```python
    17	 setenv compiler gcc
    18	
    19	#> Set location of CMAQ repo.  This will be used to point to the correct species definition files.
    20	 setenv REPO_HOME  ../CMAQ_Project
    21	 #> Source the config.cmaq file to set the build environment
    22	 source $REPO_HOME/config_cmaq.csh gcc
    23	 setenv CMAQ_HOME $PWD
    24	 setenv CMAQ_DATA  /nas1/cmaqruns/2018base/data
    25	
```
- 讀取引數(月、[批次序](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/#批次的定義)、[網格編號](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/run_mcipMM_RR_DM/#網格系統詳細定義))

```python
    26	set MO         = $argv[1]
    27	set RUN        = $argv[2]
    28	set DM         = $argv[3]
    29	
    30	       
```
- 一般定義
  - 年代、TEDS版本須手動修改

```python
    31	#> Set General Parameters for Configuring the Simulation
    32	 set VRSN      = v53               #> Code Version
    33	 set PROC      = mpi               #> serial or mpi
    34	 set MECH      = cb6r3_ae7_aq      #> Mechanism ID
    35	 set APPL      = 18${MO}              #> Application Name (e.g. Gridname)
    36	 set STKCASEE  = 11   
    37	                                                      
 ```
- 執行程式位置
  - 此環境變數不易修改，如欲切換執行其他工作批次檔，「應」跳出此次csh另外定義(使用[tmux](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/OperationSystem/tmux/))。

```python
   38	#> Define RUNID as any combination of parameters above or others. By default,
    39	#> this information will be collected into this one string, $RUNID, for easy
    40	#> referencing in output binaries and log files as well as in other scripts.
    41	 setenv RUNID  ${VRSN}_${compilerString}_${APPL}
    42	
    43	#> Set the build directory if this was not set above 
    44	#> (this is where the CMAQ executable is located by default).
    45	#if ( ! $?BINDIR ) then
    46	  setenv BINDIR $REPO_HOME/POST/combine/scripts/BLD_combine_${VRSN}_${compilerString}
    47	#endif
    48	
    49	#> Set the name of the executable.
    50	 setenv EXEC combine_${VRSN}.exe
    51	
    52	
```
- 對照網格編號及名稱(詳[網格系統詳細定義](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/#網格系統詳細定義))

```python
    53	#> Set working, input and output directories
    54	if ( $DM == 'd01' ) then
    55	  setenv GRID_NAME  EAsia_81K        
    56	else if ( $DM == 'd02' ) then
    57	  setenv GRID_NAME  sChina_27k        
    58	else if( $DM == 'd04' ) then
    59	  setenv GRID_NAME  TWN_3X3           
    60	else
    61	  echo "Error input d02/d04"
    62	  exit 1
    63	endif
    64	
```
- 輸入/輸出檔案及路徑

```python
    65	# setenv GRID_NAME TWN_3X3                 #> check GRIDDESC file for GRID_NAME options
    66	 setenv CCTMOUTDIR ${CMAQ_DATA}/output_CCTM_${RUNID}      #> CCTM Output Directory
    67	 setenv POSTDIR    ${CCTMOUTDIR}/POST                     #> Location where combine file will be written
    68	
    69	  if ( ! -e $POSTDIR ) then
    70		  mkdir $POSTDIR
    71	  endif
    72	
    73	
    74	
    75	# =====================================================================
    76	#> COMBINE Configuration Options
    77	# =====================================================================
    78	
```
- 日期、日數之計算

```python
    79	#> Set Start and End Days for looping
    80	 set BEG_DATE = `date -ud "2018-${MO}-15 -1 month" +%Y-%m-%d `
    81	 set END_DATE = `date -ud "2018-${MO}-01 +1 month" +%Y-%m-%d `
    82	#  echo ${APPL}|cut -d'n' -f2
    83	# set MRUN = `echo ${APPL}|cut -d'n' -f2`
    84	 set MRUN = 4 
    85	  @ NDYS = $MRUN * 4
    86	 set START_DATE = `date -ud "${BEG_DATE} +${NDYS}days" +%Y-%m-%d `
    87	 set END_DATE = `date -ud "${START_DATE} +32days" +%Y-%m-%d`
    88	 
```
- 物質名稱之定義
  - VOC、PM<sub>2.5</sub>、PM<sub>10</sub>之開啟與其詳細計算公式
  - 「輸出檔的層數」也在此檔案內修改
  - 濃度與沉降量2大類

```python
    89	#> Set location of species definition files for concentration and deposition species.
    90	 setenv SPEC_CONC $REPO_HOME/POST/combine/scripts/spec_def_files/SpecDef_${MECH}.txt
    91	 setenv SPEC_DEP  $REPO_HOME/POST/combine/scripts/spec_def_files/SpecDef_Dep_${MECH}.txt
    92	
    93	#> Use GENSPEC switch to generate a new specdef file (does not generate output file).
    94	 setenv GENSPEC N
    95	
    96	
    97	# =====================================================================
    98	#> Begin Loop Through Simulation Days to Create ACONC File
    99	# =====================================================================
   100	
   101	#> Set the species definition file for concentration species.
   102	 setenv SPECIES_DEF $SPEC_CONC
   103	 
```
- 日數之迴圈

```python
   104	#> Loop through all days between START_DAY and END_DAY
   105	 set TODAYG = ${START_DATE}
   106	 set TODAYJ = `date -ud "${START_DATE}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   107	 set STOP_DAY = `date -ud "${END_DATE}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   108	 set I = 0
   109	 while ($TODAYJ <= $STOP_DAY )  #>Compare dates in terms of YYYYJJJ
   110	   @ R = 6 # $I / 4 + 5
   111	   echo 'kuang' $I run$R
   112	   if ( $R > 12 ) exit 0
```
- 詳細I/O檔名之定義

```python
   113	  #> Retrieve Calendar day Information
   114	   set YYYY = `date -ud "${TODAYG}" +%Y`
   115	   set YY = `date -ud "${TODAYG}" +%y`
   116	   set MM = `date -ud "${TODAYG}" +%m`
   117	   set DD = `date -ud "${TODAYG}" +%d`
   118	   if ( "${STKCASEE}" != "" ) then
   119	     setenv CTM_APPL ${RUNID}_run${R}_$YYYY$MM${DD}_${GRID_NAME}_${STKCASEE}
   120	  else
   121	     setenv CTM_APPL ${RUNID}_$YYYY$MM${DD}_${GRID_NAME}
   122	  endif
   123	  #> for files that are indexed with Julian day:
   124	   #  set YYYYJJJ = `date -ud "${TODAYG}" +%Y%j` 
   125	
   126	  #> Define name of combine output file to save hourly average concentration.
   127	  #> A new file will be created for each month/year.
   128	   setenv OUTFILE ${POSTDIR}/COMBINE_ACONC_${CTM_APPL}.nc
   129	
   130	  #> Define name of input files needed for combine program.
   131	  #> File [1]: CMAQ conc/aconc file
   132	  #> File [2]: MCIP METCRO3D file
   133	  #> File [3]: CMAQ APMDIAG file
   134	  #> File [4]: MCIP METCRO2D file
   135	 setenv METDIR    ${CMAQ_DATA}/mcip/${APPL}_run${R}/${GRID_NAME}            #> Met Output Directory
   136	   setenv INFILE1 $CCTMOUTDIR/CCTM_ACONC_${CTM_APPL}.nc
   137	   setenv INFILE2 $METDIR/METCRO3D_${APPL}_run${R}.nc
   138	   setenv INFILE3 $CCTMOUTDIR/CCTM_APMDIAG_${CTM_APPL}.nc
   139	   setenv INFILE4 $METDIR/METCRO2D_${APPL}_run${R}.nc
   140	
```
- 程式之執行

```python
   141	  #> Executable call:
   142	 if ( $RUN == $R) then
   143	   ${BINDIR}/${EXEC}
   144	 endif
   145	
   146	  #> Increment both Gregorian and Julian Days
   147	   set TODAYG = `date -ud "${TODAYG}+1days" +%Y-%m-%d` #> Add a day for tomorrow
   148	   set TODAYJ = `date -ud "${TODAYG}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   149	   @ I = $I + 1 
   150	 end #Loop to the next Simulation Day
   151	
   152	
```
- 沉降量計算部分

```python
   153	# =====================================================================
   154	#> Begin Loop Through Simulation Days to Create DEP File
   155	# =====================================================================
   156	
   157	#> Set the species definition file for concentration species.
   158	 setenv SPECIES_DEF $SPEC_DEP
   159	 
   160	#> Loop through all days between START_DAY and END_DAY
   161	 set TODAYG = ${START_DATE}
   162	 set TODAYJ = `date -ud "${START_DATE}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   163	 set STOP_DAY = `date -ud "${END_DATE}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   164	 set I = 0
   165	 while ($TODAYJ <= $STOP_DAY )  #>Compare dates in terms of YYYYJJJ
   166	   @ R = 6 #$I / 4 + 5
   167	   echo 'kuang' $I run$R
   168	   if ( $R > 12 ) exit 0
   169	  #> Retrieve Calendar day Information
   170	   set YYYY = `date -ud "${TODAYG}" +%Y`
   171	   set YY = `date -ud "${TODAYG}" +%y`
   172	   set MM = `date -ud "${TODAYG}" +%m`
   173	   set DD = `date -ud "${TODAYG}" +%d`
```
- 詳細I/O檔名之定義

```python
   174	   if ( "${STKCASEE}" != "" ) then
   175	     setenv CTM_APPL ${RUNID}_run${R}_$YYYY$MM${DD}_${GRID_NAME}_${STKCASEE}
   176	     setenv CTM_APPD ${RUNID}_run${R}_$YYYY${MM}_${GRID_NAME}_${STKCASEE}
   177	  else
   178	     setenv CTM_APPL ${RUNID}_$YYYY$MM$DD
   179	     setenv CTM_APPD ${RUNID}_$YYYY$MM
   180	  endif
   181	  #> for files that are indexed with Julian day:
   182	   #  set YYYYJJJ = `date -ud "${TODAYG}" +%Y%j` 
   183	
   184	  #> Define name of combine output file to save hourly total deposition.
   185	  #> A new file will be created for each month/year.
   186	   setenv OUTFILE ${POSTDIR}/COMBINE_DEP_${CTM_APPD}
   187	  #> Define name of input files needed for combine program.
   188	  #> File [1]: CMAQ DRYDEP file
   189	  #> File [2]: CMAQ WETDEP file
   190	  #> File [3]: MCIP METCRO2D
   191	  #> File [4]: {empty}
   192	   setenv METDIR    ${CMAQ_DATA}/mcip/${APPL}_run${R}/${GRID_NAME}            #> Met Output Directory
   193	   setenv INFILE1 $CCTMOUTDIR/CCTM_DRYDEP_${CTM_APPL}.nc
   194	   setenv INFILE2 $CCTMOUTDIR/CCTM_WETDEP1_${CTM_APPL}.nc
   195	   setenv INFILE3 $METDIR/METCRO2D_${APPL}_run${R}.nc
   196	   setenv INFILE4
   197	
```
- 程式之執行

```python
   198	  #> Executable call:
   199	 if ( $RUN == $R) then
   200	   mpirun -np 10 ${BINDIR}/${EXEC}
   201	 endif
   202	
   203	  #> Increment both Gregorian and Julian Days
   204	   set TODAYG = `date -ud "${TODAYG}+1days" +%Y-%m-%d` #> Add a day for tomorrow
   205	   set TODAYJ = `date -ud "${TODAYG}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
   206	   @ I = $I + 1 
   207	 end #Loop to the next Simulation Day
   208	
   209	 
   210	 exit()
```
## bash版本
- 詳見[公版combine.sh](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#combine-腳本)
  - 當月所有日數都在同一目錄
  - 沒有處理沉降量
  
## Reference
- Aitken Nuclei - an overview \| ScienceDirect Topics (n.d.). Available at [sciencedirect](https://www.sciencedirect.com/topics/earth-and-planetary-sciences/aitken-nuclei) (Accessed 3 January 2022).