---
layout: default
title: SMOKE
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 1
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
tags: CMAQ nchc_service
---

# SMOKE
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
- 

## 面源
- 公版模式目前僅釋出3個面源檔案
  - 所有高空污染也以高空網格排放形式，儲存在面源檔案中
  - 24層排放量中，僅0-8有數值，其餘皆為0

|類別|時間|檔名|層數|merged|
|-|-|-|-|-|
|生物源|Jul 18  2021|b3gts_l.20181225.38.d4.ea2019_d4.ncf|1|-|
|基準排放量|Feb 10 2022|cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf|24|yes|
|grid09內插排放量(差值)|Aug 24 2021|egts_l.20181225.38.d4.ea2019_d4.ncf|9|yes|

- 即使經merge後的排放檔案，也有下列版本的差異
```bash
<
/VERSION/ SMOKEv4.7_
/NUMBER OF VARIABLES/  53  ;
---
>
/VERSION/ SMOKEv4.7_                                                            Data interpolated from grid \"Taiwan09\" to grid \"Taiwan03\"
/NUMBER OF VARIABLES/  36" ;
```
---

曠博筆記
https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/

--------------------------
登入台灣杉三號(以下都在台灣杉三號執行)
/home/帳/

--------------------------
新增污染源排放量檔案
cd ~/work/SMOKE-TW/02RunSMOKE/data/run_NewEms/output/merge/2019-01
mv ./cmaq_cb06r3_ae7.01-20181225.38.TW3-d4.NewEms.ncf /work/帳/

連結到工作目錄下
cd ~/download/model/cmaq_recommend/work/2019-01/grid03/smoke
ln -sf /work/帳/*.ncf .

--------------------------
設定模式讀取的輸入檔路徑

vi ~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.raw/run.cctm.03.csh

在set sourcefile下面增加
setenv LD_LIBRARY_PATH /opt/ohpc/Taiwania3/libs/Iimpi-2021/hdf5-1.12/lib:/opt/ohpc/Taiwania3/libs/Iimpi-2021/szip-2.1.1/lib:/opt/ohpc/Taiwania3/libs/Iimpi-2020/pnetcdf-1.12.2/lib:/opt/ohpc/Taiwania3/pkg/cmp/compilers/intel/compilers_and_libraries_2017.7.259/linux/compiler/lib/intel64_lin:/opt/ohpc/Taiwania3/libs/Iimpi-2021/netcdf-4.7.4/lib:/opt/ohpc/Taiwania3/libs/libfabric/1.11.2/lib
set CMAQ_HOME = /home/帳/download/model/cmaq_recommend
set compilerString = intel

修改讀取的排放量檔案數量及名稱
setenv N_EMIS_GR 4
setenv GR_EMIS_001    ${cmaqproject}/smoke/b3gts_l.20181225.38.d4.ea2019_d4.ncf
setenv GR_EMIS_002    ${cmaqproject}/smoke/cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf
setenv GR_EMIS_003    ${cmaqproject}/smoke/egts_l.20181225.38.d4.ea2019_d4.ncf
setenv GR_EMIS_004    ${cmaqproject}/smoke/cmaq_cb06r3_ae7.01-20181225.38.TW3-d4.NewEms.ncf

setenv GR_EMIS_LAB_001  biotaiwan
setenv GR_EMIS_LAB_002  tedstaiwan
setenv GR_EMIS_LAB_003  eataiwan
setenv GR_EMIS_LAB_004  newems

修改模擬輸出檔case名稱，原Cont改為Case
set myjob   = CaseEms

--------------------------
修改combine.sh

cd ~/download/model/cmaq_recommend/POST/combine
vi combine.sh

修改1處，原Cont改為Case
export outpath=/home/帳/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms/

--------------------------
模擬全月(loop)

起迄時間改為全月
vi ~/download/model/cmaq_recommend/work/2019-01/project.config

修改loop.sh
cd ~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.raw
vi loop.sh

修改4處，原Cont改為Case
cgfile=~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms/daily/CCTM_CGRID_v532_intel_Taiwan_$ymd.nc
cd ~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms/daily
cgfile=~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms/daily/CCTM_CGRID_v532_intel_Taiwan_$ymd.nc
cd ~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms/daily

執行前先刪除舊檔
rm -rf ~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms
rm -f ~/download/model/cmaq_recommend/POST/combine/*.nc

執行
./loop.sh

跑完全月後可以刪除檔案，節省硬碟空間
rm -rf ~/download/model/cmaq_recommend/work/2019-01/grid03/cctm.CaseEms

--------------------------
整併檔案(全月)

cd ~/download/model/cmaq_recommend/POST/combine

合併每日output檔為全月
(公版將前一月份多跑的幾天也合併進來)
ncrcat 201812*.conc.nc 201901*.conc.nc c-v1.2019-01.conc.nc

目前公版(2022/5/3版本)不用做output檔壓縮
故ncrcat -4 --cnk_map nc4 --cnk_plc all -L3這條指令省略

移到其他地方以節省硬碟空間，例如
mv ./*.nc /work/帳/

--------------------------
下載回公司機器

登入公司master

mkdir -p /nas2/公司帳號/cmaq

從台灣杉三號拷貝output檔到公司機器
scp 帳@twnia3.nchc.org.tw:/work/帳/*2019-01.conc.nc /nas2/公司帳號/cmaq/
