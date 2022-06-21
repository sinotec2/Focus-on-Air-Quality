---
layout: default
title: 開發計畫衍生性污染物健康風險評估
parent: HRA for PM & O3
grand_parent: Disease and Air Pollution
nav_order: 4
last_modified_date: 2022-06-16 13:38:36
---

#	衍生性空氣品質模式應用於地區疾病負荷之風險評估
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

[曠永銓][A1]、[蘇富榮][A2]、[潘文驥][A3]、[吳政宏][A4]

### 摘　要

在環保署健康風險評估技術規範框架之外，近年來對於火力電廠大範圍、衍生性空氣品質(包括PM<sub>2.5</sub>及O<sub>3</sub>二項)對疾病負荷的增加，亦多所關切。本文蒐集2007\~2017年全民健保研究資料庫中南、高、屏3縣市108個鄉鎮區與空氣污染相關的慢性疾病發生率數據，包括慢性阻塞性肺疾病(CODP)、下呼吸道感染、缺血性心臟病、中風、及第二型糖尿病(T2DM)等5項。彙整同一年期CAM-chem在臺灣地區的模擬結果並進行校正，以建立鄉鎮區基線空氣品質變化趨勢，以探討疾病發生與空氣品質的關係與發病斜率，並應用於南部地區疾病風險分析。

研究結果顯示，研究範圍內5項疾病中只有CODP與PM<sub>2.5</sub>之正相關較為顯著，計畫電廠對臺南市龍崎區的COPD疾病的發生最多有2.7%的正面效應，疾病發生率則以高雄市苓雅區增加4.18×10<sup>-4</sup>/yr最高，此值為該區現況發生率的之0.79%。5項疾病僅以T2DM對O<sub>3</sub>具正相關，其餘皆負相關，計畫電廠造成屏東縣霧臺鄉增加8.09×10<sup>-4</sup>/yr最高，然疾病發生率變動都在0.65%以下。

關鍵字：光化網格模式、衍生性細懸浮微粒、PM<sub>2.5</sub>、臭氧、O<sub>3</sub>、疾病負荷、風險分析

## 一、前　言

世界衛生組織全球疾病負荷研究(Global Burden of Disease,
GBD)認定環境中的PM<sub>2.5</sub>
(空氣動力直徑小於2.5微米之懸浮物)與疾病負荷的增加有關(Murray et.
al，2020)。即便我國與鄰近國家已經將PM<sub>2.5</sub>列為空氣品質標準項目且具改善成效，大型開發計畫環評過程仍然遭受質疑而延宕審查。除了按章(環保署，2011)進行健康風險評估(Health Risk Analysis HRA)之外，電廠排放空氣污染物在大氣中因光化學反應生成硫酸鹽、硝酸鹽及銨鹽等衍生性PM<sub>2.5</sub>及O<sub>3</sub>(臭氧)等，亦被認為具有更大範圍之疾病負擔風險。

HRA程序大致上可以區分為3階段：

- (1)開發計畫增量之模式模擬分析、
- (2)癌症或疾病之發生斜率分析、
- (3)二者相乘以進行風險分析。

由於HRA空氣品質指標為長時間平均值，而長時間大範圍PM<sub>2.5</sub>及O<sub>3</sub>的增量模擬耗費大量計算資源，環保署現正積極準備公告標準模式與作業方式(公版模式)。其次GDB研究以死亡率為指標與HRA以疾病發生率(致癌率)不符，而該研究使用國外疾病早期數據，與我國實際情況也不相符，這些都有待整併與發展。

由於現行HRA規範無法應用在大範圍、衍生性污染物的疾病風險評估，本文乃依照環保署修正公告之空氣品質模式模擬規範(下稱模式規範，環保署，2021a)，選擇多尺度空氣品質模式系統(CMAQ, USEPA，2020)模式進行前述評估

- 階段(1)計畫電廠的增量模擬評估，
- 階段(2)則蒐集2007\~2017年全民健保研究資料庫中與空氣污染相關的慢性疾病發生率數據，包括GDB研究提出之慢性阻塞性肺疾病(COPD)、下呼吸道感染(LRTI)、缺血性心臟病(IHD)、中風(Stroke)、及第二型糖尿病(Type 2 diabetes mellitus, T2DM)等5項疾病，搭配美國大氣院校合作(UCAR)社群大氣化學模式(CAM-chem, UCAR，2022a)在臺灣地區的模擬結果，經校正後以求得疾病發生與空氣品質的長期關係與發病斜率，並在
- 階段(3)應用於計畫電廠影響地區的疾病發生率風險分析。

計畫電廠選擇以臺電公司興達發電廠燃氣機組更新改建計畫為對象。該計畫為國內減煤增氣能源轉型政策重要指標，旨在降低環境與健康衝擊，已於2019.07.17通過環境影響評估審查。

