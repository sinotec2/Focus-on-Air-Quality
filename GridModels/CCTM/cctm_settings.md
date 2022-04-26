---
layout: default
title: CCTM之設定
parent: CCTM Main Program
grand_parent: CMAQ Model System
nav_order: 2
date: 2022-04-20 20:27:59
last_modified_date: 2022-04-20 20:28:02
---

# CCTM之設定
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

## 前言/背景
### 架構
CCTM的執行過程採用c-shell的環境變數進行設定，因此必須使用批次檔來控制。主要段落包括：
1. 編譯相關設定(視機器而異)
2. 總體設定
    1. 時間、空間及反應機制設定(不建議修改)，執行程式位置設定(視機器而異)
    2. 主要輸出/入檔案目錄位置設定(不建議修改)
    3. 日期時間及mpi控制(不建議修改)
    4. 時間步階、容錯範圍與科學設定(不建議修改)
    5. 診斷報表(不建議修改)
    6. 輸入檔案之目錄(不建議修改)
3. 逐日進行設定
    1. 逐日迴圈之準備及啟動(不建議修改)
    2. 逐日之IC/BC/臭氧/光學/氣象檔案(不建議修改)
    3. 逐日排放相關檔案之設定
    4. 在線排放之設定(未測試)
    5. 程序分析之設定(未測試)
    6. 輸出檔案名稱(不建議修改)
4. 執行有關之環境設定
    1. 控制程式之環境變數設定(不建議修改)
    2. 執行環境資源與路徑設定(視機器而異)
### 範例位置
https://github.com/sinotec2/cmaq_relatives/blob/master/run_cctmMM_RR_DM.csh


## CCTM編譯相關設定
除非測試不同編譯的差異、或移轉到不同電腦平台上，否則這一段應無修改的必要。
設定內容 包括：
1. 編譯程式(範例為gcc)。由於netCDF、IOAPI等都必須同一編譯軟體進行編譯，因此其選項為系統性須配套。
2. CCTM編譯環境(範例為/opt/CMAQ_Project/config_cmaq.csh $compiler $compilerVrsn)
3. 連結程式庫位置(範例為/opt/netcdf/netcdf4_gcc/lib)
4. 偵錯階段可以打開DIAG_LVL，否則設為0，有較少的輸出(範例為setenv CTM_DIAG_LVL 0)
- 範例

```bash
  1 #!/bin/csh -f
  2
  3 # ===================== CCTMv5.3 Run Script ========================= 
  4 # Usage: run.cctm >&! cctm_v53.log &                                
  5 #
  6 # To report problems or request help with this script/program:     
  7 #             http://www.epa.gov/cmaq    (EPA CMAQ Website)
  8 #             http://www.cmascenter.org  (CMAS Website)
  9 # ===================================================================  
 10 # ===================================================================
 11 # ===================================================================
 12 #> Runtime Environment Options
 13 # ===================================================================
 14
 15 echo 'Start Model Run At ' `date`
 16
 17 #> Toggle Diagnostic Mode which will print verbose information to
 18 #> standard output
 19  setenv CTM_DIAG_LVL 0
 20  setenv CMAQ_HOME $cwd
 21  setenv compiler  gcc
 22 #> Choose compiler and set up CMAQ environment with correct
 23 #> libraries using config.cmaq. Options: intel | gcc | pgi
 24 #setenv compiler $argv[1]
 25  if ( ! $?compiler ) then
 26    setenv compiler intel
 27  endif
 28  if ( ! $?compilerVrsn ) then
 29    setenv compilerVrsn Empty
 30  endif
 31
 32 #> Source the config.cmaq file to set the build environment
 33  cd /opt/CMAQ_Project
 34  source ./config_cmaq.csh $compiler $compilerVrsn
 35  setenv LD_LIBRARY_PATH /opt/netcdf/netcdf4_gcc/lib
 36  cd $CMAQ_HOME
```
## 總體設定
### 時間、空間及反應機制設定，執行程式位置設定
CCTM的執行是由粗網格執行後再進行細網格、時間上也是分月、分批次(與wrf相同)進行，此處以引數方式輸入。
反應機制與執行程式除非偵錯或敏感性測試階段、或移轉到不同電腦平台上，否則其位置應無修改的必要。
設定內容包括：
1. 年份(APYR)：由所在目錄名稱讀取
2. 引數(順序及意義如檔名所示run_cctmMM_RR_DM.csh)
    1. 月份(MO)：第1引數，MO=01, 02,...12
    2. 批次(RUN):第2引數，RUN=1, 2, ... 12 (1~4為前月範圍並不重複執行)
    3. 層數(DM):第3引數，DM=d02、d04
        * 層數與巢狀網格名稱具有對照關係。如要新增或修改，須注意${GRID_NAME}配套
        * 層數與ICTYPE/BCTYPE亦有搭配
3. 反應機制：與污染物項目名稱有搭配
4. 執行程式位置與名稱：
    * 程式修改及編譯：詳見另處筆記(CMAQ compilations)
    * 倘若修改，建議配套修改輸出目錄位置，以避免覆蓋過原有結果
- 範例

```bash
 37 set APYR       = `echo $CMAQ_HOME|cut -d'/' -f4|cut -c3-4`
 38 set MO         = $argv[1]
 39 set RUN        = $argv[2]
 40 set DM         = $argv[3]
 41 set APYM       = $APYR$MO
 42 set APPL       = ${APYM}_run${argv[2]}
 43 if ( $DM == 'd02' ) then
 44   setenv GRID_NAME  sChina_27k        # 16-character maximum
 45 # set ICTYPE   = profile
 46   set ICTYPE   = regrid
 47 else if( $DM == 'd04' ) then
 48   setenv GRID_NAME  TWN_3X3           # 16-character maximum
 49   set ICTYPE   = regrid
 50 else
 51   echo "Error input d02/d04"
 52   exit 1
 53 endif
 54
 55 #> Set General Parameters for Configuring the Simulation
 56  set VRSN      = v53               #> Code Version
 57  set PROC      = mpi               #> serial or mpi
 58  set MECH      = cb6r3_ae7_aq      #> Mechanism ID
 59
 60
 61 #> Define RUNID as any combination of parameters above or others. By default,
 62 #> this information will be collected into this one string, $RUNID, for easy
 63 #> referencing in output binaries and log files as well as in other scripts.
 64  setenv RUNID  ${VRSN}_${compilerString}_${APPL}
 65
 66 #> Set the build directory (this is where the CMAQ executable
 67 #> is located by default).
 68
 69  set BLD       = /opt/CMAQ_Project/CCTM/scripts/BLD_CCTM_${VRSN}_${compilerString}ENKF
 70  set EXEC      = CCTM_${VRSN}.exe
```
### 主要輸出/入檔案目錄位置設定
由於輸出/入檔案不小，建議設到足夠大的磁碟機為宜。
傳輸的速度也要注意，
設定內容包括：
1. WRKDIR：工作目錄，家目錄。CTM會暫存在此，監控執行進度。
2. OUTDIR：輸出目錄，會在其下繼續開POST，進行後處理。
3. INPDIR：輸入目錄
4. LOGDIR：CTM檔案之目錄，文字檔，偵錯用。
5. NMLpath：反應機制設定檔目錄。由於檔案不大，可以設在與程式相同路徑。
- 範例

