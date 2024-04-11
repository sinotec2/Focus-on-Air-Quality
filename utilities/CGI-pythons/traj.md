---
layout: default
title: 臺灣地區高解析度軌跡產生/自動分析系統
parent: CGI-pythons
grand_parent: Utilities
date: 2023-01-26
last_modified_date: 2024-04-09 17:56:15
tags: CGI_Pythons mmif
---

# 臺灣地區高解析度軌跡產生/自動分析系統

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


## 實例

- 以下皆更新至traj2.html版本

### 網頁計算服務網址

- http://sinotec24.com/traj2.html @iMacKuang[^9]
- http://node03.sinotech-eng.com/traj2.html @node03

## 整體服務架構

![](traj/2024-04-10-14-11-58.png)

## html說明

### 前端畫面

![](traj/2024-04-10-11-19-22.png)

- 這個畫面的設計概念延續前一版的traj.html，畫面右側維持靜態的展示，為今日12時北(中山)、中(忠明)、南(嘉義)、高(前金)測站反軌跡。左側則為選項及操作執行
  - 近5日測站反軌跡、通風指數選項
  - 畫面左側的8個選項，分成3組
    - 軌跡設定：風速風向數據及正/反軌跡選項
    - 地點：空品區縣市測站、或任意經緯度座標
    - 軌跡線起/迄之日期時間
  - html物件型態：包括jquery的下拉選單(selectmenu)、文字輸入、及日期選單(datepicker)
  - button submit物件做為整體提交並呼叫cgi_python(traj/surf_traj3.py)的觸發。
- 選單都是jquery套件，其中測站較為複雜，是連動下拉選單，主要應用append方法，按照前一選擇結果，依序帶出後一選單的內容。
- 提供cgi_python的變數4項變數
  - dirFB(正/反軌跡的方向選擇)
  - AQSname(測站代碼)、
  - date(日期)、
  - number(小時)。

### traj.html

- traj2.html說明詳見[node03](https://node03.sinotech-eng.com/traj2.html_程式說明.html)或[boostnote](https://boostnote.io/shared/05cd78db-c218-49dc-8864-46c8e77fd2c6)
- 程式下載
  - {% include download.html content="臺灣地區高解析度軌跡產生/自動分析系統[traj2.html](./traj/traj2.html)" %}

## CGI-pythons

### surf_traj3.py

- 這是個早期mac的版本，詳見[程式碼](./traj/surf_traj3.py)。
- 主要為地面軌跡計算程式負責計算(`/Users/Data/cwb/e-service/surf_trj/traj2kml.py`)，在程式中以os.system()呼叫，立即執行。主要理由是因為:
- 程式執行時間較短，很快會有結果，再加上...
- 系統會尋找過去執行成果，如果已經計算過了，將會直接提交結果，不再另行計算，以減省需要時間。
- 此處以測站代碼，而非測站名稱進行計算，traj2km.py有因而進版。
- 調用jquery的data-auto-download，直接下載成果檔案到客戶端的「下載」目錄。
- 提供Leaflet[地圖數位板(貼版)](../GIS/digitizer.md)連結，讓客戶可以馬上檢視kml成果，自行研判是否合理。Leaflet的設定在[index.js](./traj/index.js)裏。
- index.js：此js檔為調用D3js(Leaflet提供)的橋梁，主要使用者設定都在此一檔案內，包括了：
  - 起始值中心點的位置(line 11)
  - 起始地圖的縮放比例(line 12)
  - 貼圖的顏色、透明度等(line 15~17)
  - 起始站的標籤與文字內容(line 37~45)，由layer第1個物件中提取。

### surf_trajLL2.py

- 這個版本能夠讀取任意點的經緯度，並且更新了軌跡模式。詳見[surf_trajLL2程式說明](./surf_trajLL2.md)，[程式碼](traj/surf_trajLL2Mac.py)。
- 

[^9]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。敬請逕洽作者：sinotec2@gmail.com.
