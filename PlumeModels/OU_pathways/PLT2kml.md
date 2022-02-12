---
layout: default
title: PLOTFILE to KML
parent: OU Pathways
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-02-12 19:52:38
---
# PLOTFILE to KML
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
- PLOTFILE指令將會產生所有接受點(網格及離散點)的濃度結果、以及接受點的高程等訊息。
- 除了可以使用SURFER等軟體進行等值圖的繪製之外，此處將PLOTFILE轉成KML檔案，以運用快速便捷的網路地圖貼圖功能。
  - 使用[legacycontour._cntr](https://github.com/matplotlib/legacycontour)模組
  - 安裝：可動態連結github，或下載完整原始碼再`python setup.py install`
- KML檔案之寫出，可以參考[等值圖KML檔之撰寫](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/wr_kml/)

## 讀取PLOTFILE
-  

```python
# read the iscst result plot file, must be in TWD97-m system, with 8 lines as header
with open(fname, 'r') as f:
  g = [line for line in f]
#description txt is read from the third line
desc = ' '
if g[0][0:3] in ['* A','* I']:
  desc = g[:3]
  g = g[8:]
lg = len(g)
x, y, c = (np.array([float(i.split()[j]) for i in g]) for j in range(3))
```