```bash
 71
 72 #> Output Each line of Runscript to Log File
 73  if ( $CTM_DIAG_LVL != 0 ) set echo
 74
 75 #> Set Working, Input, and Output Directories
 76  setenv WORKDIR ${CMAQ_HOME}          #> Working Directory. Where the runscript is.
 77  setenv OUTDIR  /nas1/cmaqruns/2016base/data/output_CCTM_${RUNID}  #> Output Directory
 78  setenv INPDIR  ${CMAQ_HOME}/data  #Input Directory
 79  setenv LOGDIR  ${OUTDIR}/LOGS     #> Log Directory Location
 80  setenv NMLpath ${BLD}             #> Location of Namelists. Common places are:
 81                                    #>   ${WORKDIR} | ${CCTM_SRC}/MECHS/${MECH} | ${BLD}
 82
 83  echo ""
 84  echo "Working Directory is $WORKDIR"
 85  echo "Build Directory is $BLD"
 86  echo "Output Directory is $OUTDIR"
 87  echo "Log Directory is $LOGDIR"
 88  echo "Executable Name is $EXEC"
```
### 日期時間及mpi控制
除非測試不同編譯的差異、或移轉到不同電腦平台上，否則這一段應無修改的必要。
設定內容 包括：
1. 如果$RUN是5，表示此模擬批次包括當月的第一天，NEW_START為真，必須特別準備初始值檔案，其餘批次則連結到前一批次執行結果即可
2. BEGD：和其他前處理一樣，此值為前一月的15日，為各批次的起始日期，由該日期計算各批次的起迄日期。批次的時間長度為4天
3. STIME：起始時間，須涵蓋在mcip氣象檔案、BC範圍，並與ICON檔案完全一樣。
4. NSTEPS：執行CCTM的時間範圍。由於CCTM5.31.exe並不會跳日(詳見CMAQ compilations )，必須一天天執行，此值只能設為240000
5. 序列或平行運作之選擇：
    * 測試除錯階段可能選擇序列運轉，正常作業時必須為平行運作，選項有serial 及mpi。
    * CPU分配以均勻為原則，以充分運用計算資源。
    * 如不能除盡網格數，程式仍然能夠繼續進行(nodes=20、supermicro=100、mac=6)。
    * CPU總數如超過電腦實際核心數：
        * 仍可執行、但不穩定、故不建議
        * 電腦計算速度除CPU設定之外、硬碟IO亦會影響
6. CLOBBER_DATA：將會刪除並覆蓋既有的成果。
- 範例

