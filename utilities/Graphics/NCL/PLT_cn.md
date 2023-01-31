---
layout: default
title: 煙流模式結果繪製等值線圖
parent: NCL Programs
grand_parent: Graphics
has_children: true
last_modified_date: 2023-01-23 21:06:51
tags: NCL graphics plume_model
---

# 煙流模式結果繪製等值線圖
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

- 此處讀取煙流模式結果的PLT檔案（for SURFER的[x,y,c]濃度檔案），繪製等值線圖。
- 程式下載：[PLT_cn.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/PLT_cn.ncl)
- 執行之母程式[^2]：[NCLonOTM-cgi.py](../CaaS/NCLonOTM-cgi.md)，也將由該程式繼續完成貼上底圖。
- 等值線圖需要的底圖，可以參考[^1]。

## 程式碼說明

### 讀取檔案

如以[NCLonOTM-cgi.py](../CaaS/NCLonOTM-cgi.md)處理，該母程式將產生下列3個檔案。如獨立運作，使用者則需自行提供檔案。

1. param.txt：網格設定（x0,nx,dx,y0,ny,dy）
2. title.txt：標題
3. tmp.PLT：煙流模式輸出檔（去檔頭）

```bash
begin
;---Open file; substitute your own WRF output file here
  nxy=asciiread("param.txt",(/6/),"integer")
  nx=nxy(1)
  ny=nxy(4)
  t=asciiread("title.txt",1,"string")
  tit=t(0)
  f=asciiread("tmp.PLT",(/ny*nx,3/),"float")
  nnn=dimsizes(f)
  npt=toint(nnn/3)
  p=new((/ny,nx/),float)
  do j=0,ny-1
  do i=0,nx-1
    ji=j*nx+i
    p(j,i)=f(ji,2)
  end do
  end do
```

### param.txt之考量

- 直角座標系統的必要性
  - 由於煙流模式必須用直角座標系統來設定接收點及排放口位置，不接受經緯度系統
  - NCL雖然可以接受經緯度、但網格定義仍然是用等間距系統
  - 雖然各式地圖以經緯度為主，但在此還是要用直角座標系統
  - 在此使用TWD97(2度分帶)系統，符合內政部地圖系統的要求
- 外部檔案的必要性
  - NCL 的asciiread可以接受未知維度、長度的檔案，但是要在NCL程式內判斷檔案X軸及Y軸的格點數，因為沒有set()指令，困難度太高了、不建議繼續嘗試。
  - 在cgi_python內呼叫os.system("echo”)指令，將nx,ny等設定參數寫在檔案param.txt內(此處ncl程式只有用到網格數)
  - 在NCL內讀入維度、宣告檔案及變數的陣列大小、可以順利將矩陣讀入
- param.txt至少要輸入[RE GRIDCART](#re-gridcart)6個數字，數字的內容、順序及意義如[下表](#re-gridcart)所示。

### PLT 檔案之考量

- 由於此處的NCL程式並不會重新進行regrid計算，因此必須是單一網格系統之接受點。
  - 目前NCL尚不接受加入離散點、
  - X、Y方向的間距「必須」相等，可接受不同方向的格點數不同(nx!=ny)
- 然因煙流模式目前尚無法區分網格系統或離散點分別輸出成PLT檔，可行因應的方式包括：
  - 先使用dat2kml產生.grd檔(已實現)
  - 刪除煙流模式中有關其他網格系統、離散點的設定、重新執行煙流模式。
  - 另在python程式內做regrid，輸出等間距網格的結果。
  - 修改NCL程式、重新進行regrid
- PLT檔案內容範例與說明，詳見[PLOTFILE to KML#plotfile範例](../../../PlumeModels/OU_pathways/PLT2kml.md#plotfile範例)

### 繪製等值線圖

- 等值圖的像素考量
  - 在疊圖過程中，需要保持底圖與等值線圖有接近的解析度，如此二者失真的情況可以降到最低。
    - 縮放地圖：因地圖是格柵圖、不能夠縮放。
    - 縮放等值圖：雖然NCL不能輸出向量檔，但因為等值線相對單純、微小的縮放尚能接受。
  - 唯一需要控制像素
    - 在wks_type函數內控制，在此抓整個圖約2000像素、圖框內約控制在1500左右
    - 此處XY方向保持一樣（如有需要可以按照nx/ny比例修改）
- 等值線的粗細
  - 由於等值線要在複製的地圖上表現清楚，必須加粗。
  - 在nLineThicknessF變數控制，內設為1，此處設為7。
- 座標系統考量
  - 此處使用的模組為`gsn_csm_contour`，座標軸為xy之格點序，並沒有搭配座標系統與底圖，可以呈現最清晰的線條。
  - 還需另外貼上底圖

```bash
;---Create simple contour plots  
   wks_type = "png"
   wks_type@wkWidth = 2000
   wks_type@wkHeight = 2000
   wks = gsn_open_wks(wks_type,"tmp_cn")

  res                       = True            ; plot mods desired
  res@gsnMaximize           = True            ; maximize plot size
  res@tiMainString          = tit             ; main title
  res@cnLineThicknessF      =7
  plot                      = gsn_csm_contour(wks,p(:,:),res)
end
```

### 後處理

- 將繼續執行[NCLonOTM](NCLonOTM.md)將等值線圖貼在OTM底圖上。

## 基隆某電廠範例

### RE GRIDCART

- 此項設定除了pathway（RE）與keyword(GRIDCART)之外，還有網格系統的名稱與6個數字，如：`RE GRIDCART gd1 290700 40 1250 2746400 40 1250`
- 6個數字分別為：

項目|設定內容|說明
-|-|-
x0|290700|原點x座標，單位為m(TWD97系統)
nx|40|東西向格點數
dx|1250|東西向格點間距(m)
y0|2746400|原點y座標，單位為m(TWD97系統)
ny|40|南北向格點數
dy|1250|南北向格點間距(m)

### 結果圖檔

![tmp_cn.png](https://drive.google.com/uc?id=1DK7QFdVjCEk-MRA9K8klC-IsnUhyqa5W)

[^1]: 集合OTM圖磚並修剪成tiff檔之py程式，詳見[tiles_to_tiffFit.py程式說明](../CaaS/tiles_to_tiffFit.md)，或下載[tiles_to_tiffFit.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/tiles_to_tiffFit.py)
[^2]: 獨立程式說明[NCL貼在OTM底圖上](NCLonOTM.md)或NCLonOTM遠端服務,[NCLonOTM-cgi.py](../CaaS/NCLonOTM-cgi.md)