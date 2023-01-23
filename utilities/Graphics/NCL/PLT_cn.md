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
- 執行之母程式：[NCLonOTM-cgi.py](NCLonOTM.md)，也將由該程式繼續完成貼上底圖。

## 程式碼說明

### 讀取檔案

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

### 繪製等值線圖

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