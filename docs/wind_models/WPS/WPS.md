---
layout: default
title: "WPS"
parent: "WRF"
grand_parent: "wind models"
has_children: true
nav_order: 1
date:               
last_modified_date:   2021-11-25 16:21:24
permalink: /docs/wind_models/WPS/
---

# WPS

WRF的前處理系統
[WPS](https://github.com/wrf-model/WPS)顧名思義就是WRF的前處理系統(WRF Pre-processing System)，包括準備地理地形檔案的`geogrid.exe`、初始邊界檔案要讀取的觀測值準備`ungrid.exe`及網格化`metgrid.exe`等3支程式，而這三支程式共用同一個**名單**([namelist.wps demo](http://homepages.see.leeds.ac.uk/~lecag/wiser/namelist.wps.pdf))。
{: .fs-6 .fw-300 }