```bash
 92 # =====================================================================
 93
 94 #> Set Start and End Days for looping
 95  if ( $RUN == 5 ) then
 96    setenv NEW_START TRUE        #> Set to FALSE for model restart
 97  else
 98    setenv NEW_START FALSE       #> Set to FALSE for model restart
 99  endif
100 set BEGD = `date -ud "20${APYR}-${MO}-15 - 1months" +%Y-%m-%d`
101   @ A = $RUN - 1; @ DD = $A * 4 ; @ ED = $A * 4 + 3
102 setenv EMLAYS_MX 13
103 set START_DATE = `date -ud "$BEGD +${DD}days" +%Y-%m-%d` #> beginning date (July 1, 2016)
104 set END_DATE = `date -ud "$BEGD +${ED}days" +%Y-%m-%d` #> ending date    (July 14, 2016)
105  set STD_YMD = `date -ud "${START_DATE}" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
106
107 #> Set Timestepping Parameters
108  set STTIME     =       0           #> beginning GMT time (HHMMSS)
109  set NSTEPS     =  240000           #> time duration (HHMMSS) for this run
110  set TSTEP      =   10000           #> output time step interval (HHMMSS)
111
112 #> Horizontal domain decomposition
113 if ( $PROC == serial ) then
114    setenv NPCOL_NPROW "1 1"; set NPROCS   = 1 # single processor setting
115 else
116    @ NPCOL  =  8; @ NPROW = 12
117    @ NPROCS = $NPCOL * $NPROW
118    setenv NPCOL_NPROW "$NPCOL $NPROW";
119 endif
120
121 #> Define Execution ID: e.g. [CMAQ-Version-Info]_[User]_[Date]_[Time]
122 setenv EXECUTION_ID "CMAQ_CCTM${VRSN}_`id -u -n`_`date -u +%Y%m%d_%H%M%S_%N`"    #> Inform IO/API of the Execution ID
123 echo ""
124 echo "---CMAQ EXECUTION ID: $EXECUTION_ID ---"
125
126 #> Keep or Delete Existing Output Files
127 set CLOBBER_DATA = TRUE
128
129 #> Logfile Options
130 #> Master Log File Name; uncomment to write standard output to a log, otherwise write to screen
131 #setenv LOGFILE $CMAQ_HOME/$RUNID.log
132 if (! -e $LOGDIR ) then
133   mkdir -p $LOGDIR
134 endif
135 setenv PRINT_PROC_TIME Y           #> Print timing for all science subprocesses to Logfile
```

### 水平與垂直網格設定
除非網格座標系統改變（增減、平移），否則這一段應無修改的必要。
設定內容 包括：
1. GRIDDESC必須和mcip一致、配套。排放量、ICBC、土地使用、土壤等都須符合統一的座標系統。
    1. NZ（無作用），模式垂直網格數內設與WRF、MCIP一致。
    2. NCELLS（僅檢視用）
2. 輸出檔案的成分與垂直網格數，如不檢討高空煙流的擴散情況，可以不必輸出高空結果以節省空間。
    1. CONC（每步階）
    2. ACONC（逐時平均）成分與層數
        * 成分須以double quote括住，或為“ALL”(如需計算所有粒狀物，建議設為ALL)
        * 起訖層數如不指定，則為所有層數。
- 範例

```bash
137 setenv STDOUT T                    #> Override I/O-API trying to write information to both the processor
138                                    #>   logs and STDOUT [ options: T | F ]
139
140 setenv GRIDDESC $INPDIR/mcip/${APPL}/${GRID_NAME}/GRIDDESC    #> grid description file
141
142 #> Retrieve the number of columns, rows, and layers in this simulation
143 set NZ = 35
144 set NX = `grep -A 1 ${GRID_NAME} ${GRIDDESC} | tail -1 | sed 's/  */ /g' | cut -d' ' -f6`
145 set NY = `grep -A 1 ${GRID_NAME} ${GRIDDESC} | tail -1 | sed 's/  */ /g' | cut -d' ' -f7`
146 set NCELLS = `echo "${NX} * ${NY} * ${NZ}" | bc -l`
147
148 #> Output Species and Layer Options
149    #> CONC file species; comment or set to "ALL" to write all species to CONC
150    setenv CONC_SPCS "O3 NO ANO3I ANO3J NO2 FORM ISOP NH3 ANH4I ANH4J ASO4I ASO4J"
151    setenv CONC_BLEV_ELEV #" 1 1" #> CONC file layer range; comment to write all layers to CONC
152
153    #> ACONC file species; comment or set to "ALL" to write all species to ACONC
154    #setenv AVG_CONC_SPCS "O3 NO CO NO2 ASO4I ASO4J NH3"
155    setenv AVG_CONC_SPCS "ALL"
156    setenv ACONC_BLEV_ELEV #" 1 1" #> ACONC file layer range; comment to write all layers to ACONC
157    setenv AVG_FILE_ENDTIME N     #> override default beginning ACONC timestamp [ default: N ]
158
```
### 時間步階、容錯範圍與科學設定
為使模式有比較性，這段盡量使用內設值，應無修改的必要。
設定內容詳見[CCTM之科學設定](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/CCTM/science/)，包括：
1. 同步時間步階：縮短時間步階可提高正確性。加長步階秒數可有效使用CPU。
2. CTM_OCEAN_CHEM（海洋飛沫在風大時會增加PM10濃度、尚未測試）
3. CTM_WB_DUST（風蝕揚塵、可能會與TEDS重複，未測試）
4. CTM_BIDI_FERT_NH3：如取消程式無法進行
- 範例

```bash
159 #> Synchronization Time Step and Tolerance Options
160 setenv CTM_MAXSYNC 300       #> max sync time step (sec) [ default: 720 ]
161 setenv CTM_MINSYNC  60       #> min sync time step (sec) [ default: 60 ]
162 setenv SIGMA_SYNC_TOP 0.7    #> top sigma level thru which sync step determined [ default: 0.7 ]
163 #setenv ADV_HDIV_LIM 0.95    #> maximum horiz. div. limit for adv step adjust [ default: 0.9 ]
164 setenv CTM_ADV_CFL 0.95      #> max CFL [ default: 0.75]
165 #setenv RB_ATOL 1.0E-09      #> global ROS3 solver absolute tolerance [ default: 1.0E-07 ]
166
167 #> Science Options
168 setenv CTM_OCEAN_CHEM N      #> Flag for ocean halgoen chemistry and sea spray aerosol emissions [ default: Y ]
169 setenv CTM_WB_DUST N         #> use inline windblown dust emissions [ default: Y ]
170 setenv CTM_WBDUST_BELD BELD3 #> landuse database for identifying dust source regions
171                              #>    [ default: UNKNOWN ]; ignore if CTM_WB_DUST = N
172 setenv CTM_LTNG_NO N         #> turn on lightning NOx [ default: N ]
173 setenv CTM_WVEL Y            #> save derived vertical velocity component to conc
174                              #>    file [ default: N ]
175 setenv KZMIN Y               #> use Min Kz option in edyintb [ default: Y ],
176                              #>    otherwise revert to Kz0UT
177 setenv CTM_MOSAIC N          #> landuse specific deposition velocities [ default: N ]
178 setenv CTM_FST N             #> mosaic method to get land-use specific stomatal flux
179                              #>    [ default: N ]
180 setenv PX_VERSION Y          #> WRF PX LSM
181 setenv CLM_VERSION N         #> WRF CLM LSM
182 setenv NOAH_VERSION N        #> WRF NOAH LSM
183 setenv CTM_ABFLUX Y          #> ammonia bi-directional flux for in-line deposition
184                              #>    velocities [ default: N ]
185 setenv CTM_BIDI_FERT_NH3 T   #> subtract fertilizer NH3 from emissions because it will be handled
186                              #>    by the BiDi calculation [ default: Y ]
187 setenv CTM_HGBIDI N          #> mercury bi-directional flux for in-line deposition
188                              #>    velocities [ default: N ]
189 setenv CTM_SFC_HONO Y        #> surface HONO interaction [ default: Y ]
190 setenv CTM_GRAV_SETL Y       #> vdiff aerosol gravitational sedimentation [ default: Y ]
191 setenv CTM_BIOGEMIS N        #> calculate in-line biogenic emissions [ default: N ]
192
193 #> Vertical Extraction Options
194 setenv VERTEXT N
195 setenv VERTEXT_COORD_PATH ${WORKDIR}/lonlat.csv
```
### 診斷報表
為使模式有比較性，這段盡量使用內設值，應無修改的必要。
設定內容
包括：
1. IOAPI_OFFSET_64 ：support大檔案
2. APMDIAG_BLEV_ELEV： 診斷各層之主要點源排放量
- 範例

```bash
197 #> I/O Controls
198 setenv IOAPI_LOG_WRITE F     #> turn on excess WRITE3 logging [ options: T | F ]
199 setenv FL_ERR_STOP N         #> stop on inconsistent input files
200 setenv PROMPTFLAG F          #> turn on I/O-API PROMPT*FILE interactive mode [ options: T | F ]
201 setenv IOAPI_OFFSET_64 YES   #> support large timestep records (>2GB/timestep record) [ options: YES | NO ]
202 setenv IOAPI_CHECK_HEADERS N #> check file headers [ options: Y | N ]
203 setenv CTM_EMISCHK N         #> Abort CMAQ if missing surrogates from emissions Input files
204 setenv EMISDIAG F            #> Print Emission Rates at the output time step after they have been
205                              #>   scaled and modified by the user Rules [options: F | T or 2D | 3D | 2DSUM ]
206                              #>   Individual streams can be modified using the variables:
207                              #>       GR_EMIS_DIAG_## | STK_EMIS_DIAG_## | BIOG_EMIS_DIAG
208                              #>       MG_EMIS_DIAG    | LTNG_EMIS_DIAG   | DUST_EMIS_DIAG
209                              #>       SEASPRAY_EMIS_DIAG
210                              #>   Note that these diagnostics are different than other emissions diagnostic
211                              #>   output because they occur after scaling.
212
213 #> Diagnostic Output Flags
214 setenv CTM_CKSUM Y           #> checksum report [ default: Y ]
215 setenv CLD_DIAG Y            #> cloud diagnostic file [ default: N ]
216
217 setenv CTM_PHOTDIAG Y        #> photolysis diagnostic file [ default: N ]
218 setenv NLAYS_PHOTDIAG #1"    #> Number of layers for PHOTDIAG2 and PHOTDIAG3 from
219                              #>     Layer 1 to NLAYS_PHOTDIAG  [ default: all layers ]
220 #setenv NWAVE_PHOTDIAG "294 303 310 316 333 381 607"  #> Wavelengths written for variables
221                                                       #>   in PHOTDIAG2 and PHOTDIAG3
222                                                       #>   [ default: all wavelengths ]
223
224 setenv CTM_PMDIAG N          #> Instantaneous Aerosol Diagnostic File [ default: Y ]
225 setenv CTM_APMDIAG Y         #> Hourly-Average Aerosol Diagnostic File [ default: Y ]
226 setenv APMDIAG_BLEV_ELEV #"1 1"  #> layer range for average pmdiag = NLAYS
227
228 setenv CTM_SSEMDIAG N        #> sea-spray emissions diagnostic file [ default: N ]
229 setenv CTM_DUSTEM_DIAG N     #> windblown dust emissions diagnostic file [ default: N ];
230                              #>     Ignore if CTM_WB_DUST = N
231 setenv CTM_DEPV_FILE N       #> deposition velocities diagnostic file [ default: N ]
232 setenv VDIFF_DIAG_FILE N     #> vdiff & possibly aero grav. sedimentation diagnostic file [ default: N ]
233 setenv LTNGDIAG N            #> lightning diagnostic file [ default: N ]
234 setenv B3GTS_DIAG N          #> BEIS mass emissions diagnostic file [ default:
```
### 輸入檔案之目錄
前述為主要檔案的目錄(上層)，也包括輸出檔案，此處定義輸入檔部分，直到檔案名稱之前。
設定內容
包括：
1. 如果不需要輸入，可以在等號後保持空白
2. OMIpath ：採內設值
- 範例

```bash
236 # =====================================================================
237 #> Input Directories and Filenames
238 # =====================================================================
239
240 set ICpath    = $INPDIR/icon                        #> initial conditions input directory
241 set BCpath    = $INPDIR/bcon                        #> boundary conditions input directory
242 set EMISpath  = $INPDIR/emis                        #> gridded emissions input directory
243 set EMISpath2 =                                     #> gridded surface residential wood combustion emissions directory
244 set IN_PTpath = $INPDIR/ptse                        #> point source emissions input directory
245 set IN_LTpath =                                     #> lightning NOx input directory
246 set METpath   = $INPDIR/mcip/$APPL/$GRID_NAME       #> meteorology input directory
247 #set JVALpath  = $INPDIR/jproc                      #> offline photolysis rate table directory
248 set OMIpath   = $BLD                                #> ozone column data for the photolysis model
249 set LUpath    = $INPDIR/land                        #> BELD landuse data for windblown dust model
250 set SZpath    = $INPDIR/land                        #> surf zone file for in-line seaspray emissions
```
## 逐日之設定
### 逐日迴圈之準備及啟動
- CCTM.exe為每24小時模擬的方式來進行，在同一批次內的4天中，依序進行4次的CCTM.exe。
- 批次檔內以當日(TODAY)及昨日(YESTERDAY)2日輪轉方式來簡化換日的檔名問題。
- 設定內容包括：
  1. YYYYMMDD、YYYYMM、YYMMDD、YYYYJJJ等多種不同的日期表示方式，以因應檔名的方便性
  2. STKCASEE為排放清冊標記，如有排放量版本之差異，應在此設定。此標記將會出現在輸出檔名之尾端。
- 範例

```bash
252 # =====================================================================
253 #> Begin Loop Through Simulation Days
254 # =====================================================================
255 set rtarray = ""
256
257 set TODAYG = ${START_DATE}
258 set TODAYJ = `date -ud "${START_DATE}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
259 set START_DAY = ${TODAYJ}
260 set STOP_DAY = `date -ud "${END_DATE}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
261 set NDAYS = 0
262 set STKCASEE = 10   # 12US1_cmaq_cb6_2016ff_16j  # Stack Emission Version Label
263
264 while ($TODAYJ <= $STOP_DAY )  #>Compare dates in terms of YYYYJJJ
265
266   set NDAYS = `echo "${NDAYS} + 1" | bc -l`
267
268   #> Retrieve Calendar day Information
269   set YYYYMMDD = `date -ud "${TODAYG}" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYMMDD
270   set YYYYMM = `date -ud "${TODAYG}" +%Y%m`     #> Convert YYYY-MM-DD to YYYYMM
271   set YYMMDD = `date -ud "${TODAYG}" +%y%m%d`   #> Convert YYYY-MM-DD to YYMMDD
272   set YYYYJJJ = $TODAYJ
273
274   #> Calculate Yesterday's Date
275   set YESTERDAY = `date -ud "${TODAYG}-1days" +%Y%m%d` #> Convert YYYY-MM-DD to YYYYJJJ
276
277 # =====================================================================
278 #> Set Output String and Propagate Model Configuration Documentation
279 # =====================================================================
280   echo ""
281   echo "Set up input and output files for Day ${TODAYG}."
282
283   #> set output file name extensions
284   setenv CTM_APPL ${RUNID}_${YYYYMMDD}_${GRID_NAME}_${STKCASEE}
285
286   #> Copy Model Configuration To Output Folder
287   if ( ! -d "$OUTDIR" ) mkdir -p $OUTDIR
288   cp $BLD/CCTM_${VRSN}.cfg $OUTDIR/CCTM_${CTM_APPL}.cfg
289
```
### 逐日之IC/BC/臭氧/光學/氣象檔案
執行前逐一準備好檔案。目錄、檔名「不建議」修改，以避免錯誤。
設定內容 包括：
1. 初始檔案：RUN5會讀ICON檔案(須事先處理，見CMAQ初始及邊界條件設定 )，其他批次則會讀前一天的CCTM_CGRID檔案，或前一批次最後天的CCTM_CGRID檔案
2. 邊界檔案：BCON檔案，見CMAQ初始及邊界條件設定
3. 氣象檔案：並不逐日變化，但mcip與wrfout有1小時之差異，須以add_firstHr補滿第1小時。(見筆記全球空品模擬結果作為CMAQ之初始及邊界條件 附錄)
- 範例