## 二、衍生性空氣品質之長期模擬

### (一) 2019年逐時氣象場模擬

此處使用天氣研究預報模式(WRF4.1.3
UCAR，2022b)按照環保署公告之基準年代2019年進行全年模擬(環保署，2021b)。模擬自2018/12/15開始，每批次5天，各批次間重疊1天，可避免各批間因初始化造成的誤差。

空間上採雙向同步4階巢狀網格設定，分別為東亞地區(解析度81Km)、東南大陸(解析度27 Km)、臺澎金馬(解析度9 Km)、以及臺灣本島(解析度3Km)等4層。各層皆以臺灣中央山脈為中心點採對稱分布，降低不同來源方向天氣系統的影響。

土地利用資料使用美國地質調查局地表([USGS](https://zh.wikipedia.org/zh-tw/美國地質調查局))資料庫24種土地種類進行分類。初始邊界場資料依據美國國家環境預測中心([NCEP](https://www.weather.gov/ncep/))的6小時再分析場FNL資料，解析度為1.0°×1.0°。

網格及測站四維資料同化依據NCEP的高空(ds351.0)及地面(ds461.0)之氣象觀測彙整結果，以及氣象局與環保署地面測站風速、風向與氣溫數據。同化採多二次函數法修正初始模擬預測值，使模擬結果更接近實際的觀測資料，而各層於每6小時進行一次修正。

依照模式規範要求檢討全年模擬結果，各月份測站的符合度除8/11\~12月之風速外，皆可達72%以上，能符合模式規範60%以上要求。

3項氣象要素中，對高空煙流模擬以風向最為重要，此處的符合度也較高。一般WRF模擬之風速有高估的情形，尤其在北部及中部之濱海測站。本計畫位在台灣南部，因嘉南平原的遮蔽效應，受風速影響較中北部為低，高估風速對南部、內陸地區之空品模擬敏感性應不致太高。

### (二)空氣品質之初始與邊界條件(ICBC)

CMAQ雖也採巢狀網格之做法以減少境外污染的干擾(單向D1、D2、D4)，但仍需建立最大範圍(D1)模擬之初始(IC)與邊界條件(BC)，為此本文以完整大氣社群氣候模式([WACCM](https://www2.acom.ucar.edu/gcm/waccm),
UCAR，2022c)模式結果進行內插。D4邊界的O<sub>3</sub>，則使用更高解析度的歐洲中期天氣預報中心再分析數據(ECWMF，2022)進行內插值，以提高模擬的精準度。

### (三)排放量數據

開發計畫排放量採環評承諾濃度計算。本地其他背景污染源排放採TEDS 11(環保署，2022a)資料庫，包括其排放時間變化、業別等設定，輸入排放模式進行數據檔案之準備。

東亞地區之污染排放採日本環境研究所於2019/12/4公開之REAS3.1資料庫([REAS, 2020](https://www.nies.go.jp/REAS/index.html#REASv3.2.1)、[Kurokawa and Ohara 2020](https://doi.org/10.5194/acp-20-12761-2020,))，考量該機構對於東亞電廠逐月的排放量有較佳的掌握，與本評估工作主題相關。進一步以各網格排放量之月均值與氣溫變化的回歸關係為基準，套用WRF模擬各地逐時之氣溫，建立東亞排放量之逐時變化，以降低基準年代之間的差異。船舶排放部分，採納芬蘭氣象研究所逐日之船舶網格排放量(Grigoriadis
et al. ，2021)。

### (四)性能評估符合度

將WRF模擬結果、WACCM模擬結果、東亞以及TEDS
11排放數據處理結果，輸入CMAQ模式進行模擬，與測站實測值進行比較，檢討是否符合模式規範之性能評估目標要求。模擬結果符合規範之測站數比例如表1，符合度均能達到8成以上，符合模式規範的目標60%。

#### 表1 2019年網格模式模擬台灣地區測站模式性能之符合度，單位：%

|性能指標|MB|MNB/MFB|MNE/MFE|
|:-:|:-:|:-:|:-:|
|O<sub>3</sub>|93.5 |95.1|99.0|
|PM10||95.6 |100 |
|PM<sub>2.5</sub>||86.6 |94.0 |
|NO2||91.2 |99.4 |
|NMHC||89.2 |92.6 |
|SO2||91.2 |99.6 |

- MB:非配對峰值常化偏差(Maximum peak normalized Bias)
- MNB:配對值常化偏差(Mean Normalized Bias)
- MNE:配對值絕對常化誤差(Mean Normalized Error)
- MFB:配對值分數偏差(Mean Fractional Bias)
- MFE:配對值絕對分數誤差(Mean Fractional Error)

### (五)長期鄉鎮平均之PM<sub>2.5</sub>與O<sub>3</sub>空氣品質

2019年全年PM<sub>2.5</sub>與O<sub>3</sub>空間分布模擬結果如圖1與圖2所述，由於環保署公版模式模擬結果於2022年2月17日公開(環保署，2022b)，乃將其並列比較。

| ![recm_byTown.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/recm_byTown.PNG){:width="360px"}|![cmaqPMfT.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cmaqPMfT.png){:width="360px"}|
|:--:|:--:|
|<b>環保署模擬結果</b>|<b>本文模擬結果</b>|



#### 圖1 2019年臺灣各鄉鎮區PM<sub>2.5</sub>之平均值

圖1顯示大致PM<sub>2.5</sub>模擬結果都能符合西高東低、南高北低的趨勢，可以顯示出雲雨與季風對PM<sub>2.5</sub>的影響，唯本文模擬結果略低於環保署公版模式，可能因為公版模式取得大陸學界推估之排放量，相對本文排放掌握度較低。

圖2顯示二者在平原濱海地區有較接近的結果，山區則有高估。由於本文邊界條件使用了ECMWF數據而有較準確，而山區高估可能因WRF低估雲雨現象造成光化現象過度活躍。

| ![recm_byTown.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/recmO3T.png){:width="360px"}|![cmaqPMfT](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/cmaqO3T.png){:width="360px"}|
|:--:|:--:|
|<b>環保署模擬結果</b>|<b>本文模擬結果</b>|

#### 圖2 2019年臺灣各鄉鎮區O<sub>3</sub>之平均值

### (六)CAM-chem模式模擬結果分析

分析2007\~2017年共11年CAM-chem模式PM<sub>2.5</sub>及O<sub>3</sub>濃度之模擬結果，並以環保署在縣市測站之年平均值進行校正，其北(N)、中(C)、南(S)空品區平均值每2年之長期趨勢如圖3所示。選擇CAM-chem模式乃考量資料年代的覆蓋性。

| ![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/box_AQDobs.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/box_AQDsim.png)|
|:--:|:--:|
| <b>環保署測值</b>|<b>CAM-chem結果</b>|

#### 圖3 環保署及CAM-chem PM<sub>2.5</sub>長期趨勢

圖3顯示實測與模擬值都能呈現出北、中、南逐漸增加的趨勢，年度間則呈現出逐漸下降。唯CAM-chem模擬結果即使經過調整，最大值可以與觀測接近，平均值仍有低估。由於此處特別使用其年度間差異進行統計分析，整體性低估尚不致於造成困擾。

### (七)CAM-chem模擬結果之空間分布

圖4為2007\~2017年CAM-chem模式模擬臺灣地區範圍PM<sub>2.5</sub>及O<sub>3</sub>之平均濃度。雖然南部地區濃度略有低估，然整體分布可以反應前述CMAQ結果的特徵。

| ![CAM_byTown.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/CAM_byTown.PNG){:width="360px"}|![y_s_vO3T.csv.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/y_s_vO3T.csv.png){:width="360px"}|
|:--:|:--:|
|<b>PM<sub>2.5</sub> (μg/m<sup>3</sup>)</b>|<b>O<sub>3</sub></b>|

#### 圖4經調整後CAM-chem平均值之空間分布

## 三、南部地區5項空污疾病基本調查

### (一)疾病發生與PM<sub>2.5</sub>的相關性

根據全民健康保險研究資料庫200萬人抽樣檔中之「全民健保處方及治療明細檔_門急診」檔案(衛福部統計處，2014)，按前述5種疾病之國際疾病傷害及死因分類標準第九與第十版代碼，篩選2007到2017年在臺南市、高雄市及屏東縣的看診紀錄、依照年齡分成20、30、40、50與60歲以上五個區間與性別罹病人數，串接總人口數，計算疾病粗發生率(crude incidence)。並針對年齡及性別進行校正以計算標準化發生率(standardized incidence)。此數據庫與對應年度、行政區之PM<sub>2.5</sub>年均值進行相關性分析。結果如表2所示。

由地區平均狀況而言，後2項中風及T2DM為負相關，而呈現正相關的行政區數只占24.07\~ 29.63%。大多數地區因社經條件改善，生活、工作壓力、飲食習慣的變遷，反而造成疾病發生率提高，而此趨勢伴隨PM<sub>2.5</sub>逐年改善，可說並無因果關係。

表2 南部鄉鎮區之疾病發生率與PM<sub>2.5</sub>年均值之相關性分析
|疾病名稱|南部地區平均斜率||相關係數(r<sup>2</sup>)|正相關鄉鎮區數占3縣市比例|
|:-:|:-:|:-:|:-:|:-:|
||<p>絕對發生率</p>%/yr/(10 &mu;g/m<sup>3</sup>)|<p>常態化發生率</p>%/(10 &mu;g/m<sup>3</sup>)||%|
|慢性阻塞性肺疾病(COPD)|0.61|31.6194|0.27|63.89|
|下呼吸道感染(LRTI)|3.24|-11.5037|0.32|53.7|
|缺血性心臟病(IHD)|0.32|-4.0296|0.30|48.15|
|中風(Stroke)|-0.23|-87.7956|0.31|29.63|
|糖尿病(Diabetes)|-2.31|-22.1426|0.38|24.07|

前3項疾病之地區平均斜率絕對值為正值，每種疾病有其嚴重程度及發生率之特性，以LRTI最高，COPD次之、IHD最低。大致上地區有近半數以上鄉鎮區的斜率是大於0的，其中以COPD占比最高，達63.89%，值得重視。

將各行政區的疾病發生率以11年之平均值予以常態化，探討各年度的變動敏感性，其斜率正負分布情形與前述發生率之斜率有很大的出入，地區平均值僅有COPD維持正值，其餘疾病則皆為負值，顯示各行政區間的疾病發生率絕對值有很大的差異。依據臺灣胸腔暨重症加護醫學會的衛教知識，COPD與長期吸煙、二手煙有最大的關係，近年來政府在山地鄉的衛教工作顯有成就，逐步改善了該地區COPD的發生。搭配背景PM<sub>2.5</sub>濃度的降低，因而顯示出正向的相關性。

### (二)慢性阻塞性肺疾病對PM<sub>2.5</sub>罹病斜率分布

由上述討論可以得知，5項疾病中以CODP與PM<sub>2.5</sub>的正相關較為顯著，其他應無討論的必要。圖5為發生率斜率之空間分布，包括發生率絕對值及其年度變動。

| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/LungDiseasePar2.csv.png)| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/LungDiseaseParN2.csv.png)|
|:-:|:-:|
| <b>(a) 發生率絕對值(unit=1/yr/(&mu;g/m<sup>3</sup>))</b>| <b>(b)常態化發生率 (unit=1/(&mu;g/m<sup>3</sup>))</b>|

#### 圖5 南部地區各鄉鎮區COPD發生率與PM<sub>2.5</sub>回歸分析之斜率

就發生率而言，圖5(a)顯示較大值均發生在山地，由北到南自高雄市的桃源區沿著山脈延伸至屏東縣春日鄉、牡丹鄉與恆春鎮，最大斜率發生在屏東縣牡丹鄉達17.6 %/yr/(10 μg/m<sup>3</sup>)。南部地區全體的平均值也有0.61 %/yr/(10 μg/m<sup>3</sup>)。

就常態化後之發生率而言，圖5(b)中斜率大多在±5%/(10
μg/m<sup>3</sup>)之間，最大值389%/(10
μg/m<sup>3</sup>)發生在高雄市桃源區，可能係背景PM<sub>2.5</sub>濃度差異不大導致較為敏感。其他地區斜率並不高，因而區域平均值約在0.03
(1/μg/m<sup>3</sup>)左右。正值較大地區以內陸、偏鄉居多，屏東縣有較多行政區是正值。

圖中也顯示負值較大之行政區周邊似搭配有正值較大之行政區，如屏東縣南端的滿州鄉負值大，然周邊的牡丹與車城鄉則顯示較大的正值，臺南市東南邊界的南化區有較大的負值，而周邊的左鎮區及龍崎區則有較大的正值，似與偏鄉醫療資源不足與跨區就醫情形有關。即使取鄰近行政區的平均，這2區似仍能維持正值。

### (三)疾病發生與O<sub>3</sub>的相關性

南部鄉鎮區疾病發生率與對應年度O<sub>3</sub>年均值之相關性，分析結果如表3所示。

表3 南部鄉鎮區之疾病發生率與O<sub>3</sub>年均值之相關性分析

|疾病名稱|南部地區平均斜率||相關係數(r<sup>2</sup>)|正相關鄉鎮區數占全部108之比例(%)|
|:-:|:-:|:-:|:-:|:-:|
||<p>絕對發生率</p>%/yr/ppb|<p>常態化發生率</p>%/ppb|||
|慢性阻塞性肺疾病(COPD)|-8.581|-7.010|0.11|34.26%|
|下呼吸道感染(LRTI)|-80.73|-0.871|0.09|58.33%|
|缺血性心臟病(IHD)|-8.904E-02|-2.556|0.11|50.93%|
|中風(Stroke)|-1.176|-7.001|0.09|43.52%|
|糖尿病(Diabetes)|0.193|2.885|0.13|77.78%|

由表中可以發現，1\~4項疾病發生率與O<sub>3</sub>年均值大略呈現出負相關，而呈現正相關的行政區數，占3縣市108個鄉鎮區的34%\~58%，表示應有部分地區疾病發生率與O<sub>3</sub>年均值的趨勢強烈相反，這些負相關的現象實不宜以空氣品質趨勢來解釋。

5項疾病中以T2DM的正相關最為顯著，斜率及相關係數皆很可觀，後續將據以進一步探討電廠的可能影響。

將各行政區的疾病發生率以11年平均值予以常態化，探討各年度的變動與O<sub>3</sub>年均值的關係，其斜率正負分布情形與前述發生率之斜率差異不大，地區平均值亦僅有T2DM維持正值，其餘疾病則皆為負值。

### (四)第2型糖尿病對O<sub>3</sub>罹病斜率之分布

依據國家公共衛生數據([潘與傅，2019][119])，臺灣地區T2DM發生率正快速增加之中，且多數患者(3\~4成)並沒有病識感。T2DM發病機制中空氣污染物的參與過程，目前還處於假說階段。大致上當吸入氧化性的空氣污染物時，身體會產生一連串發炎反應，生成活性氧化物(reactive oxygen species, ROS)，導致肝臟糖質新生(gluconeogenesis)增加升高血糖、白色脂肪組織(white adipose tissue)發炎、棕色脂肪組織(brown adipose
tissue)的粒線體失能、肌肉利用糖分的效率下降、而造成胰臟過度勞累之典型T2DM。([Rajagopalan, S. and Brook, R.D., 2012][120])。

以下就圖6 T2DM發生率對O<sub>3</sub>斜率之分析結果空間分布進一步討論。

| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/diabetesOzn.csv.png)| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/diabetesOznN.csv.png)|
|:-:|:-:|
| <b>(a) 發生率絕對值斜率(unit=1/yr/ppb)</b>| <b>(b)常態化發生率斜率(unit=1/ppb)</b>|

