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
- 執行之母程式：[NCLonOTM-cgi.py](../CaaS/NCLonOTM-cgi.md)，也將由該程式繼續完成貼上底圖。

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

- 注意事項
  - NCL 的asciiread可以接受未知維度、長度的檔案，但是要在NCL程式內判斷檔案X軸及Y軸的格點數，因為沒有set()指令，困難度太高了、不建議繼續嘗試。
  - 在cgi_python內呼叫os.system("echo”)指令，將nx,ny等設定參數寫在檔案param.txt內(此處ncl程式只有用到網格數)
  - 在NCL內讀入維度、宣告檔案及變數的陣列大小、可以順利將矩陣讀入

### 繪製等值線圖

- 等值圖的像素考量
  - 在疊圖過程中，需要保持底圖與等值線圖有接近的解析度，如此二者失真的情況可以降到最低。
    - 縮放地圖：因地圖是格柵圖、不能夠縮放。
    - 縮放等值圖：雖然NCL不能輸出向量檔，但因為等值線相對單純、微小的縮放尚能接受。
  - 唯一需要控制像素
    - 在wks_type函數內控制，在此抓整個圖約2000像素、圖框內約控制在1500左右
    - 此處XY方向保持一樣（如有需要可以按照nx/ny比例修改）
- 等值線的粗細：
  - 由於等值線要在複製的地圖上表現清楚，必須加粗。
  - 在nLineThicknessF變數控制，內設為1，此處設為7。

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
