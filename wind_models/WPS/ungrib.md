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
  - 不過也需要持平來評估JPEG2000這件事，jasper2並不是個廢棄的版本，2年前還有更新的版本，似乎是個平行發展的性質。
- jasper如果要用brew退版次、brew同時安裝jasper@2，也都不可能，只能用[macport](https://www.macports.org/)另外安裝。

## 規格及環境設定

### 環境設定

- gcc與gfortran，需要是同一版本。
- netcdf及netcdff程式庫，可以是最新的版本。
- 會需要libpng與open_jpeg，此二者也可以接受最新的版本。
- jasper2、以macport install jasper2 安裝。參考[Library for manipulating JPEG-2000 images](https://ports.macports.org/port/jasper2/)
  - 最新的jasper4 與openjpeg 不相容。而後者是ungrib 必須安裝。

### 規格選定

- 選定OS以及編譯器種類
- 如果是最新版本的gcc與gortran， 因新版對程式碼的要求較為嚴格，要記得加上allow mismatch 、或是std等等。
- 必要時修改config.wps 內容、以避免發生行動力與影響力。

### jasper2的安裝與連結

- macport安裝指令如下(參考[Library for manipulating JPEG-2000 images](https://ports.macports.org/port/jasper2/))

```bash
sudo port install jasper2
```

- 安裝好的程式庫並不會在Cellar下，而是在`/usr/lib`下。需要另外連結。