#### 圖6 南部地區各鄉鎮區T2DM發生率與O<sub>3</sub>回歸分析之斜率

就發生率的絕對值而言，圖6(a)顯示南部地區普遍都有正值，最大值則發生在山地屏東縣之霧臺鄉，其值達3%/yr/ppb。其次為高雄市燕巢區其值約2.5%/yr/ppb。最普遍情況落在0.07
\~ 0.5%/yr/ppb之間，以致平均為0.193%/yr/ppb。

就常態化後之發生率而言，圖6(b)中斜率大多在±5%/ppb之間，最大值24.7%/ppb也是發生在屏東縣之霧臺鄉。然其他高值與前述絕對值有較大的差異，次高與第三高分別為臺南市龍崎區與屏東縣新埤鄉，這是因為考慮偏鄉罹病後有可能到都會區就診，經該鄉鎮區本身所有年度平均值常態化後，年度間相對變動的比例隨之放大。

[黎友苓，2021][130]追蹤台北市居民世代與環保署監測值的關係，結果顯示O<sub>3</sub>每增加一個IQR (3.028 ppb)其T2DM前期的罹病勝算比為1.270 (95%CI 1.080, 1.494，p=0.004)。換算每ppb將增加罹病9%/ppb，比此處南高屏地區之常態化發生率之斜率平均值2.9%/ppb還高，然尚屬同一數量級。

