---
layout: default
title: g0v/twgeojson
parent: GIS Relatives
grand_parent: Utilities
last_modified_date: 2023-01-31 09:11:25
tags: GIS geojson
---
# 零時政府提供之全台行政區界json檔
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

- 檔案取得即產生方式：[g0v github site](https://github.com/g0v)
- used by [natural earth shp檔轉topo.json](../Graphics/earth/shp_json.md)
- 行政範圍包括縣市、鄉鎮區、村里、以及選區
- json檔案形式：[geojson][geojson]、[topojson][topojson]

## Content

行政範圍|類別|檔案大小|檔名及位置|
:-:|:-:|:-:|-
縣市|geo.json|8.89 MB|[twCounty2010.geo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twCounty2010.geo.json)
縣市|topo.json|76.2 KB|[twCounty2010.topo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twCounty2010.topo.json)
縣市|topo.json|20.4 KB|[twCounty2010merge.topo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twCounty2010merge.topo.json)
鄉鎮區|geo.json|19.4 MB|[twTown1982.geo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twTown1982.geo.json)
鄉鎮區|topo.json|195 KB|[twTown1982.topo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twTown1982.topo.json)
村里|geo.json|34 MB|[twVillage1982.geo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twVillage1982.geo.json)
村里|topo.json|195 KB|[twVillage1982.topo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twVillage1982.topo.json)
選區|geo.json|9.87 MB|[twVote1982.geo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twVote1982.geo.json)
選區|topo.json|2.09 MB|[twVote1982.topo.json](https://raw.githubusercontent.com/g0v/twgeojson/master/json/twVote1982.topo.json)

[geojson]: <https://zh.wikipedia.org/wiki/GeoJSON> "GeoJSON是一種基於JSON的地理空間數據交換格式，它定義了幾種類型JSON對象以及它們組合在一起的方法，以表示有關地理要素、屬性和它們的空間範圍的數據。2015年，網際網路工程任務組（IETF）與原始規範作者組建了一個GeoJSON工作組，一起規範GeoJSON標準。在2016年8月，推出了最新的GeoJSON數據格式標準規範(RFC 7946)。GeoJSON使用唯一地理坐標參考系統WGS1984和十進位度單位，一個GeoJSON對象可以是Geometry, Feature或者FeatureCollection.其幾何對象包括有點（表示地理位置）、線（表示街道、公路、邊界）、多邊形（表示國家、省、領土），以及由以上類型組合成的複合幾何圖形。TopoJSON基於GeoJSON作了擴展，使得文件更小。"
[topojson]: <https://en.wikipedia.org/wiki/GeoJSON#TopoJSON> "TopoJSON 是自GeoJSON發展的一個分支，二者都是對地理訊息的編碼方式。TopoJSON不以離散方式來表示幾何物件，而是從「弧」這個單元共享線段之整合。弧是點的序列，而線串和多邊形被定義為弧的序列。 每個弧只定義一次，但可以通過不同的形狀多次引用，從而減少冗餘並減小文件大小。此外，TopoJSON 促進了使用地理訊息的應用程序，例如保留原貌的簡化形狀、自動地圖著色和製圖等。"

## geojson convert to kml

- online converter [products.aspose.app](https://products.aspose.app/gis/conversion/geojson-to-kml)