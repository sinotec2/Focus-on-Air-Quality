---
layout: default
title:  wrf-python
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-05-10 19:32:12
---

# wrf-python
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
### 有關wrf-python
- [wrf-python](https://github.com/NCAR/wrf-python)顧名思義就是處理wrf相關檔案的python程式庫，包括讀寫、分析、以及繪圖等等。
- wrf-python是NCAR下的開放源專案，有14位作者聯合的貢獻。目前版本為1.3.3.。
- wrf-python也是NCL停止繼續發展後轉接到python的幾個專案之一，除了wrf-python，NCAR同步也持續發展PyNGL、VAPOR等等。
- 這也意味wrf-python並不是發展完全的系統，有待持續關注、也表示如果有必要，還是必須自己使用matplotlib寫繪圖套件。
- 程式碼：[wrf-python](https://github.com/NCAR/wrf-python)
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

## 變數定義
- wrf-python最強項的功能除了繪圖之外，就屬[getvar](https://wrf-python.readthedocs.io/en/latest/user_api/generated/wrf.getvar.html)函數及其內插程式。

### Dimensions and Terran
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-odd"><td>lat</td>
<td>Latitude</td>
<td>decimal degrees</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>lon</td>
<td>Longitude</td>
<td>decimal degrees</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>ter</td>
<td>Model Terrain Height</td>
<td><p class="first">m</p>
<p>km</p>
<p>dm</p>
<p>ft</p>
<p class="last">mi</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m’</em>.</td>
</tr>
<tr class="row-odd"><td>times</td>
<td>Times in the File or Sequence</td>
<td>&#160;</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>xtimes</td>
<td><p class="first">XTIME Coordinate</p>
<p class="last">(if applicable)</p>
</td>
<td><p class="first">minutes since</p>
<p>start of</p>
<p class="last">model run</p>
</td>
<td>&#160;</td>
</tr>
</tbody>
</table>

### Height
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-odd"><td>z/height</td>
<td>Model Height for Mass Grid</td>
<td><p class="first">m</p>
<p>km</p>
<p>dm</p>
<p>ft</p>
<p class="last">mi</p>
</td>
<td><p class="first"><strong>msl</strong> (boolean): Set to False to return AGL values. True is for MSL.  Default is <em>True</em>.</p>
<p class="last"><strong>units</strong> (str) : Set to desired units. Default is <em>‘m’</em>.</p>
</td>
</tr>
<tr class="row-even"><td>height_agl</td>
<td>Model Height for Mass Grid (AGL)</td>
<td><p class="first">m</p>
<p>km</p>
<p>dm</p>
<p>ft</p>
<p class="last">mi</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m’</em>.</td>
</tr>
<tr class="row-odd"><td>zstag</td>
<td>Model Height for Vertically Staggered Grid</td>
<td><p class="first">m</p>
<p>km</p>
<p>dm</p>
<p>ft</p>
<p class="last">mi</p>
</td>
<td><p class="first"><strong>msl</strong> (boolean): Set to False to return AGL values. True is for MSL.  Default is <em>True</em>.</p>
<p class="last"><strong>units</strong> (str) : Set to desired units. Default is <em>‘m’</em>.</p>
</td>
</tr>
</tbody>
</table>


### Temperatures
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-odd"><td>eth/theta_e</td>
<td>Equivalent Potential Temperature</td>
<td><p class="first">K</p>
<p>degC</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘K’</em>.</td>
</tr>
<tr class="row-even"><td>ctt</td>
<td>Cloud Top Temperature</td>
<td><p class="first">degC</p>
<p>K</p>
<p class="last">degF</p>
</td>
<td><p class="first"><strong>fill_nocloud</strong> (boolean): Set to True to use fill values for cloud free regions rather than surface temperature. Default is <em>False</em>.</p>
<p><strong>missing</strong> (float): The fill value to use when <em>fill_nocloud</em> is True.</p>
<p><strong>opt_thresh</strong> (float): The optical depth required to trigger the cloud top temperature calculation. Default is 1.0.</p>
<p class="last"><strong>units</strong> (str) : Set to desired units. Default is <em>‘degC’</em>.</p>
</td>
</tr>
<tr class="row-odd"><td>T2</td>
<td>2m Temperature</td>
<td>K</td>
<td>&#160;</td>
</tr>
<tr class="row-odd"><td>td2</td>
<td>2m Dew Point Temperature</td>
<td><p class="first">degC</p>
<p>K</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘degC’</em>.</td>
</tr>
<tr class="row-even"><td>td</td>
<td>Dew Point Temperature</td>
<td><p class="first">degC</p>
<p>K</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘degC’</em>.</td>
</tr>
<tr class="row-odd"><td>tc</td>
<td>Temperature in Celsius</td>
<td>degC</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>th/theta</td>
<td>Potential Temperature</td>
<td><p class="first">K</p>
<p>degC</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘K’</em>.</td>
</tr>
<tr class="row-odd"><td>temp</td>
<td>Temperature (in specified units)</td>
<td><p class="first">K</p>
<p>degC</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘K’</em>.</td>
</tr>
<tr class="row-even"><td>tk</td>
<td>Temperature in Kelvin</td>
<td>K</td>
<td>&#160;</td>
</tr>
<tr class="row-odd"><td>tv</td>
<td>Virtual Temperature</td>
<td><p class="first">K</p>
<p>degC</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘K’</em>.</td>
</tr>
<tr class="row-even"><td>twb</td>
<td>Wet Bulb Temperature</td>
<td><p class="first">K</p>
<p>degC</p>
<p class="last">degF</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘K’</em>.</td>
</tr>
</tbody>
</table>

### Pressures
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>p/pres</td>
<td><p class="first">Full Model Pressure</p>
<p class="last">(in specified units)</p>
</td>
<td><p class="first">Pa</p>
<p>hPa</p>
<p>mb</p>
<p>torr</p>
<p>mmhg</p>
<p class="last">atm</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘Pa’</em>.</td>
</tr>
<tr class="row-odd"><td>pressure</td>
<td>Full Model Pressure (hPa)</td>
<td>hPa</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>slp</td>
<td>Sea Level Pressure</td>
<td><p class="first">hPa</p>
<p>hPa</p>
<p>mb</p>
<p>torr</p>
<p>mmhg</p>
<p class="last">atm</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘hPa’</em>.</td>
</tr>
</tbody>
</table>


### Velocities
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-odd"><td>omg/omega</td>
<td>Omega</td>
<td>Pa s-1</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>ua</td>
<td>U-component of Wind on Mass Points</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-odd"><td>va</td>
<td>V-component of Wind on Mass Points</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-even"><td>wa</td>
<td>W-component of Wind on Mass Points</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-odd"><td>uvmet10</td>
<td><p class="first">10 m U and V Components of Wind</p>
<p class="last">Rotated to Earth Coordinates</p>
</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-even"><td>uvmet</td>
<td><p class="first">U and V Components of Wind</p>
<p class="last">Rotated to Earth Coordinates</p>
</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-odd"><td>wspd_wdir</td>
<td><p class="first">Wind Speed and Direction (wind_from_direction)</p>
<p class="last">in Grid Coordinates</p>
</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-even"><td>wspd_wdir10</td>
<td><p class="first">10m Wind Speed and Direction (wind_from_direction)</p>
<p class="last">in Grid Coordinates</p>
</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-odd"><td>uvmet_wspd_wdir</td>
<td><p class="first">Wind Speed and Direction (wind_from_direction)</p>
<p class="last">Rotated to Earth Coordinates</p>
</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
<tr class="row-even"><td>uvmet10_wspd_wdir</td>
<td><p class="first">10m Wind Speed and Direction (wind_from_direction)</p>
<p class="last">Rotated to Earth Coordinates</p>
</td>
<td><p class="first">m s-1</p>
<p>km h-1</p>
<p>mi h-1</p>
<p>kt</p>
<p class="last">ft s-1</p>
</td>
<td><strong>units</strong> (str) : Set to desired units. Default is <em>‘m s-1’</em>.</td>
</tr>
</tbody>
</table>


### Energy
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>cape_2d</td>
<td>2D CAPE (MCAPE/MCIN/LCL/LFC)</td>
<td>J kg-1 ; J kg-1 ; m ; m</td>
<td><strong>missing</strong> (float): Fill value for output only</td>
</tr>
<tr class="row-odd"><td>cape_3d</td>
<td>3D CAPE and CIN</td>
<td>J kg-1</td>
<td><strong>missing</strong> (float): Fill value for output only</td>
</tr>
<tr class="row-even"><td>geopt/geopotential</td>
<td>Geopotential for the Mass Grid</td>
<td>m2 s-2</td>
<td>&#160;</td>
</tr>
<tr class="row-odd"><td>geopt_stag</td>
<td>Geopotential for the Vertically Staggered Grid</td>
<td>m2 s-2</td>
<td>&#160;</td>
</tr>

</tbody>
</table>

### High Order Dynamics

<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-even"><td>avo</td>
<td>Absolute Vorticity</td>
<td>10-5 s-1</td>
<td>&#160;</td>
</tr>	 
<tr class="row-even"><td>pvo</td>
<td>Potential Vorticity</td>
<td>PVU</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>helicity</td>
<td>Storm Relative Helicity</td>
<td>m2 s-2</td>
<td><strong>top</strong> (float): The top level for the calculation in meters. Default is <em>3000.0</em>.</td>
</tr>
<tr class="row-odd"><td>updraft_helicity</td>
<td>Updraft Helicity</td>
<td>m2 s-2</td>
<td><p class="first"><strong>bottom</strong> (float): The bottom level for the calculation in meters. Default is <em>2000.0</em>.</p>
<p class="last"><strong>top</strong> (float): The top level for the calculation in meters. Default is <em>5000.0</em>.</p>
</td>
</tr>
</tbody>
</table>

### Vapors, Cloudness and Precipitation
<table border="1" class="docutils">
<colgroup>
<col width="8%" />
<col width="24%" />
<col width="11%" />
<col width="58%" />
</colgroup>
<thead valign="bottom">
<tr class="row-odd"><th class="head">Variable Name</th>
<th class="head">Description</th>
<th class="head">Available Units</th>
<th class="head">Additional Keyword Arguments</th>
</tr>
</thead>
<tbody valign="top">
<tr class="row-odd"><td>pw</td>
<td>Precipitable Water</td>
<td>kg m-2</td>
<td>&#160;</td>
</tr>
<tr class="row-even"><td>rh</td>
<td>Relative Humidity</td>
<td>%</td>
<td>&#160;</td>
</tr>
<tr class="row-odd"><td>rh2</td>
<td>2m Relative Humidity</td>
<td>%</td>
<td>&#160;</td>
</tr>
<tr class="row-even">
<td>Cloud Fraction</td>
<td>%</td>
<td><p class="first"><strong>vert_type</strong> (str): The vertical coordinate type for the cloud thresholds. Must be ‘height_agl’, ‘height_msl’, or ‘pres’.  Default is ‘height_agl’.</p>
<p><strong>low_thresh</strong> (float): The low cloud threshold (meters for ‘height_agl’ and ‘height_msl’, pascals for ‘pres’). Default is 300 m (97000 Pa)</p>
<p><strong>mid_thresh</strong> (float): The mid cloud threshold (meters for ‘height_agl’ and ‘height_msl’, pascals for ‘pres’). Default is 2000 m (80000 Pa)</p>
<p class="last"><strong>high_thresh</strong> (float): The high cloud threshold (meters for ‘height_agl’ and ‘height_msl’, pascals for ‘pres’). Default is 6000 m (45000 Pa)</p>
</td>
</tr>
<tr class="row-even"><td>dbz</td>
<td>Reflectivity</td>
<td>dBZ</td>
<td><p class="first"><strong>do_variant</strong> (boolean): Set to True to enable variant calculation. Default is <em>False</em>.</p>
<p class="last"><strong>do_liqskin</strong> (boolean): Set to True to enable liquid skin calculation. Default is <em>False</em>.</p>
</td>
</tr>
<tr class="row-odd"><td>mdbz</td>
<td>Maximum Reflectivity</td>
<td>dBZ</td>
<td><p class="first"><strong>do_variant</strong> (boolean): Set to True to enable variant calculation. Default is <em>False</em>.</p>
<p class="last"><strong>do_liqskin</strong> (boolean): Set to True to enable liquid skin calculation. Default is <em>False</em>.</p>
</td>
</tr>
</tbody>
</table>

## 垂直剖面內插程式
### 引用模版及副程式
- 模版程式：[cross-section-with-mountains](https://wrf-python.readthedocs.io/en/latest/plot.html#cross-section-with-mountains)
- 副程式
  - None
### IO Files and Coordinate translation
- Input Files
  - wrfout檔案：作為空間定位的模版、地形數據
  - CCTM_ACONC檔案：與wrfout解析度相同、只是座標平移、套入wrfout的網格系統中，以便應用wrf-python內插程式庫

```python
...
wrf_file = Dataset("wrfout_d04_2019-01-29-31")
nc=Dataset('BASE3_K24.nc')
t=int(sys.argv[1])
pm=nc["PM25_TOT"][t,:,:,:]
nc=Dataset('METDOT3D_Taiwan.nc')
t0=35*24+t
UWIND=nc["UWIND"][t0,:,:-1,:-1]
VWIND=nc["VWIND"][t0,:,:-1,:-1]
...
# Get the WRF variables
ht = getvar(wrf_file, "z", timeidx=t)
ter = getvar(wrf_file, "ter", timeidx=-1)
u = getvar(wrf_file, "ua", timeidx=t)
v = getvar(wrf_file, "va", timeidx=t)
```
- 平移CMAQ vs WRF

```python
#u[:24,8:8+131,:92-12] = UWIND[:,:,12:]
#v[:24,8:8+131,:92-12] = VWIND[:,:,12:]
w = getvar(wrf_file, "wa", timeidx=t)
#U,W= 0.1**(u*cost+v*sint),0.1**(w*34)
U,W= u*cost+v*sint,w*34
dbz = getvar(wrf_file, "dbz", timeidx=-1)
dbz[:11,8:8+131,:92-12] = pm[:,:,12:]
```
- Output Files
  - pm25_*nn*.png：*nn*=00~71
  - 為典型matplotlib存檔方式

```python
pyplot.savefig('pm25_'+'{:02d}'.format(t)+'.png')
```
### 設定
- 垂直剖線的起訖點：不限定是X或Y方向、可以是任意點
```python
# Define the cross section start and end points
cross_start = CoordPair(lat=24.453917871182558, lon=120.225062233815342,)
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
  - wrf-python使用經緯度tuple作為標籤，有效位數未經修剪長短不齊。此處統一修為2碼
  - 由於原程式是運用to_np之解讀程式，將coord_pairs經緯度值讀成字串，需將其拆解後方能改變有效位數。

```python
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]
lab=[[round(float(i),2) for i in j.split(',')] for j in x_labels[:]]
x_labels=[str(i[0])+','+str(i[1]) for i in lab]
```
- 色標
  - 原程式為自主設定。不但顏色沒有連續、也不具辨識能力。
  - cmap選項有："jet"、"rainbow"、適用所有[matplotlib選項](https://matplotlib.org/stable/tutorials/colors/colormaps.html)
  
```python
cmap="rainbow",
```
- 任意方向上的沿流方向風速分量
  - 計算分量後，U及W與濃度一樣進行垂直內插到等間距網格上
  - $ U =  u \times cost + v \times sint $;
    - `lent = np.sqrt((x1-x0)**2+(y1-y0)**2)`
    - `cost = (x1-x0)/lent`
    - `sint = (y1-y0)/lent`
    
- 貼上向量
  - 參考[stackoverflow](https://stackoverflow.com/questions/42117049/plotting-wind-vectors-on-vertical-cross-section-with-matplotlib)
  - 使用matplotlib[quiver](https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.quiver.html)指令來畫箭頭，中文可參考[程式人生](https://www.796t.com/content/1546226540.html)
  - 同樣使用[:-80]來限定高度範圍、[::2]來控制箭頭的密度

```python
ax_cross.quiver(xs[::2], ys[:-80],
          to_np(u_cross_filled[:-80, ::2]), to_np(w_cross_filled[:-80, ::2]))
```

### Parallel Operation
- 因程式沒有時間前後的交互作用，各個時間可以獨立運作。
- 將時間(小時順序)作為引數

```bash

```
### GIF Producing
- 使用[imageMagick](https://imagemagick.org/script/convert.php)串連

```bash
convert pm2.5*.png PMF.gif
```

### 程式碼
- [ver_ZhonBu.py@github](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/emis_sens/ver_ZhonBu.py)

## Results
- [gif player](https://sinotec2.github.io/PM2.5CrossSect/)

| ![wrf-python.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/wrf-python.png) |
|:--:|
| <b>圖 CCTM模擬d04範圍中部地區垂直PM<sub>2.5</sub>濃度分布(wrf-python繪製)，[動態播放](https://sinotec2.github.io/PM2.5CrossSect/)，單位&mu;g/M<sup>3</sup> </b>|  


## Reference
- Gene Z. Ragen, discussion on [Plotting wind vectors on vertical cross-section with matplotlib](https://stackoverflow.com/questions/42117049/plotting-wind-vectors-on-vertical-cross-section-with-matplotlib) 2019, Oct. 8.