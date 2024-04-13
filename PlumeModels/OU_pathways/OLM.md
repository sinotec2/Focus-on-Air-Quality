---
layout: default
title: Ozone Limiting Method
parent: OU Pathways
grand_parent: Plume Models
nav_order: 2
last_modified_date: 2022-03-21 09:23:54
tags: plume_model sed
---
# Ozone Limiting Method
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
### OLM的由來與定義
參考[JAPCA 1979]https://www.tandfonline.com/doi/abs/10.1080/00022470.1979.10470866)的文章，OLM最先用在美國新污染源審查過程中NO<sub>2</sub>模式模擬短期結果的修正，現國內也列於規範中。其公式為

  NO<sub>2</sub> = 0.1 NO<sub>x</sub> + min( O<sub>3b</sub>, 0.9 NO<sub>x</sub> ) + NO<sub>2b</sub>

- NO<sub>x</sub>為模式模擬之地面濃度
- O<sub>3b</sub>、NO<sub>2b</sub>為觀測之背景臭氧與二氧化氮濃度

### OLM的基本假設：
- NO轉化成NO<sub>2</sub>是瞬間反應
- NO<sub>2</sub>的光解現象是可以忽略的
- 煙流中O<sub>3</sub>的濃度與測站測值(背景值)是一致的

### 方案討論
- 按照USEPA的篩選邏輯，背景值轉化率及可以使用地區平均值、季節或月平均值等方式，做為各篩選階段計算的參數。
- 法規評估選項中則要求使用下圖中的Tier 3 chemistry methods, 包括化學轉化之Ozone Limiting Method(OLM) 與煙流入滲之 Plume Volume Molar Ratio Method(PVMRM)。
- 相關作法在2017規範修正。

| ![OLM1.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/OLM1.png)|
|:--:|
| <b>NO<sub>2</sub>模擬結果多層次分析過程</b>|

- AERMOD
  已將OLM列入NO<sub>2</sub>模擬的設定(CO O3VALUES或CO OZONEFIL)及輸出處理程序之中。
  - 最終仍以地區代表性測站、逐時進行校正為依歸。

- ISCST3
  - 沒有這項功能，現階段只能以後處理方式進行OLM修正
- 台灣地區都會區有較多的空品測站可以做為背景測站。
  - 就保守之角度，似以所有附近測站皆計算一遍取較大值為合理結果。
  - 以AERMOD而言，須做多次、重複的模擬計算
  - 以ISCST3而言，模擬只須一次，後處理須對所有附近測站進行重複計算
  - 美國PSD並不考慮背景NO<sub>2</sub>濃度，只計算增量，因此AERMOD OLM並未加上NO<sub>2b</sub>，而是計算完後再加上背景值，雖然在同一檔案內可以接受SO BACKGRND選項。

### 作業目標
- 背景值：採測站之逐時值
- 測站：採最近的測站(範例為新北之土城及新莊測站)
- 年代：模擬及實測皆採3年數據(範例為2016~2018年全年)
- 模擬接受點：計有31 x 31個網格點與3個敏感點
- 模式：ISCST3