## 四、開發計畫空品與疾病負荷增量

### (一)開發計畫PM<sub>2.5</sub>及O<sub>3</sub>年平均增量

興達電廠新增3部燃氣機組PM<sub>2.5</sub>及O<sub>3</sub>增量年均值如圖7所示。增量計算方式為開發計畫與背景排放量一起輸入CMAQ模式模擬，減去背景排放量之模擬結果。結果顯示增量濃度不高，約僅背景濃度1%以下。PM<sub>2.5</sub>分布以西南沿海為中心，O<sub>3</sub>則以高雄、台南山區為較高濃度範圍。

| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TOT_G-X.ncDT.csv.png){:width="360px"}| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/O3_G-X.ncT.csv.png){:width="360px"}|
|:-:|:-:|
| <b>(a)PM<sub>2.5</sub>(&mu;g/m<sup>3</sup>)</b>| <b>(b)O<sub>3</sub>(ppb)</b>|

#### 圖7 興達電廠新3氣機組PM<sub>2.5</sub>及O<sub>3</sub>增量

### (二)燃氣電廠之COPD疾病風險

興達電廠新增3部燃氣機組PM<sub>2.5</sub>增量年均值，乘上前述COPD發生率回歸斜率，可以得到因更新改建計畫造成南部地區各鄉鎮區發生COPD的風險，結果如圖8所示。

| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TOT_G-X.ncDT_LungDiseasePar2.csv.png){:width="360px"}| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TOT_G-X.ncDT_LungDiseaseParN2.csv.png){:width="360px"}|
|:-:|:-:|
| <b>(a)COPD發生率之增量(1/yr)</b>| <b>(b)COPD發生率之相對變動(無單位)</b>|

#### 圖 8 興達電廠新增燃氣機組造成南部地區各鄉鎮區COPD之發生風險(單位=1/yr)

圖8(a)顯示更新改建計畫造成之PM<sub>2.5</sub>增量以沿海地區為主，阿蓮區因位置靠近廠區，PM<sub>2.5</sub>增量濃度較大，乘上發生率斜率後即形成相對敏感之熱區，COPD發生風險值達2.7×10<sup>-4</sup>/yr，略大於一般可接受風險等級10<sup>-4</sup>水準。

然此值並非所有鄉鎮區中最大值，表4列出COPD發生風險之前5大鄉鎮區，最大值為苓雅區，因該區有較高發生率回歸斜率所致，約最高值4.18×10<sup>-4</sup>/yr，然此值為該區現況之0.79%。

#### 表4 興達電廠新增燃氣機組造成COPD之發生風險前5大南部鄉鎮區

|序號|鄉鎮區|PM<sub>2.5</sub>增量年均值(&mu;g/m<sup>3</sup>)|COPD發生機率(1/yr)|COPD發生機率相對變動(無單位)|當地人口數(人)|
|:-:|:-:|:-:|:-:|:-:|:-:|
|1|高雄市苓雅區|0.1456|4.179E-04|7.942E-03|171,398|
|2|屏東縣三地門鄉|0.0472|3.829E-04|8.474E-03|7,638|
|3|屏東縣春日鄉|0.0230|3.641E-04|2.398E-03|4,863|
|4|高雄市阿蓮區|0.2013|2.735E-04|1.748E-02|28,934|
|5|臺南市中西區|0.0862|2.460E-04|1.028E-02|77,840|

