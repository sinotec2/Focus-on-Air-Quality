---
layout: default
title: WRFOUT
parent: "WRF"
has_children: true
nav_order: 5
date: 2022-10-13 13:23:56
last_modified_date:  2022-10-13 13:24:00
permalink: /wind_models/WRFOUT/
tags: wrf wrf-python

---

# WRFOUT

- WRF的輸出檔為wrfout，可為其他模式(CMAQ/[MCIP](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/)、CAMx/[wrfcamx](https://sinotec2.github.io/FAQ/2022/07/01/wrfcamx.html)、CALPUFF/calwrf、AERMOD/[MMIF](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/ME_pathways/mmif/)等)直接讀取，也可以輸入繪圖程式進行處理分析(如[wrf-python](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python)、[NCL](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL)、[GrADs](https://sinotec2.github.io/FAQ/2022/07/21/grads.html)、[earth](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/earth/uv10_json/)及[MeteoInfo](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/MeteoInfo/))，詳細說明見於個別模式與繪圖程式。
- 基本上WRFOUT是個netCDF格式檔案，因此大多數WRFOUT的處理作業，都可以用[ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)進行拆解而用ncrcat合併，等NCO程式方法完成。
- 此處所要說明的是此二者以外、或之間的處理程式。


{: .fs-6 .fw-300 }
