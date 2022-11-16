---
layout: default
title: acc_prob.py程式說明
nav_order: 5
parent: WRF三維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-16 10:33:28
---

# acc_prob.py程式說明

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

- 從軌跡點L.csv檔案，統計網格通過機率，以便進行繪圖

## 程式說明

### IO

- 引數：
  - `SEA`：季節
  - `Li`：叢集編號(自0開始)
- 輸入檔案：
  - fnames.txt(檔案路徑名稱之listing)
  - tmplateD1_27km.nc：存放通過機率的`nc`檔案模板
  - lab.csv：叢集代表軌跡線的標籤與日期對照
- 輸出檔案：
  - probJ.nc
  - 單位：crossing time/total time

### 時間迴圈

- 針對逐時反軌跡線檔案逐一處理
- 檔案按照年月(`path+'/trj_results'+ym+`)目錄放置
- 檔案名稱含有測站名稱以及時間(`trjzhongshan'+str(d)+'L.csv'`)

```python
  for d in ymdhL:
    ym=str(d)[2:6]
    fname=path+'/trj_results'+ym+'/trjzhongshan'+str(d)+'L.csv'
    df=read_csv(fname)
    if len(df)==0:continue
```
- 計算網格位置標籤(`JI`)
- 以`pivot_table`計算同一網格內的點數、一點15秒，如此可以計算出網格內的停留小時數(`pv['hr']`)


```python
    x=np.array(df.TWD97_x)-Xcent
    y=np.array(df.TWD97_y)-Ycent
    ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
    iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
    df['JI']=[j*tex+i for i,j in zip(ix,iy)]
    pv=pivot_table(df,index='JI',values='TWD97_x',aggfunc='count').reset_index()
    pv['hr']=np.array(pv.TWD97_x)*15./3600. #in unit of hr/total hr
```

- 拆解`JI`，並將結果累加在`nc`檔案內

```python
    pv['I']=[ji%tex for ji in pv.JI]
    pv['J']=[ji//tex for ji in pv.JI]
    for i in range(len(pv)):
      nc.variables[v][0,0,pv.J[i],pv.I[i]]+=pv.hr[i]
```

## [NCL](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/NCL)繪圖

- 2017~2020年1~3月測站三維反軌跡機器學習之結果
  - 圖中線條為代表性軌跡
  - 底圖為該叢集所有軌跡在網格經過時間的總合(小時)，以該叢集所有軌跡數(小時)為基準的比值。

| ![prob_traj.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/prob_traj.png)|
|:-:|
| <b>反軌跡線通過網格機率分析結果</b>|

## 程式下載

- {% include download.html content="三維軌跡線之網格通過機率分析程式：[acc_prob.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/acc_prob.py)" %}