此外在高雄市與屏東縣山區PM<sub>2.5</sub>增量略為0.02 μg/m<sup>3</sup>，而前述在高雄市與屏東縣山區有較高的COPD發生率回歸斜率，因此相乘結果，得出該區有較高的疾病發生機率。COPD發生機率最高值出現在三地門鄉及春日鄉等，約為3.6 \~ 3.8×10<sup>-4</sup>/yr。經檢討所有鄉鎮區第17名以後其餘地區，發生機率都在負值或1×10<sup>-6</sup>\~9×10<sup>-5</sup>/yr之間，符合一般可接受風險等級 10<sup>-4</sup>水準。

### (三)燃氣電廠COPD發生率相對變動

將前述常態化疾病發生斜率，乘上新3氣機組造成的PM<sub>2.5</sub>年均值增量，可以得到鄉鎮區COPD發生率相對變動量(無單位)，代表了疾病發生率相對於平均狀態的變動情形，類似相對風險之概念，如圖8(b)及表5所示。大體上地區疾病發生率的變動都在2.7%以下，略高於空氣品質增量的變動比例。

就空間上，因在臺南市東南端之龍崎區、及屏東縣枋山鄉、南州鄉等因有較大的正值斜率，即使PM<sub>2.5</sub>增量濃度不高，但相乘之後，也會造成該2區COPD發生率有較大的變動。臺南市除龍崎外，附近的關廟及左鎮區亦在熱區範圍內。

而前述高雄市桃源區、屏東縣牡丹鄉與車城鄉等處雖有較高罹病斜率，惟因位處偏遠增量影響有限，因此疾病發生率的變動幅度，也不若距離較近的前述3個熱區。

#### 表5 興達電廠新增燃氣機組造成COPD發生率相對變動前5大南部鄉鎮區

|序號|鄉鎮區|PM<sub>2.5</sub>增量年均值(&mu;g/m<sup>3</p>)|COPD發生機率相對變動(無單位)|當地人口數(人)|
|:-:|:-:|:-:|:-:|:-:|
|1|臺南市龍崎區|0.101|2.777E-02|4,048|
|2|屏東縣枋山鄉|0.0297|2.627E-02|5,456|
|3|屏東縣南州鄉|0.0752|2.113E-02|10,660|
|4|臺南市關廟區|0.1049|2.105E-02|34,370|
|5|臺南市左鎮區|0.0741|1.935E-02|4,894|

### (三)燃氣電廠之T2DM疾病風險

開發計畫O<sub>3</sub>增量年均值，乘上前述T2DM發生率回歸斜率，可以得到南部地區各鄉鎮區發生T2DM的風險，結果如圖9所示。

前述圖7(b) O<sub>3</sub>增量以高雄臺南山區為主，在濱海地區增量則為負值([NO Titration Effect][131])。由於該區恰好出現T2DM發生率負值的斜率，因此相乘之後則形成不合理的正值(空氣品質改善反而造成疾病增加)，此處不予討論。

