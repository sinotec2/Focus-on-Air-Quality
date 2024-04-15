---
layout: default
title: caline3遠端計算服務
parent: CALINE
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-04-08 15:30:32
tags: plume_model CGI_Pythons
---
# *caline3*遠端計算服務
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
- CALINE3目前仍是美國環保署公告的[替代模式](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/LargeSSPtSrcEIA/1Gaus_Stab/#usepa-scram模式種類架構)。其設定與執行詳見[CALINE3的標準輸入輸出](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/CALINE3IO/)，此處介紹遠端執行的版本。
- 模式未來發展：因CALINE後續沒有發展的計畫，系統應無持續更新的需要。

### caline3遠端計算服務
- 網址[http://sinotec24.com/CALINE3.html](http://sinotec24.com/CALINE3.html)
- 選取本地的[輸入檔案](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/caline.inp)、按下Run鍵即可。
- 同一位置也可以選擇.kml檔案，內容約定如後所述。氣象條件為8風向。

| ![CALINE_remote.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/CALINE_remote.PNG)|
|:--:|
| <b>CALINE[遠端計算網頁](http://sinotec24.com/CALINE3.html)畫面</b>| 

### CaaS檔案結構與連結
- HTML
  - $web/[CALINE3.html](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/CALINE3.html)
  - 使用[filepicker](https://github.com/benignware/jquery-filepicker)開啟使用者指定上傳的檔案
- CGI-PY：$cgi/caline/[CALINE.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/CALINE.py)，詳[說明](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/CALINE/)
- EXE
  - `CLINE='/Users/1.PlumeModels/CALINE3/caline3 '`，編譯自[CALINE3.FOR](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/CALINE3.FOR)，Y軸座標格式修改如下[說明](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/CALINE/caline_remote/#caline3for-輸出座標格式調整)。
  - KML2INP=CGI+'[kml2inp.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/kml2inp.py)'
- HEADER：$cgi/caline/[header.txt](https://github.com/sinotec2/CGI_Pythons/blob/main/ISCST_AERMOD/header.txt)
- 工作目錄與結果
  - $web/caline_results/clin_ **RAND**/
  - CALINE3.OUT
  - **RAND**為隨機產生之6碼文字

## KML 輸入與轉檔
### 輸入方式
- 輸入檔也接受.kml的形式，也算是有圖形界面的功能。約定如下：
  - 以[數位板Digitizer](http://sinotec24.com/LeafletDigitizer/index.html)建立路段與接受點的空間及屬性資料
  - 接受點與路段的順序不限
  - 一條路可接受最多50個折點（49個路段）
  - 範例如[example.kml](http://sinotec24.com/caline_results/example.kml)(如下圖)
  - 氣象與現場條件設定如下：
    - BRG:0, 45, 90, 135, 180, 225, 270, 315 等8個風向
    - U, CLAS, MIXH: 1.0m/s, 6, 100m
    - ATIM, Vs, Vd, Z0, AMB: 60min, 0, 0, 100cm, 1.0PPM
- 物件屬性的順序（在數位板上有提示）
  - 接受點：名稱、高度
  - 路線(折線)：名稱、路型、交通量、排放係數、路高及路寬
  - 屬性間的間隔可以是：`,;_/ |-(`

| ![atts.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/atts.png)|
|:--:|
| <b>[數位板](http://sinotec24.com/LeafletDigitizer/index.html)提示鍵入物件名稱與屬性</b>| 

| ![sanchong.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/sanchong.png)|
|:--:|
| <b>[數位板](http://sinotec24.com/LeafletDigitizer/index.html)所建立的範例檔案</b>| 

### kml轉成輸入檔案caline.inp([kml2inp.py](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/kml2inp.py))
- 這支內部程式的用意就是當使用者輸入kml檔時，由[CGI-PY](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/CGI-pythons/CALINE/)啟動轉檔，以利繼續執行CALINE3。
- 與其他[rd_kml](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/rd_kml/#rd_kmlpy)有類似的讀取方式，而與[rd_dat.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/PlumeModels/CALINE/rd_dat.py)有類似的輸出結構，不再贅述。
- 讀取kml檔內的資訊

```python
fname=sys.argv[1]
NS,NR,nms,hgts,lon,lat,lonp,latp,TYPs,VPHs,EMFs,WIDs=rd_kmlLL(fname)
```
- 8風向氣象條件

```python
NM=8
parm={'U':1.0,'CLAS':6,'MIXH':100,'AMB':1.0}
for var in 'U CLAS MIXH AMB'.split():
  exec(var+'=[parm["'+var+'"] for i in range(NM)]')
BRG=[45*i for i in range(NM)]
```
- 接受點及線段座標都要轉換成TWD97系統(CALINE輸出格式問題另進[CALINE3.FOR](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/CALINE3.FOR)內修改)

```python
#receptors
recp,zr=nms[NS:],hgts[NS:]
xr,yr=pnyc(lonp, latp, inverse=False)
xr=[int(i+Xcent) for i in xr]
yr=[int(i+Ycent) for i in yr]

#links
NL,(lnks,X1,Y1,X2,Y2,TYP,VPH,EMF,H,W)=0,([] for i in range(10))
for l in range(NS):
  llt=[i for i in lat[l,:] if i !=0]
  lln=[i for i in lon[l,:] if i !=0]
  x,y=pnyc(lln, llt, inverse=False)
  x=[int(i+Xcent) for i in x]
  y=[int(i+Ycent) for i in y]
  X1+=x[:-1]
  Y1+=y[:-1]
  X2+=x[1:]
  Y2+=y[1:]
  ms=len(llt)-1
  lnks+=[nms[l]+'_'+str(i) for i in range(ms)]
  TYP+=[TYPs[l] for i in range(ms)]
  VPH+=[VPHs[l] for i in range(ms)]
  EMF+=[EMFs[l] for i in range(ms)]
  H+=[hgts[l] for i in range(ms)]
  W+=[WIDs[l] for i in range(ms)]
  NL+=ms
```
## [CALINE3.FOR](https://github.com/sinotec2/CGI_Pythons/blob/main/CALINE/CALINE3.FOR) 輸出座標格式調整
- 計有3處調整，以便讓TWD97南北方向座標值(共9碼)可以順利寫出。

```fortran
...
C 290 FORMAT (4X,A1,2H. ,5A4,2X,1H*,4(1X,F6.0,1X),1H*,4X,F6.0,          CLN07190
  290 FORMAT (4X,A1,2H. ,5A4,2X,1H*,4(   F8.0   ),1H*,4X,F6.0,          CLN07190
     *    6X,F4.0,6X,A2,2X,F6.0,1X,F5.1,1X,F5.1,2X,F4.1)                CLN07200
...
C 340 FORMAT (4X,I2,2H. ,5A4,1X,1H*,4X,F6.0,3X,F6.0,3X,F6.1, !by kuang  CLN07320
  340 FORMAT (4X,I2,2H. ,5A4,1X,1H*,1X,F9.0,   F9.0,3X,F6.1,            CLN07320
     *    3X,1H*,F5.1)                                                  CLN07330
...
C 490 FORMAT (4X,I2,2H. ,5A4,1X,1H*,4X,F6.0,3X,F6.0,3X,F6.1, !by kuang  CLN07480
  490 FORMAT (4X,I2,2H. ,5A4,1X,1H*,1X,F9.0,   F9.0,3X,F6.1,            CLN07480
     *    3X,1H*,F6.1)                                                  CLN07490

```

## 結果
- 結果檔名稱為固定
- 執行過程也很快，pid基本上沒有作用。

```
pid= 23318 is already done.
Model_results:
CALINE3.OUT
caline.inp
```