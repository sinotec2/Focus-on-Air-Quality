---
layout: default
title: "ECMWF ReAnalysis"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 4
date: 2021-12-23 14:04:02
last_modified_date:   2021-12-23 14:03:54
---

# 歐洲中期天氣預報中心再分析數據之下載
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
- 歐洲中期天氣預報中心(ECMWF)之[EAC4 (ECMWF Atmospheric Composition Reanalysis 4)](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview)長期蒐集、分析、重組全球的大氣成分數據，並以目前所理解的物化方程式予以同化，行成所謂「再分析」數據庫，並且對外提供。
- 其數據目前為已建有與WRF-chem間的應用平台，以進行空氣品質的預報系統。也經常用在區域性的空氣品質解析(如[Galmarini et al. 2021](https://acp.copernicus.org/preprints/acp-2021-313/acp-2021-313.pdf)、[Jeong and Hong 2021](https://www.mdpi.com/2072-4292/13/10/1877))。

### 作業流程
- 須先在ECMWF[哥白尼倉庫](https://ads.atmosphere.copernicus.eu/user/login?destination=/)註冊帳密(免費)。在User Profile處取得將API Key，將其寫進電腦的${HOME}/.cdsapirc檔案內，範例如下：

```bash
$ cat ~/.cdsapirc
url: https://ads.atmosphere.copernicus.eu/api/v2
key: 2556:e6b523da-4703-4dc7-bcfd-94cb2d8ed395 
```
- 下載cdsapi軟件：pip install cdsapi
- 到[eac4網址](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=form)勾選下載項目
- 在網址上選好選項後，點選「Show API request」複製retrieve{...}內容，貼在python程式內，以python程式進行下載。
- 下載完成後繼續轉變格式(`ncl_convert2nc`)、將`nc`檔案內容填入`m3.nc`檔案備用(進一步檢查)

## 下載、轉檔、橫向整併

### 空品數據之下載(get_d2.py)
- 這支程式與所用的模組基本上是[哥白尼倉庫](https://ads.atmosphere.copernicus.eu/user/login?destination=/)的提供的工具，但要下載全月的檔案，還是需要一些加工。
- `dt2jul`是時間轉換常用的模組，地球科學上常用Juian date，這個模組力求簡單方便。

```python
import cdsapi
import datetime
import os
c = cdsapi.Client()

def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)
```
- `SPECs`及`PARTs`是再分析模式的空氣品質項目名稱，常用名稱如下
  - 名稱的來源除了在[eac4勾選](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=form)網址之外，也可以在[CAMS: Reanalysis data documentation](https://confluence.ecmwf.int/display/CKB/CAMS%3A+Reanalysis+data+documentation)內找到全部列表與說明。
  - 這些名稱與**CMAQ-cb6r3_ae7_aq**之對照詳[grb2D1m3RHO.py](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2D1m3/#grb2d1m3py%E7%A8%8B%E5%BC%8F%E8%AA%AA%E6%98%8E)

```python
SPECs =['carbon_monoxide', 'ethane', 'formaldehyde', 'isoprene', 'nitrogen_dioxide', 'nitrogen_monoxide', 'propane', 'sulphur_dioxide' ]
SPECs+=['ozone', 'ammonium', 'nitrate', 'olefins', 'organic_nitrates', 'paraffins']
PARTs =[
            'dust_aerosol_0.03-0.55um_mixing_ratio', 'dust_aerosol_0.55-0.9um_mixing_ratio', 'dust_aerosol_0.9-20um_mixing_ratio',
            'hydrophilic_black_carbon_aerosol_mixing_ratio', 'hydrophilic_organic_matter_aerosol_mixing_ratio', 'hydrophobic_black_carbon_aerosol_mixing_ratio',
            'hydrophobic_organic_matter_aerosol_mixing_ratio', 'nitric_acid', 'peroxyacetyl_nitrate',
            'sea_salt_aerosol_0.03-0.5um_mixing_ratio', 'sea_salt_aerosol_0.5-5um_mixing_ratio', 'sea_salt_aerosol_5-20um_mixing_ratio',
            'sulphate_aerosol_mixing_ratio',
        ]
```
- 按照空品項目、年代、月份「依序」下載
  - 「不建議」同時、多線下載。系統可能會視為機器人攻擊。
  - 以前月15日後的16日([run5](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/#%E6%89%B9%E6%AC%A1%E7%9A%84%E5%AE%9A%E7%BE%A9))0時起算，到[run12](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/#%E6%89%B9%E6%AC%A1%E7%9A%84%E5%AE%9A%E7%BE%A9)最末日21時結束
  - 符合[WRF批次定義](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/OBSGRID/obsYYMM_run.sh/#%E6%89%B9%E6%AC%A1%E7%9A%84%E5%AE%9A%E7%BE%A9)的考量是因為CMAQ的BCON檔案會跟隨此一定義批次的起迄時間，而此處下載空品數據正是為形成或補充該BCON檔案的內容。

```python
iyr=2019
for sp in SPECs+PARTs:
  for m in range(1,13):
    mo='{:02d}'.format(m)
    fname=sp+'_'+str(iyr)[2:]+mo+'.grib'
    if os.path.exists(fname):continue
    lastYr=(datetime.datetime(iyr,m,1)+datetime.timedelta(days=-1)).year
    lastMo=(datetime.datetime(iyr,m,1)+datetime.timedelta(days=-1)).month
    beg0=datetime.datetime(lastYr,lastMo,15)
    begd=beg0+datetime.timedelta(days=4*4)
    endd=beg0+datetime.timedelta(days=12*4)
    begd=str(begd.strftime("%Y-%m-%d"))
    endd=str(endd.strftime("%Y-%m-%d"))
```
- 以[哥白尼倉庫](https://ads.atmosphere.copernicus.eu/user/login?destination=/)提供的模組進行下載
  - 層數`model_level`的定義詳見[L60 model level definitions](https://confluence.ecmwf.int/display/UDOC/L60+model+level+definitions)
  - 時間：逐3小時，0時開始

```python
    c.retrieve(
    'cams-global-reanalysis-eac4',
    {
    'model_level': ['21', '22', '23', '24', '25', '26', '27',
      '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
      '39', '40', '42', '43', '44', '46', '47', '48', '49', '50', '51',
      '53', '54', '56', '57', '59'],
    'variable': sp,
    'date': begd+'/'+endd,
    'time': [
      '00:00', '03:00', '06:00',
      '09:00', '12:00', '15:00',
      '18:00', '21:00',
        ],
```
- 範圍：如果沒有界定範圍，檔案會很大。四圍經緯度邊界之順序為北、西、南、東，逆時針方向給定。
  - d00範圍：北緯-10\~50、東經60~180。`'area': [50, 60, -10, 180,],`
  - d01範圍：北緯-2\~47、東經80~160。`'area': [47, 80, -2, 160,],`
  - d02範圍：北緯15\~32、東經111~131。`'area': [32, 111, 15, 131, ],`

```python
    'area': [
      32, 111, 15,
      131,
      ],
    'format': 'grib',
    },
     fname)  
```

### 轉檔
- 因為CMAQ、CAMx等空氣品質模式目前還沒有發展`grib2`格式的IO方式，如果要以[VERDI]()檢視結果，還是要轉成`nc`格式比較方便。
- 雖然[勾選](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=form)網址有提供`nc`檔案格式的選項，但為嘗試性結果。此處還是以[ncl_stable](https://www.ncl.ucar.edu/Download/conda.shtml)軟件包的`ncl_convert2nc`來進行轉檔。

```bash
for g in $(ls *grib);do 
  /opt/miniconda3/envs/ncl_stable/bin/ncl_convert2nc $g
done
```  

### 橫向合併
- 這項作業是將同一月份的27個分項檔案，按照相同的時間、空間軸整併成一個檔案。
- 做法：先用[ncks -v](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#%E8%AE%8A%E6%95%B8variable)取出空品濃度的矩陣，再使用[ncks -A](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#%E5%85%A8%E5%9F%9F%E5%B1%AC%E6%80%A7global-attribute)逐一附加即可。

```bash
y=$(n=$(( ${#PWD} - 1 ));echo $PWD|cut -c${n}-)
for m in {01..12};do
  fn=$y$m.nc
  if [ -e $fn ];then continue;fi
  cp ammonium_$y$m.nc $fn
  ncks -O --mk_rec_dmn initial_time0_hours $fn tmp.nc
  mv tmp.nc $fn
  for nc in $(ls *_$y$m.nc|grep -v ammonium);do
    var=$(ncdump -h $nc|grep float|grep P0_L|awkk 2|cut -d'(' -f1)
    ncks -O -v $var --mk_rec_dmn initial_time0_hours $nc tmp.nc
    ncks -A tmp.nc $fn
  done
done
```

### 污染項目的對照
- [eac4](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview)`grib2`檔案使用代碼而非污染項目之名稱，因此需要建立對照表。

```bash
for nc in $(ls *_1901.nc);do 
  var=$(ncdump -h $nc|grep float|grep P0_L|awkk 2|cut -d'(' -f1)
  spec=${nc/_1901.nc/}
  echo \"${var}\":\"${spec}\",
done
```
- 結果如下，將會用在[grb2D1m3RHO.py](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2D1m3/#grb2d1m3py%E7%A8%8B%E5%BC%8F%E8%AA%AA%E6%98%8E)

```json
{
"VAR_192_217_21_P0_L105_GLL0":"ammonium_1902.nc",
"VAR_192_210_123_P0_L105_GLL0":"carbon_monoxide_1902.nc",
"VAR_192_210_4_P0_L105_GLL0":"dust_aerosol_0.03-0.55um_mixing_ratio_1902.nc",
"VAR_192_210_5_P0_L105_GLL0":"dust_aerosol_0.55-0.9um_mixing_ratio_1902.nc",
"VAR_192_210_6_P0_L105_GLL0":"dust_aerosol_0.9-20um_mixing_ratio_1902.nc",
"VAR_192_217_45_P0_L105_GLL0":"ethane_1902.nc",
"VAR_192_210_124_P0_L105_GLL0":"formaldehyde_1902.nc",
"VAR_192_210_9_P0_L105_GLL0":"hydrophilic_black_carbon_aerosol_mixing_ratio_1902.nc",
"VAR_192_210_7_P0_L105_GLL0":"hydrophilic_organic_matter_aerosol_mixing_ratio_1902.nc",
"VAR_192_210_10_P0_L105_GLL0":"hydrophobic_black_carbon_aerosol_mixing_ratio_1902.nc",
"VAR_192_210_8_P0_L105_GLL0":"hydrophobic_organic_matter_aerosol_mixing_ratio_1902.nc",
"VAR_192_217_16_P0_L105_GLL0":"isoprene_1902.nc",
"VAR_192_217_51_P0_L105_GLL0":"nitrate_1902.nc",
"VAR_192_217_6_P0_L105_GLL0":"nitric_acid_1902.nc",
"VAR_192_210_121_P0_L105_GLL0":"nitrogen_dioxide_1902.nc",
"VAR_192_217_27_P0_L105_GLL0":"nitrogen_monoxide_1902.nc",
"VAR_192_217_11_P0_L105_GLL0":"olefins_1902.nc",
"VAR_192_217_15_P0_L105_GLL0":"organic_nitrates_1902.nc",
"VAR_192_210_203_P0_L105_GLL0":"ozone_1902.nc",
"VAR_192_217_9_P0_L105_GLL0":"paraffins_1902.nc",
"VAR_192_217_13_P0_L105_GLL0":"peroxyacetyl_nitrate_1902.nc",
"VAR_192_217_47_P0_L105_GLL0":"propane_1902.nc",
"VAR_192_210_1_P0_L105_GLL0":"sea_salt_aerosol_0.03-0.5um_mixing_ratio_1902.nc",
"VAR_192_210_2_P0_L105_GLL0":"sea_salt_aerosol_0.5-5um_mixing_ratio_1902.nc",
"VAR_192_210_3_P0_L105_GLL0":"sea_salt_aerosol_5-20um_mixing_ratio_1902.nc",
"VAR_192_210_11_P0_L105_GLL0":"sulphate_aerosol_mixing_ratio_1902.nc",
"VAR_192_210_122_P0_L105_GLL0":"sulphur_dioxide_1902.nc",
}
```

## Reference
- ECMWF, **EAC4 (ECMWF Atmospheric Composition Reanalysis 4)**, [copernicus](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview),record updated 2021-12-07 16:10:05 UTC
- Helen Setchell, Carsten Maass, **L60 model level definitions**, [confluence.ecmwf](https://confluence.ecmwf.int/display/UDOC/L60+model+level+definitions),修改于 五月 22, 2019
- Galmarini, S., Makar, P., Clifton, O., Hogrefe, C., Bash, J., Bianconi, R., Bellasio, R., Bieser, J., Butler, T., Ducker, J., Flemming, J., Hozdic, A., Holmes, C., Kioutsioukis, I., Kranenburg, R., Lupascu, A., Perez-Camanyo, J.L., Pleim, J., Ryu, Y.-H., San Jose, R., Schwede, D., Silva, S., Garcia Vivanco, M., and Wolke, R. (2021). Technical Note – **AQMEII4 Activity 1: Evaluation of Wet and Dry Deposition Schemes as an Integral Part of Regional-Scale Air Quality Models** ([preprint](https://acp.copernicus.org/preprints/acp-2021-313/acp-2021-313.pdf)). Gases/Atmospheric Modelling/Troposphere/Physics (physical properties and processes). 
- Jeong, U. and Hong, H. (2021). **Assessment of Tropospheric Concentrations of NO2 from the TROPOMI/Sentinel-5 Precursor for the Estimation of Long-Term Exposure to Surface NO2 over South Korea.** [Remote Sensing](https://www.mdpi.com/2072-4292/13/10/1877) 13 (10):1877. doi:10.3390/rs13101877.
