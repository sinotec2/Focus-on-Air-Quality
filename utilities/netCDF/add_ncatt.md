---
layout: default
title: add_ncatt
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-06-29 15:47:38
tags: CAMx ptse emis uamiv
---

# 增添CAMx nc檔案所需之全域屬性
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
- CAMx過去很長一段時間是沿用[uamiv][uamiv]格式做為主要格式，其內容與CAMx程式之變數已有良好對應，特別是常數部分，前4筆表頭更是所有檔案(包括邊界[lateral_boundary][bnd]、點源[point_source][ptse]等格式)所通用。
- 其後CAMx增加了nc檔案讀寫的功能，過去這些常數則需以nc檔案的全域屬性方式進入程式。
- 因此必須在執行程式前進行確認，如有不足，則需予增添，以避免程式停擺。
- 由於這些屬性名稱在其他(如CMAQ)並未使用，因此也不致構成錯誤。

## 項目、範例及意義

|項目|CAMx|CMAQ|說明|
|:-:|:-:|:-:|:-:|
|pncgen 格式名稱|[lateral_boundary][bnd], [uamiv][uamiv], [point_source][ptse]|[ioapi][ioapi]|pncgen格式詳[ncgen & pncgen][Xncgen]|
|FTYPE|1(uamiv)|1或2|CMAQ以此辨識檔案性質1為一般4維檔、2為邊界3維檔|
|**NAME**或**CAMx_NAME**10字元|"BOUNDARY", "EMISSION", "AIRQUALITY", "PTSOURCE" "AVERAGE" |-|CAMx以此辨識檔案性質|
|ITZON|-8|-|CAMx以此計算太陽天頂角|
|IUTM|0|-|UTM zone。如非UTM系統給0即可|
|CPROJ|2|-|投影類別、即[GDTYP][GDTYP]|
|ISTAG|0|-|是否差格(風速)|
|PLON, PLAT, TLAT1, TLAT2|120.99, 23.61, 10.0, 40.0|-|蘭伯特投影參數|


## 有關全域屬性NAME或CAMx_NAME
- 7.10以前(不含7.10)舊版的CAMx模式在讀取nc檔案時，會嚴格檢查**NAME**全域屬性，以識別檔案的時間及屬性，需特別留意。
- 因應netCDF v4.6.2的進版，nc檔內不再能新增**NAME**(大寫)的全域屬性
  - 修改相關fortran程式碼，將大寫的**NAME**改成小寫*name*。
  - 使用舊版的netCDF與相依套件。RAMBOL公司[建議][oldnc]netCDF 4.6.1版
  - 將CAMx升級到7.10以上版本，屬性名稱**NAME**全數改成**CAMx_NAME**
  
- 修改程式或升級方案影響到的程式如下

```bash
kuang@master /cluster/src/CAMx/camx710
$ grep -n CAMx_NAME */*.f
DDM/ncf_rdbcddm.f:110:      this_var = 'CAMx_NAME'
DDM/ncf_rdicddm.f:98:      this_var = 'CAMx_NAME'
DDM/ncf_rdpthdr_ddm.f:106:      this_var = 'CAMx_NAME'
DDM/ncf_rdtcddm.f:110:      this_var = 'CAMx_NAME'
IO_NCF/ncf_areaprep.f:88:      this_var = 'CAMx_NAME'
IO_NCF/ncf_bndprep.f:83:      this_var = 'CAMx_NAME'
IO_NCF/ncf_cncprep.f:101:      this_var = 'CAMx_NAME'
IO_NCF/ncf_luseprep.f:72:      this_var = 'CAMx_NAME'
IO_NCF/ncf_metprep.f:84:      this_var = 'CAMx_NAME'
IO_NCF/ncf_metprep.f:112:      this_var = 'CAMx_NAME'
IO_NCF/ncf_metprep.f:140:      this_var = 'CAMx_NAME'
IO_NCF/ncf_rdpthdr.f:87:         this_var = 'CAMx_NAME'
IO_NCF/ncf_topprep.f:83:      this_var = 'CAMx_NAME'
IO_NCF/ncf_wrt_global.f:234:      ierr = nf_put_att_text(iounit, NF_GLOBAL, 'CAMx_NAME',
OSAT/ncf_rdpthdr_sa.f:92:         this_var = 'CAMx_NAME'
RTRAC/ncf_empreprt.f:100:      this_var = 'CAMx_NAME'
RTRAC/ncf_empreprt.f:135:      this_var = 'CAMx_NAME'
RTRAC/ncf_rdbcrt.f:126:      this_var = 'CAMx_NAME'
RTRAC/ncf_rdicrt.f:111:      this_var = 'CAMx_NAME'
RTRAC/ncf_rdpthdr_rt.f:92:      this_var = 'CAMx_NAME'
```
 

## add_ncatt.cs

{% include download.html content="[add_ncatt.cs](https://github.com/sinotec2/Focus-on-Air-Quality/tree/main/utilities/netCDF/add_ncatt_cs)" %}


## Reference
- sinotec2, [CAMx(UAM)的檔案格式](https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式), 2022/3/19 rev.

[uamiv]: <https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式> "CAMx所有二進制 I / O文件的格式，乃是遵循早期UAM(城市空氣流域模型EPA，1990年）建立的慣例。 該二進制文件包含4筆不隨時間改變的表頭記錄，其後則為時間序列的數據記錄。詳見CAMx(UAM)的檔案格式"
[bnd]: <https://sinotec2.github.io/FAQ/2022/06/27/CAMx_BC.html#uamiv與lateral_boundary格式內容之比較> "uamiv與lateral_boundary格式內容之比較"
[ptse]: <https://sinotec2.github.io/Focus-on-Air-Quality/CAMx/> "needs
 edit"
[ioapi]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ioapi/> "I/O API(Input/Output Applications Programming Interface)是美國環保署發展Models-3/EDSS時順帶產生的程式庫(cmascenter, I/O API concept)，用來快速存取NetCDF格式檔案，尤其對Fortran等高階語言而言，是非常必須之簡化程序。"
[Xncgen]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pncgen/#camx> "ncgen & pncgen"
[oldnc]: <https://camx-wp.azurewebsites.net/download/netcdf/> "Build netCDF v4.6.1 from Source"
[GDTYP]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/#map-projection-type> "Map projection type"