---
layout: default
title: gridded land cover/land use
parent: Geography and Land Data
grand_parent: CMAQ Models
nav_order: 3
date: 2022-01-18 13:51:37
last_modified_date: 2022-01-18 13:51:41
---

# gridded land cover/land use
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
- [GISGeography](https://gisgeography.com/free-global-land-cover-land-use-data/)蒐集了全球LCLU
- USGS的FAQ：[Where can I get global land cover data?](https://www.usgs.gov/faqs/where-can-i-get-global-land-cover-data)
- [](https://www.researchgate.net/figure/Land-use-mapping-using-the-20-category-IGBP-Modified-MODIS-and-24-category-USGS-schemes_tbl2_262952739)

- Scanlon, B., Jolly, I., Sophocleous, M., and Zhang, L. (2007). Global Impacts of Conversions From Natural to Agricultural Ecosystems on Water Resources: Quantity Versus Quality. Water Resour. Res 43. doi:10.1029/2006WR005486.
  - Global distribution of land cover based on MODIS (1 km) satellite data using International Geosphere Biosphere Program land cover classes prepared by Boston University (Earth Observing System (EOS) Data Gateway, Cropland (2%) refers to cropland/natural vegetation mosaic. 

## Irrigation
- 42種作物有一半是旱作、一半是灌溉，影響資料結構甚巨。
- MODIS對照到USGS分類時無法明確對照出是否為旱作或灌作，即使USGS也是用其他因素來辨識。可知灌作之確認確實有其困難。

- Ozdogan, M. and Gutman, G. (2008). **A new methodology to map irrigated areas using multi-temporal MODIS and ancillary data: An application example in the continental US**. Remote Sensing of Environment 112:3520–3537. doi:10.1016/j.rse.2008.04.010.
- **Moderate Resolution Imaging Spectroradiometer (MODIS) Irrigated Agriculture Dataset for the United States (MIrAD-US)**, [USGS](https://www.usgs.gov/special-topics/monitoring-vegetation-drought-stress/science/modis-irrigated-agriculture#overview)
  - Pervez MS, Brown JF. Mapping Irrigated Lands at 250-m Scale by Merging MODIS Data and National Agricultural Statistics. Remote Sensing. 2010; 2(10):2388-2412. https://doi.org/10.3390/rs2102388.
- Global irrigation areas (2001 to 2015)[GEE-COMMUN-DATASET](https://samapriya.github.io/awesome-gee-community-datasets/projects/global_irrigation/)  
  - Deepak Nagaraj, Eleanor Proust, Alberto Todeschini, Maria Cristina Rulli, Paolo D'Odorico, **A new dataset of global irrigation areas from 2001 to 2015, Advances in Water Resources**, Volume 152,2021,103910,ISSN 0309-1708,https://doi.org/10.1016/j.advwatres.2021.103910.
- Iternationl Water Management Institute, [Global Irrigated Area Mapping](http://waterdata.iwmi.org/applications/giam2000/), Aprial 25, 2014

```python
import rasterio
import numpy as np

fname='giam_28_classes_global.tif'
img = rasterio.open(fname)
nx,ny,nz=img.width,img.height,img.count
lon_1d=[-180+(360./(nx-1))*i for i in range(nx)]
lat_1d=[90-(180./(ny-1))*i for i in range(ny)]
#d00範圍：北緯-10~50、東經60~180。'area': [50, 60, -10, 180,],
lon_1d=lon_1d[26952:]
lat_1d=lat_1d[4479+1:11199+1]

lonm, latm = np.meshgrid(lon_1d, lat_1d)
x,y=pnyc(lonm,latm, inverse=False)

dd=img.read()
data=dd[0,4479+1:11199+1,26952:]
```

```python
import numpy as np
import netCDF4
from pyproj import Proj
from scipy.interpolate import griddata

Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
fname='temp.nc'
nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=(nc.variables[V[3][0]].shape[i] for i in range(4))
var=np.zeros(shape=(29,nrow,ncol))
x1d=[nc.XORIG+nc1.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc1.YCELL*i for i in range(nrow)]
x1,y1=np.meshgrid(x1d, y1d)
maxx,maxy=x1[-1,-1],y1[-1,-1]
minx,miny=x1[0,0],y1[0,0]
boo=(abs(x) <= (maxx - minx) /2+nc1.XCELL*10) & (abs(y) <= (maxy - miny) /2+nc1.YCELL*10)
idx = np.where(boo)
mp=len(idx[0])
xyc= [(x[idx[0][i],idx[1][i]],y[idx[0][i],idx[1][i]]) for i in range(mp)]
c=data[idx[0][:], idx[1][:]]
z = griddata(xyc, c, (x1, y1), method='linear')
```