### 重要技術細節
- 環保署測站測值之快速讀取：應用master:/usr/kbin/specHrSliderRect.py、用sed去頭後、用cat指令連成一個大檔備用
- 輸出逐時之模式模擬結果：要在OU段落設POSTFILE，格式選用PLOT以產生.dat格式檔備用。
- 2個矩陣逐點比較後選小值，在numpy的函數為minimum，詳參官網說明。
### CaaS
- 網址： http://sinotec24.com/OLM.html
- 注意事項：
  - 濃度單位不另轉換，須配合環保署資料，全為ppb。
  - 接受點系統的排列順序為：GRIDCART -》 DISCCART。NRcart、NRdisc可以為零，但順序不能弄錯。
  - 不限模擬時間。如有跨年需在上傳前先行合併。
  - 檔案如果過大（50MB）上傳時間會大於Gateway Timeout限制時間，讓OLM.py停擺，
    - 因此必須先行壓縮。目前接受.gz、.zip等2種壓縮形式。
    - Chrome timeout設為5min，事實上比此數字還小。建議改用firefox。(see [stackoverflow](https://stackoverflow.com/questions/39751124/increase-timeout-limit-in-google-chrome))
  - 目前Mac上環保署的數據只有2018~2020，如需別的年期，需另行下載EPA數據。
  - 暫存檔停留時間為48小時。每天清除2天前的檔案。
- 畫面：

| ![OLM2.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/OLM2.png)|
|:--:|
| <b>煙流模式NOx逐時結果之臭氧限制法後處理畫面與程式[界面](http://sinotec24.com/OLM.html)</b>|

## 環保署測站數據之讀取與準備
### [specHrSliderRect.py](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/specHrSlider/)
此處應用master:/usr/kbin/specHrSliderRect.py讀取。該程式為歷線繪圖程式，然為方便存取，程式設計輸出指定測站、成分、日期之csv檔案到所在目錄備用。

如果--action(-a)選擇，則將進入批次作業方式，如下所示。

- CaaS方案-程式外合併分析方案
  - 測站選擇：以模擬範圍中心到附近環保署測站距離為準，取最近的3站。
  - 時間選擇：以PLOT檔案內DATE之起訖時間為準

```bash
$ cat -n OLM.py
...
  17    sph='/opt/local/bin/specHrSliderRect.py'
...
  98    # perform the extraction of EPA data 
  99      for stn in stnames:
  100        fname= rst+'NO2O3'+stn+begdate+enddate+'.csv'
  101        if os.path.isfile(fname):continue
  102        cmd ='cd '+rst+';'
  103        cmd+= sph+' -t '+stn+' -s NO2,O3 -b '+begdate+' -e '+enddate+' -a s>>/tmp/wrose/wrose.out' 
  104        os.system(cmd)
```

- 3年3檔程式內合併分析方案
  - 測站選擇：新莊、土城
  - 時間選擇：2016～2018

```bash
for i in {16..18};do
    for s in xinzhuang tucheng;do
        specHrSliderRect.py -t $s -s NO2,O3 -b 20${i}0101 -e 20${i}1231 -a s
    done
done
```
- 2層for迴圈將產生6個檔案。

```bash
$ ls -lh NO2O3[xt]*201*.csv
-rwxrwxrwx 1 kuang SESAir 375K  1▒▒ 14 15:37 NO2O3tucheng2016010120161231.csv
-rwxrwxrwx 1 kuang SESAir 375K  1▒▒ 14 15:37 NO2O3tucheng2017010120171231.csv
-rwxrwxrwx 1 kuang SESAir 375K  1▒▒ 14 15:37 NO2O3tucheng2018010120181231.csv
-rwxrwxrwx 1 kuang SESAir 393K  1▒▒ 14 15:37 NO2O3xinzhuang2016010120161231.csv
-rwxrwxrwx 1 kuang SESAir 392K  1▒▒ 14 15:37 NO2O3xinzhuang2017010120171231.csv
-rwxrwxrwx 1 kuang SESAir 392K  1▒▒ 14 15:37 NO2O3xinzhuang2018010120181231.csv
```

### 按時間合併檔案
- 為分析方便，將3年的數據連成一個大檔。cat時檔案會照名稱順序依序輸出，亦即會照年代累加。

```bash
cat NO2O3tucheng201*.csv>tucheng.csv
cat NO2O3xinzhuang201*.csv>xinzhuang.csv
```
- 去表頭
  - 其中表頭會重複造成困擾
  - 用sed將其去掉，因格式都相同，在python中統一再加回即可。
sed -i '/YMDH,NO2,nam,O3,YMD,MDH/d' [xt]*csv

## ISCST3/aermod執行
### 在使用者端先行執行
- 煙流模式輸出逐時值
  - 因為檔案很大，過去一般模擬作業會避免輸出逐時值，
  - 如果輸出，也以binary(format=UNFORM)格式來儲存，需以fortran binary格式讀物。
  - 然為考慮讀取方便，還是以PLOT檔案格式(即一般的文字檔.dat格式)，檔案雖不小，但還在目前磁碟機容許範圍。
  - 設定範例如下

```bash
(py37)
kuang@master /home/iscstruns/SANYING
$ tail sanying.inp
  RECTABLE ALLAVE 1st-8th
  MAXTABLE ALLAVE 8
  PLOTFILE 1 ALL 8th  NOx-H.DAT
  PLOTFILE PERIOD ALL  NOx-Y.DAT
  POSTFILE 1    A  PLOT SANYINa.PLT
  POSTFILE 1    B  PLOT SANYINb.PLT
  POSTFILE 1    C  PLOT SANYINc.PLT
  POSTFILE 1    ALL PLOT SANYING.PLT
OU FINISHED
```
- 範例中共輸出4個PLT檔案，分別是排放群組A~C與ALL的結果。
- 其檔案與一般繪圖用的PLOTFILE一樣：
  - 濃度在第3欄
  - 時間在第7欄

```bash  
kuang@master /home/iscstruns/SANYING
$ head *8/*a.PLT
* ISCST3 (02035):  TEST RUN BY KUANG
* MODELING OPTIONS USED:
*  CONC                    URBAN FLAT        DFAULT
*        POST/PLOT FILE OF CONCURRENT  1-HR VALUES FOR SOURCE GROUP: A
*        FOR A TOTAL OF  964 RECEPTORS.
*        FORMAT: (3(1X,F13.5),1X,F8.2,2X,A6,2X,A8,2X,I8.8,2X,A8)
*        X            Y      AVERAGE CONC  ZELEV    AVE    GRP      DATE    NET ID
*  ___________  ___________  ___________  ______  ______  ________  ________  ________
  292000.00000 2761000.00000      0.00000    0.00    1-HR  A        18010101  GRD1
  292200.00000 2761000.00000      0.00000    0.00    1-HR  A        18010101  GRD1
```
- 如果是AERMOD的輸出結果略有不同，
  - 時間標籤是在第9欄(多了ZHILL    ZFLAG 2欄)

```bash
$ tail SANYING.PLT
* AERMOD ( 19191):  A Simple Example Problem for the AERMOD Model with PRIME                03/19/21
...
*        X            Y      AVERAGE CONC    ZELEV    ZHILL    ZFLAG    AVE    GRP      RANK    NET ID  DATE(CONC)
...
  292200.00000 2766800.00000      0.00000    0.00    0.00    0.00    1-HR  ALL      18122715  GRD1
  292400.00000 2766800.00000      0.00000    0.00    0.00    0.00    1-HR  ALL      18122715  GRD1
  292600.00000 2766800.00000      0.00000    0.00    0.00    0.00    1-HR  ALL      18122715  GRD1
  292800.00000 2766800.00000      0.00000    0.00    0.00    0.00    1-HR  ALL      18122715  GRD1
```
### 批次執行
- 由於iscst須執行3年，檔案名稱會重疊，因此須建立目錄執行並存放，inp檔案內有關年代的設定，則以sed來修改。

```bash
kuang@master /home/iscstruns/SANYING
$ cat sanying.cs
for i in 17 16 18;do
    cd SANYING$i
    ln -sf ../46692v01_$i.ASC 46692v01.asc
    sed -e s/2018/20$i/g ../sanying.inp >sanying.inp
    sub iscst3 sanying.inp sanying.out >&a
    cd ..
done
```

## Python程式設計說明
### 讀取PLT檔案之濃度值
- 由前述PLT的printout得知，濃度位在第3個位置、小時標籤在第7欄
- 因逢潤年，每一年的小時數(NHR)可能不同，因此需要讀取NHR來重整矩陣。
- 3年的PLT檔案讀出後，依序填入Ca矩陣中備用。

```python
    23    C=[]
    24    for i in range(16,19):
    25      fname='SANYING'+str(i)+'/SANYIN'+g+'.PLT'
    26      with open( fname,'r') as f:
    27        ll=[l for l in f]
    28      ll=ll[8:]
    29      HR=[int(l.split()[6]) for l in ll]
    30      HRs=list(set(HR))
    31      HRs.sort()
    32      NRE=HR.index(HRs[1])
    33      NHR=len(HRs)
    34      C.append(np.array([float(l.split()[2]) for l in ll]).reshape(NHR,NRE))
    35    begH=0
    36    for i in range(ny):
    37      endH=begH+nday[i]*24
    38      Ca[begH:endH,:]=C[i]
    39      begH=endH
```

### 逐時、逐點OLM之計算
-依序調用不同空品測站的背景值計算，形成時間及空間的矩陣。
- 計算以矩陣方式進行，運用前述minimum函數取2個矩陣之較小值
- 背景值只有時間的維度，空間上取None。
  - Warning: NO2b[:,:]=df.NO2[:,None] 這種用法似已經不再維護，保險起見，還是應該加np.array如：
  ```python
  no2=np.array(df.NO2)
  NO2b[:,:]=no2[:,None]
  ```

```python
    40    OLMa=[]
    41    for i in range(NS):
    42      df=dfa[i]
    43      NO2b[:,:]=df.NO2[:,None]
    44      O3b[:,:]=df.O3[:,None]
    45      OLMa.append(0.1*Ca+NO2b+np.minimum(0.9*Ca,O3b))
```

### 逐日計算區域之最大值
- 時間分段進行np.max

```python
    46    OLMmx=[]
    47    for i in range(NS):
    48      olmx=[]
    49      olm=OLMa[i]
    50      for d in range(1,ndays+1):
    51        olmx.append(np.max(olm[(d-1)*24:d*24,:],axis=(0,1)))
    52      OLMmx.append(olmx)
```
### 逐日計算敏感點之最大值
- 敏感點列在所有接受點的末三行，是固定的位置。依序將其讀出成序列olm。
- 時間也是分段進行np.max

```python
    53    OLMremx=[]
    54    for i in range(NS):
    55      olmr=[]
    56      for r in range(NRdisc,0,-1):
    57        olmx=[]
    58        olm=OLMa[i][:,NRE-r]
    59        for d in range(1,ndays+1):
    60          olmx.append(np.max(olm[(d-1)*24:d*24]))
    61        olmr.append(olmx)
    62      OLMremx.append(olmr)
```
### 輸出
- 依序印出各群組與所有污染源造成之最大NO<sub>2</sub>濃度
- 全區最大值：[土城、新莊]
- 3敏感點最大值：[土城、新莊]

```python
    63    print([[max(OLMmx[i]) for i in range(NS)]])
    64    print([[max(OLMremx[i][r]) for r in range(NRdisc)] for i in range(NS)])
```    
## 結果
- ISCST3

```bash
group A
[[164.545512, 170.241353]]
[[146.048531, 102.0, 102.0], [140.86495200000002, 93.82071, 93.0]
group B
[[102.0, 93.0]]
[[102.0, 102.0, 102.0], [93.0, 93.0, 93.0]]
group C
[[163.600081, 171.600081]]
[[102.0, 102.0, 163.600081], [93.0, 93.00052, 171.600081]]
group ALL
[[170.455872, 171.656184]]
[[147.86078500000002, 102.26189, 163.656184], [140.865016, 99.3466, 171.656184]]

csv2kml.py -f NOx-Y.DAT -d ALL (*)
```

- KML檢視，可以使用[地圖貼板](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/digitizer/#地圖貼板)：http://sinotec24.com/Leaflet.FileLayer/docs/index.html
- http://sinotec24.com/iscParser.html

- AERMOD
```bash
group A
[[161.35201, 165.25201]]
[[103.765701, 102.0, 102.0], [109.765701, 93.0, 93.0]]
group B
[[102.0, 93.0]]
[[102.0, 102.0, 102.0], [93.0, 93.0, 93.0]]
group C
[[786.582206, 790.482206]]
[[135.47926, 102.0, 675.361295], [133.57926, 93.0, 673.9612950000001]]
group ALL
[[1288.4276920000002, 1281.2276920000002]]
[[198.65718900000002, 102.0, 675.361295], [196.757189, 93.0, 673.9612950000001]]
```
## Coding
### OLM.html
- 除了說明文字圖像之外，就只有一個jquery的[filepicker](https://github.com/benignware/jquery-filepicker)物件。

### OLM.py
- 與前述程式最大的不同，除了CGI部分的IO之外，為減少客戶重複的選項，程式內部會先行研判是否已經有下載過、如果沒有，由程式研判測站及時間，以執行specHrSlider.py*程式。
- 其次，程式會輸出最大值相關訊息，成為root_rep.txt的內容，也是本程式的特色。

```bash
* ISCST3 (02035):  捷運萬大線二期第3次環差                               
* MODELING OPTIONS USED:
*  CONC                    URBAN ELEV        DFAULT                                                        NOSMPL
*        POST/PLOT FILE OF CONCURRENT  1-HR VALUES FOR SOURCE GROUP: ALL
*        FOR A TOTAL OF    3 RECEPTORS.
*        NUM OF DISCCART: 3
* NUMBER OF SIMULATION HOURS IS: 8760,*  FROM 20180101 TO 20181231
* NEAREST 3 STATIONS ARE: tucheng banqiao xinzhuang
*  MAX (NO2B,O3B) FOR tucheng STATIONS ARE: 81.000000 129.000000
*                            MAX HR ARE: 2018122009 2018052412
*  MAX OLN_NO2 IN ALL RECPTs FOR tucheng STATIONS IS: 123.562160 MAX HR IS : 18120613 MAX XY ARE: (294911, 2762966)
*  (NO2B,O3B) FOR tucheng AT THAT TIME: 35.000000 83.000000
*  MAX OLN_NO2 IN DISCCART  FOR tucheng STATIONS ARE:114.554395@18120411, 123.562160@18120613, 90.480320@18122010,
*  (NO2B,O3B) FOR tucheng AT THAT TIME:(67.000000, 41.000000), (35.000000, 83.000000), (81.000000, 19.000000),
*  MAX (NO2B,O3B) FOR banqiao STATIONS ARE: 81.000000 114.000000
*                            MAX HR ARE: 2018120409 2018091713
*  MAX OLN_NO2 IN ALL RECPTs FOR banqiao STATIONS IS: 124.554395 MAX HR IS : 18120411 MAX XY ARE: (296123, 2764056)
*  (NO2B,O3B) FOR banqiao AT THAT TIME: 79.000000 39.000000
*  MAX OLN_NO2 IN DISCCART  FOR banqiao STATIONS ARE:124.554395@18120411, 122.515923@18120411, 81.000000@18120410,
*  (NO2B,O3B) FOR banqiao AT THAT TIME:(79.000000, 39.000000), (79.000000, 39.000000), (81.000000, 19.000000),
*  MAX (NO2B,O3B) FOR xinzhuang STATIONS ARE: 73.000000 108.000000
*                            MAX HR ARE: 2018041020 2018042112
*  MAX OLN_NO2 IN ALL RECPTs FOR xinzhuang STATIONS IS: 120.856216 MAX HR IS : 18011614 MAX XY ARE: (294911, 2762966)
*  (NO2B,O3B) FOR xinzhuang AT THAT TIME: 43.000000 69.000000
*  MAX OLN_NO2 IN DISCCART  FOR xinzhuang STATIONS ARE:114.554395@18120411, 120.856216@18011614, 73.000000@18041021,
*  (NO2B,O3B) FOR xinzhuang AT THAT TIME:(60.000000, 48.000000), (43.000000, 69.000000), (73.000000, 5.900000),
```

## REF
### Reference
- Henry S. Cole & John E. Summerhays (1979) **A Review of Techniques Available for Estimating Short-Term NO2 concentrations**, [Journal of the Air Pollution Control Association, 29:8, 812-817, DOI: 10.1080/00022470.1979.10470866](https://www.tandfonline.com/doi/abs/10.1080/00022470.1979.10470866)
USEPA (2017) **Revisions to the Guideline on Air Quality Models: Enhancements to the AERMOD Dispersion Modeling System and Incorporation of Approaches to Address Ozone and Fine Particulate Matter;** [U.S. Environmental Protection Agency, 40 CFR Part 51, RIN 2060-AS54,]() 2017.
### Guidance
- numpy.minimum
- sed
  - [wiki](https://zh.wikipedia.org/wiki/Sed)
  - [Linux 指令 SED 用法教學、取代範例、詳解](https://terryl.in/zh/linux-sed-command/)
- None
  - [Efficient way to add a singleton dimension to a NumPy vector so that slice assignments work](https://stackoverflow.com/questions/9510252/efficient-way-to-add-a-singleton-dimension-to-a-numpy-vector-so-that-slice-assig)
### Family
  - here:OLM in python*
  - parent:Dr. Kuang's Evernotes_Plume models(*)
  - relatives：
    - [specHrSlider.py](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/specHrSlider/)
