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
- inputs and model sources

```bash
#sinotec2@clogin2 /work1/simenvipub01/download
#$ tree
.
├── input
│   ├── 201901.tar.xz
│   ├── 201902.tar.xz
...
│   └── 201912.tar.xz
└── model
    ├── cmaq_recommend.tar.xz
    ├── output_cctm_combine
    │   ├── nohup.out
    │   ├── v4.2019-01.conc.nc
    │   ├── v4.2019-02.conc.nc
...
    │   └── v4.2019-12.conc.nc
    └── post_process.tar.xz

3 directories, 27 files
#sinotec2@clogin2 /work1/simenvipub01/download
#$ du -ach|tail -n1
229G    total
```

## Inputs
- input tree

```bash
#kuang@DEVP /nas2/cmaq2019/download/input/201901/grid03
#$ tree |grep -v CTM
.
|-- bcon
|   `-- BCON_v532_Taiwan_2018359
|-- icon
|   `-- ICON_v532_Taiwan_2018359
|-- mcip
|   |-- GRIDBDY2D_Taiwan.nc
|   |-- GRIDCRO2D_Taiwan.nc
|   |-- GRIDDESC
|   |-- GRIDDOT2D_Taiwan.nc
|   |-- LUFRAC_CRO_Taiwan.nc
|   |-- METBDY3D_Taiwan.nc
|   |-- METCRO2D_Taiwan.nc
|   |-- METCRO3D_Taiwan.nc
|   |-- METDOT3D_Taiwan.nc
|   `-- SOI_CRO_Taiwan.nc
|-- ocean
|   `-- ocean.ncf
`-- smoke
    `-- cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf
```
### ICBC
```bash
#kuang@master /nas2/cmaq2019/download/input/201901/grid03
#$ ll icon/*9 bcon/*9
kuang@DEVP /nas2/cmaq2019/download/input/201901/grid03
$ ll icon/*9 bcon/*9
-rwxr-xr-x. 1 kuang SESAir 8678823188 Feb 25 15:00 bcon/BCON_v532_Taiwan_2018359
-rwxr-xr-x. 1 kuang SESAir  254605196 Feb 25 14:21 icon/ICON_v532_Taiwan_2018359
```

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
### 日期個案管理project.config
- [project.config](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/exec/#2-模擬案例與時間projectconfig)是公版CCTM執行腳本中3者其一，為設定個案起迄日期條件之腳本。更動此腳本內容，還需有配套動作，在此詳述。
- 何時會需要修改個案起迄日期
  - 電腦資源限制、分段執行
  - 電腦執行過程被迫中斷、重啟執行
  - 針對高濃度事件期間進行分析
  - 其他理由
- 起始日期
  - MCIP_START(eg `2018-12-25-00:00:00.0000`)：無需更動，CCTM會自全月檔案中尋找需要的開始時間
  - cmaqbcdate(eg `2018359`)：同樣也無需更動
  - cmaqicdate(eg `2019002`)
    - 因為只有單一個小時，內容為前日23時結束時所有項目的模擬值
    - 需要連結CCTM_CGRID檔案，範例如下(將**CCTM_CGRID**...20190101連結至**ICON**...20190102)

```bash
ln -s ${project.config}/${mydomain}/cctm.${myjob}/daily/CCTM_CGRID_v532_intel_Taiwan_20190101.nc ${cmaqproject}/${mydomain}/icon/ICON_v532_Taiwan_2019002
```  
- 結束日期
  - runlen：(單位為MMSS，840小時為**840**0000)
  - END_DATE(eg. `2019-01-31`)
  - 此二者取交集(較小值)

- 起迄小時：因公版模式還是維持以日為單位進行CCTM模擬，因此起迄時間均為UTC之0時。**不建議更動**以避免錯誤。
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
- 輸出(379G、最少CCTM_A*需33G)、後處理(1.6G)約需381G
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
