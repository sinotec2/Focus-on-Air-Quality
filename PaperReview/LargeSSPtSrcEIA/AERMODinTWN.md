---
layout: default
title: AERMOD在臺灣應用之實務探討
parent: Large Seaside PtSrc EIA
grand_parent: Paper Reviews
nav_order: 6
last_modified_date: 2022-05-18 15:20:06
tags: review plume_model AERMAP
---

# AERMOD在臺灣應用之實務探討
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

## 一、前言

美國環保與氣象界發展AERMOD模式用以替代ISC3模式，至少已經有20年的歷史，不論在垂直擴散的處理、地形效應的考量、沉降、以及建築物效應方面，都納入了當代重要的科學進展。美國方面模式比較研究顯示，平坦地形條件下，AERMOD模擬結果較ISC3略高一些，ISC3短期結果略高，複雜地形條件下二者差異較大，AERMOD與觀測值較為接近，ISC3模式顯然高出觀測值很多。

國內自2007年以來也至少有60篇以上的學位論文研究(詳見附表及網站資訊)，其實學術界對模式的特性與應用並不陌生。技術顧問機構也不乏應用的案例（如曠與許 2005）。然而不論在法規面、或實際環境影響評估(下略以EIA)、健康風險評估(下略以HRA)、污染源設置許可、等審查過程(下略以「審查」)，環保署目前都還沒有跟進的作為，在該署空氣品質評估技術規範，或者是空氣品質模式規範(下簡稱「規範」)與環保署模式支援中心網站(下簡稱「模式中心」)，都還是維持在ISC3版本，主要的理由在於ISC3在複雜地形個案的應用中，有其保守的特性，而臺灣地區山地佔60%以上，該署認定此舉有利環境保護之公益。

隨著國內環保意識的普及，環保法規的完備，「審查」時因模式模擬結果不通過的情形越來越少，太過保守反而不符合實際。因此環保署歷年來也持續發包委託計畫(環保署2010～2019)，思考本土化與取代ISC3的可能性。

