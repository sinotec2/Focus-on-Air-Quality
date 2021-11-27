---
layout: default
title: "namelist.oa"
parent: "OBSGRID"
grand_parent: "wind models"
nav_order: 3
date:               
last_modified_date:   2021-11-25 16:21:24
---

# namelist.oa 

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
- 


### `final`之預備

### `namelist.oa`模版
```bash
     1	&record1
     2	 start_year                  =  SYEA
     3	 start_month                 =    SMON
     4	 start_day                   =    SDAY
     5	 start_hour                  =    00
     6	 end_year                    =  EYEA
     7	 end_month                   =    EMON
     8	 end_day                     =    EDAY
     9	 end_hour                    =    00
    10	 interval                    = 21600
    11	/
    12
```
- little_r檔案的目錄    
```bash    	
    13	&record2
    14	 grid_id                     = GID
    15	 obs_filename                = '/Users/WRF4.1/NCEP/OBSGRID_DATA/final'
    16	 remove_data_above_qc_flag   = 32768
    17	 remove_unverified_data      = .TRUE.
    18	/
    19	 trim_domain                 = .TRUE.
    20	 trim_value                  = 5
    21	
```
- 最大觀測站點設定    
```bash    
    22	&record3
    23	 max_number_of_obs           = 50000
    24	 fatal_if_exceed_max_obs     = .TRUE.
    25	/
    26	
    27	&record4
    28	 qc_test_error_max           = .TRUE.
    29	 qc_test_buddy               = .TRUE.
    30	 qc_test_vert_consistency    = .FALSE.
    31	 qc_test_convective_adj      = .FALSE.
    32	 max_error_t                 = 10
    33	 max_error_uv                = 13
    34	 max_error_z                 = 8 
    35	 max_error_rh                = 50
    36	 max_error_p                 = 600
    37	 max_buddy_t                 = 8
    38	 max_buddy_uv                = 8
    39	 max_buddy_z                 = 8
    40	 max_buddy_rh                = 40
    41	 max_buddy_p                 = 800
    42	 buddy_weight                = 1.0
    43	 max_p_extend_t              = 1300
    44	 max_p_extend_w              = 1300
    45	/
    46	
    47	&record5
    48	 print_obs_files             = .FALSE.
    49	 print_found_obs             = .FALSE.
    50	 print_header                = .FALSE.
    51	 print_analysis              = .FALSE.
    52	 print_qc_vert               = .FALSE.
    53	 print_qc_dry                = .FALSE.
    54	 print_error_max             = .FALSE.
    55	 print_buddy                 = .FALSE.
    56	 print_oa                    = .FALSE.
    57	/
    58	
    59	&record7
    60	 use_first_guess             = .TRUE.
    61	 f4d                         = .TRUE.
    62	 intf4d                      =  3600
    63	 lagtem                      = .FALSE. 
    64	/
    65	
    66	&record8
    67	 smooth_type                 =  1
    68	 smooth_sfc_wind             =  0
    69	 smooth_sfc_temp             =  0
    70	 smooth_sfc_rh               =  0
    71	 smooth_sfc_slp              =  0
    72	 smooth_upper_wind           =  0
    73	 smooth_upper_temp           =  0
    74	 smooth_upper_rh             =  0
    75	/
    76	
    77	&record9
    78	 oa_type                     = 'Cressman'
    79	 radius_influence            = 0,
    80	 mqd_minimum_num_obs         = 30
    81	 mqd_maximum_num_obs         = 1000
    82	 oa_min_switch               = .TRUE.
    83	 oa_max_switch               = .TRUE.
    84	/
    85	 oa_type                     = 'MQD'
    86	 oa_3D_option                = 1
    87	 oa_3D_type                  = 'Cressman'
    88	 radius_influence            = 5,4,3,2,
    89	
    90	
    91	&plot_sounding
    92	 file_type                   = 'raw'
    93	 read_metoa                  = .TRUE.
    94	/
    95	 file_type                   = 'used'

```
### `obsYYMM_run.cs`的執行

## `obsYYMM_run.cs`分段說明

## 腳本出處
- dowps.sh：https://github.com/sinotec2/jtd/blob/main/docs/wind_models/WPS/dowps.sh
- 模版：https://github.com/sinotec2/jtd/blob/main/docs/wind_models/WPS/namelist.wps.loop

## Reference
- University of Waterloo, [WRF Tutorial](https://wiki.math.uwaterloo.ca/fluidswiki/index.php?title=WRF_Tutorial),  27 June 2019, at 14:53.
- Andre R. Erler, WRF-Tools/Python/wrfrun/[pyWPS.py](https://github.com/aerler/WRF-Tools/blob/master/Python/wrfrun/pyWPS.py), Commits on Nov 23, 2021.
- [WPS-ghrsst-to-intermediate](https://github.com/bbrashers/WPS-ghrsst-to-intermediate)
- [pywinter](https://pywinter.readthedocs.io/en/latest)
- [Here](https://sinotec2.github.io/jdt/doc/SST.md),2021-11-27 10:19:29
