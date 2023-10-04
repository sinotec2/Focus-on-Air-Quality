---
layout: default
title: 環境部測站濃度分布圖之加工
parent: matplotlib Programs
grand_parent: Graphics
date: 2023-05-30
last_modified_date: 2023-05-30 09:34:02
tags: geoplot graphics choropleth
---

# 環境部測站濃度分布圖之加工
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

- 嚴格來說，這次的貼圖並沒有使用matplotlib模組，而是使用PIL模組來進行像素的計算。
- 底圖使用[m3nc2gif.py][m3nc2gif]d03紅黃綠色階版本
- 由於[環境部濃度圖](https://airtw.moenv.gov.tw/)的解析度與畫素較低，因此先將前述底圖用[convert](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/imageMagicks/)程式來reshape，再進行平移。
- 2個圖重疊的原理，參考[NCL貼在OTM底圖上 NCLonOTM](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL/NCLonOTM/)的類似作法，將環境部濃度圖，替代底圖中的白色部分。

## 程式設計

### IO

- 底圖
  - 檔名PM25_TOT_0001.png
  - 先以ncks切割PMs檔案，再將濃度設定為一低值。再藉由[m3nc2gif][m3nc2gif]程式所來產生。
  - png檔案的解析度與像素都較大(`(WxH = 611X740)`)。先將2個圖畫的像素畫在同一個畫面上，再用尺量測台灣地區範圍的大小比例，用[convert](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/imageMagicks/)先將底圖縮小:
```bash
  convert PM25_TOT_000.png -resize 432X524 PM25_TOT_0001.png`
```

- 濃度圖(前圖)
  - 由環境部網站下載
  - 如`wget https://airtw.moenv.gov.tw/ModelSimulate/20231001/output_AVPM25_20231001140000.png`
  - 圖檔之規則詳見[環保署實測數據圖檔下載並列][epa]
  - 因濃度圖只限陸地部分，其他圖面為黑色。此部分不需轉到新圖上。
- 結果檔
  - 以`cv2.imwrite`來輸出成png檔案

### 底圖空白部分的判斷

- 因壓縮圖面或其他不明原因，再縣市界附近可能會有些像素不是白色，而是略為白色的灰色。所以如果以純白色(`[255,255,255]`)來定義"空白部分"可能會太過低估其面積，而產生邊界上的間隙。
- 此處以`[200,200,200]`以上來定義"空白部分"。運用`np.where`找出其位置。

### 平移

- png像素的Y軸原點是圖面的上方，因此在試誤時要注意方向是相反的，如果要將圖面往南移動，需增加delta y的值
- 將相同解析度與像素的2個圖輸出在同一個png檔案後，量測平移所需要的距離，轉換成像素單位。
- 還會需要進一步微調
- 最後測試結果：將底圖的原點設在`[57,143]`(y,x)

### 排除不合併的空白位置

- 因為底圖範圍比較大，因此要排除比濃度圖還大的範圍。
- 濃度圖無資料部分：不能執行貼圖。

## 程式碼

```python
import numpy as np
import cv2
import os, sys
from PIL import Image

image=cv2.imread('output_AVPM25_20231001140000.png')
#change the black sea to white
idx2=np.where(np.sum(image,axis=2)==0)
image[idx2[0],idx2[1],:]=255
ny2,nx2,nz2=image.shape

#original resolution (WxH 611X740)
#convert PM25_TOT_000.png -resize 432X524 PM25_TOT_0001.png
imageFrame=cv2.imread('PM25_TOT_0001.png')
idx=np.where(np.sum(imageFrame[57:,143:,:],axis=2)>=200*3) #white content
ix2=[];iy2=[];ix=[];iy=[]
for i in range(len(idx[0])):
    if idx[0][i]<ny2 and idx[1][i]<nx2:
        if np.sum(image[idx[0][i],idx[1][i],:])==255*3:continue
        ix2.append(idx[1][i]+143)
        iy2.append(idx[0][i]+57)
        iy.append(idx[0][i])
        ix.append(idx[1][i])
imageFrame[iy2,ix2,:]=image[iy,ix,:]
cv2.imwrite("postEPA.png",imageFrame)
```

## 結果

![](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/utilities/Graphics/matplotlib/postEPA.png)

[m3nc2gif]: https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python/4.m3nc2gif/ "m3nc檔案轉GIF"
[epa]: https://sinotec2.github.io/Focus-on-Air-Quality/ForecastSystem/PostProcess/7.d03CF/#環保署實測數據圖檔下載並列 "環保署實測數據圖檔下載並列"