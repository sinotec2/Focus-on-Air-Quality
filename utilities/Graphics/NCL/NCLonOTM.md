---
layout: default
title:  NCL貼在OTM底圖上
parent: NCL
grand_parent: Graphics
last_modified_date: 2022-06-07 20:21:17
tags: NCL graphics plume_model OpenTopoMap
---

# NCL貼在OTM底圖上 NCLonOTM

{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

## 背景

- NCL等濃度圖檔貼在openTopo底圖([NCLonOTM][1])，是一個品質較高、又不涉及底圖版權的做法。
- 此處並不是NCL程式，而是NCL產生圖檔的後處理加工。
- OpenTopoMap：開放地形圖[官網](https://opentopomap.org)、[wiki](https://wiki.openstreetmap.org/wiki/OpenTopoMap)

## NCLonOTM.py

- 這支程式是獨立版，令有包裝前後處理的cgi版本，[詳下](#NCLonOTM-cgi.py)說明。

### 程式下載

{% include download.html content="[NCLonOTM.py][1]" %}

### I/O

- 輸入檔
  1. tmp_cn.png，由[PLT_cn.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/PLT_cn.ncl)所產生（詳見[煙流模式結果繪製等值線圖](../NCL/PLT_cn))。
  2. fitted.png：OTM/OSM底圖，由[tiles_to_tiffFit.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/tiles_to_tiffFit.py)，同樣也是在[NCLonOTM-cgi.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/NCLonOTM-cgi.py)
- 輸出檔：NCLonOTM.png

### 讀取等值線圖檔

- 由png檔案讀取寬度、高度之範圍備用

```python
image=cv2.imread('tmp_cn.png')
ny,nx,nz=image.shape

#locate the frame of contour plot
nwidth=np.array([len(np.where(image[j,:,:]!=255)[0]) for j in range(ny)])
nheight=np.array([len(np.where(image[:,i,:]!=255)[0]) for i in range(nx)])
wh={'j':'nwidth','i':'nheight'}
nxy={'j':'ny','i':'nx'}
```

### 求取畫框的起訖與尺寸

```python
for ij in wh:
  n=nxy[ij]
  exec('id1=int(np.mean(np.where('+wh[ij]+'>=max('+wh[ij]+')-2)[0]))')
  exec('id2=int(np.mean(np.where('+wh[ij]+'==max(['+wh[ij]+'[i] for i in range('+n+') if abs(i-id1) > 2]))))')
  if id1==id2:
     exec('id1=np.min(np.where('+wh[ij]+'>=max('+wh[ij]+')-2)[0])')  
     exec('id2=np.max(np.where('+wh[ij]+'>=max('+wh[ij]+')-2)[0])')  
  exec(ij+'0=min([id1,id2])')
  exec(ij+'1=max([id1,id2])')
size = (j1-j0,i1-i0)
```

### 將畫框內的實線加黑

- NCL等值線有可能會出現灰階，在貼上底圖時將會出錯，需先全部轉成黑色。

```python
#darken the lines inside of the frame
image3=image[:]
boo=(image[:,:,0]==image[:,:,1]) & (image[:,:,1]==image[:,:,2])& (image[:,:,2]!=255)
idx=np.where(boo)
idx0=np.array([idx[0][i] for i in range(len(idx[0])) if idx[0][i]>j0 and idx[0][i]<j1 and idx[1][i]>i0 and idx[1][i]<i1])
idx1=np.array([idx[1][i] for i in range(len(idx[0])) if idx[0][i]>j0 and idx[0][i]<j1 and idx[1][i]>i0 and idx[1][i]<i1])
if len(idx0)>0 and len(idx1)>0:image3[idx0,idx1,:]=0
```

### 讀取OTM底圖

- 如果底圖的解析度太低，程式會停下來
- 壓縮底圖的尺寸，以符合前述圖框。

```python
#resize (alignment the resolutions)
image2=cv2.imread('fitted.png')
ny2,nx2,nz=image2.shape
if ny2<size[0] and size[0]/ny2>1.3 :sys.exit('make a more detail basemap')
rate=(ny2/size[0],nx2/size[1])
size2=(int(rate[0]*ny),int(rate[1]*nx))
im_resized = cv2.resize(image3,size2, interpolation=cv2.INTER_CUBIC)
image3=np.array(im_resized)
j0,i0=int(j0*rate[0]),int(i0*rate[1])
```

### 貼上底圖

- 將沒有數據的位置，以OTM/OSM圖檔內容取代

```python
#replace the nodata location with OSM plot
for j in range(j0,j0+ny2):
  for i in range(i0,i0+nx2):
    if (image3[j,i,:]==0).all():continue  
#    if sum(image3[j,i,:])>=200+255:
    image3[j,i,:]=image2[j-j0,i-i0,:]
cv2.imwrite("NCLonOTM.png",image3)
```

[1]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/NCLonOTM.py "NCLonOTM.py"