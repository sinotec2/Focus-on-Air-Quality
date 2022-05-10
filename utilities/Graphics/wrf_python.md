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
### 有關wrf_python
- [wrf_python](https://github.com/NCAR/wrf-python)顧名思義就是處理wrf相關檔案的python程式庫，包括讀寫、分析、以及繪圖等等。
- wrf_python是NCAR下的開放源專案，有14位作者聯合的貢獻。目前版本為1.3.3.。
- wrf_python也是NCL停止繼續發展後轉接到python的幾個專案之一，除了wrf_python，NCAR同步也持續發展PyNGL、VAPOR等等。
- 這也意味wrf_python並不是發展完全的系統，有待持續關注、也表示如果有必要，還是必須自己使用matplotlib寫繪圖套件。
- 程式碼：[wrf_python](https://github.com/NCAR/wrf-python)
- 說明、範例：[官網](https://wrf-python.readthedocs.io/en/latest/contrib.html)
### NCL、wrf-python與CCTM純量場
- NCL 雖然已經有很多範例，但是在垂直面的向量與純量分布圖這項仍然很弱。
- [NCL-for-CMAQ](https://github.com/sunsanxia/NCL-for-CMAQ)雖然有些範例是CCTM純量的垂直分布，但X軸是時間，並非水平座標，無法套用地形。
- 最困難的還是內插到統一的垂直網格系統、與地形地圖之間能沒有間隙。
  - 這點wrf-python可以做到最好。
  - 但是目前wrf-python還不能讀CMAQ系統的檔案，必須自行轉接。

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
- 模版程式：[cross-section-with-mountains](https://wrf-python.readthedocs.io/en/latest/plot.html#cross-section-with-mountains)
- 副程式
  - None
### 設定
- 垂直剖線的起訖點：不限定是X或Y方向、可以是任意點
```python
# Define the cross section start and end points
cross_start = CoordPair(lat=24.335727401728242,  lon=120.03010545651748,)
cross_end = CoordPair(lat=23.41214780981217, lon=121.79586963982419)
```

- 高度：因wrfout有40層之多，大多是自由流範圍，因此必須限定繪圖的上邊界，凸顯邊界層現象。

```python
dbz_contours = ax_cross.contourf(xs,
                                 ys[:-80],
                                 to_np(dbz_cross_filled)[:-80,:],
                                 levels=dbz_levels,
                                 cmap="rainbow",
                                 norm=dbz_norm,
                                 extend="max")
```
- X軸標籤的有效位數
  - wrf-python使用經緯度tuple作為標籤，有效位數未經修剪長短不齊。此處統一修為4碼

```python
```
- 色標
  - 原程式為自主設定。不但顏色沒有連續、也不具辨識能力。
  - cmap選項有："jet"、"rainbow"、適用所有[matplotlib選項](https://matplotlib.org/stable/tutorials/colors/colormaps.html)
  
```python
cmap="rainbow",
```
- 貼上向量
  - 任意方向上的沿流方向風速分量
  - $ U =  u \times cost + v \times sint $;
    - `lent = np.sqrt((x1-x0)**2+(y1-y0)**2)`
    - `cost = (x1-x0)/lent`
    - `sint = (y1-y0)/lent`
### IO Files
- Input Files
  - wrfout檔案：作為空間定位的模版、地形數據
  - CCTM_ACONC檔案：與wrfout解析度相同、只是座標平移、套入wrfout的網格系統中，以便應用wrf-python內插程式庫
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

| ![wrf-python.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/wrf-python.png) |
|:--:|
| <b>圖 CCTM模擬d04範圍中部地區垂直PM<sub>2.5</sub>濃度分布(NCL繪製)，單位&mu;g/M<sup>3</sup> </b>|  

## Reference
