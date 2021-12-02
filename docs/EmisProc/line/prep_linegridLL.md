---
layout: default
title: "Prepare for LineS"
parent: "Biogenic Sources"
grand_parent: "Mobile Processing"
nav_order: 1
date:               
last_modified_date:   2021-12-02 11:08:53
---

# 移動源排放檔案之準備
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
- 由環保署移動源檔案讀取資料庫維度，改寫成矩陣形式。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[植物源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/biog/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，為此處之前處理。  

## 程式分段說明


## DataFrame整合
- 將逐月檔整合成一個大的DataFrame(`biogrid2019.csv`)、另存備有
```python
kuang@node03 /nas1/TEDS/teds11/biog
$ cat wrt_csv.py
from pandas import *

P='/nas1/TEDS/teds11/merg/bioemis.space/'
col=['UTME','UTMN','tnmhc','iso','mono','onmhc','mbo']
df=DataFrame({})
for m in range(1,13):
  mo='{:02d}'.format(m)
  dfT=read_csv(P+'bioemis.space.'+mo,header=None,delim_whitespace = True)
  dfT.columns=col
  dfT['mon']=[m for i in dfT.index]
  df=df.append(dfT,ignore_index=True)
df.set_index('UTME').to_csv('biogrid2019.csv')
```

## 檔案下載
- `fortran`程式：[bio2month-teds11.f](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/biog/bio2month-teds11.f)。

## Reference
