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
- 化學社區大氣模型 (CAM-chem) 是 NCAR 社區地球系統模型 (CESM) 的一個組成部分，用於模擬全球對流層和平流層大氣成分。 
- CAM-chem 使用 MOZART 化學機制，對流層和平流層化學具有多種複雜性選擇。 
  - CAM-chem 的初始版本可參考Lamarque 等人(2012)。 
  - 用於 CCMI 和 HTAP 的 CAM-chem版本可參考Tilmes 等人(2016)。
  - Tilmes 等人描述了 CESM1.2 中的 CAM-chem。 (2015)。

## 下載
- 與前述[MOZART](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/MOZART/)一樣，[下載網址](https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)略有不同( https://www.acom.ucar.edu/cam-chem/cam-chem.shtml)
![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cam-chem_download.png)
- CAM-chem有段時間提供全年檔案下載。2021年後因管理政策改變，鼓勵使用者直接上機檢視模擬結果，甚至鼓勵在本地工作站自行模擬，因此再沒有提供全年、全球檔案下載。


## Reference
- WEG Administrator, **Welcome to the CAM-chem Wiki**,[wiki.ucar](https://wiki.ucar.edu/display/camchem/Home),13 Jun 2021
- wiki, **MOZART (model)**, [wikipedia](https://en.wikipedia.org/wiki/MOZART_(model)),last edited on 6 May 2021
- acom.ucar, **Mozart Download**, [ucar.edu](http://www.acom.ucar.edu/wrf-chem/mozart.shtml), 2013-08-30.