```bash
290 # =====================================================================
291 #> Input Files (Some are Day-Dependent)
292 # =====================================================================
293
294   #> Initial conditions
295   if ($NEW_START == true || $NEW_START == TRUE ) then
296      setenv ICFILE ICON_${VRSN}_${APPL}_${GRID_NAME}_${ICTYPE}_${YYYYMMDD}
297      if ( $MO != '01' ) then
298        set PYM = `date -ud "20${APYM}01 -1 month" +%y%m`
299        set PRUNID = ${VRSN}_${compilerString}_${PYM}_run12
300        set POUTDIR = ${OUTDIR}/../output_CCTM_${PRUNID}
301        ln -sf ${POUTDIR}/CCTM_CGRID_${PRUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc \
302                 $ICpath/$ICFILE
303      endif
304      setenv INIT_MEDC_1 notused
305      setenv INITIAL_RUN Y #related to restart soil information file
306   else
307      set ICpath = $OUTDIR
308      setenv ICFILE CCTM_CGRID_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
309      setenv INIT_MEDC_1 $ICpath/CCTM_MEDIA_CONC_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
310      setenv INITIAL_RUN N
311      if ( $TODAYJ == $START_DAY ) then
312        @ PRUN = $RUN - 1
313        set PRUNID = ${VRSN}_${compilerString}_${APYM}_run${PRUN}
314        set POUTDIR = ${OUTDIR}/../output_CCTM_${PRUNID}
315        ln -sf ${POUTDIR}/CCTM_CGRID_${PRUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc \
316                 $OUTDIR/CCTM_CGRID_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
317        ln -sf ${POUTDIR}/CCTM_MEDIA_CONC_${PRUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc \
318                 $OUTDIR/CCTM_MEDIA_CONC_${RUNID}_${YESTERDAY}_${GRID_NAME}_${STKCASEE}.nc
319      endif
320   endif
321
322   #> Boundary conditions
323   set BCFILE = BCON_${VRSN}_${APPL}_${ICTYPE}_${STD_YMD}_${GRID_NAME}
324
325   #> Off-line photolysis rates
326   #set JVALfile  = JTABLE_${YYYYJJJ}
327
328   #> Ozone column data
329   set OMIfile   = OMI_1979_to_2017.dat
330
331   #> Optics file
332   set OPTfile = PHOT_OPTICS.dat
333
334   #> MCIP meteorology files
335   setenv GRID_BDY_2D $METpath/GRIDBDY2D_${APPL}.nc  # GRID files are static, not day-specific
336   setenv GRID_CRO_2D $METpath/GRIDCRO2D_${APPL}.nc
337   setenv GRID_CRO_3D $METpath/GRIDCRO3D_${APPL}.nc
338   setenv GRID_DOT_2D $METpath/GRIDDOT2D_${APPL}.nc
339   setenv MET_CRO_2D $METpath/METCRO2D_${APPL}.nc
340   setenv MET_CRO_3D $METpath/METCRO3D_${APPL}.nc
341   setenv MET_DOT_3D $METpath/METDOT3D_${APPL}.nc
342   setenv MET_BDY_3D $METpath/METBDY3D_${APPL}.nc
343   setenv LUFRAC_CRO $METpath/LUFRAC_CRO_${APPL}.nc
344
```
### 逐日排放相關檔案之設定
為模式修改的重點位置。應注意版本的差異
設定內容 包括：
1. 地面及高空排放源都可以分群組提供，以解析各群組的貢獻，進一步解析污染源敏感性。如不提供，只須在等號右邊保持空白即可。
2. 面源須每網格提供，點源檔案分為常數部分(const)及變數部分(timvar)，且可以每日不同煙囪個數。建議單月仍然保持相同煙囪個數，以降低複雜度。
3. OBS系列變數：
    1. 為測站測值，進行濃度調整之用。其檔案格式與點源相同。如不執行修正，可免提供。
    2. 非官方程式碼，使用請自行注意。
