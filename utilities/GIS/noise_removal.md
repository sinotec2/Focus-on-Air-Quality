---
layout: default
title:  Noise Removal of a Raster Data
parent: GIS Relatives
grand_parent: Utilities
last_modified_date:   2022-03-16 16:51:21
---
# Noise Removal of a Raster Data

- [Performing Raster Noise Reduction and Edge Smoothing?](https://gis.stackexchange.com/questions/41064/performing-raster-noise-reduction-and-edge-smoothing)
- Manvir Sekhon, [Image Filters in Python](https://towardsdatascience.com/image-filters-in-python-26ee938e57d2)
  - [program](https://github.com/m4nv1r/medium_articles/blob/master/Image_Filters_in_Python.ipynb)
- [Noise Removal using Lowpass Digital Butterworth Filter in Scipy – Python](https://www.geeksforgeeks.org/noise-removal-using-lowpass-digital-butterworth-filter-in-scipy-python/)

```python
import netCDF4
import numpy as np
import os

fname='v50_SO2_2015_3_TNR_Ship.0.1x0.1.nc'
nc = netCDF4.Dataset(fname,'r')
v='emi_so2'
data=np.array(nc[v][:,:])
nc.close()
fnameO=fname.replace('.nc','N.nc')
os.system('cp '+fname+' '+fnameO)
nc = netCDF4.Dataset(fnameO,'r+')
# first a conservative filter for grayscale images will be defined.
temp = []
filter_size=9
indexer = filter_size // 2
new_image = data.copy()
nrow, ncol = data.shape
for i in range(nrow):
  for j in range(ncol):
    for k in range(i-indexer, i+indexer+1):
      for m in range(j-indexer, j+indexer+1):
        if (k > -1) and (k < nrow):
          if (m > -1) and (m < ncol):
            temp.append(data[k,m])
    temp.remove(data[i,j])
    max_value = max(temp)
    min_value = min(temp)
    if data[i,j] > max_value:
        new_image[i,j] = max_value
    elif data[i,j] < min_value:
        new_image[i,j] = min_value
    temp =[]
nc[v][:,:]=new_image[:,:]
nc.close()
```

- [Global Shipping Traffic Density](https://datacatalog.worldbank.org/search/dataset/0037580)