---
layout: default
title: Elev. Point Sources
parent: CMAQ Models
nav_order: 7
has_children: true
permalink: /GridModels/PTSE/
date:               
last_modified_date:   2021-12-02 11:08:53
---

# 高空點源排放檔案
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
- CMAQ高空排放檔案與CAMx最大不同在於不隨時間改變的排放條件(HDTVXY)是另成一檔儲存。可能是為減少檔案的大小，然CMAQ此舉增加很多錯誤的機會。
  - 常數部分：以[pt_const.py](https://github.com/sinotec2/cmaq_relatives/blob/master/ptse/pt_const.py)轉接CAMx格式之REAS與TEDS點源數據
  - 時間變化部分：以[pt_timvar.py]()，逐月轉換後再以[brk_day2.cs](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/brk_day/)裁剪成逐日檔案

## [pt_const.py](https://github.com/sinotec2/cmaq_relatives/blob/master/ptse/pt_const.py)

## [pt_timvar.py](https://github.com/sinotec2/cmaq_relatives/blob/master/ptse/pt_timvar.py)
### I/O Files
- 點源時變部分的模版
  - 參考USEPA提供的[標竿檔案包](https://gaftp.epa.gov/exposure/CMAQ/V5_3_2/Benchmark/CMAQv5.3.2_Benchmark_2Day_Input.tar.gz.list)
  - 其中的inln_mole_ptnonipm_20160701_12US1_cmaq_cb6_2016ff_16j.nc檔案做模版
  - 由於每月運轉中的點源個數不同，因此每次須執行[ncks -d](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncks/#維度剪裁)指令，裁剪出正確長度的模版。
  - 下載須指定`--no-check-certificate `：
  ```bash
  wget--no-check-certificate  https://gaftp.epa.gov/exposure/CMAQ/V5_3_2/Benchmark/CMAQv5.3.2_Benchmark_2Day_Input.tar.gz
  ```  
- CAMx逐月點源排放量。可能是6版之前的[point_source]()格式，也可能是nc檔格式(7版以後)，
- REAS逐月點源排放量：csv格式
- 程式將會產生teds*TT*.*YYMM*.timvar.nc
  - *TT*：TEDS版本
  - *YYMM*：年月

### Arguments
- CAMx逐月點源排放量檔案名稱

### 程式說明
#### 輸入檔格式
- 範例為uamiv [point_source]()格式之CAMx逐月檔案，因此需要PseudoNetCDF來解讀
  - 如為nc檔案，則以netCDF4.Dataset讀取。
```python
import PseudoNetCDF as pnc
...
pt=pnc.pncopen(sys.argv[1],format='point_source')
```


## Reference


