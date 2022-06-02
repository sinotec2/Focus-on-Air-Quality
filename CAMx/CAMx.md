---
layout: default
title: CAMx System
nav_order: 10
has_children: true
permalink: /CAMx/
last_modified_date: 2022-06-01 20:12:23
---

# Comprehensive Air Quality Model with Extensions(CAMx)

- 這裡說明Ramboll公司持續發展的[CAMx](https://www.camx.com/about/)，其模式系統的運作方式，包括氣象前處理、BC/IC、排放檔案、後處理等。
- 早先在Github公開了CAMx前後處理的fortran版本，但因為期間CAMx更新太多版本、後又引入ncf的IO，fortran版本無法持續發展下去，相關程式就陸續移到python平台上作業。
- 雙C模式的比較可以看[CAMx vs CMAQ@FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/Models/CAMx_vs_CMAQ/)這篇的回顧分析。

## 官方網站與手冊
### 程式碼與作業方式
- 相較CMAQ或WRF而言，CAMx的程式碼相對單純很多。
- 作業平台
  - CAMx不會讀取系統的環境變數，對記憶體、硬碟IO空間的需求也不是很大，因此從PC、macOS一直到工作站、cluster、超級電腦都可以適用。
- 多工方案
  - 可以使用[SMP](https://zh.wikipedia.org/wiki/对称多处理)或[DMP](https://en.wikipedia.org/wiki/Distributed_memory)多工執行，
  - 不過經測試結果：分月在不同機器、單月以[SMP]()方式是目前執行全年專案最有效率的組合。
- 

### [官網](https://www.camx.com/download/support-software/)前處理程式

|名稱|年代版本|用途|FAQ|
|-|-|-|-|
|BNDEXTR|[20sep16](https://camx-wp.azurewebsites.net/getmedia/bndextr.20sep16.tgz)|從空品濃度檔案(uamiv)切割出下層網格之邊界濃度檔案|BC|
|GEOS2CAMx|[30apr22](https://camx-wp.azurewebsites.net/getmedia/geos2camx.30apr22.tgz)|[GEOS]()模式之轉接|IC/BC|
|MOZART2CAMx |[6apr22](https://camx-wp.azurewebsites.net/getmedia/mozart2camx.6apr22.tgz)|[MOZART]()模式之轉接(for CAMx or CMAQ)|IC/BC|
||[30apr22](https://camx-wp.azurewebsites.net/getmedia/mozart2camx.30apr22.tgz)|(for CAMx v7+)||
|O3MAP|[20sep16](https://camx-wp.azurewebsites.net/getmedia/o3map.20sep16.tgz)|垂直臭氧柱檔案之轉接(for CAMx v6.0-v6.5)|o3map|
||[31may20](https://camx-wp.azurewebsites.net/getmedia/o3map.31may20.tgz)|(for CAMx v7+)||
|TUV v4.8|[8apr16](https://camx-wp.azurewebsites.net/getmedia/tuv4.8.camx6.30.8apr16.tgz)|光解常數的函數(for CAMx v6.3-v6.5)|tuv|
||[31may20](https://camx-wp.azurewebsites.net/getmedia/tuv4.8.camx7.00.31may20.tgz)|(for CAMx v7.00)||
||[15dec20](https://camx-wp.azurewebsites.net/getmedia/tuv4.8.camx7.10.15dec20.tgz)|(for CAMx v7.10)||
||[30apr22](https://camx-wp.azurewebsites.net/getmedia/tuv4.8.camx7.20.30apr22.tgz)|(for CAMx v7.10)||
|WRFCAMx|[v4.8.1.14Dec20](https://camx-wp.azurewebsites.net/getmedia/wrfcamx_v4.8.1.14Dec20.tgz)|氣象場之轉接(uamiv)|wrfcamx|
||[v5.2.10Jan22](https://camx-wp.azurewebsites.net/getmedia/wrfcamx_v5.2.10Jan22.tgz)|(ncf)||

### [後處理程式](https://www.camx.com/download/support-software/)

|名稱|年代版本|用途|FAQ|
|-|-|-|-|
|CAMx2IOAPI |[camx2ioapi.8apr16.tgz](https://camx-wp.azurewebsites.net/getmedia/camx2ioapi.8apr16_1.tgz)|uamiv avrg/dep to ncf||

### 手冊
- [CAMxUsersGude_v7.20.pdf](http://camx-wp.azurewebsites.net/Files/CAMxUsersGuide_v7.20.pdf)
- [扩展的综合空气质量模型CAMxv630簡體手冊](http://www.camx-model.cn/docs/CAMx用户手册v630.pdf)

{: .fs-6 .fw-300 }
---