4. 雖然逐日提供排放量檔案可以詳細在CTM檔案中進行檢查，但是否一定須逐日提供，是否可以像mcip檔案批次提供，此點還有待實證。
EMISSCTRL_NML之設定
* 此檔案會對排放源檔案做對照、加權
* 不必再重做SMOKE，直接修改此檔，即可得特定污染源的到增、減量效果
- 範例

```bash
345   #> Emissions Control File
346   setenv EMISSCTRL_NML    ${BLD}/EmissCtrl_${MECH}.nml
347
348   #> Spatial Masks For Emissions Scaling
349   setenv CMAQ_MASKS #  $SZpath/12US1_surf_bench.nc #> horizontal grid-dependent surf zone file
350
351   #> Gridded Emissions Files
352   setenv N_EMIS_GR 1
353   set EMISfile  = area_${GRID_NAME}.${YYYYMMDD}.nc
354   setenv GR_EMIS_001 ${EMISpath}/${APYM}/${EMISfile}
355   setenv GR_EMIS_LAB_001 GRIDDED_EMIS
356
357   set EMISfile  =
358   setenv GR_EMIS_002 ${EMISpath2}/${EMISfile}
359   setenv GR_EMIS_LAB_002 GRIDDED_RWC
360
361   #> In-line point emissions configuration
362   setenv N_EMIS_PT 1          #> Number of elevated source groups
363   setenv N_OBSS_PT 1          #> Number of elevated source groups
364   setenv STN_GRPS_001 $CMAQ_DATA/sites/${APYM}/const.nc
365   setenv STN_OBSS_001 $CMAQ_DATA/sites/${APYM}/EPA57.${YYYYMMDD}.timvar.nc_12
366   setenv STN_OBSS_LAB_001 TWN_EPA_57
367   setenv STN_OBSS_DIAG_001
368
369   set STKCASEG = teds # 12US1_2016ff_16j           # Stack Group Version Label
370 #  set STKCASEE = 10   # 12US1_cmaq_cb6_2016ff_16j  # Stack Emission Version Label
371
372   # Time-Independent Stack Parameters for Inline Point Sources
373   setenv STK_GRPS_001 $IN_PTpath/${STKCASEG}${STKCASEE}.${APYM}.const.nc
374   setenv LAYP_STTIME  $STTIME
375   setenv LAYP_NSTEPS  $NSTEPS #umber of time steps for calculating elevated-point-source emissions.
376
377   # Emission Rates for Inline Point Sources
378   setenv STK_EMIS_001 $IN_PTpath/${APYM}/${STKCASEG}${STKCASEE}.${YYYYMMDD}.timvar.nc_12
379   setenv LAYP_STDATE  $YYYYJJJ
380
381   # Label Each Emissions Stream
382   setenv STK_EMIS_LAB_001 POINT_NONEGU
383   setenv STK_EMIS_LAB_002 # POINT_EGU
384   setenv STK_EMIS_LAB_003 # POINT_OTHER
385   setenv STK_EMIS_LAB_004 # POINT_AGFIRES
386   setenv STK_EMIS_LAB_005 # POINT_FIRES
387   setenv STK_EMIS_LAB_006 # POINT_OTHFIRES
387   setenv STK_EMIS_LAB_006 # POINT_OTHFIRES
388   setenv STK_EMIS_LAB_007 # POINT_OILGAS
389   setenv STK_EMIS_LAB_008 # POINT_CMV
390
391   # Stack emissions diagnostic files
392   setenv STK_EMIS_DIAG_001 # 2DSUM
393   #setenv STK_EMIS_DIAG_002 2DSUM
394   #setenv STK_EMIS_DIAG_003 2DSUM
395   #setenv STK_EMIS_DIAG_004 2DSUM
396   #setenv STK_EMIS_DIAG_005 2DSUM
397
398
```
### 在線排放之設定
- 呼應前述[科學設定](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/CCTM/science/)，此處提供每日數據。
- 在線排放會逐時讀取氣象數據(雲雨、風速、氣溫等)來計算當時的排放量，此部分尚未測試。
- 設定內容 包括：
1. 雷電NOx
2. 生物源
3. 風吹沙
4. 海洋飛沫
5. 雙向氨氣吸收及排放(似一定要啟動)
- 範例

```bash
399   #> Lightning NOx configuration
400   if ( $CTM_LTNG_NO == 'Y' ) then
401      setenv LTNGNO "InLine"    #> set LTNGNO to "Inline" to activate in-line calculation
402
403   #> In-line lightning NOx options
404      setenv USE_NLDN  N        #> use hourly NLDN strike file [ default: Y ]
405      if ( $USE_NLDN == Y ) then
406         setenv NLDN_STRIKES ${IN_LTpath}/NLDN.12US1.${YYYYMMDD}_bench.nc
407      endif
408      setenv LTNGPARMS_FILE ${IN_LTpath}/LTNG_AllParms_12US1_bench.nc #> lightning parameter file
409   endif
410
411   #> In-line biogenic emissions configuration
412   setenv BIOSW_YN   N
413   if ( $CTM_BIOGEMIS == 'Y' ) then
414      set IN_BEISpath = ${INPDIR}/land
415      setenv GSPRO      $BLD/gspro_biogenics.txt
416 #     setenv B3GRD      $IN_BEISpath/b3grd_bench.nc
417      setenv B3GRD      $IN_BEISpath/b3gts_l.20190920-28.1.sChina_27k.teds10_16.ncf
418      setenv BIOSW_YN   Y     #> use frost date switch [ default: Y ]
419      setenv BIOSEASON  $IN_BEISpath/bioseason.cmaq.201909_sChina.ncf
420                              #> ignore season switch file if BIOSW_YN = N
421      setenv SUMMER_YN  Y     #> Use summer normalized emissions? [ default: Y ]
422      setenv PX_VERSION Y     #> MCIP is PX version? [ default: N ]
423      setenv SOILINP    $OUTDIR/CCTM_SOILOUT_${RUNID}_${YESTERDAY}.nc
424                              #> Biogenic NO soil input file; ignore if INITIAL_RUN = Y
425   endif
426
427   #> Windblown dust emissions configuration
428   if ( $CTM_WB_DUST == 'Y' ) then
429      # Input variables for BELD3 Landuse option
430      setenv DUST_LU_1 $LUpath/beld3_12US1_459X299_output_a_bench.nc
431      setenv DUST_LU_2 $LUpath/beld4_12US1_459X299_output_tot_bench.nc
432   endif
433
434   #> In-line sea spray emissions configuration
435   setenv OCEAN_1 $SZpath/12US1_surf_bench.nc #> horizontal grid-dependent surf zone file
436
437   #> Bidirectional ammonia configuration
438   if ( $CTM_ABFLUX == 'Y' ) then
439      setenv E2C_SOIL ${LUpath}/${APYM}/2016_${GRID_NAME}_soil_bench${APYM}.nc
440      setenv E2C_CHEM ${LUpath}/${APYM}/2016_${GRID_NAME}_time${YYYYMMDD}_bench.nc
441      setenv E2C_CHEM_YEST ${LUpath}/${APYM}/2016_${GRID_NAME}_time${YESTERDAY}_bench.nc
442      setenv E2C_LU ${LUpath}/beld4.${GRID_NAME}.ncf
443   endif
444
```
### 程序分析之設定
程序分析是空氣品質管理很重要的模擬工作，包括模式程序分析、來源分配解析、以及硫份追蹤3個部分，目前都還未開啟。
設定內容 包括：
1. CTM_PROCAN 程序分析
2. CTM_ISAM [來源分配解析](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ISAM/run_isamMM_RR_DM/)
3. STM_SO4TRACK硫份追蹤
- 範例

