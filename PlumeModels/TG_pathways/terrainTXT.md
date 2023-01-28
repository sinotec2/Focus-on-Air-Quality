---
layout: default
title: 地形前處理文字解析與執行控制程式
parent: RE & TG Pathways
grand_parent: Plume Models
nav_order: 3
date: 2022-02-11
last_modified_date: 2023-01-26 21:43:56
tags: plume_model sed gdal AERMAP
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

### 目標及應用

- 這支程式是一支可以獨立運作、呼叫[gen_inp](../../PlumeModels/TG_pathways/gen_inp.md)、執行aermap的外部控制程式。
- [gen_inp](../../PlumeModels/TG_pathways/gen_inp.md)雖然也可以獨立運作，然而對引數的要求較為嚴苛、不適合應用在自動化流程或使用者隨意給定的情況。因此需要有一個版本是可以接受彈性設定方式。
- 仿照本程式另外發展有CGI程式 terrain.py[^1]
- 其連續版本terrainTXT2.py，則應用在[全臺AERMAP之批次執行](../../PlumeModels/TG_pathways/twnTERR.md)

### gen_inp.py與terrainTXT.py之比較

項目|[gen_inp](../../PlumeModels/TG_pathways/gen_inp.md)|terrainTXT|說明
:-:|:-:|:-:|-
引數|`GDNAME y0 nx dx y0 ny dy`等7項|除左側7項外，亦可含`GRIDCARD`、`XYINC`等關鍵字|後者為適用在直接讀取模式設定檔
自行準備aermap.inp|是|否|後者會讀取特定檔案
產生aermap.inp|有|有|
修改aermap.inp中之DEM檔名|無|以sed修改|前者需手動確認
aermap路徑|./|/opt/local/bin|前者不必然執行
應用場合|命令列操作|自動執行|

## 程式說明

### 引數

- 字串STR： GRIDCARD XYINC Grid_Name y0 nx dx y0 ny dy 等6個數字（前3者為彈性提供）

### aermap.inp模版

- WEB+'trj_results/aermap.inp_template：置換其中的個案名稱test

```bash
CO STARTING
   TITLEONE  XYZ sample run
   DATATYPE  DEM1
   DATAFILE  test.dem
   DOMAINXY  325381 2776260 51 331219 2782072 51 
   ANCHORXY  279950 2778950 328299 2779166 51 0
**  lowr left easting  Northing Zn  easting  northing Zn of upper right
** Since longitude increases from east to west over North America, the 
** domain is defined by the southeast and northwest corners when DOMAINLL is used.
**           X-point Y-point(TWD) (UTM) easting North'g Zn of X, Y point
   RUNORNOT  run
CO FINISHED

RE STARTING
   ELEVUNIT METERS
   DISCCART  277550.0 2776550.0
   DISCCART  277650.0 2776550.0
...
   DISCCART  282450.0 2781450.0
RE FINISHED

OU STARTING
   RECEPTOR test.REC
OU FINISHED
```

### 外部程式

- /opt/local/bin/gen_inp.py：見[gen_inp.py](../../PlumeModels/TG_pathways/gen_inp.md#geninppy程式分段說明)
- /opt/local/bin/aermap
- [sed](../../utilities/OperationSystem/sed.md)

## 程式下載

### terrainTXT.py

{% include download.html content="地形前處理文字解析與執行控制程式：[terrainTXT.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/TG_pathways/terrainTXT.py)" %}，程式說明詳[文字解析副程式](terrainTXT.md)

### terrain.py

{% include download.html content="煙流模式地形前處理CGI主程式：[terrain.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrain.py)" %}

[^1]: [煙流模式地形前處理CGI主程式 terrain.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/terrain.py)，程式說明[terrain_py.md](../../utilities/CGI-pythons/terrain_py.md)
