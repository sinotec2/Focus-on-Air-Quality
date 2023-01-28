---
layout: default
title: RE & TG Pathways
parent: Plume Models
nav_order: 3
has_children: true
permalink: /PlumeModels/REnTG_pathways/
tags: CGI_Pythons plume_model
date: 2022-02-11
last_modified_date: 2023-01-28 16:35:58
---

# 接受點與地形之設定
{: .no_toc }

地形檔案因與模擬範圍、接受點解析度等有密切關連，因此通常是複雜地形煙流模式模擬作業遇到的第一項挑戰。
- 模擬範圍需符合高斯模式均勻大氣的假設，不能超過50Km，污染源與接受點之間不能有山脈阻檔
- 解析度不能太粗造成hotspot、然也無需太密，致濃度差異太小
- 有關AERMOD在臺灣應用的實務討論，可以參考[環工技師會訊11007pp39-55](http://www.tpeea.org.tw/upload/news/files/7eea35bc4c7a4189b42566fffe2f2fee.pdf)

## AQMC提供資訊

- [空氣品質模式支援中心](https://aqmc.epa.gov.tw/)（AQMC）由環保署發包計畫執行維護工作，目前提供煙流模式所需地形數據及解析度如下

### ISCST

- 下載點[  ISCST3地形資料-zip](https://aqmc.epa.gov.tw/download/ISCST3_地形資料.zip)，解析度為200m
- 範圍： 全台共828,638筆、大於0之筆數791,182筆
- 格式：[X,Y,E] (twd97-m,twd97-m,m)

### AERMOD

- 下載點[ AERMOD地形資料-zip](https://aqmc.epa.gov.tw/download/AERMOD地形資料.zip)，
- 數據範圍西從金門至彭佳嶼，南從墾丁北至馬祖、包括外島與內陸山脈、共439個檔案，每個檔案模擬範圍為10公里，解析度100M。
- 數據內容為[x yy terrain  hill] (twd97-m,twd97-m,m,m)

## 自行產生方式

- AQMC提供數據如能使用實屬萬幸，如果範圍與解析度不適用，還是需要自行以aermap進行前處理為宜，以免造成爭議。
- 產生方式除了此處所討論的內容，亦可參考[鳥哥](https://linux.vbird.org/enve/aermap-op.php)的類似作法。

{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---



