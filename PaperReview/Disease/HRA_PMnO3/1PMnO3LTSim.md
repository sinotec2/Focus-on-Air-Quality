---
layout: default
title: Long-term Sim. of PM&O3
parent: HRA for PM & O3 
grand_parent: Disease and Air Pollution
nav_order: 1
last_modified_date: 2022-06-13 09:29:35
---

# 衍生性污染物空品之長期模擬
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

為探討衍生性空氣品質項目(衍生性PM<sub>2.5</sub>、PM10、O3等)之健康風險，此處以光化模式應用在大範圍之健康風險計算，建立以疾病發生率(而不是死亡率)為指標的健康風險模型。本評估工作不考慮軌跡、箱型模式等其他選項，檢討現行應用中與發展中的模式，選擇合適的模式進行評估；其次依據目前可取得最完整的原始資料以建立模式所需要的排放、氣象、邊界、初始以及地理檔案。

## 模式選用與考量
### 模式概述
光化網格模式是目前最能完整反映大氣中衍生性空品項目之模式類型，模擬範圍可以到數百~千公里，解析度可以自數百公尺到數十公里，時間尺度由逐時到全年的模擬，均能在單一模式內完成。

化學反應包括光化反應、有機物反應、氣固態異相反應、液相反應，乾、濕沉降及雨、雪去除機制。次模式包括在線生物源、在線揚沙模式、在線海洋飛沫模式、重大點源次網格模式等等，可模擬大型點源可能造成都市及區域性之衍生性污染(環保署模式支援中心，2020年)，為重要的模式工具之一。

### 全球發展情況
全球目前運作中的光化網格模式包括
- 美國環保署發展維護的CMAQ模式(Community Model for Air Quality)、
- 美國Rambol-Environ公司持續發展的CAMx模式(Comprehensive Airquality Model with eXtension)，
- 大陸中科院研發之NAQPMS模式、
- 日本研究單位發展的SPRINTARS模式、
- 日本早期的CFORS模式(Chemical Weather Forecast System)、
- 澳洲SCIRO機構發展的TAPM/CTM模式(The Air Pollution Model and CTM Chemical Transport Model)、以及
- 歐洲CAMS整合維運的CHIMERE、DEHM、EMEP、EURAD-IM、GEM-AQ、LOTOS-EUROS、MATCH等7項叢集預報模式等等。
### 國內發展情況
- 依據環保署模式支援中心之模式說明(環保署模式支援中心，2014年)，該文納入的網格模式包括TAQM、Models-3 (CMAQ)、CAMx、UAM-V等網格模式。
- 其中CMAQ與CAMx仍陸續有發展計畫，可以順利搭配新版氣象模式(Weather Research and Forecasting Model, WRF)，且持續發展氣象偶合模式。
- 考量到模式原始碼的取得、計算資源的配合等因素，國內環評及環保單位規劃常使用的網格模式僅包括前述CMAQ及CAMx模式。 
- 至於二模式的表現，在全球各地都有比較的研究，主要的差異評析比較如表1，說明如后。

#### 表1 CAMx及CMAQ模式差異之比較

