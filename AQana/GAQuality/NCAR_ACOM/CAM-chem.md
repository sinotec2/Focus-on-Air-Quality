---
layout: default
title: "CAM-chem"
parent: "Global AQ Data Analysis"
grand_parent: "AQ Data Analysis"
nav_order: 2
date: 2021-12-12 16:29:18              
last_modified_date:   2021-12-12 16:29:14
---

# CAM-chem模式結果之讀取及應用
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

## 前言
- 社群大氣化學模式 (Community Atmosphere Model with Chemistry， [CAM-chem][CAM-chem]) 是 NCAR 社群地球系統模型 (CESM) 的一部分，用於模擬全球對流層和平流層大氣成分。 
- CAM-chem 使用 MOZART 化學機制，對流層和平流層化學具有多種複雜性選擇。 為美國大氣研究學界(UCAR)建議的全球模式結果，解析度1.25度X0.94度。 
  - CAM-chem 的初始版本可參考Lamarque 等人(2012)。 
  - 用於 CCMI 和 HTAP 的 CAM-chem版本可參考Tilmes 等人(2016)。
  - Tilmes 等人描述了 CESM1.2 中的 CAM-chem。 (2015)。

[CAM-chem]: <https://wiki.ucar.edu/display/camchem/Home> "The Community Atmosphere Model with Chemistry (CAM-chem) is a component of the NCAR Community Earth System Model (CESM) and is used for simulations of global tropospheric and stratospheric atmospheric composition."

## 下載
- 與前述[MOZART](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/MOZART/)一樣，[下載網址](https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)略有不同( https://www.acom.ucar.edu/cam-chem/cam-chem.shtml，提供2001/1~半年前的模擬（再分析）結果。
- 
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cam-chem_download.png)

- CAM-chem有段時間提供全年、全球範圍的模擬結果檔案下載。
  - 網址為：https://www.acom.ucar.edu/cam-chem/DATA/${Y}/fmerra.2.1003.FCSD.f09.qfedcmip.56L.001.cam.h1.${YMD}-${tail}.nc 

```bash
tail='00000'
test $Y -eq '2017' && tail='21600'
```
  - 2021年後因管理政策改變，鼓勵使用者直接上機檢視模擬結果，甚至鼓勵在本地工作站自行模擬，因此再沒有提供全年、全球檔案下載。


## CAM-chem的成分
CAM模式與CMAQ模式成分對照如下表：

![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CAM-chemSpec.png)

## Reference
- WEG Administrator, **Welcome to the CAM-chem Wiki**,[wiki.ucar](https://wiki.ucar.edu/display/camchem/Home),13 Jun 2021
- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.
