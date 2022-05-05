---
layout: default
title:  由圖面顏色讀取濃度值
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-02-08 16:05:00
---

# 由圖面顏色讀取濃度值
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


## rdpng3.py 程式說明
### 程式IO
- 引數：png檔案名稱
- legend.png：NullSchool PM<sub>2.5</sub>色標

| ![legend.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/legend.png) 

- 結果檔案：dict.grd

### 程式碼
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/post/rdpng3.py)

## Results

| ![17101000.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/17101000.png) | ![1710PM2_5.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/1710PM2_5.png) |
|:--:|:--:|
| <b>2017/10/10 NullSchool之PM<sub>2.5</sub>圖面，無單位 </b>|<b>  rdpng解讀結果。單位log<sub>10</sub>&mu;g/M<sup>3</sup></b>|

## Reference
