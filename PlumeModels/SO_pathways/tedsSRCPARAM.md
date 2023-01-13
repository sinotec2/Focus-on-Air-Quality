---
layout: default
title: 臺灣地區既有點源排放資訊
parent: SO Pathways
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-03-15 10:46:51
tags: plume_model ptse
tags: CGI_Pythons plume_model
---
# 臺灣地區既有點源排放資訊
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
- 雖然ISC/AERMOD的設計是為新污染源的審核程序(New Source Review、我國的許可制度)，然而污染排放條件的設定，如果有背景其他既有污染源的參照，會減少很多嘗試錯誤的機會。
  - 例如在網格模式點源排放前處理過程中的[品管程式](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/#確認資料庫的正確性)
- 除了數據品質的考量之外，背景污染源會不會造成環境的污染，也是值得公眾關切、測試、檢討的環保課題。
- 此處針對行政院環保署對外提供的TEDS(Taiwan Emission Data Set)數據庫，將其煙道數據予以轉檔、貼在[uMap](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/UMAP/)上，除方便查詢、也可做為煙流模式模擬的準備。
- 煙流模式所需煙道數據項目(*傾斜字體*表示使用者給定數據，其餘為KEYWORDS)：
  - SO LOCATION *CP_NO* POINT *TWD97-X* *TWD97-Y* *elevation*  
  - SO SRCPARAM *CP_NO* POINT *EM* *HGT* *TMP* *DIA* *VEL*
- 由於TEDS資料庫中絕大多數工廠只有一筆座標數據，但可能有許多座煙囪(`CP_NO=C_NO+NO_S`)，此處即以工廠(C_NO)為單位進行貼圖，彙整所有煙道數據在同一表單中。

## [uMap](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/GIS/UMAP/)成果
- TEDS 點源位置及煙囪條件
  - [teds10](https://umap.openstreetmap.fr/zh/map/teds10-point-data-pm25_594438#7/24.062/120.822)
  - [teds11](https://umap.openstreetmap.fr/zh/map/teds11-point-data-pm25_728979#8/24.172/120.086)

## point_qc.py
- 由於地圖系統接受的是經緯度座標，此處直接引用WGS版本之TEDS數據不另轉換。而LOCATION要用的TWD97數據，也是直接引用TEDS原數據。
- 此處僅針對排放量、NO_S、煙囪高度、流速等項目進行篩選或修改
- 煙流模式並不一定需要排放量的時間變化特性，但需要有總時數來進行單位轉換，因此DY1、HD1、WY1等數據全都不需要，只留下HY1。
- 針對煙道CP_NO進行整併(pivot_table)
  - 煙道參數、年運轉時數、與位置，採平均值
  - 排放量：採總計
- 由於點源數據還有其他運用，先將其儲存。

```python
kuang@114-32-164-198 /Users/TEDS/teds11/ptse
$ cat point_qc.py
from pandas import *
import numpy as np
df1=read_csv('point_NoBig5.csv',encoding='big5')
df2=read_csv('point_NoBig5WGS.csv',encoding='big5')
df2.loc[df2.NO_S.map(lambda x:type(x)==float),'NO_S']='Y000'
df2['CP_NO']=[i+j for i,j in zip(list(df2.C_NO),list(df2.NO_S))]
df2['LAT']=df2.UTM_N
df2['LON']=df2.UTM_E
df2.UTM_N=df1.UTM_N
df2.UTM_E=df1.UTM_E
cole=[i for i in df2.columns if 'EMI' in i]
df2['SUM_EMI']=0
for i in cole:
  a=np.array(df2.SUM_EMI)+np.array(df2[i])
  df2.SUM_EMI=a
df2qc=df2.loc[(df2.SUM_EMI>0) &(df2.HEI>0) & (df2.VEL>0)].reset_index(drop=True)
cole=['CO_EMI', 'NMHC_EMI', 'NOX_EMI', 'PM25_EMI', 'PM_EMI', 'SOX_EMI']
hdtv=[ 'HEI', 'DIA', 'TEMP', 'VEL']
tims=[ 'DY1', 'HD1', 'HY1']
loca=['LAT','LON','UTM_E','UTM_N']
df2qc['DY1']=[i*j for i,j in zip(list(df2qc.DW1),list(df2qc.WY1))]
df2qc['HY1']=[i*j for i,j in zip(list(df2qc.HD1),list(df2qc.DY1))]
pv1=pivot_table(df2qc,index='CP_NO',values=hdtv+tims+loca,aggfunc=np.mean).reset_index()
pv2=pivot_table(df2qc,index='CP_NO',values=cole,aggfunc=np.sum).reset_index()
pv=merge(pv1,pv2,on='CP_NO')
pv.loc[pv.CP_NO.map(lambda x:'U95A4209P00' in x),'HEI']=36
pv.set_index('CP_NO').to_csv('point_QCteds11.csv')
```

## SO Pathway內容之準備
- uMap雖然可以接受csv檔案，但是KML檔案還可以有別的用途，且經由[csv2kml.py]()即可轉換，因此以下將TEDS數據簡化成經緯度、名稱及標籤4個欄位。
- pivot_table的合併函數(aggfunc)中並沒有簡單的字串續接指另，借用lambda函數，可以將所有字串接續成一個大字串
  - `lambda x: ' '.join(str(v) for v in x`
  - Enrico Bergamini, [Creating non-numeric pivot tables with Python Pandas](https://medium.com/@enricobergamini/creating-non-numeric-pivot-tables-with-python-pandas-7aa9dfd788a7), Nov 8, 2016
```python
kuang@114-32-164-198 /Users/TEDS/teds11/ptse
$ cat tedsSRCPARAM.py
from pandas import *
import os
import numpy as np
pv=read_csv('point_QCteds11.csv')
pv=pv.loc[pv.HY1>0].reset_index(drop=True)
pv.TEMP+=273
pv.PM25_EMI*=1000.*1000./3600/pv.HY1
pv.HEI=[round(i,1) for i in pv.HEI]
pv['STR']=['SO LOCATION {:s} POINT {:.0f} {:.0f} 0. SO SRCPARAM {:s} {:f} {:.1f} {:3.1f} {:3.1f} {:3.1f} '\
.format(c,x,y,c,e,h,t,d,v) for c,x,y,e,h,t,d,v in zip(list(pv.CP_NO),list(pv.UTM_E),list(pv.UTM_N),list(pv.PM25_EMI),\
list(pv.HEI),list(pv.TEMP),list(pv.DIA),list(pv.VEL))]
pv['C_NO']=[i[:8] for i in pv.CP_NO]
df1=pivot_table(pv,index='C_NO',values=['LON','LAT'],aggfunc=np.mean).reset_index()
df2=pivot_table(pv,index='C_NO',values='STR',aggfunc=lambda x: ' '.join(str(v) for v in x)).reset_index()
pv=merge(df1,df2,on='C_NO')
pv.STR=[i.replace('SO ','\nSO ') for i in pv.STR]
col=['LON','LAT','C_NO','STR']
pv[col].set_index('LON').to_csv('tedsSRCPARAM.csv')
os.system('/opt/local/bin/csv2kml.py -f tedsSRCPARAM.csv -n N -g LL')
```