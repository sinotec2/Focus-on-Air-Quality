---
layout: default
title: 揚塵排放之準備
parent: Ground Level Emissions
grand_parent: CMAQ Models
nav_order: 2
date: 
last_modified_date: 2022-01-11 19:52:24  
---

# 揚塵排放之準備
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

## Reference

<a id=Wind_Blown_Dust></a>

### Wind-Blown Dust
The actual amount of dust emitted from an arid surface depends on wind speed, surface roughness, moisture content of the soil, vegetation coverage, soil type and texture, and air density.  The main mechanism behind strong dust storms is called “saltation bombardment”(跳躍轟擊) or “sandblasting.”(噴砂) The physics of saltation include the movement of sand particles due to wind, the impact of these particles to the surface that removes part of the soil volume, and the release of smaller dust particles. CMAQ first calculates friction velocity at the surface of the Earth. Once this friction velocity exceeds a threshold value, saltation, or horizontal movement, flux is obtained. Finally, the vertical flux of the dust is calculated based on a sandblasting efficiency formulation – a vertical-to-horizontal dust flux ratio.

CMAQ uses time-varying vegetation coverage, soil moisture and wind speed from the meteorological model, WRF. The vegetation coverage in WRF can vary depending on the configuration. In WRFv4.1+, the *Pleim-Xiu land-surface model* (**PX LSM**) was modified to provide CMAQ vegetation fraction (**VEGF_PX** in WRF renamed **VEG** in MCIP) from either the **old fractional landuse weighting table lookup method** (*pxlsm_modis_veg* = 0), or a new option where vegetation fraction is directly read from the **monthly MODIS derived vegetation** coverage (*pxlsm_modis_veg* = 1) found in the wrflowinp_d0* file(s). This was done because in recent years WRF has provided high resolution ~1 km monthly vegetation coverage that is more accurate than tables. Updates are backward compatible with older version of MCIP or WRF as long as **VEG** and **VEGF_PX**/**VEGFRA** are in those files. If users employ a different land surface model like the **NOAH LSM**, MCIP will assign the values of **VEGFRA** in WRF to **VEG** for CMAQ and the dust module will operate the same. Using the **MODIS** data in WRF via the new **PX** vegetation option provides the dust model a more accurate representation of vegetation in regions where windblown dust most occurs. 

The CMAQ windblown dust module optionally utilizes additional land use information beyond the land use information contained in the MCIP files. This *optional additional* land use information is generally available for **North American domains only** and is provided by specifying two (**DUST_LU_1** and **DUST_LU_2**) additional input data files. See [Chapter 4](CMAQ_UG_ch04_model_inputs.md) for more information on these optional model input files. If these optional additional input files are not available (e.g. for a hemispheric modeling domain), the windblown dust module can function with only the land use information contained in the MCIP files. See [Appendix A](Appendix/CMAQ_UG_appendixA_model_options.md) on further information on how to specify the land use information for the windblown dust module.

The CMAQ windblown dust module is controlled by the following RunScript flag:

```
setenv CTM_WB_DUST Y
```

Note that if this flag is set to N to indicate zero wind-blown dust emissions, users should set the CTM_EMISCHK variable in the RunScript to FALSE to avoid crashing CMAQ when it cannot find species it is looking for from dust emissions.

Alternatively, users can also edit the emission control file by commenting out the coarse and fine species expected for the wind-blown dust module. The following species are emitted by the Dust module and may be referenced in the emission control file [Table 6-1](#Table6-1):

<a id=Table6-1></a>

**Table 6-1. Aerosol Species Predicted by the Wind-Blown Dust Module** 

|**Dust Surrogate Name** | **Default CMAQ Species** | **Description** |
| --------------- | ---------|--------------------------------------- |
| PMFINE_SO4      | ASO4     | Fine-mode Sulfate                      |               
| PMCOARSE_SO4    | ASO4     | Coarse-mode Sulfate                    |             
| PMFINE_NO3      | ANO3     | Fine-mode Nitrate                      |                       
| PMCOARSE_NO3    | ANO3     | Coarse-mode Nitrate                    |                       
| PMFINE_CL       | ACL      | Fine-mode Chlorine                     |                       
| PMCOARSE_CL     | ACL      | Coarse-mode Chlorine                   |                       
| PMFINE_NH4      | ANH4     | Fine-mode Ammonium                     |                       
| PMFINE_NA       | ANA      | Fine-mode Sodium                       |                       
| PMFINE_CA       | ACA      | Fine-mode Calcium                      |                       
| PMFINE_MG       | AMG      | Fine-mode Magnesium                    |                       
| PMFINE_K        | AK       | Fine-mode Potassium                    |                       
| PMFINE_POC      | APOC     | Fine-mode Organic Carbon               |                       
| PMFINE_PNCOM    | APNCOM   | Fine-mode Non-Carbon Organic Matter    |                       
| PMFINE_LVPO1    | ALVPO1   | Fine-mode Low-Volatility hydrocarbon-like OA |                       
| PMFINE_LVOO1    | ALVOO1   | Fine-mode Low-Volatility Oxygenated OA |                       
| PMFINE_EC       | AEC      | Fine-mode Black or Elemental Carbon    |                       
| PMFINE_FE       | AFE      | Fine-mode Iron                         |                       
| PMFINE_AL       | AAL      | Fine-mode Aluminum                     |                       
| PMFINE_SI       | ASI      | Fine-mode Silicon                      |                       
| PMFINE_TI       | ATI      | Fine-mode Titanium                     |                       
| PMFINE_MN       | AMN      | Fine-mode Manganese                    |                       
| PMFINE_H2O      | AH2O     | Fine-mode Water                        |                       
| PMCOARSE_H2O    | AH2O     | Coarse-mode Water                      |                       
| PMFINE_OTHR     | AOTHR    | Fine-mode Other                        |                       
| PMCOARSE_SOIL   | ASOIL    | Coarse-mode Non-Anion Dust             |             
| PMFINE_MN_HAPS  | AMN_HAPS | Fine-mode Air toxics Manganese         |        
| PMCOARSE_MN_HAPS| AMN_HAPS | Coarse-mode Air toxics Manganese       |      
| PMFINE_NI       | ANI      | Fine-mode Nickel                       |           
| PMCOARSE_NI     | ANI      | Coarse-mode Nickel                     |         
| PMFINE_CR_III   | ACR_III  | Fine-mode Trivalent Chromium           |           
| PMCOARSE_CR_III | ACR_III  | Coarse-mode Trivalent Chromium         |         
| PMFINE_AS       | AAS      | Fine-mode Arsenic                      |            
| PMCOARSE_AS     | AAS      | Coarse-mode Arsenic                    |          
| PMFINE_PB       | APB      | Fine-mode Lead                         |           
| PMCOARSE_PB     | APB      | Coarse-mode Lead                       |         
| PMFINE_CD       | ACD      | Fine-mode Cadmium                      |            
| PMCOARSE_CD     | ACD      | Coarse-mode Cadmium                    |          
| PMFINE_PHG      | APHG     | Fine-mode Mercury                      |
| PMCOARSE_PHG    | APHG     | Coarse-mode Mercury                    |
 
 <a id="dust_lu_1"></a>

**DUST_LU_1 – Gridded land cover/land use**
<!-- BEGIN COMMENT -->
[Return to Table 4-1](#dust_lu_1_t)
<!-- END COMMENT -->

Used by: CCTM – windblown dust version only

The gridded land cover/land use (LCLU) file is an I/O API GRDDED3 file of BELD3 data projected to the modeling domain. This file must contain the following LCLU variables to be compatible with the CMAQ dust module:

-   USGS_urban
-   USGS_drycrop
-   **USGS_irrcrop**
-   **USGS_cropgrass**
-   USGS_cropwdlnd
-   USGS_grassland
-   USGS_shrubland
-   USGS_shrubgrass
-   USGS_savanna
-   USGS_decidforest
-   USGS_evbrdleaf
-   USGS_coniferfor
-   USGS_mxforest
-   USGS_water
-   USGS_wetwoods
-   USGS_sprsbarren
-   USGS_woodtundr
-   USGS_mxtundra
-   USGS_snowice

These categories are used to determine dust source locations and canopy scavenging factors for estimating dust emission in the model. This file can be created for North America using the Spatial Allocator and BELD3 tiles. The DUST_LU_1 file corresponds to the “a” output file from the Spatial Allocator. See the chapters on [creating inputs to SMOKE biogenic processing](https://www.cmascenter.org/sa-tools/documentation/4.2/html/smoke_bio_inputs.html) and [generating BELD3 data for biogenic emissions processing](https://www.cmascenter.org/sa-tools/documentation/4.2/html/scripts_test.html) of the Spatial Allocator User’s Guide for details.

<a id="dust_lu_2"></a>
**DUST_LU_2 – BELD land use “TOT” data file**
<!-- BEGIN COMMENT -->
[Return to Table 4-1](#dust_lu_1_t)
<!-- END COMMENT -->

Used by: CCTM – windblown dust version only

The gridded land cover/land use (LCLU) file is an I/O API GRDDED3 file of BELD3 data projected to the modeling domain. This file must contain the following variables to be compatible with the CMAQ dust module:

-   **FOREST**

This variable is used in combination with the variables in the **DUST_LU_1** file to determine canopy scavenging factors for estimating dust emission in the model. This file can be created for North America using the Spatial Allocator and BELD3 tiles. The **DUST_LU_2** file corresponds to the “tot” output file from the Spatial Allocator. See the chapters on [creating inputs to SMOKE biogenic processing](https://www.cmascenter.org/sa-tools/documentation/4.2/html/smoke_bio_inputs.html) and [generating BELD3 data for biogenic emissions processing](https://www.cmascenter.org/sa-tools/documentation/4.2/html/scripts_test.html) of the Spatial Allocator User’s Guide for details. Please also note that the "tot" input file provided with the Spatial Allocator package prior to March 12, 2020 contained incorrect values for the **FOREST** variable. An updated file with Spatial Allocator input data containing the corrected "tot" files has been posted on the CMAS data warehouse and can be accessed at [this link](https://drive.google.com/file/d/1wUo0E45U6o_JNoxmnx1Cxv89LsvENTrI/view).


### Windblown dust emissions configuration

<!-- BEGIN COMMENT -->

[Return to Top](#TOC_A)

<!-- END COMMENT -->

-   `CTM_WB_DUST [default: False]`<a id=CTM_WB_DUST></a>  
    Setting to calculate online windblown dust emissions in CCTM. Setting this variable to Y also enables the option to provide additional gridded landuse input files beyond the land use information contained in the MCIP files. Whether or not additional landuse information is provide and, if yes, whether that additional landuse information is provided in one or two files is controlled by the environment variable CTM_WBDUST_BELD. See [Chapter 6](../CMAQ_UG_ch06_model_configuration_options.md#wind-blown-dust) for further information.
    
- `CTM_WBDUST_BELD [default: UNKNOWN]`<a id=CTM_WBDUST_BELD></a>  
     Landuse database for identifying dust source regions; ignore if CTM_WB_DUST = FALSE
    - BELD3: Use BELD3 landuse data for windblown dust calculations. The user needs to specify the DUST_LU_1 and DUST_LU_2 files described in [Chapter 4](../CMAQ_UG_ch04_model_inputs.md). These files typically are available for North American domains only.
    - UNKNOWN: Use landuse information provided by MCIP for windblown dust calculations
    
-   `DUST_LU_1 [default: Path to BELD3 Data]`<a id=DUST_LU_1></a>  
    Input BELD "A" landuse netCDF file gridded to the modeling domain. Only used if `CTM_WBDUST_BELD` is set to BELD3.  

-   `DUST_LU_2 [default: Path to BELD3 Data]`<a id=DUST_LU_2></a>  
    Input BELD "TOT" landuse netCDF file gridded to the modeling domain. Only used if `CTM_WBDUST_BELD` is set to BELD3.  

- [source](https://raw.githubusercontent.com/USEPA/CMAQ/main/DOCS/Users_Guide/Appendix/CMAQ_UG_appendixA_model_options.md)

- MODIS_0:var_desc = "17. MODIS: 0 water                                                              " ;
- MODIS_1:var_desc = "1. MODIS: 1 evergreen needleleaf *forest*                                         " ;
- MODIS_2:var_desc = "2. MODIS: 2 evergreen broadleaf *forest*                                          " ;
- MODIS_3:var_desc = "3. MODIS: 3 deciduous needleleaf *forest*                                         " ;
- MODIS_4:var_desc = "4. MODIS: 4 deciduous broadleaf *forest*                                          " ;
- MODIS_5:var_desc = "5. MODIS: 5 mixed *forests*                                                       " ;
- MODIS_6:var_desc = "6. MODIS: 6 closed shrublands                                                   " ;
- MODIS_7:var_desc = "7. MODIS: 7 open shrublands                                                     " ;
- MODIS_8:var_desc = "8. MODIS: 8 woody savannas(稀樹草原)                                             " ;
- MODIS_9:var_desc = "9. MODIS: 9 savannas                                                            " ;
- MODIS_10:var_desc = "10. MODIS: 10 grasslands                                                        " ;
- MODIS_11:var_desc = "11. MODIS: 11 permanent wetlands                                                " ;
- MODIS_12:var_desc = "12. MODIS: 12 croplands                                                         " ;
- MODIS_13:var_desc = "13. MODIS: 13 urban and built up                                                " ;
- MODIS_14:var_desc = "14. MODIS: 14 cropland / natural vegetation mosaic                              " ;
- MODIS_15:var_desc = "15. MODIS: 15 permanent snow and ice                                            " ;
- MODIS_16:var_desc = "16. MODIS: 16 barren or sparsely vegetated                                      " ;
- MODIS_Res1:var_desc = "18. MODIS: Reserved (e.g. Unclassified)                                         " ;
- MODIS_Res2:var_desc = "19. MODIS: Reserved (e.g. Fill Value)                                           " ;
- MODIS_Res3:var_desc = "20. MODIS: Reserved                                                             " ;
- NLCD_11:var_desc = "21. NLCD: 11 Open Water                                                         " ;
- NLCD_12:var_desc = "22. NLCD: 12 Perennial Ice/Snow                                                 " ;
- NLCD_21:var_desc = "23. NLCD: 21 Developed Open Space                                               " ;
- NLCD_22:var_desc = "24. NLCD: 22 Developed Low Intensity                                            " ;
- NLCD_23:var_desc = "25. NLCD: 23 Developed Medium Intensity                                         " ;
- NLCD_24:var_desc = "26. NLCD: 24 Developed High Intensity                                           " ;
- NLCD_31:var_desc = "27. NLCD: 31 Barren Land (Rock/Sand/Clay)                                       " ;
- NLCD_41:var_desc = "28. NLCD: 41 Deciduous Forest                                                   " ;
- NLCD_42:var_desc = "29. NLCD: 42 Evergreen Forest                                                   " ;
- NLCD_43:var_desc = "30. NLCD: 43 Mixed Forest                                                       " ;
- NLCD_51:var_desc = "31. NLCD: 51 Dwarf Scrub                                                        " ;
- NLCD_52:var_desc = "32. NLCD: 52 Shrub/Scrub                                                        " ;
- NLCD_71:var_desc = "33. NLCD: 71 Grassland/Herbaceous                                               " ;
- NLCD_72:var_desc = "34. NLCD: 72 Sedge/Herbaceous                                                   " ;
- NLCD_73:var_desc = "35. NLCD: 73 Lichens                                                            " ;
- NLCD_74:var_desc = "36. NLCD: 74 Moss                                                               " ;
- NLCD_81:var_desc = "37. NLCD: 81 Pasture/Hay                                                        " ;
- NLCD_82:var_desc = "38. NLCD: 82 Cultivated Crops                                                   " ;
- NLCD_90:var_desc = "39. NLCD: 90 Woody Wetlands                                                     " ;
- NLCD_95:var_desc = "40. NLCD: 95 Emergent Herbaceous Wetlands                                       " ;


|MODIS Category Land Use Description |USGS Category Land Use Description|
|-|-|
|1 Evergreen Needleleaf Forest |14 Evergreen Needleleaf|
|2 Evergreen Broadleaf Forest |13 Evergreen Broadleaf|
|3 Deciduous Needleleaf Forest |12 Deciduous Needleleaf Forest|
|4 Deciduous Broadleaf Forest |11 Deciduous Broadleaf Forest|
|5 Mixed Forests |15 Mixed Forest|
|6 Closed Shrublands |8 Shrubland|
|7 Open Shrublands |9 Mixed Shrubland/Grassland|
|8 Woody Savannas|10 Savanna|
|9 Savannas |10 Savanna|
|10 Grasslands 7 Grassland|
|11 Permanent Wetlands |17 Herbaceous Wetland|
||18 Wooden Wetland|
|12 Croplands|2 Dryland Cropland and Pasture|
||3 Irrigated Cropland and Pasture|
||4 Mixed Dryland/Irrigated Cropland and Pasture|
|13 Urban and Built-Up |1 Urban and Built-up Land|
|14 Cropland/Natural Vegetation |5 Cropland/Grassland Mosaic|
||6 Cropland/Woodland Mosaic|
|15 Snow and Ice 2|4 Snow or Ice|
|16 Barren or Sparsely Vegetated |19 Barren or Sparsely Vegetated|
|17 Water |16 Water Bodies|
|18 Wooded Tundra |21 Wooded Tundra|
|19 Mixed Tundra |22 Mixed Tundra|
|23 Bare Ground Tundra|-|
|20 Barren Tundra |20 Herbaceous Tundra|
- Park, R., Hong, S., Kwon, H., Kim, S., Guenther, A., Woo, J., and Loughner, C. (2013). **An evaluation of O3 dry deposition simulations in East Asia**. [ATMOSPHERIC CHEMISTRY AND PHYSICS](https://www.researchgate.net/figure/Land-use-mapping-using-the-20-category-IGBP-Modified-MODIS-and-24-category-USGS-schemes_tbl2_262952739) 14. doi:10.5194/acpd-14-919-2014.



### 2018_EAsia_81K_time20180315_bench.nc variables
- CPHT:var_desc = Crop Height
- DN:var_desc = N-NO3 Denitrification
- DN2:var_desc = N-N2O from NO3 Denitrification
- FBARE:var_desc = Bare Land Fraction for Wind Erosion
- FPL:var_desc = Labile P Fertilizer
- FPO:var_desc = Organic P Fertilizer
- GMN:var_desc = N Mineralized                                                                   
- HMN:var_desc = OC Change by Soil Respiration
- L1_ANH3:var_desc = Layer1 N-NH3 AppRate                                                            
- L1_ANO3:var_desc = Layer1 N-NO3 AppRate                                                            
- L1_AON:var_desc = Layer1 N-ON AppRate                               
- L1_BD:var_desc = Layer1 Bulk Density                                                          
- L1_C:var_desc = Layer1 Carbon
- L1_DEP:var_desc = Layer1 Depth                                                                
- L1_NH3:var_desc = Layer1 N - Ammonia                                                          
- L1_NITR:var_desc = Layer1 N - Nitrified NH3                                                   
- L1_NO3:var_desc = Layer1 N - Nitrate                                                          
- L1_ON:var_desc = Layer1 N - Organic N                                                         
- L1_SW:var_desc = Layer1 Soil Water
- L2_ANH3:var_desc = Layer2 N-NH3 AppRate                                                       
- L2_ANO3:var_desc = Layer2 N-NO3 AppRate                                                       
- L2_AON:var_desc = Layer2 N-ON AppRate                                                         
- L2_BD:var_desc = Layer2 Bulk Density                                                          
- L2_C:var_desc = Layer2 Carbon
- L2_DEP:var_desc = Layer2 Depth                                                                
- L2_NH3:var_desc = Layer2 N- Ammonia                                                           
- L2_NITR:var_desc = Layer2 N - Nitrified NH3                                                   
- L2_NO3:var_desc = Layer2 N - Nitrate                                                          
- L2_ON:var_desc = Layer2 N - Organic N                                                         
- L2_SW:var_desc = Layer2 Soil Water
- LAI:var_desc = Leaf Area Index                                                                
- MNP:var_desc =  P Mineralized                                                                 
- NFIX:var_desc = N Fixation
- T1_BD:var_desc = TotalSoilnoLayer1 Bulk Density                                                  
- T1_C:var_desc = TotalSoilnoLayer1 Carbon
- T1_DEP:var_desc = TotalSoilnoLayer1 Depth                                                        
- T1_NH3:var_desc = TotalSoilnoLayer1 N - Ammonia                                                  
- T1_NITR:var_desc = TotalSoilnoLayer1 N - Nitrified NH3                                           
- T1_NO3:var_desc = TotalSoilnoLayer1 N - Nitrate                                                  
- T1_ON:var_desc = TotalSoilnoLayer1 N - Organic N                                                 
- TFLAG:var_desc = Timestep-valid flags:  (1) YYYYDDD or (2) HHMMSS                                
- YW:var_desc = Wind Erosion

## CMAQ Wind-Blown Dust Incremental Results

| ![CMAQ_WBDinc.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CMAQ_WBDinc.PNG) |
|:--:|
| <b>2018/03/31-04/07沙塵暴期間d01範圍PM10最大增量之分布</b>|

## Composition of Wind Blown Dust
- Tegen, I. & Kohfeld, K.E.: **Atmospheric Transport of Silicon, in: The silica cycle, human perturbations and impacts on aquatic systems**, edited by Ittekot V. et al. anthropic, Scope 66, 2006. [Simon Fraser University](http://rem-main.rem.sfu.ca/papers/kohfeld/TegenKohfeld_Scope_ch_7pp81_92.pdf)
- Claquin, T., M. Schulz, and Y. Balkanski. 1999. **Modelling the mineralogy of atmospheric dust sources.** Journal of Geophysical Research 104:22,243–22,256.[agupubs](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/1999JD900416)
- Leinen, M., Prospero, J.M., Arnold, E., and Blank, M. (1994). **Mineralogy of aeolian dust reaching the North Pacific Ocean: 1. Sampling and analysis.** Journal of Geophysical Research: Atmospheres 99 (D10):21017–21023. doi:10.1029/94JD01735.[agupubs](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/94JD01735)
- Merrill, J., E. Arnold, M. Leinen, and C. Weaver, **Mineralogy of aeolian dust reaching the north Pacific Ocean, 2, Relationship of mineral assemblages to atmospheric transport patterns**, J. Geophys. Res., 99, 21,025-21,032, 1994.[agupubs](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/94JD01734)
- wiki, **蒙古高原沙塵暴**, [wiki](https://zh.wikipedia.org/wiki/蒙古高原沙尘暴)
  - 2001年中國進行的分析資料顯示，亞洲沙塵當中含有高濃度的矽（24-32%）、鋁（5.9-7.4%）、鈣（6.2-12%）及鐵。
  - 另外也有一些毒物，其中以較重的物質為多（如有毒的水銀與鎘，多由燃煤釋出），這定出亞洲沙塵的淵源。
- Zhang, X. Y., S. L. Gong, Z. X. Shen, F. M. Mei, X. X. Xi, L. C. Liu, Z. J. Zhou, D. Wang, Y. Q. Wang, and Y. Cheng, Characterization of soil dust aerosol in China and its transport and distribution during 2001 ACE-Asia: Network observations, J. Geophys. Res., 108, doi:10.1029/2002JD002632, in press, 2003, [agupubs](https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2002JD002632)
- Gong, S.L., Zhang, X.Y., Zhao, T.L., McKendry, I.G., Jaffe, D.A., and Lu, N.M. (2003). Characterization of soil dust aerosol in China and its transport and distribution during 2001 ACE‐Asia: 2. Model simulation and validation. Journal of Geophysical Research: Atmospheres 108 IssueD9. doi:10.1029/2002JD002632.[agupubs](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2002JD002633)

- Table 3. Source Profiles, Weight Percent, of Dust Elements in Asian Dust Aerosol Mass

|Asian Dust Sources|Al|Ca|Fe|K|Mg|Mn|Si|Ti|sum|
|-|-|-|-|-|-|-|-|-|-|
|Western High-Dust Sourcea|7|12|6|3|3|0.1|24|0.5|55.6|
|Northern High-Dust Sourceb|7|7|4|2|2|0.1|30|0.5|52.6|
|Loess area|7|8|4|3|1|0.1|29|0.5|52.6|
|Molecular wt.|26.98|40.078|55.845|39.0983|24.305|54.938044|28.0855|47.867||
|total oxides/metal|

```python
sp='Al|Ca|Fe|K|Mg|Mn|Si|Ti'.split('|')
oxn=[3/2,1,3/2,0.5,1,7/2,2,2]
mw=[float(i) for i in '26.98|40.078|55.845|39.0983|24.305|54.938044|28.0855|47.867'.split('|')]
s='7^I12^I6^I3^I3^I0.1^I24^I0.5';WesternHDS=[float(i) for i in s.split()]
s='7^I7^I4^I2^I2^I0.1^I30^I0.5';NorthernHDS=[float(i) for i in s.split()]
s='7	8	4	3	1	0.1	29	0.5';LoessArea=[float(i) for i in s.split()]
In [45]: L=[i+i/m*o*16 for i ,m, o in zip(LoessArea,mw,oxn)]
In [46]: L
Out[46]:
[13.226834692364715,
 11.19377214431858,
 5.71904378189632,
 3.6138374302719045,
 1.6583007611602552,
 0.20193300657009194,
 62.041961154332306,
 0.8342595107276412]
In [47]: sum(L)
Out[47]: 98.48994248164182
In [48]: N=[i+i/m*o*16 for i ,m, o in zip(NorthernHDS,mw,oxn)]
In [49]: sum(N)
Out[49]: 99.68378721884399
In [50]: W=[i+i/m*o*16 for i ,m, o in zip(WesternHDS,mw,oxn)]
In [51]: sum(W)
Out[51]: 99.56606211287455
```
- ACONC檔案中的地殼元素名稱，均為J(accumulation mode):

```python
In [59]: nc = netCDF4.Dataset(fname, 'r')

In [60]: V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]

In [63]: sp=[i.upper() for i in sp]

In [65]: for m in sp:
    ...:     print([i for i in V[3] if 'A'+m in i])
    ...:
['AALJ', 'SOAALK']
['ACAJ', 'ASEACAT']
['AFEJ']
['AKJ']
['AMGJ']
['AMNJ']
['ASIJ']
['ATIJ']
```


- Tejas Shah, Yuge Shi, Ross Beardsley and Greg Yarwood, **Speciation Tool User’s Guide Version 5.0**, Ramboll US Corporation,[cmascenter](https://www.cmascenter.org/speciation_tool/documentation/5.0/Ramboll_sptool_users_guide_V5.pdf), June 2020
  - 𝑀𝑂<sub>𝑢𝑛𝑎𝑑𝑗𝑢𝑠𝑡𝑒𝑑</sub> = ∑𝑂𝑥<sub>𝐸𝑙</sub> × 𝐸<sub>𝐸𝑙</sub>
  - where 𝑀𝑂<sub>𝑢𝑛𝑎𝑑𝑗𝑢𝑠𝑡𝑒𝑑</sub> is the unadjusted MO, Ox<sub>𝐸𝑙</sub> is the **oxygen-to-metal ratio** for metal El as shown Table E-2, and 𝐸<sub>𝐸𝑙</sub> is the **emission** of metal El, except for Na, Ca, Mg and K. For these 4 metals, the 𝐸<sub>𝐸𝑙</sub> should reflect the difference between the atom form of the metal and the ion form. If, for Na, Ca, Mg, and K, the profile has only one form (atom or ion but not both) then the 𝐸<sub>𝐸𝑙</sub> should be set to 0. Also, if the difference is negative, it should be set to 0. Note that for metal oxides with multiple forms an average oxygen to metal ratio across all forms is used.

|Species|MW of metal<sup>1</sup>|Oxide Form 1|Oxide Form 2|Oxide Form 3|oxygen/metal ratio Ox<sub>𝐸𝑙</sub>|
|-|-|-|-|-|-|
|Mg|24.31|MgO|||0.658|
|Al|26.98|Al<sub>2</sub>O<sub>3</sub>|||0.889|
|Si|28.09|SiO<sub>2</sub>|||1.139|
|K|39.10|K<sub>2</sub>O|||0.205|
|Ca|40.08|CaO|||0.399|
|Ti|47.87|TiO<sub>2</sub>|||0.669|
|Mn|54.94|MnO|MnO<sub>2</sub>|Mn<sub>2</sub>O<sub>7</sub>|0.631|
|Fe|55.85|FeO|Fe<sub>2</sub>O<sub>3</sub>||0.358|

### submicron asian dust composition
- Vlasenko, A., Sjögren, S., Weingartner, E., Gäggeler, H.W., and Ammann, M. (2005). **Generation of Submicron Arizona Test Dust Aerosol: Chemical and Hygroscopic Properties**. [Aerosol Science and Technology](https://www.tandfonline.com/doi/pdf/10.1080/027868290959870) 39 (5):452–460. doi:10.1080/027868290959870.
  - Elemental composition of mineral dust expressed in **%** of atom

|Species|ATD powder ICP-OES|Particle bulk ICP-OES|Particle surface  XPS|
|-|-|-|-|
|Na|2.3 ± 0.2|2.9 ± 0.2|2|
|Mg|2.1 ± 0.2|4.7 ± 0.2|∗|
|Al|8.2 ± 0.3|15.9 ± 0.3|24|
|Si|79.1 ± 1|63 ± 1|63|
|K|1.7 ± 0.2|3.1 ± 0.2|3|
|Fe|2.2 ± 0.1|4.9 ± 0.2|3|
|Ca|4 ± 0.2|4.8 ± 0.2|5|

∗XPS data on Mg is not available because Mg anticathode was used as X-ray source.

Mass concentration (in µg·m−3) of identified compounds in water-soluble fraction of mineral dust aerosol generated from ATD

|Compound Concentration|
|-|-|
|Fluoride |0.1 ± 0.05|
|Acetate |<0.3|
|Formate |<0.5|
|Chloride |0.7 ± 0.1|
|Nitrate |0.2 ± 0.1|
|Sulphate |41 ± 0.5|
|Phosphate |3 ± 0.3|

- YANG, T., SUN, Y.-L., ZHANG, W., WANG, Z.-F., and WANG, X.-Q. (2016). **Chemical characterization of submicron particles during typical air pollution episodes in spring over Beijing**. [Atmospheric and Oceanic Science Letters](https://www.tandfonline.com/doi/full/10.1080/16742834.2016.1173509) 9 (4):255–262. doi:10.1080/16742834.2016.1173509.
  - The two-factor solution, including a hydrocarbon-like OA (HOA) and an oxygenated OA (OOA) with fpeak = 0, was chosen in this study.

  |spec|Haze Episode|Clean|Dust Episode|
  |-|-|-|-|
  |org|31|79|64|
  |Chl|2|2|3|
  |NH4|19|9|12|
  |NO3|32|2|10|
  |SO4|15|7|12|
  
  |spec|Haze Episode|Clean|Dust Episode|
  |-|-|-|-|
  |HOA|21|59|47|
  |OOA|79|41|53|
  
### CAMS / EAC4 DUST meaning
- Aerosol model updates
  - The CAMS aerosol model component of the IFS was previously described in Morcrette et al. (2009). It is a hybrid bulk–bin scheme with 12 prognostic tracers, consisting of three bins for sea salt depending on size (0.03–0.5, 0.5–5 and 5–20 &mu;m), three bins for dust (0.030–0.55, 0.55–0.9 and 0.9–20 &mu;m), hydrophilic and hydrophobic organic matter (OM), and black carbon (BC), plus sulfate aerosol and a gas-phase sulfur dioxide (SO2) precursor. 
  - The different aerosol types are treated as externally mixed, i.e. separate particles. Transport by advection, convection and diffusion is handled by the meteorological model component of the IFS. 
  - The aerosol scheme includes prescribed and online emissions (as described in Sect. 2.2), dry and wet deposition, production of sulfate from SO2, and ageing of hydrophobic OM and BC to hydrophilic OM and BC. 
  - Nitrate aerosols are not yet included in the aerosol scheme. The missing nitrate aerosol is likely to cause an underestimation of total aerosol in the forecast model in regions where nitrate would be a significant component. 
  - The total aerosol will be corrected by the assimilation of total AOD observations.
- Inness, A., Ades, M., Agustí-Panareda, A., Barré, J., Benedictow, A., Blechschmidt, A.-M., Dominguez, J.J., Engelen, R., Eskes, H., Flemming, J., Huijnen, V., Jones, L., Kipling, Z., Massart, S., Parrington, M., Peuch, V.-H., Razinger, M., Remy, S., Schulz, M., and Suttie, M. (2019). **The CAMS reanalysis of atmospheric composition**. [Atmospheric Chemistry and Physics](https://acp.copernicus.org/articles/19/3515/2019/) 19 (6):3515–3556. doi:10.5194/acp-19-3515-2019.

- New nitrate and ammonium aerosol species,
  - Richard Engelen,**Implementation of IFS cycle 46r1**, [confluence.ecmwf](https://confluence.ecmwf.int/display/COPSRV/Implementation+of+IFS+cycle+46r1)July 05, 2019

  