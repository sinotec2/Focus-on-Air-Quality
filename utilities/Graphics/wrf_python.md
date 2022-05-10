---
layout: default
title:  wrf_python
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-05-10 19:32:12
---

# wrf_python
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
- [wrf_python](https://github.com/NCAR/wrf-python)顧名思義就是處理wrf相關檔案的python程式庫，包括讀寫、分析、以及繪圖等等。
- wrf_python是NCAR下的開放源專案，有14位作者聯合的貢獻。目前版本為1.3.3.。
- wrf_python也是NCL停止繼續發展後轉接到python的幾個專案之一，除了wrf_python，NCAR同步也持續發展PyNGL、VAPOR等等。
- 這也意味wrf_python並不是發展完全的系統，有待持續關注、也表示如果有必要，還是必須自己使用matplotlib寫繪圖套件。
- 程式碼：[wrf_python](https://github.com/NCAR/wrf-python)
- 說明、範例：[官網](https://wrf-python.readthedocs.io/en/latest/contrib.html)

## 程式庫安裝
### conda安裝
- 見[官網-安裝](https://wrf-python.readthedocs.io/en/latest/installation.html)

```python
conda install -c conda-forge wrf-python
```
### openMP重新編譯
- 如果資料分析時能夠啟動電腦的所有核心，那是再好不過了

```bash
git clone https://github.com/NCAR/wrf-python
cd ./fortran/build_help
gfortran -o sizes -fopenmp omp_sizes.f90
python sub_sizes.py
cd ..
gfortran -E ompgen.F90 -fopenmp -cpp -o omp.f90
f2py *.f90 -m _wrffortran -h wrffortran.pyf --overwrite-signature
cd ..
python setup.py clean --all
python setup.py config_fc --f90flags="-mtune=generic -fopenmp" build_ext --libraries="gomp" build
pip install .
```

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
- [CCTM模擬d01範圍PM10之時間變化 GIF](http://114.32.164.198/soong/pm10.gif)

| ![pm10_ncl.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/pm10_ncl.PNG) |
|:--:|
| <b>圖 CCTM模擬d01範圍PM10之結果(NCL繪製)，單位log<sub>10</sub>&mu;g/M<sup>3</sup> </b>|  

## Reference
