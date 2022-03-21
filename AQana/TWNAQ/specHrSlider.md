---
layout: default
title: specHrSlider.py
parent: Taiwan AQ Analysis
grand_parent: AQ Data Analysis
last_modified_date: 2022-02-08 13:46:05
---

# specHrSlider.py
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
### 大要

     本程式用在篩選測站高值，經由matplotlib.widget的滑桿與查核紐，可以縮減重複執行程式的次數，提升查找的效率。

### 說明

     由於空品分析非但著眼於最高值，有時濃度時間變化的波形、測站之間的上下游關係，也經常是分析的重點，過去為查找適合的個案，經常要重複執行程式，產生圖表、由其中分析較具有代表性的個案，工作量龐大複雜。

     為改善此一工作形態，使用互動式繪圖軟體，建立圖形界面程式(GUI)，都是可行的方式。由於前者所費不貲，在嘗試錯誤階段需要大量資源，並不經濟，後者可藉以小程式套件，即可發揮很大效果。本程式即為成功案例。

### 繪圖軟體

     基本上是python程式，主要引用pandas與matplotlib程式庫。

     由於matplotlib有自己的GUI程式[matplotlib.widget](https://matplotlib.org/api/widgets_api.html?highlight=widget)，功能雖然不多，但是在程式修改、圖面與資料的傳遞等問題，都較其他架構來得容易。

### 程式檔案位置

     master:/usr/kbin/specHrSlider.py

## 使用方式

### 命令列指令
- usage: specHrSlider.py [-h] -t STNAM -s SPNAM -b BEGD -e ENDD -a ACTION
  - STNAM：空品測站名稱，
    - 目前還是以拼音英文為限(小寫)，測站數不限
    - 測站間以逗點","區隔，
    - 測站名稱也會用在暫時csv檔存取之命名。
  - SPNAM：空氣品質項目(大寫)，本程式只接受一個空品項目。
  - BEGD：起始日曆年月日，共8碼(包含當日)
  - ENDG：結束日曆年月日，共8碼(包含當日)
  - ACTION：plot(在X Window顯示)、save存成png檔案，可使用specHr.py程式以免除GUI按鍵。
- GUI指令
  - 在命令列輸入時間與測站的最大範圍之後，微調即靠GUI按鍵來達成。
  - checkbutton：測站之勾選或取消
  - Sliders：
    - beg/end點選後程式會重新繪圖，或取消視窗(X)，程式不會中斷，會重新繪圖。
    - mov可以滑動曲線，按取消視窗(X)鍵即重新更新x日期座標軸。
  - Exit：中斷程式，跳出並關閉視窗。
- 顯示方式：
  - 當ACTION以plot方式執行程式時，會抓取DISPLAY之環境變數，須有相對應之x window或jupyter等界面。

- 範例

```bash
specHrSlider.py -t xiaogang,daliao,chaozhou,pingdong -s SO2 -b 20180101 -e 20180331 -a p
```

| ![specHrSlider1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/specHrSlider1.png)|![specHrSlider2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/specHrSlider2.png)|
|:--:|:--:|
| <b>左圖為GUI版本specHrSlider.py</b>|<b>右圖為原來命令列版本specHr.py</b>|

## 資料檔案

### 輸入檔案    

- 空品站數據 
	- 程式會讀取master:/home/backup/data/epa下各年度之原始空品資料檔，如果缺少檔案，就無法完整做圖。
	- 空品測站名稱與代碼對照表，存放在/home/backup/data/epa/pys/sta_list.json
	- 空品項目名稱與代碼對照表，存放在/home/backup/data/epa/pys/item2.txt
- 如果要搬移到個人電腦上運作，須修改檔案之路徑。

### 結果檔案

- 會在工作目錄產生暫存之csv檔案，以避免讀取原始資料費時不經濟。
- 起迄日期的暫存檔input.txt，也會在工作目錄產生。
- 圖檔會統一放在工作目錄的pngs下，由於檔案可能很多，可以避免雜亂。
　     
## 程式設計說明
### 分段說明

1. line89~181 TRY架構：
	- 讀取CSV暫存檔，若無暫存檔，則由原始檔案讀取並製造一個暫存檔。
	- 主要運用pandas程式來整理時間序列檔案。
2. line190~WHILE架構：
	- 由於matplotlib沒有master.loop()方法，而圖形(xy軸)更新時，圖檔必須關閉再開，為避免程式關閉造成中斷，此處以無限迴圈while True:的方式，取代master.loop()方法。
	- 此法當網路速度屏障時，會有明顯的關閉再開的閃動，如果是單機作業，關閉再開的銜接時間可以縮短到極限，因此畫面還可以保持暫留效果。 
3. line212~237：
	- pandas與matploglib做圖，此部分為一般的xy圖，並無特色。
4. line239~243與函數func：
	- 此段為check button之段落(參考https://matplotlib.org/gallery/widgets/slider_demo.html#sphx-glr-gallery-widgets-slider-demo-py)，
	- 由於測站數可能不一樣，因此原來範例中的按鈕改以序列方式執行。
5. line223~260與函數update：
	- 此段為Slider的用法，同樣參考前例，Slider除了用以收取beg和end，即為程式所需的起始和結束日期，另外還加了一項mover的Slider，可以前後移動曲線，
	- 程式會輸出其beg與end，做為下次繪圖之輸入數據。
6. line261~263與函數reset：為button方法段落。用來終止WHILE架構。

### Coding
- check the [FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/specHrSlider.py)

## links

Here：specHrSlider.py(*)
Parent：Dr. Kuang's Evernotes_trajectories(*)
