---
layout: default
title:  MeteoInfo
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-03-19 21:14:15
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

## MeteoInfo

前言

MeteoInfo是由中国气象科学研究院王亚强研究员开发的一款适用于GIS应用程序和科学计算环境（尤其是气象界）的集成框架。([知乎2020](https://zhuanlan.zhihu.com/p/136906305))
特色比較

相較於歐美龐大之地球科研備援，中國在這方面的成就似仍不足。其中最值得推荐的就是MeteoInfo系統。

MeteoInfo擁有龐大之案檔支援種類，依據2014的發表，計有12項資料格式，如下表所示。

|Data format|Data type|File type|Decoding difficulty level|Development by| Users|
|-|-|-|-|-|-|
|NetCDF|Grid|Binary|Difficult, need API library|[Unidata](https://www.unidata.ucar.edu/software/netcdf/)|Widely used, some conventions are used by atmospheric community|
|GRIB 1 and 2|Grid|Binary|Difficult|WMO|Atmospheric community|
|GrADS binary|Grid and station|Binary|Moderate|[IGES](http://opengrads.org/)|Atmospheric community|
|HDF EOS5|Grid and swath|Binary|Difficult, need API library|HDF group and NASA|Satellite community|
|ARL packed|Grid|Binary|Moderate|NOAA ARL|ARL model users|
|HYSPLIT output|Grid, station and trajectory|Binary (grid and station) or text (trajectory)|Easy|NOAA ARL|HYSPLIT model users|
|MICAPS|Grid, station and trajectory|Most are text|Easy|CMA|Atmospheric community in China|
|SYNOP|Station|Text|Moderate|WMO|Atmospheric community|
|METAR|Station|Text|Moderate|ICAO|Aviation and atmospheric communities|
|NOAA ISH|Station|Text|Moderate|NOAA|Atmospheric community|
|Longitude/latitude station|Station|Text|Easy|MeteoInfo|MeteoInfo users|
|ESRI ASCII grid|Grid|Text|Easy|ESRI|ArcGIS users|
|Surfer ASCII grid|Grid|Text|Easy|Golden Software|Surfer users|

* 可以套疊使用者指定之shape檔，做為底圖
* 套用Jython語言進行自動化

## 下載安裝
### 下載點
- [http://meteothink.org](http://meteothink.org/downloads/index.html)

### 安裝
* 隨插即用、適用在ms win、linux、macOS等所有平台

## 範例
- 
Relatives:
* 報告品質等值線+中文地形底圖OTM與NCL等值圖遠端計算服務
* line coordinates(in csv format) convert to KML file csv2kml
* 除了google map之外的展示平台
    * 地圖貼板
    * 地圖數位板
Reference

* 知乎(2020)Meteoinfo软件讲解及其下载方法
* Wang, Y.Q. (2014). MeteoInfo: GIS software for meteorological data visualization and analysis. Meteorological Applications 21 (2):360–368. doi:https://doi.org/10.1002/met.1345.