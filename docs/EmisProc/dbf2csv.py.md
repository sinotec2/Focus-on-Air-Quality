---
layout: default
title: "dbf2csv.py"
parent: "Emission Processing"
nav_order: 1
last_modified_at:   2021-12-01 13:06:16
---

# 龐大`.dbf`檔案之讀取
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

### `.dbf`檔案格式之歷史與必須性
- 在`python`、`ruby`等高階資料庫程式語言流行之前，[DBASE](https://zh.wikipedia.org/wiki/DBase)是早期常用的資料庫軟體之一，雖然目前仍然持續發展應用，然其活力已大不如前。`dbf`檔案即為[DBASE](https://zh.wikipedia.org/wiki/DBase)軟體指定使用的資料庫檔案格式，目前仍為環保署[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)資料庫之公告檔案格式，其強項包括：
  - 具有清楚規範的表頭
  - 資料表之長度可以跨越一般軟體的限制，然而**仍有上限**。
  - 為多數軟體、程式語言間互通之格式

### 方案及策略
- 如前所述，使用資料庫軟體查詢、修改，會因應**資料筆數太長**而失敗
- python提供了許多`dbf`檔案格式的reader
  - 包括pandas即可直接讀取，[網友](https://stackoverflow.com/questions/41898561/pandas-transform-a-dbf-table-into-a-dataframe)也曾充分討論並速度評比，
  - 經測試，[simpledbf](https://pypi.org/project/simpledbf/)可以正確解讀[TEDS](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)之`.dbf`檔，具有簡捷之特性  

## 執行
- 用法：`dbf2csv.py TEDS11_AREA_WGS84.dbf`

## 程式說明
- 使用[simpledbf](https://pypi.org/project/simpledbf/)的`Dbf5`模組
- 有中文狀況會因`py27`/`py37`版本而有差異，須以嘗試錯誤法寫出
  - `py27`對寫出中文較寬鬆
  - `py37`須註明`coding`
- 寫出檔案(`TEDS11_AREA_WGS84.csv`共367萬筆)格式為csv，方便後續處理

```python
kuang@master /nas1/TEDS/teds11
$ cat dbf2csv.py
from simpledbf import Dbf5
from pandas import *
import sys
fname=sys.argv[1]
if 'dbf' in fname:
  fnameO=fname.replace('dbf','csv')
elif 'DBF' in fname:
  fnameO=fname.replace('DBF','csv')
else:
  sys.exit('name must contain dbf or DBF')
dbf = Dbf5(fname, codec='utf-8')
df = dbf.to_dataframe()
try:
  df.set_index(df.columns[1]).to_csv(fnameO,coding='utf8')
except:
  df.set_index(df.columns[1]).to_csv(fnameO)
```

## Reference
- Ryan Nelson, simpledbf 0.2.6, [pypi](https://pypi.org/project/simpledbf/), Released: May 14, 2015