|文獻|項目|CAMx|CMAQ|評析|
|-|-|-|-|-|
|1997加州南灣案例模擬比較 ([Ralph et al., 2005][Ralph et al., 2005])|銨鹽|細粒銨鹽偏差0~-86% 總銨鹽-5~-53%|細粒銨鹽估計較準，但總銨鹽低估-50~-60%|各有軒輊|
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
|德州臭氧模擬(Byun; Byun et al. 2007)|垂直擴散|K|K+PBL 相似律|垂直擴散對臭氧模擬具敏感性|
|密爾瓦基都會2002年1/4/7/10月(Baker and Timin, 2008)|細懸浮微粒成分模擬與實測值比較(PS,PN)|偏差4~-71%、誤差1.05~1.47|偏差2~37%、誤差1.07~1.33|硫酸鹽符合度較高|
||細懸浮微粒成分模擬相對結果|細粒硫酸鹽較高|細粒硝酸鹽、銨鹽、元素碳、有機碳較高|二模式相關係數r<sup>2</sup>硫酸鹽0.82、硝酸鹽0.59、銨鹽0.78、元素碳0.89、有機碳0.93|
|珠江三角洲2004年10月(Shen et al., 2011)|對實測臭氧的相關係數|0.74|0.73|CAMx略佳|
||常化偏差|8.8%|-8.5%|CAMx略高|
||常化誤差|37.9%|36.7%|CMAQ略佳|
||傳輸、乾沉降、化學反應及垂直擴散|CAMx較高、二模式R=0.92|CMAQ模擬結果普遍較CAMx為低，相差17%|入流邊界對CAMx較敏感|
|東北亞2016 /12比較(Itahashi et al., 2018)|硫酸鹽|較高|較低
增加金屬催化反應仍無增加氧化|CMAQ低估肇因濕沉降損失|
||SO2|較高|低估|CMAQ低估肇因乾沉降損失|
||煙流次網格模式|在線式能考慮多煙陣重疊|離線式預處理|CAMx略佳|

資料來源：各參考文獻。本計畫彙整

[Ralph et al., 2005]: <http://crcsite.wpengine.com/wp-content/uploads/2019/05/CRC-A-40-2_Final_7-11-05r.pdf> "Morris, R.E., Koo, B., Lau, S., Yarwood, G., and Way, R. (2005). Application of CAMx and CMAQ Models to the August - September, 1997 SCOS Episode (No. CRC Project A-40-2). Coordinating Research Council Atmospheric Impacts Committee."

### [Ralph et al., 2005][Ralph et al., 2005]之早期比較
- Environ公司在美國統整研究委員會(CRC)資助下進行了CAMx與CMAQ的比較研究 ，氣象模式統一使用MM5模式的模擬結果，排放源使用CAMx-to-CMAQ程式以統一使用CARB網格排放資料庫及點源數據，最高解析度都設為5KM。
- 二模式對該案例最大臭氧濃度值(187 ppb)都為低估(CAMx -20%、CMAQ -50%)。低估理由為局部環流及外海高值臭氧並未在MM5解析出來。而就懸浮微粒而言，二模式也有一樣低估的情形。
- 就懸浮微粒成分而言，二模式對元素碳都有高估，肇因於觀測值的不確定性，有機碳則有-75~-85%之低估，肇因於排放清冊項目不足。CMAQ的細粒銨鹽估計較準，但總銨鹽低估-50~-60%，CAMx的細粒銨鹽估計偏差0~-86%，總銨鹽較佳-5~-53%，各有軒輊。
- 硝酸鹽表現以CMAQ較佳，常化偏差-44~ +45%，CAMx為高估20~118%。細粒硫酸鹽項目則以CAMx較佳-31~21%，CMAQ則為低估-10~44%。
- 總硫酸鹽項目二模式都有低估，CAMx(-27~-45%)略勝CMAQ(-45~55%)。

### 本評估工作之考量
雖然個別模式在增量的模擬結果仍然會有性質與少數的差異，然在環評應用中，都必須符合環保署所訂的性能評估規範，及經過環保署認可的程序。在測站上的表現上會趨於一致。

