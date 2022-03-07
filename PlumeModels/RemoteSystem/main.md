---
layout: default
title: ISCST/AERMOD 主程式
parent: Remote Processing
grand_parent: Plume Models
nav_order: 6
last_modified_date: 2022-03-07 15:17:07
---
# ISCST/AERMOD 主程式
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
- 煙流模式主程式的遠端計算網頁。
- 主要服務已經準備好各項輸入檔案的使用者，Javascripts將會讀取使用者提供的檔案存到伺服器上，並啟動CGI_Python程式進行煙流模式的遠端計算。
- 因計算時間超過網頁停等容許時間。此處不採取bash scripts定期檢視郵寄結果策略，而是直接限制總執行緒，讓工作站優先服務先提出submit的使用者，因此使用者可以經由短暫的等待得到結果、或由網頁提供的連結，自行檢視工作站的執行進度。
- 由於ISCST與AERMOD有相似的執行方式，因此將二模式整合在同一網頁執行，增加模式的選項，以降低介面的重複性，使用者也方便進行模式間的比較。
- 服務僅限模式計算，後處理部分讓使用者視需要自行下載結果檔案，再啟動其他程式進行處理、繪圖。

## HTML
### 設計
- 以表格方式整理模擬過程、各程序之程式版本、內容、IO及範例、檢核方式以及筆記。
- 提交CGI_python物件
  - 4個檔案：依序為run stream、氣象檔(AERMOD會需要獨立的高空數據檔)、以及複雜地型時需要的地形檔。
  - `model`：模式之選項，ISCST或AERMOD二擇一

### Coding
- [AERMOD.html](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/AERMOD.html)

## CGI_PYTHON
### [AERMOD.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/AERMOD.py)之程式設計
- 執行緒之讀取
  - 應用subprocess模組進行讀取。bash指令運用了ps、grep、以及wc
  - 因工作站有可能同時運作了iscst及aermod程式，因此分別讀取緒數予以相加。
  - 工作站為 6 核心，限制總緒數在5以下以提高服務效能(see [TODO's]())

```python
npid1=subprocess.check_output('ps -ef|grep aermod|grep -v grep|wc -l',shell=True).decode('utf8').strip('\n')
npid2=subprocess.check_output('ps -ef|grep iscst3|grep -v grep|wc -l',shell=True).decode('utf8').strip('\n')
npid=int(npid1)+int(npid2)
if npid>=5:
  print 'total '+str(npid)+' iscst or aermod processes are running, please wait. </br>'
  print '</body></html>'
  sys.exit()
```
