---
layout: default
title: 煙流受地形效應之影響
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 3
last_modified_date: 2022-05-16 09:42:56
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

- 臺灣地區空品不良日數逐月變化
  - 行向(縱)：自北到南測站
  - 列向(橫)：1~12月
  - 季節變化：冬季(9月~隔年4月)高、6~8月低

| ![TCCIP第34期電子報_圖2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TCCIP第34期電子報_圖2.png)|
|:--:|
| <b>2005年至2017年臺灣環保署一般測站空氣品質指標不良達橘燈以上（AQI > 100，對敏感族群不健康）之月平均日數統計，(a)臭氧（O<sub>3</sub>）指標，(b)細懸浮微粒（PM<sub>2.5</sub>）指標。([蔡等2019][蔡等2019])</b>|

[蔡等2019]: <https://tccip.ncdr.nat.gov.tw/km_newsletter_one.aspx?nid=20191202172107> "蔡宜君、謝佩蓉、李貞潁、許晃雄，臺灣空氣品質變化與氣候變遷, 2019/12/01 臺灣氣候變遷推估資訊與調適知識平台電子報034期"

### 日夜變化
- 中\~小、都會區尺度

| ![Pendergast1.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/Pendergast1.PNG)|
|:--:|
| <b>日夜加熱差異造成的環流與空污現象([Pendergast 1984][Pendergast 1984] in [Atmospheric science and power production][Randerson 1984])</b>|

[Pendergast 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Malcolm M. Pendergast, 1984, Chap. 2, METEOROLOGICAL FUNDAMENTALS, in Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."

[Randerson 1984]: <https://www.osti.gov/biblio/6503687-atmospheric-science-power-production> "Randerson, D. (1984). Atmospheric science and power production (No. DOE/TIC-27601). USDOE Technical Information Center, Oak Ridge, TN."
- 林園臭氧事件與氣流軌跡線
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

### CTDMPLUS 
| ![CTDMPLUS.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CTDMPLUS.PNG)|
|:-:|
| <b>([Perry 1992][Perry 1992])</b>|

[Perry 1992]: <https://www.jstor.org/stable/26186577> "Perry, S.G. (1992). CTDMPLUS: A Dispersion Model for Sources near Complex Topography. Part I: Technical Formulations. Journal of Applied Meteorology (1988-2005) 31 (7):633–645."


### AERMOD 的地形模擬

| ![AERMOD1.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/AERMOD1.png)|
|:-:|
| <b>([Lin et. al 1974][Lin et. al 1974])</b>|
| ![AERMOD2.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/AERMOD2.png)|
| <b>([Lin et. al 1974][Lin et. al 1974])</b>|
