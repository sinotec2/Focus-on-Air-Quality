---
layout: default
title: CAMx vs CMAQ
parent: Models and Comparisons
grand_parent: Paper Reviews
nav_order: 1
last_modified_date: 2022-06-01 11:29:09
---

# CAMx vs CMAQ
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

## 模式選用與考量
### 模式概述
光化網格模式是目前最能完整反映大氣中衍生性空品項目之模式類型，模擬範圍可以到數百~千公里，解析度可以自數百公尺到數十公里，時間尺度由逐時到全年的模擬，均能在單一模式內完成。

化學反應包括光化反應、有機物反應、氣固態異相反應、液相反應，乾、濕沉降及雨、雪去除機制。次模式包括在線生物源、在線揚沙模式、在線海洋飛沫模式、重大點源次網格模式等等，可模擬大型點源可能造成都市及區域性之衍生性污染(環保署模式支援中心，2020年)，為重要的模式工具之一。

### 全球發展情況
全球目前運作中的光化網格模式包括
- 美國環保署發展維護的[CMAQ模式](https://www.epa.gov/cmaq)(Community Model for Air Quality)、
- 美國Rambol-Environ公司持續發展的[CAMx模式](https://www.camx.com/about/)(Comprehensive Airquality Model with eXtension)，
- 大陸中科院研發之[NAQPMS模式](http://www.dqkxqk.ac.cn/qhhj/ch/html/20140203.htm)、
- 日本研究單位發展的[SPRINTARS模式](https://sprintars.riam.kyushu-u.ac.jp/indexe.html)、
- 日本早期的[CFORS模式](https://www-cfors.nies.go.jp/~cfors/outline.html)(Chemical Weather Forecast System)、
- 澳洲SCIRO機構發展的[TAPM/CTM模式](https://www.cmar.csiro.au/research/tapm/docs/CSIRO-TAPM-CTM_UserManual.pdf)(The Air Pollution Model and CTM Chemical Transport Model)、以及
- 歐洲CAMS整合維運的CHIMERE、DEHM、EMEP、EURAD-IM、GEM-AQ、LOTOS-EUROS、MATCH等7項[叢集預報模式](https://atmosphere.copernicus.eu/regional-air-quality-production-systems)等等。

### 國內發展情況
- 依據環保署模式支援中心之模式說明(環保署模式支援中心，2014年)，該文納入的網格模式包括TAQM、Models-3 (CMAQ)、CAMx、UAM-V等網格模式。
- 其中CMAQ與CAMx仍陸續有發展計畫，可以順利搭配新版氣象模式(Weather Research and Forecasting Model, WRF)，且持續發展氣象偶合模式。
- 考量到模式原始碼的取得、計算資源的配合等因素，國內環評及環保單位規劃常使用的網格模式僅包括前述CMAQ及CAMx模式。 

### 科學差異
- [CAMx v6.10 and CMAQ v5.0.2](https://views.cira.colostate.edu/wiki/wiki/1061/camx-and-cmaq-technical-summary)

### 個案應用結果差異
- 至於二模式的表現，在全球各地都有比較的研究，主要的差異評析比較如表1，說明如后。

#### 表1		CAMx及CMAQ模式差異之比較

|文獻|項目|CAMx|CMAQ|評析|
|-|-|-|-|-|
|1997加州南灣案例模擬比較 ([Ralph et al., 2005][Ralph et al., 2005])|銨鹽|細粒銨鹽偏差0~-86%總銨鹽-5 ~ -53%|細粒銨鹽估計較準，但總銨鹽低估-50 ~ -60%|各有軒輊|
||硝酸鹽|高估20~118%|偏差-44~ +45%|CMAQ略佳|
||細粒硫酸鹽|-31~21%|低估-10~44%|CAMx略佳|
||總硫酸鹽|-27~-45%|-45~-55%|CAMx略佳|
|2010年1月中國(薛等人，2014年)|光化速率計算|在線(6.0)|離線(4.7.1)|全年計算在線計算較為方便|
||水平平流計算|PPM|Hyamo|差異不大|
||水平擴散計算|顯式同步|Multiscale|近距離差異不大|
||垂直對流計算|隱式尤拉|Vyamo|隱式準度較高|
||垂直擴散計算|隱式尤拉|ACM2_inline|隱式準度較高|
||氣膠化學機制|CF|aero5|CF較為保守|
||乾沉降機制|Wesely89|Aero_depv2|Wesely損失較小|
||相同條件下(PM<sub>2.5</sub>、硫酸鹽及硝酸鹽)模擬值之比較|較高(16.5、45.67、34.14%)|較低|電廠排放以SN為主，硫酸鹽及硝酸鹽為主要衍生性PM|
|德州臭氧模擬([Byun et al. 2007a][Byun et al. 2007], [Byun et al. 2007b][Byun et al. ppt])|垂直擴散|K|K+PBL 相似律|垂直擴散對臭氧模擬具敏感性|
|密爾瓦基都會2002年1/4/7/10月([Baker and Timin 2008][Baker and Timin 2008])|細懸浮微粒成分模擬與實測值比較(PS,PN)|偏差4~-71%、誤差1.05~1.47|偏差2~37%、誤差1.07~1.33|CAMx硫酸鹽符合度較高CMAQ硝酸鹽較佳|
||細懸浮微粒成分模擬相對結果|細粒硫酸鹽較高|細粒硝酸鹽、銨鹽、元素碳、有機碳較高|二模式相關係數r<sup>2</sup>硫酸鹽0.82、硝酸鹽0.59、銨鹽0.78、元素碳0.89、有機碳0.93|
|珠江三角洲2004年10月([Shen et al. 2011][Shen et al. 2011])|對實測臭氧的相關係數|0.74|0.73|CAMx略佳|
||常化偏差|8.8%|-8.5%|CAMx略高|
||常化誤差|37.9%|36.7%|CMAQ略佳|
||傳輸、乾沉降、化學反應及垂直擴散|CAMx較高、二模式R=0.92|CMAQ模擬結果普遍較CAMx為低，相差17%|入流邊界對CAMx較敏感|
|東北亞2016 /12比較([Itahashi et al. 2018][Itahashi et al. 2018])|硫酸鹽|較高|較低、增加金屬催化反應仍無增加氧化|CMAQ低估肇因濕沉降損失|
||SO<sub>2</sub>|較高|低估|CMAQ低估肇因乾沉降損失|
||煙流次網格模式|在線式能考慮多煙陣重疊|離線式預處理|CAMx略佳|
|美國東南部跨境傳輸減量規劃([Odman et al. 2020][Odman et al. 2020])|總NOx和發電機組NOx排放對下游O3的貢獻|APCA通常較大|歸零較不敏感|CAMx較敏感|
||上游州對下游未達標地點之關聯點數|較多|較少|CAMx較敏感|


資料來源：各參考文獻。本計畫彙整

## 模式比較個案說明
### 1997加州南灣案例之模擬比較([Ralph et al., 2005][Ralph et al., 2005])
- Environ公司([Rambol-Environ](https://ramboll.com/environment-and-health)前身)在美國統整研究委員會(CRC)資助下進行了CAMx與CMAQ的比較研究 ，
  - 氣象模式統一使用MM5模式的模擬結果，
  - 排放源使用CAMx-to-CMAQ程式以統一使用CARB網格排放資料庫及點源數據，
  - 最高解析度都設為5KM。
- 二模式對該案例最大臭氧濃度值(187 ppb)都為低估(CAMx -20%、CMAQ -50%)。
  - 低估理由為局部環流及外海高值臭氧並未在MM5解析出來。
  - 而就懸浮微粒而言，二模式也有一樣低估的情形。
- 就懸浮微粒成分而言，二模式對元素碳都有高估，肇因於觀測值的不確定性，有機碳則有-75~-85%之低估，肇因於排放清冊項目不足。
- CMAQ的細粒銨鹽估計較準，但總銨鹽低估-50~-60%，CAMx的細粒銨鹽估計偏差0~-86%，總銨鹽較佳-5~-53%，各有軒輊。
- 硝酸鹽表現以CMAQ較佳，常化偏差-44~ +45%，CAMx為高估20~118%。細粒硫酸鹽項目則以CAMx較佳-31~21%，CMAQ則為低估-10~44%。
- 總硫酸鹽項目二模式都有低估，CAMx(-27~-45%)略勝CMAQ(-45~55%)。
### 美國德州案例([Byun et al. 2007a][Byun et al. 2007], [Byun et al. 2007b][Byun et al. ppt])
- 美國休士頓大學曾以CMAQ(4.2.2)與CAMx (4.03)模擬德州的臭氧，研究發現，大體上二模式的表現並沒有太大的差異。由於該課題受VOCs特性的影響很大，而模式對VOCs的拆解有不同的作法，後者使用CBM IV，雖然具有碳數守恆的優勢，但前者使用SAPRC99有更多直接表示的VOCs化合物種，因此會有較為出色的模擬結果。
- 不過就化學反應機制的議題而言，在後來2個模式的更新版本，已經完全沒有差異了，CAMx亦可以使用SAPRC，且碳鍵機制(cb6)也加入SAPRC所用的內、外雙鍵、同時也加入苯、萜類等特定化合物，以降低化學機制選擇可能造成的差異。
- 其次，在垂直擴散項的模擬，基本上2個模式都是以K-theory計算垂直擴散，然而Kv值的計算，當時CMAQ是使用PBL相似法則，而CAMx則使用O'Brien (1970) 法計算。
- 後來版本的2個模式，在Kv計算差異之間也做了很大的修正。以CAMx 6而言，除了OB70之外亦有CMAQ ACM2, MYJ 及YSU等選項、端視前端氣象模式的邊界層選項而定。此外，還提供了kv_patch程式，以解決次網格局部土地使用差異所造成Kv的奇異值問題。

### 中國珠江三角洲案例([Shen et al. 2011][Shen et al. 2011])
- 在珠江三角洲的個案研究中，發現CMAQ(4.5.1)與CAMx(5.01)有高度的相似性，二者的相關係數R=0.92，然而CMAQ模擬結果普遍較CAMx為低，相差17% 。
- 這些差異主要有三個來源，包括乾沉降、化學反應及垂直擴散。該研究對CAMx的建議是在乾沉降計算方式的選項應該要多一些，而CMAQ的光解速率則應加強，以使臭氧的模擬更接近實際。
- 由於乾沉降是空氣污染的重要損失項，為保持模式的保守特性，此一項目若能保持低估，對於模式整體表現是比較有益。


### 東北亞二次氣膠之模擬([Itahashi et al. 2018][Itahashi et al. 2018])
- 本研究主要針對硫酸鹽氣溶膠 (SO<SUB>4</SUB><SUP>-2</SUP>) 進行比較分析，該物質是日本顆粒物的主要成分。
- J-STREAM階段第一階段
  - 日本模式間比對研究 J-STREAM 發現，雖然模式很好地捕捉到了 SO<SUB>4</SUB><SUP>-2</SUP>，但它在冬季被低估了。
  - 在 J-STREAM 的第一階段，我們改進了 Fe 和 Mn 催化的氧化，並部分改善了低估。
- 第二階段
  - 2016 年 12 月的冬季霧霾在名古屋和東京進行深入觀察，是第二階段的目標期。將CMAQ和CAMx模擬結果與日本觀測結果進行比較。
  - 統計分析表明，兩個模型都滿足建議的模型性能標準。
  - CMAQ 靈敏度模擬解釋了模型性能的改進。儘管通過金屬催化途徑和 CMAQ 中的 NO<sub>2</sub> 反應增加了水氧化，但 CMAQ 模擬的 SO<SUB>4</SUB><SUP>-2</SUP> 濃度低於 CAMx。
- 沉積解釋了這種差異。
  - 經分析CMAQ的SO<sub>4</sub><sup>-2</sup>濃度低於 CAMx 的原因是 CMAQ 中的SO<sub>2</sub> 濃度較低，而 SO<SUB>4</SUB><SUP>-2</SUP> 濕沉降量較高。
  - 乾沉降速度導致 SO<sub>2</sub> 濃度的差異。
  - 這些結果表明沉積在提高我們對環境濃度行為的理解方面的重要性。

### 美國東南部跨境傳輸減量規劃([Odman et al. 2020][Odman et al. 2020])
- 該研究以CAMx/CB6r2及CMAQ/CB05模式分析東南部10州（阿拉巴馬州、佛羅里達州、喬治亞州、肯塔基州、密西西比州、北卡羅來納州、南卡羅來納州、田納西州、弗吉尼亞州和西弗吉尼亞州）對臭氧 (O3) 的貢獻，以符合該國法規要求。
- 由於 2017 年O3設計值(DVF)已經公佈，因此該研究也檢討了EPA推薦的建模方法(CMAQ/CB05)的準確性。
- 一般來說，CAMx/CB6r2 模擬的 DVF 比 CMAQ/CB05 更高，平均差異為 0.5 ppb。因此，本研究確認美國東部的 24 個地點為 CAMx/CB6r2 未達標（DVF ≥76 ppb），而 CMAQ/CB05 只有 16 個地點。
- 使用監測站網格點的 ( relative response factors RRF) 而不是 附近3×3矩陣最大 RRF（EPA 提議的跨州空氣污染規則 (CSAPR) 建模中使用的方法）（EPA，2015a），後者會導致某些監測站的 DVF 更高，並且降低其他站的 DVF。
- 使用 CAMx人為污染源評估工具 (Anthropogenic Precursor Culpability Assessment APCA) 結果顯示，在順風狀態下，NOx 排放量對 O3 的貢獻超過 VOC。
- 使用 CAMx/APCA 以及 CMAQ/歸零模擬分別量化了東南各州的人為 NOx 排放總量和發電機組 (EGU) NOx 排放對下游 O3 的貢獻。
  - 從 CAMx/APCA 獲得的貢獻量通常大於從 CMAQ/歸零的結果。
  - 因此，由 CAMx/APCA 確定認為[重大貢獻][sig]的減量，可能對CMAQ/歸零法而言是微不足道的。   
  - 阿拉巴馬州、肯塔基州、密西西比州、田納西州、弗吉尼亞州和西弗吉尼亞州與 CAMx/APCA 的 2、3、1、1、6 和 5 個未達標地點相關聯。
  - 而CMAQ/歸零法只分析出肯塔基州、弗吉尼亞州和西弗吉尼亞州與 2、3 和 2 個未達標地點有關聯。
  - 此外，各項減量與改善顯著關係中，以EGU NOx 貢獻佔人為 NOx 貢獻總量的 10-55%最為重要。
- 東南部各州可以使用本研究中產生的信息來幫助制定“好鄰居”州實施計劃 (SIP)。

## Reference
- [Ralph et al., 2005][Ralph et al., 2005]
- [Byun et al. 2007a][Byun et al. 2007]
- [Byun et al. 2007b][Byun et al. ppt]
- [Shen et al. 2011][Shen et al. 2011]
- [Baker and Timin 2008][Baker and Timin 2008]
- [Itahashi et al. 2018][Itahashi et al. 2018]
- [Odman et al. 2020][Odman et al. 2020]

[Ralph et al., 2005]: <http://crcsite.wpengine.com/wp-content/uploads/2019/05/CRC-A-40-2_Final_7-11-05r.pdf> "Morris, R.E., Koo, B., Lau, S., Yarwood, G., and Way, R. (2005). Application of CAMx and CMAQ Models to the August - September, 1997 SCOS Episode (No. CRC Project A-40-2). Coordinating Research Council Atmospheric Impacts Committee."
[Byun et al. ppt]: <http://www.ruf.rice.edu/~eesi/scs/Byun.ppt> "Daewon Byun, Soontae Kim, Beata Czader, Seungbum Kim(2007) Simulation of Houston-Galveston Airshed Ozone Episode with EPA’s CMAQ, Institute for Multi-dimensional Air Quality Studies, University of Houston. "
[Byun et al. 2007]: <https://www.sciencedirect.com/science/article/pii/S1352231006008752> "Byun, D.W., Kim, S.-T., and Kim, S.-B. (2007). Evaluation of air quality models for the simulation of a high ozone episode in the Houston metropolitan area. Atmospheric Environment 41 (4):837–853. doi:10.1016/j.atmosenv.2006.08.038."
[Shen et al. 2011]: <https://www.researchgate.net/publication/255972051_Evaluation_and_intercomparison_of_ozone_simulations_by_Models-3CMAQ_and_CAMx_over_the_Pearl_River_Delta> "Shen, J., XueSong, W., Li, J., Yunpeng, L., and YuanHang, Z. (2011). Evaluation and intercomparison of ozone simulations by Models-3/CMAQ and CAMx over the Pearl River Delta. Science China-Chemistry 54:1789–1800. doi:10.1007/s11426-011-4390-z."
[Baker and Timin 2008]: <> "Kirk Baker and Brian Timin (2008). PM<sub>2.5</sub> SOURCE APPORTIONMENT COMPARISON OF CMAQ AND CAMX ESTIMATES. Presented at the 7th Annual Community Modeling & Analysis System (CMAS) Conference, UNC Institute for the Environment, Chapel Hill, NC."
[Itahashi et al. 2018]: <https://www.mdpi.com/2073-4433/9/12/488> "Itahashi, S., Yamaji, K., Chatani, S., Hisatsune, K., Saito, S., and Hayami, H. (2018). Model Performance Differences in Sulfate Aerosol in Winter over Japan Based on Regional Chemical Transport Models of CMAQ and CAMx. Atmosphere 9 (12):488. doi:10.3390/atmos9120488."

[Odman et al. 2020]: <https://www.researchgate.net/publication/341613008_Interstate_transport_of_ozone_in_eastern_United_States_An_analysis_of_the_impact_of_southeastern_states'_emissions_in_2017> "Odman, M., Qin, M., Hu, Y., Russell, A., and Boylan, J. (2020). Interstate transport of ozone in eastern United States: An analysis of the impact of southeastern states’ emissions in 2017. Atmospheric Environment 236:117628. doi:10.1016/j.atmosenv.2020.117628."
[sig]: <> "「顯著貢獻」為影響大於 2008 年 O3 NAAQS 的 1%（即≥0.76 ppb）"