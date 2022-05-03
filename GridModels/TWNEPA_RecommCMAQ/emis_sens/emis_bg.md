---
layout: default
title: 背景說明
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 1
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 背景說明
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
- CCTM可以接受重疊之排放量檔案
- 公版模式目前並未提出具系統性之排放量組合。似必須待其公開SMOKE方能一致化。

## 面源

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

