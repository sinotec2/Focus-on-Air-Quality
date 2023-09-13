---
layout: default
title:  surf_trajLL2
parent: CGI-pythons
grand_parent: Utilities
date: 2022-06-07
last_modified_date: 2023-01-13 16:34:59
tags: trajectory CWBWRF CGI_Pythons NCL
---

# 地面2維軌跡線計算服務
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

> 這個服務網頁提供最近5日北、中、嘉、高等4處的反軌跡(中央氣象局WRF_3km預報數據、後修正以GFS 10天預報及降尺度WRF執行結果)、以及歷年地面測站觀測數據計算之正/反軌跡。

- 服務網頁位址：[http://125.229.149.182/traj2.html](http://125.229.149.182/traj2.html)
- python程式[下載](./surf_trajLL2.py)。不同版本說明與修改細節詳見[內網版本與新增功能](../../TrajModels/ftuv10/4.daily_traj%40ses.md)
- 軌跡計算詳見[ftuv10](../../TrajModels/ftuv10/ftuv10.md)
- 呼叫程式
  - [traj2kml.py](../../wind_models/CODiS/5.traj.md)
  - [ftuv10.py](../../TrajModels/ftuv10/ftuv10.md)
  - [ncl](../Graphics/NCL/)

{% include download.html content="[臺灣地區高解析度軌跡產生/自動分析系統cgi程式](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/surf_trajLL2.py)" %}