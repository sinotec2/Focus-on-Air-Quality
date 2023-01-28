---
layout: default
title: 地形前處理文字解析與執行控制程式
parent: RE & TG Pathways
grand_parent: Plume Models
nav_order: 3
date: 2022-02-11
last_modified_date: 2023-01-26 21:43:56
tags: plume_model sed gdal
---

# 地形前處理文字解析與執行控制程式
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

- 這支程式是一支可以獨立運作、呼叫[gen_inp](../../PlumeModels/TG_pathways/gen_inp.md)、執行aermap的外部控制程式。
- 仿照本程式另外發展有CGI程式 terrain.py[^1]
- 其連續版本terrainTXT2.py，則應用在[全臺AERMAP之批次執行](../../PlumeModels/TG_pathways/twnTERR.md)

## 程式說明

### 引數

- 字串STR： GRIDCARD XYINC 等6個數字

### aermap.inp模版

- WEB+'trj_results/aermap.inp_template：置換其中的個案名稱test

### 外部程式

- /opt/local/bin/gen_inp.py：見[gen_inp.py](../../PlumeModels/TG_pathways/gen_inp.md#geninppy程式分段說明)
- /opt/local/bin/aermap
- [sed](../../utilities/OperationSystem/sed.md)

## 程式下載

### terrainTXT.py

{% include download.html content="地形前處理文字解析與執行控制程式：[terrainTXT.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/TG_pathways/terrainTXT.py)" %}，程式說明詳[文字解析副程式](terrainTXT.md)

### terrain.py

{% include download.html content="煙流模式地形前處理CGI主程式：[terrain.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrain.py)" %}

[^1]: [煙流模式地形前處理CGI主程式 terrain.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrain.py)，程式說明[terrain_py.md]
