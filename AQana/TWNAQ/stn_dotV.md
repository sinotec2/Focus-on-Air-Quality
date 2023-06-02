---
layout: default
title: 依據Voronoi圖進行空間外插
parent: Taiwan AQ Analysis
grand_parent: AQ Data Analysis
last_modified_date: 2023-06-01 14:59:49
tags: python
---

# 以Voronoi圖進行環保署測站數據之空間外插
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

- 有關Voronoi圖的原理、製作方式以及結果詳見[空品測站之Voronoi圖][Voronoi]
- 在該次作業中，已將全台公版模式範圍之1x1網格點所應對應到的測站，進行了[Voronoi圖][Voronoi]的分配。
- 此處延續[鄉鎮區平均值計算(以接鄰為考量)][stn_dot]內外積之矩陣計算方式，擴大到1x1網格系統，以連接到[Voronoi圖][Voronoi]的成果。
- 目標：
  1. 填補沒有值的行政區域。
  2. 測試在大型矩陣中、矩陣內外積的效率。

## 程式差異

## 執行結果比較

### 計算各網格點的濃度

- 此一階段將[日均值計算][daymean]結果(`var`、維度依序為：`[測項、日期、測站]`)，與[Voronoi圖][Voronoi]的測站分配結果(`fac1`，維度依序為：`[測站、網格]`)，以內積方式進行相乘
- `fac1`之準備詳下，`var`之矩陣作法同[stn_dot][stn_dot]

```python
llv=pd.read_csv('/nas2/cmaqruns/2022fcst/fusion/Voronoi/gridLLvor.csv')
nxy=393*276
if len(llv)!=nxy:sys.exit('wrong grid matching')
all_stn=set(list(llv.AQID))
ns=len(all_stn)
seq=list(all_stn)
seq.sort()
seqn={seq[i]:i for i in range(ns)}
fac1=np.zeros(shape=(ns,nxy))
for t in range(nxy):
  i=llv.AQID[t]
  fac1[seqn[i],t]=1.
...
res1=np.ma.dot(var,fac1)
```

### 鄉鎮區範圍內網格濃度之平均

- 前階段結果(`res1`、維度為`[測項、日期、網格]`)，與鄉鎮區在各網格點內之分配(`fac2`)，維度為`[網格、鄉鎮區]`，進行內積計算。
- 過去這項作業是使用`pandas.pivot_table`來計算，此處因測項與時間等維度都較複雜，pandas雖然也有平行運算功能，但仍然較比`np.ma.dot`慢了許多。

```python
sw=set(llv.TOWNCODE)
nw=len(sw)
seq=list(sw)
seq.sort()
seqn={seq[i]:i for i in range(nw)}
fac2=np.zeros(shape=(nxy,nw))
for t in range(nw):
  a=llv.loc[llv.TOWNCODE==seq[t]]
  n=len(a)
  for i in a.index:
    fac2[i,t]=1./n

res=np.ma.dot(res1,fac2)
```

- 經測試，程式可以使用到master的12核心(total 20)、devp的64核心(total 100)進行平行計算。

## 處理結果比較

- hue color scale

|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-06-01-14-56-35.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-06-01-14-53-38.png)|
|:-:|:-:|
|stn_dot結果|stn_dotV結果|

- discrete color scale(參考[m3nc檔案轉GIF-浮動的濃度等級](../../utilities/Graphics/wrf-python/4.m3nc2gif.md#浮動的濃度等級))

|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-06-02-10-14-33.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-06-02-10-19-25.png)|![](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/attachments/2023-06-02-10-24-20.png)|
|:-:|:-:|:-:|
|stn_dot結果|stn_dotV結果|LGHAP2009結果|

## 程式下載

{% include download.html content="[stn_dotV.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/TWNAQ/stn_dotV.py)" %}

[Voronoi]: https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/Voronoi/ "空品測站之Voronoi圖"
[stn_dot]: https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/stn_dot/ "環保署測站數據鄉鎮區平均值之計算"
[daymean]: https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/daymean/ "環保署測站數據日均值之計算"