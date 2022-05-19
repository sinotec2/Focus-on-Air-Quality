---
layout: default
title: 污染源在空品測站上的表現
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 4
last_modified_date: 2022-05-16 09:42:56
---

# 污染源在空品測站上的表現
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

## 高雄屏地區空氣污染物的空間及時間序列差異特性分析
臺灣地區秋冬季節空氣品質不良率偏高，即使排除境外因素污染仍以高屏較差(詳[臺灣地區空品不良日數逐月變化](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/3TerrainEffect/#臺灣地區空品不良日數逐月變化))。

本研究針對高屏雄地區空氣品質自動監測站歷史資料，分析空氣污染物空間及時間序列差異特性，探討主題包括特殊性工業區溯源、臭氧事件日煙流三維軌跡分析、局部PM2.5污染事件分析、週末與週間晚餐時間污染物之尖峰濃度發生機率差異(peaking hour probability difference, PHPD)分析等及監測數據雲端監控系統應用於工業區污染溯源，相關成果可作為規劃減量策略及未來管制重點之參考。

## 林園特殊性工業區測站監測數據之雲端監控系統
本研究建立林園特殊性工業區測站監測數據之雲端監控系統，搭配VOCs污染指紋排放地圖，藉由比對監測數據、排放指紋物種特徵以及風向，強化污染來源之查找。本法已成功應用於確認林園工業區多起製程異常排放或洩漏事件，後續則持續監控場所改善進度。


## 林園臭氧事件之北高雄污染源三維正軌跡分析
- 林園工業區分析過程，發現多次出現非本地污染特徵之高值(如乙、丙烯同時之高值)，因此進一步分析更大範圍影響的可能性。
- 藉由WRF建立地區風場，分析林園站2018/10/13臭氧事件日煙流三維軌跡分析，測試北、南高雄高空污染源夜間的煙流行為，以檢討林園地區臭氧污染成因。
### 事件日之綜觀天氣
- 氣流線與空氣品質，可以參考[Nullschool][NS20181013]之歷史檔案。為典型鋒面通過之東北季風天氣，並沒有明顯的境外污染現象。
- [https://www1.wetter3.de/Archiv/](https://www1.wetter3.de/Archiv/)可以查到[GFS](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast)模擬這2天鋒面通過臺灣高低層虛位溫差異([KO-index](http://www.eumetrain.org/data/2/20/Content/theory_ko.htm)、等值線)及高層垂直運動(hPa/h以色塊標示)的歷程
  - 事件日當天KO指標0值正好通過高雄地區，海面為負值、陸地為正值，如圖所示：

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/2018101200_10_as.gif)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/2018101300_10_as.gif)|
|:-:|:-:|
| <b>2018101200</b>|<b>2018101300</b>|

[NS20181013]: <https://earth.nullschool.net/#2018/10/13/0400Z/chem/surface/level/overlay=cosc/orthographic=-238.92,24.73,2066> "https://earth.nullschool.net/#2018/10/13/0400Z/chem/surface/level/overlay=cosc/orthographic=-238.92,24.73,2066"

### 空品與地面風速風向
- 事件日中午高屏地區臭氧濃度之空間分布如圖所示
  - 合併所有特工站及環保署測站尖峰臭氧濃度，以解析度1公里進行Kriging內插。Surfer繪圖。
  - 林園特工站之間的間距約為2Km，以南方濱海的3個測站具有相同特性，而其他測站測值較低，由此可以推斷此一臭氧煙流超標範圍在本市範圍的空間尺度僅約2Km。然而對潮州站與下游大範圍，都有可能是超標的狀況。

| ![20181013Surfer.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/20181013Surfer.png)|
|:-:|
| <b>2018/10/13 高屏地區環保署測站(白點)及特工測站(紅點)臭氧尖峰濃度之分布，林園測站測值尖峰濃度為126 ppb</b>|

- 事件日前後、環保署林園站及鄰近其他4站之臭氧歷線如下圖所示。
  - 林園站之高濃度確實有其空間的獨立性
  - 而NOx/NMHC前驅物濃度來看，符合地區週變化的特性(週四 ~ 週日)，唯10/12及13日零時皆出現NMHC及NOx之異常高值。
  - 由特工區測站顯示為乙烯，除鄰近污染源排放，亦可能來自北方仁大工業區)。夜間同時排放NMHC及NOx之污染源很可能是燃燒塔。

| ![O3@20181011fengshanxiaogangdaliaolinyuanrenwu.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/O3@20181011fengshanxiaogangdaliaolinyuanrenwu.png)|![NOxO3NMHC@20181011linyuan.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NOxO3NMHC@20181011linyuan.png)|
|:--:|:--:|
|<b>2018/10/13事件日前後、林園站及鄰近其他4站之臭氧歷線</b>|<b>同時段林園站NOx及NMHC與臭氧歷線</b>|