```bash
445 #> Inline Process Analysis
446   setenv CTM_PROCAN N        #> use process analysis [ default: N]
447   if ( $?CTM_PROCAN ) then   # $CTM_PROCAN is defined
448      if ( $CTM_PROCAN == 'Y' || $CTM_PROCAN == 'T' ) then
449 #> process analysis global column, row and layer ranges
450 #       setenv PA_BCOL_ECOL "10 90"  # default: all columns
451 #       setenv PA_BROW_EROW "10 80"  # default: all rows
452 #       setenv PA_BLEV_ELEV "1  4"   # default: all levels
453         setenv PACM_INFILE ${NMLpath}/pa_${MECH}.ctl
454         setenv PACM_REPORT $OUTDIR/"PA_REPORT".${YYYYMMDD}
455      endif
456   endif
457
458 #> Integrated Source Apportionment Method (ISAM) Options
459  setenv CTM_ISAM N
460  if ( $?CTM_ISAM ) then
461     if ( $CTM_ISAM == 'Y' || $CTM_ISAM == 'T' ) then
462        setenv SA_IOLIST ${WORKDIR}/isam_control.txt
463        setenv ISAM_BLEV_ELEV " 1 1"
464        setenv AISAM_BLEV_ELEV " 1 1"
465
466        #> Set Up ISAM Initial Condition Flags
467        if ($NEW_START == true || $NEW_START == TRUE ) then
468           setenv ISAM_NEW_START Y
469           setenv ISAM_PREVDAY
470        else
471           setenv ISAM_NEW_START N
472           setenv ISAM_PREVDAY "$OUTDIR/CCTM_SA_CGRID_${RUNID}_${YESTERDAY}.nc"
473        endif
474
475        #> Set Up ISAM Output Filenames
476        setenv SA_ACONC_1      "$OUTDIR/CCTM_SA_ACONC_${CTM_APPL}.nc -v"
477        setenv SA_CONC_1       "$OUTDIR/CCTM_SA_CONC_${CTM_APPL}.nc -v"
478        setenv SA_DD_1         "$OUTDIR/CCTM_SA_DRYDEP_${CTM_APPL}.nc -v"
479        setenv SA_WD_1         "$OUTDIR/CCTM_SA_WETDEP_${CTM_APPL}.nc -v"
480        setenv SA_CGRID_1      "$OUTDIR/CCTM_SA_CGRID_${CTM_APPL}.nc -v"
481
482        #> Set optional ISAM regions files
483 #      setenv ISAM_REGIONS /work/MOD3EVAL/nsu/isam_v53/CCTM/scripts/input/RGN_ISAM.nc
484
485     endif
486  endif
487
488
489 #> Sulfur Tracking Model (STM)
490  setenv STM_SO4TRACK N        #> sulfur tracking [ default: N ]
491  if ( $?STM_SO4TRACK ) then
492     if ( $STM_SO4TRACK == 'Y' || $STM_SO4TRACK == 'T' ) then
493
494       #> option to normalize sulfate tracers [ default: Y ]
495       setenv STM_ADJSO4 Y
496
497     endif
498  endif
499
```

### 輸出檔案名稱、層數
* 檔名因與後處理有關，「不建議」任何修改
* 高空層數
    * 如用做下一網格子系統的邊界值，「必須」有3D的輸出
    * 如果沒有下一網格子系統(IC/BC會需要完整層數)，可以只輸出第一層，以減省磁碟機空間。
        * 無設定（整句加註）：將會輸出所有層數
        * 1 1：只輸出第1層、地面層
    * 影響所及之設定

|Variable|Setting|default|Line#|
|-|:-:|-|:-:|
|CONC_BLEV_ELEV|" 1 1"|all layers|151|
|ACONC_BLEV_ELEV|" 1 1"|all layers|156|
|APMDIAG_BLEV_ELEV|(according to ACONC)|NLAYS|226|
|PA_BLEV_ELEV|"1  4"|all levels|452|
|ISAM_BLEV_ELEV|" 1 1"|all levels|463|
|AISAM_BLEV_ELEV|" 1 1"|all levels|464|


- 範例

