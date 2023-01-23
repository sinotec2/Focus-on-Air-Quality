---
layout: default
title: WRFOUT
parent: "WRF"
has_children: true
nav_order: 5
date: 2022-10-13 13:23:56
last_modified_date:  2022-10-13 13:24:00
permalink: /wind_models/WRFOUT/
tags: wrf wrf-python wrfcamx

---

# WRFOUT

{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## 背景

- WRF的輸出檔為wrfout，可為其他模式(CMAQ/[MCIP](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/MCIP/)、CAMx/[wrfcamx](https://sinotec2.github.io/FAQ/2022/07/01/wrfcamx.html)、CALPUFF/calwrf、AERMOD/[MMIF](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/ME_pathways/mmif/)等)直接讀取，也可以輸入繪圖程式進行處理分析(如[wrf-python](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python)、[NCL](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL)、[GrADs](https://sinotec2.github.io/FAQ/2022/07/21/grads.html)、[earth](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/earth/uv10_json/)及[MeteoInfo](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/MeteoInfo/))，詳細說明見於個別模式與繪圖程式。
- 基本上WRFOUT是個netCDF格式檔案，因此大多數WRFOUT的處理作業，都可以用[ncks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/)進行拆解而用ncrcat合併，等NCO程式方法完成。
- 此處所要說明的是此二者以外、或之間的處理程式。

## 排放量按照月均溫與逐時氣溫分配

- [REASv3.1之面源#氣溫反比變化](../../CAMx/emis/4.3REASgrnd.md)

## 時間與空間的整併

### CAMS高度內插至WRF系統

- [CAMS高度之內插方式](../../AQana/GAQuality/ECMWF_CAMS/5.CAMS_vertdisc.md)

### 整併wrfout

- 成為全月檔案[add_xtime程式](../../GridModels/MCIP/add_xtime.md)：雖然此一方式證實不甚可行、串連的程式尚具有參考價值。
- [對時間軸整併任意批次WRF之結果](1.acc_DM.md):其危險性詳見文中說明。

## 轉檔與顯示小工具

### pr_times.py

- [WRF的時間標籤](../../utilities/DateTime/WRF_Times.md)雖然從wrf執行結果的檔名已經表明了檔案的日期，對於其他程式產生的wrfout檔案、或起始時間不是正好從0時開始，這支小程式對掌握檔案的時間標籤有非常重要的貢獻。

### CWBWRF grib2檔案轉wrfout系列程式

- [rd_grbCubicA.py](../../wind_models/cwbWRF_3Km/3.rd_grbCubicA.md)
- [相同網格系統之grb2轉檔](../../wind_models/cwbWRF_3Km/4.fil_grb_nc.md)

### wrf-chem rd_dust.py

- 基本上**WRF-chem**的模擬結果基本上還是個`wrfout`，詳見[ WRF-chem的後處理](../../wind_models/WRF-chem/rd_dust.md)