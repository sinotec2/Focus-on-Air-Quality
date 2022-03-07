---
layout: default
title: AERMODs 遠端執行系統
parent: Remote Processing
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-03-07 13:29:39
---
# ISC/AERMOD 遠端執行系統
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
- [高斯煙流模式](https://www.eng.uwo.ca/people/esavory/Gaussian%20plumes.pdf)是大氣擴散模式中最常被應用的一大類別，是環保法規中的一環、也是民眾關切工廠污染的項目。
- 空間尺度數十公尺～50公里，時間尺度小時～5年。
- 關切的污染來源包括煙囪、道路、面源、體源。
- 整體大氣擴散模式的架構詳見[wiki](https://en.wikipedia.org/wiki/Atmospheric_dispersion_modeling) 、此處應用之模式包括ISC與AERMOD，其說明與應用詳見[空氣品質模式支援中心簡要描述](https://aqmc.epa.gov.tw/airquality_1.php)或[USEPA SCRAM](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#aermod)等官方網站。

### 目標
- 要在短時間內建立ISCST/AERMOD或其他煙流模式的工作流程並不容易，不單需要軟硬體的配合，也需要熟悉前處理的流程，整合了環境、大氣擴散、流體力學、地理圖學等學科，也需要資訊、環工、化工等工程基本訓練，使用者經常卡關而無法完成解析任務。
- 此外，面對政府公開資訊的浪潮，如何自動擷取、分析評估、裁切整合、將本土資料應用在關切的環境議題與環境法律架構中，也是值得推廣的環境教育項目之一。
- 最後，即使過去集合許多專家、工程師撰寫了數以萬計的程式碼，缺少應用的界面與推廣，也是曇花一現。因此如何有效、更多應用這些資源，發揮應有的價值，也是建立本系統的目的。

### 解決方案
- 在我國與其他先進國家，煙流模式是環保法規中技術成分很高的一環。基本上，模式的程式碼屬於公開領域、雖然也有商業軟體提供系統性的整合應用功能、有顧問公司提供評估報告整體技術服務，但基本上、核心的模式是透明公開的，可以由[USEPA SCRAM](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models)下載、更新。
- 由一般商業軟體套件(如[BREEZE AERMOD](https://www.trinityconsultants.com/software/dispersion/aermod)、[AERMOD View™](https://www.weblakes.com/products/aermod/index.html)、[AERMOD Cloud](https://www.envitrans.com/software-aermod-cloud.php)、[BEEST Suite](https://www.providenceoris.com/product/beest-suite/))的功能可以發現主要的技術瓶頸所在，包括(括弧內為本土化遭遇問題)：
  - 背景地圖顯示(台灣官方使用twd97系統與國外UTM無法接軌)
  - 氣象檔案產生、選取、基本檢核(中央氣象局數據無法併入系統)
  - 地形檔案之預備、資料切割、格式轉換、基本檢核(內政部dtm數據之應用)
  - 排放檔案之預備(既有污染源環保署TEDS數據之配套、檢核)
  - 建築物前處理(同樣也有座標問題)
  - 模擬結果等值圖產生(底圖之套用)
  - 分析表格的產出
- 除軟體或系統服務之外，亦有顧問公司提供技術服務，項目：
  - 提供AERMOD必要之數據([氣象](https://www.enviroware.com/aermod/)、[WRF-generated meteorological datasets](https://airqualitysupport.com.au/wrfdata/)等)
  - 前述技術分析之執行([雲端執行](https://www.trinityconsultants.com/software/high-speed-modeling-services/cluster-computing))、圖表的產出、分析、解釋
  - 環保法律文件（許可審查、環評分析）之準備、意見答覆、報告修正
- 付費（收費）的商業模式之所以存在的理由與必要，主要是前述學科與技術上的特性，也因此法律對專業證照制度確實有所要求。
- 然對民眾關切事項，政府或非官方單位也提供了免費的計算服務（或成果展現），如：
  - 火山影響之遠端解析
    - NOAA’s [HYSPLIT](https://www.ready.noaa.gov/HYSPLIT.php)（軌跡及空品模擬)
    - [UNRESP](https://vumo.cloud/what-is-vumo/) and [cemac/UNRESPForecastingSystem](https://github.com/cemac/UNRESPForecastingSystem)
  - 砂塵暴之遠端解析
    - 中央氣象局預報[境外污染傳輸趨勢](https://www.cwb.gov.tw/V8/C/W/AtmosPollution.html)
  - 污染源排放之立體空間解析([AEREarth](https://aerearth.airsci.com/))

### 整體界面與分支工作
綜上所述，不論是付費、免費之計算服務，作業項目之形成與污染源地點、模擬年代之確定有關，應為最基本、使用者必須輸入的項目。
- 氣象、地形、排放源、建築物等前處理
  - 雖為模式執行之整體流程，然個別也需提供界面，藉以確認、檢核或局部修正
- AERMOD主程式
  - 不論是一貫化作業流程、或使用者自備輸入檔，都應提供輸入界面
- 工作時間之管控
  - 整體流程中以氣象檔案之處理最耗費時間，且超過一般網頁等待時間，容易造成timeout錯誤，須列入背景幕後執行。
  - 其餘尚能在幕前運作。
  - 須建立程序管控程式，管理幕前、幕後工作之分配與同步化。

## Compute as a Service (CaaS)
- 服務窗口網頁位置：[http://114.32.164.198/aermods.html](http://114.32.164.198/aermods.html)
- Web site working hours:07:00\~19:00, Mon\~Fri

### 輸入範例：
- kml檔案，如下範例：
  - 4個污染源廠房頂點之座標，名稱分別為b1~b4，廠房高度皆為40m
  - 3座煙囪中心點位置，名稱分別為hs1~2、c1，高度為250、250、150m。
- 以[kml](https://zh.wikipedia.org/wiki/KML)檔案做為輸入座標介面的[理由](/Focus-on-Air-Quality/PlumeModels/RemoteSystem/aermods/#以kml檔案做為輸入座標介面的理由)。

```html
<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Placemark><ExtendedData><Data name="name"><value>b1 40</value></Data></ExtendedData>
        <Polygon><outerBoundaryIs><LinearRing>
                <coordinates>
                        120.19663095490615,22.857488325541038 120.19679403318152,22.85681209804539
                        120.19768667247264,22.85701773485837 120.19751071962675,22.857682097730326
                        120.19663095490615,22.857488325541038
                </coordinates>
        </LinearRing></outerBoundaryIs></Polygon>
</Placemark>
<Placemark><ExtendedData><Data name="name"><value>b2 40</value></Data></ExtendedData>
        <Polygon><outerBoundaryIs><LinearRing>
                <coordinates>
                        120.19689703007319,22.856535278808 120.19707298291907,22.855874864967262
                        120.19794845600703,22.85608050319815 120.197781086099,22.85674487061339
                        120.19689703007319,22.856535278808
                </coordinates></LinearRing></outerBoundaryIs>
        </Polygon>
</Placemark>
<Placemark><ExtendedData><Data name="name"><value>b3 40</value></Data></ExtendedData>
        <Polygon><outerBoundaryIs><LinearRing><coordinates>120.19745922101721,22.855811591521636
                120.19758796704993,22.855301449110527 120.19830465349516,22.85547149649191
                120.1981415750561,22.855965820333473 120.19745922101721,22.855811591521636</coordinates></LinearRing></outerBoundaryIs>
        </Polygon>
</Placemark>
<Placemark><ExtendedData><Data name="name"><value>b4 40</value></Data></ExtendedData>
        <Polygon><outerBoundaryIs><LinearRing><coordinates>120.19779825230219,22.85494948915392
                120.19794416453807,22.854431434225983 120.198652267718,22.854609392268987
                120.19849348074787,22.855107673489712 120.19779825230219,22.85494948915392</coordinates></LinearRing></outerBoundaryIs>
        </Polygon>
</Placemark>
<Placemark><ExtendedData><Data name="name"><value>hs1 250</value></Data></ExtendedData>
        <Point><coordinates>
                120.19625544548036,22.85676958667696</coordinates></Point></Placemark>
<Placemark><ExtendedData><Data name="name"><value>hs2 250</value></Data></ExtendedData>
        <Point><coordinates>
                120.19671678543092,22.854960364468663</coordinates></Point></Placemark>
<Placemark><ExtendedData><Data name="name"><value>c 150</value></Data></ExtendedData>
        <Point><coordinates>
                120.19549369812013,22.858133902251407</coordinates></Point></Placemark>
</Document>
</kml>
```

### 必須資訊說明
- 煙囪位置(點)：將做為模擬個案之中心座標
- 囪煙名稱：將做為個案名稱

### 輔助資訊
- 廠房建築物平面圖
  - 建築物頂點位置(多邊形)：必須「逆時針」方向輸入
  - 建築物名稱(含高度、名稱高度間可以空格、逗號、分號、斜槓等區格)
- 煙囪如有高度跟在名稱之後，將會優先使用，否則會從TEDS資料庫中選取位置最接近的煙囪。

### 數位板之使用
- 可以使用[數位板](http://114.32.164.198/LeafletDigitizer/index.html)點取座標值（另存成KML檔案）。
- 檢核：
  - [rotate_kml](http://114.32.164.198/rotate_kml.html)→旋轉角度，輸出成bpip輸入檔格式（詳見[Rotate_KML](https://www.evernote.com/l/AH2hvNqCSJlDq6SZOOYYMx4zimV-4cdbfQY)）
  - [iscParser](http://114.32.164.198/iscParser.html)→解讀bpip輸入檔，輸出成kml格式(反解)
### email
- 非必要項目。
  - 如不輸入，離開網頁後暫存訊息即消失
- 如輸入email，可隨時離開網頁，系統將寄結果之連結到信箱

## HTML
### 設計
- 以表格方式整理模擬過程、各程序之程式版本、內容、IO及範例、檢核方式以及筆記。
- 提交CGI_python([rd_kmlFull.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/rd_kmlFull.py))之物件
  - `filename`：kml檔名
  - `year`：氣象數據之年代
  - `emailadd`：電郵信箱(optional)

### coding
- [download html](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/aermods.html)

## CGI_PYTHON
### [rd_kmlFull.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/rd_kmlFull.py)之程式設計
此程式讀取html提供之kml檔案，進行解析後將依序執行：
- Rotate KML
- [BPIPPRIM]()
- [GENINP](/Focus-on-Air-Quality/PlumeModels/Terrain/gen_inp/) and AERMAP
- [MMIF]()
- [AERMOD]()
- WAIT and CHECK
  - wait_mmif4aermod.cs
  - wart_map4aermod.cs
  - chk_aermod.cs

### wait_mmif4aermod.cs coding
- 此批次檔主要執行mmif(aermod的氣象前處理程式)，aermod主程式及後處理程式，因為CGI程式不能等待太久，需將耗時的程式放在背景執行，因此需要有一批次檔持續察看執行情形，如有結果則啟動後續作業。
- 設計每30秒檢查一次mmif的執行緒數，如果只剩1個執行緒，則
  - 接著執行AERMOD
  - 進行後續後處理
    1. [Dat2kml](/Focus-on-Air-Quality/utilities/GIS/wr_kml/#dat2kml) 將PLOTFILE轉成等值線圖（KML格式、SURFER  grd格式）
    1. OLM後處理
    1. 壓縮所有結果
    1. 寄信

```bash
kuang@114-32-164-198 ~/Downloads
$ cat /opt/local/bin/wait_mmif4aermod.cs
#$1=path to zip
#$2=email
pth=$1
cd $pth
if compgen -G "mmif*out" > /dev/null; then
  MMIF=$(ls mmif*out|tail -n1)
else
  MMIF=0
fi
AERMOD=/Users/1.PlumeModels/AERMOD/aermod_source/aermod.exe

n=$(ps -ef|grep aermod.exe|wc -l)
n=$(( $n - 1 ))
m=$(ps -ef|grep aermap|wc -l)
n=$(( $n + $m - 1 ))
m=$(ps -ef|grep mmif|wc -l)
n=$(( $n + $m - 1 ))

web=/Library/WebServer/Documents
http=http://114.32.164.198
opth=${pth/$web/$http}

msg="Hello AERMOD user:\n Your aermod submit was accepted, please wait and check this email.\
    since "$n" aermap/mmif/aermod are running, the resultant zip file($opth/result.zip) may be erased after 48 hrs! \n \
    (sent by machine do not reply)"
echo $msg|mail -s "AERMOD ACCEPTED" $mailadd

if [ -e aermap.out ]; then
  while true;do
    SUC=$(grep Finishes|grep AERMAP|wc -l)
    if [ $SUC -eq 1 ];then
    break
    fi
    sleep 30s
  done 
fi

if [ $MMIF -ne 0 ];then
  while true;do
    SUC=$(grep Reached $MMIF|wc -l)
    if [ $SUC -eq 1 ];then
      break
    fi
    sleep 30s
  done
  cp *sfc /Library/WebServer/Documents/mmif_results/
  cp *pfl /Library/WebServer/Documents/mmif_results/
fi

for inp in $(ls *_[CNPS]*.inp);do
  out=${inp/inp/out}
  $AERMOD $inp $out >> isc.out &
done
```
## Discussion
### 以kml檔案做為輸入座標介面的理由
- [kml](https://zh.wikipedia.org/wiki/KML)為Google所發展、運維之語言，具有其穩定性。此處應用到其多邊形(Polygon, 標註廠房平面圖)、以及點(Point,標註煙囪中心位置)之記錄方式。
- 為許多繪圖軟體所接受，容易輸出。
- 充分使用既有開放源碼之數位板(Digitizer)與地圖功能、方便偵錯、
- 直接以經緯度系統輸入，可以避免地圖投影方式可能的錯誤

### Known Bugs and TODOs
- 同時需要花時間執行之程式可能包括mmif、aermap、aermod等等，如果超過工作站之核心數將會接近無限期等候，應設定停損點。
- 以蒐詢程式結果似容易出錯，建議改為針對pid進行定期ps檢視，不論程式是否出錯均能有效控制其結束時間。

## Reference

