---
layout: default
title: 輸入輸出檔案管理
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 2
date: 2022-04-18 09:28:55
last_modified_date: 2022-04-18 09:28:58
---

# 公版模式輸入輸出檔案管理
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

## Inputs
- input tree

```bash
#kuang@DEVP /nas2/cmaq2019/download/input/201901/grid03
#$ tree bcon icon mcip ocean smoke
```

    bcon
    `-- BCON_v532_Taiwan_2018359
    icon
    `-- ICON_v532_Taiwan_2018359
    mcip
    |-- GRIDBDY2D_Taiwan.nc
    |-- GRIDCRO2D_Taiwan.nc
    |-- GRIDDESC
    |-- GRIDDOT2D_Taiwan.nc
    |-- LUFRAC_CRO_Taiwan.nc
    |-- METBDY3D_Taiwan.nc
    |-- METCRO2D_Taiwan.nc
    |-- METCRO3D_Taiwan.nc
    |-- METDOT3D_Taiwan.nc
    `-- SOI_CRO_Taiwan.nc
    ocean
    `-- ocean.ncf
    smoke
    `-- cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf


### 排放量檔案
- 版本：2022/2/10
- 應有Base及b3gts，但似乎只有一個，且造成山區VOCs的顯著差異，應為生物源

```bash
# ~/download/input/201901/grid03/smoke
-rwxr-xr-x 1 sinotec2 TRI1111114 1.2G Feb 10 11:07 cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.tar.gz
# ~/cmaq_recommend/work/2019-01/grid03/cctm.raw
#$ more run.cctm.03.csh
...
 setenv N_EMIS_GR 2
 setenv GR_EMIS_001    ${cmaqproject}/smoke/b3gts_l.20181225.38.d4.ea2019_d4.ncf
 setenv GR_EMIS_002    ${cmaqproject}/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.ContEms.ncf

 setenv GR_EMIS_LAB_001  biotaiwan
 setenv GR_EMIS_LAB_002  tedstaiwan
...
```
- 

### 氣象檔案
- 版本
  - 2022/2/10
  - WRF ARW V3.8.1
- 全月(自前月25日起)合併成一個檔案
- 24層高度(海上)


      [  19.973816,    59.98133 ,   120.13907 ,   241.18448 ,
        445.79684 ,   739.0711  ,  1085.8995  ,  1490.2742  ,
        1962.2716  ,  2458.058   ,  2978.798   ,  3527.9873  ,
        4110.1367  ,  4729.7773  ,  5390.418   ,  6097.217   ,
        6859.475   ,  7688.0864  ,  8595.766   ,  9601.749   ,
      10733.327   , 12030.674   , 13558.192   , 15437.946   ]


```bash
# ~/download/input/201901//grid03/mcip
-rwxr-xr-x 1 sinotec2 TRI1111114 1000K May 31  2021 LUFRAC_CRO_Taiwan.nc
```

## Results
- 似非連續批次完成

```bash
#sinotec2@clogin2 /work1/simenvipub01/download/model/output_cctm_combine
-rwxrwxr-x 1 simenvipub01 TRI111490 4.8G Feb 16 21:34 v4.2019-05.conc.nc
-rwxrwxr-x 1 simenvipub01 TRI111490 4.7G Feb 24 15:48 v4.2019-01.conc.nc
-rwxrwxr-x 1 simenvipub01 TRI111490 4.7G Feb 24 16:02 v4.2019-12.conc.nc
-rw------- 1 simenvipub01 TRI111490   19 Apr  6 14:57 nohup.out
```
- 似缺少生物源排放量

| ![Old-New_dVOCs.gif](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/Old-New_dVOCs.gif) |
|:--:|
| <b>重跑第1日與下載output的差值(VOC_logPPBC)</b>|



## 磁碟機空間估算
- 一個月輸入30G
- 輸出(379G)、後處理(1.6G)約需381G
- 合計約411G
- 可減至131G


```bash
#kuang@DEVP /nas2/cmaqruns/2019force/output/2019-01/grid03
#$ du_lsd .
8.1G    ./bcon/
287G    ./cctm.ContEms/
486M    ./icon/
26G     ./mcip/
148K    ./ocean/
59G     ./smoke/
```
- 單一個案、12個月估計：最大約需4.5T，至少1.5T
