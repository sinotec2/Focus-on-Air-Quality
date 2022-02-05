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



## Reference
- Mohit Kaushik, **Reading and Visualizing GeoTiff | Satellite Images with Python**, [towardsdatascience](https://towardsdatascience.com/reading-and-visualizing-geotiff-images-with-python-8dcca7a74510),Aug 2, 2020
- Mapbox Revision, **Rasterio: access to geospatial raster data**, [readthedocs](https://rasterio.readthedocs.io/en/latest/), 2018
- Chimin, **Day26 網格資料的處理-Rasterio初探**, [ithome](https://ithelp.ithome.com.tw/articles/10209222)2018-11-10 21:56:37