山區相對敏感之熱區T2DM發生風險值達8.09×10<sup>-4</sup>/yr(屏東縣霧臺鄉，見表6)，大於一般可接受風險等級10<sup>-4</sup>水準。此外在高雄市範圍內的茂林、旗山區，因有較高的O<sub>3</sub>增量，因此相乘後有較高的罹病風險(4.7 \~ 5.3×10<sup>-4</sup>/yr)，其餘在平地、沿海地區等88個鄉鎮區，發生機率都在負值或1×10<sup>-6</sup>
\~ 7×10<sup>-5</sup>/yr之間，符合一般可接受風險等級10<sup>-4</sup>水準。

| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/O3_G-X.ncT_diabetesOzn0.csv.png){:width="360px"}| ![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/O3_G-X.ncT_diabetesOznN0.csv.png){:width="360px"}|
|:-:|:-:|
| <b>(a)糖尿病發生率之增量(1/yr)</b>| <b>(b)糖尿病發生率之相對變動(無單位)</b>|

圖9 興達電廠新增燃氣機組造成南部地區各鄉鎮區T2DM之發生風險

表6 興達電廠新增燃氣機組造成T2DM之發生風險前5大鄉鎮區

|序號|縣市|鄉鎮區|O<sub>3</sub>增量年均值(ppb)|<p>糖尿病發生機率</p>(10<sup>-4</sup>/yr)|當地人口數(人)|
|:-:|:-:|:-:|:-:|:-:|:-:|
|1|屏東縣|霧臺鄉|0.026|8.09|3,383|
|2|高雄市|茂林區|0.053|5.58|1,870|
|3|高雄市|旗山區|0.048|5.44|37,750|
|4|屏東縣|三地門鄉|0.064|2.89|7,638|
|5|屏東縣|泰武鄉|0.030|2.62|5,405|

### (四)燃氣電廠之T2DM發生率相對變動

將前述常化疾病發生斜率，乘上新3氣機組造成的O<sub>3</sub>年均值增量，可以得到鄉鎮區T2DM發生率相對變動量(無單位)，如圖9(b)及表7所示。

#### 表7 興達電廠新增燃氣機組造成T2DM發生率相對變動前5大南部鄉鎮區

|序號|縣市|鄉鎮區|O<sub>3</sub>增量年均值(ppb)|糖尿病發生機率相對變動(10<sup>-3</sup>)|當地人口數(人)|
|:-:|:-:|:-:|:-:|:-:|:-:|
|1|高雄市|杉林區|0.0783|6.52|12,380|
|2|屏東縣|霧臺鄉|0.0261|6.44|3,383|
|3|高雄市|茂林區|0.0525|5.65|1,870|
|4|高雄市|美濃區|0.0705|4.55|40,780|
|5|高雄市|旗山區|0.0475|3.98|37,750|

如不討論前述濱海地區負值增量與負值斜率造成的不合理現象，大體上新增3部燃氣機組造成地區疾病發生率的變動都在0.65%以下。就空間上而言，如前所述在高雄市東區山地如高雄市杉林、茂林、美濃、旗山等區，因有較大的O<sub>3</sub>增量，故而造成該區T2DM發生率有較大的變動。

屏東縣霧臺鄉因有較高相對發生回歸斜率，雖然O<sub>3</sub>增量不是最高，也有較高的變動。

## 五、結　論

本文仿照現有HRA規範之階段流程，展開大範圍衍生性空氣品質項目之健康風險分析程序。在階段(1)網格模式模擬2019年CMAQ背景濃度，除了以空品測站數值進行性能評估，達到8成以上測站的符合率，也與該署2022年2月公開的模擬結果進行比較，在空間分布上達成合理之相似度。增量模擬顯示興達電廠新增3部燃氣機組的PM<sub>2.5</sub>與O<sub>3</sub>增量均在背景值的1%以下。前者影響以西南沿海電廠為中心範圍、後者則分布高雄台南東方山區。

階段(2)建立了南部地區各鄉鎮區5項疾病的罹病斜率及其變動率，並非所有疾病與長期空氣品質都具有全面的正相關性，經檢討後以COPD發生率之PM<sub>2.5</sub>斜率以及T2DM發生率之O<sub>3</sub>斜率具有討論之意義。

階段(3)將2者相乘後發現開發計畫增量對地區COPD受PM<sub>2.5</sub>增量影響最高4.18×10<sup>-4</sup>/yr、變動幅度最高2.7%；T2DM受O<sub>3</sub>增量影響風險最高8.09×10<sup>-4</sup>/yr、變動0.65%以下，應屬有限。

## 致謝

本文承蒙臺灣電力公司提供研究經費、環保署提供全國排放及空氣品質數據、衛福部提供全民健康保險研究資料庫，特致謝忱。

## 參考文獻

Murray, C.J.L., et. al(total 940 authors). (2020). Global burden of 87
risk factors in 204 countries and territories, 1990--2019: a systematic
analysis for the Global Burden of Disease Study 2019. The Lancet 396
(10258):1223--1249. doi:10.1016/S0140-6736(20)30752-2.

