---
layout: default
title:  EAC的時間標籤
parent: Dates and Times
grand_parent: Utilities
last_modified_date: 2022-06-07 17:06:31
tags: datetime
---

# EAC的時間標籤
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
## nc bytes to datetime

### reanalysis data

- [EAC4]()檔案基本上是個grib2檔案，即使經[ncl_convert2nc]()轉換了之後，雖為nc檔，然其架構內涵與WRF或者是IOAPI-m3.nc皆完全不同，需要特別處理。
- ncl_convert2nc會將EAC4檔案的時間標籤名稱命名為**initial_time0**，為一[時間、字串長]()之2維的字串陣列。
  - 字串共有**18**個字元
  - 樣式為*mm/dd/yyyy (hh:mm)*
  - 目標要轉成wrf格式`%m/%d/%Y (%H:%M)`
- 同樣先將個別**18**個byte轉成str，再連成字串、，最後再讀成datetime

```python
SDATE=[datetime.datetime.strptime(''.join([str(i, encoding='utf-8') for i in list(nc.variables[V[1][0]][t, :])]),\
 '%m/%d/%Y (%H:%M)') for t in range(nt)]
```
- 參考：[pr_GrbTime.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/DateTime/pr_GrbTime.py)

### forecast data

- CAMS預報場經ncl_conver2nc轉換後，並沒有initial_time的變數項，而是存在於每項污染濃度的屬性:`nc.variables[V[3][0]].initial_time`
- 因為該時間標籤已經是個string了，不需要再encoding 與join，直接進行轉換即可。指令：`bdate=datetime.datetime.strptime(''.join(nc.variables[V[3][0]].initial_time),'%m/%d/%Y (%H:%M)')`
- 該時間只是模式啟始時間，如要計算每個time frame的時間，另有變數(V[0])`forecast_time0`，為0 \~ 120的整數(單位為小時)，可供使用：`SDATE=[bdate+datetime.timedelta(hours=int(i)) for i in  nc['forecast_time0'][:].data]`

## datetime to nc bytes

- 目前尚未有應用之需求

## 直接開啟grib2檔案

- 使用pygrib模組來開啟：`grbs = pygrib.open(fname)`
- grib2檔案可能只有單一個timeframe(如CWB_WRF之結果檔)，要讀取所有內容才能決定。
  - grib2的record number序號是由1開始排序，長度為`grbs.messages`
  - 如每個record是不同時間框架(EAC4檔案)，validDate會有所不同。
- 檔案內有2個時間資訊
  - `grbs[1].anaDate`：為批次作業的啟始時間。
  - `grbs[1].validDate`：為該grib2檔案的時間框架。
  - 類型為datetime.datetime
  - 格式如：`2022-07-29 12:00:00`

```python
#!/cluster/miniconda/envs/gribby/bin/python
import sys
import pygrib
fname=sys.argv[1]
grbs = pygrib.open(fname)
dates=list(set([grbs[i].validDate for i in range(1,grbs.messages+1)]))
n=len(dates)
if n>1:
  dates.sort()
for i in range(n):
  print(i,dates[i])
```

## Reference
