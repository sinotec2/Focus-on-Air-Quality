---
layout: default
title:  EAC的時間標籤
parent: Dates and Times
grand_parent: Utilities
last_modified_date: 2022-06-07 17:06:31
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

## datetime to nc bytes
- 目前尚未有應用之需求

## Reference
