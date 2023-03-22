---
layout: default
title:  CMAQ結果製作成GIF
parent: NCL Programs
grand_parent: Graphics
has_children: true
last_modified_date: 2023-01-23 19:28:03
tags: NCL graphics m3nc2gif
---

# CMAQ結果製作成GIF
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

- CMAQ結果之等值圖有下列幾種做法
  1. VERDI手工或批次作圖
  2. 使用wrf-python程式m3nc2gif.py做成png與gif
  3. 使用公版模式提供的程式作圖
  4. 使用ncl程式。即此處要介紹的內容。

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

- CCTM模擬d01範圍PM<sub>10</sub>之時間變化([內容說明](../../../GridModels/Abundant_NoG_Runs/CWBWRF_15k.md))
  - [GIF_file@iMacKuang](http://125.229.149.182/soong/pm10.gif)
  - [GifPlayer@sinotec2.github.io](https://sinotec2.github.io/cmaqprog/NCL_China_WBDust/)

| ![pm10_ncl.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/pm10_ncl.PNG) |
|:--:|
| <b>圖 CCTM模擬d01範圍PM10之結果(NCL繪製)，單位log<sub>10</sub>&mu;g/M<sup>3</sup> </b>|  

## Reference