目前環保署委託台灣地區空氣品質預測及分析計畫使用的模式為WRF搭配CMAQ (如環保署近期委託辦理「臺灣空氣品質模式數據平台」計畫(成功大學，2019，即所謂公版模式計畫)，CMAQ確實在國內外學術界取得優勢之地位。
經期中階段報告之檢討比較，為考量能與其他同步進行之模式分析工作一齊比較，本評估分析採用CMAQv53。
## 氣象條件之模擬
對於多尺度的氣象模擬，目前選項仍以學術界通用之wrf為主。主要考量該模式為美國政府及學界持續投入發展、在國內各大學也列為教研之重要工具，具有較廣泛的支援應用。本評估工作之模擬方式說明如下：
### 版本選擇之考量
CMAQ的氣象前處理MCIP (5.0)模式有較高標準的限制，除了土地使用類別之外，對於wrfout的標題、模擬起始時間、時間標籤等，也會檢查其一致性(wrf 4.1~4.2)。以下分析使用新版的wrf (4.1.3 2019)進行，可以符合MCIP的要求。
### 模擬個案(時間)及範圍(空間)
針對空氣污染排放總量資料庫清冊(Taiwan Emission Data System, TEDS)年代選擇2019年全年，模式自2019/12/15開始模擬，每批次5天，各批次間重疊1天，可避免各批間因初始化造成的人為誤差。

空間上採巢狀網格設定，分別為東亞地區(解析度81 Km)、東南大陸(解析度27 Km)、臺澎金馬(解析度9 Km)、以及臺灣本島(解析度3 Km)等4層。各層皆以臺灣中央山脈為中心點採對稱分布，降低不同來源方向天氣系統的影響。本計畫位在南部地區，與北方邊界有充分的模擬空間，在盛行東北風之冬半年污染季節中可以有效降低邊界的影響。

### 模式初始及邊界條件、四階同化選項
- 土地利用資料使用美國地質調查局地表資料庫([USGS][USGS])，其依照USGS的24種土地種類進行分類。土地使用分類在CMAQ模式系統中也會需要。
- 初始邊界場資料依據美國國家環境預測中心(National Center for Environmental Prediction, [NCEP][NCEP])的6小時再分析場FNL 資料，解析度為1.0°×1.0°。
- 網格及測站四維資料同化(Four Dimension Data Assimilation, FDDA)依據NCEP的高空(ds351.0)及地面(ds461.0)之氣象觀測彙整結果，以及氣象局與環保署地面測站風速、風向與氣溫數據。OBSGRID同化程式採 Multiquadric scheme修正初始模擬預測值，使模擬結果更接近實際的觀測資料，而各層於每6小時進行一次修正。

[USGS]: <https://zh.wikipedia.org/zh-tw/美國地質調查局> "「美國地質調查局」是美國內政部轄下的科學機構，是內政部唯一純粹的科學部門，有約一萬名人員，總部設在維吉尼亞州里斯頓，在科羅拉多州丹佛和加利福尼亞州門洛公園設有辦事處。 美國地質調查局的科學家主要研究美國的地形、自然資源和自然災害與應付方法；負責生物學、地理學、地質學和水文學四大科學範疇。"
[NCEP]: <https://www.weather.gov/ncep/> "美國國家環境預測中心、上級機構： 國家氣象局、下屬單位： 風暴預測中心， 氣象預報中心， Climate Prediction Center、等等"
### 模擬結果檢討
依照空氣品質規範要求檢討wrf 2019年模擬結果如表1所示，各月份測站的符合度除8/11~12月之風速外，皆可達72%以上，大致能符合規範60%以上要求。

#### 表1	 wrf 模擬結果之測站符合度檢討

|月|6項綜合符合度|溫度||風速||風向||
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|||MBE|MAGE|MBE|RMSE|WNMB|WNME|
|1|89.40|83.30|97.80|70.00|90.00|95.60|100.00|
|2|95.00|88.90|97.80|86.70|96.70|100.00|100.00|
|3|95.90|94.40|97.80|85.60|97.80|100.00|100.00|
|4|96.90|93.30|97.80|91.10|98.90|100.00|100.00|
|5|95.90|94.40|97.80|85.60|98.90|98.90|100.00|
|6|96.30|93.30|97.80|92.20|95.60|98.90|100.00|
|7|91.10|94.40|97.80|67.80|88.90|97.80|100.00|
|8|86.50|93.30|97.80|54.40|75.60|97.80|100.00|
|9|89.10|93.30|97.80|61.10|83.30|98.90|100.00|
|10|90.00|91.10|97.80|67.80|86.70|96.70|100.00|
|11|84.60|91.10|97.80|50.00|72.20|96.70|100.00|
|12|86.10|95.60|97.80|50.00|74.40|98.90|100.00|
|avg|91.4 |92.2 |97.8 |71.9 |88.3 |98.4 |100.0 |

單位：%

  1. 值偏差(Mean Biased Error, MBE)；
  1. 配對值絕對值偏差(Mean Absolute Gross Error, MAGE)；
  1. 配對值均方根誤差(Root Mean Square Error, RMSE)；
  1. 風向配對值標準化偏差(Wind Normalized Mean Bias, WNMB)；
  1. 風向配對值標準化絕對值偏差(Wind Normalized Mean Error, WNME)

3項氣象要素中，對高空煙流模擬以風向最為重要，此處的符合度也較高。一般WRF模擬之風速有高估的情形，尤其在北部及中部之濱海測站。本計畫位在台灣南部，因嘉南平原的遮蔽效應，受風速影響較中北部為低，高估風速對南部、內陸地區之空品模擬敏感性，預期應為有限。
 

## 空氣品質之初始與邊界條件(ICBC)
- 網格模式雖採巢狀網格之做法，可以有效減少境外污染造成的干擾，但仍要有最大範圍模擬所需的空氣品質初始(IC)與邊界條件(BC)。CMAQ可以使用[WACCM][WACCM]、[GEOS-chem][GEOS-chem]、[CAM-chem][CAM-chem]等全球模式之模擬結果，也可以選用固定值之組合(profile)做為敏感性測試。
- 美國大氣院校合作(UCAR)發展營運之完整大氣社群氣候模式 ([WACCM][WACCM]) 是一個綜合數值模型，涵蓋從地球表面到熱氣層的高度範圍。WACCM 的開發是跨部門合作，整合了HAO 的高層大氣模式、ACOM 的中溫層大氣模式和 CGD 的對流層模式的部分模組，使用 NCAR 社群地球系統模型 (CESM) 作為通用數值框架，其化學模組則為MOZART-4。本評估工作乃下載WACCM模式結果做為D1之ICBC。
- 化學機制方面，標準的MOZART-4有85個氣態污染物，12個氣膠成分，39條光化反應以及157條氣態反應，碳鍵機制採lump法，VOCs包括3個烯烴與烷烴類物質，以及4碳以上與芳香烴類物質(BIGALK, BIGENE及TOLUENE)。
- 該模式水平空間解析度視不同機器平台略有差異，一般而言介於2.5 ~ 2.8度之間，高度為Non_Hydrostatic SIGMA-P座標從最底層(1000HPa到模式頂層4.50E-6 HPa) 有89層，檔案儲存的時間解析度則為6小時。
- 由於CMAQ目前只有公開單向巢狀網格模式版本，因此D1模擬完之後，另就模擬結果進行進一步處理，裁剪出D2範圍之BC檔，以此類推，直到D4範圍。D4邊界條件中的臭氧，則使用更高解析度的ECMWF 再分析數據內插值，以提高模擬的精準度。
- 由於CMAQ每批次模擬結束前，皆會將瞬時化學成份詳細值，寫入結果中，此檔案即為下一批次模擬的初始檔IC，只需適當連結不必另外處理。

[GEOS-chem]: <https://geos-chem.seas.harvard.edu/> "GEOS-Chem Community Mission: to advance understanding of human and natural influences on the environment through a comprehensive, state-of-the-science, readily accessible global model of atmospheric composition."
[CAM-chem]: <https://wiki.ucar.edu/display/camchem/Home> "The Community Atmosphere Model with Chemistry (CAM-chem) is a component of the NCAR Community Earth System Model (CESM) and is used for simulations of global tropospheric and stratospheric atmospheric composition."
[WACCM]: <https://www2.acom.ucar.edu/gcm/waccm> "The Whole Atmosphere Community Climate Model (WACCM) is a comprehensive numerical model, spanning the range of altitude from the Earth's surface to the thermosphere"

##	排放量數據
網格模式使用排放量的檢核重點包括開發計畫本身要探討的污染排放、還包括本地與境外之背景排放量。本評估工作之作法分項說明如下：
### 開發計畫污染源排放
除未來之燃氣計畫與中間期程之外，網格模式部分也探討既有燃煤、燃氣機組排放對環境的衝擊，組合方式如前述4個運轉階段。未來計畫則採環評承諾濃度計算，現況則按照TEDS 11之2019年數據，包括各機組逐時之變化情形。
### 本地背景污染源排放
- 電廠煙流造成環境氧化物及粒狀物濃度影響，同時煙氣轉化也倚靠背景既有其他污染源所造成的氧化物及粒狀前驅物，因此當地背景排放對電廠增量之估算亦非常重要。
- 本評估工作採環保署公開之TEDS 11資料庫，包括其排放時間變化、業別等設定，輸入排放模式進行數據檔案之準備。地面源之NO2及VOCs (以單鍵物質PAR為代表)空間分布如圖5.2.3-1所示。
- 由圖中可以看到NO2在高速公路與都會區有較高的排放量，應為柴油車與高速行駛車輛之排放。南高屏地區則以高雄市臨港地區較高，相較北部新北、桃園等大範圍高NO2排放量地區，南、高、屏地區的NO2排放量較低(面、線源)。
- 圖中顯示PAR的分布則較為均勻，也是北部排放較南部為高。此外山區排放量不低，應為植物呼吸作用之排放。






 	 
(a)NO2	(b)PAR
#### 圖1	2019年9月d4範圍TEDS 11基準排放量之分布(gmole/s)

### 東亞地區之污染排放
- 本評估工作採日本環境研究所公開之REAS資料庫([REAS, 2020][REAS, 2020]、[Kurokawa and Ohara 2020][Kurokawa and Ohara 2020])，除了考慮其於2019/12/4公開REAS3.1版之外，其資料年代(2015)也與本評估工作基準年2019最為接近，同時該機構對於東亞電廠逐月的排放量有較佳的掌握，與本評估工作關切項目有相同的目標。
- 進一步分析該排放數據庫，發現具有顯著的月份差異，大體上粒狀物、硫氧化物與氮氧化物等與能源有關項目是秋冬季高、夏季低，可能與大陸與東北亞地區的冬季取暖現象有關，而氨氣(生物源指標)則以夏季較高、冬季較低。
- 因此本評估工作乃以各網格排放量之月均值與氣溫變化的回歸關係為基準，套用wrf模擬各地逐時之氣溫，建立東亞排放量之逐時變化，以降低2015年與2019年之間的可能差異。詳[Global/Regional Emission/ASia/地面排放檔之轉換@FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/REAS/reas2cmaq/)。
- REAS在船舶排放部分有所不足，此項目乃參考芬蘭氣象研究所之研究，該研究應用各主要港口AIS數據，配合衛星觀測反衍，推估全球2015年逐日之船舶網格排放量([Grigoriadis et. al 2020][Grigoriadis et. al 2020])，詳見[全球船隻排放量之處理@FAQ](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/FMI-STEAM/)。

[REAS, 2020]: <https://www.nies.go.jp/REAS/index.html#REASv3.2.1> "日本國立環境研究所 Data Sets:REASv3.2.1"
[Kurokawa and Ohara 2020]: <https://doi.org/10.5194/acp-20-12761-2020,> "Kurokawa, J. and Ohara, T.: Long-term historical trends in air pollutant emissions in Asia: Regional Emission inventory in ASia (REAS) version 3, Atmos. Chem. Phys., 20, 12761-12793, https://doi.org/10.5194/acp-20-12761-2020, 2020."

[Grigoriadis et. al 2020]: <> "Grigoriadis, A., Mamarikas, S., Ioannidis, I., Majamäki, E., Jalkanen, J.-P., and Ntziachristos, L. (2021). Development of exhaust emission factors for vessels: A review and meta-analysis of available data. Atmospheric Environment: X 12:100142. doi:10.1016/j.aeaoa.2021.100142."

##	性能評估符合度
- 將wrf模擬結果、MOZART模擬結果、東亞以及TEDS 11排放數據處理結果，輸入CMAQ模式進行模擬，與測站實測值進行比較，檢討是否符合空品模式模擬規範之性能評估目標要求。
- 本評估工作完成了2019年CMAQ背景濃度的模擬與必要之校調，結果之符合程度說明如表5.3-1所示。
- 此處為提高模式模擬的符合度，適度針對測站所在網格排放進行調整，依照模式模擬規定，須在環保審查時提出調整的數量及項目。

#### 表2 	2019年網格模式模擬台灣地區測站模式性能之符合度

|月份|總評|O<sub>3</sub>|||PM10||PM<sub>2.5</sub>||NO2||NMHC||SO2||
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|||MB|MNB|MNE|MFB|MFE|MFB|MFE|MNB|MNE|MNB|MNE|MNB|MNE|
|01|87.6|94.8|98.3|98.3|98.3|100|89.7|96.6|89.7|98.3|81.5|96.3|86.2|100|
|02|85.2|94.8|93.0|98.2|93.1|100|84.5|89.7|86.2|100|81.5|81.5|87.9|98.3|
|03|89.1|93.1|96.6|100|98.3|100|86.2|96.6|91.4|100|96.3|100|98.3|100|
|04|89.1|91.4|93.1|96.6|98.3|100|89.7|98.3|93.1|100|100|100|98.3|100|
|05|87.5|91.4|86.2|98.3|93.1|100|87.9|94.8|93.1|100|96.3|100|94.8|100|
|06|86.1|86.2|94.8|98.3|87.9|100|79.3|89.7|94.8|100|96.3|100|91.4|100|
|07|87.7|94.8|96.6|100|93.1|100|84.5|89.7|94.8|100|96.3|100|89.7|100|
|08|86.1|91.4|91.4|98.3|91.4|100|82.8|87.9|93.1|96.6|92.6|96.3|93.1|100|
|09|87.1|98.3|100|100|98.3|100|86.2|91.4|89.7|100|81.5|81.5|87.9|98.3|
|10|88.7|98.3|100|100|100|100|93.1|100|89.7|100|81.5|81.5|89.7|100|
|11|86.4|93.1|93.1|100|96.6|100|87.9|96.6|87.9|98.3|81.5|81.5|89.7|98.3|
|12|88.0|94.8|98.3|100|98.3|100|87.9|96.6|91.4|100|85.2|92.6|87.9|100|
|全年|87.4 |93.5 |95.1 |99.0 |95.6 |100 |86.6 |94.0 |91.2 |99.4 |89.2 |92.6 |91.2 |99.6 |


- 單位：%
- 非配對峰值常化偏差(Maximum peak normalized Bias, MB)、
- 配對值常化偏差(Mean Normalized Bias, MNB)、
- 配對值絕對常化誤差(Mean Normalized Error, MNE)、
- 配對值分數偏差(Mean Fractional Bias, MFB)、
- 配對值絕對分數誤差(Mean Fractional Error, MFE)

## 長期鄉鎮平均之PM與O<sub>3</sub>空氣品質
分析臺南市、高雄市及屏東縣等3縣市108個鄉鎮區，年度含蓋2007~2017年共11年，PM<sub>2.5</sub>及O<sub>3</sub>濃度乃讀自CAM-chem ([Community Atmosphere Model][CAM-chem]) 模式模擬結果，並以環保署在縣市測站之年平均值進行校正，作為相關性分析之依據。

由於歷年之空品模擬已經在NCAR系統架構中持續進行，全球數據下載、處理分析、與校正之方法與過程，詳見[CAM-chem模式結果之讀取及應用](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/CAM-chem/)。

### 時間趨勢
- CAM-chem模擬結果經校正調整後臺灣各空品區的歷年平均值

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/box_AQDobs.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/box_AQDsim.png)|
|:--:|:--:|
| <b>環保署測值</b>|<b>CAM-chem模擬校正調整後</b>|

### 空間分布
- 臺灣各鄉鎮區之平均值

| ![recm_byTown.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/recm_byTown.PNG)|![CAM_byTown.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CAM_byTown.PNG)|
|:--:|:--:|
|<b>環保署模擬2019平均值</b>|<b>CAM-chem模擬結果經校正調整後的歷年平均值</b>|