- 當日地面二維正、反軌跡之分析，可以參考[林園臭氧事件與氣流軌跡線](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/3TerrainEffect/#林園臭氧事件與氣流軌跡線)，作法詳[由CWB數據計算軌跡](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/traj/)

### 三維正軌跡累積頻率分析方法
- 三維風場來自WRF模式D4範圍模擬結果、水平解析度3公里、垂直40層。開啟FDDA。
- 軌跡線通過網格之累積頻率函數作法可以參考[林等1998][林等1998]。
- 分析程式參考[WRF三維軌跡分析](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/traj3D/)。
- 繪圖軟體使用[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI)。

[林等1998]: <http://mopl.as.ntu.edu.tw/web/ASJ/26/26-3-3.pdf> "林能暉、彭啟明、陳進煌(1998) 東亞硫化物之長程輸送: 氣流軌跡線之應用, 大氣科學26:3, 265-280."

### 北高雄污染源三維正軌跡累積頻率
- 正軌跡來自仁大工業區，高度125M。
- 網格水平解析度為 3 Km、垂直為等間距 50 M 共 51 格。
- 污染粒子自凌晨開始，每 15 秒釋放、逐一追蹤其通過網格位置，每小時結算其出現機率。


| ![3dTraj1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/3dTraj1.PNG)|
|:-:|
| <b>2018/10/13北高雄污染源三維正軌跡累積頻率之ZY、XY平面分布圖(上：ZY平面，X向加總。下：XY平面，地面第1層)</b>|

結果顯示北高雄污染源煙流在夜間北風作用下向南發展到達林園地區，而地區的下沉氣流則會將煙流帶至地面造成污染。

### 南高雄污染源三維正軌跡累積頻率
- 污染源位於大發工業區，同樣自凌晨開始釋放

| ![3dTraj2.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/3dTraj2.PNG)|
|:-:|
| <b>2018/10/13南高雄污染源三維正軌跡累積頻率之ZY、XY平面分布圖(上圖：ZY側面圖，X方向加總結果。下圖：XY平面圖，地面第1層)</b>|

南高雄污染源煙流的流布情形則呈現不同樣態，海面上受到下沉氣流作用，煙流垂直運動確實受到抑制，將可以維持較高濃度而不會被擴散稀釋，而在海風的帶動下在中午造成海岸地區的較高污染。

## 局部PM2.5污染現象
除臭氧及VOCs溯源之外，本研究也探討了局部PM2.5污染的現象。2015~2018年高屏地區冬半年PM2.5日均值盒鬚圖之變遷分析結果顯示，雖然多數測站呈現改善趨勢，但發現林園、橋頭及大寮等3處測站，近3年不但無改善趨勢，反而有劣化現象，3年平均值以林園站增加8 μg/m3為最高，倘這3站的劣化現象再扣除上游縣市的改善所造成的影響，劣化幅度將達到20 μg/m3。另進一步分析各測站PM2.5日均值超出所有高屏測站平均值達10 μg/m3以上之日數，並將超出日數較多的測站視定義為空間極值測站，發現2015~2016年以潮州站為主具有較高的空間極值特性，而2018年則為橋頭與站亦有較高的空間極值特性，次高者為林圜站，就性質上有很大差異，推測可能因儀器更換造成的差異。

為減少測站因年度間儀器調校所造成的不確定性，本研究再進一步分別將各年度冬半年PM2.5日均值進行標準化後加以比較，以減少測站因年度間調校所造成的不確定性，發現各站成為空間的極值的天數普遍有逐年增加趨勢，原因為境外或上游縣市污染改善，使得局部污染對測站的影響更為明顯。，且由南高雄PM2.5空間極值發生之三維煙流軌跡分析，與前述北高雄VOCs造成林園臭氧高值有類似的氣流動力原因。

最後本研究建立測站濃度日變化之PHP分析架構，如發現南高雄地區上午和正午SO2之PHP，與交通尖峰關係不大，與垂直擴散現象、或前述下沉氣流的現象有較為密切的關係，除了風場模擬之外，空品觀測亦為地區垂直擴散現象之印證指標。

進一步以PM2.5的週末與週間晚餐時間PHPD差值作為餐飲業粒狀物排放指標，發現歷年以舊高雄市區的楠梓、左營及小港等3處測站的排放情形較為嚴重，惟後二者近年已有降低的趨勢，而楠梓站則呈現先降後升的趨勢。另新市區仁武、大寮及林園等3處測站的排放情形目前雖尚不嚴重，但有呈現逐年上升的趨勢，此一指標可作為再繼續觀察及因應加嚴週末餐飲業排放管制措施之效果分析。

本研究並建立林園特殊性工業區測站監測數據之雲端監控系統，搭配本研究發展的林園工業區污染指紋排放地圖，及整理出特定指紋物種溯源可能對應之工廠製程，藉由比對林園特工站監測數據與排放指紋物種特徵，強化監測數據雲端監控系統應用於污染溯源之可行性。本法已成功應用於確認林園工業區多起製程異常排放或洩漏事件，後續可持續監控場所改善情形。

關鍵字：煙流三維軌跡、局部PM2.5污染事件、污染物尖峰濃度發生機率差異、異常排放溯源。
論文主題：排放源特性與源解析、氣膠監測評估及空氣品質模式。

## Source
- 原文發表於[第26屆國際氣膠科技研討會ICAST26th](http://www.taar.org.tw/uploads/conference/1016/2019ICAST手冊_0925r1.pdf)
  - 曠永銓、簡誌良、李其霈、郭子豪、宋國安、陳金瀛, 2019, 高雄屏地區空氣污染物的空間及時間序列差異特性分析, 26屆國際氣膠科技研討會, 中原大學, 10/4 ~ 5, 2019.
