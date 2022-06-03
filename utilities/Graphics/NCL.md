---
layout: default
title:  NCL Programs
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-02-05 09:43:40
---

# NCL Programs
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
- NCL([NCAR Command Language](https://www.ncl.ucar.edu/))是美國大氣研究中心出台的繪圖軟體，目前已經出到6.6.2版。
- 雖然NCL也會持續維護，然而自2019年開始，NCAR開始將系統陸續[轉到python平台](https://www.ncl.ucar.edu/Document/Pivot_to_Python/faq.shtml)上，6.6.2版之上將不會發展新的功能。
- 由於NCL的圖面已為各大期刊所熟識，其解析度、正確性及品質也受到肯定，因此許多程式仍然繼續沿用。
- 此處介紹CMAQ結果GIF之製作方式，以做為範例。

## 程式說明
### 引用模版及副程式
- 模版程式：NCL Graphics: Contour Effects[coneff_18.ncl](https://www.ncl.ucar.edu/Applications/Scripts/coneff_18.ncl)
- 副程式
  - None

### IO Files
- Input Files
  - CMAQ濃度檔案；將[combine](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/run_combMM_R_DM/)後之PM10及TFLAG(以[ncks]())切割出來單獨成檔即可。
  - GRIDCRO2D_1804_run5.nc：只會讀取其中的經緯度(4階)矩陣
  - bou2_4p.shp：[大陸地區之行政區界](https://github.com/GuangchuangYu/chinamap/blob/master/inst/extdata/china/bou2_4p.shp)
- Output Files
  - pm10*nnn*.png：*nnn*=000~215

### GIF Producing
- 使用[imageMagick](https://imagemagick.org/script/convert.php)串連

```bash
convert pm10*.png pm10.gif
```

### 程式碼
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/post/pm10.ncl)

## Results
- [CCTM模擬d01範圍PM10之時間變化](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/Abundant_NoG_Runs/CWBWRF_15k/) 
  - [GIF_file@iMacKuang](http://114.32.164.198/soong/pm10.gif)
  - [GifPlayer@sinotec2.github.io](https://sinotec2.github.io/cmaqprog/NCL_China_WBDust/)

| ![pm10_ncl.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/pm10_ncl.PNG) |
|:--:|
| <b>圖 CCTM模擬d01範圍PM10之結果(NCL繪製)，單位log<sub>10</sub>&mu;g/M<sup>3</sup> </b>|  

## Reference
