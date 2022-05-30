---
layout: default
title: 後製工具
parent: Recommend System
grand_parent: CMAQ Model System
nav_order: 4
date: 2022-04-22 10:28:51
has_children: true
last_modified_date: 2022-04-22 10:28:56
permalink: /GridModels/TWNEPA_RecommCMAQ/post_process
---

# 後製工具
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
- 網格模式模擬結果是否符合測站實測值，是模式性能評估的目的，也是證明模式是否可用的關鍵。雖然當時學者([陳王琨、林忠銓，2003])提出環保署性能評估制度將會將有衍生問題的可能，但畢竟92年迄今也經過了20年的歷史，制度仍然存在而且正常運作、沒有太大幅度的震盪。
- 由於模式模擬與驗證過程還有很多細節，不是條文能夠一一詳細規範，環保署乃提供驗證所需的數據及工具，以便將驗證過程能夠規格化，減省審查的時間。
- 驗證過程所需的圖表，過去也是耗費精力的作業，環保署能夠提供軟體工具，也是頗令新人振奮的。至於是否影響到技術顧問機構的業務，那就隨走隨看囉。

[陳王琨、林忠銓，2003]: <http://nhuir.nhu.edu.tw/retrieve/7958/3042040201.pdf> "陳王琨、林忠詮，2003，「空氣品質模擬規範與模式審核管理新制度之建置研究」，2003 年氣膠研討會論文集"

## 下載及安裝
- 下載點：國網1號：/work1/simenvipub01/download/model/post_process.tar.xz
- 解壓縮： `tar xvfJ ...`
```bash
scp sinotec2@twn1:/work1/simenvipub01/download/model/post_process.tar.xz .
tar xvfJ post_process.tar.xz
```
- 使用者可以選擇在國網3號或本地執行
  - 都需要安裝Evaluate環境
  - 檔名必須是**v1**.YYYY-MM.conc.nc
  - 檔案內容需要有地面風速(WSPD10)之輸出

### Python 環境設定
- 程式庫安裝：將會安裝成**Evaluate**之環境

```bath
#/nas2/cmaq2019/download/model/post_process/Performance
conda env create --quiet --file environment.yml
kuang@DEVP /nas2/cmaq2019/download/model/post_process/Performance
#$ conda env list
# conda environments:
#
base                     /opt/anaconda3
Evaluate                 /opt/anaconda3/envs/Evaluate
ncl_stable               /opt/anaconda3/envs/ncl_stable
py27                     /opt/anaconda3/envs/py27
py37                  *  /opt/anaconda3/envs/py37
```
- 目前環保署提供了Performance目錄下的程式，
- Compare/目錄下並沒有任何檔案

## 程式系統架構與執行
### 整體架構
- 目前只提供tar檔裏Performance目錄項下的檔案，如[2022年2月17日我國CMAQ公告模式教育訓練─後製工具操作教學](https://drive.google.com/drive/folders/1_GdUsRXQU1p8QhwwDbhz-nVhgUQBbftX)圖所示。
- 理論上如果使用公版模式的所有條件，應該是不需要提供模擬驗證比對的相關圖表。只需要提供增量濃度分布圖(Air_Increment_tool)
- 此處乃就所提供的程式一一執行，以了解公版模式的定性、定量的表現，以及符合性能規範的程度。

| ![post_process.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/post_process.png) |
|:--:|
| <b>圖1公版模式後製工具程式庫、數據檔案目錄架構</b>|

### 檔案管理
- 作業目錄：在每項工具目錄(*_tool)下，會有執行檔、Data目錄、執行後也會產生Output目錄
- 檔案連結：
  - Data/Sim/mcip:將mcip的
  - Data/Sim/cctm：將模式模擬結果連結至此，更名為v1...conc.nc

## 環保署後製工具的問題
- 陸續發現的問題會條列於此供參。
### 標準輸入(standard input)的問題與解決建議
- 公版模式後製工具的引數都是以標準輸入(standard input)方式執行，引發執行時間過長tty被斷線的問題、此種長時間卦網的執行方式也是國網中心所不樂見的。
- 解決方式
  - 將輸入內容寫成文字檔，以`<`輸入：`python ..py < YrMn.txt &`
  - 使用`tmux`開啟工作段。也會使作業在背景執行。
  - 修改python程式，將`input(...)`改成`sys.argv[1]`

### 有關增量模擬分析
- 不能分析負值的增量(減量效益)，這對AQMP來說很重要。
  - 將Base和Case互換

### 程式內設還需修改
- cctm檔名
- 程式會讀取combine後的地面風速。而繪製濃度等值圖並不需要該項目。
- 沒有全國測站的符合比例，只有分區，無法對整體有所掌握

### 等值圖的問題
- 雖然使用了`rainbow`，顏色豐富，但因設定為漸層色階，辨識能力太差、階層太多，無法從圖中讀出確切的數值。建議：
  - 改成如[NOAA 1-Hr Average Ozone forecasting](https://airquality.weather.gov/)、[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis_sens/2add_NewPt/#201901模擬結果差值)、[hIncremental Evaluation of New CMAQ Versions](https://www.epa.gov/cmaq/incremental-evaluation-new-cmaq-versions)
  - 減少階層至10層左右、20層以下。
- SO2只有出日均值濃度分布，無法討論大型污染源的行為。
- 增量色階不存在上限值(`extend=Max`)。
  - 超過最高色階的範圍，仍是該最高色階的顏色，
  - 這對模擬最大值的出現位置，是嚴重模糊化。

## Table of Contents in Post_process