本文除回顧AERMOD在臺灣應用遭遇之困難、未來在「審查」時可能之爭議、並以自建之教學系統(http://http://sinotec24.com/aermods.html，下簡稱「系統」)，提供廣泛之模擬經驗，以供業界參考，甚或自行測試以快速累積模式經驗。該「系統」程式自2018年陸續建立，並自2020開始服務中原大學環工所、臺大環工所、陽明大學環衛所研究生教學，迄今持續運轉。

以下就模擬範圍、接受點密度、氣象檔案之前處理、地形檔案之前處理、沉降議題、建築物議題等依序討論。

## 二、模擬範圍與接受點密度
由於AERMOD基本上仍然為一高斯模式，因此其應用範圍在空間上是否能夠保持「均質」(homogeneous)、在時間上是否能被認定為「假穩定」(pseudo steady state)，符合這2項條件方能算是有效的應用，然個案之煙囪排放條件、位置之地形與氣象條件都有差異，為具體討論此2條件之符合與否，本文將TEDS10中點源數據陳列於umap動態地形圖之上，便於查詢如圖1所示。

#### 圖1　臺灣地區點源之分布與其煙道條件
- 內容下載自環保署TEDS10.0資料庫，然部分煙道條件不合理處，如座標、高度、溫度、內徑等都經品質管制修正。
- 點源參數中之座標系統採TWD97，以維持直角座標系統。 
- umap：[teds10-point-data-pm25](http://umap.openstreetmap.fr/zh/map/teds10-point-data-pm25_594438#9/23.3789/121.0219)

| ![TWN1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN1.png)|
|:--:|
| <b>(1)臺灣本島範圍之點源家數</b>|
| ![TWN2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN2.png)|
| <b>（2）個別工廠點源排放條件(ISC3/AERMOD 排放格式)|

### (一)空間範圍

依據圖1臺灣地區目前的工廠大多座落在平地範圍，山地雖然也有被列管的飯店民宿，但畢竟屬於小污染源，重大污染源因有溫排水、物資運輸需求，大多在濱海地區、港區。
  
按照過去ISC3的模式限制，要求空間範圍以不超過50Km為範圍。在臺灣地區除了濱海地區可以超過20Km範圍以外，其餘地區很難在20Km內仍然可以保持風場、溫度場乃至於大氣擴散的各項特性「均質」之狀態。複雜地形條件下超過3～5Km之模擬範圍應該都難以維持其「均質」的特性，此點會在氣象前處理的解析度問題內進一步探討。

由於「均質」大氣在水平方向沒有速度的梯度，按照連續方程式此時將不會有垂直速度的梯度，因地面垂直速度為0，因此亦即不會有垂直速度。

圖2將2020年中央氣象局(CWB)模擬全臺近地層垂直速度結果，進行均方根計算(以cm/s表示)如圖2所示，相對而言，彰化以南的西部縣市，垂直速度年均方根值約在1cm/s以下，是最能符合「均質」條件地區，臺中與桃竹苗地區垂直速度1～2cm/s，略能符合「均質」條件，相對山區海拔越高、坡度越陡峭，越不符合「均質」條件，應避免使用AERMOD，幸而對照圖1這些地區，目前並沒有污染源設置。各縣市範圍內「均質」程度亦有差異，建議後續還需按縣市垂直速度分布、地形、污染源座落情況詳細界定，避免模式的誤用。
 
#### 圖2 2020 CWB WRF 近地層垂直速度均方根值之分布
- 資料來源：中央氣象局/opendata/  https://opendata.cwb.gov.tw/fileapi/opendata/MIC/M-A0064-0$i.grb2
- $i=00~84

| ![TWN3.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN3.png)|
|:--:|
| <b>圖2 2020 CWB WRF 近地層垂直速度均方根值之分布</b>| 

除了模式本身的「均質」條件限制之外，「規範」也要求模擬範圍要能夠正常顯示污染源所造成最大濃度，模擬範圍會等於污染源到最大落地濃度距離的4倍，就此一實務要求而言，濱海地區風速強勁，搭配較高的煙囪高度，經常使最大濃度發生在污染源下游數Km之外。相對而言，內地、臺北、臺中等盆地地形範圍內、或較低的煙囪，風速就會較低，太大的範圍就顯得不實際，模式使用者經常必須嘗試錯誤，以求得最合適的模擬範圍。如圖3「系統」自動設定模擬範圍與其年均值結果範例。

#### 圖3 濱海及盆地內污染源之模擬範圍與年均值結果
- 三角形為污染源位置。白色框為合理的模擬範圍。
- AERMOD 遠端計算服務，作業網址http://sinotec24.com/AERMOD.html

| ![TWN3f.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN3f.png)|
|:--:|
| <b>(a)濱海地區污染源案例　　　　　　(b)盆地地形污染源案例</b>| 
					
圖3「系統」模擬濱海及盆地內污染源之模擬範圍與年均值結果(示意圖)

圖中濱海案例較為單純，污染源及最大濃度之間的距離約3.8Km取4Km，其他並沒有其他的落地煙流，模擬範圍取16Km應屬合理。

臺北盆地個案除了污染源附近的最大濃度煙流之外，距離污染源僅0.7Km，在周邊山地也造成次高濃度，如果只限制在4倍距離約3Km雖確實可以呈現最大濃度，但建議可以取大一些，以顯示完整煙流形狀為宜。

就此空間範圍此一項目而言，AERMOD與ISC3並沒有太大的差異。但AERMOD可以順利接受氣象模式的成果，任何地方均能有代表性的氣象數據(詳後述)，過去執行ISC3時，受到臺灣地區氣象站空間分布的限制，模擬範圍勉強納入測站而做不必要的擴張，這種不符合邏輯的設定將不會(必)再有了。

#### 圖4 濱海污染源及角落2020年CWB WRF地面風花圖
圖4模擬濃度乃採圖3(a)污染源所在地(範圍中心點)之WRF模式做為代表性氣象值，另在範圍陸方3個角落，也同時顯示WRF之地面風全年風花圖進行比較。


| ![TWN4a.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN4a.png)| ![TWN4b.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN4b.png)|
|:--:|:--:|
|<b>(a)污染源所在地</b>|<b>(b) 圖3(a)東北角</b>| 
| ![TWN4c.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN4c.png)| ![TWN4d.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN4d.png)|
|<b>(c)圖3(a)西南角</b>|<b>(d)圖3(a)東南角</b>| 

由圖可以發現，濱海地區地勢平坦、地表粗略度大略相同，中心點與西南之風花圖彼此較為類似，然其東方內陸情況還是差異很大。

#### 圖5 盆地污染源及角落2020年CWB WRF風花圖
盆地個案角落之風花圖如圖5所示，如以外圍較大模擬範圍，四圍風花圖與中心點有較大的差異，具有東西方向明顯的梯度，「均質」之假設條件不復存在，必須縮小模擬範圍至圖3白色框為宜。

| ![TWN5a.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN5a.png)| ![TWN5b.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN5b.png)|
|:--:|:--:|
|<b>(a)圖3(b)西北角</b>|<b>(b) 圖3(a)東北角</b>| 
| ![TWN5c.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN5c.png)| ![TWN5d.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN5d.png)|
|<b>(c)圖3(a)西南角</b>|<b>(d)圖3(a)污染源所在地</b>| 

### (二)時間範圍

目前「模式中心」提供氣象檔案的時間範圍為一年一個檔案、每檔案都是逐時，這是可以符合「假穩定」條件的。回顧過去的AERMOD研究報告之應用，還沒有發現時間間距是低於小時的。

使用者如果要進行長時間的健康風險評估，可以進行跨年的模擬再予以平均。AERMOD可以在一次的作業內就完成這項工作，這點讓使用者十分方便。

在CALM HOURS的處理上，AERMOD與ISC3有相同的邏輯，這點也不必特別擔心，只要確認選擇法規選項即可。
### (三)接受點密度
接受點密度除了影響模式計算時間之外，也與等值圖圖面的解析度有關，「規範」要求以5倍於排放源高度設定，最大不得大於500m，這些規定是上限值。由於計算機的進步，解析度高於「規範」要求並非難事。

在地形檔案中是有水平解析度的下限值的，一般公開之數值地形資料解析度約20～40m，因為低於此範圍內沒有數據，只是內插，並沒有提供額外訊息，因此高於此解析度也是沒有必要的。

過去至少有7篇學生論文將AERMOD應用在都會區線源的模擬，遇到了模式解析度設定問題，雖然這不是許可審查所關心的，但是環評也可能會遇到此一情況。新版AERMOD是有納入CALINE模組(非法規使用)，有能力應用在線源的模擬，但在接受點的設計上，太密集的間距會遭遇到建築物、道路等都市地上物的干擾，該視為複雜地形處理之，還是平坦地形忽略之?如果是網格化的接受點，建議還是規避比較好，或者更換其他可以模擬街谷效應的模式，而不必使用AERMOD。

## 三、氣象檔案之前處理
目前ISC3所需之氣象檔案已在「模式中心」網站提供，並持續新增最近年代之資料。該中心提供檔案以氣象局測站為主，雖有空間含括範圍不足、致使應用上難以符合模式「均質」基本假設之困境，但長久以來也實際擔負模式標準化的責任。
### (一)WRF+MMIF方案
AERMOD的氣象檔案內容項目比ISC3多，無法再像過去單以氣象局之觀測數據即可計算，一般可以經由現地高低塔長期觀測數據利用AERMET程式進行轉換，或可由大氣動力模式如MM5或WRF模擬結果經MMIF讀取。臺灣地區除了少數台電電廠有短期的高低塔觀測，其他污染源大多只有簡易的氣象數據，並不足夠。

所幸目前包括學術單位與技術顧問機構已有不少WRF之執行經驗，政府opendata資料亦每日提供中央氣象局WRF模式3 Km解析度之模擬結果，可以使用MMIF程式進行轉檔。
### (二)使用WRF+MMIF之好處包括：
- WRF部分
  -	WRF模擬結果可由官方提供，具有一定程度之品質，
  -	模擬範圍涵蓋整個臺灣地區與外島，解析度達3Km，在一般AERMOD模擬範圍內可以有許多選項，WRF結果足以進行敏感性分析。
  -	opendata網站不足之時間亦可向氣象局價購，不必擔心數據不足困難。
  -	地面參數如土地使用、粗糙度、反照率、蒸散比等，可以與氣象局WRF之設定取得一致，有助於模式標準化。
  -	WRF模擬準確度有一定水準
- MMIF 部分  
  -	MMIF程式由美國環保署提供並持續維護，可以確保正確轉檔，
  -	MMIF輸出文字檔可以進行品質確認
  -	MMIF除了輸出AERMOD所需之地面與高空，也輸出AERMET模擬所需檔案，使用者可以自行補充執行AERMET程式

「系統」目前已經完成2016～2020年點源所在位置的WRF轉檔，其結果檔案之連結位置亦陳列於umap網站上可供使用者點選下載，如圖6所示。

#### 圖6 點源所在網格MMIF轉檔結果

| ![TWN6a.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN6a.png)|
|:--:|
| <b>(a)網格位置</b>|
| ![TWN6b.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN6b.png)|
| <b>(b)結果檔案連結|
							
mmif 遠端執行系統，作業網址http://sinotec24.com/mmif.html
地圖查詢http://umap.openstreetmap.fr/zh/map/3km_590688#8/23.712/122.009
 
圖6中可見即使是平地範圍，也並布滿計算網格，這是因為河川地、水體、農地、鹽田等，目前並無工廠開發，未來也不太可能開發。

倘若新污染源所在地不屬於既有已轉檔網格，「系統」亦提供遠端計算服務，只需提供含有污染源經緯度之KML檔案，或直接提供mmif.inp控制檔，「系統」會執行2020年氣象局WRF輸出檔之轉檔計算。
### (三)WRF+MMIF轉檔的正確性檢討
最主要影響煙流模擬結果的氣象要素是風速、風向。圖7為2020年CWB WRF模擬地面風速風向與環保署測站之比較，比較之統計指標參考「規範」指定氣象模式之性能評估項目。採用環保署測站是因為CWB並不會使用該等測站數據進行同化分析納入WRF中，具有獨立性。

由圖中可以顯示，各月份大都能達成性能評估符合度在60%以上之「規範」要求，12月份風速的總體誤差(OB)，WRF預報仍有高估的趨勢，該月份其他項目平均尚能超過60%的符合度。
#### 圖7 CWB WRF模擬測站風速風向之性能評估符合度

| ![TWN7.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN7.png)|
|:--:|
| <b>圖7 CWB WRF模擬測站風速風向之性能評估符合度</b>|

## 四、地形檔案之前處理
按照「規範」的定義，當煙流高度低於周圍地形高度，則必須啟動複雜地形機制，照此規定，臺灣地區大多數點源都位於複雜地形之中。然而過去「模式中心」對ISC3並沒有提出標準化檔案或作法，主要因為個案的煙囪、煙流高度不一、解析度不同、模擬範圍也有異，實務上無法標準化。

複雜地形條件下AERMOD所需要的「山丘高」(Hill Height污染源附近代表性高地之高度)可以使用其地形前處理程式AERMAP，相較氣象部分已經有許多相關研究與作業化系統，地形受到到關切並不多，該程式可以說是整體系統中最為複雜的部分。

早期因國內數位地形資料尚未開放、即使已有前處理程式，仍因轉檔不易，大多採取自行撰寫程式取代AERMAP（如曠與許2005、環保署2009、林2010），曠與許2005 過去提出ISC3及AERMOD在全臺各地之計算結果比較，確能證實ISC3在複雜地形條件下較AERMOD高估。林2010以台中電廠周邊測站測值證實AERMOD的濃度分布較ISCST3更符合觀測。

近年來因為國內外數值地形資料漸漸開放、工作站上也公開許多轉檔程式（gdal_translate），AERMAP的技術瓶頸已不復存在。有關AERMAP的運作過程可以參考崑山科技大學蔡德明教授提供之網頁說明。蔡教授建議一次轉換臺灣全島數值地形數據(Digital Terrain Model DTM)，再視AERMOD需要範圍進行計算，經比較測試，這個策略並沒有較快，因為一般AERMOD模擬範圍有限，臺灣大多地區又是山地，因此計算上不如每次下載以污染源為中心之少量、足夠DTM數據(儲存於「系統」備用)、按照實際需要進行轉換，再進行AERMAP計算，會比較有效率。

#### 圖8 既有點源之AERMAP執行結果

| ![TWN8.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN8.png)|
|:--:|
| <b>圖8 既有點源所在網格之AERMAP執行結果(umap與連結範例)</b>|

淺藍色框線為AERMAP/AERMOD接受點網格範圍，深藍色標記為點源位置(1Km解析度)儲存網址：http://umap.openstreetmap.fr/zh/map/twn1x1-aermap-results_593832#8/23.685/121.278

圖8為「系統」計算現有點源位置(1Km解析度)為中心，周圍複雜地形檔案之計算結果，同樣以連結方式陳列於umap網站。選擇以1Km為解析度，而不是每一家工廠都計算一遍，主要是因為大多個案模擬範圍都會大於1Km，對於污染源是否位於範圍中心尚能允許部分誤差，倘若真的誤差太大，使用者也可以應用「系統」AERMAP功能自行調整範圍與解析度，引用已經下載之DTM數據，重新進行計算。

AERMAP計算結果中的REC檔案，內容即為模擬範圍之地形高及「山丘高」，以內含文件(include file)之形式，用以進行複雜地形之設定。除此之外，計算結果尚包括表1所示檔案。
#### 表1 AERMAP前處理之成果檔案

|檔案(副檔名)|內容用途|
|-|-|
|tiff檔|下載之DTM數據，可供GIS進一步處理或繪圖。|
|KML檔|進行DTM數據之等值線繪製|
|DEM檔|DEM為美國USGS之常用格式，為AERMAP輸入DTM檔案指定格式之一。|
|aermap.inp|AERMAP主控檔|
|aermap.out|AERMAP螢幕輸出內容|
|re.dat|接受點座標及高程(ISC3格式)|
|TG.TXT|ISC3地形內含文件|
|REC檔|AERMOD地形內含文件|

煙流模式的地形處理，遠端作業網址http://sinotec24.com/terrain.html

## 五、建築物議題
BPIP前處理在ISC3時代就存在了，AERMOD也繼續延用BPIP(PRIME版本)，使用者可以自訂座標系統簡單點出建築物頂點與煙囪位置、輸入高度、高程至控制檔，程式就會計算ISC3或AERMOD所需的建築物參數。
 
過去在「審查」時這一部分因沒有顯示軟體，只看文字檔可以說是完全空白，無從確認。國外有技術機構(AEREarth)提供免費圖形顯示服務，然而是UTM系統且不接受臺灣之51區。

因應此一情況，「系統」提供了遠端計算服務，在該系統數位版點入前述位置與高度產生KML檔案之後，直接進入「系統」進行BPIP-PRIME計算，或自建控制檔交由「系統」計算，也可以由系統解讀控制檔，反寫成KML檔案，以利繪圖顯示。除了建築物之外，「系統」亦會解讀污染源之空間形態，將其寫成KML檔案。貼在OpenTopoMap如圖9所示。

#### 圖9 建築物與污染源空間設定之圖面確認範例

| ![TWN9ab.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN9ab.png)|
|:--:|
| <b>(a)KML圖面確認　　　　　　(b) BPIP輸入檔(範例)</b>|
| ![TWN9c.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/TWN9c.png)|
| <b>(c)體源空間位置檢核之範例</b>|

橙色底為輸入座標所對應之空間位置。藍色汽球為煙囪位置(假想)。底圖為OpenTopoMap
## 六、後處理臭氧限制法(OLM Ozone Limiting Method)議題
2019年9月17日環保署加嚴了NO2的小時濃度標準至0.1ppm，這使得過去以NOx濃度當成NO2的作法顯得太過保守，需考慮實際大氣的轉化能力。簡言之此法乃以最接近測站之O3實際值，做為NO增量轉化成NO2之最大值，加上原來排放中NO2所造成之增量，即為最後增量評估結果。

AERMOD具有內設之OLM模組，按照美國空品模式指引，可以分階使用季均值為代表、或鄰近測站實際小時值檔案輸入模式，模式計算時就考量OLM，不必後處理。「系統」為同時服務ISC3及AERMOD，仍採取後處理作法，執行模式時須指定輸出逐時NOx檔案(OU POSTFILE)以利後處理。

進入「系統」之OLM有2個方式，一者不必指定，AERMOD模擬NOx時「系統」直接進行後處理。一者使用者也可以提供自行模擬之NOx逐時輸出檔案(或壓縮檔)，讓「系統」進行後處理。「系統」會由現行環保署測站中找出最近的3個測站，針對模擬的時間找出對應小時的O3與NO2監測值，處理結果如表2所示。

### 表2 OLM後處理之成果檔案(北高雄案例)

|類別|檔案名稱|檔案內容|
|-|-|-|
|模式逐時輸出檔|NO2HR-MAX.dat|ISC3/AERMOD輸出之逐時NOx值|
|修正後之逐時增量值|NO2HR-MAX_rep.txt|修正後的最大值資訊|
||NO2HR-MAX_nanzi.dat|以楠梓站O3修正|
||NO2HR-MAX_qiaotou.dat| 以橋頭站O3修正|
||NO2HR-MAX_renwu.dat| 以仁武站O3修正|
|測站逐時測值|NO2O3nanzi2018010120181231.csv|2018年楠梓站NO2O3|
||NO2O3qiaotou2018010120181231.csv|2018年橋頭站NO2O3 |
||NO2O3renwu2018010120181231.csv|2018年仁武站NO2O3 |
|逐時測值時序圖|NO2O3@20180101nanzi.png |2018年楠梓站NO2O3|
||NO2O3@20180101qiaotou.png |2018年橋頭站NO2O3|
||NO2O3@20180101renwu.png|2018年仁武站NO2O3 |

煙流模式NOx逐時結果之臭氧限制法後處理，遠端作業網址http://sinotec24.com/OLM.html
## 七、結語：遠端計算之必要性
本文彙整並探討了AERMOD在國內的模擬經驗，以及在模擬範圍、解析度、氣象、地形與建築物等條件方面的議題，以供未來模式標準化相關討論之參考依據。
-	在氣象方面，本文提出以WRF+MMIF流程，應為目前最容易標準化、充分代表性、並與中央氣象局作業完全結合的作法。
-	地形方面，因數值地形數據普及化，作業流程瓶頸已經不復存在，建議還是使用AERMAP，並儘量減少模擬範圍。

雖然這些前置作業具有一定程度的技術性，經由顯示軟體的查核確認，足以掌握其正確性與品質，在「審查」時能以達成最佳的溝通。

隨著模式的升級與複雜化、程式計算的專業化，個人電腦即可執行之ISC3時代已經過去，需要在計算資源、支援專業、標準化檔案儲存空間等，都能大型化、集中化，此處也以運轉中之教學系統經驗，建議主管機關可以思考建置遠端計算系統之必要性，以快速提升評估的準確性、透明度、使AERMOD能正式應用在各項審查程序之中。
## 八、致謝
感謝輔英科大副校長林清和教授提供MMIF與AERMAP意見。感謝中興工程集團提供WRF及地形等背景數據與計算資源。感謝教學過程所有參與學生、研究生之意見。
## 參考文獻
- 行政院環保署(2003) 模式模擬規範附錄一高斯擴散模式使用規範.pdf民國92 年 12 月 25 日(舊版) 
- 曠永銓.許珮蒨(2005) AERMOD 煙流模式在臺灣地區之應用研究 中興工程, Vol 88, pp. 55-62
- 行政院環保署(2009)空氣品質模式技術及對策支援計畫, EPA-98-FA11-03-A229
- VBird (2019) AERMOD - AERMAP 地形與受體 https://linux.vbird.org/enve/aermap-op.php
- 行政院環保署(2019)建置AERMOD本土化模式及空品模式審驗制度專案工作計畫 108A047

## 附表 臺灣地區應用AERMOD之學位論文一覽表
- 搜尋排序互動表格 http://sinotec24.com/AERMOD_review.html
## Source
- 原文發表於[2021環工技師會訊11007pp39-55](http://www.tpeea.org.tw/upload/news/files/7eea35bc4c7a4189b42566fffe2f2fee.pdf)，經部分修正更新。