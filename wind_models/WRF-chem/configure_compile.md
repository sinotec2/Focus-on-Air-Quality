---
layout: default
title: 配置及編譯
parent: WRF-chem
grand_parent: "WRF"
nav_order: 1
date: 2021-12-27 16:53:48
last_modified_date: 2021-12-27 16:53:42
---

# WRF-chem 的配置及編譯 

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
- 基本上**WRF-chem**的配置與**WRF**沒有差異，需要netCDF、HD5、JASPER、Z等程式庫及包括檔。
- 唯一差異是必須開啟**chem**相關的環境變數

```bash
setenv EM_CORE 1
setenv WRF_CHEM 1
```

## WRF-chem程式碼之下載
- 雖然WRF4.3壓倒性檔目錄下有`chem`，然其檔案並非最新。



## Reference
