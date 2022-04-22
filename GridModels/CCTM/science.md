---
layout: default
title: CCTM之科學設定
parent: CCTM Main Program
grand_parent: CMAQ Model System
nav_order: 3
date: 2022-04-20 20:27:59
last_modified_date: 2022-04-20 20:45:42
---

# CCTM之科學設定
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

|項目|環境變數|US EPA|base|force|comment|
|-|:-|:-:|:-:|:-:|:-|
|海洋飛沫|CTM_OCEAN_CHEM|Y|N|Y|由於新版WRF在外海有高估的趨勢，開啟海洋飛沫會造成高估|
|風吹砂|CTM_WB_DUST|Y|Y|N|公版似乎不太著重PM10計算、沒有處理本土沙塵暴問題|
|閃電NOx|CTM_LTNG_NO|N|N|N|-|
|edyintb|KZMIN|Y|Y|Y|-|
|沉降速度土地使用差別化|CTM_MOSAIC|N|N|N|-|
|葉面氣孔通量差別化|CTM_FST|N|N|N|-|
|PX模組|PX_VERSION|Y|Y|Y|-|
|CLM模組|CLM_VERSION|N|N|N|-|
|NOAH模組|NOAH_VERSION|N|N|N|-|
|雙向氨沉降在線計算|CTM_ABFLUX|Y|Y|N|公版直接引入氨排放量估算值|
|扣除肥料氨氣排放|CTM_BIDI_FERT_NH3 |Y|Y|N|直接引入就不必扣除|
|雙向汞沉降在線計算|CTM_HGBIDI|N|N|N|(沒有涉及汞的議題)|
|HONO表面反應|CTM_SFC_HONO|Y|Y|Y|-|
|顆粒物重力沉降|CTM_GRAV_SETL|Y|Y|Y|-|
|生物排放在線計算|CTM_BIOGEMIS|N|N|N|-|


```bash
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
```