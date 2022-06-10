---
layout: default
title: calpuff遠端計算
nav_order: 5
parent: CALPUFF
grand_parent: Trajectory Models
last_modified_date: 2022-06-11 00:15:47
---

# calpuff遠端計算系統之實現
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
- calpuff執行會需要地形、氣象、臭氧濃度與排放等前處理，雖然目前有[calwrf](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALMET/calwrf/)的轉接，可以減省很多整併的工作，但也僅限地形與氣象部分。其他項目還是得一一解決(詳[calpuff.inp](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/calpuff_inp/))。
- 因為calpuff程式並沒有平行計算的設計，執行會需要較長時間，這是遠端計算系統困難的地方。其他困難還包括：
  - 氣象檔非常龐大，該如何提供？
  - 結果檔案即使以[con2nc](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2nc/)處理成nc檔案，可以用VERDI開啟，依然不是馬上可以檢視結果。後處理還有待提升。

### [CPUFF721遠端計算服務](http://114.32.164.198/CALPUFF.html)
- 位置:[http://114.32.164.198/CALPUFF.html](http://114.32.164.198/CALPUFF.html)
- 畫面

| ![CALPUFF_remote.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_remote.PNG)|
|:-:|
| <b>CPUFF721執行進度網頁畫面</b>|

### 檔案系統架構
- HTML
  - $web/[CALPUFF.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/CALPUFF.html)
    - 開啟檔案(使用者提供的[calpuff.inp](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/calpuff.inp))
      - 使用者只能修改點源排放相關設定
    - 呼叫CGI-PY：CALPUFF.py或demo.py
  - $web/cpuff_results/demo/[autorefreash.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/autorefresh.html)：每10秒報告cpuff、或m3nc2gif.py的執行進度、連結到工作站整體模式運作情況網頁[status.html](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/HTML/status/)
  - $web/cpuff_results/demo/[done.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/done.html)：執行停止的結果畫面
  - [$web/cpuff_results/demo/cpuff_gifs.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/cpuff_gifs.html)：模擬結果之gif檔案。

- CGI-PY
  - $cgi/calpuff/[CALPUFF.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/calpuff.py)：啟動cpuff主程式、啟動監看程式waitc.cs
  - $cgi/calpuff/[demo.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/demo.py)：檢視$web/cpuff_results/demo目錄下之文件。
- EXE
  - calpuff主程式：`CPUFF='/Users/cpuff/src/CALPUFF_v7.2.1_L150618/cpuff721 &> /dev/null 2>&1'`
  - 監看程式：`WAITC=WEB+'/cpuff_results/waitc.cs'`。cpuff執行完之後會接續執行：
    - [calpuff.con轉nc檔案](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPOST/con2nc/)：`/Users/cpuff/src/CALPOST_v7.1.0_L141010/con2nc >& con2nc.out`
    - [將nc檔案讀出寫成gif檔案](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python/4.m3nc2gif)：`../demo/m3nc2gif.py cpuff.nc >& con2nc.out`


## 結果畫面與連結

### 檔案連結

```
pid= 77547(check progress)
Model_results:
calmet.dat
calpuff.con.S.grd02.nc
calpuff.inp
cpuff.out
```
### 程式進度畫面

| ![CALPUFF_prog.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_prog.PNG)|
|:-:|
| <b>CPUFF721執行進度網頁畫面</b>|

| ![CALPUFF_nc.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CPUFF_nc.PNG)|
|:-:|
| <b>CPUFF721最終進度網頁畫面</b>|

### [cpuff_gifs.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALPUFF/cpuff_gifs.html)


| ![cpuff_gifs.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/cpuff_gifs.png)|
|:-:|
| <b>CPUFF721最終進度網頁畫面</b>|
