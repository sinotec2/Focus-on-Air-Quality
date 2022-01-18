---
layout: default
title:  GeoTiff檔之讀取
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2022-01-18 15:40:57
---

# python解析KML檔
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
- python 2.7 時代有libtiff可用，可參考[githup](https://github.com/pearu/pylibtiff)
- [](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510)
  - [rasterio]

```python
import rasterio
from rasterio.plot import show
fp = r'GeoTiff_Image.tif'
img = rasterio.open(fp)
show(img)
```

```python
import rasterio
fname='giam_28_classes_global.tif'
img = rasterio.open(fname)
nx,ny,nz=img.width,img.height,img.count
data=img.read()
print(len(set(data.flatten()))) #29
```