行政院環境保護署(2011)
健康風險評估技術規範https://oaout.epa.gov.tw/law/LawContent.aspx?id=GL004851
l

行政院環境保護署(2021a)
空氣品質模式模擬規範<https://oaout.epa.gov.tw/law/LawContent.aspx?id=GL005316>

USEPA(2022), CMAQ: The Community Multiscale Air Quality Modeling System,
<https://www.epa.gov/cmaq>, LAST UPDATED ON MARCH 7, 2022.

UCAR(2022a), Community Atmosphere Model with Chemistry,
<https://wiki.ucar.edu/display/camchem/Home>, LAST UPDATED ON MAY 31,
2022.

UCAR(2022b), WEATHER RESEARCH AND FORE-CASTING MODEL,
https://www.mmm.ucar.edu/weather-research-and-forecasting-model, LAST
UPDATED 2022.

行政院環境保護署(2021b)
案例月及案例季及模擬期程https://aqmc.epa.gov.tw/regulations_2.php#regulations_2\_1

UCAR(2022c), WACCM, <https://www2.acom.ucar.edu/gcm/> waccm, LAST
UPDATED 2022.

ECWMF(2022), CAMS global reanalysis (EAC4),
<https://ads.atmosphere.copernicus.eu/>, 2022.

行政院環境保護署(2022a) 空氣污染排放清冊(Taiwan Emission Data System)
[https://air.epa.gov.tw/EnvTopics/
AirQuality_6.aspx](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx),
LAST UPDATED ON JUNE 15, 2022.

Kurokawa, J. and Ohara, T.(2020) Long-term historical trends in air
pollutant emissions in Asia: Regional Emission inventory in ASia (REAS)
version 3, Atmos. Chem. Phys., 20, 12761-12793,
https://doi.org/10.5194/acp-20-12761-2020, 2020.

Grigoriadis, A., Mamarikas, S., Ioannidis, I., Majamäki, E., Jalkanen, J.-P., and Ntziachristos, L. (2021). Development of exhaust emission factors for vessels: A review and meta-analysis of available data. Atmospheric Environment: X 12:100142. doi:10.1016/j.aeaoa.2021.100142.

行政院環境保護署(2022b) 公告網格模式模擬系統概述、第二次教育訓練，2022/2/17

衛生福利部統計處(2014) 全民健保處方及治療明細檔_門急診─西醫、中醫及牙醫資料庫使用手冊，https://www.mohw.gov.tw/dl-16113-d7805f26-95c9-4d94-accb-166abb859404.html。

[潘文涵、傅茂祖 (2019)][119].
糖尿病之流行病學及病因、診斷、分類糖尿病防治手冊（糖尿病預防、診斷與控制流程指引）-醫事人員參考。

[Rajagopalan, S. and Brook, R.D. (2012)][120]. Air pollution and type 2
diabetes: mechanistic insights. Diabetes 61 (12):3037--3045.
doi:10.2337/db12-0190.

[黎友苓(2021)][130]. 空氣污染物對早發型糖尿病及糖尿病前期之相關性研究
公共衛生學系博士班. 臺北醫學大學, 台北市.

[A1]: <> "環興科技股份有限公司總工程師"
[A2]: <> "環興科技股份有限公司環境一部主任"
[A3]: <https://ieohs.ym.edu.tw/files/11-1237-74.php> "陽明交大環境與職業衛生研究所副教授"
[A4]: <> "台電環境保護處副處長"
[119]: <https://www.hpa.gov.tw/Pages/ashx/File.ashx?FilePath=~/File/Attach/1235/File_6877.pdf> " 潘文涵 and 傅茂祖 (2019). 糖尿病之流行病學及病因、診斷、分類糖尿病防治手冊（糖尿病預防、診斷與控制流程指引）-醫事人員參考. Available at https://www.hpa.gov.tw/Pages/ashx/File.ashx?FilePath=~/File/Attach/1235/File_6877.pdf."
[120]: <https://diabetes.diabetesjournals.org/content/diabetes/61/12/3037.full.pdf> " Rajagopalan, S. and Brook, R.D. (2012). Air pollution and type 2 diabetes: mechanistic insights. Diabetes 61 (12):3037–3045. doi:10.2337/db12-0190.[pdf]"
[130]: <https://hdl.handle.net/11296/eum3xj> "黎友苓 (2021). 空氣污染物對早發型糖尿病及糖尿病前期之相關性研究 公共衛生學系博士班. 臺北醫學大學, 台北市."
[131]: <http://www-personal.umich.edu/~sillman/ozone.htm> "NOx 滴定：即臭氧與猗氧化氮的大氣化學反應，會使臭氧濃度消失轉化成二氧化氮。在夜間或 NOx 排放量非常大的附近（例如發電廠），通過 NOx 滴定過程會降低臭氧濃度。"