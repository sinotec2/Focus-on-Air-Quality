---
layout: default
title: 輸出入檔案及傳輸
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 2
date: 2023-02-20
last_modified_date: 2023-03-23 11:46:30
tags: CMAQ nchc_service
---

# 公版模式輸入輸出檔案及傳輸管理
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
 setenv GR_EMIS_003    ${cmaqproject}/smoke/egts_l.20181225.38.d4.ea2019_d4.ncf

 setenv GR_EMIS_LAB_001  biotaiwan
 setenv GR_EMIS_LAB_002  tedstaiwan
 setenv GR_EMIS_LAB_003  d3_to_d4
...
```

### 氣象檔案

- 版本
  - 2022/2/10
  - WRF ARW V3.8.1
- 全月(自前月25日起)合併成一個檔案
- 24層高度(海上為例)

      [   40.546402,    81.18201 ,   162.81754 ,   327.71338 ,
         579.40753 ,   750.26733 ,   923.67737 ,  1278.5795  ,
        1592.402   ,  1909.9487  ,  2231.2837  ,  2847.8464  ,
        3487.8079  ,  4750.3086  ,  6017.6245  ,  7289.3013  ,
        8589.708   ,  9896.907   , 11196.109   , 13107.695   ,
       14985.391   , 16782.564   , 18600.848   , 20403.428   ]


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
    - 需要連結CCTM_CGRID檔案，範例如下(將**CCTM_CGRID**...2019**0101**連結至**ICON**...2019**002**)
    - 注意：CCTM_CGRID的日期型式為%Y%m%d，ICON為%Y%J

```bash
ln -s ${project.config}/${mydomain}/cctm.${myjob}/daily/CCTM_CGRID_${CAS}_20190101.nc ${cmaqproject}/${mydomain}/icon/ICON_${CAS}_2019002
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

## 檔案傳輸方案

### scp

- 傳統的scp會需要OTP，不適合自動化傳送。
- 有最快的速度，適合大型檔案的傳送。
- 建議還是需要先壓縮後再傳送

### s3fs

- 雖然官方提供了好幾個設置網路磁碟機的說明檔案(包括aws s3、google drive等等)，但雲端並非專用，能夠用到的頻寬非常有限，檔案傳送的速度非常慢。只能適用小型檔案。
- 詳NCHC[利用 s3fs 掛載 S3 bucket 儲存使用說明](https://iservice.nchc.org.tw/download_file.php?f=BKLavuxfqIbbhpoWDidwFNkhwCvMFdKZFi5R94gI_b2NmqXxUH5S59lqbpAsUptGNdOMn6RLqs3mDwkFqjbo0g)
- ~/.aws/credential檔案的設法，可以參考[AWS Command Line Interface -> User Guide for Version 2](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

### git

- 國網環境中提供了git指令，經測試與github之間的聯繫還算正常速度，也沒有額外的安全需求。
- 如果模擬可以簡化到圖檔層次，建議可以採用git方式直接上傳。