```bash
500 # =====================================================================
501 #> Output Files
502 # =====================================================================
503
504   #> set output file names
505   setenv S_CGRID         "$OUTDIR/CCTM_CGRID_${CTM_APPL}.nc"         #> 3D Inst. Concentrations
506   setenv CTM_CONC_1      "$OUTDIR/CCTM_CONC_${CTM_APPL}.nc -v"       #> On-Hour Concentrations
507   setenv A_CONC_1        "$OUTDIR/CCTM_ACONC_${CTM_APPL}.nc -v"      #> Hourly Avg. Concentrations
508   setenv MEDIA_CONC      "$OUTDIR/CCTM_MEDIA_CONC_${CTM_APPL}.nc -v" #> NH3 Conc. in Media
509   setenv CTM_DRY_DEP_1   "$OUTDIR/CCTM_DRYDEP_${CTM_APPL}.nc -v"     #> Hourly Dry Deposition
510   setenv CTM_DEPV_DIAG   "$OUTDIR/CCTM_DEPV_${CTM_APPL}.nc -v"       #> Dry Deposition Velocities
511   setenv B3GTS_S         "$OUTDIR/CCTM_B3GTS_S_${CTM_APPL}.nc -v"    #> Biogenic Emissions
512   setenv SOILOUT         "$OUTDIR/CCTM_SOILOUT_${CTM_APPL}.nc"       #> Soil Emissions
513   setenv CTM_WET_DEP_1   "$OUTDIR/CCTM_WETDEP1_${CTM_APPL}.nc -v"    #> Wet Dep From All Clouds
514   setenv CTM_WET_DEP_2   "$OUTDIR/CCTM_WETDEP2_${CTM_APPL}.nc -v"    #> Wet Dep From SubGrid Clouds
515   setenv CTM_PMDIAG_1    "$OUTDIR/CCTM_PMDIAG_${CTM_APPL}.nc -v"     #> On-Hour Particle Diagnostics
516   setenv CTM_APMDIAG_1   "$OUTDIR/CCTM_APMDIAG_${CTM_APPL}.nc -v"    #> Hourly Avg. Particle Diagnostics
517   setenv CTM_RJ_1        "$OUTDIR/CCTM_PHOTDIAG1_${CTM_APPL}.nc -v"  #> 2D Surface Summary from Inline Photolysis
518   setenv CTM_RJ_2        "$OUTDIR/CCTM_PHOTDIAG2_${CTM_APPL}.nc -v"  #> 3D Photolysis Rates
519   setenv CTM_RJ_3        "$OUTDIR/CCTM_PHOTDIAG3_${CTM_APPL}.nc -v"  #> 3D Optical and Radiative Results from Photolysis
520   setenv CTM_SSEMIS_1    "$OUTDIR/CCTM_SSEMIS_${CTM_APPL}.nc -v"     #> Sea Spray Emissions
521   setenv CTM_DUST_EMIS_1 "$OUTDIR/CCTM_DUSTEMIS_${CTM_APPL}.nc -v"   #> Dust Emissions
522   setenv CTM_IPR_1       "$OUTDIR/CCTM_PA_1_${CTM_APPL}.nc -v"       #> Process Analysis
523   setenv CTM_IPR_2       "$OUTDIR/CCTM_PA_2_${CTM_APPL}.nc -v"       #> Process Analysis
524   setenv CTM_IPR_3       "$OUTDIR/CCTM_PA_3_${CTM_APPL}.nc -v"       #> Process Analysis
525   setenv CTM_IRR_1       "$OUTDIR/CCTM_IRR_1_${CTM_APPL}.nc -v"      #> Chem Process Analysis
526   setenv CTM_IRR_2       "$OUTDIR/CCTM_IRR_2_${CTM_APPL}.nc -v"      #> Chem Process Analysis
527   setenv CTM_IRR_3       "$OUTDIR/CCTM_IRR_3_${CTM_APPL}.nc -v"      #> Chem Process Analysis
528   setenv CTM_DRY_DEP_MOS "$OUTDIR/CCTM_DDMOS_${CTM_APPL}.nc -v"      #> Dry Dep
529   setenv CTM_DRY_DEP_FST "$OUTDIR/CCTM_DDFST_${CTM_APPL}.nc -v"      #> Dry Dep
530   setenv CTM_DEPV_MOS    "$OUTDIR/CCTM_DEPVMOS_${CTM_APPL}.nc -v"    #> Dry Dep Velocity
531   setenv CTM_DEPV_FST    "$OUTDIR/CCTM_DEPVFST_${CTM_APPL}.nc -v"    #> Dry Dep Velocity
532   setenv CTM_VDIFF_DIAG  "$OUTDIR/CCTM_VDIFF_DIAG_${CTM_APPL}.nc -v" #> Vertical Dispersion Diagnostic
533   setenv CTM_VSED_DIAG   "$OUTDIR/CCTM_VSED_DIAG_${CTM_APPL}.nc -v"  #> Particle Grav. Settling Velocity
534   setenv CTM_LTNGDIAG_1  "$OUTDIR/CCTM_LTNGHRLY_${CTM_APPL}.nc -v"   #> Hourly Avg Lightning NO
535   setenv CTM_LTNGDIAG_2  "$OUTDIR/CCTM_LTNGCOL_${CTM_APPL}.nc -v"    #> Column Total Lightning NO
536   setenv CTM_VEXT_1      "$OUTDIR/CCTM_VEXT_${CTM_APPL}.nc -v"       #> On-Hour 3D Concs at select sites
537
538   #> set floor file (neg concs)
539   setenv FLOOR_FILE ${OUTDIR}/FLOOR_${CTM_APPL}.txt
540
541   #> look for existing log files and output files
542   ( ls CTM_LOG_???.${CTM_APPL} > buff.txt ) >& /dev/null
543   ( ls ${LOGDIR}/CTM_LOG_???.${CTM_APPL} >> buff.txt ) >& /dev/null
544   set log_test = `cat buff.txt`; rm -f buff.txt
545
546   set OUT_FILES = (${FLOOR_FILE} ${S_CGRID} ${CTM_CONC_1} ${A_CONC_1} ${MEDIA_CONC}         \
547              ${CTM_DRY_DEP_1} $CTM_DEPV_DIAG $B3GTS_S $SOILOUT $CTM_WET_DEP_1\
548              $CTM_WET_DEP_2 $CTM_PMDIAG_1 $CTM_APMDIAG_1             \
549              $CTM_RJ_1 $CTM_RJ_2 $CTM_RJ_3 $CTM_SSEMIS_1 $CTM_DUST_EMIS_1 $CTM_IPR_1 $CTM_IPR_2       \
550              $CTM_IPR_3 $CTM_IRR_1 $CTM_IRR_2 $CTM_IRR_3 $CTM_DRY_DEP_MOS                   \
551              $CTM_DRY_DEP_FST $CTM_DEPV_MOS $CTM_DEPV_FST $CTM_VDIFF_DIAG $CTM_VSED_DIAG    \
552              $CTM_LTNGDIAG_1 $CTM_LTNGDIAG_2 $CTM_VEXT_1 )
553   if ( $?CTM_ISAM ) then
554      if ( $CTM_ISAM == 'Y' || $CTM_ISAM == 'T' ) then
555         set OUT_FILES = (${OUT_FILES} ${SA_ACONC_1} ${SA_CONC_1} ${SA_DD_1} ${SA_WD_1}      \
556                          ${SA_CGRID_1} )
557      endif
558   endif
559   set OUT_FILES = `echo $OUT_FILES | sed "s; -v;;g" | sed "s;MPI:;;g" `
560   ( ls $OUT_FILES > buff.txt ) >& /dev/null
561   set out_test = `cat buff.txt`; rm -f buff.txt
562
563   #> delete previous output if requested
564   if ( $CLOBBER_DATA == true || $CLOBBER_DATA == TRUE  ) then
565      echo
566      echo "Existing Logs and Output Files for Day ${TODAYG} Will Be Deleted"
567
568      #> remove previous log files
569      foreach file ( ${log_test} )
570         #echo "Deleting log file: $file"
571         /bin/rm -f $file
572      end
573
574      #> remove previous output files
575      foreach file ( ${out_test} )
576         #echo "Deleting output file: $file"
577         /bin/rm -f $file
578      end
579      /bin/rm -f ${OUTDIR}/CCTM_EMDIAG*${RUNID}_${YYYYMMDD}.nc
580
581   else
582      #> error if previous log files exist
583      if ( "$log_test" != "" ) then
584        echo "*** Logs exist - run ABORTED ***"
585        echo "*** To overide, set CLOBBER_DATA = TRUE in run_cctm.csh ***"
586        echo "*** and these files will be automatically deleted. ***"
587        exit 1
588      endif
589
590      #> error if previous output files exist
591      if ( "$out_test" != "" ) then
592        echo "*** Output Files Exist - run will be ABORTED ***"
593        foreach file ( $out_test )
594           echo " cannot delete $file"
595        end
596        echo "*** To overide, set CLOBBER_DATA = TRUE in run_cctm.csh ***"
597        echo "*** and these files will be automatically deleted. ***"
598        exit 1
599      endif
600   endif
601
```
## 執行有關之環境設定
### 控制程式之環境變數設定
- 起始日時、時間長度與步階、IC/BC/OMI及光解數據
- 污染物名稱定義
- 光化學反應與係數
- 此段應無修改的必要，只要確定連結得到正確的檔案
- 範例

