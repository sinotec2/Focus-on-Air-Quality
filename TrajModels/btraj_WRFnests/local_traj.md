---
layout: default
title: 局部反軌跡成果分析
nav_order: 6
parent: WRF三維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-16 15:15:48
---

# 局部反軌跡成果分析

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

- 過去曾經針對高雄地區南北工業區燃燒塔排放進行WRF三維正軌跡通過[機率分析](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/4Linyuan3Dtraj/#林園臭氧事件污染源三維正軌跡分析)。
  - 唯該分析系針對汙染事件個案。
  - 且地區呈現明顯的日夜垂直運動差異
- 此處則以北部測站局部反軌跡為討論焦點
  - 排除境外軌跡
  - 時間不限、跨年度、只有季節區別
  - 其餘分析過程詳前述說明([三維反軌跡線之計算](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/bt2_DVP/)、[choose10.py](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/choose10/)、[km.py](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/km/)、以及[acc_prob.py程式說明](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/acc_prob/))

## 結果討論

| ![local_traj.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/local_traj.png)|
|:-:|
| <b>機器學習方法解析2017~2020年冬、春季臺灣北部近域氣團路徑。氣團軌跡終點為臺北盆地中的環保署中山站，高度50M，起點為觸地位置，高度為地面。藍色線為冬季分類結果，紅色線為春季結果，由於軌跡轉向時風速很慢，叢集結果有降低維度的傾向，點數不及10點。</b>|

### 起訖的高度

- 按照定義，只要軌跡線高度不落地，就會繼續向外延伸而成為其他**非本地來源**(即為**境外**)之分析結果。
- 圖中這2類叢集，都是來自臺灣地面、最後到達台北盆地中央測站之路徑。春季來自桃園近海、冬季則來自基隆地區。就解釋上有本地汙染的可能性。
- 此處雖然並未對測站的空品進行解釋，然而就軌跡線較短的結果來看，伴隨空品不良的可能性非常高。
- 由地面最後到達測站，似乎有較合理的解釋基礎。

### 起訖的時間

- 由到達測站的風向(西南及南)來看，為台北盆地清晨的風向，氣流為來自景美新店山區的山風。
- 如此倒推可知，起點則應為日間海風(春季)或者谷風(冬季)

### 途徑與地形效應

- 冬季軌跡
  - 略有環流的特徵，雖然起訖點相距20Km，接近封閉環流的型態。
  - 軌跡線在雪山山脈的北側、沿著山脈的走勢到達烏來一帶、入夜後則滯留山區、在該處轉向北行。
  - 垂直氣流並未將其帶到更高的高度，應為垂直運動受到抑制、不利擴散的天候。
- 春季軌跡
  - 桃園地區日間盛行海風，由於地勢平坦，海風可以跨越林口臺地邊緣，到達三峽、新店山區。
  - 同樣的，軌跡線在此轉向北行，隨著夜間(清晨)的山風到達市區。
