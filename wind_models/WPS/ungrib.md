---
layout: default
title: grib2檔案之讀取
parent: "WPS"
grand_parent: "WRF"
nav_order: 6
date:               
last_modified_date: 2024-07-20 09:13:39
tags: CWBWRF landuse wrf WPS
---

# ungrib

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

- ungrib拖到這麼晚才寫下這篇筆記，因為軟體系統進步太快、編譯遭遇困難，2019～2021年之後就沒有更新。有賴GPT的提醒，JPEG2000與新版jasper不相容的問題才有所覺醒，順利突破編譯、重新上線。
  - jasper目前已經進到4.2.4版，WPS雖然也有持續進步（見[wrf-model/WPS@github](https://github.com/wrf-model/WPS/tree/master)），ungrib似乎沒有太大的進步，還是使用JPEG2000來解壓縮。
- jasper如果要用brew退版次、同時安裝jasper@2，也都不可能，只能用macport另外安裝。
