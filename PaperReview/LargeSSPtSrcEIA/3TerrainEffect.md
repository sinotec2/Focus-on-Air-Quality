---
layout: default
title: 煙流受地形效應之影響
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 3
last_modified_date: 2022-05-16 09:42:56
tags: terrain trajectory CODiS AERMAP
---

# 煙流受地形效應之影響
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

## 差異加熱對氣流與空污的效應
### 季節變化
- 全球、大陸尺度
- 冬季：東北季風，將大陸地區霧霾、沙塵帶到臺灣
- 夏季：西南季風、帶來海洋較乾淨氣流

![Pendergast2a.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Pendergast2a.PNG)
![Pendergast2b.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Pendergast2b.PNG)


 <b>季節加熱差異造成的環流與空污現象([Pendergast 1984][Pendergast 1984] in [Atmospheric science and power production][Randerson 1984])，圖a為一月均溫、圖b為7月均溫，單位為華氏</b>

#### 臺灣地區空品不良日數逐月變化
  - 行向(縱)：自北到南測站
  - 列向(橫)：1~12月
  - 季節變化：冬季(9月~隔年4月)高、6~8月低

| ![TCCIP第34期電子報_圖2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TCCIP第34期電子報_圖2.png)|
|:--:|
| <b>2005年至2017年臺灣環保署一般測站空氣品質指標不良達橘燈以上（AQI > 100，對敏感族群不健康）之月平均日數統計，(a)臭氧（O<sub>3</sub>）指標，(b)細懸浮微粒（PM<sub>2.5</sub>）指標。([蔡等2019][蔡等2019])</b>|

[蔡等2019]: <https://tccip.ncdr.nat.gov.tw/km_newsletter_one.aspx?nid=20191202172107> "蔡宜君、謝佩蓉、李貞潁、許晃雄，臺灣空氣品質變化與氣候變遷, 2019/12/01 臺灣氣候變遷推估資訊與調適知識平台電子報034期"

### 日夜變化
#### 中\~小、都會區尺度海陸風、山谷風概念

| ![Pendergast1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Pendergast1.PNG)|
|:--:|
| <b>日夜加熱差異造成的環流與空污現象([Pendergast 1984][Pendergast 1984] in [Atmospheric science and power production][Randerson 1984])</b>|

[Pendergast 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Malcolm M. Pendergast, 1984, Chap. 2, METEOROLOGICAL FUNDAMENTALS, in Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."

[Randerson 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Randerson, D. (1984). Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."
#### 林園臭氧事件與氣流軌跡線
  - 環保署林園站中午O<sub>3</sub>尖峰時間反軌跡(白色) vs.
  - 當天2時北高雄某廠燃燒塔之正軌跡(紅色)
  - 夜間：北風\~東北風，為秋冬季盛行風、山風、陸風
  - 日間：西北\~西風，為海風
  - 軌跡線繪製詳參[由CWB數據計算軌跡](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/traj/)

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/LinyuanBTRJ1.PNG)|
|:-:|
| <b>(a)2018/10/13/12:00時，O<sub>3</sub>=126ppb</b>|
| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/2018102712linyuan.png)|
| <b>(b)2018/10/27/13:00時，O<sub>3</sub>=121ppb</b>|
| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/LinyuanBTRJ3.PNG)|
| <b>(c)2018/12/3/13:00時，O<sub>3</sub>=126ppb</b>|

- 燃燒塔正軌跡分析證實了以北高雄燃燒塔對反應生成測站O<sub>3</sub>高值有較大的可能性  
  - 北方工業區燃燒塔以當天凌晨CEMS記錄最大流量發生時間，做為正軌跡線的起始時間，圖中為紅色點線表示。
  - 由圖中可以發現，紅、白2條軌跡線在高雄市西南側沿海與近海地區大多呈現平行運動，間距約為2~4公里，約為一般網格模式解析度範圍，應為污染源的精確位置、或風場模式內插所造成的誤差。
  - 然而就污染物受日夜海陸風的性質而言，圖中正、反軌跡線可以確認造成林園測站O<sub>3</sub>高值的污染源，非常可能就是仁大工業區之燃燒塔排放。

## 氣流、獨立山、與空氣污染
- 氣流遇山的行為：左右繞過、翻越，
- 視風速、山形、斜坡、以及大氣穩定度而定

