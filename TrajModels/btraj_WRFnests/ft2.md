---
layout: default
title: 正軌跡分析
nav_order: 7
parent: WRF三維軌跡分析
grand_parent: Trajectory Models
last_modified_date: 2022-11-17 09:09:30
---

# CWBWRF預報風場之正軌跡分析

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

- 正軌跡分析的用途焦點除了在污染源行為的預測之外，也可以引用預報風場，檢討煙流在未來風場中可能的走向。
- 原本設計[bt2.py][bt]時就已經將正/反軌跡的選擇設計成輸入引數之一，因此程式並沒有太大的差異，只是讀取風場數據的差異。
- 目前政府公開資訊中已經提供了中央氣象局15公里及3公里的WRF結果，垂直解析度雖然不是很充分，卻也足夠跨縣市、跨境的軌跡分析。 

## 程式設計

項目|[bt2.py][bt]|本程式[ft2.py][ft]|說明
:-:|:-:|:-:|-
WRF來源|自行執行結果|CWBWRF|預報場每日更新
巢狀網格層數|4|2|東亞與東南中國
網格間距(Km)|81/27/9/3|15/3|
垂直層數|40|11|
起始小時(Z)|0|6|

### 程式碼差異

```python
$ diff ft2.py bt2_DVP.py
25,26c25,26
<   iii=int(x//dx[2]+ncol[2]//2)
<   jjj=int(y//dx[2]+nrow[2]//2)
---
>   iii=int(x//dx[4]+ncol[4]//2)
>   jjj=int(y//dx[4]+nrow[4]//2)
42c42
<         jj=int((j-nrow[n]//2)*fac[n] +nrow[2]//2)
---
>         jj=int((j-nrow[n]//2)*fac[n] +nrow[4]//2)
44c44
<           ii=int((i-ncol[n]//2)*fac[n] +ncol[2]//2)
---
>           ii=int((i-ncol[n]//2)*fac[n] +ncol[4]//2)
74c74
<     for n in range(1,-1,-1):
---
>     for n in range(3,-1,-1):
119c119
<   fnames=['CWB_forecast/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in [1,3]]
---
>   fnames=['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]
191,193c191,193
< nrow.append(nrow[0]*5)
< ncol.append(ncol[0]*5)
< dx=[15000,3000,3000]
---
> nrow.append(nrow[0]*27)
> ncol.append(ncol[0]*27)
> dx=[81000,27000,9000,3000,3000]
195c195
< fac=[dx[n]//dx[2] for n in range(3)]
---
> fac=[dx[n]//dx[4] for n in range(5)]
197,199c197,199
< x_mesh = [(i-ncol[2]//2)*dx[2] for i in range(ncol[2])]
< y_mesh = [(j-nrow[2]//2)*dx[2] for j in range(nrow[2])]
< z_mesh = [k*dz for k in range(nlay[2])]
---
> x_mesh = [(i-ncol[4]//2)*dx[4] for i in range(ncol[4])]
> y_mesh = [(j-nrow[4]//2)*dx[4] for j in range(nrow[4])]
> z_mesh = [k*dz for k in range(nlay[4])]
201,204c201,204
< xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(2)]
< xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(2)]
< ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(2)]
< ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(2)]
---
> xmin=[-dx[i]*(int(ncol[i]/2)) for i in range(4)]
> xmax=[ dx[i]*(int(ncol[i]/2)) for i in range(4)]
> ymin=[-dx[i]*(int(nrow[i]/2)) for i in range(4)]
> ymax=[ dx[i]*(int(nrow[i]/2)) for i in range(4)]
206c206
< for n in range(2):
---
> for n in range(4):
236c236
<   if t1==nt[0] or t1<0:
---
>   if t1==24 or t1<0:
242c242
<   uvwg=np.zeros(shape=(3,2,nlay[2],nrow[2],ncol[2],))
---
>   uvwg=np.zeros(shape=(3,2,nlay[4],nrow[4],ncol[4],))
```

## 程式下載

{% include download.html content="[CWBWRF預報風場之正軌跡分析程式][ft]" %}

[bt]: <https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/btraj_WRFnests/bt2_DVP/> "三維反軌跡線之計算"
[ft]: <https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/btraj_WRFnests/ft2.py> "CWBWRF預報風場之正軌跡分析程式"
