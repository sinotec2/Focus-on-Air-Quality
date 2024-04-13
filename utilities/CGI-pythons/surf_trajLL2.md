---
layout: default
title:  surf_trajLL2
parent: CGI-pythons
grand_parent: Utilities
date: 2022-06-07
last_modified_date: 2023-01-13 16:34:59
tags: trajectory CWBWRF CGI_Pythons NCL
---

# surf_trajLL2程式說明
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

> 這個服務網頁提供最近5日北、中、嘉、高等4處的反軌跡(中央氣象局WRF_3km預報數據、後修正以GFS 10天預報及降尺度WRF執行結果)、以及歷年地面測站觀測數據計算之正/反軌跡，整體服務說明見[臺灣地區高解析度軌跡產生/自動分析系統](traj.md)

### 整體服務架構

![](traj/2024-04-10-14-11-58.png)

### 相關資源

- 服務網頁位址：[http://sinotec24.com/traj2.html](http://sinotec24.com/traj2.html)
- python程式[下載](traj/surf_trajLL2Mac.py)。不同版本說明與修改細節詳見[內網版本與新增功能](../../TrajModels/ftuv10/4.daily_traj%40ses.md)
- 軌跡計算詳見[ftuv10](../../TrajModels/ftuv10/ftuv10.md)
- 呼叫程式
  - [traj2kml.py](../../wind_models/CODiS/5.traj.md)
  - [ftuv10.py](../../TrajModels/ftuv10/ftuv10.md)
  - [ncl](../Graphics/NCL/)

{% include download.html content="[臺灣地區高解析度軌跡產生/自動分析系統cgi程式](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/CGI-pythons/surf_trajLL2.py)" %}

## 程式說明

### 主要程序

- 開始
  - 設定路徑和相關變數
- 處理表單輸入
  - 獲取地點名稱和經緯度
  - 判斷方向和日期等信息
- 生成臨時文件名和路徑
- 檢查是否已存在相應的文件
  - 如果存在，顯示下載鏈接
- 生成和執行系統命令
  - 包括圖像處理和NCL腳本執行
  - 顯示作業提交信息和下載鏈接
- 結束

![](traj/2024-04-10-15-40-22.png)

### 避免覆蓋的策略

這個版本可以提供多人同時運作，以發揮node03工作站的算力，為避免覆蓋檔案，採取的對策有二

- NCL更改輸出檔名
  - `topo.png` $\rightarrow$ 從`filename.txt`中讀取檔名
  - 但是`filename.txt`還是會被覆蓋
  ```python
  topo = asciiread("filename.txt",-1,"string")
  wks = gsn_open_wks(wks_type,topo) ; send graphics to PNG file
  ``` 
- 隨機目錄
  - centos似乎不允許apache在`/tmp`建立目錄，因此將其建在`WEB`之下，並加上前綴(`tmp_`)以利批次維護。
  - 開啟目錄後，測試新增一個空白檔

  ```python
  ...
  import tempfile as tf
  ...
  trj=WEB+'trj_results/'
  ran=tf.NamedTemporaryFile().name.replace('/tmp','')
  pth=trj+'trj_'+ran+'/'
  result=os.system('mkdir -p '+pth+';touch '+pth+'a')
  ```

### filename.txt

- 這個文字檔的內容儲存個案的csv檔名，除用做檔案的連結以外，也會做為NCL圖標題、以及圖檔名稱。
- 這個檔案改在軌跡計算程式內([`root+'/cwb/e-service/btraj_WRFnests/ftuv10_10d.py'`](../../TrajModels/ftuv10/ftuv10_10d.py))產生
- 是否有'trj_results'目錄，取決於單機版還是多人隨機目錄版，前者是有的、後者取消，檔案將存在工作目錄。

```python
...
  name=dr+'trj'+nam[0]+DATE+'.csv'
...
with open('filename.txt','w') as f:
  f.write(name.split('/')[1])
```