### [水洞](https://slideplayer.com/slide/709993/)試驗
- 無因次流體力學參數
  - [福祿數](https://zh.m.wikipedia.org/zh-tw/福祿數)：慣性力和重力效應之比
  - [雷諾數](https://zh.wikipedia.org/zh-tw/雷诺数)：流體慣性力與黏性力的比值
- F<sub>H</sub> &le; 0.2 : 繞山
- F<sub>H</sub> &ge; 0.9 : 中心線可翻越、阻體後渦流隨F<sub>H</sub>增加而減少


| ![FrRe.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/FdRe.PNG)|
|:-:|
| <b>不同流況水洞試驗攝影結果，流體自左方流入，3維鐘形獨立山高H。([Hunt et. al 1978][Hunt et. al 1978])</b>|

[Hunt et. al 1978]: <https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=20015MB7.TXT> " J. C. R. Hunt, W. H. Snyder, and R. E. Lawson, Jr., Flow Structure and Turbulent Diffusion Around a Three-Dimensional Hill, in Fluid Modeling Study on Effects of Stratification, Part I. Flow Structure, Report EPA-600/4-78-041, U. S. Environmental Protection Agency, 1978."

- 繞山煙流之濃度分布

| ![Lin1974.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/Lin1974.PNG)|
|:-:|
| <b>水洞模擬煙流通過3維鐘形獨立山之濃度分布，並與平坦地形分布相比([Lin et. al 1974][Lin et. al 1974])</b>|


[Lin et. al 1974]: <https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=2000XKAB.TXT> "J.-T. Lin, H.-T. Liu, and Y.-H. Pao, Laboratory Simulation of Plume Dispersion in Stably Stratified Flows over a Complex Terrain, Flow Research Report No. 29, prepared for U. S. Environmental Protection Agency, Flow Research, Inc., Kent, Wash., 1974.)"

### CTDMPLUS 模式的作法

| ![CTDMPLUS1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CTDMPLUS1.PNG)|
|:-:|
| <b>分流點前仍為平坦地形，分流點後其上翻越山嶺，其下繞行山嶺左右。([Perry 1992][Perry 1992])</b>|

| ![CTDMPLUS2.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CTDMPLUS2.PNG)|
|:-:|
| <b>翻越部分煙流的計算方式([Perry 1992][Perry 1992])，此一機制與ISCST3相同</b>|

| ![CTDMPLUS.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CTDMPLUS.PNG)|
|:-:|
| <b>分流點下繞山煙流的計算概念：將山嶺壓縮成延流方向之直線線段([Perry 1992][Perry 1992])</b>|

| ![CTDMPLUS3.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CTDMPLUS3.PNG)|
|:-:|
| <b>以橢圓形等高線模擬山嶺之組合逼近實際複雜地形([Perry 1992][Perry 1992])</b>|

[Perry 1992]: <https://www.jstor.org/stable/26186577> "Perry, S.G. (1992). CTDMPLUS: A Dispersion Model for Sources near Complex Topography. Part I: Technical Formulations. Journal of Applied Meteorology (1988-2005) 31 (7):633–645."

### AERMOD 的地形模擬
- 分流線高度觀念
  - 高於分流線者將翻越山嶺。以山嶺不存在情況估算。
  - 低者將繞山、或直接撞擊地表面。以山嶺地表面高度計算。

| ![AERMOD1.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/AERMOD1.png)|
|:-:|
|<b>地形影響煙流的2個極端情況概念圖。地表高度與絕對高度之定義如圖(AERMAP Training, [Roger 2007][Roger 2007])</b>|

- 最後濃度為二者之加權平均

| ![AERMOD2.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/AERMOD2.png)|
|:-:|
| <b>AERMOD地形效應的加權計算方式示意圖。from AERMAP Training([Roger 2007][Roger 2007])</b>|

[Roger 2007]: <https://slideplayer.com/slide/10395603/> "Roger W. Brode, AERMAP Training, U.S. EPA/OAQPS/AQAD Air Quality Modeling Group, NESCAUM Permit Modeling Committee Annual Meeting, 5/31, 2007."

### 複雜地形模擬案例
- 林口電廠(AERMOD)
  - mmif氣象1/21\~31
  - 有建築物

| ![noterr.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/noterr.png) |![withterr.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/withterr.png)|
|:--:|:--:|
| <b>無地形，煙流偏西南方，為東北季風影響</b>|有地形，煙流方向偏南，擴散範圍受到限制，集中在河谷低地。受限於80\~100M等高線範圍。最大值較高51\~754&mu;/M<sup>3</sup>|

- 中華紙漿(AERMOD)

| ![zhonghuaTer.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/zhonghuaTer.PNG)|
|:-:|
| <b></b>|

- 和平水泥(file:///I:/home/kuang/AQMP/202201/20220401_固定污染源模式模擬技術審查研習會/02.高斯擴散模式模擬審查實務議題.pdf)

| ![hepingTer.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/hepingTer.PNG)|
|:-:|
| <b></b>|

### 煙流模式地形前處理遠端執行
- 因AERMOD地形前處理過程繁雜，又涉及美國地調所檔案特殊格式，解決方式：
  - 由環保署提供處理程式、處理結果、
  - 由遠端執行方式分享既有處理系統與結果
- [煙流模式的地形處理說明](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/REnTG_pathways/)
- [遠端執行](http://125.229.149.182/terrain.html)
- TEDS點源附近地形檔案處理結果
  - [TEDS10](http://umap.openstreetmap.fr/zh/map/twn1x1-aermap-results_593832#8/23.712/121.009)
  - [TEDS11](https://umap.openstreetmap.fr/zh/map/taiwan-aermap_11-points_730878#7/23.671/121.084)