```bash
602   #> for the run control ...
603   setenv CTM_STDATE      $YYYYJJJ
604   setenv CTM_STTIME      $STTIME
605   setenv CTM_RUNLEN      $NSTEPS
606   setenv CTM_TSTEP       $TSTEP
607   setenv INIT_CONC_1 $ICpath/$ICFILE
608   setenv BNDY_CONC_1 $BCpath/$BCFILE
609   setenv OMI $OMIpath/$OMIfile
610   setenv OPTICS_DATA $OMIpath/$OPTfile
611  #setenv XJ_DATA $JVALpath/$JVALfile
612   set TR_DVpath = $METpath
613   set TR_DVfile = $MET_CRO_2D
614
615   #> species defn & photolysis
616   setenv gc_matrix_nml ${NMLpath}/GC_$MECH.nml
617   setenv ae_matrix_nml ${NMLpath}/AE_$MECH.nml
618   setenv nr_matrix_nml ${NMLpath}/NR_$MECH.nml
619   setenv tr_matrix_nml ${NMLpath}/Species_Table_TR_0.nml
620
621   #> check for photolysis input data
622   setenv CSQY_DATA ${NMLpath}/CSQY_DATA_$MECH
623
624   if (! (-e $CSQY_DATA ) ) then
625      echo " $CSQY_DATA  not found "
626      exit 1
627   endif
628   if (! (-e $OPTICS_DATA ) ) then
629      echo " $OPTICS_DATA  not found "
630      exit 1
631   endif
632
```

### 記憶體與路徑設定、執行程式
- 執行程式所需電腦的環境資源，一般用unlimit控制，須視機器的情況來設定。
- 此外mpi的路徑也不同，須考量EXE編譯程式版本配套使用。
- 設定內容 包括：
  1. unlimit/limit
  2. mpi 路徑
- 執行程式（line 656）
- 完成當日工作，準備次日日期
- 範例

```bash
633 # ===================================================================
634 #> Execution Portion
635 # ===================================================================
636
637   #> Print attributes of the executable
638   if ( $CTM_DIAG_LVL != 0 ) then
639      ls -l $BLD/$EXEC
640      size $BLD/$EXEC
641 #     unlimit
642 #     limit
643   endif
644
645   #> Print Startup Dialogue Information to Standard Out
646   echo
647   echo "CMAQ Processing of Day $YYYYMMDD Began at `date`"
648   echo
649
650   #> Executable call for single PE, uncomment to invoke
651   #( /usr/bin/time -p $BLD/$EXEC ) |& tee buff_${EXECUTION_ID}.txt
652
653   #> Executable call for multi PE, configure for your system
654   set MPI = /usr/local/bin
655   set MPIRUN = $MPI/mpirun
656   ( /usr/bin/time -p mpirun  --oversubscribe -np $NPROCS $BLD/$EXEC ) |& tee buff_${EXECUTION_ID}.txt
657
658   #> Harvest Timing Output so that it may be reported below
659   set rtarray = "${rtarray} `tail -3 buff_${EXECUTION_ID}.txt | grep -Eo '[+-]?[0-9]+([.][0-9]+)?' | head -1` "
660   rm -rf buff_${EXECUTION_ID}.txt
661
662   #> Abort script if abnormal termination
663   if ( ! -e $OUTDIR/CCTM_CGRID_${CTM_APPL}.nc ) then
664     echo ""
665     echo "**************************************************************"
666     echo "** Runscript Detected an Error: CGRID file was not written. **"
667     echo "**   This indicates that CMAQ was interrupted or an issue   **"
668     echo "**   exists with writing output. The runscript will now     **"
669     echo "**   abort rather than proceeding to subsequent days.       **"
670     echo "**************************************************************"
671     break
672   endif
673
674   #> Print Concluding Text
675   echo
676   echo "CMAQ Processing of Day $YYYYMMDD Finished at `date`"
677   echo
678   echo "\\\\\=====\\\\\=====\\\\\=====\\\\\=====/////=====/////=====/////=====/////"
679   echo
680
681 # ===================================================================
682 #> Finalize Run for This Day and Loop to Next Day
683 # ===================================================================
684
685   #> Save Log Files and Move on to Next Simulation Day
686   mv CTM_LOG_???.${CTM_APPL} $LOGDIR
687   if ( $CTM_DIAG_LVL != 0 ) then
688     mv CTM_DIAG_???.${CTM_APPL} $LOGDIR
689   endif
690
691   #> check for first run and first day and d02
692   #>duplicate the CCTM_ACON result for preceding day for preparing BCON_d04
693   if ( $TODAYJ == $START_DAY && $RUN == 5 && $DM == 'd02' ) then
694     cd $OUTDIR
695       python ../icon/ACONC31-30.py CCTM_ACONC_${CTM_APPL}.nc
696     cd $CMAQ_HOME
697   endif
698
699   #> The next simulation day will, by definition, be a restart
700   setenv NEW_START false
701
702   #> Increment both Gregorian and Julian Days
703   set TODAYG = `date -ud "${TODAYG}+1days" +%Y-%m-%d` #> Add a day for tomorrow
704   set TODAYJ = `date -ud "${TODAYG}" +%Y%j` #> Convert YYYY-MM-DD to YYYYJJJ
705
706 end  #Loop to the next Simulation Day
```
### 批次時間報表

```bash
707
708 # ===================================================================
709 #> Generate Timing Report
710 # ===================================================================
711 set RTMTOT = 0
712 foreach it ( `seq ${NDAYS}` )
713     set rt = `echo ${rtarray} | cut -d' ' -f${it}`
714     set RTMTOT = `echo "${RTMTOT} + ${rt}" | bc -l`
715 end
716
717 set RTMAVG = `echo "scale=2; ${RTMTOT} / ${NDAYS}" | bc -l`
718 set RTMTOT = `echo "scale=2; ${RTMTOT} / 1" | bc -l`
719
720 echo
721 echo "=================================="
722 echo "  ***** CMAQ TIMING REPORT *****"
723 echo "=================================="
724 echo "Start Day: ${START_DATE}"
725 echo "End Day:   ${END_DATE}"
726 echo "Number of Simulation Days: ${NDAYS}"
727 echo "Domain Name:               ${GRID_NAME}"
728 echo "Number of Grid Cells:      ${NCELLS}  (ROW x COL x LAY)"
729 echo "Number of Layers:          ${NZ}"
730 echo "Number of Processes:       ${NPROCS}"
731 echo "   All times are in seconds."
732 echo
733 echo "Num  Day        Wall Time"
734 set d = 0
735 set day = ${START_DATE}
736 foreach it ( `seq ${NDAYS}` )
737     # Set the right day and format it
738     set d = `echo "${d} + 1"  | bc -l`
739     set n = `printf "%02d" ${d}`
740
741     # Choose the correct time variables
742     set rt = `echo ${rtarray} | cut -d' ' -f${it}`
743
744     # Write out row of timing data
745     echo "${n}   ${day}   ${rt}"
746
747     # Increment day for next loop
748     set day = `date -ud "${day}+1days" +%Y-%m-%d`
749 end
750 echo "     Total Time = ${RTMTOT}"
751 echo "      Avg. Time = ${RTMAVG}"
752 #source run_cctmMM_RR_DMX.csh 01 ${RUN} d04
753 exit
```

## Reference
1. https://forum.cmascenter.org/t/cctm-stops-running-on-long-simulation/292/12
1. Example
https://github.com/sinotec2/cmaq_relatives/blob/master/run_cctmMM_RR_DM.csh
1. Notes
  - CMAQ compilations
  - CMAQ初始及邊界條件設定

Here：
CCTM之設定